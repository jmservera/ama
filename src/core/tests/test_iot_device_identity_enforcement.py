"""Issue 110 AC: each simulated device is a distinct IoT Hub identity with schema version and
stable reading ID (multi-home cohort, deterministic replay, no credential material)."""

import dataclasses
import json
import re
import unittest
from datetime import UTC, datetime, timedelta

from zava_forward.core.synthetic import device_identity as di
from zava_forward.core.synthetic import live_readings as lr
from zava_forward.core.synthetic import sensor_identity

HOMES = tuple(f"HOME-{i:03d}" for i in range(40))
START = datetime(2026, 11, 4, 0, 0, tzinfo=UTC)
SECRET = re.compile(
    r"SharedAccessKey|HostName=|DeviceId=.*SharedAccess|primaryKey|secondaryKey|BEGIN .*PRIVATE",
    re.IGNORECASE,
)


def cohort(seed: int = 110, slots: int = 12, homes: tuple[str, ...] = HOMES) -> list[lr.Reading]:
    gen = lr.Generator(seed)
    return [
        gen.reading(h, START + timedelta(seconds=lr.SLOT_SECONDS * i))
        for i in range(slots)
        for h in homes
    ]


def sensors(homes: tuple[str, ...]) -> list[dict[str, object]]:
    return [{"sensor_id": sensor_identity.sensor_key(h), "home_id": h} for h in homes]


class DistinctDeviceIdentityTests(unittest.TestCase):
    def test_every_home_gets_one_distinct_deterministic_iot_hub_device(self) -> None:
        readings = cohort(slots=1)
        devices = {r.home_id: r.device_id for r in readings}
        self.assertEqual(len(set(devices.values())), len(HOMES))
        for home, device in devices.items():
            self.assertEqual(device, "SYN-" + sensor_identity.sensor_key(home))
            self.assertRegex(device, r"SYN-[A-Z0-9][A-Z0-9_-]{0,19}")
        self.assertEqual(devices, {r.home_id: r.device_id for r in cohort(seed=999, slots=1)})

    def test_manifest_plan_is_one_to_one_and_matches_reading_devices(self) -> None:
        manifest = di.plan("run-110", "owner", sensors(HOMES))
        by_home = {i.home_id: i.device_id for i in manifest.identities}
        self.assertEqual(by_home, {r.home_id: r.device_id for r in cohort(slots=1)})
        self.assertEqual(len({i.device_id for i in manifest.identities}), len(HOMES))

    def test_manifest_rejects_duplicate_device_or_home(self) -> None:
        for bad in (sensors(HOMES[:2]) + sensors(HOMES[:1]),):
            with self.assertRaisesRegex(di.DeviceIdentityError, "DEVICE_HOME_NOT_ONE_TO_ONE"):
                di.plan("run-110", "owner", bad)
        with self.assertRaisesRegex(di.DeviceIdentityError, "INVALID_DEVICE_IDENTITY"):
            di.plan("run-110", "owner", [{"sensor_id": "AAA", "home_id": "H1"}])

    def test_cohort_batch_passes_distinct_checks(self) -> None:
        lr.require_distinct(cohort())

    def test_shared_device_across_homes_is_rejected(self) -> None:
        a, b = cohort(slots=1)[:2]
        clash = dataclasses.replace(b, device_id=a.device_id)
        with self.assertRaisesRegex(lr.LiveReadingError, "DEVICE_ID_MISMATCH"):
            lr.require_distinct([a, clash])

    def test_one_home_under_two_devices_or_two_homes_one_device_is_rejected(self) -> None:
        a = cohort(slots=1)[0]
        other = dataclasses.replace(a, home_id="HOME-999")
        with self.assertRaises(lr.LiveReadingError):
            lr.require_distinct([a, other])

    def test_forged_device_id_is_rejected(self) -> None:
        reading = cohort(slots=1)[0]
        with self.assertRaisesRegex(lr.LiveReadingError, "DEVICE_ID_MISMATCH"):
            dataclasses.replace(reading, device_id="SYN-OTHER").validate()
        with self.assertRaisesRegex(lr.LiveReadingError, "SENSOR_ID_MISMATCH"):
            dataclasses.replace(reading, sensor_id="OTHER", device_id="SYN-OTHER").validate()


