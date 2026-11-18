"""Issue 111: the sensor view separates fault and out-of-range readings; it mutates nothing."""

import unittest
from typing import Any

from zava_forward.core import sensor_view


def health(**latest: str) -> dict[str, str]:
    return sensor_view.reading_health({"latest": latest})


class ReadingHealth(unittest.TestCase):
    def test_states(self) -> None:
        cases = [
            (dict(temperature_c="18.5", humidity_pct="60"), "ok"),
            (dict(temperature_c="18.5", humidity_pct="140"), "out_of_range"),
            (dict(temperature_c="-80", humidity_pct="50"), "out_of_range"),
            (dict(temperature_c="n/a", humidity_pct="50"), "fault"),
            (dict(temperature_c="nan", humidity_pct="50"), "fault"),
            (dict(temperature_c="inf", humidity_pct="50"), "fault"),
            (dict(humidity_pct="50"), "fault"),
        ]
        for latest, state in cases:
            with self.subTest(latest=latest):
                self.assertEqual(health(**latest)["state"], state)

    def test_no_reading_is_not_a_fault(self) -> None:
        self.assertEqual(sensor_view.reading_health(None)["state"], "none")
        self.assertEqual(sensor_view.reading_health({"latest": None})["state"], "none")

    def test_input_is_not_changed(self) -> None:
        sensors: dict[str, Any] = {"latest": dict(temperature_c="99", humidity_pct="50")}
        before = repr(sensors)
        sensor_view.reading_health(sensors)
        self.assertEqual(repr(sensors), before)


if __name__ == "__main__":
    unittest.main()
