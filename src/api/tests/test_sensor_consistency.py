"""Composed CSV/SDK/SQL handover; no live Hub or Azure acceptance."""

import contextlib
import csv
import io
import json
import os
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest import mock

import test_sensor_consumer as consumer_tests
import test_sensor_handover as fixture
from azure.eventhub import EventData
from sensor_consumer_fixture import CONTROL, POLICY, store_at
from test_sensor_consumer_live import live
from zava_forward.core.sensor_consumer import READING_COLUMNS, ConsumerError, SensorConsumer
from zava_forward.core.sqlstore import CASE_COLS
from zava_forward.core.synthetic import sensor_backfill, sensor_faults
from zava_forward.core.synthetic.live_readings import WEATHER_REFERENCE_SCENARIO, Generator
from zava_forward.core.synthetic.sensor_consistency import (
    WEATHER_TOLERANCES,
    Tolerance,
    report,
    weather_report,
)
from zava_forward.core.synthetic.sensor_stream import Replay, descriptor, replay, wire

from zava_forward.api.iot_stream import AUTH, DEVICE, Binding, decode
from zava_forward.api.sensor_handover_verify import main as verify_main
from zava_forward.api.sensor_handover_verify import open_existing_store
from zava_forward.api.sensor_handover_verify import run as verify
from zava_forward.api.sensor_ingestion import SensorIngestion