class SchemaVersionTests(unittest.TestCase):
    def test_every_reading_carries_an_explicit_supported_schema_version(self) -> None:
        for reading in cohort(slots=2):
            self.assertIn(reading.schema_version, lr.LIVE_VERSIONS)
            self.assertEqual(reading.row()["schema_version"], reading.schema_version)
        v2 = lr.Generator(1, cadence_seconds=lr.MINUTE_SECONDS).reading("HOME-001", START)
        self.assertEqual(v2.schema_version, lr.SCHEMA_VERSION_V2)

    def test_missing_or_unknown_schema_version_is_rejected(self) -> None:
        reading = cohort(slots=1)[0]
        for value, code in (
            ("", "SCHEMA_VERSION_MISSING"),
            ("reading-v0", "SCHEMA_VERSION_UNSUPPORTED"),
        ):
            with self.assertRaisesRegex(lr.LiveReadingError, code):
                dataclasses.replace(reading, schema_version=value).validate()
            row = reading.row()
            row["schema_version"] = value
            with self.assertRaisesRegex(lr.LiveReadingError, code):
                lr.validate_row(row)
        row = reading.row()
        del row["schema_version"]
        with self.assertRaisesRegex(lr.LiveReadingError, "SCHEMA_VERSION_MISSING"):
            lr.validate_row(row)


class StableReadingIdTests(unittest.TestCase):
    def test_replay_yields_identical_reading_ids_and_bodies(self) -> None:
        first, second = cohort(), cohort()
        self.assertEqual([r.reading_id for r in first], [r.reading_id for r in second])
        self.assertEqual([r.body() for r in first], [r.body() for r in second])

    def test_reading_id_is_independent_of_seed_and_values(self) -> None:
        self.assertEqual(
            [r.reading_id for r in cohort(seed=1)], [r.reading_id for r in cohort(seed=2)]
        )

    def test_reading_ids_are_unique_across_cohort_and_time(self) -> None:
        ids = [r.reading_id for r in cohort(slots=48)]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(len(i) <= 40 for i in ids))

    def test_reading_id_embeds_device_sensor_and_slot(self) -> None:
        reading = cohort(slots=3)[-1]
        self.assertEqual(
            reading.reading_id,
            f"LIVE-{reading.sensor_id}-{reading.observed_at:%Y%m%dT%H%M}Z",
        )

    def test_duplicate_reading_id_in_a_batch_is_rejected(self) -> None:
        reading = cohort(slots=1)[0]
        with self.assertRaisesRegex(lr.LiveReadingError, "READING_ID_COLLISION"):
            lr.require_distinct([reading, reading])

    def test_missing_or_tampered_reading_id_is_rejected(self) -> None:
        row = cohort(slots=1)[0].row()
        lr.validate_row(row)
        missing = dict(row, reading_id="")
        with self.assertRaisesRegex(lr.LiveReadingError, "READING_ID_MISSING"):
            lr.validate_row(missing)
        del missing["reading_id"]
        with self.assertRaisesRegex(lr.LiveReadingError, "READING_ID_MISSING"):
            lr.validate_row(missing)
        with self.assertRaisesRegex(lr.LiveReadingError, "READING_ID_MISMATCH"):
            lr.validate_row(dict(row, reading_id="LIVE-OTHER-20261104T0000Z"))


class NoCredentialMaterialTests(unittest.TestCase):
    def test_telemetry_and_manifest_carry_no_keys_or_connection_strings(self) -> None:
        for reading in cohort(slots=2):
            self.assertIsNone(SECRET.search(reading.body().decode()))
            self.assertNotIn("credential", json.dumps(reading.row()).lower())
        manifest = di.plan("run-110", "owner", sensors(HOMES[:3]))
        self.assertIsNone(SECRET.search(repr(manifest)))
        self.assertTrue(all(i.credential_ref == "" for i in manifest.identities))


if __name__ == "__main__":
    unittest.main()
