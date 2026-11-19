"""Audit that every child of Epic #73 has one explicit disposition in repository evidence.

Refs #73. Read-only over the audit note; it never asserts live GitHub state and never
promotes the epic or a child to accepted.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/reference/research/issue-73-epic-audit-live-r2-2026-11-19.md"

CLOSED = "Closed"
IN_PROGRESS = "In progress"
CHILDREN = {74: CLOSED, 75: CLOSED, 77: CLOSED, 78: CLOSED, 135: CLOSED, 183: CLOSED}
CHILDREN.update({76: IN_PROGRESS, 79: IN_PROGRESS, 80: IN_PROGRESS})
UNTICKED = {76: 1, 79: 2, 80: 1}


def note_lines():
    return NOTE.read_text(encoding="utf-8").splitlines()


def table_row(prefix):
    rows = [ln for ln in note_lines() if ln.startswith(prefix)]
    return rows[0] if rows else ""


class Epic73ChildDispositionAudit(unittest.TestCase):
    def test_every_child_has_one_disposition_row(self):
        for number, disposition in CHILDREN.items():
            rows = [
                ln for ln in note_lines() if re.match(rf"\| #{number} \| (?:CLOSED|OPEN) \|", ln)
            ]
            self.assertEqual(len(rows), 1, f"#{number}")
            self.assertTrue(rows[0].rstrip().endswith(f"| {disposition} |"), rows[0])

    def test_open_children_record_unticked_count_and_a_residual(self):
        text = NOTE.read_text(encoding="utf-8")
        for number, count in UNTICKED.items():
            self.assertIn(f"| #{number} | OPEN | {count} |", text)
            self.assertRegex(text, rf"\| #{number} \| [^|]+ \| [^|]{{20,}} \|")

    def test_epic_criteria_one_and_two_are_not_tickable(self):
        for prefix in ("| 1 |", "| 2 |"):
            row = table_row(prefix)
            self.assertIn("Not met", row)
            self.assertRegex(row, r"\| No\. ")

    def test_note_never_records_the_epic_accepted_or_closed(self):
        for line in note_lines():
            if re.search(r"#73\b[^|.]{0,40}\b(?:closed|accepted|approved)\b", line, re.IGNORECASE):
                self.assertRegex(line, r"\bnot\b|\bno\b|\bnothing\b|\bnever\b", line[:120])


if __name__ == "__main__":
    unittest.main()