class SqlHandoverTests(consumer_tests.SensorConsumerTests):
    def test_composed_joint_query_statistics_and_reopened_window_replay(self) -> None:
        self.assertEqual(self.consumer.mssql, os.environ.get("ZF_SENSOR_MSSQL") == "1")
        selected, climate, measures = (
            fixture.selection(),
            fixture.ConstructedClimate(),
            fixture.measures(),
        )
        spec = Replay(days=4)
        end = "2024-10-05T00:00:00Z"
        # Available cases are independent of device claims and synthetic stock.
        original = self.store.db.execute("SELECT body FROM cases WHERE id='ZF-1'").fetchone()
        assert original is not None
        case = json.loads(str(original[0]))
        home = "stock-home-0000000000002"
        case["id"] = home
        columns = ", ".join(column for column in CASE_COLS if column != "body")
        self.store.db.execute(
            f"INSERT INTO cases(id,seq,body,{columns}) "
            f"SELECT ?,seq,?,{columns} FROM cases WHERE id='ZF-1'",
            (home, json.dumps(case)),
        )
        self.consumer.configure(
            replace(POLICY, window_end=end, max_past_seconds=4 * 86400),
            [
                replace(
                    CONTROL,
                    sensor_id=str(sensor["sensor_id"]),
                    home_id=str(sensor["home_id"]),
                    mapping_end=end,
                    calibration_end=end,
                )
                for sensor in selected.sensors(spec.seed)
            ],
        )
        properties_before = self.snapshot()
        history = Path(self.tmp.name) / "history"
        manifest = sensor_backfill.write(
            history,
            stock=selected,
            climate=climate,
            measures=measures,
            seed=spec.seed,
            days=spec.days,
            cadence=spec.cadence_minutes,
        )
        with (history / "readings-0000.csv").open(newline="") as stream:
            reference = list(csv.DictReader(stream))
        desc = descriptor(selected, spec, climate=climate, measures=measures)
        self.assertEqual(manifest["retrofit_history_sha256"], desc["retrofit_history_sha256"])
        self.assertEqual(manifest["climate_source"], desc["climate"])
        self.assertEqual(manifest["composed_model"], desc["composed_model"])
        self.assertEqual(manifest["household_model"], desc["household_model"])
        self.assertEqual(manifest["retrofit_model"], desc["retrofit_model"])
        prefix = [row for row in reference if row["observed_at"] < fixture.HANDOVER]
        adapter = SensorIngestion(self.store)
        # Actual persisted writer bytes enter the same #110 admission boundary.
        receipts = adapter.consume(
            [dict(row) for row in prefix], received_at="2024-10-04T16:00:00Z"
        )
        self.assertTrue(all(receipt.reason == "ACCEPTED" for receipt in receipts))
        frames = replay(selected, replace(spec, first_slot=6), climate=climate, measures=measures)
        bindings = {
            frame.device_id: Binding(frame.device_id, frame.row["sensor_id"], frame.row["home_id"])
            for frame in frames
        }
        for binding in bindings.values():
            binding.validate()
        for frame in frames:
            event = EventData(wire(frame.row))
            event.properties = {
                DEVICE: frame.device_id.encode(),
                AUTH: b'{"scope":"device","type":"x509"}',
            }
            row = decode(event, bindings)
            receipts = adapter.consume([row], received_at=frame.row["observed_at"])
            self.assertEqual(receipts[0].reason, "ACCEPTED")

        def queried() -> list[dict[str, str]]:
            observed = []
            for home in ("ZF-1", "stock-home-0000000000002"):
                stored = self.store.db.execute(
                    f"SELECT {', '.join(READING_COLUMNS)} FROM sensor_reading "
                    "WHERE home_id=? ORDER BY observed_at",
                    (home,),
                ).fetchall()
                self.assertEqual(len(stored), 12)
                control = self.store.db.execute(
                    "SELECT body FROM sensor_consumer_control WHERE sensor_id=?",
                    (stored[0][0],),
                ).fetchone()
                assert control is not None
                units = json.loads(str(control[0]))
                for record in stored:
                    row = {
                        key: str(value)
                        for key, value in zip(READING_COLUMNS, record, strict=True)
                        if key != "injected_fault"
                    }
                    stamp = record[3]
                    if isinstance(stamp, datetime):
                        self.assertIsNone(stamp.tzinfo)
                        row["observed_at"] = stamp.replace(tzinfo=UTC).strftime(
                            "%Y-%m-%dT%H:%M:%SZ"
                        )
                    row.update(
                        temperature_unit=units["temperature_unit"],
                        humidity_unit=units["humidity_unit"],
                        calibrated=str(units["calibration_confirmed"]).lower(),
                    )
                    observed.append(row)
            return observed

        observed = queried()
        homes = ("ZF-1", "stock-home-0000000000002")
        self.assertEqual(self.consumer.observed_series(homes), observed)
        with self.assertRaises(ConsumerError):
            self.consumer.observed_series([])
        result = report(observed, reference, handover=fixture.HANDOVER)
        self.assertTrue(result["passed"], result)
        before = self.counts()
        self.assertEqual(before, (24, 24, 0))
        reopened = store_at(self.tmp.name)
        self.addCleanup(reopened.db.close)
        retry = SensorIngestion(reopened)
        self.assertIsInstance(retry.consumer, SensorConsumer)
        # Retry the whole prefix/suffix window, not only its most recent reading.
        replayed = retry.consume(
            [dict(row) for row in reference],
            received_at="2024-10-04T16:00:00Z",
        )
        self.assertTrue(all(item.reason == "ACCEPTED" and item.replay for item in replayed))
        self.assertEqual(self.counts(), before)
        self.assertEqual(queried(), observed)
        self.assertEqual(self.snapshot(), properties_before)
        # The operator verifier gives the same verdict, and re-running writes nothing new.
        verdict = verify(
            reopened,
            reference,
            handover=fixture.HANDOVER,
            replay_check=True,
            received_at="2024-10-04T16:00:00Z",
        )
        self.assertTrue(verdict["passed"] and verdict["idempotent"], verdict)
        self.assertEqual(self.counts(), before)
        # A stored value that departs from its retained accepted payload is refused.
        original = reopened.db.execute(
            "SELECT temperature_c FROM sensor_reading WHERE home_id=? AND observed_at=?",
            ("ZF-1", reference[-1]["observed_at"]),
        ).fetchone()[0]
        reopened.db.execute(
            "UPDATE sensor_reading SET temperature_c='40' WHERE home_id=? AND observed_at=?",
            ("ZF-1", reference[-1]["observed_at"]),
        )
        with self.assertRaises(ConsumerError):
            verify(reopened, reference, handover=fixture.HANDOVER)
        reopened.db.execute(
            "UPDATE sensor_reading SET temperature_c=? WHERE home_id=? AND observed_at=?",
            (original, "ZF-1", reference[-1]["observed_at"]),
        )
        # Readings outside the reference window are bounded away, not a coverage mismatch.
        subset = [row for row in reference if row["observed_at"] >= reference[2]["observed_at"]]
        homes = sorted({row["home_id"] for row in subset})
        windows = {
            home: (
                min(r["observed_at"] for r in subset if r["home_id"] == home),
                max(r["observed_at"] for r in subset if r["home_id"] == home),
            )
            for home in homes
        }
        bounded = self.consumer.observed_series(homes, windows)
        self.assertEqual(len(bounded), len(subset))
        with self.assertRaises(ConsumerError):
            self.consumer.observed_series(homes, {homes[0]: windows[homes[0]]})
        if not self.consumer.mssql:
            readonly = open_existing_store({"ZF_STORE": "sqlite", "ZF_SQLITE": reopened.db_path})
            db = readonly.assistant_connection()
            self.addCleanup(db.close)
            with self.assertRaises(sqlite3.OperationalError):
                db.execute("DELETE FROM sensor_reading")
            with self.assertRaises(ValueError):
                open_existing_store(
                    {"ZF_STORE": "sqlite", "ZF_SQLITE": str(Path(self.tmp.name) / "none.db")}
                )
        missing = Path(self.tmp.name) / "absent.csv"
        self.assertEqual(
            verify_main(["--reference", str(missing), "--handover", fixture.HANDOVER]), 2
        )
        truncated = Path(self.tmp.name) / "truncated.csv"
        truncated.write_text("home_id,observed_at\nZF-1\n")
        out = io.StringIO()
        with (
            mock.patch(
                "zava_forward.api.sensor_handover_verify.open_existing_store",
                return_value=reopened,
            ),
            contextlib.redirect_stdout(out),
        ):
            code = verify_main(["--reference", str(truncated), "--handover", fixture.HANDOVER])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(out.getvalue())["refused"], "REFERENCE_ROW_INCOMPLETE")


