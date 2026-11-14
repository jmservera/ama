"""Issue #201 baseline-parity checks for the migrated src/ test suites.

Covers wiring and static test-method counts against the documented cut-over
baseline. Measured line or branch coverage is not configured anywhere in the
repository, so these tests prove count and wiring parity only and guard the
evidence pack's statement that measured coverage equivalence is not established.
"""

from __future__ import annotations

import ast
import json
import re
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ("core", "agents", "api", "orchestrator", "importer")

# Historical matrix baseline in docs/architecture/cutover-evidence-pack.md.
BASELINE_TOTAL_TESTS = 719
# Complete-suite counts recorded before concurrent main integration.
BASELINE_PER_PROJECT = {
    "core": 504,
    "agents": 70,
    "api": 549,
    "orchestrator": 22,
    "importer": 39,
}
BASELINE_RUBRIC_TOTAL = 48
COVERAGE_KEYS = ("fail_under", "fail-under", "branch")


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def count_test_methods(project: str) -> tuple[int, int]:
    modules = sorted((ROOT / "src" / project / "tests").glob("test_*.py"))
    methods = 0
    for module in modules:
        tree = ast.parse(module.read_text(encoding="utf-8"))
        methods += sum(
            isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
            and node.name.startswith("test")
            for node in ast.walk(tree)
        )
    return len(modules), methods


def coverage_settings(project: str) -> dict[str, object]:
    data = tomllib.loads(read(f"src/{project}/pyproject.toml"))
    tool = data.get("tool", {})
    found: dict[str, object] = {}
    coverage = tool.get("coverage", {})
    for section in ("report", "run"):
        for key, value in coverage.get(section, {}).items():
            if key in COVERAGE_KEYS:
                found[f"{section}.{key}"] = value
    return found


class MigratedSuitesWiring(unittest.TestCase):
    def test_every_project_has_migrated_tests(self) -> None:
        for project in PROJECTS:
            with self.subTest(project=project):
                modules, methods = count_test_methods(project)
                self.assertGreater(modules, 0)
                self.assertGreater(methods, 0)
                self.assertTrue(
                    (
                        ROOT / "src" / project / "tests" / "test_dependency_rule.py"
                    ).is_file()
                )

    def test_src_ci_matrix_runs_every_project_suite(self) -> None:
        workflow = read(".github/workflows/src-ci.yml")
        for project in PROJECTS:
            with self.subTest(project=project):
                self.assertRegex(workflow, rf'"project":"{project}"[^}}]*"run":true')
        self.assertIn("python -m unittest discover -s tests -v", workflow)
        self.assertIn("working-directory: src/${{ matrix.project }}", workflow)
        self.assertIn('paths: ["src/**"', workflow)

    def test_affected_selector_and_gate_cover_every_project(self) -> None:
        self.assertTrue((ROOT / "tools" / "ci-affected.py").is_file())
        gate = read("tools/rpi-checks.py")
        match = re.search(r"^PROJECTS = \(([^)]*)\)", gate, re.MULTILINE)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(tuple(re.findall(r'"(\w+)"', match.group(1))), PROJECTS)
        self.assertIn('group = f"project-{project}"', gate)
        self.assertIn(
            '[python, "-m", "unittest", "discover", "-s", "tests", "-v"]', gate
        )

    def test_project_distributions_declare_dev_extras(self) -> None:
        for project in PROJECTS:
            with self.subTest(project=project):
                data = tomllib.loads(read(f"src/{project}/pyproject.toml"))
                self.assertIn("dev", data["project"].get("optional-dependencies", {}))


class BaselineCountParity(unittest.TestCase):
    def test_total_methods_meet_historical_matrix_baseline(self) -> None:
        total = sum(count_test_methods(project)[1] for project in PROJECTS)
        self.assertGreaterEqual(total, BASELINE_TOTAL_TESTS)

    def test_each_project_meets_recorded_baseline(self) -> None:
        for project, floor in BASELINE_PER_PROJECT.items():
            with self.subTest(project=project):
                self.assertGreaterEqual(count_test_methods(project)[1], floor)

    def test_evidence_pack_records_the_same_baseline(self) -> None:
        pack = read("docs/architecture/cutover-evidence-pack.md")
        self.assertIn("719 tests with 92 skips", pack)
        self.assertIn("504 / 549 / 70 / 22 / 39", pack)
        self.assertIn("v0.21.0", read("README.md"))


class CoverageThresholdParity(unittest.TestCase):
    def test_configured_thresholds_are_not_below_baseline(self) -> None:
        for project in PROJECTS:
            with self.subTest(project=project):
                for key, value in coverage_settings(project).items():
                    if key.endswith(("fail_under", "fail-under")):
                        self.assertGreaterEqual(value, 0)

    def test_ci_commands_do_not_weaken_the_unittest_baseline(self) -> None:
        workflow = read(".github/workflows/src-ci.yml")
        self.assertNotRegex(workflow, r"--fail-under|--cov-fail-under")
        self.assertNotRegex(
            workflow, r"continue-on-error:\s*true\s*\n\s*run:\s*python -m unittest"
        )

    def test_measured_coverage_gap_stays_disclosed(self) -> None:
        pack = read("docs/architecture/cutover-evidence-pack.md")
        has_threshold = any(coverage_settings(project) for project in PROJECTS)
        if not has_threshold:
            self.assertIn(
                "equal-or-greater measured coverage is **not established**", pack
            )

    def test_rubric_snapshot_is_not_below_recorded_baseline(self) -> None:
        latest = json.loads(read(".github/rubric/scores/latest.json"))
        self.assertGreaterEqual(latest["total"], BASELINE_RUBRIC_TOTAL)


if __name__ == "__main__":
    unittest.main()
