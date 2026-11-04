"""Sensor analysis from retained SQL readings: read-only and fail closed (Refs #111)."""

import tempfile
import unittest
from dataclasses import replace
from datetime import UTC, datetime, timedelta

from sensor_consumer_fixture import CONTROL, POLICY, RECEIVED, observations, store_at
from zava_forward.core import sensor_analysis as sa
from zava_forward.core import sensor_analysis_store as store
from zava_forward.core.sensor_consumer import SensorConsumer, preflight
from zava_forward.core.synthetic import sensor_scenarios as ss

START = datetime(2024, 10, 1, tzinfo=UTC)
WINDOW = ss.Window(START, START + timedelta(days=1))
AS_OF = WINDOW.end
HOME = CONTROL.home_id


class RetainedAnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = store_at(self.tmp.name, reset=True)
        self.addCleanup(self.store.db.close)
        self.consumer = SensorConsumer(self.store)
        if self.consumer.mssql:
            self.skipTest("SQLite-only focused test")
        self.consumer.configure(POLICY, [CONTROL])
        for row in preflight(observations()):
            self.assertEqual(self.consumer.process(row, RECEIVED).status, "accepted")

    def snapshot(self) -> tuple[object, ...]:
        return tuple(
            tuple(self.store.db.execute(f"SELECT * FROM {table} ORDER BY 1, 2").fetchall())
            for table in ("sensor_reading", "sensor_delivery", "cases")
        )

    def test_matches_pure_derivation_over_retained_rows_and_is_reproducible(self) -> None:
        rows = self.consumer.observed_series([HOME])
        expected = sa.derive_signal(HOME, rows, WINDOW, AS_OF, "granted")
        first = store.analyse_retained(self.consumer, HOME, WINDOW, AS_OF)
        self.assertEqual(first, expected)
        self.assertEqual(first, store.analyse_retained(self.consumer, HOME, WINDOW, AS_OF))
        self.assertGreater(first.valid, 0)
        self.assertEqual(first.priority_effect, "NONE")

    def test_read_only_and_no_task_without_approved_rule(self) -> None:
        before = self.snapshot()
        signal = store.analyse_retained(self.consumer, HOME, WINDOW, AS_OF)
        self.assertIsNone(sa.review_task_candidate(signal))
        self.assertEqual(self.snapshot(), before)

    def test_declined_unknown_and_unmapped_consent_fail_closed(self) -> None:
        for consent, sufficiency, reason in (
            ("declined", sa.DECLINED, "MONITORING_DECLINED"),
            ("unknown", sa.INSUFFICIENT, "CONSENT_NOT_CONFIRMED"),
        ):
            with self.subTest(consent=consent):
                self.consumer.configure(POLICY, [replace(CONTROL, consent=consent)])
                signal = store.analyse_retained(self.consumer, HOME, WINDOW, AS_OF)
                self.assertEqual((signal.sufficiency, signal.reasons), (sufficiency, (reason,)))
                self.assertEqual(signal.priority_effect, "NONE")
        self.consumer.configure(POLICY, [])
        self.assertEqual(self.consumer.home_consent(HOME), "unknown")

    def test_any_declined_control_wins(self) -> None:
        other = replace(CONTROL, sensor_id="SENS-SYN-2", consent="declined")
        self.consumer.configure(POLICY, [CONTROL, other])
        self.assertEqual(self.consumer.home_consent(HOME), "declined")

    def test_stale_and_missing_readings_are_insufficient(self) -> None:
        stale = store.analyse_retained(self.consumer, HOME, WINDOW, AS_OF + timedelta(days=30))
        self.assertEqual((stale.sufficiency, stale.outcome), (sa.STALE, sa.INSUFFICIENT))
        later = ss.Window(START + timedelta(days=5), START + timedelta(days=6))
        none = store.analyse_retained(self.consumer, HOME, later, later.end)
        self.assertEqual(none.reasons, ("NO_READINGS_IN_WINDOW",))
        self.assertEqual(none.priority_effect, "NONE")

    def test_unreadable_store_is_insufficient_with_no_priority_effect(self) -> None:
        self.store.db.execute("DROP TABLE sensor_consumer_control")
        signal = store.analyse_retained(self.consumer, HOME, WINDOW, AS_OF)
        self.assertEqual(
            (signal.sufficiency, signal.outcome, signal.reasons, signal.priority_effect),
            (sa.INSUFFICIENT, sa.INSUFFICIENT, (store.UNAVAILABLE,), "NONE"),
        )

    def test_unmapped_or_invalid_home_is_insufficient(self) -> None:
        for home in ("ZF-UNMAPPED", "x" * 80):
            with self.subTest(home=home):
                signal = store.analyse_retained(self.consumer, home, WINDOW, AS_OF)
                self.assertEqual(
                    (signal.sufficiency, signal.priority_effect), ("INSUFFICIENT", "NONE")
                )
                self.assertEqual(signal.valid, 0)


if __name__ == "__main__":
    unittest.main()
