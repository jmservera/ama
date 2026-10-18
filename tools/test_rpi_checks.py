"""Focused orchestration failures; application behavior stays in existing suites."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "rpi_checks", Path(__file__).with_name("rpi-checks.py")
)
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


class GateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="rpi-contract-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()
        self.out = Path(self.temp.name) / "out"
        self.out.mkdir()
        for name in (
            "tools/rpi-checks.py",
            "src/check-container.py",
            *[f".github/workflows/{name}" for name in gate.WORKFLOWS],
        ):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# fixture\n")
        self.git("init", "-q")
        self.git("add", ".")
        self.git(
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.test",
            "commit",
            "-qm",
            "fixture",
        )
        self.base = self.git("rev-parse", "HEAD")
        self.git("update-ref", "refs/remotes/origin/main", self.base)

    def git(self, *args: str) -> str:
        return subprocess.check_output(
            ["git", "-C", str(self.root), *args], text=True, stderr=subprocess.PIPE
        ).strip()

    def runner(self) -> Any:
        return gate.Runner(self.root, self.out, self.base, [])

    def test_nonzero_command_blocks(self) -> None:
        runner = self.runner()
        runner.snapshot = self.root
        with self.assertRaises(gate.GateError):
            runner.command([sys.executable, "-c", "raise SystemExit(7)"])
        self.assertEqual(runner.rows[0]["exit_code"], 7)

    def test_missing_tools_and_dependencies_block(self) -> None:
        with (
            patch.object(gate.shutil, "which", return_value=None),
            self.assertRaises(gate.GateError),
        ):
            gate.tool_identity()
        runner = self.runner()
        runner.snapshot = self.root
        for argv in (
            ["/nonexistent/rpi-binary"],
            [sys.executable, "-c", "import absent_rpi_package"],
        ):
            with self.subTest(argv=argv), self.assertRaises(gate.GateError):
                runner.command(argv)

    def test_timeout_blocks(self) -> None:
        runner = self.runner()
        runner.snapshot = self.root
        with self.assertRaises(gate.GateError):
            runner.command([sys.executable, "-c", "import time; time.sleep(20)"], timeout=1)
        self.assertEqual(runner.rows[-1]["exit_code"], 124)

    def test_unexpected_skip_blocks_but_declared_discovery_skip_is_recorded(self) -> None:
        text = (
            "test_x (test_x.SQL.test_x) ... skipped 'needs a SQL Server (ZF_TEST_MSSQL=1)'\n"
            "Ran 1 test in 0.1s\n\nOK (skipped=1)\n"
        )
        self.assertEqual(len(gate.check_skips(text)["skips"]), 1)
        for value, integration in (
            (text, True),
            (text.replace("needs a SQL Server (ZF_TEST_MSSQL=1)", "missing tool"), False),
            (text.replace("skipped=1", "skipped=2"), False),
        ):
            with (
                self.subTest(value=value, integration=integration),
                self.assertRaises(gate.GateError),
            ):
                gate.check_skips(value, integration=integration)

    def test_commit_identity_change_invalidates(self) -> None:
        before = gate.clean_identity(self.root, self.base)
        self.git(
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.test",
            "commit",
            "--allow-empty",
            "-qm",
            "correction",
        )
        after = gate.clean_identity(self.root, self.base)
        self.assertNotEqual(before, after)

    def test_base_movement_invalidates(self) -> None:
        self.git(
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.test",
            "commit",
            "--allow-empty",
            "-qm",
            "main moved",
        )
        self.git("update-ref", "refs/remotes/origin/main", "HEAD")
        with self.assertRaises(gate.GateError):
            gate.clean_identity(self.root, self.base)

    def test_dirty_tracked_untracked_and_ignored_inputs_block(self) -> None:
        for name in (
            "module.py",
            "test_extra.py",
            "pyproject.toml",
            ".ignored.py",
            "src/check-container.py",
        ):
            with self.subTest(name=name):
                path = self.root / name
                original = path.read_bytes() if path.exists() else None
                path.write_text("uncommitted\n")
                if name.startswith(".ignored"):
                    (self.root / ".git/info/exclude").write_text(".ignored.py\n")
                with self.assertRaises(gate.GateError):
                    gate.clean_identity(self.root, self.base)
                if original is None:
                    path.unlink()
                else:
                    path.write_bytes(original)

    def test_unique_resources_and_sql_ownership(self) -> None:
        first = self.runner()
        other = self.out / "other"
        other.mkdir()
        second = gate.Runner(self.root, other, self.base, [])
        self.assertNotEqual(first.token, second.token)
        document: dict[str, Any] = {
            "Id": "a" * 64,
            "State": {"Running": True},
            "Config": {"Labels": {"ama.rpi.owner": first.token}},
            "NetworkSettings": {
                "Ports": {"1433/tcp": [{"HostIp": "127.0.0.1", "HostPort": "25432"}]}
            },
        }
        self.assertEqual(gate.owned_sql(document, "a" * 64, first.token), "25432")
        for owner, container in ((second.token, "a" * 64), (first.token, "b" * 64)):
            with self.assertRaises(gate.GateError):
                gate.owned_sql(document, container, owner)
        document["NetworkSettings"]["Ports"]["1433/tcp"][0]["HostIp"] = "0.0.0.0"
        with self.assertRaises(gate.GateError):
            gate.owned_sql(document, "a" * 64, first.token)

    def test_interruption_cleanup_only_removes_owned_container(self) -> None:
        runner = self.runner()
        runner.containers.add("a" * 64)
        document = {"Id": "a" * 64, "Config": {"Labels": {"ama.rpi.owner": runner.token}}}
        completed = subprocess.CompletedProcess([], 0, json.dumps([document]), "")
        with patch.object(gate.subprocess, "run", return_value=completed) as run:
            runner.cleanup()
        self.assertEqual(run.call_args_list[-1].args[0], ["docker", "rm", "-f", "a" * 64])
        runner.containers.add("b" * 64)
        with (
            patch.object(gate.subprocess, "run", return_value=completed),
            self.assertRaises(gate.GateError),
        ):
            runner.cleanup()

    def test_tampered_or_failed_receipt_refuses_without_executing_content(self) -> None:
        path = self.out / "receipt.json"
        gate.atomic_json(path, {"status": "passed", "argv": ["do-not-execute"]})
        (self.out / "receipt.sha256").write_text("wrong\n")
        with patch.object(gate.subprocess, "run") as run, self.assertRaises(gate.GateError):
            gate.verify(self.root, path, self.base)
        run.assert_not_called()
        gate.atomic_json(path, {"schema": 1, "status": "failed"})
        (self.out / "receipt.sha256").write_text(gate.digest(path))
        with self.assertRaises(gate.GateError):
            gate.verify(self.root, path, self.base)
        receipt = {
            "schema": 1,
            "status": "passed",
            "identity": gate.clean_identity(self.root, self.base),
            "tools": {},
            "environments": {},
            "extras": [],
            "groups": gate.required_groups([]),
            "commands": [
                {"group": name, "exit_code": 0, "log": "gate.log", "sha256": "fixture"}
                for name in gate.required_groups([])
            ],
            "files": {
                "gate.log": "fixture",
                "axe-4.10.3.min.js": "fixture",
                "regulatory-ux-results.json": "fixture",
                **{f"{p}-{s}.json": "fixture" for p in gate.IMAGES for s in ("gate", "all")},
                **{f"{p}.spdx.json": "fixture" for p in gate.IMAGES},
            },
            "trivy_database": {},
            "images": {
                "mssql": "fixture",
                **{
                    name: {"id": "fixture", "tag": "fixture"}
                    for name in ("logo-0600", *[f"image-{p}" for p in gate.IMAGES])
                },
            },
        }
        gate.atomic_json(path, receipt)
        (self.out / "receipt.sha256").write_text(gate.digest(path))
        real_digest = gate.digest
        real_output = gate.subprocess.check_output

        def output(argv: list[str], **kwargs: Any) -> Any:
            return "fixture\n" if argv[0] == "docker" else real_output(argv, **kwargs)

        with (
            patch.object(gate, "tool_identity", return_value={}),
            patch.object(gate, "environment_identity", return_value={}),
            patch.object(gate, "scan_database", return_value={}),
            patch.object(gate.subprocess, "check_output", side_effect=output),
            patch.object(
                gate,
                "digest",
                side_effect=lambda p: (
                    real_digest(p) if p.name == "receipt.json" or p.is_file() else "fixture"
                ),
            ),
        ):
            gate.verify(self.root, path, self.base)
            for name in ("untracked_source.py", "test_extra.py", "config.toml"):
                (self.root / name).touch()
                with self.assertRaises(gate.GateError):
                    gate.verify(self.root, path, self.base)
                (self.root / name).unlink()
            receipt["groups"].pop()
            gate.atomic_json(path, receipt)
            (self.out / "receipt.sha256").write_text(real_digest(path))
            with self.assertRaises(gate.GateError):
                gate.verify(self.root, path, self.base)

    def test_matrix_drift_and_unreviewed_extra_commands_refuse(self) -> None:
        self.assertEqual(len(gate.required_groups([])), 17)
        self.assertEqual(gate.SQL_SELECTORS[0], "test_mssqlstore")
        for value in (
            "api:test_module;curl external",
            "api:../../private",
            "bash:echo",
            "api:test_x\nid",
        ):
            with self.subTest(value=value), self.assertRaises(gate.GateError):
                gate.extra_selector(value)
        self.assertEqual(
            gate.extra_selector("api:test_x.Case.test_method"), ("api", "test_x.Case.test_method")
        )
        runner = self.runner()
        runner.snapshot = self.root

        def version(argv: list[str], **kwargs: Any) -> str:
            return "Python 3.12.3" if argv[0] == "python3" else "Version: 0.76.0"

        with (
            patch.object(runner, "command", side_effect=version),
            patch.object(gate, "tool_identity", return_value={}),
        ):
            runner.preflight()
        self.assertTrue(runner.failures)

    def test_axe_and_scan_database_cannot_silently_skip(self) -> None:
        with self.assertRaises(gate.GateError):
            gate.scan_database(self.out / "absent.json")
        path = self.out / "metadata.json"
        now = datetime.now(UTC)
        for delta in (-1, 1):
            path.write_text(
                json.dumps(
                    {
                        "UpdatedAt": (now - timedelta(hours=2)).isoformat(),
                        "NextUpdate": (now + timedelta(hours=delta)).isoformat(),
                    }
                )
            )
            if delta < 0:
                with self.assertRaises(gate.GateError):
                    gate.scan_database(path)
            else:
                self.assertIn("sha256", gate.scan_database(path))
        assert gate.__file__ is not None
        source = Path(gate.__file__).read_text()
        self.assertIn("if digest(axe) != AXE_SHA256:", source)
        runner = self.runner()
        with patch.dict(
            os.environ,
            {"ZF_SQL_SERVER": "real.invalid", "AZURE_TOKEN": "secret", "ZF_DATA": "/private/data"},
        ):
            self.assertNotIn("ZF_SQL_SERVER", runner.env)
            self.assertNotIn("AZURE_TOKEN", runner.env)
            self.assertNotEqual(runner.env["ZF_DATA"], "/private/data")


if __name__ == "__main__":
    unittest.main()
