"""Focused orchestration failures; application behavior stays in existing suites."""

from __future__ import annotations

import copy
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
import venv
from contextlib import redirect_stderr, redirect_stdout
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch

SPEC = importlib.util.spec_from_file_location(
    "rpi_checks", Path(__file__).with_name("rpi-checks.py")
)
assert SPEC is not None and SPEC.loader is not None
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


class GateTests(unittest.TestCase):
    def test_employee_acceptance_cli_is_required_without_extras_and_dispatched(self) -> None:
        module = "checks.employee_acceptance_check"
        self.assertIn("browser", gate.required_groups([]))
        checks = gate.required_checks(
            self.root,
            {
                "owner": "a" * 24,
                "sql": {},
                "images": {},
                "extras": [],
                "executed_groups": ["browser"],
            },
        )
        selected = [row for row in checks if module in row["argv"]]
        self.assertEqual(len(selected), 1)
        contract = selected[0]
        self.assertEqual(contract["argv"], ["<output>/venvs/api/bin/python", "-m", module])
        self.assertEqual(contract["cwd"], "src/api")
        self.assertEqual(
            contract["env"],
            {"PYTHONPATH": ".:src:tests:../core/src:../agents/src:../core/tests:../agents/tests"},
        )
        self.assertTrue(contract["suite"])
        self.assertTrue(contract["integration"])
        self.assertEqual(
            checks[checks.index(contract) - 1]["argv"],
            ["<output>/venvs/api/bin/python", "-m", "playwright", "install", "chromium"],
        )
        runner = self.runner()
        runner.snapshot = self.root
        commands = []

        def command(argv: list[str], cwd: str = ".", **kwargs: Any) -> str:
            commands.append(argv)
            if module in argv:
                self.assertEqual(argv, [runner.python("api"), *contract["argv"][1:]])
                self.assertEqual(cwd, contract["cwd"])
                self.assertEqual(
                    kwargs,
                    {"env": contract["env"], "suite": True, "integration": True},
                )
                self.assertEqual(
                    commands[-2],
                    [runner.python("api"), "-m", "playwright", "install", "chromium"],
                )
                raise gate.GateError("fixture stops after employee acceptance dispatch")
            return ""

        with patch.object(runner, "lint"), patch.object(runner, "command", side_effect=command):
            runner.browser()
        self.assertEqual(
            runner.failures, ["browser: fixture stops after employee acceptance dispatch"]
        )

    def test_employee_acceptance_receipt_requires_cli_paths_flags_and_zero_skips(self) -> None:
        original = self.scoped_receipt(["browser"])
        gate.verify_commands(self.root, self.out, original)
        for mutation in (
            "missing",
            "module",
            "paths",
            "suite",
            "integration",
            "exit",
            "zero",
            "count",
            "discovery-skip",
            "sql-skip",
        ):
            with self.subTest(mutation=mutation):
                receipt = copy.deepcopy(original)
                row = next(
                    row
                    for row in receipt["commands"]
                    if "checks.employee_acceptance_check" in row["argv"]
                )
                path = self.out / row["log"]
                saved = path.read_text()
                if mutation == "missing":
                    receipt["commands"].remove(row)
                elif mutation == "module":
                    row["argv"][-1] = "checks.design_system_browser_check"
                elif mutation == "paths":
                    row["env"]["PYTHONPATH"] = ".:src"
                elif mutation in ("suite", "integration"):
                    row[mutation] = False
                elif mutation == "exit":
                    row["exit_code"] = 1
                else:
                    count = 0 if mutation == "zero" else 2 if mutation == "count" else 3
                    results = "test_x ... ok\n" * count
                    skips = []
                    if mutation.endswith("skip"):
                        test, reason = (
                            next(iter(gate.SQL_NOT_APPLICABLE))
                            if mutation == "sql-skip"
                            else ("test_x", "Chromium is installed by the later browser-check step")
                        )
                        results = "test_x ... ok\n" * 2 + f"{test} ... skipped '{reason}'\n"
                        skips = [{"test": test, "reason": reason}]
                    text = (
                        f"{results}Ran {count} tests in 0.1s\n\nOK"
                        + (" (skipped=1)" if skips else "")
                        + "\n"
                    )
                    path.write_text(text)
                    row.update(
                        tests=count,
                        executed=count - len(skips),
                        skips=skips,
                        sha256=gate.digest(path),
                    )
                    receipt["files"][row["log"]] = row["sha256"]
                try:
                    with self.assertRaises(gate.GateError):
                        gate.verify_commands(self.root, self.out, receipt)
                finally:
                    path.write_text(saved)

    def test_employee_acceptance_runtime_requires_three_tests_and_zero_skips(self) -> None:
        runner = self.runner()
        runner.snapshot = self.root
        runner.group = "browser"
        sql_test, sql_reason = next(iter(gate.SQL_NOT_APPLICABLE))
        success = "test_x ... ok\n" * 3 + "Ran 3 tests in 0.1s\n\nOK\n"
        discovery = (
            "test_x ... skipped 'Chromium is installed by the later browser-check step'\n" * 3
            + "Ran 3 tests in 0.1s\n\nOK (skipped=3)\n"
        )
        sql_skip = (
            "test_x ... ok\n" * 2
            + f"{sql_test} ... skipped '{sql_reason}'\n"
            + "Ran 3 tests in 0.1s\n\nOK (skipped=1)\n"
        )
        for output, valid in (
            (success, True),
            (success.replace("Ran 3", "Ran 0"), False),
            (success.replace("Ran 3", "Ran 2"), False),
            (discovery, False),
            (sql_skip, False),
        ):
            with self.subTest(output=output), patch("builtins.print"):
                argv = [
                    sys.executable,
                    "-c",
                    f"print({output!r})",
                    "checks.employee_acceptance_check",
                ]
                if valid:
                    runner.command(argv, suite=True, integration=True)
                    self.assertEqual(runner.rows[-1]["tests"], 3)
                    self.assertEqual(runner.rows[-1]["executed"], 3)
                    self.assertEqual(runner.rows[-1]["skips"], [])
                else:
                    with self.assertRaises(gate.GateError):
                        runner.command(argv, suite=True, integration=True)

    def test_chat_panel_browser_command_is_required_and_dispatched_with_opt_in(self) -> None:
        checks = gate.required_checks(
            self.root,
            {
                "owner": "a" * 24,
                "sql": {},
                "images": {},
                "extras": [],
                "executed_groups": ["browser"],
            },
        )
        selected = [row for row in checks if gate.CHAT_PANEL_BROWSER_SELECTOR in row["argv"]]
        self.assertEqual(len(selected), 1)
        contract = selected[0]
        self.assertEqual(
            contract["argv"],
            [
                "<output>/venvs/api/bin/python",
                "-m",
                "unittest",
                "-v",
                gate.CHAT_PANEL_BROWSER_SELECTOR,
            ],
        )
        self.assertEqual(contract["cwd"], "src/api")
        self.assertEqual(
            contract["env"],
            {
                "PYTHONPATH": "<checkout>/src/api/tests:<checkout>/src/core/tests:"
                "<checkout>/src/agents/tests",
                "ZF_BROWSER_TESTS": "1",
            },
        )
        self.assertTrue(contract["suite"])
        self.assertTrue(contract["integration"])
        runner = self.runner()
        runner.snapshot = self.root

        def command(argv: list[str], cwd: str = ".", **kwargs: Any) -> str:
            if gate.CHAT_PANEL_BROWSER_SELECTOR in argv:
                self.assertEqual(argv, [runner.python("api"), *contract["argv"][1:]])
                self.assertEqual(cwd, contract["cwd"])
                self.assertEqual(
                    kwargs,
                    {
                        "env": {
                            **runner.tests_env("api", True),
                            "ZF_BROWSER_TESTS": "1",
                        },
                        "suite": True,
                        "integration": True,
                    },
                )
                raise gate.GateError("fixture stops after exact dispatch")
            return ""

        with patch.object(runner, "lint"), patch.object(runner, "command", side_effect=command):
            runner.browser()
        self.assertEqual(runner.failures, ["browser: fixture stops after exact dispatch"])

    def test_chat_panel_discovery_skip_is_exact_and_integration_fails_closed(self) -> None:
        test, reason = gate.CHAT_PANEL_DISCOVERY_SKIP
        text = f"{test} ... skipped '{reason}'\nRan 1 test in 0.1s\n\nOK (skipped=1)\n"
        self.assertIn(reason, gate.EXPECTED_SKIP_REASONS)
        self.assertEqual(
            gate.check_skips(text, group="project-api"),
            {"tests": 1, "executed": 0, "skips": [{"test": test, "reason": reason}]},
        )
        for value, group, integration in (
            (text, "", False),
            (text, "project-core", False),
            (text, "browser", True),
            (text, "project-api", True),
            (text.replace("PanelTests", "OtherTests"), "project-api", False),
            (text.replace(reason, "missing Chromium"), "project-api", False),
        ):
            with self.subTest(value=value, group=group, integration=integration):
                with self.assertRaises(gate.GateError):
                    gate.check_skips(value, group=group, integration=integration)
        runner = self.runner()
        runner.snapshot = self.root
        runner.group = "project-api"
        captured = io.StringIO()
        with redirect_stdout(captured):
            runner.command([sys.executable, "-c", f"print({text!r})"], suite=True)
        self.assertEqual(runner.rows[-1]["skips"], [{"test": test, "reason": reason}])
        runner.group = "browser"
        with redirect_stdout(captured), self.assertRaises(gate.GateError):
            runner.command([sys.executable, "-c", f"print({text!r})"], suite=True, integration=True)
        self.assertIn(text, captured.getvalue())
        self.assertEqual(captured.getvalue().count(text), 2)

    def test_synthetic_skip_fixture_does_not_contaminate_outer_suite(self) -> None:
        transcript = io.StringIO()
        suite = unittest.TestSuite(
            [GateTests("test_chat_panel_discovery_skip_is_exact_and_integration_fails_closed")]
        )
        with redirect_stdout(transcript), redirect_stderr(transcript):
            result = unittest.TextTestRunner(stream=transcript, verbosity=2).run(suite)
        self.assertTrue(result.wasSuccessful(), transcript.getvalue())
        self.assertEqual(
            gate.check_skips(transcript.getvalue(), group="static"),
            {"tests": 1, "executed": 1, "skips": []},
        )

    def test_chat_panel_required_receipt_rejects_missing_flag_selector_or_execution(self) -> None:
        original = self.scoped_receipt(["browser"])
        gate.verify_commands(self.root, self.out, original)
        for mutation in (
            "missing",
            "flag",
            "selector",
            "skip",
            "zero",
            "unexpected-skip",
            "wrong-success",
            "missing-success",
            "duplicate-success",
            "extra-success",
            "wrong-count",
        ):
            with self.subTest(mutation=mutation):
                receipt = copy.deepcopy(original)
                row = next(
                    row
                    for row in receipt["commands"]
                    if gate.CHAT_PANEL_BROWSER_SELECTOR in row["argv"]
                )
                path = self.out / row["log"]
                saved = path.read_text()
                if mutation == "missing":
                    receipt["commands"].remove(row)
                elif mutation == "flag":
                    row["env"].pop("ZF_BROWSER_TESTS")
                elif mutation == "selector":
                    row["argv"][-1] = "test_chat_panel.PanelTests"
                elif mutation.endswith("success") or mutation == "wrong-count":
                    test = gate.CHAT_PANEL_DISCOVERY_SKIP[0]
                    result = f"{test} ... ok\n"
                    if mutation == "wrong-success":
                        result = result.replace("PanelTests", "OtherTests")
                    elif mutation == "missing-success":
                        result = ""
                    elif mutation == "duplicate-success":
                        result *= 2
                    elif mutation == "extra-success":
                        result += "test_x (test_x.Fixture.test_x) ... ok\n"
                    count = 2 if mutation == "wrong-count" else 1
                    text = f"{result}Ran {count} tests in 0.1s\n\nOK\n"
                    path.write_text(text)
                    row.update(
                        gate.check_skips(text),
                        sha256=gate.digest(path),
                    )
                    receipt["files"][row["log"]] = row["sha256"]
                else:
                    test, reason = gate.CHAT_PANEL_DISCOVERY_SKIP
                    if mutation == "unexpected-skip":
                        reason = "missing dependency"
                    text = f"{test} ... skipped '{reason}'\nRan 1 test in 0.1s\n\nOK (skipped=1)\n"
                    if mutation == "zero":
                        text = "Ran 0 tests in 0.1s\n\nOK\n"
                    path.write_text(text)
                    row["sha256"] = gate.digest(path)
                    receipt["files"][row["log"]] = row["sha256"]
                    row.update(
                        tests=0 if mutation == "zero" else 1,
                        executed=0,
                        skips=[] if mutation == "zero" else [{"test": test, "reason": reason}],
                    )
                try:
                    with self.assertRaises(gate.GateError):
                        gate.verify_commands(self.root, self.out, receipt)
                finally:
                    path.write_text(saved)

    def test_chat_panel_exact_success_parser_preserves_other_suite_contracts(self) -> None:
        test = gate.CHAT_PANEL_DISCOVERY_SKIP[0]
        text = f"{test} ... ok\nRan 1 test in 0.1s\n\nOK\n"
        self.assertEqual(
            gate.check_skips(text, integration=True, group="browser", expected_test=test),
            {"tests": 1, "executed": 1, "skips": []},
        )
        unrelated = text.replace("PanelTests", "OtherTests")
        self.assertEqual(
            gate.check_skips(unrelated, integration=True, group="browser"),
            {"tests": 1, "executed": 1, "skips": []},
        )
        for output in (unrelated, text.replace(" ... ok", " ... expected failure")):
            with self.subTest(output=output):
                with self.assertRaises(gate.GateError):
                    gate.check_skips(output, integration=True, group="browser", expected_test=test)

    def test_chat_panel_runtime_requires_exact_success_evidence(self) -> None:
        runner = self.runner()
        runner.snapshot = self.root
        runner.group = "browser"
        test = gate.CHAT_PANEL_DISCOVERY_SKIP[0]
        text = f"{test} ... ok\nRan 1 test in 0.1s\n\nOK\n"
        for output, valid in ((text, True), (text.replace("PanelTests", "OtherTests"), False)):
            with self.subTest(valid=valid):
                argv = [
                    sys.executable,
                    "-c",
                    f"print({output!r})",
                    gate.CHAT_PANEL_BROWSER_SELECTOR,
                ]
                if valid:
                    runner.command(argv, suite=True, integration=True)
                    self.assertEqual(runner.rows[-1]["executed"], 1)
                    self.assertEqual(runner.rows[-1]["skips"], [])
                else:
                    with self.assertRaises(gate.GateError):
                        runner.command(argv, suite=True, integration=True)

    def test_chat_panel_discovery_receipt_recomputes_scoped_skip_evidence(self) -> None:
        receipt = self.scoped_receipt(["project-api"])
        row = next(row for row in receipt["commands"] if row["suite"])
        test, reason = gate.CHAT_PANEL_DISCOVERY_SKIP
        text = (
            "test_x (test_x.Fixture.test_x) ... ok\n"
            f"{test} ... skipped '{reason}'\nRan 2 tests in 0.1s\n\nOK (skipped=1)\n"
        )
        path = self.out / row["log"]
        path.write_text(text)
        row.update(gate.check_skips(text, group="project-api"), sha256=gate.digest(path))
        receipt["files"][row["log"]] = row["sha256"]
        gate.verify_commands(self.root, self.out, receipt)
        row["skips"] = []
        with self.assertRaises(gate.GateError):
            gate.verify_commands(self.root, self.out, receipt)

    def test_browser_asset_discovery_skip_is_exact_and_integration_fails_closed(self) -> None:
        test = (
            "test_native_routes_waits_dom_observation_and_actual_coverage "
            "(test_browser_asset_urls.BrowserAssetUrls."
            "test_native_routes_waits_dom_observation_and_actual_coverage)"
        )
        reason = "Chromium is installed by the later browser-check step"
        text = (
            "test_x (test_x.Fixture.test_x) ... ok\n"
            f"{test} ... skipped '{reason}'\nRan 2 tests in 0.1s\n\nOK (skipped=1)\n"
        )
        self.assertIn(reason, gate.EXPECTED_SKIP_REASONS)
        expected = {"tests": 2, "executed": 1, "skips": [{"test": test, "reason": reason}]}
        self.assertEqual(gate.check_skips(text), expected)
        self.assertEqual(gate.check_skips(text, group="project-api"), expected)
        for value, group, integration in (
            (text, "browser", True),
            (text, "project-api", True),
            (text.replace(reason, reason + " (missing dependency)"), "project-api", False),
            (text.replace(reason, "needs " + reason), "project-api", False),
            (text.replace(reason, reason.lower()), "project-api", False),
            (text.replace(reason, "missing Chromium"), "project-api", False),
            (text.replace("skipped=1", "skipped=2"), "project-api", False),
            (
                text.replace(
                    "... ok", "... skipped 'unrecognised integration/dependency reason'"
                ).replace("skipped=1", "skipped=2"),
                "project-api",
                False,
            ),
        ):
            with self.subTest(value=value, group=group, integration=integration):
                with self.assertRaises(gate.GateError):
                    gate.check_skips(value, group=group, integration=integration)

    def test_browser_asset_discovery_receipt_recomputes_skip_evidence(self) -> None:
        receipt = self.scoped_receipt(["project-api"])
        row = next(row for row in receipt["commands"] if row["suite"])
        test = (
            "test_native_routes_waits_dom_observation_and_actual_coverage "
            "(test_browser_asset_urls.BrowserAssetUrls."
            "test_native_routes_waits_dom_observation_and_actual_coverage)"
        )
        reason = "Chromium is installed by the later browser-check step"
        text = (
            "test_x (test_x.Fixture.test_x) ... ok\n"
            f"{test} ... skipped '{reason}'\nRan 2 tests in 0.1s\n\nOK (skipped=1)\n"
        )
        path = self.out / row["log"]
        path.write_text(text)
        row.update(gate.check_skips(text, group="project-api"), sha256=gate.digest(path))
        receipt["files"][row["log"]] = row["sha256"]
        gate.verify_commands(self.root, self.out, receipt)
        row["skips"] = []
        with self.assertRaises(gate.GateError):
            gate.verify_commands(self.root, self.out, receipt)

    def test_journey_import_paths_keep_safety_and_shared_fixtures(self) -> None:
        checks = gate.required_checks(
            Path("."),
            {
                "owner": "a" * 24,
                "sql": {},
                "images": {},
                "extras": [],
                "executed_groups": ["browser"],
            },
        )
        journey = next(row for row in checks if "checks.case_journey_browser_check" in row["argv"])
        self.assertEqual(
            journey["env"]["PYTHONPATH"],
            "<output>/safety:<checkout>/src/api/tests:<checkout>/src/core/tests:"
            "<checkout>/src/agents/tests",
        )

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
            "infra/main.bicep",
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
        self.git("switch", "-qc", "feat/receipt-fixture")

    def git(self, *args: str) -> str:
        return subprocess.check_output(
            ["git", "-C", str(self.root), *args], text=True, stderr=subprocess.PIPE
        ).strip()

    def runner(self) -> Any:
        return gate.Runner(self.root, self.out, self.base, [])

    def scoped_receipt(self, groups: list[str], *, passed: bool = False) -> dict[str, Any]:
        selected = gate.selection(self.root, self.base, "changed", [])
        receipt: dict[str, Any] = {
            "schema": 4,
            "scope": "partial",
            "status": "passed" if passed else "failed",
            "resume_eligible": not passed,
            "resume": None,
            "selection": selected,
            "groups": groups,
            "executed_groups": groups,
            "identity": gate.clean_identity(self.root, self.base),
            "tools": {},
            "owner": "a" * 24,
            "sql": {},
            "images": {},
            "extras": [],
            "commands": [],
            "files": {},
        }
        for name in gate.selected_environments(groups):
            environment = self.out / "venvs" / name
            venv.EnvBuilder(with_pip=False, symlinks=True).create(environment)
            metadata = environment / "lib/python3.12/site-packages/fixture.dist-info"
            metadata.mkdir()
            (metadata / "METADATA").write_text("Name: fixture\nVersion: 1.0\n")
        for index, check in enumerate(gate.required_checks(self.root, receipt)):
            row = {k: v for k, v in check.items() if k not in ("probe", "attempts")}
            name = f"{index:04d}-{check['group']}.log"
            text = ""
            if check["suite"]:
                text = "test_x ... ok\nRan 1 test in 0.1s\n\nOK\n"
                if gate.CHAT_PANEL_BROWSER_SELECTOR in check["argv"]:
                    text = f"{gate.CHAT_PANEL_DISCOVERY_SKIP[0]} ... ok\nRan 1 test in 0.1s\n\nOK\n"
                if gate.EMPLOYEE_ACCEPTANCE_BROWSER_MODULE in check["argv"]:
                    text = "test_x ... ok\n" * 3 + "Ran 3 tests in 0.1s\n\nOK\n"
                row.update(gate.check_skips(text))
            (self.out / name).write_text(text)
            row.update(exit_code=0, log=name, sha256=gate.digest(self.out / name))
            receipt["commands"].append(row)
        (self.out / "snapshot-inputs.log").write_text("")
        receipt["environments"] = gate.environment_identity(
            self.out, gate.selected_environments(groups)
        )
        receipt["files"] = {
            path.name: gate.digest(path) for path in self.out.iterdir() if path.is_file()
        }
        self.seal(receipt)
        return receipt

    def seal(self, receipt: dict[str, Any]) -> Path:
        path = self.out / "receipt.json"
        gate.atomic_json(path, receipt)
        (self.out / "receipt.sha256").write_text(gate.digest(path))
        return path

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
        self.assertIn("shellcheck", gate.TOOLS)
        runner = self.runner()
        runner.snapshot = self.root
        with (
            patch.object(
                gate.shutil,
                "which",
                side_effect=lambda name: None if name == "shellcheck" else sys.executable,
            ),
            patch.object(runner, "command") as command,
        ):
            with self.assertRaisesRegex(gate.GateError, "Missing required tool: shellcheck"):
                gate.tool_identity()
            runner.preflight()
            command.assert_not_called()
        self.assertEqual(runner.failures, ["preflight: Missing required tool: shellcheck"])
        binary = self.out / "shellcheck"
        binary.write_bytes(b"original tool identity")
        with (
            patch.object(
                gate.shutil,
                "which",
                side_effect=lambda name: str(binary) if name == "shellcheck" else sys.executable,
            ),
            patch.object(gate.subprocess, "check_output", return_value="fixture-docker\n"),
        ):
            before = gate.tool_identity()
            binary.write_bytes(b"changed tool identity")
            after = gate.tool_identity()
        self.assertNotEqual(before["shellcheck"], after["shellcheck"])
        self.assertEqual(
            {name: value for name, value in before.items() if name != "shellcheck"},
            {name: value for name, value in after.items() if name != "shellcheck"},
        )
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
        real_open = os.open
        lock_paths = []

        def open_lock(path: Path, flags: int, mode: int) -> int:
            lock_paths.append(path)
            return real_open(self.out / "owned-host-lock", flags, mode)

        for directory in ("/caller-one/scratch", "/caller-two/scratch"):
            with (
                patch.dict(os.environ, {"TMPDIR": directory, "TEMP": directory, "TMP": directory}),
                patch.object(gate.os, "open", side_effect=open_lock),
                gate.heavy_lock(1),
            ):
                pass
        self.assertEqual(lock_paths, [Path("/tmp/ama-rpi-heavy.lock")] * 2)

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
        real_run = gate.subprocess.run
        for retry in (False, True):
            with self.subTest(retry=retry):
                output = self.out / f"cancel-{retry}"
                output.mkdir()
                cancelled = gate.Runner(self.root, output, self.base, [])
                child = Mock(pid=987654321)
                child.communicate.side_effect = [
                    KeyboardInterrupt("Interrupted by signal 15"),
                    ("owned child stopped\n", None),
                ]
                metadata = {
                    "Id": "c" * 64,
                    "Config": {"Labels": {"ama.rpi.owner": cancelled.token}},
                }
                docker_commands: list[list[str]] = []

                def owned_run(
                    argv: list[str],
                    *,
                    metadata: dict[str, Any] = metadata,
                    docker_commands: list[list[str]] = docker_commands,
                    **kwargs: Any,
                ) -> Any:
                    if argv[0] != "docker":
                        return real_run(argv, **kwargs)
                    docker_commands.append(argv)
                    return subprocess.CompletedProcess(argv, 0, json.dumps([metadata]), "")

                def interrupt(
                    cancelled: Any = cancelled, child: Any = child, retry: bool = retry
                ) -> None:
                    with (
                        patch.object(gate.subprocess, "Popen", return_value=child),
                        patch.object(gate.os, "killpg") as killpg,
                        cancelled.gate("mssql"),
                    ):
                        cancelled.containers.add("c" * 64)
                        try:
                            cancelled.command(["fixture-child"], retry=retry)
                        finally:
                            killpg.assert_called_once_with(child.pid, gate.signal.SIGINT)
                        self.fail("Cancellation continued to the next command")

                with (
                    patch.object(cancelled, "preflight", side_effect=interrupt),
                    patch.object(cancelled, "projects") as projects,
                    patch.object(cancelled, "namespace_static_infra") as later,
                    patch.object(gate, "tool_identity", return_value={}),
                    patch.object(gate.subprocess, "run", side_effect=owned_run),
                    self.assertRaisesRegex(gate.GateError, "Interrupted by signal 15"),
                ):
                    cancelled.run()
                projects.assert_not_called()
                later.assert_not_called()
                self.assertEqual(
                    docker_commands,
                    [["docker", "inspect", "c" * 64], ["docker", "rm", "-f", "c" * 64]],
                )
                receipt = json.loads((output / "receipt.json").read_text())
                self.assertEqual(receipt["status"], "failed")
                self.assertEqual(receipt["groups"], [])
                self.assertEqual(len(receipt["commands"]), 1)
                row = receipt["commands"][0]
                self.assertEqual(row["exit_code"], 130)
                self.assertTrue(row["interrupted"])
                self.assertNotIn("expected_probe_failure", row)
                self.assertFalse(cancelled.snapshot.exists())
                self.assertFalse(cancelled.containers)

    def test_tampered_or_failed_receipt_refuses_without_executing_content(self) -> None:
        path = self.out / "receipt.json"
        gate.atomic_json(path, {"status": "passed", "argv": ["do-not-execute"]})
        (self.out / "receipt.sha256").write_text("wrong\n")
        with patch.object(gate.subprocess, "run") as run, self.assertRaises(gate.GateError):
            gate.verify(self.root, path, self.base)
        run.assert_not_called()
        gate.atomic_json(path, {"schema": 3, "status": "failed"})
        (self.out / "receipt.sha256").write_text(gate.digest(path))
        with self.assertRaises(gate.GateError):
            gate.verify(self.root, path, self.base)
        for name in (*gate.PROJECTS, "namespace"):
            environment = self.out / "venvs" / name
            venv.EnvBuilder(with_pip=False, symlinks=True).create(environment)
            site = environment / "lib/python3.12/site-packages"
            distribution = site / "fixture-1.0.dist-info"
            distribution.mkdir()
            (distribution / "METADATA").write_text("Name: fixture\nVersion: 1.0\n")
            (distribution / "direct_url.json").write_text('{"url":"file:///fixture"}\n')
            (site / "fixture.pth").write_text("# inert fixture\n")
        receipt = {
            "schema": 4,
            "scope": "full",
            "selection": {"mode": "all", "paths": [], "groups": gate.required_groups([])},
            "executed_groups": gate.required_groups([]),
            "resume": None,
            "status": "passed",
            "identity": gate.clean_identity(self.root, self.base),
            "tools": {"shellcheck": {"sha256": "e" * 64}},
            "environments": gate.environment_identity(self.out),
            "extras": [],
            "groups": gate.required_groups([]),
            "owner": "a" * 24,
            "sql": {"container": "b" * 64, "port": "25432"},
            "commands": [],
            "files": {
                "axe-4.10.3.min.js": "fixture",
                "regulatory-ux-results.json": "fixture",
                "case-journey-results.json": "fixture",
                "workflow-coverage.json": "fixture",
                "browser-bytecode-policy.pth": "fixture",
                "snapshot-inputs.log": "fixture",
                **{f"{p}-{s}.json": "fixture" for p in gate.IMAGES for s in ("gate", "all")},
                **{f"{p}.spdx.json": "fixture" for p in gate.IMAGES},
            },
            "trivy_database": {},
            "images": {
                "mssql": "sha256:" + "c" * 64,
                **{
                    name: {
                        "id": "sha256:" + "d" * 64,
                        "tag": "zava-forward-"
                        + ("api" if name == "logo-0600" else name.removeprefix("image-"))
                        + ":rpi-"
                        + "a" * 24
                        + ("-logo0600" if name == "logo-0600" else ""),
                    }
                    for name in ("logo-0600", *[f"image-{p}" for p in gate.IMAGES])
                },
            },
        }
        checks = gate.required_checks(self.root, receipt)
        self.assertEqual(
            sum(gate.EMPLOYEE_ACCEPTANCE_BROWSER_MODULE in check["argv"] for check in checks),
            1,
        )
        for index, check in enumerate(checks):
            row = {key: value for key, value in check.items() if key not in ("probe", "attempts")}
            logfile = f"{index:04d}-{check['group']}.log"
            text = "fixture success\n"
            if check["suite"]:
                text = "test_x (test_x.Fixture.test_x) ... ok\nRan 1 test in 0.1s\n\nOK\n"
                if gate.CHAT_PANEL_BROWSER_SELECTOR in check["argv"]:
                    text = f"{gate.CHAT_PANEL_DISCOVERY_SKIP[0]} ... ok\nRan 1 test in 0.1s\n\nOK\n"
                if gate.EMPLOYEE_ACCEPTANCE_BROWSER_MODULE in check["argv"]:
                    text = "test_x ... ok\n" * 3 + "Ran 3 tests in 0.1s\n\nOK\n"
                row.update(gate.check_skips(text, integration=check["integration"]))
            if check["argv"][0] == "git":
                text = ""
            if check["argv"][1:3] == ["-c", gate.WORKFLOW_INVENTORY]:
                text = json.dumps({name: {"test": {"steps": []}} for name in gate.WORKFLOWS})
            (self.out / logfile).write_text(text)
            row.update(exit_code=0, log=logfile, sha256=gate.digest(self.out / logfile))
            receipt["commands"].append(row)
            receipt["files"][logfile] = row["sha256"]
        for name in receipt["files"]:
            target = self.out / name
            if target.exists():
                continue
            if name.endswith(("-gate.json", "-all.json")):
                content: Any = {
                    "Trivy": {"Version": "0.76.0"},
                    "Metadata": {"ImageID": "sha256:" + "d" * 64},
                    "Results": [{}],
                }
            elif name.endswith(".spdx.json"):
                content = {
                    "spdxVersion": "SPDX-2.3",
                    "name": "sha256:" + "d" * 64,
                    "packages": [{}],
                    "creationInfo": {"creators": ["Tool: trivy-0.76.0"]},
                }
            elif name == "regulatory-ux-results.json":
                content = {
                    "outcome": "passed",
                    "axe_status": "executed",
                    "axe_version": "4.10.3",
                    "axe_sha256": gate.AXE_SHA256,
                    "scans": [{"violations": []}],
                }
            elif name == "case-journey-results.json":
                content = {
                    "browser": "fixture Chromium",
                    "axe_version": "4.10.3",
                    "page_errors": [],
                    "zoom": "chrome.tabs.setZoom=2; innerWidth<=640",
                    "scans": [{"violations": []} for _ in range(87)],
                }
            elif name == "workflow-coverage.json":
                content = {"steps": []}
            else:
                target.write_text("")
                continue
            target.write_text(json.dumps(content))
        receipt["files"] = {name: gate.digest(self.out / name) for name in receipt["files"]}
        receipt["files"]["axe-4.10.3.min.js"] = gate.AXE_SHA256
        gate.atomic_json(path, receipt)
        (self.out / "receipt.sha256").write_text(gate.digest(path))
        real_digest = gate.digest
        real_output = gate.subprocess.check_output

        def output(argv: list[str], **kwargs: Any) -> Any:
            self.assertIn(argv[0], ("git", "docker"), "Verification must not execute environments")
            if argv[0] == "docker":
                return "sha256:" + ("c" if argv[-1].startswith("mcr.") else "d") * 64 + "\n"
            return real_output(argv, **kwargs)

        with (
            patch.object(gate, "tool_identity", return_value=receipt["tools"]),
            patch.object(gate, "scan_database", return_value={}),
            patch.object(gate.subprocess, "check_output", side_effect=output),
            patch.object(
                gate,
                "digest",
                side_effect=lambda p: (
                    gate.AXE_SHA256 if p.name == "axe-4.10.3.min.js" else real_digest(p)
                ),
            ),
        ):
            gate.verify(self.root, path, self.base)
            with (
                patch.object(
                    gate, "tool_identity", return_value={"shellcheck": {"sha256": "f" * 64}}
                ),
                self.assertRaisesRegex(gate.GateError, "Receipt tool identity mismatch"),
            ):
                gate.verify(self.root, path, self.base)
            original_receipt = copy.deepcopy(receipt)
            # Each exact mandatory command must survive, even if groups/files stay consistent.
            for index, check in enumerate(checks):
                with self.subTest(missing_command=index, group=check["group"]):
                    changed = copy.deepcopy(original_receipt)
                    removed = changed["commands"].pop(index)
                    changed["files"].pop(removed["log"])
                    gate.atomic_json(path, changed)
                    (self.out / "receipt.sha256").write_text(real_digest(path))
                    with self.assertRaises(gate.GateError):
                        gate.verify(self.root, path, self.base)
            changed = copy.deepcopy(original_receipt)
            suites = [row for row in changed["commands"] if row["suite"]]
            for row in suites:
                changed["commands"].remove(row)
                changed["files"].pop(row["log"])
            self.assertEqual(len(suites), 10)
            gate.atomic_json(path, changed)
            (self.out / "receipt.sha256").write_text(real_digest(path))
            with self.assertRaises(gate.GateError):
                gate.verify(self.root, path, self.base)
            for mutation in ("selector", "counts", "probe", "infra-env", "suite-log"):
                with self.subTest(mutation=mutation):
                    changed = copy.deepcopy(original_receipt)
                    sqlrow = next(
                        row
                        for row in changed["commands"]
                        if row["group"] == "mssql" and row["suite"]
                    )
                    if mutation == "selector":
                        sqlrow["argv"].pop()
                    elif mutation == "counts":
                        sqlrow["executed"] = 0
                    elif mutation == "probe":
                        sqlrow.update(exit_code=1, expected_probe_failure=True)
                    elif mutation == "infra-env":
                        next(
                            row
                            for row in changed["commands"]
                            if row["group"] == "infra" and row["suite"]
                        )["env"] = {}
                    else:
                        (self.out / sqlrow["log"]).write_text("no suite executed\n")
                        sqlrow["sha256"] = real_digest(self.out / sqlrow["log"])
                        changed["files"][sqlrow["log"]] = sqlrow["sha256"]
                    gate.atomic_json(path, changed)
                    (self.out / "receipt.sha256").write_text(real_digest(path))
                    with self.assertRaises(gate.GateError):
                        gate.verify(self.root, path, self.base)
                    if mutation == "suite-log":
                        (self.out / sqlrow["log"]).write_text(
                            "test_x (test_x.Fixture.test_x) ... ok\nRan 1 test in 0.1s\n\nOK\n"
                        )
            for name, key, value in (
                ("regulatory-ux-results.json", "outcome", "failed"),
                ("case-journey-results.json", "zoom", "device scale only"),
                ("case-journey-results.json", "scans", []),
                ("case-journey-results.json", "scans", [{"violations": []}] * 86),
                ("case-journey-results.json", "scans", [{"violations": []}] * 88),
                (
                    "case-journey-results.json",
                    "scans",
                    [{"violations": [{"impact": "serious"}]}] * 87,
                ),
                ("case-journey-results.json", "page_errors", ["Uncaught failure"]),
                ("api-gate.json", "Results", [{"Vulnerabilities": [{"Severity": "HIGH"}]}]),
                ("api.spdx.json", "packages", []),
                ("workflow-coverage.json", "steps", [{"coverage": "fabricated"}]),
            ):
                with self.subTest(result_evidence=name):
                    target = self.out / name
                    original_content = target.read_text()
                    report = json.loads(original_content)
                    report[key] = value
                    target.write_text(json.dumps(report))
                    changed = copy.deepcopy(original_receipt)
                    changed["files"][name] = real_digest(target)
                    gate.atomic_json(path, changed)
                    (self.out / "receipt.sha256").write_text(real_digest(path))
                    with self.assertRaises(gate.GateError):
                        gate.verify(self.root, path, self.base)
                    target.write_text(original_content)
            gate.atomic_json(path, original_receipt)
            (self.out / "receipt.sha256").write_text(real_digest(path))
            environment = self.out / "venvs/core"
            site = environment / "lib/python3.12/site-packages"
            marker = self.out / "must-not-execute"
            malicious_startup = (
                f"import pathlib; pathlib.Path({str(marker)!r}).write_text('executed')\n"
            )
            for target, content in (
                (
                    environment / "bin/python",
                    f"#!/bin/sh\nprintf executed > {marker}\n".encode(),
                ),
                (site / "fixture.pth", malicious_startup.encode()),
                (site / "sitecustomize.py", malicious_startup.encode()),
                (site / "usercustomize.py", malicious_startup.encode()),
                (site / "__editable___fixture_finder.py", malicious_startup.encode()),
                (site / "fixture-1.0.dist-info/METADATA", b"Name: fixture\nVersion: 2.0\n"),
                (site / "fixture-1.0.dist-info/direct_url.json", b'{"url":"file:///changed"}'),
                (environment / "pyvenv.cfg", b"include-system-site-packages = true\n"),
            ):
                with self.subTest(tampered=target.relative_to(environment)):
                    link = os.readlink(target) if target.is_symlink() else None
                    original = target.read_bytes() if target.exists() and link is None else None
                    mode = target.stat().st_mode if target.exists() else 0o600
                    if target.is_symlink():
                        target.unlink()
                    target.write_bytes(content)
                    target.chmod(0o700 if target.name == "python" else mode)
                    with self.assertRaises(gate.GateError):
                        gate.verify(self.root, path, self.base)
                    self.assertFalse(marker.exists(), "Untrusted interpreter/startup code executed")
                    target.unlink()
                    if link is not None:
                        target.symlink_to(link)
                    elif original is not None:
                        target.write_bytes(original)
                        target.chmod(mode)
            bounded = site / "fixture-1.0.dist-info/oversized"
            with bounded.open("wb") as stream:
                stream.truncate(8 * 1024 * 1024 + 1)
            with self.assertRaisesRegex(gate.GateError, "bounded regular"):
                gate.verify(self.root, path, self.base)
            bounded.unlink()
            for target in (site / "linked.pth", site / "fixture-1.0.dist-info/linked"):
                target.symlink_to(site / "fixture.pth")
                with self.subTest(symlink=target.name), self.assertRaises(gate.GateError):
                    gate.verify(self.root, path, self.base)
                target.unlink()
            fifo = site / "fifo.pth"
            os.mkfifo(fifo)
            with self.assertRaisesRegex(gate.GateError, "bounded regular"):
                gate.verify(self.root, path, self.base)
            fifo.unlink()
            metadata = site / "fixture-1.0.dist-info/METADATA"
            content = metadata.read_bytes()
            metadata.unlink()
            with self.assertRaisesRegex(gate.GateError, "METADATA is missing"):
                gate.verify(self.root, path, self.base)
            metadata.write_bytes(content)
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

    def test_scanned_image_builds_skip_layer_cache(self) -> None:
        fresh = gate.image_build_argv("D", "T", "C", fresh=True)
        cached = gate.image_build_argv("D", "T", "C", fresh=False)
        self.assertEqual(fresh[:4], ["docker", "build", "--no-cache", "--memory=3g"])
        self.assertIn("--cpu-quota=200000", fresh)
        self.assertNotIn("--no-cache", cached)
        self.assertEqual([a for a in fresh if a != "--no-cache"], cached)
        receipt = {
            "extras": [],
            "images": {
                "mssql": "sha256:" + "c" * 64,
                **{
                    name: {
                        "id": "sha256:" + "d" * 64,
                        "tag": "zava-forward-"
                        + ("api" if name == "logo-0600" else name.removeprefix("image-"))
                        + ":rpi-"
                        + "a" * 24
                        + ("-logo0600" if name == "logo-0600" else ""),
                    }
                    for name in ("logo-0600", *[f"image-{p}" for p in gate.IMAGES])
                },
            },
            "owner": "a" * 24,
            "sql": {"container": "b" * 64, "port": "25432"},
        }
        builds = {}
        for check in gate.required_checks(self.root, receipt):
            if check["argv"][:2] == ["docker", "build"]:
                builds[check["group"]] = check["argv"]
        self.assertEqual(len(builds), 5)
        for group, argv in builds.items():
            self.assertEqual("--no-cache" in argv, group != "logo-0600", group)

    def test_changed_selection_mapping_and_closure(self) -> None:
        cases = {
            "docs/example.md": {"preflight", "namespace", "static"},
            ".github/agents/ama-backlog-delivery-coordinator.agent.md": {
                "preflight",
                "namespace",
                "static",
            },
            ".copilot-tracking/rpi-sessions/state.json": {"preflight", "namespace", "static"},
            "tools/rpi-checks.py": {"preflight", "namespace", "static", "tooling"},
            "tools/test_rpi_checks.py": {"preflight", "namespace", "static", "tooling"},
            "infra/tests/test_deploy.py": {"preflight", "namespace", "static", "infra"},
            "src/agents/tests/test_example.py": {
                "preflight",
                "namespace",
                "static",
                "project-agents",
                "project-api",
            },
            "src/api/checks/example.py": {
                "preflight",
                "namespace",
                "static",
                "project-api",
                "browser",
            },
            "src/core/tests/test_example.py": {
                "preflight",
                "namespace",
                "static",
                *[f"project-{p}" for p in gate.PROJECTS],
            },
            "src/api/requirements.txt": {
                "preflight",
                "namespace",
                "static",
                "project-api",
                "image-api",
                "logo-0600",
                "mssql",
            },
            "src/orchestrator/Dockerfile": {
                "preflight",
                "namespace",
                "static",
                "project-orchestrator",
                "image-orchestrator",
            },
            "src/core/src/zava_forward/core/mssqlstore.py": set(gate.required_groups([]))
            - {"infra", "migration", "browser"},
        }
        for path, expected in cases.items():
            with self.subTest(path=path):
                self.assertEqual(set(gate.changed_groups([path], [])), expected)
        for path in (
            "unknown",
            "tools/another.py",
            ".github/workflows/src-ci.yml",
            "src/trivy.yaml",
            "src/check-container.py",
            "src/.dockerignore",
        ):
            with self.subTest(path=path):
                self.assertEqual(
                    gate.changed_groups(["docs/example.md", path], []), gate.required_groups([])
                )
        self.assertEqual(gate.changed_groups([], []), ["preflight", "namespace", "static"])
        extras = gate.changed_groups([], ["api:test_fixture.Case.test_method"])
        self.assertIn("project-api", extras)
        self.assertIn("extra-api:test_fixture.Case.test_method", extras)

    def test_changed_selection_tracks_deleted_renamed_and_unusual_paths(self) -> None:
        source = self.root / "tools/rpi-checks.py"
        renamed = self.root / "docs/name\nwith\ttabs.md"
        renamed.parent.mkdir()
        source.rename(renamed)
        self.git("add", "-A")
        self.git(
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.test",
            "commit",
            "-qm",
            "rename",
        )
        selected = gate.selection(self.root, self.base, "changed", [])
        self.assertEqual(
            set(selected["paths"]), {"tools/rpi-checks.py", "docs/name\nwith\ttabs.md"}
        )
        self.assertIn("tooling", selected["groups"])

    def test_partial_scope_is_rejected_by_default_before_live_probes(self) -> None:
        path = self.out / "receipt.json"
        for scope in (None, "partial", "invalid"):
            gate.atomic_json(path, {"schema": 4, "status": "passed", "scope": scope})
            with patch.object(gate, "tool_identity") as tools, self.assertRaises(gate.GateError):
                gate.verify(self.root, path, self.base)
            tools.assert_not_called()
        gate.atomic_json(path, {"scope": "partial"})
        with patch.object(
            gate,
            "validate_receipt",
            return_value={"scope": "partial", "identity": {"head": "h", "base": "b"}},
        ) as validate:
            gate.verify(self.root, path, self.base, required_scope="partial")
        validate.assert_called_once()

    def test_partial_contract_has_no_unselected_resources(self) -> None:
        receipt = {
            "owner": "a" * 24,
            "sql": {},
            "images": {},
            "extras": [],
            "executed_groups": ["preflight", "namespace", "static", "tooling"],
        }
        checks = gate.required_checks(self.root, receipt)
        self.assertEqual({c["group"] for c in checks}, set(receipt["executed_groups"]))
        self.assertFalse(any(c["argv"][:2] == ["docker", "build"] for c in checks))
        with patch.object(gate, "digest", return_value="not-axe"):
            (self.out / "snapshot-inputs.log").write_text("")
            gate.verify_results(self.out, receipt)

    def test_commands_accept_cross_group_interleaving_not_in_group_reordering(self) -> None:
        receipt: dict[str, Any] = {
            "owner": "a" * 24,
            "sql": {},
            "images": {},
            "extras": [],
            "executed_groups": ["preflight", "static"],
            "commands": [],
            "files": {},
        }
        for index, check in enumerate(gate.required_checks(self.root, receipt)):
            row = {k: v for k, v in check.items() if k not in ("probe", "attempts")}
            name = f"{index:04d}-{check['group']}.log"
            text = "fixture"
            if check["suite"]:
                text = "test_x ... ok\nRan 1 test in 0.1s\n\nOK\n"
                row.update(gate.check_skips(text))
            if check["argv"][0] == "git":
                text = ""
            (self.out / name).write_text(text)
            row.update(exit_code=0, log=name, sha256=gate.digest(self.out / name))
            receipt["commands"].append(row)
            receipt["files"][name] = row["sha256"]
        rows = receipt["commands"]
        receipt["commands"] = rows[7:8] + rows[:7] + rows[8:]
        gate.verify_commands(self.root, self.out, receipt)
        receipt["commands"][1:3] = reversed(receipt["commands"][1:3])
        with self.assertRaises(gate.GateError):
            gate.verify_commands(self.root, self.out, receipt)

    def test_parallel_scheduler_overlaps_independent_groups_and_blocks_dependents(self) -> None:
        runner = self.runner()
        runner.jobs = 2
        runner.groups = ["namespace"]
        barrier = threading.Barrier(2)
        seen = []

        def dispatch(group: str) -> None:
            barrier.wait(timeout=5)
            seen.append(group)
            runner.groups.append(group)

        with patch.object(runner, "dispatch", side_effect=dispatch):
            runner.schedule(["project-core", "project-agents"])
        self.assertEqual(set(seen), {"project-core", "project-agents"})
        runner.groups = ["namespace"]
        seen.clear()

        def fail(group: str) -> None:
            seen.append(group)
            runner.failures.append(f"{group}: fixture failure")

        with patch.object(runner, "dispatch", side_effect=fail):
            runner.schedule(["project-api", "browser", "mssql"])
        self.assertEqual(seen, ["project-api"])
        self.assertTrue(any("browser: blocked" in failure for failure in runner.failures))

    def test_parallel_commands_have_unique_logs_and_thread_local_groups(self) -> None:
        runner = self.runner()
        runner.snapshot = self.root
        runner.jobs = 2
        barrier = threading.Barrier(2)

        def dispatch(group: str) -> None:
            with runner.gate(group):
                barrier.wait(timeout=5)
                runner.command([sys.executable, "-c", "print('parallel')"])

        with patch.object(runner, "dispatch", side_effect=dispatch):
            runner.schedule(["project-core", "project-agents"])
        self.assertEqual(len({row["log"] for row in runner.rows}), 2)
        self.assertEqual({row["group"] for row in runner.rows}, {"project-core", "project-agents"})
        self.assertFalse(runner.active)

    def test_sql_and_image_resources_are_serial(self) -> None:
        runner = self.runner()
        runner.jobs = 3
        runner.groups = ["namespace", "project-api"]
        active = 0
        peak = 0
        mutex = threading.Lock()

        def work(*args: Any, **kwargs: Any) -> None:
            nonlocal active, peak
            with mutex:
                active += 1
                peak = max(active, peak)
            threading.Event().wait(0.02)
            with mutex:
                active -= 1
            group = (
                "mssql" if not args else "logo-0600" if kwargs.get("stress") else f"image-{args[0]}"
            )
            runner.groups.append(group)

        with (
            patch.object(runner, "sql", side_effect=work),
            patch.object(runner, "image", side_effect=work),
        ):
            runner.schedule(["mssql", "image-api", "image-agents", "logo-0600"])
        self.assertEqual(peak, 1)

    def test_worker_limit_respects_cpu_memory_and_invalid_jobs(self) -> None:
        real_read = Path.read_text
        real_exists = Path.exists
        values = {
            "/sys/fs/cgroup/cpu.max": "400000 100000",
            "/proc/meminfo": "MemAvailable: 16000000 kB\n",
            "/sys/fs/cgroup/memory.max": str(16 * 1024**3),
            "/sys/fs/cgroup/memory.current": str(1024**3),
        }

        def read(path: Path, *args: Any, **kwargs: Any) -> str:
            return values[str(path)] if str(path) in values else real_read(path, *args, **kwargs)

        with (
            patch.object(Path, "read_text", read),
            patch.object(Path, "exists", lambda p: str(p) in values or real_exists(p)),
            patch.object(gate.os, "sched_getaffinity", return_value=set(range(8))),
            patch.object(gate, "cgroup_directories", return_value=[Path("/sys/fs/cgroup")]),
        ):
            self.assertEqual(gate.worker_limit(8), 2)
            values["/sys/fs/cgroup/cpu.max"] = "150000 100000"
            with self.assertRaises(gate.GateError):
                gate.worker_limit(2)
            values["/sys/fs/cgroup/cpu.max"] = "max 100000"
            values["/sys/fs/cgroup/memory.max"] = str(4 * 1024**3)
            with self.assertRaises(gate.GateError):
                gate.worker_limit(1)
            values["/sys/fs/cgroup/memory.max"] = "max"
            self.assertEqual(gate.worker_limit(8), 3)
            for jobs in (0, -1):
                with self.assertRaises(gate.GateError):
                    gate.worker_limit(jobs)

    def test_sql_dependency_manifests_select_the_real_consumer(self) -> None:
        for path in (
            "src/api/requirements.txt",
            "src/api/requirements.in",
            "src/api/pyproject.toml",
            "src/core/pyproject.toml",
        ):
            with self.subTest(path=path):
                selected = gate.changed_groups([path], [])
                self.assertIn("mssql", selected)
                self.assertIn("project-api", selected)

    def test_api_extra_suites_wait_for_shared_environment_writers(self) -> None:
        for completed in (["namespace", "project-api"], ["namespace", "project-api", "setup-api"]):
            output = self.out / str(len(completed))
            output.mkdir()
            runner = gate.Runner(self.root, output, self.base, [])
            runner.groups = completed
            runner.jobs = 3
            seen: list[str] = []
            active = 0
            peak = 0
            mutex = threading.Lock()

            def work(
                group: str, *, mutex: Any = mutex, seen: list[str] = seen, runner: Any = runner
            ) -> None:
                nonlocal active, peak
                with mutex:
                    active += 1
                    peak = max(peak, active)
                    seen.append(group)
                threading.Event().wait(0.01)
                with mutex:
                    active -= 1
                runner.groups.append(group)

            groups = [
                "browser",
                "mssql",
                "extra-api:test_a.Case.test_a",
                "extra-api:test_b.Case.test_b",
            ]
            with patch.object(runner, "dispatch", side_effect=work):
                runner.schedule(groups)
            self.assertEqual(seen, groups)
            self.assertEqual(peak, 1)

    def test_worker_limit_intersects_nested_cgroups_and_ancestors(self) -> None:
        mount = self.out / "cgroups"
        nested = mount / "user/session"
        nested.mkdir(parents=True)
        for directory in (mount, nested.parent, nested):
            (directory / "cpu.max").write_text("max 100000")
            (directory / "memory.max").write_text("max")
            (directory / "memory.current").write_text(str(1024**3))
        (nested / "cpu.max").write_text("200000 100000")
        (nested / "memory.max").write_text(str(5 * 1024**3))
        real_read = Path.read_text
        values = {
            "/proc/self/cgroup": "0::/user/session\n",
            "/proc/self/mountinfo": f"29 23 0:26 / {mount} rw - cgroup2 cgroup rw\n",
            "/proc/meminfo": "MemAvailable: 64000000 kB\n",
        }

        def read(path: Path, *args: Any, **kwargs: Any) -> str:
            return values[str(path)] if str(path) in values else real_read(path, *args, **kwargs)

        with (
            patch.object(Path, "read_text", read),
            patch.object(gate.os, "sched_getaffinity", return_value=set(range(16))),
        ):
            self.assertEqual(gate.cgroup_directories(), [nested, nested.parent, mount])
            with self.assertRaises(gate.GateError):
                gate.worker_limit(8)
            (nested / "memory.max").write_text(str(6 * 1024**3))
            self.assertEqual(gate.worker_limit(8), 1)
            (nested.parent / "cpu.max").write_text("150000 100000")
            with self.assertRaises(gate.GateError):
                gate.worker_limit(8)
            (nested.parent / "cpu.max").write_text("max 100000")
            (nested.parent / "memory.max").write_text(str(5 * 1024**3))
            with self.assertRaises(gate.GateError):
                gate.worker_limit(8)
            values["/proc/self/cgroup"] = "0::/../../hidden\n"
            with self.assertRaisesRegex(gate.GateError, "membership"):
                gate.worker_limit(8)
            values["/proc/self/cgroup"] = "0::/user/session\n"
            values["/proc/self/mountinfo"] = ""
            with self.assertRaisesRegex(gate.GateError, "mount"):
                gate.worker_limit(8)

    def test_real_partial_fixture_requires_matching_selection_and_evidence(self) -> None:
        receipt = self.scoped_receipt(["preflight", "namespace", "static"], passed=True)
        path = self.out / "receipt.json"
        with patch.object(gate, "tool_identity", return_value={}):
            gate.verify(self.root, path, self.base, required_scope="partial")
            for key, value in (
                ("scope", "full"),
                ("groups", ["preflight"]),
                ("executed_groups", []),
                ("selection", {"mode": "changed", "paths": ["fake"], "groups": []}),
            ):
                mutated = dict(receipt, **{key: value})
                self.seal(mutated)
                with self.subTest(key=key), self.assertRaises(gate.GateError):
                    gate.verify(self.root, path, self.base, required_scope="partial")
            self.seal(receipt)
            (self.out / receipt["commands"][0]["log"]).write_text("tampered")
            with self.assertRaises(gate.GateError):
                gate.verify(self.root, path, self.base, required_scope="partial")

    def test_resume_reuses_successes_without_replaying_commands(self) -> None:
        parent = self.scoped_receipt(["preflight", "namespace"])
        parent_path = self.out / "receipt.json"
        before = {name: (self.out / name).read_bytes() for name in parent["files"]}
        new_out = Path(self.temp.name) / "resume"
        new_out.mkdir()
        runner = gate.Runner(
            self.root, new_out, self.base, [], selected=parent["selection"], resume=parent_path
        )
        observed = []

        def fake_setup(name: str, packages: list[str], dev: bool = True) -> None:
            observed.append((runner.group, name))
            # Setup identity is independently bound; parent environments stay untouched.
            environment = runner.envs / name
            venv.EnvBuilder(with_pip=False, symlinks=True).create(environment)
            metadata = environment / "lib/python3.12/site-packages/fixture.dist-info"
            metadata.mkdir()
            (metadata / "METADATA").write_text("Name: fixture\nVersion: 1.0\n")
            template = {
                "owner": runner.token,
                "sql": {},
                "images": {},
                "extras": [],
                "executed_groups": [runner.group],
            }
            for check in gate.required_checks(self.root, template):
                fake_command(check)

        def fake_command(check: dict[str, Any]) -> None:
            row = {k: v for k, v in check.items() if k not in ("probe", "attempts")}
            name = f"{len(runner.rows):04d}-{check['group']}.log"
            text = ""
            if check["suite"]:
                text = "test_x ... ok\nRan 1 test in 0.1s\n\nOK\n"
                row.update(gate.check_skips(text))
            (new_out / name).write_text(text)
            row.update(exit_code=0, log=name, sha256=gate.digest(new_out / name))
            runner.rows.append(row)

        def fake_static(group: str) -> None:
            self.assertEqual(group, "static")
            observed.append(("executed", group))
            template = {
                "owner": runner.token,
                "sql": {},
                "images": {},
                "extras": [],
                "executed_groups": [group],
            }
            for check in gate.required_checks(self.root, template):
                fake_command(check)
            runner.groups.append(group)

        with (
            patch.object(gate, "tool_identity", return_value={}),
            patch.object(runner, "install", side_effect=fake_setup),
            patch.object(runner, "dispatch", side_effect=fake_static),
            patch.object(runner, "preflight") as preflight,
        ):
            path = runner.run()
            gate.verify(self.root, path, self.base, required_scope="partial")
            preflight.assert_not_called()
            final = json.loads(path.read_text())
            self.assertEqual(final["groups"], parent["selection"]["groups"])
            self.assertEqual(final["executed_groups"], ["static", "setup-namespace"])
            self.assertEqual(observed, [("setup-namespace", "namespace"), ("executed", "static")])
            self.assertEqual(final["resume"]["sha256"], gate.digest(parent_path))
            for name, content in before.items():
                self.assertEqual((self.out / name).read_bytes(), content)
            (self.out / parent["commands"][0]["log"]).write_text("parent tamper")
            with self.assertRaises(gate.GateError):
                gate.verify(self.root, path, self.base, required_scope="partial")

    def test_resume_rejects_identity_checkpoint_tool_and_environment_drift(self) -> None:
        parent = self.scoped_receipt(["preflight", "namespace"])
        path = self.out / "receipt.json"
        with patch.object(gate, "tool_identity", return_value={}):
            gate.validate_receipt(self.root, path, self.base, passing=False)
            self.seal(dict(parent, resume_eligible=False))
            with self.assertRaisesRegex(gate.GateError, "checkpoint"):
                gate.validate_receipt(self.root, path, self.base, passing=False)
            self.seal(parent)
            with (
                patch.object(gate, "tool_identity", return_value={"changed": {}}),
                self.assertRaises(gate.GateError),
            ):
                gate.validate_receipt(self.root, path, self.base, passing=False)
            metadata = (
                self.out / "venvs/namespace/lib/python3.12/site-packages/fixture.dist-info/METADATA"
            )
            original = metadata.read_text()
            metadata.write_text("changed")
            with self.assertRaises(gate.GateError):
                gate.validate_receipt(self.root, path, self.base, passing=False)
            metadata.write_text(original)
            self.git(
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=fixture@example.test",
                "commit",
                "--allow-empty",
                "-qm",
                "changed head",
            )
            with self.assertRaises(gate.GateError):
                gate.validate_receipt(self.root, path, self.base, passing=False)

    def test_scheduler_orders_shared_environments_and_cancels_before_cleanup(self) -> None:
        runner = self.runner()
        runner.jobs = 3
        runner.groups = ["namespace", "project-api"]
        observed = []

        def record(group: str) -> None:
            observed.append(group)
            runner.groups.append(group)

        with patch.object(runner, "dispatch", side_effect=record):
            runner.schedule(["static", "infra", "migration", "tooling", "browser", "mssql"])
        self.assertLess(observed.index("static"), observed.index("infra"))
        self.assertLess(observed.index("infra"), observed.index("migration"))
        self.assertLess(observed.index("migration"), observed.index("tooling"))
        self.assertLess(observed.index("browser"), observed.index("mssql"))
        with (
            patch.object(runner, "dispatch", side_effect=KeyboardInterrupt),
            self.assertRaises(KeyboardInterrupt),
        ):
            runner.schedule(["project-core"])
        self.assertTrue(runner.cancelled.is_set())
        with self.assertRaises(gate.GateError):
            runner.command(["must-not-execute"])

    def test_runner_image_build_uses_shared_argv(self) -> None:
        runner = self.runner()
        runner.snapshot = self.root
        seen: list[list[str]] = []

        def record(argv: list[str], **kwargs: Any) -> str:
            seen.append(argv)
            if argv[:2] == ["docker", "build"]:
                raise RuntimeError("stop after build")
            return ""

        for stress in (False, True):
            seen.clear()
            with (
                patch.object(runner, "command", side_effect=record),
                patch.object(runner, "python", return_value="python3"),
                patch.object(gate.shutil, "copytree"),
                patch.object(Path, "chmod"),
            ):
                with self.assertRaises(RuntimeError):
                    runner.image("api", stress=stress)
            builds = [a for a in seen if a[:2] == ["docker", "build"]]
            self.assertEqual(len(builds), 1)
            self.assertEqual("--no-cache" in builds[0], not stress)

    def test_matrix_drift_and_unreviewed_extra_commands_refuse(self) -> None:
        self.assertEqual(len(gate.required_groups([])), 17)
        self.assertEqual(gate.SQL_SELECTORS[0], "test_mssqlstore")
        self.assertEqual(set(gate.WORKFLOW_HASHES), set(gate.WORKFLOWS))
        root = Path(__file__).resolve().parents[1]
        for name in gate.WORKFLOWS:
            with self.subTest(workflow=name):
                self.assertEqual(
                    gate.WORKFLOW_HASHES[name], gate.digest(root / ".github/workflows" / name)
                )
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
            runner.rows.append({"group": runner.group})
            return "Python 3.12.3" if argv[0] == "python3" else "Version: 0.76.0"

        with (
            patch.object(runner, "command", side_effect=version) as command,
            patch.object(gate, "tool_identity", return_value={}),
            patch.dict(
                gate.WORKFLOW_HASHES,
                {
                    name: gate.digest(self.root / ".github/workflows" / name)
                    for name in gate.WORKFLOWS
                },
            ),
        ):
            runner.preflight()
            self.assertEqual(runner.failures, [])
            for name in gate.WORKFLOWS:
                with self.subTest(drift=name):
                    path = self.root / ".github/workflows" / name
                    original = path.read_bytes()
                    path.write_bytes(original + b"# changed\n")
                    runner.preflight()
                    self.assertEqual(runner.failures, [f"preflight: Workflow matrix drift: {name}"])
                    path.write_bytes(original)
                    runner.failures.clear()
        command.assert_any_call(["shellcheck", "--version"], timeout=60)

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
