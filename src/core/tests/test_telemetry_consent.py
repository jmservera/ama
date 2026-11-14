"""Issue 151: withdrawal halts admission, flags the sensor view and leaves duties untouched."""

import tempfile
import unittest
from dataclasses import replace

from sensor_consumer_fixture import CONTROL, POLICY, RECEIVED, observations, store_at
from zava_forward.core import sensor_view, telemetry_consent
from zava_forward.core.sensor_consumer import SensorConsumer, preflight


class WithdrawalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = store_at(self.tmp.name, reset=True)
        self.addCleanup(self.store.db.close)
        self.consumer = SensorConsumer(self.store)
        self.consumer.configure(POLICY, [CONTROL])
        self.rows = observations()

    def process(self, row: dict) -> object:
        return self.consumer.process(next(iter(preflight([row]))), RECEIVED)

    def cases(self) -> tuple[object, ...]:
        return tuple(self.store.db.execute("SELECT id, body FROM cases ORDER BY id").fetchall())

    def test_notice_covers_what_why_who_stop_and_safety(self) -> None:
        self.assertEqual(
            set(telemetry_consent.NOTICE),
            {"collected", "why", "who_sees", "how_to_stop", "not_affected"},
        )
        text = telemetry_consent.NOTICE["not_affected"]
        self.assertIn("repairs", text)
        self.assertIn("safety", text)

    def test_withdrawal_halts_new_admission_and_keeps_prior_readings(self) -> None:
        first, second = self.rows[:2]
        self.assertEqual(self.process(first).status, "accepted")
        cases = self.cases()
        outcome = telemetry_consent.withdraw(self.consumer, POLICY, [CONTROL], CONTROL.home_id)
        self.assertEqual(outcome.collection, "stopped")
        self.assertFalse(outcome.blocks_repairs_or_safety)
        self.assertEqual(outcome.preserved_duties, telemetry_consent.PRESERVED_DUTIES)
        receipt = self.process(second)
        self.assertEqual((receipt.status, receipt.reason), ("rejected", "CONSENT"))
        count = self.store.db.execute("SELECT COUNT(*) FROM sensor_reading").fetchone()[0]
        self.assertEqual(int(count), 1)
        self.assertEqual(self.cases(), cases)

    def test_withdrawal_flags_downstream_views(self) -> None:
        self.assertEqual(self.process(self.rows[0]).status, "accepted")
        self.assertEqual(self.consumer.home_consent(CONTROL.home_id), "granted")
        telemetry_consent.withdraw(self.consumer, POLICY, [CONTROL], CONTROL.home_id)
        self.assertEqual(self.consumer.home_consent(CONTROL.home_id), "declined")
        out = sensor_view.view(self.store.db, CONTROL.home_id, None, 1727740800.0)
        self.assertEqual(out["state"], "consent-withheld")
        self.assertIsNone(out["latest"])

    def test_other_homes_are_unchanged_and_unknown_home_is_refused(self) -> None:
        other = replace(CONTROL, sensor_id="SENS-SYN-2", home_id="ZF-2")
        telemetry_consent.withdraw(self.consumer, POLICY, [CONTROL, other], CONTROL.home_id)
        stored = {
            r[0]: r[1]
            for r in self.store.db.execute(
                "SELECT sensor_id, body FROM sensor_consumer_control"
            ).fetchall()
        }
        self.assertIn('"declined"', stored["SENS-SYN-1"])
        self.assertIn('"granted"', stored["SENS-SYN-2"])
        with self.assertRaises(ValueError):
            telemetry_consent.withdraw(self.consumer, POLICY, [CONTROL], "ZF-9")


if __name__ == "__main__":
    unittest.main()
