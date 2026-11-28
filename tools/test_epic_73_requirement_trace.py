"""Drift guard for the Epic #73 requirement trace note.

Refs #73. Offline and read-only: checks that every requirement named in the issue has one
row, that each cited test file defines the cited test, and that a deferral gives a reason.
It does not run the cited tests and never records the epic or a requirement as accepted.
"""

import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import epic_73_trace_run as runner

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/reference/research/issue-73-requirement-trace-2026-11-20.md"
REQUIREMENTS = ["BG-011"] + [f"FR-00{n}" for n in range(1, 8)] + ["FR-032", "FR-034", "NFR-003"]
CHECK_RE = re.compile(r"`([\w/.-]+\.py)::(test_\w+)`")


def rows():
    found = {}
    for line in NOTE.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0] in REQUIREMENTS:
            found.setdefault(cells[0], []).append(cells)
    return found


class Epic73RequirementTrace(unittest.TestCase):
    def test_each_requirement_has_exactly_one_row(self):
        found = rows()
        for req in REQUIREMENTS:
            self.assertEqual(len(found.get(req, [])), 1, req)

    def test_checked_rows_cite_existing_tests(self):
        for req, (row,) in rows().items():
            checks = CHECK_RE.findall(row[3])
            if row[1] == "Checked":
                self.assertTrue(checks, req)
            for path, name in checks:
                source = ROOT / path
                self.assertTrue(source.is_file(), f"{req}: {path}")
                self.assertRegex(
                    source.read_text(encoding="utf-8"), rf"def {name}\(", f"{req}: {name}"
                )

    def test_deferred_rows_state_a_reason_and_status_is_known(self):
        for req, (row,) in rows().items():
            self.assertIn(row[1], {"Checked", "Deferred"}, req)
            if row[1] == "Deferred":
                self.assertGreaterEqual(len(row[3]), 40, req)

    def test_note_never_records_the_epic_accepted(self):
        text = NOTE.read_text(encoding="utf-8")
        self.assertIn("ticks nothing", text)
        self.assertNotRegex(text, r"(?i)#73\b[^.\n]{0,40}\b(?:is|was) (?:accepted|closed)\b")

    def test_runner_builds_an_exact_unittest_id_for_every_cited_test(self):
        cited = runner.cited_tests()
        self.assertEqual(set(cited), set(REQUIREMENTS) - {"BG-011"})
        for req, checks in cited.items():
            for path, name in checks:
                argv, cwd, pythonpath = runner.command(path, name)
                self.assertTrue(cwd.is_dir(), req)
                self.assertTrue(argv[-1].endswith(f".{name}"), req)
                self.assertIn("../core/src", pythonpath)

    def test_runner_refuses_a_cited_test_outside_src_projects(self):
        with self.assertRaises(ValueError):
            runner.command("tools/test_x.py", "test_y")


if __name__ == "__main__":
    unittest.main()
