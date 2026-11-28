"""Issue 1907: person-run assistive-technology testing is deferred; the record must say so."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TESTS = ROOT / "src" / "api" / "tests"
BASELINE = (
    ROOT / "docs" / "reference" / "research" / "ux" / "wcag-conformance-baseline.md"
).read_text()

DEMO_KEYBOARD_TESTS = (
    "test_safety_screen_wcag_keyboard.py",
    "test_alert_chat_keyboard_live.py",
    "test_specialist_keyboard_check.py",
)


class AssistiveTechnologyDeferral(unittest.TestCase):
    def test_gap_g1_keeps_person_run_assistive_technology_as_not_run(self) -> None:
        gap = next(line for line in BASELINE.splitlines() if line.startswith("* `G-1`"))
        self.assertIn("screen-reader", gap)
        self.assertIn("`Not run`", gap)

    def test_baseline_makes_no_conformance_claim(self) -> None:
        self.assertIn("we do not claim conformance", BASELINE)

    def test_automated_keyboard_checks_stay_in_demo_scope(self) -> None:
        missing = [name for name in DEMO_KEYBOARD_TESTS if not (TESTS / name).is_file()]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
