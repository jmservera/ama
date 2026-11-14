"""Window ingestion idempotence and handover continuity per home (issue 188)."""

import tempfile
import unittest
from datetime import UTC, datetime, timedelta

from sensor_consumer_fixture import CONTROL, POLICY, RECEIVED, observations, store_at
from test_sensor_consumer_live import live
from zava_forward.core.sensor_consumer import SensorConsumer
from zava_forward.core.sensor_ingest import handover_continuity, home_series, ingest_window
from zava_forward.core.synthetic.sensor_consistency import Tolerance

HANDOVER = "2024-10-01T01:30:00Z"
START = datetime(2024, 10, 1, 1, 30, tzinfo=UTC)
LOOSE = Tolerance(point=2.0, mean_step=2.0)
TIGHT = Tolerance(point=0.01, mean_step=0.01)


def live_rows(temperature: str = "17.20", humidity: str = "58.00") -> list[dict[str, object]]:
    return [
        live(START + timedelta(minutes=5 * i), temperature_c=temperature, humidity_pct=humidity)
        for i in range(2)
    ]


class IngestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = store_at(self.tmp.name, reset=True)
        self.addCleanup(self.store.db.close)
        self.consumer = SensorConsumer(self.store)
        self.consumer.configure(POLICY, [CONTROL])

    def count(self) -> int:
        return int(self.store.db.execute("SELECT COUNT(*) FROM sensor_reading").fetchone()[0])

    def test_rerunning_a_window_is_idempotent(self) -> None:
        first = ingest_window(self.consumer, observations(), RECEIVED)
        self.assertEqual((first.accepted, first.replayed, first.clean), (2, 0, True))
        before = self.consumer.retained_envelopes(["ZF-1"])
        again = ingest_window(self.consumer, observations(), RECEIVED)
        self.assertEqual((again.accepted, again.replayed, again.clean), (0, 2, True))
        self.assertEqual(self.count(), 2)
        self.assertEqual(self.consumer.retained_envelopes(["ZF-1"]), before)

    def test_changed_value_in_existing_slot_is_reported_not_stored(self) -> None:
        ingest_window(self.consumer, live_rows(), RECEIVED)
        changed = ingest_window(self.consumer, live_rows(temperature="18.00"), RECEIVED)
        self.assertEqual((changed.accepted, changed.replayed), (0, 0))
        self.assertEqual(dict(changed.rejected), {"IDENTITY_CONFLICT": 2})
        self.assertEqual(self.count(), 2)

    def test_backfill_and_live_query_together_in_time_order(self) -> None:
        ingest_window(self.consumer, observations() + live_rows(), RECEIVED)
        rows = home_series(self.consumer, "ZF-1")
        self.assertEqual(len(rows), 4)
        self.assertEqual({r["home_id"] for r in rows}, {"ZF-1"})
        stamps = [r["observed_at"] for r in rows]
        self.assertEqual(stamps, sorted(stamps))
        self.assertEqual(
            [r["schema_version"] for r in rows][:2], [observations()[0]["schema_version"]] * 2
        )
        bounded = home_series(self.consumer, "ZF-1", ("2024-10-01T01:00:00Z", HANDOVER))
        self.assertEqual(len(bounded), 2)

    def test_handover_within_declared_tolerance_passes(self) -> None:
        ingest_window(self.consumer, observations() + live_rows(), RECEIVED)
        report = handover_continuity(
            home_series(self.consumer, "ZF-1"),
            handover=HANDOVER,
            window_minutes=120,
            temperature=LOOSE,
            humidity=Tolerance(point=2.0, mean_step=5.0),
        )
        self.assertEqual((report["before_count"], report["after_count"]), (2, 2))
        self.assertTrue(report["passed"], report)

    def test_discontinuity_beyond_tolerance_fails_and_tolerance_is_inclusive(self) -> None:
        ingest_window(self.consumer, observations() + live_rows(temperature="25.00"), RECEIVED)
        rows = home_series(self.consumer, "ZF-1")
        report = handover_continuity(
            rows, handover=HANDOVER, window_minutes=120, temperature=LOOSE, humidity=LOOSE
        )
        self.assertFalse(report["passed"])
        self.assertFalse(report["metrics"]["temperature_c"]["checks"]["point"])
        exact = handover_continuity(
            rows,
            handover=HANDOVER,
            window_minutes=120,
            temperature=Tolerance(point=8.03, mean_step=8.15),
            humidity=Tolerance(point=2.0, mean_step=5.0),
        )
        self.assertTrue(exact["passed"], exact)

    def test_one_sided_or_invalid_configuration_is_refused(self) -> None:
        ingest_window(self.consumer, observations(), RECEIVED)
        rows = home_series(self.consumer, "ZF-1")
        with self.assertRaisesRegex(ValueError, "INSUFFICIENT_HANDOVER_SAMPLES"):
            handover_continuity(
                rows, handover=HANDOVER, window_minutes=120, temperature=TIGHT, humidity=TIGHT
            )
        with self.assertRaisesRegex(ValueError, "INVALID_HANDOVER_CONFIGURATION"):
            handover_continuity(
                rows, handover=HANDOVER, window_minutes=0, temperature=TIGHT, humidity=TIGHT
            )


if __name__ == "__main__":
    unittest.main()
