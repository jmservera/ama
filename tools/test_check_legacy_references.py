"""Behaviour tests for tools/check-legacy-references.py (Issue #203)."""

import importlib.util
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

    def test_repository_has_no_violations(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(checker.check_references(root), [])


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


if __name__ == "__main__":
    unittest.main()
