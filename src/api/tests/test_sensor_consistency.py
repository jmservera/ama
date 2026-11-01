"""Composed CSV/SDK/SQL handover; no live Hub or Azure acceptance."""

import csv
import json
import os
import sqlite3
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

import test_sensor_consumer as consumer_tests
import test_sensor_handover as fixture
from azure.eventhub import EventData
from sensor_consumer_fixture import CONTROL, POLICY, store_at
from zava_forward.core.sensor_consumer import READING_COLUMNS, ConsumerError, SensorConsumer
from zava_forward.core.sqlstore import CASE_COLS
from zava_forward.core.synthetic import sensor_backfill
from zava_forward.core.synthetic.sensor_consistency import Tolerance, report
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
        # A perturbed stored value fails at zero tolerance and passes within a wide one.
        reopened.db.execute(
            "UPDATE sensor_reading SET temperature_c='40' WHERE home_id=? AND observed_at=?",
            ("ZF-1", reference[-1]["observed_at"]),
        )
        self.assertFalse(verify(reopened, reference, handover=fixture.HANDOVER)["passed"])
        wide = Tolerance(point=100, mean_step=100, stddev=100)
        self.assertTrue(
            verify(reopened, reference, handover=fixture.HANDOVER, temperature=wide)["passed"]
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
