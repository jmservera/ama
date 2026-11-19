"""Audit that every child of Epic #93 has one explicit disposition in repository evidence.

Refs #93. Read-only over the audit note; it never asserts live GitHub state and never
promotes the epic or a child to accepted.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/reference/research/issue-93-epic-audit-live-2026-11-18.md"

CLOSED = "closed"
IN_PROGRESS = "in-progress"
CHILDREN = {94: CLOSED, 95: CLOSED, 99: CLOSED, 96: IN_PROGRESS}


def note_lines():
    return NOTE.read_text(encoding="utf-8").splitlines()


def table_row(prefix):
    rows = [ln for ln in note_lines() if ln.startswith(prefix)]
    return rows[0] if rows else ""


class Epic93ChildDispositionAudit(unittest.TestCase):
    def test_every_child_is_named_in_the_audit_note(self):
        text = NOTE.read_text(encoding="utf-8")
        for number in CHILDREN:
            self.assertRegex(text, rf"#{number}\b", f"#{number} missing")

    def test_open_child_records_its_residual_and_closed_children_are_marked(self):
        text = NOTE.read_text(encoding="utf-8")
        for number, disposition in CHILDREN.items():
            if disposition == CLOSED:
                self.assertRegex(text, rf"#{number}[^.\n]*CLOSED", f"#{number}")
        self.assertRegex(text, r"#96 OPEN with one unticked criterion")
        self.assertRegex(text, r"approved versioned schema")

    def test_epic_criteria_one_and_two_are_not_tickable(self):
        for prefix in ("| 1 |", "| 2 |"):
            row = table_row(prefix)
            self.assertIn("Not met", row)
            self.assertRegex(row, r"\| No\. ")

    def test_note_never_records_the_epic_accepted_or_closed(self):
        for line in note_lines():
            if re.search(r"#93\b[^|.]{0,40}\b(?:closed|accepted|approved)\b", line, re.IGNORECASE):
                self.assertRegex(line, r"\bnot\b|\bno\b|\bnothing\b|\bnever\b", line[:120])


if __name__ == "__main__":
    unittest.main()
