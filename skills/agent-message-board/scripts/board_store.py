"""Small, local SQLite message board shared by agent CLI entry points."""

import argparse
from contextlib import closing
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
import time


SCHEMA_VERSION = 2


class SetupRequired(ValueError):
    pass


def config_path():
    config_home = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return config_home.expanduser().resolve() / "agent-message-board/config.json"


def database_path():
    path = config_path()
    if not path.is_file():
        raise SetupRequired("Ask the user where to create or access the board database, then run "
                            "setup_agent_message_board.py --database <user-chosen-absolute-path>.")
    configuration = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(configuration, dict) or configuration.get("version") != 1:
        raise ValueError(f"Invalid board configuration: {path}")
    value = configuration.get("database")
    if not isinstance(value, str) or not value or not Path(value).is_absolute():
        raise ValueError(f"Board configuration needs an absolute database path: {path}")
    return Path(value)


def connect(*, create=False, path=None):
    path = database_path() if path is None else path
    if create:
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    elif not path.is_file():
        raise SetupRequired(f"Configured database is missing at {path}. Ask the user whether to "
                            "recreate it there or choose an existing board; do not create it automatically.")
    mode = "rwc" if create else "rw"
    connection = sqlite3.connect(path.as_uri() + "?mode=" + mode, uri=True, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def check_schema(connection):
    version = connection.execute("PRAGMA user_version").fetchone()[0]
    if version == 1:
        raise ValueError("This board needs a username upgrade. Run setup_agent_message_board.py "
                         "--database with the already configured database path.")
    if version != SCHEMA_VERSION:
        raise ValueError(f"Unsupported board schema {version}; expected {SCHEMA_VERSION}.")
    # user_version is also used by other SQLite applications.
    connection.execute("SELECT id, thread_id, title, body, username, project, created_at FROM posts LIMIT 0")
    connection.execute("SELECT rowid, title, body FROM posts_fts LIMIT 0")


def save_config(path):
    destination = config_path()
    destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=destination.parent,
                                         delete=False) as stream:
            temporary = Path(stream.name)
            json.dump({"version": 1, "database": str(path)}, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def status():
    if not config_path().is_file():
        return {"configured": False, "config": str(config_path()),
                "next_step": "Ask the user for the database location before setup, search, or posting."}
    path = database_path()
    with closing(connect()) as connection:
        check_schema(connection)
    return {"configured": True, "config": str(config_path()), "database": str(path)}


def setup(database):
    path = Path(database).expanduser()
    if not path.is_absolute():
        raise ValueError("Provide the absolute database file path chosen by the user.")
    path = path.resolve()
    with closing(connect(create=True, path=path)) as connection:
        # Changing journal mode can return BUSY immediately despite the connection
        # timeout when several first-time setup processes open the same file.
        deadline = time.monotonic() + 10
        while True:
            try:
                connection.execute("PRAGMA journal_mode = WAL")
                break
            except sqlite3.OperationalError as error:
                if str(error) not in ("database is locked", "database is busy") or time.monotonic() >= deadline:
                    raise
                time.sleep(0.05)
        try:
            connection.execute("BEGIN IMMEDIATE")
            version = connection.execute("PRAGMA user_version").fetchone()[0]
            if version not in (0, 1, SCHEMA_VERSION):
                raise ValueError(f"Unsupported board schema {version}; database left intact.")
            if version == 0:
                if connection.execute(
                    "SELECT name FROM sqlite_master WHERE name NOT LIKE 'sqlite_%' LIMIT 1"
                ).fetchone():
                    raise ValueError("The selected database contains other data; choose a board database.")
                connection.execute("""
                    CREATE TABLE posts (
                        id INTEGER PRIMARY KEY,
                        thread_id INTEGER REFERENCES posts(id),
                        title TEXT NOT NULL,
                        body TEXT NOT NULL,
                        username TEXT NOT NULL,
                        project TEXT,
                        created_at TEXT NOT NULL,
                        CHECK ((thread_id IS NULL AND length(title) > 0)
                            OR (thread_id IS NOT NULL AND title = ''))
                    )
                """)
                connection.execute("CREATE INDEX posts_thread ON posts(thread_id, id)")
                connection.execute("CREATE INDEX posts_project ON posts(project)")
                connection.execute("""
                    CREATE VIRTUAL TABLE posts_fts USING fts5(
                        title, body, content='posts', content_rowid='id'
                    )
                """)
                connection.execute("""
                    CREATE TRIGGER posts_insert AFTER INSERT ON posts BEGIN
                        INSERT INTO posts_fts(rowid, title, body)
                        VALUES (new.id, new.title, new.body);
                    END
                """)
                connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
            elif version == 1:
                # Preserve conversation attribution for old posts without retaining
                # separate model/session fields. IDs keep legacy names distinct.
                authors = connection.execute(
                    "SELECT id, agent, session FROM posts ORDER BY id"
                ).fetchall()
                connection.execute("ALTER TABLE posts RENAME COLUMN agent TO username")
                names = {}
                for author in authors:
                    username = names.setdefault(
                        (author["agent"], author["session"]), f"LegacyMember_{author['id']}"
                    )
                    connection.execute(
                        "UPDATE posts SET username = ? WHERE id = ?", (username, author["id"]),
                    )
                connection.execute("ALTER TABLE posts DROP COLUMN session")
                connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
            check_schema(connection)
            connection.commit()
        except Exception:
            connection.rollback()
            raise
    save_config(path)
    return {"database": str(path), "config": str(config_path()), "schema_version": SCHEMA_VERSION}


def clean_label(value, label, maximum=200):
    if not value or not value.strip():
        raise ValueError(f"{label} must not be empty.")
    value = value.strip()
    if len(value) > maximum or any(ord(char) < 32 for char in value):
        raise ValueError(f"{label} must be a single line of at most {maximum} characters.")
    return value


def post(*, title=None, thread_id=None, body, username, project=None):
    username = clean_label(username, "Username", maximum=64)
    if not body.strip():
        raise ValueError("Message body must not be empty.")
    if len(body.encode("utf-8")) > 256_000:
        raise ValueError("Message body must be at most 256,000 UTF-8 bytes.")
    if thread_id is None:
        title = clean_label(title, "Title")
        project = clean_label(project, "Project") if project is not None else None
    elif title is not None or project is not None:
        raise ValueError("Replies inherit the thread title and project; omit --title and --project.")
    timestamp = datetime.now(timezone.utc).isoformat()
    with closing(connect()) as connection, connection:
        check_schema(connection)
        if thread_id is not None:
            root = connection.execute(
                "SELECT project FROM posts WHERE id = ? AND thread_id IS NULL", (thread_id,)
            ).fetchone()
            if root is None:
                raise ValueError(f"Thread {thread_id} does not exist. Use a thread ID, not a reply ID.")
            project, title = root["project"], ""
        cursor = connection.execute(
            """INSERT INTO posts(thread_id, title, body, username, project, created_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (thread_id, title, body, username, project, timestamp),
        )
        post_id = cursor.lastrowid
    return {"post_id": post_id, "thread_id": thread_id or post_id,
            "username": username, "project": project, "created_at": timestamp}


def search(query, *, project=None, limit=10, offset=0):
    # Literal words, OR'ed: agent queries cannot accidentally become FTS operators.
    terms = list(dict.fromkeys(re.findall(r"\w+", query, flags=re.UNICODE)))
    if not terms:
        raise ValueError("Search needs at least one word or number.")
    if len(terms) > 64:
        raise ValueError("Search accepts at most 64 distinct terms; use a short query.")
    expression = " OR ".join('"' + term + '"' for term in terms)
    with closing(connect()) as connection:
        check_schema(connection)
        rows = connection.execute(
            """SELECT p.id AS post_id, COALESCE(p.thread_id, p.id) AS thread_id,
                      root.title, p.username, p.project, p.created_at,
                      snippet(posts_fts, -1, '', '', ' … ', 40) AS excerpt
               FROM posts_fts JOIN posts p ON p.id = posts_fts.rowid
               JOIN posts root ON root.id = COALESCE(p.thread_id, p.id)
               WHERE posts_fts MATCH ? AND (? IS NULL OR p.project = ? OR p.project IS NULL)
               ORDER BY bm25(posts_fts, 5.0, 1.0), p.id DESC LIMIT ? OFFSET ?""",
            (expression, project, project, limit + 1, offset),
        ).fetchall()
    return {"matches": [dict(row) for row in rows[:limit]],
            "next_offset": offset + limit if len(rows) > limit else None}


def read_thread(thread_id, *, limit=10, offset=0):
    with closing(connect()) as connection, connection:
        check_schema(connection)
        connection.execute("BEGIN")
        root = connection.execute(
            "SELECT * FROM posts WHERE id = ? AND thread_id IS NULL", (thread_id,)
        ).fetchone()
        if root is None:
            raise ValueError(f"Thread {thread_id} does not exist.")
        replies = connection.execute(
            "SELECT * FROM posts WHERE thread_id = ? ORDER BY id LIMIT ? OFFSET ?",
            (thread_id, limit + 1, offset),
        ).fetchall()
    return {"thread": dict(root), "replies": [dict(row) for row in replies[:limit]],
            "next_offset": offset + limit if len(replies) > limit else None}


def positive_integer(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be positive")
    return number


def page_limit(value):
    number = positive_integer(value)
    if number > 100:
        raise argparse.ArgumentTypeError("must be at most 100")
    return number


def page_offset(value):
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be nonnegative")
    return number


def run(action):
    try:
        result = action()
    except SetupRequired as error:
        print(json.dumps({"error": str(error), "code": "setup_required"}), file=sys.stderr)
        return 2
    except (ValueError, OSError, sqlite3.Error) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
