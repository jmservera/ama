"""Advisory 7-day sensor trend summary on the home sensor payload (issues 1288 and 111).

Local engineering evidence on synthetic rows. The trend is deterministic directionality only: it is
labelled advisory, never enters the captured Quality source or snapshot digest, and changes no gate.
"""

import json
import time
import unittest
from collections.abc import Sequence
from typing import Any

from zava_forward.core import sensor_view
from zava_forward.core.sensor_consumer import READING_COLUMNS

import test_quality_sensors as tqs

DAY = 86400


class Trend(tqs.Seed):
    def view(self) -> Any:
        return self.service.sensors(self.pm, "ZF-1")

    def series(
        self,
        temps: Sequence[float | str],
        humid: Sequence[float | str],
        days: float = 6.0,
        sensor: str = tqs.DEFAULT,
    ) -> None:
        """Evenly spaced readings from `days` ago to one hour ago."""
        end = int(time.time()) - 3600
        step = (days * DAY - 3600) / max(len(temps) - 1, 1)
        with self.service.transaction() as db:
            for i, (t, h) in enumerate(zip(temps, humid, strict=True)):
                row = dict(
                    sensor_id=sensor,
                    reading_id=f"T-{i:04d}",
                    home_id="ZF-1",
                    observed_at=tqs.stamp(end - (len(temps) - 1 - i) * step),
                    temperature_c=str(t),
                    humidity_pct=str(h),
                    source_type="SYNTHETIC",
                    scenario="BACKFILL_2Y",
                    seed="1",
                    schema_version="reading-v1",
                    injected_fault="none",
                )
                db.execute(
                    f"INSERT INTO sensor_reading VALUES ({','.join('?' * len(READING_COLUMNS))})",
                    tuple(row[c] for c in READING_COLUMNS),
                )

    def trend(self) -> Any:
        return self.view()["trend"]

    def test_rising_and_falling_in_plain_language(self) -> None:
        self.put(0)
        n = 30
        self.series([18 + i * 0.1 for i in range(n)], [70 - i for i in range(n)])
        trend = self.trend()
        temp, humid = trend["variables"]["temperature_c"], trend["variables"]["humidity_pct"]
        self.assertEqual((temp["direction"], humid["direction"]), ("rising", "falling"))
        self.assertIn("Temperature is rising over the last 7 days", temp["text"])
        self.assertIn("Moisture (relative humidity) is falling", humid["text"])
        self.assertEqual(temp["unit"], "degC")
        self.assertIsNone(trend["reason"])
        self.assertEqual(trend["sensor_id"], tqs.DEFAULT)
        self.assertLessEqual(trend["readings_used"], 2 * sensor_view.TREND_SIDE_MAX)

    def test_steady_within_thresholds(self) -> None:
        self.put(0)
        self.series(
            [20.0, 20.1, 19.9, 20.2, 20.0, 19.9, 20.1, 20.0], [55, 56, 55, 54, 55, 56, 55, 55]
        )
        variables = self.trend()["variables"]
        self.assertEqual(variables["temperature_c"]["direction"], "steady")
        self.assertEqual(variables["humidity_pct"]["direction"], "steady")

    def test_dense_history_stays_bounded(self) -> None:
        self.put(0)
        n = 400
        self.series([18 + i * 0.01 for i in range(n)], [50] * n)
        trend = self.trend()
        self.assertEqual(trend["readings_used"], 2 * sensor_view.TREND_SIDE_MAX)
        self.assertEqual(trend["variables"]["temperature_c"]["direction"], "rising")
        self.assertEqual(trend["variables"]["humidity_pct"]["direction"], "steady")

    def test_insufficient_when_few_readings_or_short_span(self) -> None:
        self.put(0)
        self.assertEqual(self.trend()["variables"]["temperature_c"]["direction"], "insufficient")
        self.assertIsNone(self.trend()["sensor_id"])
        self.series([18, 19, 20, 21, 22], [50, 51, 52, 53, 54])
        few = self.trend()
        self.assertEqual(few["variables"]["temperature_c"]["direction"], "insufficient")
        self.assertIn("Insufficient readings", few["summary"])

    def test_insufficient_when_span_under_a_day(self) -> None:
        self.put(0)
        self.series([18 + i for i in range(10)], [50 + i for i in range(10)], days=0.5)
        self.assertEqual(self.trend()["variables"]["humidity_pct"]["direction"], "insufficient")

    def test_unusable_values_never_become_zero_or_steady(self) -> None:
        self.put(0)
        self.series(["None"] * 10, [50 + i * 3 for i in range(10)])
        variables = self.trend()["variables"]
        self.assertEqual(variables["temperature_c"]["direction"], "insufficient")
        self.assertEqual(variables["humidity_pct"]["direction"], "rising")

    def test_readings_older_than_seven_days_are_excluded(self) -> None:
        self.put(0)
        self.series([18 + i for i in range(10)], [50] * 10, days=9)
        trend = self.trend()
        self.assertLess(trend["readings_used"], 10)
        self.assertGreater(trend["readings_used"], 0)

    def test_advisory_only_provenance_is_explicit(self) -> None:
        self.put(0)
        self.series([18 + i * 0.2 for i in range(10)], [50] * 10)
        trend = self.trend()
        self.assertIs(trend["advisory_only"], True)
        self.assertIs(trend["provenance"]["advisory_only"], True)
        self.assertIs(trend["provenance"]["affects_stage_gates"], False)
        self.assertIs(trend["provenance"]["calibrated"], False)
        self.assertIn("Advisory only", trend["summary"])

    def test_consent_withheld_shows_no_trend_values(self) -> None:
        self.put(0, consent="declined")
        self.series([18 + i for i in range(10)], [50 + i for i in range(10)])
        trend = self.trend()
        self.assertEqual(self.view()["state"], "consent-withheld")
        self.assertEqual(trend["readings_used"], 0)
        self.assertTrue(all(v["direction"] == "insufficient" for v in trend["variables"].values()))
        self.assertNotIn("change", trend["variables"]["temperature_c"])

    def test_trend_is_outside_the_captured_source_and_gates(self) -> None:
        self.put(0)
        self.series([18 + i for i in range(10)], [50] * 10)
        stage_before = json.dumps(self.store._case("ZF-1").get("stage"), default=str)
        with self.service.transaction() as db:
            source = sensor_view.capture_source(
                db, "ZF-1", None, int(time.time()), self.service.mssql
            )
        self.assertNotIn("trend", source)
        self.assertIn("trend", self.view())
        self.assertEqual(
            json.dumps(self.store._case("ZF-1").get("stage"), default=str), stage_before
        )


if __name__ == "__main__":
    unittest.main()
