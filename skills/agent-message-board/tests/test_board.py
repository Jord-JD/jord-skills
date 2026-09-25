"""Exercise JSON board commands, concurrent writers, and independent folder replicas."""

from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from board_store import write_json


class BoardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.board = Path(self.temp.name) / "chosen board"
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

    def setup_board(self, directory=None, environment=None):
        return self.invoke("setup_agent_message_board.py", "--directory", directory or self.board,
                           environment=environment)

    def post(self, title="Database setup", body="Use a local database.",
             username="MapleMaker_a7c92f", **options):
        arguments = ["--username", username, "--title", title, "--body", body]
        for key, value in options.items():
            arguments.extend(["--" + key, value])
        return self.invoke("post_to_agent_message_board.py", *arguments)

    def reply(self, thread, body="Database fix verified.", environment=None):
        return self.invoke("post_to_agent_message_board.py", "--username", "CopperFinch_83bd12",
                           "--thread", thread, "--body", body, environment=environment)

    def search(self, query, *arguments, environment=None):
        return self.invoke("search_agent_message_board.py", "--query", query, *arguments,
                           environment=environment)

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
        self.assertFalse(self.board.exists())

    def test_missing_board_is_not_recreated(self):
        self.setup_board()
        shutil.rmtree(self.board)
        result = self.invoke("search_agent_message_board.py", "--query", "testing", success=False)
        self.assertEqual(result.returncode, 2)
        self.assertFalse(self.board.exists())

    def test_setup_preserves_posts_and_reply_identity(self):
        self.setup_board()
        root = self.post(project="owner/repo")
        root_path = self.board / "posts" / (root["post_id"] + ".json")
        original = root_path.read_bytes()
        reply = self.invoke("post_to_agent_message_board.py", "--username", "CopperFinch_83bd12",
                            "--thread", root["thread_id"], "--body-file", "-",
                            input="Verified: café tests pass.\nSecond line.")
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
        self.assertTrue(match["thread_available"])
        self.assertEqual(root_path.read_bytes(), original)
        self.assertEqual(str(uuid.UUID(root["post_id"])), root["post_id"])

    def test_search_includes_all_projects_and_preserves_labels(self):
        self.setup_board()
        shared = self.post()
        local = self.post(project="owner/repo")
        other = self.post(project="owner/other")
        matches = self.search('"database" (missing) *')["matches"]
        self.assertEqual({row["post_id"] for row in matches},
                         {shared["post_id"], local["post_id"], other["post_id"]})
        self.assertEqual({row["project"] for row in matches}, {None, "owner/repo", "owner/other"})
        self.invoke("search_agent_message_board.py", "--query", "database", "--project", "owner/repo",
                    success=False)
        self.assertEqual(self.search("xyznotfound"), {"matches": [], "next_offset": None})

    def test_username_reuse_and_body_file(self):
        self.setup_board()
        message = Path(self.temp.name) / "message.md"
        message.write_text("A user's preference.\nKeep it concise.", encoding="utf-8")
        result = self.invoke("post_to_agent_message_board.py", "--title", "Preference",
                             "--username", "MapleMaker_gpt6astra_a7c92f", "--body-file", message)
        self.assertEqual(result["username"], "MapleMaker_gpt6astra_a7c92f")
        self.assertEqual(self.post(username=result["username"])["username"], result["username"])
        self.assertNotIn("agent", result)
        self.assertNotIn("session", result)
        self.assertEqual(self.search("preference")["matches"][0]["username"], result["username"])

    def test_invalid_posts_leave_no_partial_data(self):
        self.setup_board()
        self.invoke("post_to_agent_message_board.py", "--title", "Oops", "--body", "x", success=False)
        self.invoke("post_to_agent_message_board.py", "--username", "MapleMaker_a7c92f", "--thread",
                    str(uuid.uuid4()), "--body", "orphan", success=False)
        self.invoke("post_to_agent_message_board.py", "--username", "MapleMaker_a7c92f", "--title", "Empty",
                    "--body", "  ", success=False)
        self.invoke("post_to_agent_message_board.py", "--username", "MapleMaker_a7c92f", "--thread",
                    "../../outside", "--body", "invalid", success=False)
        root = self.post()
        reply = self.reply(root["thread_id"])
        self.invoke("post_to_agent_message_board.py", "--username", "MapleMaker_a7c92f", "--thread",
                    reply["post_id"], "--body", "nested", success=False)
        self.invoke("post_to_agent_message_board.py", "--username", "MapleMaker_a7c92f", "--thread",
                    root["thread_id"], "--project", "wrong", "--body", "wrong", success=False)
        self.assertEqual(len(list((self.board / "posts").iterdir())), 2)

    def test_pagination(self):
        self.setup_board()
        root = self.post()
        for index in range(3):
            self.reply(root["thread_id"], f"database reply {index}")
        first = self.invoke("search_agent_message_board.py", "--thread", root["thread_id"], "--limit", 2)
        second = self.invoke("search_agent_message_board.py", "--thread", root["thread_id"],
                             "--limit", 2, "--offset", first["next_offset"])
        self.assertEqual(len(first["replies"]), 2)
        self.assertEqual(len(second["replies"]), 1)
        self.assertIsNone(second["next_offset"])
        for index in range(3):
            self.post(title=f"Database discussion {index}")
        matches = self.search("database", "--limit", 2)
        rest = self.search("database", "--limit", 2, "--offset", matches["next_offset"])
        self.assertEqual(len({m["post_id"] for m in matches["matches"] + rest["matches"]}), 4)
        self.assertIsNone(rest["next_offset"])
        self.invoke("search_agent_message_board.py", "--query", "database", "--limit", 101, success=False)

    def test_search_prioritizes_distinct_query_coverage_over_title_weight(self):
        self.setup_board()
        broad = self.post(title="Troubleshooting notes", body="USB packet timeout fixed.")
        partial = self.post(title="USB packet", body="USB USB USB packet")
        narrow = self.post(title="USB", body="USB " * 50)
        result = self.search("USB packet timeout")["matches"]
        self.assertEqual([row["post_id"] for row in result],
                         [broad["post_id"], partial["post_id"], narrow["post_id"]])
        repeated = self.search("usb USB packet timeout timeout")["matches"]
        self.assertEqual([row["post_id"] for row in repeated], [row["post_id"] for row in result])

    def test_search_retains_title_weight_for_equal_query_coverage(self):
        self.setup_board()
        title_hit = self.post(title="USB packet", body="Troubleshooting notes.")
        body_hit = self.post(title="Troubleshooting notes", body="USB packet")
        result = self.search("usb packet")["matches"]
        self.assertEqual([row["post_id"] for row in result], [title_hit["post_id"], body_hit["post_id"]])

    def test_search_keeps_best_reply_without_crowding_other_threads(self):
        self.setup_board()
        busy = self.post(title="USB notes", body="USB connection troubleshooting.")
        best = self.reply(busy["thread_id"], "USB packet timeout fixed by changing the buffer.")
        for index in range(8):
            self.reply(busy["thread_id"], f"USB packet observation {index}")
        other = self.post(title="Packet timeout", body="Another device behaves differently.")
        third = self.post(title="USB", body="A separate discussion.")
        first = self.search("usb packet timeout", "--limit", 2)
        second = self.search("usb packet timeout", "--limit", 2, "--offset", first["next_offset"])
        self.assertEqual(len(first["matches"]), 2)
        self.assertEqual(first["matches"][0]["post_id"], best["post_id"])
        self.assertIn("changing the buffer", first["matches"][0]["excerpt"])
        results = first["matches"] + second["matches"]
        self.assertEqual([row["thread_id"] for row in results],
                         [busy["thread_id"], other["thread_id"], third["thread_id"]])
        self.assertIsNone(second["next_offset"])

    def test_concurrent_setup_and_posts(self):
        with ThreadPoolExecutor(max_workers=4) as executor:
            list(executor.map(lambda _: self.setup_board(), range(4)))
            posts = list(executor.map(lambda i: self.post(title=f"Concurrent {i}",
                                     username=f"MapleMaker_{i:06x}"), range(16)))
        self.assertEqual(len({post["post_id"] for post in posts}), 16)
        self.assertEqual(len(self.search("concurrent", "--limit", 100)["matches"]), 16)
        self.assertEqual(len(list((self.board / "posts").iterdir())), 16)

    def test_independent_replicas_merge_concurrent_replies(self):
        self.setup_board()
        root = self.post()
        other_board = Path(self.temp.name) / "other-machine-board"
        other_environment = dict(self.environment, XDG_CONFIG_HOME=str(Path(self.temp.name) / "other-config"))
        shutil.copytree(self.board, other_board)
        self.setup_board(other_board, other_environment)
        one = self.reply(root["thread_id"], "First offline reply.")
        two = self.reply(root["thread_id"], "Second offline reply.", environment=other_environment)
        self.assertNotEqual(one["post_id"], two["post_id"])
        for source, destination in ((self.board, other_board), (other_board, self.board)):
            for path in (source / "posts").glob("*.json"):
                target = destination / "posts" / path.name
                if not target.exists():
                    shutil.copyfile(path, target)
        for environment in (self.environment, other_environment):
            thread = self.invoke("search_agent_message_board.py", "--thread", root["thread_id"],
                                 environment=environment)
            self.assertEqual({p["id"] for p in thread["replies"]}, {one["post_id"], two["post_id"]})

    def test_reply_can_arrive_before_root(self):
        self.setup_board()
        root = self.post()
        reply = self.reply(root["thread_id"])
        root_path = self.board / "posts" / (root["post_id"] + ".json")
        original = root_path.read_bytes()
        root_path.unlink()
        result = self.search("database")
        self.assertEqual(result["matches"][0]["post_id"], reply["post_id"])
        self.assertFalse(result["matches"][0]["thread_available"])
        thread = self.invoke("search_agent_message_board.py", "--thread", root["thread_id"])
        self.assertTrue(thread["missing_thread"])
        self.assertIsNone(thread["thread"])
        self.assertEqual(len(thread["replies"]), 1)
        root_path.write_bytes(original)
        self.assertFalse(self.invoke("search_agent_message_board.py", "--thread", root["thread_id"])["missing_thread"])

    def test_incomplete_malformed_and_conflict_files_are_reported(self):
        self.setup_board()
        root = self.post()
        posts = self.board / "posts"
        (posts / ".unfinished.tmp").write_text('{"partial":', encoding="utf-8")
        broken = posts / (str(uuid.uuid4()) + ".json")
        broken.write_text('{"partial":', encoding="utf-8")
        original = posts / (root["post_id"] + ".json")
        shutil.copyfile(original, posts / (root["post_id"] + ".sync-conflict.json"))
        result = self.search("database")
        self.assertEqual(len(result["matches"]), 1)
        self.assertEqual(result["skipped_files"], 2)
        self.assertEqual(len(result["warnings"]), 2)
        self.assertIn("warnings", self.search("nomatch"))

    def test_post_publication_cannot_overwrite_an_existing_file(self):
        self.setup_board()
        root = self.post()
        path = self.board / "posts" / (root["post_id"] + ".json")
        original = path.read_bytes()
        with self.assertRaises(FileExistsError):
            write_json(path, {"body": "replacement"})
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(len(list(path.parent.iterdir())), 1)

    def test_invalid_setup_and_old_sqlite_configuration_are_not_changed(self):
        self.invoke("setup_agent_message_board.py", "--directory", "relative", success=False)
        selected_file = Path(self.temp.name) / "existing.sqlite3"
        selected_file.write_bytes(b"leave me alone")
        self.invoke("setup_agent_message_board.py", "--directory", selected_file, success=False)
        self.assertFalse(self.config_home.exists())
        config = self.config_home / "agent-message-board/config.json"
        config.parent.mkdir(parents=True)
        original = json.dumps({"version": 1, "database": str(selected_file)})
        config.write_text(original, encoding="utf-8")
        result = self.invoke("setup_agent_message_board.py", "--status", success=False)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(config.read_text(), original)
        self.assertEqual(selected_file.read_bytes(), b"leave me alone")
        self.assertFalse(self.board.exists())

    def test_unsupported_post_format_does_not_break_valid_search(self):
        self.setup_board()
        root = self.post()
        path = self.board / "posts" / (root["post_id"] + ".json")
        future = json.loads(path.read_text())
        future["version"] = 99
        future["id"] = str(uuid.uuid4())
        future["thread_id"] = future["id"]
        (path.parent / (future["id"] + ".json")).write_text(json.dumps(future))
        result = self.search("database")
        self.assertEqual(len(result["matches"]), 1)
        self.assertEqual(result["skipped_files"], 1)


if __name__ == "__main__":
    unittest.main()
