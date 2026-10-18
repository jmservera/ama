"""Real offline command and connection ownership checks on synthetic fixtures."""

from __future__ import annotations

import contextlib
import importlib.util
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

    def test_driverless_help_sqlite_success_failure_and_missing_mssql_driver(self) -> None:
        root = Path(__file__).resolve().parents[3]
        env = {
            **os.environ,
            **self.env,
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONPATH": os.pathsep.join(
                str(root / part)
                for part in ("src/core/src", "src/orchestrator/src", "src/core/tests")
            ),
        }
        probe = subprocess.run(
            [
                sys.executable,
                "-S",
                "-c",
                "import importlib.util;assert importlib.util.find_spec('mssql_python') is None",
            ],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(probe.returncode, 0, probe.stderr)
        command = [sys.executable, "-S", "-m", "zava_forward.orchestrator.document_rescan"]
        help_result = subprocess.run(
            [*command, "--help"],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        self.assertIn("--synthetic-local", help_result.stdout)
        success = subprocess.run(
            [*command, "--synthetic-local", "--limit", "1"],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(success.returncode, 2, success.stderr)
        self.assertEqual(json.loads(success.stdout)["clean"], 1)
        self.store.docstore.delete("ZF-1", "d1")
        failure = subprocess.run(
            [*command, "--synthetic-local", "--limit", "1"],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(failure.returncode, 1, failure.stderr)
        self.assertEqual(json.loads(failure.stdout)["failed"], 1)
        self.assertIn("DOCUMENT_RESCAN_FAILED", failure.stderr)
        missing_driver = subprocess.run(
            [*command, "--synthetic-local"],
            env={**env, "ZF_STORE": "mssql"},
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(missing_driver.returncode, 1)
        self.assertIn("DOCUMENT_RESCAN_ERROR", missing_driver.stderr)
        for result in (success, failure, missing_driver):
            self.assertNotIn("Traceback", result.stderr)
            self.assertNotIn("SYN_PRIVATE", result.stdout + result.stderr)

    @unittest.skipUnless(importlib.util.find_spec("mssql_python"), "optional MSSQL driver absent")
    def test_selected_mssql_driver_error_is_sanitized_before_store_return(self) -> None:
        from mssql_python import Error

        stdout, stderr = io.StringIO(), io.StringIO()
        with (
            patch.dict(os.environ, {**self.env, "ZF_STORE": "mssql"}),
            patch(
                "zava_forward.orchestrator.document_rescan.open_store",
                side_effect=Error(
                    "SYN_PRIVATE_SQL_DRIVER_DIAGNOSTIC", "SYN_PRIVATE_DDBC_DIAGNOSTIC"
                ),
            ),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            self.assertEqual(main(["--synthetic-local"]), 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("DOCUMENT_RESCAN_ERROR", stderr.getvalue())
        self.assertNotIn("SYN_PRIVATE", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

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

    def test_actual_cli_conflict_recovery_entire_root_stream_is_safe(self) -> None:
        constructor: Any = SqlStore
        other = constructor(str(self.path), self.env["ZF_SQLITE"])
        self.addCleanup(other.db.close)
        discard = self.store._discard
        self.store.audit("system", "SYN_prior", "ZF-1", "SYN committed prefix")

        def scan(*args: Any) -> tuple[str, str]:
            from zava_forward.core.document_rescan import run

            self.assertEqual(run(other, limit=1)["clean"], 1)
            return "clean", "SYN stale"

        def broken_recovery(pending: Any = ()) -> None:
            discard(pending)
            raise OSError("SYN_PRIVATE_SQL_RECOVERY_DIAGNOSTIC")

        stdout, stderr = io.StringIO(), io.StringIO()
        with (
            patch.dict(os.environ, self.env),
            patch("zava_forward.orchestrator.document_rescan.open_store", return_value=self.store),
            patch.object(self.store.scanner, "scan", side_effect=scan),
            patch.object(self.store, "_discard", side_effect=broken_recovery),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
            self.assertLogs(level="DEBUG") as logs,
        ):
            self.assertEqual(main(["--synthetic-local", "--limit", "1"]), 1)
        report = json.loads(stdout.getvalue())
        self.assertEqual((report["failed"], report["clean"], report["committed"]), (1, 0, 0))
        entire_stream = "\n".join(logs.output) + stderr.getvalue() + stdout.getvalue()
        self.assertNotIn("SYN_PRIVATE", entire_stream)
        self.assertNotIn("Traceback", entire_stream)
        self.assertIn("DOCUMENT_RESCAN_FAILED", entire_stream)
        with other.lock:
            self.assertEqual(other.detail("ZF-1")["documents"][0]["scan"]["status"], "clean")
        self.assertEqual(
            [entry["action"] for entry in other.audit_entries()],
            ["SYN_prior", "document_rescanned"],
        )
        self.assertTrue(other.verify_audit())

    def test_actual_cli_malformed_scanner_returns_structured_safe_failure(self) -> None:
        for value in (
            None,
            (),
            ("clean",),
            ("clean", "SYN", "extra"),
            ["clean", "SYN"],
            {"clean": "SYN"},
            "clean",
            ("unknown", "SYN_PRIVATE"),
            ("clean", None),
        ):
            constructor: Any = SqlStore
            target = constructor(str(self.path), self.env["ZF_SQLITE"])
            stdout, stderr = io.StringIO(), io.StringIO()
            with (
                self.subTest(shape=type(value).__name__),
                patch.dict(os.environ, self.env),
                patch("zava_forward.orchestrator.document_rescan.open_store", return_value=target),
                patch.object(target.scanner, "scan", return_value=value),
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
                self.assertLogs(level="ERROR") as logs,
            ):
                self.assertEqual(main(["--synthetic-local", "--limit", "1"]), 1)
                report = json.loads(stdout.getvalue())
                self.assertEqual((report["failed"], report["clean"], report["checked"]), (1, 0, 1))
            self.assertNotIn("Traceback", "\n".join(logs.output) + stderr.getvalue())
            self.assertNotIn("SYN_PRIVATE", "\n".join(logs.output) + stderr.getvalue())
            with self.store.lock:
                self.assertEqual(
                    self.store.detail("ZF-1")["documents"][0]["scan"]["status"], "pending"
                )
            self.assertEqual(list(self.store.audit_entries()), [])
            self.assertTrue(self.store.detail("ZF-1")["legal_hold"]["active"])
            self.assertEqual(self.store.docstore.get("ZF-1", "d0"), b"SYN body")
        for boundary in ("scanner", "storage", "runner"):
            constructor = SqlStore
            target = constructor(str(self.path), self.env["ZF_SQLITE"])
            stdout, stderr = io.StringIO(), io.StringIO()
            failure: Exception = TypeError("SYN_PRIVATE_SCANNER_DIAGNOSTIC")
            if boundary == "storage":
                failure = OSError("SYN_PRIVATE_STORAGE_DIAGNOSTIC")
                location = patch.object(target.docstore, "get", side_effect=failure)
            elif boundary == "scanner":
                location = patch.object(target.scanner, "scan", side_effect=failure)
            else:
                location = patch(
                    "zava_forward.orchestrator.document_rescan.run", side_effect=failure
                )
            with (
                patch.dict(os.environ, self.env),
                patch("zava_forward.orchestrator.document_rescan.open_store", return_value=target),
                location,
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                if boundary != "runner":
                    with self.assertLogs(level="ERROR") as logs:
                        self.assertEqual(main(["--synthetic-local", "--limit", "1"]), 1)
                    self.assertEqual(json.loads(stdout.getvalue())["failed"], 1)
                    self.assertNotIn("SYN_PRIVATE", "\n".join(logs.output))
                else:
                    self.assertEqual(main(["--synthetic-local"]), 1)
                    self.assertIn("DOCUMENT_RESCAN_ERROR", stderr.getvalue())
            self.assertNotIn("SYN_PRIVATE", stdout.getvalue() + stderr.getvalue())
            self.assertNotIn("Traceback", stdout.getvalue() + stderr.getvalue())

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
