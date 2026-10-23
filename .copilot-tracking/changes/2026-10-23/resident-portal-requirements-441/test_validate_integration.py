"""Focused issue 441 scope and baseline regression contracts."""

import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location(
    "resident_validation", Path(__file__).with_name("validate-integration.py")
)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


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


if __name__ == "__main__":
    unittest.main()
