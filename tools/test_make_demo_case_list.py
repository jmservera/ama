"""Focused tests for tools/make-demo-case-list.py (Refs #2008, #80): synthetic data only."""

import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

from zava_forward.core.import_preview import preview_file
from zava_forward.core.xlsx import read_workbook

SCRIPT = Path(__file__).with_name("make-demo-case-list.py")
spec = importlib.util.spec_from_file_location("make_demo_case_list", SCRIPT)
assert spec and spec.loader
gen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)
COMMITTED = Path(__file__).resolve().parent.parent / "docs/reference/research/demo-workbook"


class DemoWorkbookTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        old = sys.argv
        sys.argv = ["x", "--out-dir", str(self.dir)]
        self.addCleanup(setattr, sys, "argv", old)
        gen.main()
        self.path = self.dir / "demo-case-list.xlsx"

    def test_preview_shows_clean_mapping_problem_and_conflict_rows(self):
        before = hashlib.sha256(self.path.read_bytes()).hexdigest()
        prev, _ = preview_file(self.path)
        self.assertEqual(hashlib.sha256(self.path.read_bytes()).hexdigest(), before)
        self.assertEqual(prev.sheet, "Cases")
        how = {c.field: c.how for c in prev.columns}
        self.assertEqual(how["reference"], "alias")
        self.assertEqual(how["status"], "exact")
        self.assertIn("Resident name", prev.unmapped_headers)
        self.assertTrue(prev.blocking)
        self.assertIn("Duplicate reference DEMO-002 on rows 3 and 11", prev.conflicts)
        self.assertEqual(prev.ready, 6)
        self.assertEqual({r.row for r in prev.to_fix}, {8, 9, 10, 11})

    def test_only_invented_values(self):
        cells = [
            c for rows in read_workbook(self.path.read_bytes()).values() for r in rows for c in r
        ]
        self.assertFalse([c for c in cells if "@" in c])
        self.assertTrue(all(r[1].startswith("Demo Resident") for r in gen.ROWS))

    def test_committed_copy_matches_generator(self):
        if not (COMMITTED / "demo-case-list.csv").exists():
            self.skipTest("committed copy not generated yet")
        self.assertEqual(
            (COMMITTED / "demo-case-list.csv").read_text(encoding="utf-8"), gen.csv_text()
        )
        committed, _ = preview_file(COMMITTED / "demo-case-list.xlsx")
        regenerated, _ = preview_file(self.path)
        self.assertEqual(
            [(r.row, r.values, r.problems) for r in committed.rows],
            [(r.row, r.values, r.problems) for r in regenerated.rows],
        )


if __name__ == "__main__":
    unittest.main()
