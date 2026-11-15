"""Generator and simulator emissions are labelled synthetic and free of personal-data patterns."""

import itertools
import unittest
from dataclasses import replace
from datetime import UTC, datetime
from typing import Any

from test_device_identity import sensors
from test_sensor_stream import selection
from zava_forward.core.synthetic import device_identity as di
from zava_forward.core.synthetic import device_provision as dp
from zava_forward.core.synthetic import live_readings, privacy, scale_fixture, sensor_stream


class EmissionAuditTests(unittest.TestCase):
    def test_scale_fixture_records_are_labelled_and_clean(self) -> None:
        for name, rows in (
            ("homes", scale_fixture.homes(20)),  # type: ignore[no-untyped-call]
            ("households", scale_fixture.households(20)),  # type: ignore[no-untyped-call]
            ("events", scale_fixture.events(20)),  # type: ignore[no-untyped-call]
        ):
            for row in itertools.islice(rows, 20):
                self.assertEqual(privacy.record_issues(row, scale_home=name == "homes"), [], name)

    def test_stream_frames_and_descriptor_are_labelled_and_clean(self) -> None:
        for fault in sorted(sensor_stream.FAULTS):
            for frame in sensor_stream.replay(selection(), sensor_stream.Replay(fault=fault)):
                self.assertEqual(privacy.emission_issues(frame.row), [], fault)
                sensor_stream.wire(frame.row)
        self.assertEqual(
            privacy.emission_issues(sensor_stream.descriptor(selection(), sensor_stream.Replay())),
            [],
        )

    def test_live_reading_row_is_labelled_and_clean(self) -> None:
        generator = live_readings.Generator(seed=1)
        moment = live_readings.slot_floor(datetime(2026, 1, 5, 9, tzinfo=UTC))
        row = generator.reading("SYN-00001", moment).row()
        self.assertEqual(privacy.emission_issues(row), [])

    def test_wire_refuses_unlabelled_or_personal_rows_with_fixed_codes(self) -> None:
        frame = next(iter(sensor_stream.replay(selection(), sensor_stream.Replay())))
        changes: tuple[tuple[dict[str, Any], str], ...] = (
            ({"source_type": "REAL"}, "STREAM_ROW_NOT_SYNTHETIC"),
            ({"source_type": ""}, "STREAM_ROW_NOT_SYNTHETIC"),
            ({"contains_real_data": True}, "STREAM_ROW_NOT_SYNTHETIC"),
            ({"scenario": "resident@example.org"}, "STREAM_ROW_PERSONAL_DATA"),
            ({"scenario": "SW1A 1AA"}, "STREAM_ROW_PERSONAL_DATA"),
            ({"scenario": "07700 900123"}, "STREAM_ROW_PERSONAL_DATA"),
        )
        for change, code in changes:
            with self.subTest(change=code), self.assertRaises(sensor_stream.StreamError) as caught:
                sensor_stream.wire({**frame.row, **change})
            self.assertEqual(str(caught.exception), code)
            self.assertNotIn("example.org", str(caught.exception))
        missing = {key: value for key, value in frame.row.items() if key != "source_type"}
        with self.assertRaisesRegex(sensor_stream.StreamError, "STREAM_ROW_NOT_SYNTHETIC"):
            sensor_stream.wire(missing)

    def test_provision_report_is_labelled_and_refuses_personal_owner(self) -> None:
        plan = di.plan("run-185", "Named Owner", sensors(2))
        body = dp.report(plan, "provision", "dry-run")
        self.assertEqual(privacy.emission_issues(body), [])
        for owner in ("person@example.org", "07700 900123"):
            with self.subTest(owner=owner), self.assertRaises(dp.ProvisionError) as caught:
                dp.report(replace(plan, credential_owner=owner), "provision", "dry-run")
            self.assertEqual(str(caught.exception), "CREDENTIAL_OWNER_PERSONAL_DATA")


if __name__ == "__main__":
    unittest.main()
