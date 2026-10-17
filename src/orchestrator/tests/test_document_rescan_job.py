"""Real offline command and connection ownership checks on synthetic fixtures."""

from __future__ import annotations

import contextlib
import io
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from test_document_rescan import seed
from zava_forward.core.sqlstore import SqlStore

from zava_forward.orchestrator.document_rescan import main


class RescanCommand(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        seed(self.path)
        self.env = dict(
            ZF_DATA=str(self.path),
            ZF_STORE="sqlite",
            ZF_SQLITE=str(self.path.with_suffix(".sqlite")),
            ZF_SCANNER="local",
            ZF_DOC_STORE="local",
        )
        constructor: Any = SqlStore
        self.store = constructor(str(self.path), self.env["ZF_SQLITE"])
        self.addCleanup(self.store.db.close)
        for index in range(3):
            self.store.docstore.put("ZF-1", f"d{index}", b"SYN body", "text/plain")

    def command(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "zava_forward.orchestrator.document_rescan",
                "--synthetic-local",
                *args,
            ],
            env={**os.environ, **self.env},
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    def test_actual_command_incomplete_page_then_terminal_then_idempotent(self) -> None:
        first = self.command("--limit", "1")
        self.assertEqual(first.returncode, 2, first.stderr)
        page = json.loads(first.stdout)
        self.assertEqual(page["clean"], 1)
        self.assertEqual(page["next_after"], ["ZF-1", "d0"])
        self.assertIn("synthetic-demo", page["scanner"])
        last = self.command("--after", *page["next_after"])
        self.assertEqual(last.returncode, 0, last.stderr)
        self.assertEqual(json.loads(last.stdout)["clean"], 2)
        repeat = self.command()
        self.assertEqual(repeat.returncode, 0, repeat.stderr)
        self.assertEqual(json.loads(repeat.stdout)["checked"], 0)
        self.assertEqual(len(list(self.store.audit_entries())), 3)

    def test_preflight_refuses_implicit_scanner_data_store_and_invalid_bounds(self) -> None:
        for changes, args in (
            ({"ZF_DATA": ""}, ["--synthetic-local"]),
            ({"ZF_SCANNER": ""}, ["--synthetic-local"]),
            ({"ZF_STORE": "json"}, ["--synthetic-local"]),
            ({}, []),
            ({}, ["--synthetic-local", "--limit", "0"]),
            ({}, ["--synthetic-local", "--after", "", "d0"]),
        ):
            with (
                patch.dict(os.environ, {**self.env, **changes}),
                patch("zava_forward.orchestrator.document_rescan.open_store") as opened,
                contextlib.redirect_stderr(io.StringIO()),
            ):
                with self.assertRaises(SystemExit):
                    main(args)
                opened.assert_not_called()

    def test_failure_is_safe_nonzero_and_bytes_remain_pending(self) -> None:
        self.store.docstore.delete("ZF-1", "d0")
        result = self.command("--limit", "1")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)["failed"], 1)
        self.assertIn("DOCUMENT_RESCAN_FAILED", result.stderr)
        self.assertNotIn("SYN_PRIVATE_NAME", result.stderr)
        with self.store.lock:
            self.assertEqual(self.store.detail("ZF-1")["documents"][0]["scan"]["status"], "pending")

    def test_successful_main_closes_owned_connection(self) -> None:
        with (
            patch.dict(os.environ, self.env),
            patch("zava_forward.orchestrator.document_rescan.open_store", return_value=self.store),
            contextlib.redirect_stdout(io.StringIO()),
        ):
            self.assertEqual(main(["--synthetic-local"]), 0)
        with self.assertRaises(sqlite3.ProgrammingError):
            self.store.db.execute("SELECT 1")

    def test_initialization_failure_after_real_open_closes_without_masking(self) -> None:
        connections = []
        original_open = SqlStore._open
        error = ValueError("SYN_PRIVATE credential/path diagnostic")

        def opened(store: Any, db_path: str) -> None:
            original_open(store, db_path)
            connections.append(store.db)

        with (
            patch.object(SqlStore, "_open", opened),
            patch.object(SqlStore, "_create_schema", side_effect=error),
        ):
            constructor: Any = SqlStore
            with self.assertRaises(ValueError) as caught:
                constructor(str(self.path), self.env["ZF_SQLITE"])
            self.assertIs(caught.exception, error)
            stderr = io.StringIO()
            with patch.dict(os.environ, self.env), contextlib.redirect_stderr(stderr):
                self.assertEqual(main(["--synthetic-local"]), 1)
            self.assertIn("DOCUMENT_RESCAN_ERROR", stderr.getvalue())
            self.assertNotIn("SYN_PRIVATE", stderr.getvalue())
        self.assertEqual(len(connections), 2)
        for db in connections:
            with self.assertRaises(sqlite3.ProgrammingError):
                db.execute("SELECT 1")

    def test_exit_precedence_for_pending_continuation_and_committed(self) -> None:
        for fields, expected in (
            ({"pending": 1}, 2),
            ({"next_after": ["ZF-1", "d0"]}, 2),
            ({"pending": 1, "failed": 1}, 1),
            ({"pending": 1, "committed": 1}, 1),
            ({}, 0),
        ):
            report: dict[str, Any] = dict(pending=0, failed=0, committed=0, next_after=None)
            report.update(fields)
            with (
                patch.dict(os.environ, self.env),
                patch("zava_forward.orchestrator.document_rescan.open_store") as opened,
                patch("zava_forward.orchestrator.document_rescan.run", return_value=report),
                contextlib.redirect_stdout(io.StringIO()),
            ):
                opened.return_value.scanner.name = "synthetic-demo"
                self.assertEqual(main(["--synthetic-local"]), expected)
                opened.return_value.db.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
