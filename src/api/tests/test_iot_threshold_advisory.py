"""Advisory damp and mould watch from simulated readings (Refs #165, #1288, #111).

Fictional synthetic values only. The watch is advisory: it carries a text label, never changes
case or hazard state and adds no aria-invalid attribute.
"""

import copy
import unittest
from typing import Any

from zava_forward.core import sensor_view


def source(temperature: str, humidity: str) -> dict[str, Any]:
    return dict(latest=dict(temperature_c=temperature, humidity_pct=humidity))


class IotThresholdAdvisory(unittest.TestCase):
    def test_high_humidity_raises_a_labelled_watch(self) -> None:
        out = sensor_view.advisory(source("20.0", "82.5"))
        self.assertTrue(out["watch"])
        self.assertEqual(out["label"], "Sensor watch")
        self.assertIn("Sensor watch", out["text"])
        self.assertIn("Humidity 82.5 %RH", out["reasons"][0])

    def test_low_temperature_raises_a_watch_and_both_breaches_list_both(self) -> None:
        self.assertEqual(len(sensor_view.advisory(source("15.0", "50.0"))["reasons"]), 1)
        self.assertEqual(len(sensor_view.advisory(source("15.0", "90.0"))["reasons"]), 2)

    def test_boundary_values_breach_and_normal_values_do_not(self) -> None:
        self.assertTrue(sensor_view.advisory(source("20.0", "75.0"))["watch"])
        self.assertTrue(sensor_view.advisory(source("16.0", "50.0"))["watch"])
        calm = sensor_view.advisory(source("20.0", "55.0"))
        self.assertFalse(calm["watch"])
        self.assertEqual(calm["label"], "No watch")
        self.assertEqual(calm["reasons"], [])

    def test_missing_or_unreadable_reading_raises_no_watch(self) -> None:
        cases: list[dict[str, Any] | None] = [
            None,
            dict(latest=None),
            source("x", "y"),
            dict(latest={}),
        ]
        for sensors in cases:
            out = sensor_view.advisory(sensors)
            self.assertFalse(out["watch"])
            self.assertEqual(out["reasons"], [])

    def test_every_outcome_states_the_advisory_framing_and_exercise_label(self) -> None:
        cases: list[dict[str, Any] | None] = [None, source("20.0", "55.0"), source("10.0", "90.0")]
        for sensors in cases:
            out = sensor_view.advisory(sensors)
            self.assertIn("inspection required before changing case status", out["framing"])
            self.assertIn("Advisory only", out["framing"])
            self.assertTrue(out["thresholds"].startswith("EXERCISE VALUE"))
        self.assertIn("inspection required", sensor_view.advisory(source("10.0", "90.0"))["text"])

    def test_advisory_is_deterministic_and_does_not_mutate_its_input(self) -> None:
        sensors = source("12.0", "88.0")
        before = copy.deepcopy(sensors)
        self.assertEqual(sensor_view.advisory(sensors), sensor_view.advisory(sensors))
        self.assertEqual(sensors, before)

    def test_advisory_carries_no_state_or_aria_markup(self) -> None:
        out = sensor_view.advisory(source("10.0", "90.0"))
        self.assertFalse({"status", "hazard", "case_status", "approved"} & set(out))
        self.assertNotIn("aria-invalid", repr(out))


if __name__ == "__main__":
    unittest.main()
