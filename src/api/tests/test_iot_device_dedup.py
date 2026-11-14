"""Per-device message redelivery lands once per (sensor_id, reading_id) (issue 110)."""

import json
import tempfile
import unittest
from dataclasses import replace
from datetime import UTC, datetime

from azure.eventhub import EventData
from sensor_consumer_fixture import CONTROL, POLICY, RECEIVED, store_at
from zava_forward.core.sensor_consumer import SensorConsumer
from zava_forward.core.synthetic import live_readings
from zava_forward.core.synthetic.sensor_identity import sensor_key
from zava_forward.core.synthetic.sensor_stream import StreamError

from zava_forward.api.iot_stream import AUTH, DEVICE, Binding, decode

HOMES = ("ZF-1", "ZF-2", "ZF-3")
SLOT = datetime(2024, 10, 1, 1, 0, tzinfo=UTC)


def event(device_id: str, row: dict[str, str]) -> EventData:
    result = EventData(json.dumps(row).encode())
    result.properties = {DEVICE: device_id.encode(), AUTH: b'{"scope":"device","type":"x509"}'}
    return result


class DeviceDedupTests(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.store = store_at(tmp.name, reset=True)
        self.addCleanup(self.store.db.close)
        self.consumer = SensorConsumer(self.store)
        self.bindings = {}
        controls = []
        for home in HOMES:
            sensor = sensor_key(home)
            self.bindings["SYN-" + sensor] = Binding("SYN-" + sensor, sensor, home)
            controls.append(replace(CONTROL, sensor_id=sensor, home_id=home))
        self.consumer.configure(POLICY, controls)

    def count(self) -> int:
        return int(self.store.db.execute("SELECT COUNT(*) FROM sensor_reading").fetchone()[0])

    def test_redelivery_per_device_is_replayed_and_stored_once(self) -> None:
        generator = live_readings.Generator()
        for home in HOMES:
            reading = generator.reading(home, SLOT)
            row = decode(event(reading.device_id, reading.row()), self.bindings)
            first = self.consumer.process(row, RECEIVED)
            again = self.consumer.process(
                decode(event(reading.device_id, reading.row()), self.bindings), RECEIVED
            )
            self.assertEqual((first.status, first.replay), ("accepted", False))
            self.assertTrue(again.replay)
            self.assertEqual(again.reference, first.reference)
        self.assertEqual(self.count(), len(HOMES))
        rows = self.store.db.execute("SELECT sensor_id, reading_id FROM sensor_reading").fetchall()
        self.assertEqual(len({tuple(r) for r in rows}), len(HOMES))

    def test_tampered_redelivery_is_quarantined_as_identity_conflict(self) -> None:
        reading = live_readings.Generator().reading(HOMES[0], SLOT)
        self.consumer.process(
            decode(event(reading.device_id, reading.row()), self.bindings), RECEIVED
        )
        tampered = {**reading.row(), "temperature_c": "30.00"}
        receipt = self.consumer.process(
            decode(event(reading.device_id, tampered), self.bindings), RECEIVED
        )
        self.assertEqual((receipt.status, receipt.reason), ("rejected", "IDENTITY_CONFLICT"))
        self.assertEqual(self.count(), 1)

    def test_decode_refuses_foreign_schema_or_unstable_reading_id(self) -> None:
        reading = live_readings.Generator().reading(HOMES[0], SLOT)
        for change, code in (
            ({"reading_id": "LIVE-OTHER-20241001T0100Z"}, "READING_ID_MISMATCH"),
            ({"observed_at": "2024-10-01T01:03:00Z"}, "READING_ID_MISMATCH"),
        ):
            with self.assertRaisesRegex(StreamError, code):
                decode(event(reading.device_id, {**reading.row(), **change}), self.bindings)
        other = self.bindings["SYN-" + sensor_key(HOMES[1])]
        with self.assertRaisesRegex(StreamError, "DEVICE_ENVELOPE_MISMATCH"):
            decode(event(other.device_id, reading.row()), self.bindings)


if __name__ == "__main__":
    unittest.main()
