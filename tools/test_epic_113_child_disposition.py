"""Audit that every child of Epic #113 has one explicit disposition in repository evidence.

Refs #113. Read-only over the dated audit note; it never asserts live GitHub state and
never promotes the epic or a child to accepted.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/reference/research/issue-113-child-disposition-live-2026-11-20.md"

CLOSED = "closed"
MOVED = "closed-criteria-moved"
OPEN = "open-residual"
CHILDREN = {
    114: OPEN,
    116: OPEN,
    117: OPEN,
    118: CLOSED,
    119: MOVED,
    120: MOVED,
    121: OPEN,
    122: MOVED,
}
DEFERRAL = {119: 2147, 120: 2136, 122: 2116}


def note_lines():
    return NOTE.read_text(encoding="utf-8").splitlines()


def child_row(number):
    rows = [ln for ln in note_lines() if ln.startswith(f"| #{number} |")]
    return rows[0] if rows else ""


def criterion_row(number):
    rows = [ln for ln in note_lines() if ln.startswith(f"| {number} |")]
    return rows[0] if rows else ""


class Epic113ChildDispositionAudit(unittest.TestCase):
    def test_every_child_has_one_row_with_its_recorded_disposition(self):
        for number, disposition in CHILDREN.items():
            rows = [ln for ln in note_lines() if ln.startswith(f"| #{number} |")]
            self.assertEqual(len(rows), 1, f"#{number}")
            self.assertIn(f"| {disposition} |", rows[0], f"#{number}")

    def test_state_matches_disposition(self):
        for number, disposition in CHILDREN.items():
            state = "OPEN" if disposition == OPEN else "CLOSED"
            self.assertIn(f"| {state} |", child_row(number), f"#{number}")

    def test_closed_children_with_moved_criteria_name_an_open_deferral_issue(self):
        for number, target in DEFERRAL.items():
            row = child_row(number)
            self.assertIn(f"#{target}", row, f"#{number}")
            self.assertRegex(row, r"OPEN, label `delivery:deferred`", f"#{number}")

    def test_open_children_record_a_residual(self):
        for number, disposition in CHILDREN.items():
            if disposition != OPEN:
                continue
            residual = child_row(number).split("|")[-2]
            self.assertRegex(residual, r"unticked|waits|criteri", f"#{number} has no residual")

    def test_criterion_two_is_not_met_while_a_child_is_open(self):
        self.assertTrue(any(d == OPEN for d in CHILDREN.values()))
        row = criterion_row(2)
        self.assertIn("Not met", row)
        self.assertIn("Unproven", row)

    def test_criteria_one_and_three_are_not_tickable(self):
        self.assertIn("Not met", criterion_row(1))
        self.assertRegex(criterion_row(3), r"Unprovable for the demo")

    def test_note_never_records_the_epic_accepted_or_closed(self):
        claim = re.compile(r"#113\b[^|.]{0,40}\b(?:closed|accepted|approved)\b", re.IGNORECASE)
        for line in note_lines():
            if claim.search(line):
                self.assertRegex(line, r"\bnot\b|\bno\b|\bnothing\b|\bnever\b", line[:120])
        self.assertTrue(any("stays open" in ln and "#113" in ln for ln in note_lines()))


if __name__ == "__main__":
    unittest.main()
