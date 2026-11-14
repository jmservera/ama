"""Advisory 7-day sensor trend summary on the home sensor payload (issues 1288 and 111).

Local engineering evidence on synthetic rows. The trend is deterministic directionality only: it is
labelled advisory, never enters the captured Quality source or snapshot digest, and changes no gate.
"""

import copy
import dataclasses
import json
import random
import shutil
import tempfile
import time
import unittest
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import release_support
from sensor_consumer_fixture import CONTROL, POLICY
from tests import test_mvp
from zava_forward.core import projection, sensor_view
from zava_forward.core.assistants import Assistants
from zava_forward.core.sensor_consumer import READING_COLUMNS, SensorConsumer
from zava_forward.core.sqlstore import SqlStore

DAY = 86400
DEFAULT = "SENS-SYN-1"
ASSIST_CONFIG = {
    "ZF_ASSIST_AUTHORITY": "local-nonbillable-test-authority",
    "ZF_ASSIST_EXPIRES": "2099-01-01T00:00:00Z",
    "ZF_ASSIST_CALL_ALLOWANCE": "100",
    "ZF_ASSIST_TOKEN_ALLOWANCE": "2000000",
    "ZF_ASSIST_PROACTIVE": "1",
}


def stamp(seconds: float) -> str:
    return datetime.fromtimestamp(seconds, UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


class Trend(unittest.TestCase):
    def setUp(self) -> None:
        root = Path(tempfile.mkdtemp(prefix="sensor-trend-test-"))
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        data = copy.deepcopy(test_mvp.DATA)
        people = [
            dict(code=f"ROLE-{i}", name=f"Human {i}", email=f"human{i}@example.test", role=role)
            for i, role in enumerate(projection.STAFF_ROLES + ("Contractor", "Unknown"))
        ]
        data["staff"] = people
        self.pm = next(p for p in people if p["role"] == "Retrofit Programme Manager")
        (root / "seed.json").write_text(json.dumps(data))
        self.store = SqlStore(str(root / "seed.json"), str(root / "cases.sqlite"))
        self.service = Assistants(self.store, ASSIST_CONFIG)
        release_support.install(self.store)
        self.addCleanup(self.store.db.close)
        self.addCleanup(self.service.stop)
        with self.service.transaction() as db:
            for table in (
                "sensor_reading",
                "sensor_consumer_control",
                "sensor_consumer_control_home",
                "sensor_consumer_index_state",
                "sensor_consumer_policy",
            ):
                db.execute(f"DROP TABLE IF EXISTS {table}")

    def put(self, count: int = 0, consent: str = "granted") -> None:
        control = dataclasses.replace(CONTROL, sensor_id=DEFAULT, home_id="ZF-1", consent=consent)
        SensorConsumer(self.store).configure(POLICY, [control])

    def view(self) -> Any:
        return self.service.sensors(self.pm, "ZF-1")

    def series(
        self,
        temps: Sequence[float | str],
        humid: Sequence[float | str],
        days: float = 6.0,
        sensor: str = DEFAULT,
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
                    observed_at=stamp(end - (len(temps) - 1 - i) * step),
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
        self.assertEqual(trend["sensor_id"], DEFAULT)
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

    def rows(self, order: Sequence[int], count: int = 30) -> None:
        """Insert the same retained readings in the given arrival order, with fixed timestamps."""
        base = 1_700_000_000
        with self.service.transaction() as db:
            db.execute("DELETE FROM sensor_reading")
            for i in order:
                row = dict(
                    sensor_id=DEFAULT,
                    reading_id=f"R-{i:04d}",
                    home_id="ZF-1",
                    observed_at=stamp(base - (count - i) * 4 * 3600),
                    temperature_c=str(18 + i * 0.1),
                    humidity_pct=str(60 + i % 7),
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

    def digests(self, as_of: int = 1_700_000_000) -> dict[str, Any]:
        with self.service.transaction() as db:
            out = sensor_view.view(db, "ZF-1", None, as_of, self.service.mssql)
        digests: dict[str, Any] = out["reproducibility"]
        return digests

    def test_digests_identical_across_shuffled_arrival_and_repeats(self) -> None:
        self.put(0)
        order = list(range(30))
        self.rows(order)
        first = self.digests()
        self.assertEqual(first["analysis_version"], sensor_view.ANALYSIS_VERSION)
        self.assertEqual(first["as_of"], stamp(1_700_000_000))
        self.assertEqual(first, self.digests())
        random.Random(111).shuffle(order)
        self.rows(order)
        self.assertEqual(first, self.digests())
        self.rows(order[::-1])
        self.assertEqual(first, self.digests())

    def test_digests_change_with_retained_readings_and_as_of(self) -> None:
        self.put(0)
        self.rows(range(30))
        base = self.digests()
        self.rows(range(29))
        changed = self.digests()
        self.assertNotEqual(base["input_digest"], changed["input_digest"])
        self.assertNotEqual(base["output_digest"], changed["output_digest"])
        self.rows(range(30))
        later = self.digests(1_700_000_000 + 7200)
        self.assertEqual(base["input_digest"], later["input_digest"])
        self.assertNotEqual(base["output_digest"], later["output_digest"])

    def test_api_payload_exposes_versioned_digests(self) -> None:
        self.put(0)
        self.series([18 + i * 0.1 for i in range(12)], [60] * 12)
        out = self.view()["reproducibility"]
        self.assertEqual(out["analysis_version"], sensor_view.ANALYSIS_VERSION)
        for key in ("input_digest", "output_digest"):
            self.assertRegex(out[key], r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
