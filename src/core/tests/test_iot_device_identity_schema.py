"""Per-device Hub identity, explicit schema version and stable reading ID (issue 110)."""

import unittest
from datetime import UTC, datetime, timedelta

from zava_forward.core.synthetic import device_identity, live_readings

HOMES = ("HOME-001", "HOME-002", "HOME-003", "HOME-004", "HOME-005")
SLOT = datetime(2026, 11, 14, 9, 5, tzinfo=UTC)


class DeviceIdentitySchemaTests(unittest.TestCase):
    def readings(self, cadence: int = live_readings.SLOT_SECONDS) -> list[live_readings.Reading]:
        generator = live_readings.Generator(cadence_seconds=cadence)
        return [generator.reading(home, SLOT) for home in HOMES]

    def test_every_home_has_a_distinct_device_and_sensor_identity(self) -> None:
        readings = self.readings()
        self.assertEqual(len({r.device_id for r in readings}), len(HOMES))
        self.assertEqual(len({r.sensor_id for r in readings}), len(HOMES))
        for r in readings:
            self.assertEqual(r.device_id, "SYN-" + r.sensor_id)
            device_identity.verify_envelope(r.device_id, r.row())

    def test_schema_version_is_explicit_per_cadence(self) -> None:
        five = self.readings()[0].row()
        one = self.readings(live_readings.MINUTE_SECONDS)[0].row()
        self.assertEqual(five["schema_version"], live_readings.SCHEMA_VERSION)
        self.assertEqual(one["schema_version"], live_readings.SCHEMA_VERSION_V2)
        device_identity.verify_envelope("SYN-" + one["sensor_id"], one)

    def test_reading_id_is_stable_across_redelivery_and_distinct_per_slot(self) -> None:
        first, again = self.readings()[0], self.readings()[0]
        self.assertEqual(first.reading_id, again.reading_id)
        self.assertEqual(first.body(), again.body())
        later = live_readings.Generator().reading(HOMES[0], SLOT + timedelta(minutes=5))
        self.assertNotEqual(first.reading_id, later.reading_id)
        self.assertEqual(
            first.reading_id, live_readings.reading_id_for(first.sensor_id, first.observed_at)
        )

    def test_shared_gateway_or_foreign_identity_is_rejected(self) -> None:
        a, b = self.readings()[:2]
        for device, row in (
            (b.device_id, a.row()),
            ("SYN-GATEWAY", a.row()),
            (a.device_id, {**a.row(), "home_id": HOMES[1]}),
        ):
            with self.assertRaises(device_identity.DeviceIdentityError) as ctx:
                device_identity.verify_envelope(device, row)
            self.assertEqual(str(ctx.exception), "DEVICE_ENVELOPE_MISMATCH")

    def test_missing_schema_or_unstable_reading_id_is_rejected(self) -> None:
        r = self.readings()[0]
        row = r.row()
        cases = (
            ({"schema_version": "reading-v0"}, "SCHEMA_VERSION_REQUIRED"),
            ({"reading_id": "LIVE-OTHER-20261114T0905Z"}, "READING_ID_MISMATCH"),
            ({"observed_at": "2026-11-14T09:10:00Z"}, "READING_ID_MISMATCH"),
            ({"observed_at": "bad"}, "READING_ID_MISMATCH"),
        )
        for change, code in cases:
            with self.assertRaises(device_identity.DeviceIdentityError) as ctx:
                device_identity.verify_envelope(r.device_id, {**row, **change})
            self.assertEqual(str(ctx.exception), code)
        without = {k: v for k, v in row.items() if k != "schema_version"}
        with self.assertRaises(device_identity.DeviceIdentityError):
            device_identity.verify_envelope(r.device_id, without)


if __name__ == "__main__":
    unittest.main()
