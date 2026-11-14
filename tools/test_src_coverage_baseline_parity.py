"""Issue #201 baseline-parity checks for the migrated src/ test suites.

Covers wiring, static test-method counts and real unittest TestLoader discovery
of non-skipped executable tests against the documented v0.21.0 cut-over
baseline (719 tests). Measured line or branch coverage is not configured
anywhere in the repository, so these tests prove count and wiring parity only
and guard the evidence pack's statement that measured coverage equivalence is
not established. Hosted CI coverage comparison remains open: the issue is
`Refs #201`, never `Closes #201`.
"""

from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
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
# The 719 baseline includes 92 skips, so the like-for-like 7x check uses the
# discovered total; non-skipped tests are held to a separate 6x floor.
BASELINE_MULTIPLE = 7
NON_SKIPPED_MULTIPLE = 6
DISCOVERY_SCRIPT = """
import unittest


def flatten(suite):
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from flatten(item)
        else:
            yield item


cases = list(flatten(unittest.TestLoader().discover("tests")))


def skipped(case):
    method = getattr(case, case._testMethodName, None)
    return bool(
        getattr(type(case), "__unittest_skip__", False)
        or getattr(method, "__unittest_skip__", False)
    )


print(len(cases), sum(not skipped(case) for case in cases))
"""
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


def discover_counts(project: str) -> tuple[int, int]:
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    env["PYTHONPATH"] = os.pathsep.join(
        str(ROOT / "src" / dep / "tests") for dep in ("core",) if dep != project
    )
    result = subprocess.run(
        [sys.executable, "-c", DISCOVERY_SCRIPT],
        cwd=ROOT / "src" / project,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    total, active = result.stdout.split()[-2:]
    return int(total), int(active)


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


class ExecutableDiscoveryParity(unittest.TestCase):
    def test_discovered_non_skipped_tests_exceed_baseline_multiple(self) -> None:
        counts = {project: discover_counts(project) for project in PROJECTS}
        for project, (total, active) in counts.items():
            with self.subTest(project=project):
                self.assertGreater(active, 0)
                self.assertLessEqual(active, total)
        discovered = sum(total for total, _ in counts.values())
        active_total = sum(active for _, active in counts.values())
        self.assertGreater(discovered, BASELINE_TOTAL_TESTS * BASELINE_MULTIPLE)
        self.assertGreater(active_total, BASELINE_TOTAL_TESTS * NON_SKIPPED_MULTIPLE)


class CoverageThresholdParity(unittest.TestCase):
    def test_no_project_configures_a_weaker_than_zero_gate(self) -> None:
        for project in PROJECTS:
            with self.subTest(project=project):
                for key, value in coverage_settings(project).items():
                    if key.endswith(("fail_under", "fail-under")):
                        self.assertGreater(value, 0)

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


if __name__ == "__main__":
    unittest.main()
