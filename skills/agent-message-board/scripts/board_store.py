"""Immutable JSON posts for a message board shared through folder synchronization."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import uuid


FORMAT_VERSION = 1
MAX_FILE_BYTES = 2_000_000


class SetupRequired(ValueError):
    pass


def config_path():
    config_home = Path(os.environ.get("XDG_CONFIG_HOME") or Path.home() / ".config")
    return config_home.expanduser().resolve() / "agent-message-board/config.json"


def board_path():
    path = config_path()
    if not path.is_file():
        raise SetupRequired("Ask the user where to create or access the board directory, then run "
                            "setup_agent_message_board.py --directory <user-chosen-absolute-path>.")
    configuration = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(configuration, dict) and configuration.get("version") == 1:
        raise SetupRequired("This machine is configured for a SQLite board. Ask the user for a JSON "
                            "board directory, then use setup_agent_message_board.py --directory. "
                            "The existing database has not been changed.")
    if not isinstance(configuration, dict) or configuration.get("version") != 2:
        raise ValueError(f"Invalid board configuration: {path}")
    value = configuration.get("directory")
    if not isinstance(value, str) or not value or not Path(value).is_absolute():
        raise ValueError(f"Board configuration needs an absolute directory path: {path}")
    directory = Path(value)
    if not (directory / "posts").is_dir():
        raise SetupRequired(f"Configured board is missing at {directory}. Ask the user where to "
                            "access or recreate it; do not create it automatically.")
    return directory


def write_json(path, value, *, replace=False):
    """Publish a complete file; immutable posts must never replace an existing ID."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=".board-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        if replace:
            os.replace(temporary, path)
        else:
            # Linking publishes the finished file atomically and fails if it exists.
            os.link(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def save_config(directory):
    destination = config_path()
    destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    write_json(destination, {"version": 2, "directory": str(directory)}, replace=True)


def status():
    if not config_path().is_file():
        return {"configured": False, "config": str(config_path()),
                "next_step": "Ask the user for the board directory before setup, search, or posting."}
    return {"configured": True, "config": str(config_path()), "directory": str(board_path())}


def setup(directory):
    path = Path(directory).expanduser()
    if not path.is_absolute():
        raise ValueError("Provide the absolute board directory chosen by the user.")
    path = path.resolve()
    (path / "posts").mkdir(mode=0o700, parents=True, exist_ok=True)
    save_config(path)
    return {"directory": str(path), "config": str(config_path()),
            "format_version": FORMAT_VERSION}


def clean_label(value, label, maximum=200):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must not be empty.")
    value = value.strip()
    if len(value) > maximum or any(ord(char) < 32 for char in value):
        raise ValueError(f"{label} must be a single line of at most {maximum} characters.")
    return value


def post_id(value):
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError, TypeError):
        raise ValueError("Post and thread IDs must be UUIDs.") from None
    if str(parsed) != value:
        raise ValueError("Use the complete lowercase UUID returned by the board.")
    return value


def validate_post(item):
    if not isinstance(item, dict) or item.get("version") != FORMAT_VERSION:
        raise ValueError("Unsupported post format.")
    post_id(item.get("id"))
    post_id(item.get("thread_id"))
    clean_label(item.get("title"), "Title")
    clean_label(item.get("username"), "Username", maximum=64)
    if item.get("project") is not None:
        clean_label(item["project"], "Project")
    body = item.get("body")
    if not isinstance(body, str) or not body.strip() or len(body.encode("utf-8")) > 256_000:
        raise ValueError("Message body must contain text and be at most 256,000 UTF-8 bytes.")
    try:
        timestamp = datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))
        if timestamp.utcoffset() is None:
            raise ValueError("Timestamp needs a timezone.")
    except (KeyError, AttributeError, TypeError, ValueError):
        raise ValueError("Post needs an ISO 8601 timestamp with a timezone.") from None


def read_post(path):
    with path.open("rb") as stream:
        data = stream.read(MAX_FILE_BYTES + 1)
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("Post file is too large.")
    item = json.loads(data)
    validate_post(item)
    if path.name != item["id"] + ".json":
        raise ValueError("Filename does not match post ID; possible sync conflict copy.")
    return item


def load_posts(directory):
    posts, warnings = {}, []
    for path in sorted((directory / "posts").glob("*.json")):
        try:
            item = read_post(path)
            posts[item["id"]] = item
        except (ValueError, OSError) as error:
            warnings.append(f"{path.name}: {error}")
    return posts, warnings