class LiveEnvelopeReplayTests(unittest.TestCase):
    received = "2024-10-02T00:00:00Z"

    def seeded(self, with_live: bool = True) -> tuple[object, SensorConsumer, list[dict[str, str]]]:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        store = store_at(tmp.name, reset=True)
        self.addCleanup(store.db.close)
        consumer = SensorConsumer(store)
        self.assertEqual(consumer.mssql, os.environ.get("ZF_SENSOR_MSSQL") == "1")
        consumer.configure(
            replace(POLICY, max_past_seconds=86400),
            [CONTROL, replace(CONTROL, sensor_id="SENS-SYN-2")],
        )
        sensor = sensor_backfill.sensor_for({"id": "ZF-1"})
        sensor["fault_profile"] = "none"
        source = sensor_backfill.readings(
            sensor, outdoor=[(10.0 + i / 10, 70.0) for i in range(24)], days=1, cadence=60
        )
        reference = [
            dict(row)
            for packet in sensor_faults.packets(
                source, sensor_faults.configure({}), 183, "SENS-SYN-1"
            )
            for row in packet.rows
        ]
        for row in reference:
            self.assertEqual(consumer.process(row, self.received).status, "accepted")
        if with_live:
            live_row = live(sensor_id="SENS-SYN-2", reading_id="LIVE-SENS-SYN-2-20241001T0100Z")
            self.assertEqual(consumer.process(live_row, self.received).status, "accepted")
        return store, consumer, reference

    def test_raw_replay_keeps_live_envelope_exact_beside_backfill(self) -> None:
        store, consumer, _ = self.seeded()
        before = consumer.retained_envelopes(["ZF-1"])
        receipts = SensorIngestion(store).consume(before, received_at=self.received)
        self.assertEqual(len(receipts), len(before))
        self.assertTrue(all(item.reason == "ACCEPTED" and item.replay for item in receipts))
        self.assertEqual(consumer.retained_envelopes(["ZF-1"]), before)
        self.assertEqual(
            len([row for row in before if row["schema_version"] == "live-sim-reading-v1"]), 1
        )

    def test_handover_refuses_window_with_live_rows_instead_of_passing(self) -> None:
        store, consumer, reference = self.seeded()
        before = consumer.retained_envelopes(["ZF-1"])
        for replay_check in (False, True):
            with self.assertRaisesRegex(ValueError, "HANDOVER_SCHEMA_UNSUPPORTED"):
                verify(
                    store,
                    reference,
                    handover="2024-10-01T12:00:00Z",
                    cadence_minutes=60,
                    replay_check=replay_check,
                    received_at=self.received,
                )
        self.assertEqual(consumer.retained_envelopes(["ZF-1"]), before)
        csv_path = Path(store.db_path).parent / "reference.csv"
        with csv_path.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(reference[0]))
            writer.writeheader()
            writer.writerows(reference)
        out = io.StringIO()
        with (
            mock.patch(
                "zava_forward.api.sensor_handover_verify.open_existing_store", return_value=store
            ),
            contextlib.redirect_stdout(out),
        ):
            code = verify_main(
                [
                    "--reference",
                    str(csv_path),
                    "--handover",
                    "2024-10-01T12:00:00Z",
                    "--cadence-minutes",
                    "60",
                ]
            )
        self.assertEqual(code, 2)
        self.assertEqual(
            json.loads(out.getvalue()),
            {"passed": False, "refused": "HANDOVER_SCHEMA_UNSUPPORTED"},
        )

    def test_handover_still_passes_for_legacy_only_window(self) -> None:
        store, _, reference = self.seeded(with_live=False)
        verdict = verify(store, reference, handover="2024-10-01T12:00:00Z", cadence_minutes=60)
        self.assertTrue(verdict["passed"], verdict)


