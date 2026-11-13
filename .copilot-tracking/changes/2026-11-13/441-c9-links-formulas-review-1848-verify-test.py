"""Fixtures for the issue 441 criterion 9 verifier."""

import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "verify441", Path(__file__).with_name("441-c9-links-formulas-review-1848-verify.py")
)
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)


class Memory:
    def __init__(self, files):
        self.files = files

    def read(self, rel):
        return self.files[rel]

    def exists(self, rel):
        return rel in self.files or any(f.startswith(rel + "/") for f in self.files)


class VerifierTests(unittest.TestCase):
    def test_slug_and_duplicate_headings(self):
        self.assertEqual(
            v.slug("A `Code` [Link](x.md) (2026-10-13)!"), "a-code-link-2026-10-13"
        )
        text = "# Same\n\n## Same\n\n```\n# hidden\n```\n"
        self.assertEqual(v.anchors(text), {"same", "same-1"})

    def test_targets_balance_parentheses_and_titles(self):
        line = '[a](x_(1).md#h "t") and ![i](<y z.png>)'
        self.assertEqual(v.targets(line), ["x_(1).md#h", "y z.png"])

    def test_links_report_missing_file_and_anchor_only(self):
        files = {
            "docs/a.md": "# A\n[ok](b.md#top) [bad](b.md#nope) [gone](c.md) [dir](sub/) "
            "[self](#a) [ext](https://example.com)\n",
            "docs/b.md": "# Top\n",
            "docs/sub/x.md": "",
        }
        result = v.check_links(Memory(files), ["docs/a.md"])
        self.assertEqual(result["relative_links"], 5)
        self.assertEqual(result["external_links_not_fetched"], 1)
        self.assertEqual(len(result["broken"]), 2)
        self.assertIn("missing anchor", result["broken"][0])
        self.assertIn("missing file", result["broken"][1])

    def test_formula_comparison_detects_a_wrong_published_value(self):
        brd = Path(v.ROOT / v.BRD).read_text()
        self.assertTrue(v.check_formulas(brd, Path(v.ROOT / v.PRD).read_text())["ok"])
        broken = brd.replace("| 14.74 | 94.33 |", "| 15.74 | 94.33 |", 1)
        self.assertFalse(
            v.check_formulas(broken, Path(v.ROOT / v.PRD).read_text())["ok"]
        )

    def test_table_row_parses_percent_and_thousands(self):
        self.assertEqual(
            v.table_row("| X label | 1,200 | 50% |\n", "X label"), [1200.0, 50.0]
        )
        with self.assertRaises(KeyError):
            v.table_row("| Y | 1 |\n", "X")


if __name__ == "__main__":
    unittest.main()
