"""Regression test for the FR-044/AC-084 owner directions in the BRD and PRD (Issue #441)."""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRD = (ROOT / "docs/brds/agentic-retrofit-programme-brd.md").read_text(encoding="utf-8")
PRD = (ROOT / "docs/prds/zava-forward-retrofit-programme-demonstrator.md").read_text(
    encoding="utf-8"
)


def row(text, prefix):
    return next(line for line in text.splitlines() if line.startswith(prefix))


class OwnerDirectionTests(unittest.TestCase):
    def test_directions_recorded_without_approval_claim(self):
        for text, prefix in ((BRD, "| OD-53 |"), (PRD, "| OQ-029 |")):
            line = row(text, prefix)
            self.assertIn("2026-11-02", line)
            self.assertIn("Legal/Compliance", line)
            self.assertIsNone(re.search(r"OD-53 (is )?approved", line, re.I))

    def test_od53_remains_open_and_review_default(self):
        self.assertIn("Operational approval remains OPEN", row(BRD, "| OD-53 |"))
        self.assertIn("individually human-approved", row(BRD, "| OD-53 |"))
        self.assertIn("per-message", row(PRD, "| OQ-029 |"))


if __name__ == "__main__":
    unittest.main()
