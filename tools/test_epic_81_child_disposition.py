"""Audit that every child of Epic #81 has one explicit disposition in repository evidence.

Refs #81. Read-only over the audit note; it never asserts live GitHub state and never
promotes the epic or a child to accepted.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE = ROOT / "docs/reference/research/issue-81-epic-audit-live-r3-2026-11-20.md"

CHILDREN = (82, 83, 84, 85, 86, 87, 88, 130, 131)


def note_lines():
    return NOTE.read_text(encoding="utf-8").splitlines()


def table_row(prefix):
    rows = [ln for ln in note_lines() if ln.startswith(prefix)]
    return rows[0] if rows else ""


class Epic81ChildDispositionAudit(unittest.TestCase):
    def test_every_child_row_is_marked_closed(self):
        for number in CHILDREN:
            row = table_row(f"| #{number} |")
            self.assertIn("| CLOSED |", row, f"#{number}")

    def test_closed_child_with_residual_names_its_deferral_issue(self):
        row = table_row("| #130 |")
        self.assertRegex(row, r"deferred to #2117")
        self.assertRegex(
            NOTE.read_text(encoding="utf-8"), r"#2117 is OPEN with label `delivery:deferred`"
        )

    def test_criterion_two_is_proven_and_criterion_one_is_not(self):
        self.assertRegex(table_row("| 2 |"), r"\| Proven \|")
        self.assertRegex(table_row("| 1 |"), r"\| Unproven \|")

    def test_note_never_records_the_epic_accepted_or_closed(self):
        for line in note_lines():
            if re.search(r"#81\b[^|.]{0,40}\b(?:closed|accepted|approved)\b", line, re.IGNORECASE):
                self.assertRegex(line, r"\bnot\b|\bno\b|\bnothing\b|\bnever\b", line[:120])


if __name__ == "__main__":
    unittest.main()
