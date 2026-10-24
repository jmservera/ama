"""Focused issue 441 scope and baseline regression contracts."""

import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "resident_validation", Path(__file__).with_name("validate-integration.py")
)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)
REPOSITORY_ROOT = validator.ROOT
SOURCE_BASE = validator.BASE


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="resident-validation-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-q")
        (self.root / "existing.md").write_text("# Existing\n")
        adr = self.root / "docs/adrs/0001-existing.md"
        adr.parent.mkdir(parents=True)
        adr.write_text("# Protected ADR\n")
        self.git("add", ".")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.test",
                 "commit", "-qm", "fixture")
        self.base = self.git("rev-parse", "HEAD").strip()
        self.git("update-ref", "refs/remotes/origin/main", self.base)
        self.patches = patch.multiple(validator, ROOT=self.root, BASE=self.base)
        self.patches.start()
        self.addCleanup(self.patches.stop)

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True)

    def test_issue_scope_allows_only_canonical_comparisons(self):
        paths = [
            validator.BRD, validator.PRD, ".github/rubric/scores/latest.json",
            validator.PACKAGE + "test_validate_integration.py",
            validator.PACKAGE + "resident-service-unregistered-proposal.md",
            validator.PACKAGE + "source-evidence/prd/reviewer-findings.yaml",
            validator.PACKAGE + "source-evidence/prd/reviewer-report.yaml",
            ".copilot-tracking/reviews/logs/2026-10-23/"
            "resident-portal-requirements-441-correction1-review.md",
        ]
        self.assertEqual(validator.canonical_changes(paths), sorted([validator.BRD, validator.PRD]))

    def test_unrelated_and_numbered_adr_paths_rejected(self):
        for path in (
            "src/api/unrelated.py", "docs/unrelated.md", "docs/adrs/0007-resident.md",
            ".github/rubric/artifacts.json", ".github/rubric/scores/badge.svg",
            ".copilot-tracking/plans/2026-10-23/other-issue-plan.md",
            validator.PACKAGE + "../other.md", validator.PACKAGE + "node_modules/tool.js",
        ):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "outside issue 441"):
                validator.canonical_changes([path])
        renamed = self.root / validator.PACKAGE / "moved.md"
        renamed.parent.mkdir(parents=True)
        self.git("mv", "docs/adrs/0001-existing.md", str(renamed))
        with self.assertRaisesRegex(ValueError, "docs/adrs/0001-existing.md"):
            validator.branch_changes()

    def test_scope_base_excludes_upstream_and_checks_untracked(self):
        artifact = self.root / ".github/rubric/artifacts.json"
        artifact.parent.mkdir(parents=True)
        artifact.write_text("{}\n")
        self.git("add", ".")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.test",
                 "commit", "-qm", "upstream")
        scope_base = self.git("rev-parse", "HEAD").strip()
        self.git("update-ref", "refs/remotes/origin/main", scope_base)
        doc = self.root / validator.BRD
        doc.parent.mkdir(parents=True)
        doc.write_text("# New canonical fixture\n")
        tracking = self.root / ".copilot-tracking/plans/2026-10-23/resident-portal-requirements-441-plan.md"
        tracking.parent.mkdir(parents=True)
        tracking.write_text("# Evidence\n")
        self.assertEqual(validator.branch_changes(), (scope_base, [validator.BRD]))
        score = self.root / ".github/rubric/scores/latest.json"
        score.parent.mkdir(parents=True)
        score.write_text("{}\n")
        self.git("add", ".")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.test",
                 "commit", "-qm", "committed issue inputs")
        self.assertEqual(validator.branch_changes(), (scope_base, [validator.BRD]))
        (self.root / "unrelated.py").write_text("pass\n")
        with self.assertRaisesRegex(ValueError, "unrelated.py"):
            validator.branch_changes()

    def test_new_file_empty_baseline_existing_file_preserved(self):
        self.assertEqual(validator.git_bytes("new.md", allow_missing=True), b"")
        self.assertEqual(validator.git_bytes("existing.md", allow_missing=True), b"# Existing\n")
        with self.assertRaises(subprocess.CalledProcessError):
            validator.git_bytes("new.md")

    def test_invalid_base_is_not_missing_file(self):
        with patch.object(validator, "BASE", "not-a-real-ref"):
            with self.assertRaises(subprocess.CalledProcessError):
                validator.git_bytes("new.md", allow_missing=True)

    def test_new_fragment_target_uses_empty_baseline(self):
        (self.root / "new.md").write_text("# New heading\n")
        path = self.root / "source.md"
        text = "[New](new.md#new-heading)"
        self.assertEqual(validator.broken_links(path, text, baseline=True), {"new.md#new-heading"})
        self.assertEqual(validator.broken_links(path, text), set())

    def test_existing_fragment_uses_baseline_not_current_heading(self):
        (self.root / "existing.md").write_text("# Changed\n")
        path = self.root / "source.md"
        text = "[Existing](existing.md#existing)"
        self.assertEqual(validator.broken_links(path, text, baseline=True), set())
        self.assertEqual(validator.broken_links(path, text), {"existing.md#existing"})

    def test_fragment_baseline_git_error_propagates(self):
        with patch.object(validator, "BASE", "not-a-real-ref"):
            with self.assertRaises(subprocess.CalledProcessError):
                validator.broken_links(self.root / "source.md",
                                       "[Existing](existing.md#existing)", baseline=True)

    def test_missing_cli_is_a_tool_failure_not_a_diagnostic(self):
        missing = self.root / "absent-markdownlint.cjs"
        with self.assertRaisesRegex(RuntimeError, "MODULE_NOT_FOUND") as caught:
            validator.lint(b"# Valid\n", missing)
        self.assertIn(str(missing), str(caught.exception))

    def test_actual_main_rejects_missing_cli_without_a_report(self):
        missing = self.root / "absent-markdownlint.cjs"
        report = self.root / "report.json"
        with patch.multiple(validator, ROOT=REPOSITORY_ROOT, BASE=SOURCE_BASE), patch.object(
                sys, "argv", ["validate-integration.py", "--markdownlint-cli", str(missing),
                              "--out", str(report)]):
            with self.assertRaisesRegex(RuntimeError, "markdownlint failed.*absent-markdownlint"):
                validator.main()
        self.assertFalse(report.exists())

    def test_genuine_lint_results_retain_normalized_comparison(self):
        no_column = b"stdin:3 MD012/no-multiple-blanks Multiple consecutive blank lines\n"
        column = b"stdin:5:7 MD034/no-bare-urls Bare URL used\n"
        shifted = no_column.replace(b":3 ", b":30 ") + column.replace(b":5:7 ", b":50:9 ")
        results = [
            subprocess.CompletedProcess([], 0, stdout=b"", stderr=b""),
            subprocess.CompletedProcess([], 1, stdout=b"", stderr=no_column + column),
            subprocess.CompletedProcess([], 1, stdout=b"", stderr=shifted + column),
        ]
        with patch.object(validator.subprocess, "run", side_effect=results):
            clean = validator.lint(b"", Path("cli.cjs"))
            baseline = validator.lint(b"baseline", Path("cli.cjs"))
            candidate = validator.lint(b"candidate", Path("cli.cjs"))
        self.assertEqual(clean, (0, [], {}))
        self.assertEqual(baseline[0], 1)
        self.assertEqual(baseline[1], (no_column + column).decode().splitlines())
        self.assertEqual(dict(candidate[2] - baseline[2]), {"MD034/no-bare-urls Bare URL used": 1})
        self.assertEqual(candidate[2]["MD012/no-multiple-blanks Multiple consecutive blank lines"], 1)

    def test_lint_rejects_startup_config_and_inconsistent_output(self):
        diagnostic = b"stdin:3 MD012/no-multiple-blanks Multiple consecutive blank lines\n"
        for code, stdout, stderr in (
                (1, b"", b"Error: Cannot find module 'dependency'\n"),
                (1, b"", b"Cannot read or parse config file 'config.json': ENOENT\n" + diagnostic),
                (1, b"", b"SyntaxError: Unexpected token\n"),
                (1, b"", b""), (0, b"", diagnostic), (0, b"unexpected output\n", b""),
                (2, b"", diagnostic), (4, b"", b"Cannot read config\n"), (-15, b"", b""),
                (1, diagnostic, b""), (1, b"", b"stdin:0 MD012/rule Invalid line\n")):
            with self.subTest(code=code, stdout=stdout, stderr=stderr), patch.object(
                    validator.subprocess, "run",
                    return_value=subprocess.CompletedProcess([], code, stdout=stdout, stderr=stderr)):
                with self.assertRaisesRegex(RuntimeError, "markdownlint failed.*cli.cjs"):
                    validator.lint(b"# Input\n", Path("cli.cjs"))


if __name__ == "__main__":
    unittest.main()
