"""Behaviour tests for tools/check-legacy-references.py (Issue #203)."""

import contextlib
import importlib.util
import io
import subprocess
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "check_legacy_references", Path(__file__).with_name("check-legacy-references.py")
)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class ReferenceTests(unittest.TestCase):
    def test_untagged_path_is_flagged_and_tagged_path_passes(self):
        bad = checker.reference_violations("docs/a.md", "Code lives in `mvp/web/`.\n")
        self.assertEqual(len(bad), 1)
        good = checker.reference_violations(
            "docs/a.md", "Code lived in `mvp/web/` (archive `v0.21.0`).\n"
        )
        self.assertEqual(good, [])

    def test_generic_phrase_and_nested_paths_are_ignored(self):
        text = "A prototype/PoC/MVP and src/mvp/x and ../prototype/x are not retired paths.\n"
        self.assertEqual(checker.reference_violations("docs/a.md", text), [])

    def test_package_name_only_in_dated_records(self):
        line = "See mvp/zavaforward_mvp/a.py (archive v0.21.0).\n"
        self.assertEqual(len(checker.reference_violations("docs/live.md", line)), 1)
        self.assertEqual(
            checker.reference_violations("docs/adrs/0002-pilot-readiness-architecture.md", line),
            [],
        )

    def test_records_and_guards_are_exempt(self):
        line = "mvp/zavaforward_mvp/a.py\n"
        self.assertEqual(checker.reference_violations("docs/reference/log.md", line), [])
        self.assertEqual(checker.reference_violations("tools/rpi-checks.py", line), [])

    def test_dated_live_evidence_is_exempt_but_other_research_is_not(self):
        line = "mvp/zavaforward_mvp/a.py\n"
        for path in (
            "docs/reference/research/issue-198-rubric-live-r2-2026-11-18.md",
            "docs/reference/research/issue-200-live-20261118T1618Z-evidence/probe.txt",
            "docs/reference/research/src-repoint-live-audit-200-2026-11-18.md",
            "docs/reference/research/2026-11-19-issue-202-mvp-workflow-retirement.md",
            "tools/test_private_mvp_data_exclusion.py",
        ):
            self.assertEqual(checker.reference_violations(path, line), [], path)
        for path in (
            "docs/reference/research/issue-198-notes.md",
            "docs/reference/research/2026-11-19-notes.md",
            "docs/reference/research/ux/design-system-2026-11-18.md",
        ):
            self.assertEqual(len(checker.reference_violations(path, line)), 2, path)

    def test_repository_has_no_violations(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(checker.check_references(root), [])


class WorkflowWiringTests(unittest.TestCase):
    def setUp(self):
        root = Path(__file__).resolve().parents[1]
        self.text = (root / ".github/workflows/legacy-references.yml").read_text(encoding="utf-8")

    def test_pull_requests_of_any_path_run_the_checker_and_its_tests(self):
        self.assertRegex(self.text, r"(?m)^  pull_request:\n(?!    paths)")
        self.assertIn("python3 tools/check-legacy-references.py --files", self.text)
        self.assertIn("tools/test_check_legacy_references.py", self.text)

    def test_workflow_is_read_only_and_pinned(self):
        self.assertIn("permissions:\n  contents: read", self.text)
        self.assertRegex(self.text, r"actions/checkout@[0-9a-f]{40}")
        self.assertIn("persist-credentials: false", self.text)
        self.assertNotIn("secrets.", self.text)


class LinkTests(unittest.TestCase):
    def test_relative_links_resolve_or_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "b.md").write_text("b\n", encoding="utf-8")
            text = (
                "[ok](./b.md#top) [gone](missing.md) [web](https://x.test/a) [anchor](#h)\n"
                "`[code](nope.md)`\n```\n[fenced](nope.md)\n```\n[ref][r]\n\n[r]: ../nowhere.md\n"
            )
            found = checker.link_violations(root, "docs/a.md", text)
            self.assertEqual(len(found), 2)
            self.assertIn("missing.md", found[0])
            self.assertIn("nowhere.md", found[1])

    def test_changed_markdown_includes_branch_and_untracked_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def git(*args):
                subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)

            git("init", "-q", "-b", "main")
            git("config", "user.email", "t@example.test")
            git("config", "user.name", "t")
            (root / "old.md").write_text("old\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "base")
            git("checkout", "-qb", "topic")
            (root / "new.md").write_text("[x](gone.md)\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "topic")
            (root / "loose.md").write_text("loose\n", encoding="utf-8")
            self.assertEqual(checker.changed_markdown(root, "main"), ["loose.md", "new.md"])
            self.assertEqual(len(checker.check_links(root, ["new.md"])), 1)
            self.assertEqual(len(checker.check_links(root, ["new.md"], "main")), 1)
            (root / "old.md").write_text("old\n[gone](nope.md)\n", encoding="utf-8")
            self.assertEqual(checker.added_lines(root, "main", "old.md"), {2})
            (root / "old.md").write_text("[old](nope.md)\nold\n[gone](nope.md)\n", encoding="utf-8")
            self.assertEqual(len(checker.check_links(root, ["old.md"], "main")), 2)


class MainExitCodeTests(unittest.TestCase):
    def run_main(self, files, *args):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            (root / "docs").mkdir()
            for name, text in files.items():
                (root / "docs" / name).write_text(text, encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            with contextlib.redirect_stdout(io.StringIO()) as out:
                code = checker.main(["--root", str(root), *args])
            return code, out.getvalue()

    def test_clean_repository_exits_zero(self):
        code, out = self.run_main({"a.md": "plain\n"}, "--files", "docs/a.md")
        self.assertEqual(code, 0)
        self.assertIn("references: 0 violation(s); links: 0 violation(s)", out)

    def test_reference_violation_exits_one(self):
        code, out = self.run_main({"a.md": "Code lives in `mvp/web/`.\n"}, "--files")
        self.assertEqual(code, 1)
        self.assertIn("docs/a.md:1: retired path without archive tag", out)

    def test_broken_link_fails_unless_all_links_is_informational(self):
        files = {"a.md": "[gone](missing.md)\n"}
        code, out = self.run_main(files, "--files", "docs/a.md")
        self.assertEqual(code, 1)
        self.assertIn("unresolved link missing.md", out)
        code, _ = self.run_main(files, "--all-links")
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
