"""Fixed synthetic discovery demonstration command (Refs #125)."""

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

from zava_forward.core import discovery_assistant_boundary as boundary
from zava_forward.core import discovery_assistant_demo as demo
from zava_forward.core import discovery_assistant_drafting as drafting
from zava_forward.core.version import __version__

CORE_ROOT = Path(__file__).resolve().parents[1]


def run_module(*args: str, env: dict[str, str] | None = None, cwd: str | None = None) -> Any:
    return subprocess.run(
        [sys.executable, "-m", "zava_forward.core", *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd,
        check=False,
    )


class ReportTests(unittest.TestCase):
    def test_fixture_hours_references_and_gaps(self) -> None:
        report = demo.run_demo()
        calc = report["calculation"]
        self.assertEqual(calc["hours"], {"design": 60.0, "install": 12.0, "survey": 36.5})
        self.assertEqual(calc["source_references"][0], "SYN-EVT-001")
        self.assertNotIn("SYN-EVT-007", calc["source_references"])
        self.assertEqual(calc["gaps"], ["unusable-timestamp:SYN-P2/install"])
        self.assertEqual(
            report["conventional_table"]["rows"],
            [
                {"stage": "design", "hours": 60.0},
                {"stage": "install", "hours": 12.0},
                {"stage": "survey", "hours": 36.5},
            ],
        )
        self.assertTrue(report["expected_arithmetic"]["passed"])
        self.assertTrue(report["overall_passed"])
        self.assertTrue(report["fixture"]["explicitly_fictional"])
        self.assertEqual(report["core_version"], __version__)

    def test_not_ready_deny_and_unapproved(self) -> None:
        report = demo.run_demo()
        self.assertEqual(report["readiness"]["status"], boundary.NOT_READY)
        self.assertEqual(len(report["readiness"]["missing"]), 10)
        self.assertEqual(report["readiness"]["satisfied"], [])
        self.assertFalse(report["readiness"]["connection_to_company_data_permitted"])
        self.assertEqual(report["company_connection"], "DENY")
        self.assertEqual(report["design_hypothesis_status"], "UNAPPROVED_DESIGN_HYPOTHESIS")
        self.assertFalse(report["approved_solution"])

    def test_refused_decisions_are_never_dispatched(self) -> None:
        decisions = {d["tool"]: d for d in demo.run_demo()["authority_decisions"]}
        write = decisions["write_source_system"]
        self.assertFalse(write["allowed"])
        self.assertEqual(write["reason"], "DENIED_BY_AUTHORITY_BOUNDARY")
        self.assertFalse(decisions["read_company_dataset"]["allowed"])
        for decision in decisions.values():
            self.assertFalse(decision["dispatched"])
            self.assertFalse(decision["attempted"])
            self.assertFalse(decision["writes_to_source_system"])

    def test_draft_is_deterministic_fallback_without_model(self) -> None:
        draft = demo.run_demo()["draft"]
        self.assertEqual(draft["text"], demo.EXPECTED_DRAFT_TEXT)
        self.assertFalse(draft["model_used"])
        self.assertEqual(draft["fallback_reason"], "NO_DRAFTER")
        self.assertEqual(draft["status"], drafting.DRAFT_FOR_HUMAN_REVIEW)
        self.assertFalse(draft["validated_finding"])

    def test_human_and_model_proof_is_absent(self) -> None:
        comparison = demo.run_demo()["comparison"]
        self.assertFalse(comparison["criterion_met"])
        self.assertFalse(comparison["assistant_preferred"])
        self.assertEqual(comparison["human_result_pointers"], [])
        self.assertEqual(comparison["comparable_measures"], [])
        self.assertEqual(len(comparison["missing_by_measure"]), 10)
        for methods in comparison["missing_by_measure"].values():
            self.assertEqual(len(methods), 4)

    def test_repeatability_and_render_are_stable(self) -> None:
        first, second = demo.run_demo(), demo.run_demo()
        self.assertEqual(demo.render(first), demo.render(second))
        self.assertTrue(first["repeatability"]["identical"])
        self.assertEqual(first["repeatability"]["runs"], 3)
        self.assertEqual(json.loads(demo.render(first)), first)


class FailureTests(unittest.TestCase):
    def run_main(self, *args: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = demo.main(args)
        return code, out.getvalue(), err.getvalue()

    def test_expectation_mismatch_fails_command(self) -> None:
        with mock.patch.object(demo, "EXPECTED_HOURS", {"design": 61.0, "install": 12.0}):
            code, out, err = self.run_main()
        report = json.loads(out)
        self.assertEqual(code, 1)
        self.assertEqual(report["expected_arithmetic"]["mismatches"], ["hours"])
        self.assertFalse(report["overall_passed"])
        self.assertIn("failed", err)

    def test_repeatability_failure_fails_command(self) -> None:
        counter = iter(range(100))

        def drifting(_events: Any) -> dict[str, Any]:
            return {
                "hours": demo.EXPECTED_HOURS,
                "n": next(counter),
                "source_references": [],
                "gaps": [],
            }

        with mock.patch.object(demo, "_calculate", drifting):
            report = demo.run_demo()
            code, _out, _err = self.run_main()
        self.assertFalse(report["repeatability"]["identical"])
        self.assertFalse(report["overall_passed"])
        self.assertEqual(code, 1)

    def test_unknown_arguments_fail_explicitly(self) -> None:
        code, out, err = self.run_main("--path", "x")
        self.assertEqual(code, 2)
        self.assertEqual(out, "")
        self.assertIn("no arguments", err)

    def test_no_environment_or_file_access(self) -> None:
        def refuse(*_a: Any, **_k: Any) -> Any:
            raise AssertionError("demo touched environment or filesystem")

        with (
            mock.patch("builtins.open", refuse),
            mock.patch.object(os, "getenv", refuse),
            mock.patch.object(os.environ, "get", refuse),
            mock.patch.object(os.environ, "__getitem__", refuse),
            mock.patch.object(Path, "home", refuse),
        ):
            self.assertTrue(demo.run_demo()["overall_passed"])


class InstalledCommandTests(unittest.TestCase):
    def test_version_unchanged_without_arguments(self) -> None:
        result = run_module()
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, f"zava-forward-core {__version__}\n")

    def test_other_arguments_keep_version_behaviour(self) -> None:
        result = run_module("--version")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, f"zava-forward-core {__version__}\n")

    def test_demo_runs_from_this_worktree_without_inputs(self) -> None:
        with tempfile.TemporaryDirectory() as home:
            env = {
                "PATH": os.environ.get("PATH", ""),
                "HOME": home,
                "ZF_DATA": str(Path(home) / "poisoned" / "zavaforward.json"),
            }
            result = run_module("discovery-demo", env=env, cwd=home)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(list(Path(home).iterdir()), [])
        report = json.loads(result.stdout)
        self.assertEqual(report["company_connection"], "DENY")
        self.assertTrue(report["overall_passed"])
        self.assertTrue(Path(demo.__file__).resolve().is_relative_to(CORE_ROOT))

    def test_demo_rejects_extra_arguments(self) -> None:
        result = run_module("discovery-demo", "--dataset", "x.csv")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("no arguments", result.stderr)


if __name__ == "__main__":
    unittest.main()
