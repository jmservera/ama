"""Consumer contract: retrofit profiles classify from observations only (exercise values)."""

import unittest
from datetime import timedelta
from typing import ClassVar

from zava_forward.core.synthetic import sensor_scenarios as ss

# Exercise tolerances, not sourced thresholds or an operational rule.
MATERIAL_TEMPERATURE_C = 0.5
MATERIAL_HUMIDITY_POINTS = 2.0


def direction(delta: dict[str, float]) -> str:
    cooler = delta["temperature_c"] <= -MATERIAL_TEMPERATURE_C
    damper = delta["humidity_points"] >= MATERIAL_HUMIDITY_POINTS
    warmer = delta["temperature_c"] >= MATERIAL_TEMPERATURE_C
    drier = delta["humidity_points"] <= -MATERIAL_HUMIDITY_POINTS
    if warmer and drier:
        return "IMPROVEMENT"
    if cooler or damper:
        return "ADVERSE_EFFECT"
    return "NO_CHANGE"


def classify(comparison: dict[str, object]) -> str:
    if comparison["status"] != "SUFFICIENT":
        return "INSUFFICIENT"
    deltas = comparison["deltas"]
    assert isinstance(deltas, dict)
    early, late = direction(deltas["early"]), direction(deltas["late"])
    if early == "NO_CHANGE" and late == "IMPROVEMENT":
        return "DELAYED_EFFECT"
    return late


class RetrofitConsumerContractTests(unittest.TestCase):
    cases: ClassVar[tuple[ss.Case, ...]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = tuple(c for c in ss.generate() if c.truth.family == "retrofit")

    def test_each_profile_classifies_from_observations_only(self) -> None:
        self.assertEqual(
            {c.truth.expected_outcome for c in self.cases},
            {"IMPROVEMENT", "NO_CHANGE", "DELAYED_EFFECT", "ADVERSE_EFFECT"},
        )
        measure_at = ss.START + timedelta(days=14)
        for case in self.cases:
            with self.subTest(case=case.truth.label):
                comparison = ss.retrofit_comparison(case.rows, measure_at)
                self.assertNotIn("truth", comparison)
                self.assertEqual(classify(comparison), case.truth.expected_outcome)

    def test_insufficient_data_never_classifies_as_effect(self) -> None:
        measure_at = ss.START + timedelta(days=14)
        for case in self.cases:
            with self.subTest(case=case.truth.label):
                comparison = ss.retrofit_comparison(case.rows[: 14 * 24], measure_at)
                self.assertEqual(classify(comparison), "INSUFFICIENT")


if __name__ == "__main__":
    unittest.main()
