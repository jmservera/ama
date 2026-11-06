"""live-sim-reading-v1 admission: sunlight kept, idempotent per home and slot (issue 188)."""

import os
import tempfile
import unittest
from dataclasses import replace
from datetime import UTC, datetime, timedelta

from sensor_consumer_fixture import CONTROL, POLICY, RECEIVED, observations, store_at
from zava_forward.core.sensor_consumer import (
    LIVE_FIELDS,
    ConsumerError,
    Observation,
    SensorConsumer,
)
from zava_forward.core.synthetic.live_readings import Reading

SLOT = datetime(2024, 10, 1, 1, 0, tzinfo=UTC)


def live(slot: datetime = SLOT, **changes: str) -> Observation:
    reading = Reading("ZF-1", "SENS-SYN-1", "SYN-SENS-SYN-1", slot, 12.34, 66.5, 301.25, 184)
    return {**reading.row(), **changes}


class LiveReadingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = store_at(self.tmp.name, reset=True)
        self.addCleanup(self.store.db.close)
        self.consumer = SensorConsumer(self.store)
        self.assertEqual(self.consumer.mssql, os.environ.get("ZF_SENSOR_MSSQL") == "1")
        self.consumer.configure(POLICY, [CONTROL])

    def count(self) -> int:
        return int(self.store.db.execute("SELECT COUNT(*) FROM sensor_reading").fetchone()[0])

    def test_accepts_and_replays_without_duplicate(self) -> None:
        first = self.consumer.process(live(), RECEIVED)
        self.assertEqual((first.status, first.reason), ("accepted", "ACCEPTED"))
        again = self.consumer.process(live(), RECEIVED)
        self.assertTrue(again.replay)
        self.assertEqual(again.reference, first.reference)
        self.assertEqual(self.count(), 1)

    def test_same_slot_with_other_values_is_a_conflict_not_a_second_row(self) -> None:
        self.consumer.process(live(), RECEIVED)
        changed = self.consumer.process(live(temperature_c="13.00"), RECEIVED)
        self.assertEqual((changed.status, changed.reason), ("rejected", "IDENTITY_CONFLICT"))
        self.assertEqual(self.count(), 1)

    def test_sunlight_retained_and_joins_backfill_series(self) -> None:
        back = observations()[0]
        self.assertEqual(self.consumer.process(back, RECEIVED).status, "accepted")
        self.assertEqual(self.consumer.process(live(), RECEIVED).status, "accepted")
        rows = self.consumer.retained_envelopes(["ZF-1"])
        self.assertEqual([r["schema_version"] for r in rows][-1], "live-sim-reading-v1")
        self.assertEqual(len(rows), 2)
        stamps = [r["observed_at"] for r in rows]
        self.assertEqual(stamps, sorted(stamps))
        self.assertEqual(rows[-1]["sunlight_wm2"], "301.25")
        self.assertEqual(rows[-1]["sunlight_unit"], "W/m2")
        self.assertEqual(rows[-1]["temperature_unit"], rows[0]["temperature_unit"])
        self.assertEqual(rows[-1]["home_id"], rows[0]["home_id"])

    def test_rejections_are_durable_data_quality_exceptions(self) -> None:
        cases = {
            "SCHEMA": live(injected_fault="drift"),
            "IDENTITY": live(reading_id="LIVE-SENS-SYN-1-20241001T0105Z"),
            "UTC_TIME": live(observed_at="2024-10-01T01:02:00Z"),
            "NUMBER": live(sunlight_wm2="-1.00"),
            "UNIT": live(sunlight_unit="lux"),
            "RANGE": live(sunlight_wm2="1400.01"),
            "UNMAPPED": live(sensor_id="OTHER-1", reading_id="LIVE-OTHER-1-20241001T0100Z"),
        }
        for reason, row in cases.items():
            with self.subTest(reason):
                receipt = self.consumer.process(row, RECEIVED)
                self.assertEqual((receipt.status, receipt.reason), ("rejected", reason))
                dq = self.consumer.inspect_exception(receipt.reference)
                assert dq is not None
                self.assertEqual(dq["manual_route"], "manual-sensor-review")
        self.assertEqual(self.count(), 0)

    def test_declined_consent_and_late_slot_are_rejected(self) -> None:
        self.consumer.process(live(SLOT + timedelta(minutes=5)), RECEIVED)
        late = self.consumer.process(live(SLOT), RECEIVED)
        self.assertEqual((late.status, late.reason), ("rejected", "OUT_OF_ORDER"))

    def test_envelope_round_trip_is_lossless_and_replays(self) -> None:
        original = live()
        self.consumer.process(original, RECEIVED)
        (envelope,) = self.consumer.retained_envelopes(["ZF-1"])
        self.assertEqual(envelope, original)
        self.assertEqual(set(envelope), set(LIVE_FIELDS))
        self.assertNotIn("calibrated", envelope)
        again = self.consumer.process(Observation(envelope), RECEIVED)
        self.assertEqual((again.status, again.reason, again.replay), ("accepted", "ACCEPTED", True))
        self.assertEqual(self.count(), 1)

    def test_mixed_schemas_keep_exact_envelopes_and_projection_excludes_live(self) -> None:
        back = observations()[0]
        self.consumer.process(back, RECEIVED)
        self.consumer.process(live(), RECEIVED)
        envelopes = self.consumer.retained_envelopes(["ZF-1"])
        self.assertEqual([e["schema_version"] for e in envelopes][-1], "live-sim-reading-v1")
        self.assertEqual(envelopes[0], {k: back[k] for k in back if k != "injected_fault"})
        projection = self.consumer.observed_series(["ZF-1"])
        self.assertEqual(projection, envelopes[:1])
        self.assertTrue(all("sunlight_wm2" not in row for row in projection))
        for envelope in envelopes:
            self.assertEqual(
                self.consumer.process(Observation(envelope), RECEIVED).reason, "ACCEPTED"
            )

    def test_replay_keeps_consent_mapping_and_calibration_controls(self) -> None:
        self.consumer.process(live(), RECEIVED)
        (envelope,) = self.consumer.retained_envelopes(["ZF-1"])
        window = {"ZF-1": ("2024-10-01T01:00:00Z", "2024-10-01T01:00:00Z")}
        self.assertEqual(self.consumer.retained_envelopes(["ZF-1"], window), [envelope])
        # Admission controls are evaluated on first sight; a changed envelope is not a replay.
        cases = (
            ("CONSENT", replace(CONTROL, consent="declined")),
            ("CALIBRATION", replace(CONTROL, calibration_confirmed=False)),
            ("CALIBRATION", replace(CONTROL, calibration_end="2024-10-01T01:05:00Z")),
            ("MAPPING_INTERVAL", replace(CONTROL, mapping_end="2024-10-01T01:05:00Z")),
        )
        for index, (reason, control) in enumerate(cases):
            with self.subTest(reason=reason, control=control):
                self.consumer.configure(POLICY, [control])
                receipt = self.consumer.process(
                    live(SLOT + timedelta(minutes=5 * (1 + index))), RECEIVED
                )
                self.assertEqual((receipt.status, receipt.reason), ("rejected", reason))
        self.consumer.configure(POLICY, [CONTROL])
        self.assertEqual(self.count(), 1)

    def test_unwitnessed_live_row_is_an_explicit_diagnostic_not_a_fabrication(self) -> None:
        self.consumer.process(live(), RECEIVED)
        self.store.db.execute("UPDATE sensor_delivery SET observation_body=NULL")
        with self.assertRaises(ConsumerError) as raised:
            self.consumer.retained_envelopes(["ZF-1"])
        self.assertEqual(raised.exception.code, "SENSOR_OUTCOME_MALFORMED")


if __name__ == "__main__":
    unittest.main()
