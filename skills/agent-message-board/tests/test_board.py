"""Exercise public scripts with isolated configuration and separate processes."""

from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


class BoardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.database = Path(self.temp.name) / "chosen board/board.sqlite3"
        self.config_home = Path(self.temp.name) / "config"
        self.environment = dict(os.environ, XDG_CONFIG_HOME=str(self.config_home),
                                PYTHONDONTWRITEBYTECODE="1")

    def invoke(self, script, *arguments, success=True, input=None, environment=None):
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / script), *map(str, arguments)],
            env=environment or self.environment, input=input, text=True,
            capture_output=True, timeout=20, cwd=self.temp.name,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            return json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(result.stderr)
        self.assertEqual(result.stdout, "")
        return result

    def setup_board(self):
        return self.invoke("setup_agent_message_board.py", "--database", self.database)

    def post(self, title="Database setup", body="Use a local database.", username="MapleMaker_a7c92f", **options):
        arguments = ["--username", username, "--title", title, "--body", body]
        for key, value in options.items():
            arguments.extend(["--" + key, value])
        return self.invoke("post_to_agent_message_board.py", *arguments)

    def search(self, query, *arguments):
        return self.invoke("search_agent_message_board.py", "--query", query, *arguments)

    def test_first_use_requires_location_and_creates_nothing(self):
        status = self.invoke("setup_agent_message_board.py", "--status")
        self.assertFalse(status["configured"])
        self.invoke("setup_agent_message_board.py", success=False)
        for script, args in [
            ("search_agent_message_board.py", ["--query", "testing"]),
            ("post_to_agent_message_board.py", ["--username", "MapleMaker_a7c92f", "--title", "Test", "--body", "x"]),
        ]:
            result = self.invoke(script, *args, success=False)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stderr)["code"], "setup_required")
        self.assertFalse(self.config_home.exists())
        self.assertFalse(self.database.parent.exists())

    def test_missing_configured_database_is_not_recreated(self):
        self.setup_board()
        self.database.unlink()
        result = self.invoke("search_agent_message_board.py", "--query", "testing", success=False)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.database.exists())

    def test_setup_preserves_posts_and_reply_identity(self):
        self.setup_board()
        root = self.post(project="owner/repo")
        reply = self.invoke("post_to_agent_message_board.py", "--username", "CopperFinch_83bd12",
                            "--thread", root["thread_id"],
                            "--body-file", "-", input="Verified: café tests pass.\nSecond line.")
        self.setup_board()
        self.assertTrue(self.invoke("setup_agent_message_board.py", "--status")["configured"])
        thread = self.invoke("search_agent_message_board.py", "--thread", root["thread_id"])
        self.assertEqual(thread["thread"]["username"], "MapleMaker_a7c92f")
        self.assertEqual(thread["replies"][0]["username"], "CopperFinch_83bd12")
        self.assertEqual(thread["replies"][0]["project"], "owner/repo")
        self.assertIn("café", thread["replies"][0]["body"])
        match = self.search("café")["matches"][0]
        self.assertEqual(match["post_id"], reply["post_id"])
        self.assertEqual(match["thread_id"], root["thread_id"])
        self.assertEqual(match["title"], "Database setup")

    def test_scope_literal_queries_and_empty_results(self):
        self.setup_board()
        shared = self.post()
        local = self.post(project="owner/repo")
        self.post(project="owner/other")
        matches = self.search('"database" (missing) *', "--project", "owner/repo")["matches"]
        self.assertEqual({row["post_id"] for row in matches},
                         {shared["post_id"], local["post_id"]})
        self.assertEqual(len(self.search("database")["matches"]), 3)
        self.assertEqual(self.search("xyznotfound"), {"matches": [], "next_offset": None})

    def test_username_reuse_and_body_file(self):
        self.setup_board()
        message = Path(self.temp.name) / "message.md"
        message.write_text("A user's preference.\nKeep it concise.", encoding="utf-8")
        result = self.invoke("post_to_agent_message_board.py", "--title", "Preference",
                             "--username", "MapleMaker_a7c92f", "--body-file", message)
        self.assertEqual(result["username"], "MapleMaker_a7c92f")
        self.assertEqual(self.post(username=result["username"])["username"], result["username"])
        self.assertNotIn("agent", result)
        self.assertNotIn("session", result)
        match = self.search("preference")["matches"][0]
        self.assertEqual(match["username"], result["username"])
        self.assertNotIn("agent", match)
        self.assertNotIn("session", match)

    def test_invalid_posts_leave_no_partial_data(self):
        self.setup_board()
        self.invoke("post_to_agent_message_board.py", "--title", "Oops", "--body", "x", success=False)
        self.invoke("post_to_agent_message_board.py", "--username", "MapleMaker_a7c92f", "--thread", 999,
                    "--body", "orphan", success=False)
        self.invoke("post_to_agent_message_board.py", "--username", "MapleMaker_a7c92f", "--title", "Empty",
                    "--body", "  ", success=False)
        root = self.post()
        reply = self.invoke("post_to_agent_message_board.py", "--username", "MapleMaker_a7c92f", "--thread",
                            root["thread_id"], "--body", "first reply")
        self.invoke("post_to_agent_message_board.py", "--username", "MapleMaker_a7c92f", "--thread",
                    reply["post_id"], "--body", "nested", success=False)
        self.invoke("post_to_agent_message_board.py", "--username", "MapleMaker_a7c92f", "--thread",
                    root["thread_id"], "--project", "wrong", "--body", "wrong", success=False)
        with sqlite3.connect(self.database) as connection:
            self.assertEqual(connection.execute("SELECT count(*) FROM posts").fetchone()[0], 2)

    def test_pagination(self):
        self.setup_board()
        root = self.post()
        for index in range(3):
            self.invoke("post_to_agent_message_board.py", "--username", "MapleMaker_a7c92f", "--thread",
                        root["thread_id"], "--body", f"database reply {index}")
        first = self.invoke("search_agent_message_board.py", "--thread", root["thread_id"], "--limit", 2)
        second = self.invoke("search_agent_message_board.py", "--thread", root["thread_id"],
                             "--limit", 2, "--offset", first["next_offset"])
        self.assertEqual(len(first["replies"]), 2)
        self.assertEqual(len(second["replies"]), 1)
        self.assertIsNone(second["next_offset"])
        matches = self.search("database", "--limit", 2)
        rest = self.search("database", "--limit", 2, "--offset", matches["next_offset"])
        self.assertEqual(len(matches["matches"] + rest["matches"]), 4)
        self.assertIsNone(rest["next_offset"])
        self.invoke("search_agent_message_board.py", "--query", "database", "--limit", 101,
                    success=False)

    def test_concurrent_setup_and_posts(self):
        with ThreadPoolExecutor(max_workers=4) as executor:
            list(executor.map(lambda _: self.setup_board(), range(4)))
            posts = list(executor.map(lambda i: self.post(title=f"Concurrent {i}", username=f"MapleMaker_{i:06x}"), range(16)))
        self.assertEqual(len({post["post_id"] for post in posts}), 16)
        self.assertEqual(len({post["username"] for post in posts}), 16)
        self.assertEqual(len(self.search("concurrent", "--limit", 100)["matches"]), 16)
        with sqlite3.connect(self.database) as connection:
            self.assertEqual(connection.execute("PRAGMA integrity_check").fetchone()[0], "ok")

    def test_existing_board_can_be_accessed_from_new_configuration(self):
        self.setup_board()
        root = self.post()
        environment = dict(self.environment, XDG_CONFIG_HOME=str(Path(self.temp.name) / "other-config"))
        self.invoke("setup_agent_message_board.py", "--database", self.database, environment=environment)
        result = self.invoke("search_agent_message_board.py", "--thread", root["thread_id"],
                             environment=environment)
        self.assertEqual(result["thread"]["id"], root["post_id"])

    def test_invalid_setup_does_not_save_configuration(self):
        self.invoke("setup_agent_message_board.py", "--database", "relative.db", success=False)
        self.database.parent.mkdir()
        with sqlite3.connect(self.database) as connection:
            connection.execute("CREATE TABLE unrelated (value TEXT)")
            connection.execute("INSERT INTO unrelated VALUES ('keep')")
        self.invoke("setup_agent_message_board.py", "--database", self.database, success=False)
        self.assertFalse(self.config_home.exists())
        with sqlite3.connect(self.database) as connection:
            self.assertEqual(connection.execute("SELECT value FROM unrelated").fetchone()[0], "keep")
            connection.execute("PRAGMA user_version = 1")
        self.invoke("setup_agent_message_board.py", "--database", self.database, success=False)
        self.assertFalse(self.config_home.exists())

    def test_future_schema_is_not_overwritten(self):
        self.setup_board()
        self.post()
        with sqlite3.connect(self.database) as connection:
            connection.execute("PRAGMA user_version = 999")
        self.invoke("setup_agent_message_board.py", "--database", self.database, success=False)
        self.invoke("search_agent_message_board.py", "--query", "database", success=False)
        with sqlite3.connect(self.database) as connection:
            self.assertEqual(connection.execute("PRAGMA user_version").fetchone()[0], 999)
            self.assertEqual(connection.execute("SELECT count(*) FROM posts").fetchone()[0], 1)

    def test_upgrade_preserves_old_threads_and_author_groups(self):
        self.setup_board()
        root = self.post()
        reply = self.invoke("post_to_agent_message_board.py", "--username", "MapleMaker_a7c92f",
                            "--thread", root["thread_id"], "--body", "Database fix verified.")
        other = self.post()
        with sqlite3.connect(self.database) as connection:
            connection.execute("ALTER TABLE posts RENAME COLUMN username TO agent")
            connection.execute("ALTER TABLE posts ADD COLUMN session TEXT NOT NULL DEFAULT 'run-one'")
            connection.execute("UPDATE posts SET agent = 'openai-gpt-6-astra-high'")
            connection.execute("UPDATE posts SET session = 'run-two' WHERE id = ?", (other["post_id"],))
            connection.execute("PRAGMA user_version = 1")
        self.invoke("search_agent_message_board.py", "--query", "database", success=False)
        self.setup_board()
        thread = self.invoke("search_agent_message_board.py", "--thread", root["thread_id"])
        self.assertEqual(thread["thread"]["username"], f"LegacyMember_{root['post_id']}")
        self.assertEqual(thread["replies"][0]["username"], thread["thread"]["username"])
        self.assertEqual(thread["replies"][0]["id"], reply["post_id"])
        self.assertEqual(thread["replies"][0]["body"], "Database fix verified.")
        other_thread = self.invoke("search_agent_message_board.py", "--thread", other["thread_id"])
        self.assertNotEqual(other_thread["thread"]["username"], thread["thread"]["username"])
        self.assertEqual(len(self.search("database")["matches"]), 3)
        self.setup_board()
        self.post(username="CopperFinch_opus5.5_83bd12")
        with sqlite3.connect(self.database) as connection:
            columns = {row[1] for row in connection.execute("PRAGMA table_info(posts)")}
            self.assertIn("username", columns)
            self.assertNotIn("agent", columns)
            self.assertNotIn("session", columns)
            self.assertEqual(connection.execute("PRAGMA foreign_key_check").fetchall(), [])


if __name__ == "__main__":
    unittest.main()
