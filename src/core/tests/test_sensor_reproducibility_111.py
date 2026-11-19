"""Cross-store sensor analysis, review task, and digest reproducibility (Refs #111).

Fictional exercise data and constructed approvals: SYNTHETIC TEST ONLY, never an operational rule
or signoff. Missing, stale, unconsented, weather-only, or unreadable data is INSUFFICIENT/STALE/
DECLINED, carries priority_effect == "NONE", never mutates ranking, and never duplicates tasks.
"""

import copy
import json
import os
import random
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Callable, Mapping, Sequence
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Protocol, cast
from unittest import mock

import dataset
from sensor_consumer_fixture import CONTROL, POLICY
from zava_forward.core import projection
from zava_forward.core import sensor_analysis as sa
from zava_forward.core import sensor_analysis_store as sas
from zava_forward.core import sensor_review_draft as srd
from zava_forward.core.sensor_consumer import (
    READING_COLUMNS,
    ConsumerError,
    Observation,
    SensorConsumer,
    SensorControl,
    preflight,
)
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store
from zava_forward.core.synthetic import sensor_scenarios as ss
from zava_forward.core.synthetic.live_readings import Reading

HOME = CONTROL.home_id
WINDOW = ss.Window(ss.START, ss.START + timedelta(days=ss.DAYS))
AS_OF = WINDOW.end
STAMP_START = "2024-01-01T00:00:00Z"
STAMP_END = "2024-01-30T00:00:00Z"
RECEIVED = STAMP_END
SC_POLICY = replace(
    POLICY, window_start=STAMP_START, window_end=STAMP_END, max_past_seconds=86400 * 30
)
SC_CONTROL = replace(
    CONTROL,
    mapping_start=STAMP_START,
    mapping_end=STAMP_END,
    calibration_start=STAMP_START,
    calibration_end=STAMP_END,
)
SYNTHETIC_APPROVAL = sa.RuleApproval(
    sa.RULE_ID, sa.ANALYSIS_VERSION, "SYNTHETIC TEST ONLY", "SYNTHETIC-TEST-SENTINEL"
)
APPROVED = sa.AnalysisPolicy(approval=SYNTHETIC_APPROVAL)
SCENARIOS = {c.truth.label: c for c in ss.generate() if c.truth.family == "damp"}
PEOPLE = {
    role: dict(code=f"R{i}", name=f"Person {i}", email=f"p{i}@example.test", role=role)
    for i, role in enumerate(
        projection.STAFF_ROLES + ("Contractor", "Application Administrator", "Resident")
    )
}
QI = PEOPLE["Quality Inspector"]

_OPEN_JSON_STORE = cast(Callable[[str], Store], Store)
_OPEN_SQL_STORE = cast(Callable[[str, str], SqlStore], SqlStore)

FRESH_REPRODUCE = """
import json, sys
from datetime import timedelta
from zava_forward.core import sensor_analysis as sa
from zava_forward.core import sensor_analysis_store as sas
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store
from zava_forward.core.synthetic import sensor_scenarios as ss

kind, seed_path, second_arg, home = sys.argv[1:5]
policy = sa.AnalysisPolicy(
    approval=sa.RuleApproval(
        sa.RULE_ID, sa.ANALYSIS_VERSION, "SYNTHETIC TEST ONLY", "SYNTHETIC-TEST-SENTINEL"
    )
)
window = ss.Window(ss.START, ss.START + timedelta(days=ss.DAYS))
if kind == "json":
    target = Store(seed_path)
    payload = sas.reproduce_retained(target, home, window, window.end, policy)
else:
    sql_target = SqlStore(seed_path, second_arg)
    try:
        payload = sas.reproduce_retained(sql_target, home, window, window.end, policy)
    finally:
        sql_target.db.close()
print(json.dumps(payload, sort_keys=True))
"""


class _RankedCarrier(Protocol):
    cases: dict[str, dict[str, Any]]
    live_path: str

    def _ranking(self) -> dict[str, dict[str, Any]]: ...


