"""Deterministic synthetic sensor estimate for the resident showcase (#462)."""

from __future__ import annotations

import unittest
from datetime import UTC, datetime, timedelta
from typing import Any

from zava_forward.core import resident_forecast as rf

NOW = datetime(2026, 10, 25, 12, tzinfo=UTC)


def history(count: int, temp: float | None = 19.0, step: float = 0.0, **last: Any) -> list[Any]:
    rows = []
    for i in range(count):
        at = NOW - timedelta(hours=(count - 1 - i) * 2)
        rows.append(
            {
                "observed_at": at.isoformat().replace("+00:00", "Z"),
                "temperature_c": None if temp is None else temp + step * i,
                "humidity_pct": 55.0 + step * i,
                "temperature_status": "Recorded",
                "humidity_status": "Recorded",
            }
        )
    rows[-1].update(last)
    return rows


class ForecastTests(unittest.TestCase):
    def test_six_points_four_hours_apart_and_deterministic(self) -> None:
        first = rf.forecast(history(12), NOW)
        self.assertEqual(first, rf.forecast(history(12), NOW))
        self.assertEqual(len(first["points"]), 6)
        self.assertEqual(first["points"][0]["forecast_at"], "2026-10-25T16:00:00Z")
        self.assertEqual(first["points"][-1]["forecast_at"], "2026-10-26T12:00:00Z")
        self.assertTrue(first["synthetic"])
        self.assertEqual(first["reason"], "")

    def test_values_stay_inside_display_bounds_and_drift_is_clamped(self) -> None:
        wild = rf.forecast(history(12, temp=40.0, step=3.0), NOW)
        for point in wild["points"]:
            self.assertLessEqual(point["temperature_c"], 45.0)
            self.assertLessEqual(point["humidity_pct"], 100.0)
            self.assertGreaterEqual(point["humidity_pct"], 0.0)

    def test_few_readings_suppress_the_forecast(self) -> None:
        got = rf.forecast(history(5), NOW)
        self.assertEqual((got["points"], got["reason"]), ([], rf.REASON_FEW))

    def test_stale_history_is_flagged_and_not_forecast(self) -> None:
        later = NOW + timedelta(hours=25)
        self.assertTrue(rf.is_stale(history(12), later))
        self.assertFalse(rf.is_stale(history(12), NOW + timedelta(hours=24)))
        self.assertEqual(rf.forecast(history(12), later)["reason"], rf.REASON_STALE)

    def test_missing_latest_channel_is_not_invented(self) -> None:
        got = rf.forecast(history(12, temperature_c=None), NOW)
        self.assertTrue(all(p["temperature_c"] is None for p in got["points"]))
        self.assertTrue(all(p["humidity_pct"] is not None for p in got["points"]))

    def test_empty_history_has_no_forecast_and_is_not_stale(self) -> None:
        self.assertFalse(rf.is_stale([], NOW))
        self.assertEqual(rf.forecast([], NOW)["points"], [])


if __name__ == "__main__":
    unittest.main()