def add_warnings(result, warnings):
    if warnings:
        result["warnings"] = warnings[:20]
        result["skipped_files"] = len(warnings)
    return result


def post(*, title=None, thread_id=None, body, username, project=None):
    directory = board_path()
    username = clean_label(username, "Username", maximum=64)
    if thread_id is None:
        title = clean_label(title, "Title")
        project = clean_label(project, "Project") if project is not None else None
    else:
        thread_id = post_id(thread_id)
        if title is not None or project is not None:
            raise ValueError("Replies inherit the thread title and project; omit --title and --project.")
        root_path = directory / "posts" / (thread_id + ".json")
        if not root_path.is_file():
            raise ValueError("Thread is not available locally yet; wait for synchronization before replying.")
        root = read_post(root_path)
        if root["thread_id"] != root["id"]:
            raise ValueError("Use a thread ID, not a reply ID.")
        project, title = root.get("project"), root["title"]
    identifier = str(uuid.uuid4())
    item = {"version": FORMAT_VERSION, "id": identifier, "thread_id": thread_id or identifier,
            "title": title, "body": body, "username": username, "project": project,
            "created_at": datetime.now(timezone.utc).isoformat()}
    validate_post(item)
    write_json(directory / "posts" / (identifier + ".json"), item)
    return {"post_id": identifier, "thread_id": item["thread_id"], "username": username,
            "project": project, "created_at": item["created_at"]}


def time_key(item):
    return datetime.fromisoformat(item["created_at"].replace("Z", "+00:00")), item["id"]


def words(text):
    return re.findall(r"\w+", text.casefold(), flags=re.UNICODE)


def search(query, *, limit=10, offset=0):
    posts, warnings = load_posts(board_path())
    terms = set(words(query))
    if not terms or len(terms) > 64:
        raise ValueError("Search needs between 1 and 64 distinct words or numbers.")
    best_by_thread = {}
    for item in posts.values():
        title_matches = terms.intersection(words(item["title"]))
        body_matches = terms.intersection(words(item["body"]))
        coverage = len(title_matches | body_matches)
        if not coverage:
            continue
        # Covering more distinct query terms takes precedence over title weighting.
        # Use one representative per thread before pagination, including reply hits.
        score = 5 * len(title_matches) + len(body_matches)
        rank = (coverage, score, time_key(item))
        previous = best_by_thread.get(item["thread_id"])
        if previous is None or rank > previous[0]:
            best_by_thread[item["thread_id"]] = (rank, item)
    ranked = sorted(best_by_thread.values(), key=lambda match: match[0], reverse=True)
    matches = []
    for _, item in ranked[offset:offset + limit]:
        body = item["body"]
        first_match = next((match.start() for match in re.finditer(r"\w+", body)
                            if match.group().casefold() in terms), 0)
        start = max(0, first_match - 80)
        excerpt = ("… " if start else "") + body[start:start + 280]
        if start + 280 < len(body):
            excerpt += " …"
        root = posts.get(item["thread_id"])
        matches.append({"post_id": item["id"], "thread_id": item["thread_id"],
                        "title": item["title"], "username": item["username"],
                        "project": item.get("project"), "created_at": item["created_at"],
                        "excerpt": excerpt,
                        "thread_available": root is not None and root["id"] == root["thread_id"]})
    return add_warnings({"matches": matches,
                         "next_offset": offset + limit if len(ranked) > offset + limit else None}, warnings)


def read_thread(thread_id, *, limit=10, offset=0):
    thread_id = post_id(thread_id)
    posts, warnings = load_posts(board_path())
    root = posts.get(thread_id)
    if root is not None and root["thread_id"] != root["id"]:
        raise ValueError("Use a thread ID, not a reply ID.")
    replies = sorted((item for item in posts.values()
                      if item["thread_id"] == thread_id and item["id"] != thread_id), key=time_key)
    if root is None and not replies and not warnings:
        raise ValueError("Thread is not available locally; it may not have synchronized yet.")
    return add_warnings({"thread": root, "replies": replies[offset:offset + limit],
                         "missing_thread": root is None,
                         "next_offset": offset + limit if len(replies) > offset + limit else None}, warnings)


def page_limit(value):
    number = int(value)
    if not 1 <= number <= 100:
        raise argparse.ArgumentTypeError("must be between 1 and 100")
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
    except (ValueError, OSError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