START = datetime(2024, 10, 1, 0, 0, tzinfo=UTC)
SLOTS = [START + timedelta(minutes=5 * i) for i in range(36)]
HANDOVER = "2024-10-01T01:30:00Z"


def weather_rows(seed: int, scenario: str | None = None) -> list[dict[str, str]]:
    generator = Generator(seed) if scenario is None else Generator(seed, scenario=scenario)
    return [generator.reading("ZF-1", slot).row() for slot in SLOTS]


class WeatherContinuityTests(unittest.TestCase):
    received = "2024-10-02T00:00:00Z"

    def seeded(
        self, changes: dict[int, dict[str, str]] | None = None
    ) -> tuple[object, SensorConsumer]:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        store = store_at(tmp.name, reset=True)
        self.addCleanup(store.db.close)
        consumer = SensorConsumer(store)
        self.assertEqual(consumer.mssql, os.environ.get("ZF_SENSOR_MSSQL") == "1")
        consumer.configure(
            replace(POLICY, max_past_seconds=86400),
            [replace(CONTROL, sensor_id=weather_rows(184)[0]["sensor_id"])],
        )
        for index, row in enumerate(weather_rows(184)):
            row = {**row, **(changes or {}).get(index, {})}
            self.assertEqual(consumer.process(row, self.received).status, "accepted")
        return store, consumer

    def reference(self) -> list[dict[str, str]]:
        return weather_rows(901, WEATHER_REFERENCE_SCENARIO)

    def check(self, store: object, reference: list[dict[str, str]], **options: object) -> dict:
        return verify(store, reference, handover=HANDOVER, cadence_minutes=5, **options)

    def test_valid_weather_continuity_is_labelled_constructed_and_unapproved(self) -> None:
        store, _ = self.seeded()
        verdict = self.check(store, self.reference())
        self.assertTrue(verdict["passed"], verdict)
        self.assertEqual(verdict["version"], "synthetic-weather-continuity-v1")
        self.assertEqual(verdict["evidence"], "constructed-distribution-check")
        self.assertIn("not an approved operational tolerance", str(verdict["tolerance_status"]))
        self.assertEqual(verdict["generator"]["version"], "live-sim-generator-v1")
        self.assertEqual(verdict["tolerances"]["sunlight_wm2"]["unit"], "W/m2")
        self.assertEqual(
            verdict["tolerances"]["temperature_c"]["point"],
            WEATHER_TOLERANCES["temperature_c"].point,
        )
        self.assertEqual(len(verdict["series"]), 1)
        self.assertEqual(set(verdict["series"][0]["metrics"]), set(WEATHER_TOLERANCES))

    def test_gross_discontinuity_fails_numerically_not_by_refusal(self) -> None:
        shifted = {
            i: {"temperature_c": f"{float(row['temperature_c']) + 15:.2f}"}
            for i, row in enumerate(weather_rows(184))
            if i >= 18
        }
        store, _ = self.seeded(shifted)
        verdict = self.check(store, self.reference())
        self.assertFalse(verdict["passed"])
        self.assertFalse(verdict["series"][0]["metrics"]["temperature_c"]["checks"]["point"])

    def test_idempotent_rerun_leaves_store_and_report_unchanged(self) -> None:
        store, consumer = self.seeded()
        before = consumer.retained_envelopes(["ZF-1"])
        first = self.check(store, self.reference(), replay_check=True, received_at=self.received)
        second = self.check(store, self.reference(), replay_check=True, received_at=self.received)
        self.assertTrue(first["passed"] and first["idempotent"], first)
        self.assertEqual(first, second)
        self.assertEqual(consumer.retained_envelopes(["ZF-1"]), before)
        duplicate = consumer.process(dict(weather_rows(184)[0]), self.received)
        self.assertTrue(duplicate.replay)

    def test_mismatched_or_mixed_inputs_are_rejected_not_dropped(self) -> None:
        store, consumer = self.seeded()
        before = consumer.retained_envelopes(["ZF-1"])
        base = self.reference()
        cases = [
            ("INVALID_HANDOVER_OBSERVATION", [{**base[0], "sunlight_unit": "kW/m2"}, *base[1:]]),
            ("INVALID_HANDOVER_OBSERVATION", weather_rows(901)),
            ("HANDOVER_METADATA_MISMATCH", [{**base[0], "label": "other label"}, *base[1:]]),
            ("HANDOVER_COVERAGE_MISMATCH", [*base[:10], *base[11:]]),
            (
                "HANDOVER_SCHEMA_UNSUPPORTED",
                [*base[:-1], {**base[-1], "schema_version": "reading-v2"}],
            ),
        ]
        for code, rows in cases:
            with self.subTest(code), self.assertRaisesRegex(ValueError, code):
                self.check(store, rows, replay_check=True, received_at=self.received)
        with self.assertRaisesRegex(ValueError, "HANDOVER_TOLERANCE_NOT_APPLICABLE"):
            self.check(store, base, temperature=Tolerance(point=1.0))
        self.assertEqual(consumer.retained_envelopes(["ZF-1"]), before)

    def test_relabelled_copy_with_equal_declared_seed_is_refused_without_writes(self) -> None:
        store, consumer = self.seeded()
        before = consumer.retained_envelopes(["ZF-1"])
        observed = weather_rows(184)
        for seed in ("184", "-0" if observed[0]["seed"] == "0" else observed[0]["seed"]):
            copy = [{**r, "scenario": WEATHER_REFERENCE_SCENARIO, "seed": seed} for r in observed]
            with self.subTest(seed), self.assertRaisesRegex(ValueError, "NOT_DISTINCT"):
                weather_report(observed, copy, handover=HANDOVER, cadence_minutes=5)
            with (
                self.subTest(seed, path="verify"),
                self.assertRaisesRegex(ValueError, "NOT_DISTINCT"),
            ):
                self.check(store, copy, replay_check=True, received_at=self.received)
        self.assertEqual(consumer.retained_envelopes(["ZF-1"]), before)

    def test_core_indoor_report_refuses_weather_rows_explicitly(self) -> None:
        rows = weather_rows(184)
        with self.assertRaisesRegex(ValueError, "INVALID_HANDOVER_OBSERVATION"):
            report(rows, rows, handover=HANDOVER, cadence_minutes=5)

    def test_weather_reference_against_indoor_or_mixed_window_is_refused(self) -> None:
        indoor = LiveEnvelopeReplayTests()
        indoor.received = self.received
        indoor.addCleanup = self.addCleanup  # type: ignore[method-assign]
        indoor.assertEqual = self.assertEqual  # type: ignore[method-assign]
        store, consumer, backfill = indoor.seeded()
        before = consumer.retained_envelopes(["ZF-1"])
        for replay_check in (False, True):
            with self.assertRaisesRegex(ValueError, "HANDOVER_SCHEMA_UNSUPPORTED"):
                self.check(store, self.reference(), replay_check=replay_check)
        self.assertEqual(consumer.retained_envelopes(["ZF-1"]), before)
        store, _ = self.seeded()
        with self.assertRaisesRegex(ValueError, "HANDOVER_SCHEMA_UNSUPPORTED"):
            verify(store, backfill, handover="2024-10-01T12:00:00Z", cadence_minutes=60)