class _PermutedSource:
    def __init__(
        self,
        consent: str,
        envelopes: Sequence[dict[str, str]],
    ) -> None:
        self._consent = consent
        self._envelopes = [dict(row) for row in envelopes]

    def home_consent(self, home_id: str) -> str:
        return self._consent if home_id == HOME else "unknown"

    def retained_envelopes(
        self,
        home_ids: Sequence[str],
        windows: Mapping[str, tuple[str, str]] | None = None,
    ) -> list[dict[str, str]]:
        _ = (home_ids, windows)
        return [dict(row) for row in self._envelopes]


def _write_seed(directory: Path) -> Path:
    data = copy.deepcopy(dataset.DATA)
    data["staff"] = list(PEOPLE.values())
    seed_path = directory / "seed.json"
    seed_path.write_text(json.dumps(data), encoding="utf-8")
    return seed_path


def _scenario_rows(label: str) -> list[dict[str, str]]:
    return [
        {str(k): str(v) for k, v in dict(r, home_id=HOME, sensor_id=SC_CONTROL.sensor_id).items()}
        for r in SCENARIOS[label].rows
    ]


def _observations(rows: Sequence[Mapping[str, str]]) -> list[Observation]:
    return [{str(k): str(v) for k, v in row.items()} for row in rows]


def _ranking_snapshot(target: Store | SqlStore) -> str:
    ranked = cast(_RankedCarrier, target)
    return json.dumps(ranked._ranking(), sort_keys=True)


def _hazards_snapshot(target: Store | SqlStore) -> str:
    ranked = cast(_RankedCarrier, target)
    payload = {cid: case.get("hazards", []) for cid, case in sorted(ranked.cases.items())}
    return json.dumps(payload, sort_keys=True)


def _sql_cases_ranking_columns(sql_store: SqlStore) -> list[tuple[object, ...]]:
    rows = sql_store.db.execute(
        "SELECT id, rkey, priority_correction, queue_new, queue_priority,"
        " queue_stale, queue_blocked, queue_overdue, queue_unowned"
        " FROM cases ORDER BY id"
    ).fetchall()
    return [tuple(row) for row in rows]


class ReproducibilityAcrossStoresTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        env_patch = mock.patch.dict(os.environ, {srd.FLAG: "1", "ZF_SENSOR_MSSQL": ""})
        env_patch.start()
        self.addCleanup(env_patch.stop)

    def _open_pair(self, name: str) -> tuple[Path, Store, Path, SqlStore]:
        folder = Path(self.tmp.name) / name
        folder.mkdir(parents=True, exist_ok=True)
        seed_path = _write_seed(folder)
        json_store = _OPEN_JSON_STORE(str(seed_path))
        db_path = folder / "state.sqlite"
        sql_store = _OPEN_SQL_STORE(str(seed_path), str(db_path))
        self.addCleanup(sql_store.db.close)
        return seed_path, json_store, db_path, sql_store

    def _ingest_pair(
        self,
        json_store: Store,
        sql_store: SqlStore,
        rows: Sequence[Mapping[str, str]],
        controls: Sequence[SensorControl] = (SC_CONTROL,),
        *,
        chunk_size: int = 100,
    ) -> SensorConsumer:
        added = sas.retain_json_readings(json_store, controls, rows)
        self.assertEqual(added, len(rows))
        consumer = SensorConsumer(sql_store)
        consumer.configure(SC_POLICY, controls)
        obs = _observations(rows)
        for start in range(0, len(obs), chunk_size):
            for item in preflight(obs[start : start + chunk_size]):
                receipt = consumer.process(item, RECEIVED)
                self.assertEqual(receipt.status, "accepted")
        return consumer

    def test_cross_store_parity_and_reload_durability(self) -> None:
        with self.assertRaises(ConsumerError) as sql_only_err:
            SensorConsumer(_OPEN_JSON_STORE(str(_write_seed(Path(self.tmp.name)))))
        self.assertEqual(sql_only_err.exception.code, "UNSUPPORTED_STORE_SQL_REQUIRED")

        for label, expects_task in (
            ("sustained_high_humidity", True),
            ("repeated_overnight_peaks", True),
            ("normal", False),
        ):
            with self.subTest(label=label):
                seed_path, json_store, _, sql_store = self._open_pair(f"parity-{label}")
                with self.assertRaises(ConsumerError) as json_req_err:
                    sas.retain_json_readings(sql_store, [SC_CONTROL], [])
                self.assertEqual(json_req_err.exception.code, "JSON_STORE_REQUIRED")
                with self.assertRaises(ConsumerError) as adapter_err:
                    sas.JsonRetainedStore(sql_store)
                self.assertEqual(adapter_err.exception.code, "JSON_STORE_REQUIRED")

                rows = _scenario_rows(label)
                self._ingest_pair(json_store, sql_store, rows)
                reopened_json = _OPEN_JSON_STORE(str(seed_path))

                pure_task = sa.reproduce_review_task(
                    rows, APPROVED, home_id=HOME, window=WINDOW, as_of=AS_OF
                )
                pure_full = sa.reproduce_sensor_analysis(
                    rows, APPROVED, home_id=HOME, window=WINDOW, as_of=AS_OF
                )
                json_sig = sas.analyse_retained(json_store, HOME, WINDOW, AS_OF, APPROVED)
                reopened_sig = sas.analyse_retained(reopened_json, HOME, WINDOW, AS_OF, APPROVED)
                sql_sig = sas.analyse_retained(sql_store, HOME, WINDOW, AS_OF, APPROVED)
                self.assertEqual(json_sig, sql_sig)
                self.assertEqual(reopened_sig, sql_sig)

                json_rep = sas.reproduce_retained(json_store, HOME, WINDOW, AS_OF, APPROVED)
                reopened_rep = sas.reproduce_retained(reopened_json, HOME, WINDOW, AS_OF, APPROVED)
                sql_rep = sas.reproduce_retained(sql_store, HOME, WINDOW, AS_OF, APPROVED)
                self.assertEqual(json_rep, sql_rep)
                self.assertEqual(reopened_rep, sql_rep)
                self.assertEqual(json_rep, pure_task)
                self.assertEqual(
                    json_rep["provenance"]["output_digest"],
                    pure_full["output_digest"],
                )
                self.assertEqual(
                    json_rep["provenance"]["policy_digest"],
                    sa.policy_digest(APPROVED),
                )
                self.assertEqual(bool(json_rep["review_task"]), expects_task)

                unapproved_json = srd.draft_from_retained(json_store, QI, HOME, WINDOW, AS_OF)
                unapproved_sql = srd.draft_from_retained(sql_store, QI, HOME, WINDOW, AS_OF)
                self.assertEqual(unapproved_json, unapproved_sql)
                expected_refusal = "NO_APPROVED_RULE" if expects_task else "NO_REVIEW_SIGNAL"
                self.assertEqual(unapproved_json["refusal"], expected_refusal)

                with mock.patch.object(srd, "server_policy", return_value=APPROVED):
                    draft_json = srd.draft_from_retained(
                        json_store, QI, HOME, WINDOW, AS_OF, at="2026-11-15T07:00:00Z"
                    )
                    draft_sql = srd.draft_from_retained(
                        sql_store, QI, HOME, WINDOW, AS_OF, at="2026-11-15T07:00:00Z"
                    )
                self.assertEqual(draft_json, draft_sql)
                self.assertEqual(draft_json["created"], expects_task)
                reloaded_after_draft = _OPEN_JSON_STORE(str(seed_path))
                read_json = srd.read_drafts(json_store, QI, HOME)
                read_reloaded = srd.read_drafts(reloaded_after_draft, QI, HOME)
                read_sql = srd.read_drafts(sql_store, QI, HOME)
                self.assertEqual(read_json, read_sql)
                self.assertEqual(read_reloaded, read_sql)

    def test_sql_physical_row_order_chunking_and_reading_id_tie_breaking(self) -> None:
        rows = _scenario_rows("sustained_high_humidity")
        _, _, _, sql_forward = self._open_pair("sql-forward")
        consumer_forward = SensorConsumer(sql_forward)
        consumer_forward.configure(SC_POLICY, [SC_CONTROL])
        obs = _observations(rows)
        for start in range(0, len(obs), 100):
            for item in preflight(obs[start : start + 100]):
                self.assertEqual(consumer_forward.process(item, RECEIVED).status, "accepted")

        _, _, _, sql_chunk29 = self._open_pair("sql-chunk29")
        consumer_chunk29 = SensorConsumer(sql_chunk29)
        consumer_chunk29.configure(SC_POLICY, [SC_CONTROL])
        for start in range(0, len(obs), 29):
            for item in preflight(obs[start : start + 29]):
                self.assertEqual(consumer_chunk29.process(item, RECEIVED).status, "accepted")
        for item in preflight(obs[:40]):
            replay_receipt = consumer_chunk29.process(item, RECEIVED)
            self.assertTrue(replay_receipt.replay)

        _, _, _, sql_shuffled_insert = self._open_pair("sql-shuffled-insert")
        consumer_shuffled = SensorConsumer(sql_shuffled_insert)
        consumer_shuffled.configure(SC_POLICY, [SC_CONTROL])
        stored_readings = list(
            sql_forward.db.execute(
                f"SELECT {', '.join(READING_COLUMNS)} FROM sensor_reading"
            ).fetchall()
        )
        stored_deliveries = list(
            sql_forward.db.execute(
                "SELECT reference, status, reason, received_at, observation_body"
                " FROM sensor_delivery"
            ).fetchall()
        )
        rng = random.Random(20261115)
        rng.shuffle(stored_readings)
        stored_deliveries.reverse()
        placeholders = ", ".join("?" for _ in READING_COLUMNS)
        with sql_shuffled_insert.dblock:
            for r_row in stored_readings:
                sql_shuffled_insert.db.execute(
                    f"INSERT INTO sensor_reading ({', '.join(READING_COLUMNS)})"
                    f" VALUES ({placeholders})",
                    tuple(r_row),
                )
            for d_row in stored_deliveries:
                sql_shuffled_insert.db.execute(
                    "INSERT INTO sensor_delivery"
                    " (reference, status, reason, received_at, observation_body)"
                    " VALUES (?, ?, ?, ?, ?)",
                    tuple(d_row),
                )

        baseline = sas.reproduce_retained(sql_forward, HOME, WINDOW, AS_OF, APPROVED)
        self.assertEqual(
            sas.reproduce_retained(sql_chunk29, HOME, WINDOW, AS_OF, APPROVED),
            baseline,
        )
        self.assertEqual(
            sas.reproduce_retained(sql_shuffled_insert, HOME, WINDOW, AS_OF, APPROVED),
            baseline,
        )

        envelopes = consumer_forward.retained_envelopes([HOME])
        reversed_source = _PermutedSource("granted", list(reversed(envelopes)))
        shuffled_envelopes = list(envelopes)
        rng.shuffle(shuffled_envelopes)
        shuffled_source = _PermutedSource("granted", shuffled_envelopes)
        self.assertEqual(
            sas.reproduce_retained(reversed_source, HOME, WINDOW, AS_OF, APPROVED),
            baseline,
        )
        self.assertEqual(
            sas.reproduce_retained(shuffled_source, HOME, WINDOW, AS_OF, APPROVED),
            baseline,
        )

        _, tie_json, _, tie_sql = self._open_pair("sql-tie-break")
        tie_consumer = SensorConsumer(tie_sql)
        tie_consumer.configure(SC_POLICY, [SC_CONTROL])
        v1_cols = tuple(col for col in READING_COLUMNS if col != "injected_fault")
        tie_z = {
            "sensor_id": SC_CONTROL.sensor_id,
            "reading_id": "READ-TIE-Z",
            "home_id": HOME,
            "observed_at": "2024-01-02T00:00:00Z",
            "temperature_c": "18.50",
            "humidity_pct": "79.00",
            "source_type": "SYNTHETIC",
            "scenario": "tie-check",
            "seed": "111",
            "schema_version": "reading-v1",
        }
        tie_a = dict(tie_z, reading_id="READ-TIE-A", humidity_pct="80.00")
        sas.retain_json_readings(tie_json, [SC_CONTROL], [tie_z, tie_a])
        with tie_sql.dblock:
            for tie_row in (tie_z, tie_a):
                tie_sql.db.execute(
                    f"INSERT INTO sensor_reading ({', '.join(READING_COLUMNS)})"
                    f" VALUES ({placeholders})",
                    tuple(tie_row[c] for c in v1_cols) + (None,),
                )
        sql_ties = tie_consumer.retained_envelopes([HOME])
        json_ties = sas.JsonRetainedStore(tie_json).retained_envelopes([HOME])
        self.assertEqual([r["reading_id"] for r in sql_ties], ["READ-TIE-A", "READ-TIE-Z"])
        self.assertEqual(sql_ties, json_ties)
        self.assertEqual(
            sas.reproduce_retained(tie_sql, HOME, WINDOW, AS_OF, APPROVED),
            sas.reproduce_retained(tie_json, HOME, WINDOW, AS_OF, APPROVED),
        )

    def test_duplicate_and_out_of_order_replay_idempotence_and_conflict_rejection(self) -> None:
        rows = _scenario_rows("repeated_overnight_peaks")
        clean_sig = sa.derive_signal(HOME, rows, WINDOW, AS_OF, "granted", APPROVED)
        clean_tuples = sa.reading_tuples(rows)
        clean_analysis = sa.reproduce_sensor_analysis(
            rows, APPROVED, home_id=HOME, window=WINDOW, as_of=AS_OF
        )
        clean_task = sa.reproduce_review_task(
            rows, APPROVED, home_id=HOME, window=WINDOW, as_of=AS_OF
        )

        replayed = list(rows) + [dict(r) for r in rows[:25]] + [dict(r) for r in rows[-15:]]
        random.Random(111).shuffle(replayed)
        self.assertEqual(
            sa.derive_signal(HOME, replayed, WINDOW, AS_OF, "granted", APPROVED),
            clean_sig,
        )
        self.assertEqual(sa.reading_tuples(replayed), clean_tuples)
        self.assertEqual(
            sa.reproduce_sensor_analysis(
                replayed, APPROVED, home_id=HOME, window=WINDOW, as_of=AS_OF
            ),
            clean_analysis,
        )
        self.assertEqual(
            sa.reproduce_review_task(replayed, APPROVED, home_id=HOME, window=WINDOW, as_of=AS_OF),
            clean_task,
        )

        _, json_store, _, sql_store = self._open_pair("replay-stores")
        consumer = self._ingest_pair(json_store, sql_store, rows)
        before_json = sas.reproduce_retained(json_store, HOME, WINDOW, AS_OF, APPROVED)
        before_sql = sas.reproduce_retained(sql_store, HOME, WINDOW, AS_OF, APPROVED)
        self.assertEqual(before_json, clean_task)
        self.assertEqual(before_sql, clean_task)

        partial_replay = [dict(r) for r in reversed(rows[:30])]
        self.assertEqual(sas.retain_json_readings(json_store, [SC_CONTROL], partial_replay), 0)
        for item in preflight(_observations(rows[:30])):
            self.assertTrue(consumer.process(item, RECEIVED).replay)
        self.assertEqual(
            sas.reproduce_retained(json_store, HOME, WINDOW, AS_OF, APPROVED),
            before_json,
        )
        self.assertEqual(
            sas.reproduce_retained(sql_store, HOME, WINDOW, AS_OF, APPROVED),
            before_sql,
        )

        conflicting_same_id = dict(rows[0], humidity_pct="11.00")
        with self.assertRaises(ConsumerError) as conflict_err:
            sas.retain_json_readings(json_store, [SC_CONTROL], [conflicting_same_id])
        self.assertEqual(conflict_err.exception.code, "IDENTITY_CONFLICT")

        conflicting_same_slot = dict(rows[5], reading_id="CONFLICT-SLOT-5", humidity_pct="11.00")
        conflict_out = sa.reproduce_review_task(
            [*rows, conflicting_same_slot],
            APPROVED,
            home_id=HOME,
            window=WINDOW,
            as_of=AS_OF,
        )
        self.assertEqual(conflict_out["signal"]["sufficiency"], sa.INSUFFICIENT)
        self.assertIn("DUPLICATE", conflict_out["signal"]["reasons"])
        self.assertIsNone(conflict_out["review_task"])
        self.assertNotEqual(
            conflict_out["provenance"]["input_digest"],
            clean_task["provenance"]["input_digest"],
        )

    def test_insufficient_fallbacks_never_mutate_priority_or_duplicate_tasks(self) -> None:
        _, json_store, _, sql_store = self._open_pair("fallbacks-and-ranking")
        json_rank_before = _ranking_snapshot(json_store)
        sql_rank_before = _ranking_snapshot(sql_store)
        sql_cols_before = _sql_cases_ranking_columns(sql_store)
        json_haz_before = _hazards_snapshot(json_store)
        sql_haz_before = _hazards_snapshot(sql_store)

        for target in (json_store, sql_store):
            unconfigured = sas.reproduce_retained(target, HOME, WINDOW, AS_OF, APPROVED)
            self.assertEqual(unconfigured["signal"]["sufficiency"], sa.INSUFFICIENT)
            self.assertEqual(unconfigured["signal"]["reasons"], (sas.UNAVAILABLE,))
            self.assertEqual(unconfigured["signal"]["priority_effect"], "NONE")
            self.assertFalse(unconfigured["signal"]["diagnoses_hazard"])
            self.assertIsNone(unconfigured["review_task"])
            self.assertEqual(srd.read_drafts(target, QI, HOME)["state"], "consent-withheld")
            with mock.patch.object(srd, "server_policy", return_value=APPROVED):
                refused = srd.draft_from_retained(target, QI, HOME, WINDOW, AS_OF)
            self.assertEqual(refused["refusal"], "RETAINED_READINGS_UNAVAILABLE")

        rows = _scenario_rows("sustained_high_humidity")
        consumer = self._ingest_pair(json_store, sql_store, rows)

        weather_window = ss.Window(WINDOW.end, WINDOW.end + timedelta(days=1))
        weather_row = Reading(
            HOME,
            SC_CONTROL.sensor_id,
            "SYN-SENS-SYN-1",
            datetime(2024, 1, 29, 1, 5, tzinfo=UTC),
            12.34,
            66.5,
            301.25,
            184,
        ).row()
        self.assertEqual(sas.retain_json_readings(json_store, [SC_CONTROL], [weather_row]), 1)
        self.assertEqual(consumer.process(dict(weather_row), RECEIVED).status, "accepted")
        for target in (json_store, sql_store):
            weather_out = sas.reproduce_retained(
                target, HOME, weather_window, weather_window.end, APPROVED
            )
            self.assertEqual(weather_out["signal"]["reasons"], (sas.WEATHER_NOT_INDOOR,))
            self.assertEqual(weather_out["signal"]["priority_effect"], "NONE")
            self.assertIsNone(weather_out["review_task"])

        later_window = ss.Window(WINDOW.end + timedelta(days=2), WINDOW.end + timedelta(days=3))
        for target in (json_store, sql_store):
            stale_out = sas.reproduce_retained(
                target, HOME, WINDOW, AS_OF + timedelta(days=30), APPROVED
            )
            self.assertEqual(stale_out["signal"]["sufficiency"], sa.STALE)
            self.assertEqual(stale_out["signal"]["reasons"], ("LATEST_READING_STALE",))
            self.assertEqual(stale_out["signal"]["priority_effect"], "NONE")
            self.assertIsNone(stale_out["review_task"])

            empty_out = sas.reproduce_retained(
                target, HOME, later_window, later_window.end, APPROVED
            )
            self.assertEqual(empty_out["signal"]["sufficiency"], sa.STALE)
            self.assertEqual(empty_out["signal"]["reasons"], ("NO_READINGS_IN_WINDOW",))
            self.assertEqual(empty_out["signal"]["priority_effect"], "NONE")
            self.assertIsNone(empty_out["review_task"])

        for consent, expected_suff, expected_reason in (
            ("declined", sa.DECLINED, "MONITORING_DECLINED"),
            ("unknown", sa.INSUFFICIENT, "CONSENT_NOT_CONFIRMED"),
        ):
            updated_control = replace(SC_CONTROL, consent=consent)
            sas.retain_json_readings(json_store, [updated_control], [])
            consumer.configure(SC_POLICY, [updated_control])
            for target in (json_store, sql_store):
                consent_out = sas.reproduce_retained(target, HOME, WINDOW, AS_OF, APPROVED)
                self.assertEqual(consent_out["signal"]["sufficiency"], expected_suff)
                self.assertEqual(consent_out["signal"]["reasons"], (expected_reason,))
                self.assertEqual(consent_out["signal"]["priority_effect"], "NONE")
                self.assertIsNone(consent_out["review_task"])

        sas.retain_json_readings(json_store, [SC_CONTROL], [])
        consumer.configure(SC_POLICY, [SC_CONTROL])
        with mock.patch.object(srd, "server_policy", return_value=APPROVED):
            first_json = srd.draft_from_retained(
                json_store, QI, HOME, WINDOW, AS_OF, at="2026-11-15T07:30:00Z"
            )
            first_sql = srd.draft_from_retained(
                sql_store, QI, HOME, WINDOW, AS_OF, at="2026-11-15T07:30:00Z"
            )
            self.assertTrue(first_json["created"])
            self.assertEqual(first_json, first_sql)
            for delta_hours in (0, 2):
                replay_json = srd.draft_from_retained(
                    json_store,
                    QI,
                    HOME,
                    WINDOW,
                    AS_OF + timedelta(hours=delta_hours),
                    at="2026-11-16T00:00:00Z",
                )
                replay_sql = srd.draft_from_retained(
                    sql_store,
                    QI,
                    HOME,
                    WINDOW,
                    AS_OF + timedelta(hours=delta_hours),
                    at="2026-11-16T00:00:00Z",
                )
                self.assertEqual((replay_json["created"], replay_json["existing"]), (False, True))
                self.assertEqual(replay_json, replay_sql)

        self.assertEqual(len(cast(_RankedCarrier, json_store).cases[HOME][srd.CASE_KEY]), 1)
        self.assertEqual(len(cast(_RankedCarrier, sql_store).cases[HOME][srd.CASE_KEY]), 1)
        self.assertEqual(_ranking_snapshot(json_store), json_rank_before)
        self.assertEqual(_ranking_snapshot(sql_store), sql_rank_before)
        self.assertEqual(_sql_cases_ranking_columns(sql_store), sql_cols_before)
        self.assertEqual(_hazards_snapshot(json_store), json_haz_before)
        self.assertEqual(_hazards_snapshot(sql_store), sql_haz_before)

    def test_fresh_process_hashseed_determinism_across_store_and_sqlstore(self) -> None:
        seed_path, json_store, db_path, sql_store = self._open_pair("hashseed-subprocesses")
        rows = _scenario_rows("sustained_high_humidity")
        self._ingest_pair(json_store, sql_store, rows)
        expected = json.dumps(
            sas.reproduce_retained(sql_store, HOME, WINDOW, AS_OF, APPROVED),
            sort_keys=True,
        )
        src_root = Path(__file__).resolve().parents[1] / "src"
        tests_root = Path(__file__).resolve().parent
        python_path = f"{src_root}{os.pathsep}{tests_root}"

        for kind, second_arg in (("json", "-"), ("sql", str(db_path))):
            for hash_seed in ("1", "424242"):
                env = dict(
                    os.environ,
                    PYTHONHASHSEED=hash_seed,
                    PYTHONDONTWRITEBYTECODE="1",
                    PYTHONPATH=python_path,
                    ZF_SENSOR_MSSQL="",
                )
                completed = subprocess.run(
                    [
                        sys.executable,
                        "-B",
                        "-c",
                        FRESH_REPRODUCE,
                        kind,
                        str(seed_path),
                        second_arg,
                        HOME,
                    ],
                    capture_output=True,
                    check=True,
                    env=env,
                    text=True,
                )
                self.assertEqual(completed.stdout.strip(), expected)


if __name__ == "__main__":
    unittest.main()
