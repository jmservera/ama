"""#133 evaluator-view and #111 reproducibility tests driven by retrofit_exercise_scenarios.

Exercise values only: the view helpers below are test oracles, not #111/#133 production code.
"""

import json
import unittest
from datetime import datetime
from typing import Any, ClassVar

from zava_forward.core.synthetic import sensor_scenarios as ss

MATERIAL_TEMPERATURE_C = 0.5  # exercise tolerance, not a sourced threshold
APPROVED_NOTE = "Descriptive exercise only; not causation, blame or a savings promise"
FORBIDDEN = ("saving", "saves", "blame", "fault of", "resident caused")


def evaluator_view(scenario: dict[str, Any]) -> dict[str, Any]:
    """Baseline/outcome view built from observations; expectations stay separate labels."""
    measure_at = datetime.fromisoformat(scenario["measure_at"].replace("Z", "+00:00"))
    comparison = ss.retrofit_comparison(scenario["rows"], measure_at)
    return {
        "case_id": scenario["case_id"],
        "status": comparison["status"],
        "deltas": comparison["deltas"],
        "note": comparison["interpretation"],
        "value_status": scenario["value_status"],
    }


def review_priority(view: dict[str, Any]) -> str:
    """Missing or stale data is INSUFFICIENT and never lowers priority (FR-050)."""
    if view["status"] != "SUFFICIENT":
        return "INSUFFICIENT"
    late = view["deltas"]["late"]
    return "REVIEW" if late["temperature_c"] <= -MATERIAL_TEMPERATURE_C else "ROUTINE"


class RetrofitScenarioConsumerTests(unittest.TestCase):
    scenarios: ClassVar[tuple[dict[str, Any], ...]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.scenarios = tuple(ss.retrofit_exercise_scenarios())

    def test_scenarios_are_labelled_and_cover_all_directions(self) -> None:
        self.assertEqual(
            {s["expected_direction"] for s in self.scenarios},
            {"IMPROVEMENT", "NO_CHANGE", "DELAYED_EFFECT", "ADVERSE_EFFECT"},
        )
        for s in self.scenarios:
            self.assertEqual(s["value_status"], ss.EXERCISE_LABEL)

    def test_evaluator_view_is_descriptive_and_not_blaming(self) -> None:
        for s in self.scenarios:
            with self.subTest(case=s["label"]):
                view = evaluator_view(s)
                self.assertEqual(view["status"], "SUFFICIENT")
                text = json.dumps(view).lower()
                for word in FORBIDDEN:
                    self.assertNotIn(word, text.replace(APPROVED_NOTE.lower(), ""))
                self.assertEqual(view["note"], APPROVED_NOTE)
                self.assertNotIn("expected_direction", view)

    def test_adverse_scenario_routes_to_review_and_others_do_not(self) -> None:
        for s in self.scenarios:
            with self.subTest(case=s["label"]):
                expected = "REVIEW" if s["expected_direction"] == "ADVERSE_EFFECT" else "ROUTINE"
                self.assertEqual(review_priority(evaluator_view(s)), expected)

    def test_derivation_is_reproducible_from_retained_readings(self) -> None:
        again = ss.retrofit_exercise_scenarios()
        for first, second in zip(self.scenarios, again, strict=True):
            self.assertEqual(evaluator_view(first), evaluator_view(second))

    def test_truncated_readings_are_insufficient_never_routine(self) -> None:
        for s in self.scenarios:
            with self.subTest(case=s["label"]):
                short = {**s, "rows": s["rows"][: 14 * 24]}
                self.assertEqual(review_priority(evaluator_view(short)), "INSUFFICIENT")


if __name__ == "__main__":
    unittest.main()
