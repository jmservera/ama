"""Actual SQL sensor processing, recovery and independent-connection concurrency."""

import json
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, replace
from pathlib import Path

from sensor_consumer_fixture import CONTROL, POLICY, RECEIVED, observations, store_at
from zava_forward.core.sensor_consumer import (
    ConsumerError,
    Observation,
    Receipt,
    SensorConsumer,
    preflight,
)


class SensorConsumerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.store = store_at(self.tmp.name, reset=True)
        self.addCleanup(self.store.db.close)
        self.consumer = SensorConsumer(self.store)
        if self.consumer.mssql:
            with self.consumer._write() as db:
                for table in (
                    "sensor_data_quality_exception",
                    "sensor_delivery",
                    "sensor_consumer_control",
                    "sensor_consumer_policy",
                    "sensor_reading",
                    "sensor_register",
                ):
                    db.execute(f"IF OBJECT_ID(N'{table}', N'U') IS NOT NULL DROP TABLE {table}")
                db.execute("DELETE FROM cases WHERE id='ZF-2'")
        self.consumer.configure(POLICY, [CONTROL])
        self.before = self.snapshot()

    def snapshot(self) -> tuple[object, ...]:
        return (
            tuple(self.store.db.execute("SELECT id, body FROM cases ORDER BY id").fetchall()),
            tuple(self.store.db.execute("SELECT seq, hash FROM audit ORDER BY seq").fetchall()),
        )

    def consume(
        self,
        rows: list[Observation],
        received_at: str = RECEIVED,
        consumer: SensorConsumer | None = None,
    ) -> tuple[Receipt, ...]:
        selected = consumer or self.consumer
        return tuple(selected.process(row, received_at) for row in preflight(rows))

    def counts(self) -> tuple[int, ...]:
        return tuple(
            int(self.store.db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
            for table in ("sensor_reading", "sensor_delivery", "sensor_data_quality_exception")
        )

    def assert_rejected(self, row: Observation, reason: str) -> Receipt:
        receipt = self.consume([row])[0]
        self.assertEqual((receipt.status, receipt.reason), ("rejected", reason))
        dq = self.consumer.inspect_exception(receipt.reference)
        self.assertIsNotNone(dq)
        assert dq is not None
        self.assertEqual((dq["status"], dq["reason"]), ("Open", reason))
        self.assertEqual(dq["manual_route"], "manual-sensor-review")
        self.assertEqual(dq["accountable_role"], "exercise-data-quality-review")
        self.assertEqual(dq["received_at"], RECEIVED)
        return receipt

    def test_append_replay_conflict_reopen_no_other_mutation(self) -> None:
        row = observations()[0]
        first = self.consume([row])[0]
        self.assertEqual(first.status, "accepted")
        self.assertEqual(self.counts(), (1, 1, 0))
        reopened = store_at(self.tmp.name)
        self.addCleanup(reopened.db.close)
        second = SensorConsumer(reopened)
        self.assertEqual(self.consume([row], consumer=second)[0], replace(first, replay=True))
        changed = {**row, "temperature_c": "21.00"}
        self.assert_rejected(changed, "IDENTITY_CONFLICT")
        self.assertEqual(self.counts(), (1, 2, 1))
        self.assertEqual(self.snapshot(), self.before)
        stored = self.store.db.execute(
            "SELECT schema_version, temperature_c FROM sensor_reading"
        ).fetchone()
        self.assertEqual(stored[0], "sensor-fault-input-v1")
        self.assertEqual(float(stored[1]), float(str(row["temperature_c"])))

    def test_fault_observations_only_quality(self) -> None:
        for fault, reason in (
            ("unmapped", "UNMAPPED"),
            ("wrong_unit", "UNIT"),
            ("clock_skewed", "MAPPING_INTERVAL"),
            ("uncalibrated", "CALIBRATION"),
        ):
            with self.subTest(fault=fault):
                self.assert_rejected(observations(fault)[0], reason)
        self.assertEqual(self.counts(), (0, 4, 4))

    def test_duplicate_and_out_of_order(self) -> None:
        rows = observations("duplicate")
        receipts = self.consume(rows)
        self.assertEqual([r.replay for r in receipts], [False, True, False, True])
        self.assertEqual(self.counts(), (2, 2, 0))

    def test_observed_time_not_delivery_order(self) -> None:
        rows = observations("out_of_order")
        result = self.consume(rows)
        self.assertEqual([r.reason for r in result], ["ACCEPTED", "OUT_OF_ORDER"])
        self.assertEqual(self.counts(), (1, 2, 1))
        dq = self.consumer.inspect_exception(result[1].reference)
        assert dq is not None
        self.assertEqual(dq["observed_at"], rows[1]["observed_at"])
        self.assertEqual(dq["received_at"], RECEIVED)

    def test_equal_time_new_identity_never_asserts_normal(self) -> None:
        row = observations()[0]
        self.consume([row])
        self.assert_rejected({**row, "reading_id": "EQUAL-TIME"}, "OUT_OF_ORDER")
        self.assertEqual(self.counts(), (1, 2, 1))

    def test_closed_schema_types_nonfinite_precision_ids_and_time(self) -> None:
        baseline = observations()[0]
        variants: list[tuple[Observation, str]] = [
            ({k: v for k, v in baseline.items() if k != "reading_id"}, "SCHEMA"),
            ({**baseline, "fault_label": "valid"}, "SCHEMA"),
            ({**baseline, "temperature_c": True}, "SCHEMA"),
            ({**baseline, "temperature_c": float("nan")}, "SCHEMA"),
            ({**baseline, "temperature_c": "nan"}, "NUMBER"),
            ({**baseline, "humidity_pct": "inf"}, "NUMBER"),
            ({**baseline, "temperature_c": "20.001"}, "NUMBER"),
            ({**baseline, "sensor_id": "sens-syn-1"}, "IDENTITY"),
            ({**baseline, "reading_id": "ID "}, "IDENTITY"),
            ({**baseline, "schema_version": "approval-looking-string"}, "SCHEMA"),
            ({**baseline, "observed_at": "2024-10-01T00:00:00+01:00"}, "UTC_TIME"),
            ({**baseline, "observed_at": "2024-13-01T00:00:00Z"}, "UTC_TIME"),
            ({**baseline, "seed": "9223372036854775808"}, "PROVENANCE"),
            ({**baseline, "calibrated": "approved"}, "CALIBRATION"),
        ]
        for row, reason in variants:
            with self.subTest(reason=reason, changed=set(row) ^ set(baseline)):
                first = self.assert_rejected(row, reason)
                self.assertTrue(self.consume([row])[0].replay)
                self.assertNotIn("SENS", repr(first))
        self.assertEqual(self.counts(), (0, len(variants), len(variants)))

    def test_ranges_inclusive_not_clamped(self) -> None:
        row = observations()[0]
        for index, (temperature, humidity, reason) in enumerate(
            (
                ("-10.00", "0.00", "ACCEPTED"),
                ("45.00", "100.00", "ACCEPTED"),
                ("45.01", "50.00", "RANGE"),
                ("20.00", "100.01", "RANGE"),
            )
        ):
            result = self.consume(
                [
                    {
                        **row,
                        "reading_id": f"BOUND-{index}",
                        "observed_at": f"2024-10-01T0{index // 2}:00:0{index}Z",
                        "temperature_c": temperature,
                        "humidity_pct": humidity,
                    }
                ],
                "2024-10-01T02:00:10Z",
            )[0]
            # First sample is 10 seconds outside the supplied past window.
            self.assertEqual(result.reason, "CLOCK_SKEW" if index < 2 else reason)
        self.consumer.configure(replace(POLICY, max_past_seconds=7210), [CONTROL])
        for index, (temperature, humidity) in enumerate((("-10.00", "0.00"), ("45.00", "100.00"))):
            result = self.consume(
                [
                    {
                        **row,
                        "reading_id": f"EDGE-{index}",
                        "observed_at": f"2024-10-01T00:00:0{index}Z",
                        "temperature_c": temperature,
                        "humidity_pct": humidity,
                    }
                ],
                "2024-10-01T02:00:10Z",
            )[0]
            self.assertEqual(result.reason, "ACCEPTED")

    def test_mapping_consent_calibration_independent(self) -> None:
        row = observations()[0]
        controls = (
            (replace(CONTROL, home_id="ZF-2"), "HOME_MISMATCH"),
            (replace(CONTROL, consent="unknown"), "CONSENT"),
            (replace(CONTROL, consent="declined"), "CONSENT"),
            (replace(CONTROL, calibration_confirmed=False), "CALIBRATION"),
            (replace(CONTROL, calibration_start="2024-10-01T00:00:01Z"), "CALIBRATION"),
            (replace(CONTROL, mapping_start="2024-10-01T00:00:01Z"), "MAPPING_INTERVAL"),
        )
        for index, (control, reason) in enumerate(controls):
            self.consumer.configure(POLICY, [control])
            self.assert_rejected({**row, "reading_id": f"CONTROL-{index}"}, reason)
        self.consumer.configure(POLICY, [])
        self.assert_rejected(row, "UNMAPPED")

    def test_clock_window_interval_boundaries(self) -> None:
        row = observations()[0]
        self.assertEqual(self.consume([row])[0].reason, "ACCEPTED")
        for name, policy, control, observed, received, reason in (
            ("BEFORE", POLICY, CONTROL, "2024-09-30T23:59:59Z", RECEIVED, "MAPPING_INTERVAL"),
            (
                "END",
                POLICY,
                CONTROL,
                "2024-10-02T00:00:00Z",
                "2024-10-02T00:00:00Z",
                "MAPPING_INTERVAL",
            ),
            (
                "CLOCK",
                POLICY,
                CONTROL,
                "2024-10-01T01:00:00Z",
                "2024-10-01T03:00:01Z",
                "CLOCK_SKEW",
            ),
            ("FUTURE", POLICY, CONTROL, "2024-10-01T02:00:01Z", RECEIVED, "CLOCK_SKEW"),
            (
                "WINDOW",
                replace(POLICY, window_start="2024-10-01T01:00:01Z"),
                CONTROL,
                "2024-10-01T01:00:00Z",
                RECEIVED,
                "WINDOW",
            ),
            (
                "CAL-END",
                POLICY,
                replace(CONTROL, calibration_end="2024-10-01T01:00:00Z"),
                "2024-10-01T01:00:00Z",
                RECEIVED,
                "CALIBRATION",
            ),
        ):
            self.consumer.configure(policy, [control])
            result = self.consume([{**row, "reading_id": name, "observed_at": observed}], received)[
                0
            ]
            self.assertEqual(result.reason, reason)

    def test_historical_replay_does_not_readmit_after_control_change(self) -> None:
        row, next_row = observations()
        accepted = self.consume([row])[0]
        self.consumer.configure(POLICY, [replace(CONTROL, consent="declined")])
        self.assertEqual(
            self.consume([row], "2026-01-01T00:00:00Z")[0], replace(accepted, replay=True)
        )
        rejected = self.assert_rejected(next_row, "CONSENT")
        self.consumer.configure(POLICY, [CONTROL])
        self.assertEqual(self.consume([next_row])[0], replace(rejected, replay=True))
        self.assertEqual(self.counts(), (1, 2, 1))

    def test_unknown_reviewer_owned_manual_route_and_no_sensitive_receipt(self) -> None:
        self.consumer.configure(replace(POLICY, reviewer=None), [CONTROL])
        row = observations("wrong_unit")[0]
        receipt = self.assert_rejected(row, "UNIT")
        dq = self.consumer.inspect_exception(receipt.reference)
        assert dq is not None
        self.assertEqual(dq["reviewer"], "Unassigned")
        restricted = self.store.db.execute(
            "SELECT observation_body FROM sensor_delivery WHERE reference=?", (receipt.reference,)
        ).fetchone()
        self.assertEqual(json.loads(restricted[0]), row)
        self.assertNotIn("observation_body", dq)
        for value in (row["sensor_id"], row["reading_id"], row["temperature_c"], row["home_id"]):
            self.assertNotIn(str(value), json.dumps(asdict(receipt)))
        with self.assertRaisesRegex(ValueError, "MANUAL_ROUTE_REQUIRED"):
            self.consumer.configure(replace(POLICY, manual_route=""), [CONTROL])

    def test_sql_empty_vs_malformed_controls(self) -> None:
        self.assertEqual(self.counts(), (0, 0, 0))
        self.consumer.configure(POLICY, [])
        self.assert_rejected(observations()[0], "UNMAPPED")
        self.store.db.execute("UPDATE sensor_consumer_policy SET body='not-json'")
        with self.assertRaisesRegex(ConsumerError, "SENSOR_CONTROLS_MALFORMED"):
            self.consume(observations())
        self.assertEqual(self.counts(), (0, 1, 1))

    def test_unsupported_store_and_envelope(self) -> None:
        with self.assertRaisesRegex(ConsumerError, "UNSUPPORTED_STORE_SQL_REQUIRED"):
            SensorConsumer(object())
        for batch in ([], observations() * 51, [{"secret": {"nested": "value"}}]):
            with self.assertRaisesRegex(ConsumerError, "INVALID_BATCH"):
                preflight(batch)
        self.assertEqual(self.counts(), (0, 0, 0))

    def test_actual_json_store_explicitly_unsupported(self) -> None:
        from zava_forward.core.store import Store

        json_store = Store(str(Path(self.tmp.name) / "constructed.json"))
        with self.assertRaisesRegex(ConsumerError, "UNSUPPORTED_STORE_SQL_REQUIRED"):
            SensorConsumer(json_store)
        self.assertEqual(self.counts(), (0, 0, 0))

    def test_corrupt_persisted_outcomes_are_not_success_shaped(self) -> None:
        row = observations()[0]
        self.consume([row])
        self.store.db.execute("UPDATE sensor_delivery SET status='unexpected'")
        with self.assertRaisesRegex(ConsumerError, "SENSOR_OUTCOME_MALFORMED"):
            self.consume([row])
        self.store.db.execute("UPDATE sensor_delivery SET status='accepted'")
        self.store.db.execute("DELETE FROM sensor_reading")
        with self.assertRaisesRegex(ConsumerError, "SENSOR_OUTCOME_MALFORMED"):
            self.consume([row])
        self.store.db.execute("DELETE FROM sensor_delivery")
        invalid = observations("wrong_unit")[0]
        self.consume([invalid])
        self.store.db.execute("DELETE FROM sensor_data_quality_exception")
        with self.assertRaisesRegex(ConsumerError, "SENSOR_OUTCOME_MALFORMED"):
            self.consume([invalid])

    def retained_state(self) -> tuple[object, ...]:
        return tuple(
            tuple(self.store.db.execute(f"SELECT * FROM {table}").fetchall())
            for table in ("sensor_reading", "sensor_delivery", "sensor_data_quality_exception")
        )

    def damage_reading(self, column: str, value: str) -> None:
        if self.consumer.mssql and value in ("invalid-sql-time", "not-a-number", "NaN"):
            self.store.db.execute(
                f"ALTER TABLE sensor_reading ALTER COLUMN {column} NVARCHAR(40) NULL"
            )
        self.store.db.execute(f"UPDATE sensor_reading SET {column}=?", (value,))

    def test_retained_reading_replay_refuses_malformed_and_inconsistent_values(self) -> None:
        row = observations()[0]
        self.consume([row])
        for column, value in (
            ("observed_at", "invalid-sql-time"),
            ("temperature_c", "not-a-number"),
            ("humidity_pct", "NaN"),
            ("home_id", "ZF-OTHER"),
            ("scenario", "DIFFERENT"),
            ("schema_version", "reading-v1"),
            ("temperature_c", "21.00"),
            ("injected_fault", "OUTLIER"),
        ):
            with self.subTest(column=column, value=value):
                self.damage_reading(column, value)
                before = self.retained_state()
                try:
                    with self.assertRaisesRegex(
                        ConsumerError, "SENSOR_OUTCOME_MALFORMED"
                    ) as caught:
                        self.consume([row])
                    self.assertEqual(str(caught.exception), "SENSOR_OUTCOME_MALFORMED")
                    self.assertEqual(self.retained_state(), before)
                finally:
                    self.store.db.execute(
                        f"UPDATE sensor_reading SET {column}=?", (row.get(column),)
                    )

    def test_retained_witness_must_match_reading_and_digest(self) -> None:
        row = observations()[0]
        self.consume([row])
        for body in (
            "not-json",
            json.dumps({**row, "temperature_c": "21.00"}),
            json.dumps({**row, "calibrated": "false"}),
            json.dumps({**row, "reading_id": "OTHER"}),
            json.dumps({"source_type": "SYNTHETIC"}),
        ):
            with self.subTest(body=body):
                self.store.db.execute("UPDATE sensor_delivery SET observation_body=?", (body,))
                before = self.retained_state()
                with self.assertRaisesRegex(ConsumerError, "SENSOR_OUTCOME_MALFORMED"):
                    self.consume([row])
                self.assertEqual(self.retained_state(), before)

    def test_new_admission_refuses_malformed_latest_without_raw_parse_error(self) -> None:
        first, second = observations()
        self.consume([first])
        for column, value in (
            ("observed_at", "invalid-sql-time"),
            ("temperature_c", "not-a-number"),
            ("humidity_pct", "NaN"),
        ):
            with self.subTest(column=column):
                self.damage_reading(column, value)
                before = self.retained_state()
                try:
                    with self.assertRaisesRegex(ConsumerError, "SENSOR_OUTCOME_MALFORMED"):
                        self.consume([second])
                    self.assertEqual(self.retained_state(), before)
                finally:
                    self.store.db.execute(f"UPDATE sensor_reading SET {column}=?", (first[column],))

    def test_truthful_historical_replay_ignores_withdrawn_current_authority(self) -> None:
        row = observations()[0]
        accepted = self.consume([row])[0]
        self.consumer.configure(
            replace(POLICY, window_start="2025-10-01T00:00:00Z", window_end="2025-10-02T00:00:00Z"),
            [
                replace(
                    CONTROL,
                    consent="declined",
                    calibration_confirmed=False,
                    mapping_start="2025-10-01T00:00:00Z",
                    mapping_end="2025-10-02T00:00:00Z",
                )
            ],
        )
        before = self.retained_state()
        self.assertEqual(
            self.consume([row], "2026-01-01T00:00:00Z")[0], replace(accepted, replay=True)
        )
        self.assertEqual(self.retained_state(), before)

    def test_seed_integer_semantics_reopen_replay_and_later_admission(self) -> None:
        baseline = observations()[0]
        for index, seed in enumerate(
            ("-0", "0", "-1", "-9223372036854775807", "9223372036854775807")
        ):
            with self.subTest(seed=seed):
                row = {
                    **baseline,
                    "reading_id": f"SEED-{index}",
                    "observed_at": f"2024-10-01T00:{index * 10:02d}:00Z",
                    "seed": seed,
                }
                first = self.consume([row])[0]
                self.assertEqual(first.status, "accepted")
                reopened = store_at(self.tmp.name)
                self.addCleanup(reopened.db.close)
                before = self.retained_state()
                replay = self.consume([row], consumer=SensorConsumer(reopened))[0]
                self.assertEqual(replay, replace(first, replay=True))
                self.assertEqual(self.retained_state(), before)
                later = {
                    **row,
                    "reading_id": f"SEED-LATER-{index}",
                    "observed_at": f"2024-10-01T00:{index * 10 + 5:02d}:00Z",
                }
                self.assertEqual(self.consume([later])[0].status, "accepted")
        self.assertEqual(self.counts(), (10, 10, 0))

    def corrupt_ordering_timestamp(self, row: Observation, value: str) -> None:
        if self.consumer.mssql:
            kind = self.store.db.execute(
                "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS"
                " WHERE TABLE_NAME='sensor_reading' AND COLUMN_NAME='observed_at'"
            ).fetchone()
            assert kind is not None
            if kind[0] == "datetime2":
                self.store.db.execute(
                    "ALTER TABLE sensor_reading ALTER COLUMN observed_at NVARCHAR(40) NULL"
                )
                for accepted in observations():
                    self.store.db.execute(
                        "UPDATE sensor_reading SET observed_at=? WHERE reading_id=?",
                        (accepted["observed_at"], accepted["reading_id"]),
                    )
        self.store.db.execute(
            "UPDATE sensor_reading SET observed_at=? WHERE sensor_id=? AND reading_id=?",
            (value, row["sensor_id"], row["reading_id"]),
        )

    def assert_corrupt_ordering_refused(self, value: str) -> None:
        first, second = observations()
        self.consume([first, second])
        between = {
            **first,
            "reading_id": "BETWEEN",
            "observed_at": "2024-10-01T00:30:00Z",
        }
        self.corrupt_ordering_timestamp(second, value)
        before = self.retained_state()
        with self.assertRaisesRegex(ConsumerError, "SENSOR_OUTCOME_MALFORMED"):
            self.consume([between])
        self.assertEqual(self.retained_state(), before)

    def test_low_sorting_retained_timestamp_refused(self) -> None:
        self.assert_corrupt_ordering_refused("!bad-time")

    def test_invalid_month_retained_timestamp_refused(self) -> None:
        self.assert_corrupt_ordering_refused("2024-00-01T01:00:00Z")

    def test_duplicate_maximum_witness_mismatch_refused(self) -> None:
        self.assert_corrupt_ordering_refused(str(observations()[0]["observed_at"]))

    def test_independent_connection_same_key_concurrency(self) -> None:
        row = observations()[0]
        barrier = threading.Barrier(2)
        other_store = store_at(self.tmp.name)
        self.addCleanup(other_store.db.close)

        def writer(consumer: SensorConsumer) -> Receipt:
            barrier.wait(timeout=10)
            return self.consume([row], consumer=consumer)[0]

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(
                pool.map(writer, (SensorConsumer(self.store), SensorConsumer(other_store)))
            )
        self.assertEqual(sum(r.replay for r in results), 1)
        self.assertEqual(self.counts(), (1, 1, 0))

    def test_independent_connection_distinct_time_race(self) -> None:
        barrier = threading.Barrier(2)

        def writer(row: Observation) -> Receipt:
            barrier.wait(timeout=10)
            return self.consume([row], consumer=SensorConsumer(self.store))[0]

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(writer, observations()))
        self.assertIn(
            [r.reason for r in results], (["ACCEPTED", "ACCEPTED"], ["OUT_OF_ORDER", "ACCEPTED"])
        )
        self.assertEqual(self.counts()[1], 2)

    def test_current_controls_home_rechecked_after_waiting_writer(self) -> None:
        baseline = observations()[0]
        for index, (field, value, reason) in enumerate(
            (
                ("consent", "declined", "CONSENT"),
                ("home_id", "ZF-OTHER", "HOME_MISMATCH"),
                ("calibration_confirmed", False, "CALIBRATION"),
                ("missing_home", True, "HOME_UNAVAILABLE"),
            )
        ):
            self.consumer.configure(POLICY, [CONTROL])
            waiting = threading.Event()
            stale = SensorConsumer(self.store)

            def admission(
                waiting: threading.Event = waiting,
                index: int = index,
                stale: SensorConsumer = stale,
            ) -> Receipt:
                waiting.set()
                return self.consume(
                    [{**baseline, "reading_id": f"CURRENT-{index}"}], consumer=stale
                )[0]

            with ThreadPoolExecutor(max_workers=1) as pool:
                with self.consumer._write() as db:
                    future = pool.submit(admission)
                    self.assertTrue(waiting.wait(timeout=10))
                    if field == "missing_home":
                        db.execute("DELETE FROM cases WHERE id='ZF-1'")
                    else:
                        body = asdict(CONTROL)
                        body[field] = value
                        db.execute(
                            "UPDATE sensor_consumer_control SET body=? WHERE sensor_id=?",
                            (json.dumps(body), CONTROL.sensor_id),
                        )
                result = future.result(timeout=20)
            self.assertEqual(result.reason, reason)
        self.assertEqual(self.counts(), (0, 4, 4))

    def _trigger(self, table: str, remove: bool = False) -> None:
        name = "sensor_test_failure"
        if self.consumer.mssql:
            self.store.db.execute(f"IF OBJECT_ID(N'{name}', N'TR') IS NOT NULL DROP TRIGGER {name}")
            if not remove:
                self.store.db.execute(
                    f"CREATE TRIGGER {name} ON {table} AFTER INSERT AS"
                    " THROW 50020, 'constructed failure', 1"
                )
        else:
            self.store.db.execute(f"DROP TRIGGER IF EXISTS {name}")
            if not remove:
                self.store.db.execute(
                    f"CREATE TRIGGER {name} BEFORE INSERT ON {table}"
                    " BEGIN SELECT RAISE(ABORT, 'constructed failure'); END"
                )

    def test_real_engine_accepted_and_rejected_rollback(self) -> None:
        for fault, table in (
            (None, "sensor_delivery"),
            ("wrong_unit", "sensor_data_quality_exception"),
        ):
            self._trigger(table)
            with self.assertRaisesRegex(ConsumerError, "SENSOR_SQL_UNAVAILABLE"):
                self.consume([observations(fault)[0]])
            self.assertEqual(self.counts(), (0, 0, 0))
            self._trigger(table, remove=True)
        self.assertEqual(self.consume([observations()[0]])[0].status, "accepted")

    def test_committed_ack_loss_reopen_reconciles_both_outcomes(self) -> None:
        class LostAck(SensorConsumer):
            def acknowledge(self, receipt: Receipt) -> None:
                raise RuntimeError("not-for-diagnostics")

        for fault, expected in ((None, "accepted"), ("wrong_unit", "rejected")):
            row = observations(fault)[0]
            with self.assertRaisesRegex(ConsumerError, "SENSOR_COMMIT_UNCERTAIN") as caught:
                self.consume([row], consumer=LostAck(self.store))
            reopened = store_at(self.tmp.name)
            self.addCleanup(reopened.db.close)
            result = self.consume([row], consumer=SensorConsumer(reopened))[0]
            self.assertEqual(result.reference, caught.exception.reference)
            self.assertEqual(result.status, expected)
            self.assertTrue(result.replay)
        self.assertEqual(self.counts(), (1, 2, 1))

    def test_legacy_reading_without_witness_is_not_success(self) -> None:
        row = observations()[0]
        self.consume([row])
        self.store.db.execute("DELETE FROM sensor_delivery")
        self.assert_rejected(row, "IDENTITY_CONFLICT")
        self.assertEqual(self.counts(), (1, 1, 1))

    def test_existing_legacy_and_stock_reading_schemas_retained(self) -> None:
        from zava_forward.core.synthetic import sensor_backfill

        for ddl in (sensor_backfill.SQL_DDL, sensor_backfill.STOCK_SQL_DDL):
            with self.consumer._write() as db:
                db.execute("DROP TABLE sensor_reading")
                if self.consumer.mssql:
                    for statement in ddl.split(";"):
                        if statement.strip().startswith("CREATE TABLE sensor_reading"):
                            db.execute(statement)
                else:
                    sensor_backfill._create_sqlite_schema(db)
            row = observations()[0]
            # Exercise migration with a populated legacy table, not only fresh DDL.
            self.store.db.execute(
                "INSERT INTO sensor_reading (sensor_id, reading_id, home_id, observed_at,"
                " temperature_c, humidity_pct, source_type, scenario, seed, schema_version)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    "LEGACY",
                    "LEGACY-1",
                    "ZF-1",
                    "2024-01-01T00:00:00" if self.consumer.mssql else "2024-01-01T00:00:00Z",
                    "20.00",
                    "50.00",
                    "SYNTHETIC",
                    "BACKFILL_2Y",
                    183,
                    "reading-v1",
                ),
            )
            self.consumer.configure(POLICY, [CONTROL])
            # Clear only the test's previous iteration witness, not production data.
            self.store.db.execute("DELETE FROM sensor_delivery")
            self.assertEqual(self.consume([row])[0].status, "accepted")
            self.assertEqual(
                self.store.db.execute(
                    "SELECT schema_version FROM sensor_reading WHERE sensor_id='LEGACY'"
                ).fetchone()[0],
                "reading-v1",
            )


if __name__ == "__main__":
    unittest.main()
