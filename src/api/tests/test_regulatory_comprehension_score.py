"""Coverage for the staff comprehension scoring arithmetic (#215)."""

from __future__ import annotations

import unittest
from typing import Any

from checks.regulatory_comprehension_score import score


def round_of() -> list[dict[str, Any]]:
    records = []
    for group in ("repairs", "housing", "grants"):
        for number in (1, 2, 3):
            person = f"{group[:2]}{number}"
            for task in (1, 2, 3, 4, 5):
                records.append(
                    {"participant": person, "group": group, "task": task, "correct": True}
                )
    return records


class ComprehensionScoreTests(unittest.TestCase):
    def test_all_correct_meets_thresholds(self) -> None:
        result = score(round_of())
        self.assertTrue(result["thresholds_met"])
        self.assertEqual(result["overall_rate"], 1.0)

    def test_critical_error_fails_even_with_high_rate(self) -> None:
        records = round_of()
        records[0]["critical_error"] = True
        result = score(records)
        self.assertFalse(result["thresholds_met"])
        self.assertEqual(result["critical_errors"], [{"participant": "re1", "task": 1}])

    def test_group_below_eighty_percent_fails(self) -> None:
        records = round_of()
        for record in records:
            if record["group"] == "grants" and record["task"] in (1, 2, 3):
                record["correct"] = False
        result = score(records)
        self.assertFalse(result["thresholds_met"])
        self.assertAlmostEqual(result["group_rates"]["grants"], 0.4)

    def test_small_or_missing_group_is_not_a_pass(self) -> None:
        records = [r for r in round_of() if r["group"] != "housing"]
        result = score(records)
        self.assertFalse(result["thresholds_met"])
        self.assertTrue(any("Fewer than 3" in p for p in result["problems"]))

    def test_incomplete_duplicate_and_bad_records_are_reported(self) -> None:
        records = round_of()
        records.pop()
        records.append(dict(records[0]))
        records.append({"participant": "", "group": "finance", "task": 9, "correct": 1})
        problems = " ".join(score(records)["problems"])
        self.assertIn("no record for tasks", problems)
        self.assertIn("Duplicate record", problems)
        self.assertIn("Unusable group", problems)
        self.assertFalse(score(records)["thresholds_met"])

    def test_no_records_has_no_rate(self) -> None:
        result = score([])
        self.assertIsNone(result["overall_rate"])
        self.assertFalse(result["thresholds_met"])


if __name__ == "__main__":
    unittest.main()
