"""End-to-end sensor non-authority invariant tests across all core workflows (Refs #109).

Proves across ingestion, deterministic analysis, retained reproduction, review drafts, JSON Store,
SqlStore, hazards, Awaab's Law / external service clocks, safety and legal holds, gates, and
deterministic home ranking that sensor readings, signals, absence of alerts, and unapproved drafts
never diagnose a hazard, start a clock, release a hold, or alter home ranking.
"""

import copy
import json
import os
import tempfile
import unittest
from collections.abc import Callable, Iterable, Mapping, Sequence
from contextlib import AbstractContextManager
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Protocol, cast
from unittest import mock

import dataset
from sensor_consumer_fixture import CONTROL, POLICY
from zava_forward.core import (
    controls,
    gates,
    ranking,
)
from zava_forward.core import (
    sensor_analysis as sa,
)
from zava_forward.core import (
    sensor_analysis_store as sas,
)
from zava_forward.core import (
    sensor_ingest as si,
)
from zava_forward.core import (
    sensor_review_draft as srd,
)
from zava_forward.core.sensor_consumer import Observation, SensorConsumer
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store
from zava_forward.core.synthetic import live_readings, sensor_consistency
from zava_forward.core.synthetic import sensor_scenarios as ss

CID = "ZF-1"
AS_OF = "2026-11-15"
AWARE_AT = "2026-01-02T09:00+00:00"
RESPONSE_DUE_AT = "2026-01-03T09:00+00:00"
RESPONDED_AT = "2026-01-02T15:00+00:00"
UPDATE_DUE_AT = "2026-01-04T09:00+00:00"
WINDOW = ss.Window(ss.START, ss.START + timedelta(days=ss.DAYS))
SCENARIOS = {c.truth.label: c for c in ss.generate() if c.truth.family == "damp"}
SYNTHETIC_APPROVAL = sa.RuleApproval(
    sa.RULE_ID, sa.ANALYSIS_VERSION, "SYNTHETIC TEST ONLY", "SYNTHETIC-TEST-109"
)
APPROVED_POLICY = sa.AnalysisPolicy(approval=SYNTHETIC_APPROVAL)
TOLERANCE = sensor_consistency.Tolerance(point=25.0, mean_step=25.0)

STAFF: tuple[dict[str, Any], ...] = (
    {
        "code": "QI-1",
        "name": "Quinn Inspector",
        "email": "quinn@example.test",
        "role": "Quality Inspector",
    },
    {
        "code": "PM-1",
        "name": "Pat Manager",
        "email": "pat@example.test",
        "role": "Retrofit Programme Manager",
    },
    {
        "code": "RC-1",
        "name": "Rex Coordinator",
        "email": "rex@example.test",
        "role": "Retrofit Coordinator",
    },
    {
        "code": "BS-1",
        "name": "Bea Safe",
        "email": "bea@example.test",
        "role": "Building Safety Liaison",
    },
    {
        "code": "BS-2",
        "name": "Bo Safe",
        "email": "bo@example.test",
        "role": "Building Safety Liaison",
    },
)
QI, PM, RC, BEA, BO = STAFF


class _WorkflowStore(Protocol):
    lock: AbstractContextManager[object]
    cases: dict[str, dict[str, Any]]
    staff: dict[str, dict[str, Any]]
    db: Any

    def _case(self, case_id: str) -> dict[str, Any]: ...
    def save(self) -> None: ...
    def audit(self, who: str, action: str, case_id: str, detail: str) -> None: ...
    def audit_entries(self, case_id: str | None = None) -> Iterable[dict[str, Any]]: ...
    def _ranking(self) -> list[dict[str, Any]]: ...
    def raise_hazard(
        self,
        user: Mapping[str, Any],
        case_id: str,
        category: str,
        priority: str,
        note: str = "",
        metadata: Mapping[str, Any] | None = None,
    ) -> int: ...
    def refer_hazard(
        self,
        user: Mapping[str, Any],
        case_id: str,
        idx: int,
        to_email: str,
        job: str,
        metadata: Mapping[str, Any] | None = None,
    ) -> None: ...
    def receive_hazard(
        self, user: Mapping[str, Any], case_id: str, idx: int, evidence: object
    ) -> None: ...
    def accept_hazard(
        self, user: Mapping[str, Any], case_id: str, idx: int, evidence: object
    ) -> None: ...
    def observe_hazard_times(
        self,
        user: Mapping[str, Any],
        case_id: str,
        idx: int,
        metadata: Mapping[str, Any] | None,
    ) -> None: ...
    def record_repair(
        self, user: Mapping[str, Any], case_id: str, idx: int, evidence: object = None
    ) -> None: ...
    def release_hazard(
        self,
        user: Mapping[str, Any],
        case_id: str,
        idx: int,
        note: str = "",
        evidence: object = None,
    ) -> None: ...
    def place_legal_hold(
        self, user: Mapping[str, Any], case_id: str, reference: object
    ) -> dict[str, Any]: ...
    def release_legal_hold(self, user: Mapping[str, Any], case_id: str) -> None: ...


_open_json_store = cast(Callable[[str], _WorkflowStore], Store)
_open_sql_store = cast(Callable[[str, str], _WorkflowStore], SqlStore)
_rank = cast(
    Callable[[Sequence[Mapping[str, Any]], Mapping[str, Any], str | None], list[dict[str, Any]]],
    ranking.rank,
)
_reasons = cast(Callable[[Mapping[str, Any]], list[tuple[str, str]]], ranking.reasons)
_sql_key = cast(Callable[[Mapping[str, Any], Mapping[str, Any]], str], ranking.sql_key)
_evidence_text = cast(Callable[[object, str], str], controls.evidence_text)
_is_sensor_ref = cast(Callable[[object], bool], controls.is_sensor_reference)
_CURRENT_POLICY: dict[str, Any] = cast(dict[str, Any], ranking.CURRENT)
_SENSOR_REFUSAL = str(controls.SENSOR_REFUSAL)


def _scenario_rows(label: str = "sustained_high_humidity") -> list[dict[str, str]]:
    return [{**row, "home_id": CID, "sensor_id": "SENS-SYN-1"} for row in SCENARIOS[label].rows]


def _sample_signal(label: str = "sustained_high_humidity") -> sa.Signal:
    return sa.derive_signal(
        CID, _scenario_rows(label), WINDOW, WINDOW.end, "granted", APPROVED_POLICY
    )


def _ingest_all(
    consumer: SensorConsumer, rows: Sequence[Mapping[str, Any]], received_at: str
) -> si.WindowReceipt:
    accepted = 0
    replayed = 0
    rejected: dict[str, int] = {}
    for start in range(0, len(rows), 100):
        chunk = [cast(Observation, dict(r)) for r in rows[start : start + 100]]
        part = si.ingest_window(consumer, chunk, received_at)
        sa.enforce_sensor_non_authority(part)
        accepted += part.accepted
        replayed += part.replayed
        for reason, count in part.rejected.items():
            rejected[reason] = rejected.get(reason, 0) + count
    return si.WindowReceipt(accepted, replayed, rejected)


def _configure_consumer(
    sql_store: SqlStore,
    *,
    consent: str = "granted",
    window_start: str = "2024-01-01T00:00:00Z",
    window_end: str = "2024-01-29T00:00:00Z",
) -> SensorConsumer:
    consumer = SensorConsumer(sql_store)
    pol = replace(
        POLICY,
        window_start=window_start,
        window_end=window_end,
        max_past_seconds=30 * 86400,
        max_future_seconds=0,
    )
    ctrl = replace(
        CONTROL,
        consent=consent,
        mapping_start=window_start,
        mapping_end=window_end,
        calibration_start=window_start,
        calibration_end=window_end,
    )
    consumer.configure(pol, [ctrl])
    return consumer


def _authority_fingerprint(store: _WorkflowStore) -> dict[str, Any]:
    cases = [store.cases[cid] for cid in sorted(store.cases)]
    snap = ranking.snapshot(cases, _CURRENT_POLICY, AS_OF)
    target = store.cases[CID]
    booking = [g.as_record() for g in gates.booking_gates(target, [], on=AS_OF)]
    return {
        "rank": _rank(cases, _CURRENT_POLICY, AS_OF),
        "sql_keys": [_sql_key(c, _CURRENT_POLICY) for c in cases],
        "reasons": {c["id"]: _reasons(c) for c in cases},
        "snapshot_hash": snap["snapshot_hash"],
        "store_ranking": store._ranking(),
        "hazards": copy.deepcopy(target["hazards"]),
        "legal_hold": copy.deepcopy(target.get("legal_hold")),
        "stage": target["stage"],
        "days_in_stage": target["days_in_stage"],
        "booking_gates": booking,
    }


class TestSensorNonAuthority(unittest.TestCase):
    def _make_store(self, *, sql: bool) -> _WorkflowStore:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        base = Path(tmp.name)
        data = copy.deepcopy(cast(dict[str, Any], dataset.DATA))
        data["staff"] = [copy.deepcopy(person) for person in STAFF]
        seed_path = base / "seed.json"
        seed_path.write_text(json.dumps(data), encoding="utf-8")
        if sql:
            store = _open_sql_store(str(seed_path), str(base / "state.sqlite"))
            store.db.execute("PRAGMA synchronous = OFF")
            self.addCleanup(store.db.close)
            return store
        return _open_json_store(str(seed_path))

    def _audit_count(self, store: _WorkflowStore) -> int:
        return len(list(store.audit_entries()))

    def _store_version(self, store: _WorkflowStore) -> object:
        if isinstance(store, SqlStore):
            rv: Mapping[str, int] = store._rv
            return rv[CID]
        return json.dumps(store.cases[CID], sort_keys=True)

    def test_value_and_receipt_constructors_enforce_strict_non_authority(self) -> None:
        sig = _sample_signal()
        cand = sa.review_task_candidate(sig, APPROVED_POLICY)
        self.assertIsNotNone(cand)
        assert cand is not None
        receipt = si.WindowReceipt(4, 1, {"OUT_OF_RANGE": 1})
        self.assertEqual(receipt, si.WindowReceipt(4, 1, {"OUT_OF_RANGE": 1}))
        for valid in (sig, cand, receipt, sa.as_dict(sig), sa.as_dict(cand)):
            sa.enforce_sensor_non_authority(valid)

        bad_signal_Mutations: tuple[dict[str, Any], ...] = (
            {"priority_effect": "EMERGENCY"},
            {"priority_effect": ""},
            {"diagnoses_hazard": True},
            {"diagnoses_hazard": 1},
            {"diagnoses_hazard": 0},
        )
        for changes in bad_signal_Mutations:
            with self.subTest(target="Signal", changes=changes):
                with self.assertRaisesRegex(ValueError, sa.SENSOR_NON_AUTHORITY_ERROR):
                    replace(sig, **changes)

        bad_candidate_mutations: tuple[dict[str, Any], ...] = (
            {"task_type": "HAZARD_RAISED"},
            {"queue": "safety-referrals"},
            {"status": "APPROVED"},
            {"resident_report_unaffected": False},
            {"resident_report_unaffected": 1},
            {"changes_ranking": True},
            {"starts_clock": True},
            {"releases_hold": True},
            {"diagnoses_hazard": True},
            {"changes_ranking": 0},
        )
        for changes in bad_candidate_mutations:
            with self.subTest(target="ReviewTaskCandidate", changes=changes):
                with self.assertRaisesRegex(ValueError, sa.SENSOR_NON_AUTHORITY_ERROR):
                    replace(cand, **changes)

        for flag in ("diagnoses_hazard", "starts_clock", "releases_hold", "changes_ranking"):
            for bad_val in (True, 1, 0, "false"):
                bad_flag: dict[str, Any] = {flag: bad_val}
                with self.subTest(target="WindowReceipt", flag=flag, bad_val=bad_val):
                    with self.assertRaisesRegex(ValueError, sa.SENSOR_NON_AUTHORITY_ERROR):
                        replace(receipt, **bad_flag)

        bad_payloads: tuple[object, ...] = (
            object(),
            {},
            {**sa.as_dict(sig), "priority_effect": "RANK_UP"},
            {**sa.as_dict(sig), "diagnoses_hazard": True},
            {**sa.as_dict(cand), "changes_ranking": True},
            {**sa.as_dict(cand), "starts_clock": True},
            {**sa.as_dict(cand), "releases_hold": True},
            {**sa.as_dict(cand), "status": "ACTIVE"},
            {
                "diagnoses_hazard": False,
                "starts_clock": True,
                "releases_hold": False,
                "changes_ranking": False,
            },
        )
        for payload in bad_payloads:
            with self.subTest(target="enforce_sensor_non_authority", payload=payload):
                with self.assertRaisesRegex(ValueError, sa.SENSOR_NON_AUTHORITY_ERROR):
                    sa.enforce_sensor_non_authority(payload)

    def test_handover_continuity_and_retained_reproduction_remain_non_authoritative(self) -> None:
        store = self._make_store(sql=True)
        sql_store = cast(SqlStore, store)
        baseline = _authority_fingerprint(store)
        base_audits = self._audit_count(store)
        consumer = _configure_consumer(sql_store)
        rows = _scenario_rows("sustained_high_humidity")

        receipt = _ingest_all(consumer, rows, "2024-01-29T00:00:00Z")
        self.assertEqual(receipt.accepted, len(rows))
        for flag in ("diagnoses_hazard", "starts_clock", "releases_hold", "changes_ranking"):
            self.assertIs(getattr(receipt, flag), False)

        retained = si.home_series(consumer, CID)
        continuity = si.handover_continuity(
            retained,
            handover="2024-01-15T00:00:00Z",
            window_minutes=360,
            temperature=TOLERANCE,
            humidity=TOLERANCE,
        )
        for flag in ("diagnoses_hazard", "starts_clock", "releases_hold", "changes_ranking"):
            self.assertIs(continuity[flag], False)

        unapproved = sas.reproduce_retained(consumer, CID, WINDOW, WINDOW.end)
        self.assertIsNone(unapproved["review_task"])
        self.assertEqual(unapproved["signal"]["priority_effect"], "NONE")
        self.assertIs(unapproved["signal"]["diagnoses_hazard"], False)

        reproduced = sas.reproduce_retained(consumer, CID, WINDOW, WINDOW.end, APPROVED_POLICY)
        self.assertIsNotNone(reproduced["review_task"])
        assert reproduced["review_task"] is not None
        sa.enforce_sensor_non_authority(reproduced["signal"])
        sa.enforce_sensor_non_authority(reproduced["review_task"])
        self.assertEqual(_authority_fingerprint(store), baseline)
        self.assertEqual(self._audit_count(store), base_audits)

    def test_end_to_end_adverse_faulty_weather_and_declined_series_preserve_workflows(
        self,
    ) -> None:
        store = self._make_store(sql=True)
        sql_store = cast(SqlStore, store)
        baseline = _authority_fingerprint(store)

        # 1. Adverse extreme humidity + schema-smuggled authority keys on observations
        consumer = _configure_consumer(sql_store)
        adverse = _scenario_rows("sustained_high_humidity")
        extreme = [{**row, "humidity_pct": "100.0"} for row in adverse[:48]] + adverse[48:]
        smuggled = {
            **adverse[0],
            "reading_id": "SMUGGLED-AUTH-1",
            "diagnoses_hazard": "true",
            "starts_clock": "true",
            "releases_hold": "true",
            "changes_ranking": "true",
        }
        ingested = _ingest_all(consumer, [*extreme, smuggled], "2024-01-29T00:00:00Z")
        self.assertEqual(ingested.accepted, len(extreme))
        self.assertEqual(sum(ingested.rejected.values()), 1)
        sig_adverse = sas.analyse_retained(consumer, CID, WINDOW, WINDOW.end, APPROVED_POLICY)
        self.assertEqual((sig_adverse.outcome, sig_adverse.priority_effect), (sa.REVIEW, "NONE"))
        self.assertIs(sig_adverse.diagnoses_hazard, False)
        self.assertEqual(_authority_fingerprint(store), baseline)

        # 2. Stale evaluation past max_staleness_hours
        sig_stale = sas.analyse_retained(
            consumer, CID, WINDOW, WINDOW.end + timedelta(days=5), APPROVED_POLICY
        )
        self.assertEqual((sig_stale.sufficiency, sig_stale.outcome), (sa.STALE, sa.INSUFFICIENT))
        self.assertEqual(_authority_fingerprint(store), baseline)

        # 3. Declined resident consent
        _configure_consumer(sql_store, consent="declined")
        sig_declined = sas.analyse_retained(consumer, CID, WINDOW, WINDOW.end, APPROVED_POLICY)
        self.assertEqual(
            (sig_declined.sufficiency, sig_declined.outcome), (sa.DECLINED, sa.INSUFFICIENT)
        )
        self.assertIsNone(sa.review_task_candidate(sig_declined, APPROVED_POLICY))
        self.assertEqual(_authority_fingerprint(store), baseline)

        # 4. Live outdoor weather-sim readings in a later window (not indoor measurement)
        live_start = datetime(2024, 3, 1, 0, 0, tzinfo=UTC)
        live_end = live_start + timedelta(days=ss.DAYS)
        live_consumer = _configure_consumer(
            sql_store,
            consent="granted",
            window_start="2024-03-01T00:00:00Z",
            window_end="2024-03-29T00:00:00Z",
        )
        weather_row = live_readings.Reading(
            CID, "SENS-SYN-1", "SYN-SENS-SYN-1", live_start, 9.5, 92.0, 290.0, 184
        ).row()
        weather_receipt = si.ingest_window(
            live_consumer, [cast(Observation, dict(weather_row))], "2024-03-01T00:05:00Z"
        )
        self.assertEqual(weather_receipt.accepted, 1)
        sig_weather = sas.analyse_retained(
            live_consumer, CID, ss.Window(live_start, live_end), live_end, APPROVED_POLICY
        )
        self.assertEqual(sig_weather.outcome, sa.INSUFFICIENT)
        self.assertIn(sas.WEATHER_NOT_INDOOR, sig_weather.reasons)
        self.assertEqual(_authority_fingerprint(store), baseline)

    def test_absence_of_sensor_alert_never_clears_open_hazard_clock_or_hold(self) -> None:
        for sql in (False, True):
            with self.subTest(sql=sql):
                store = self._make_store(sql=sql)
                idx = store.raise_hazard(
                    RC,
                    CID,
                    "Damp and mould",
                    "Emergency",
                    note="Resident reported black mould behind wardrobe",
                    metadata={
                        "source": "Resident call RES-CALL-2026-109",
                        "aware_at": AWARE_AT,
                    },
                )
                store.refer_hazard(
                    RC,
                    CID,
                    idx,
                    BEA["email"],
                    "REP-EXT-109",
                    metadata={"evidence": "External safety desk dispatch REF-109"},
                )
                store.receive_hazard(BEA, CID, idx, "Safety desk receipt ACK-109")
                store.accept_hazard(BEA, CID, idx, "Safety desk accepted case ACC-109")
                store.observe_hazard_times(
                    BEA,
                    CID,
                    idx,
                    {
                        "evidence": "External repairs ledger TIM-109",
                        "response_due_at": RESPONSE_DUE_AT,
                        "responded_at": RESPONDED_AT,
                        "resident_update_due_at": UPDATE_DUE_AT,
                    },
                )
                if sql:
                    consumer = _configure_consumer(cast(SqlStore, store))
                    _ingest_all(consumer, _scenario_rows("normal"), "2024-01-29T00:00:00Z")
                    normal_sig = sas.analyse_retained(
                        consumer, CID, WINDOW, WINDOW.end, APPROVED_POLICY
                    )
                else:
                    normal_sig = _sample_signal("normal")
                self.assertEqual(normal_sig.outcome, sa.NO_SIGNAL)

                active_state = _authority_fingerprint(store)
                haz = store.cases[CID]["hazards"][idx]
                self.assertFalse(haz["released"])
                self.assertEqual(haz["hold"]["status"], "Active")
                self.assertEqual(haz["aware_at"], AWARE_AT)
                self.assertEqual(haz["response_due_at"], RESPONSE_DUE_AT)
                safety_gate = next(
                    g for g in active_state["booking_gates"] if g["gate"] == "safety"
                )
                self.assertEqual(safety_gate["outcome"], gates.FAIL)
                self.assertIn(("safety_open", "Safety issue open"), active_state["reasons"][CID])

                audits_before = self._audit_count(store)
                ver_before = self._store_version(store)
                for citation in ("NO_EXERCISE_SIGNAL", "NO_SIGNAL", "SENS-SYN-1", "sensor:ZF-1:r1"):
                    with self.assertRaises(ValueError) as ctx:
                        store.record_repair(BEA, CID, idx, f"Cleared because {citation}")
                    self.assertEqual(str(ctx.exception), _SENSOR_REFUSAL)
                    with self.assertRaises(ValueError) as ctx2:
                        store.release_hazard(
                            BO, CID, idx, note="Normal humidity", evidence=f"Telemetry {citation}"
                        )
                    self.assertEqual(str(ctx2.exception), _SENSOR_REFUSAL)
                self.assertEqual(_authority_fingerprint(store), active_state)
                self.assertEqual(self._audit_count(store), audits_before)
                self.assertEqual(self._store_version(store), ver_before)

    def test_review_drafts_remain_non_authoritative_and_tampered_drafts_fail_closed(self) -> None:
        for sql in (False, True):
            with self.subTest(sql=sql), mock.patch.dict(os.environ, {srd.FLAG: "1"}):
                store = self._make_store(sql=sql)
                draft_store = cast(srd.DraftStore, store)
                if sql:
                    consumer = _configure_consumer(cast(SqlStore, store))
                    _ingest_all(
                        consumer, _scenario_rows("sustained_high_humidity"), "2024-01-29T00:00:00Z"
                    )
                    default_attempt = srd.draft_from_retained(
                        draft_store, QI, CID, WINDOW, WINDOW.end
                    )
                    self.assertFalse(default_attempt["created"])

                baseline = _authority_fingerprint(store)
                sig = _sample_signal()
                created = srd._record_draft_synthetic(draft_store, QI, CID, sig, APPROVED_POLICY)
                self.assertTrue(created["created"])
                self.assertEqual(_authority_fingerprint(store), baseline)

                projected = srd.read_drafts(draft_store, QI, CID)
                if sql:
                    self.assertEqual((projected["state"], len(projected["drafts"])), ("ok", 1))
                    draft_view = projected["drafts"][0]
                    self.assertEqual(draft_view["state"], srd.STATE)
                    self.assertNotIn("activation", draft_view)
                    self.assertIsNone(store.cases[CID][srd.CASE_KEY][0]["activation"])
                    self.assertIs(draft_view["manual_review_only"], True)
                    self.assertIs(draft_view["approval_verified"], False)
                else:
                    self.assertEqual(
                        (projected["state"], projected["drafts"]), ("consent-withheld", [])
                    )

                tamperings: tuple[Callable[[dict[str, Any]], None], ...] = (
                    lambda rec: rec.__setitem__("state", "APPROVED"),
                    lambda rec: rec.__setitem__("manual_review_only", False),
                    lambda rec: rec.__setitem__("approval_verified", True),
                    lambda rec: rec.__setitem__("activation", "ACTIVE"),
                    lambda rec: rec["candidate"].__setitem__("changes_ranking", True),
                    lambda rec: rec["candidate"].__setitem__("starts_clock", True),
                    lambda rec: rec["candidate"].__setitem__("releases_hold", True),
                    lambda rec: rec["candidate"].__setitem__("diagnoses_hazard", True),
                    lambda rec: rec["candidate"].__setitem__("resident_report_unaffected", False),
                    lambda rec: rec["candidate"].__setitem__("status", "ACTIVE"),
                )
                original = copy.deepcopy(store.cases[CID][srd.CASE_KEY][0])
                expected_mismatch = {
                    "state": "INTEGRITY_MISMATCH",
                    "task_key": original["task_key"],
                }
                for mutate in tamperings:
                    with store.lock:
                        target_rec = copy.deepcopy(original)
                        mutate(target_rec)
                        target_rec["draft_digest"] = srd._digest(target_rec)
                        store._case(CID)[srd.CASE_KEY][0] = target_rec
                        store.save()
                    again = srd._record_draft_synthetic(draft_store, QI, CID, sig, APPROVED_POLICY)
                    self.assertEqual(again["draft"], expected_mismatch)
                    if sql:
                        tampered_view = srd.read_drafts(draft_store, QI, CID)
                        self.assertEqual(tampered_view["drafts"], [expected_mismatch])

    def test_hazard_and_clock_workflows_refuse_sensor_citations_payloads_and_actors(self) -> None:
        sensor_tokens = (
            "SENS-SYN-1",
            "LIVE-SENS-SYN-1-20241001T0105Z",
            "SYN-SENS-PUB1",
            "SENS-110",
            "sensor:ZF-1:r1",
            "sensor_signal:ZF-1",
            "source:sensors",
            "iot-hub:msg-9",
            "SENSOR_REVIEW_DUE",
            "SENSOR-RH-PERSISTENCE-EXERCISE",
            "NO_EXERCISE_SIGNAL",
            "REVIEW_CANDIDATE",
            "sensor-analysis-exercise-v1",
            "sensor-review-draft-v1",
            "live-sim-reading-v1",
        )
        for token in sensor_tokens:
            self.assertTrue(_is_sensor_ref(token), token)
            with self.assertRaises(ValueError):
                _evidence_text(f"Ref {token}", "evidence")

        sig = _sample_signal()
        cand = sa.review_task_candidate(sig, APPROVED_POLICY)
        assert cand is not None
        receipt = si.WindowReceipt(1, 0, {})

        for sql in (False, True):
            with self.subTest(sql=sql):
                store = self._make_store(sql=sql)
                baseline = _authority_fingerprint(store)
                audits_before = self._audit_count(store)
                ver_before = self._store_version(store)
                sensor_actor = {**BEA, "sensor_id": "SENS-SYN-1", "source_type": "SENSOR"}

                with self.assertRaises(PermissionError):
                    store.raise_hazard(
                        sensor_actor,
                        CID,
                        "Damp and mould",
                        "Significant",
                        metadata={"source": "Surveyor visit SUR-1", "aware_at": AWARE_AT},
                    )
                for bad_meta in (
                    {"source": "SENS-SYN-1", "aware_at": AWARE_AT},
                    {"source": "Surveyor SUR-1", "aware_at": AWARE_AT, "sensor_signal": sig},
                    {"source": "Surveyor SUR-1", "aware_at": AWARE_AT, "sensor_candidate": cand},
                    {"source": "Surveyor SUR-1", "aware_at": AWARE_AT, "receipt": receipt},
                    {
                        "source": "Surveyor SUR-1",
                        "aware_at": AWARE_AT,
                        "nested": [{"sensor_id": "SENS-SYN-1"}],
                    },
                ):
                    with self.assertRaises(ValueError):
                        store.raise_hazard(
                            RC, CID, "Damp and mould", "Significant", metadata=bad_meta
                        )
                with self.assertRaises(ValueError):
                    store.raise_hazard(
                        RC,
                        CID,
                        "Damp and mould",
                        "Significant",
                        note="Triggered by SENSOR_REVIEW_DUE",
                        metadata={"source": "Surveyor SUR-1", "aware_at": AWARE_AT},
                    )

                self.assertEqual(_authority_fingerprint(store), baseline)
                self.assertEqual(self._audit_count(store), audits_before)
                self.assertEqual(self._store_version(store), ver_before)

                # Legitimate human surveyor observation mentioning physical room hardware succeeds
                idx = store.raise_hazard(
                    RC,
                    CID,
                    "Damp and mould",
                    "Significant",
                    note=(
                        "Surveyor inspected bedroom wall near sensor casing; "
                        "damp confirmed visually"
                    ),
                    metadata={"source": "Surveyor inspection SUR-2026-88", "aware_at": AWARE_AT},
                )
                with self.assertRaises(ValueError):
                    store.refer_hazard(
                        RC,
                        CID,
                        idx,
                        BEA["email"],
                        "SENS-SYN-1",
                        metadata={"evidence": "Safety email DISPATCH-1"},
                    )
                store.refer_hazard(
                    RC,
                    CID,
                    idx,
                    BEA["email"],
                    "EXT-JOB-88",
                    metadata={"evidence": "Safety email DISPATCH-1"},
                )
                with self.assertRaises(ValueError):
                    store.receive_hazard(BEA, CID, idx, {"sensor_reading": "r1"})
                store.receive_hazard(BEA, CID, idx, "Safety receipt ACK-88")
                with self.assertRaises(ValueError):
                    store.accept_hazard(BEA, CID, idx, "sensor:ZF-1:r1")
                store.accept_hazard(BEA, CID, idx, "Safety acceptance ACC-88")
                with self.assertRaises(ValueError):
                    store.observe_hazard_times(
                        BEA,
                        CID,
                        idx,
                        {
                            "evidence": "External clock CLK-88",
                            "response_due_at": RESPONSE_DUE_AT,
                            "source_type": "IOT_HUB",
                        },
                    )
                self.assertIsNone(store.cases[CID]["hazards"][idx].get("response_due_at"))

    def test_safety_release_refuses_tampered_stored_sensor_evidence_and_preserves_gate(
        self,
    ) -> None:
        for sql in (False, True):
            with self.subTest(sql=sql):
                store = self._make_store(sql=sql)
                idx = store.raise_hazard(
                    RC,
                    CID,
                    "Damp and mould",
                    "Significant",
                    note="Visual damp inspection",
                    metadata={"source": "Surveyor report SUR-501", "aware_at": AWARE_AT},
                )
                store.refer_hazard(
                    RC,
                    CID,
                    idx,
                    BEA["email"],
                    "JOB-501",
                    metadata={"evidence": "Dispatch DIS-501"},
                )
                store.receive_hazard(BEA, CID, idx, "Receipt REC-501")
                store.accept_hazard(BEA, CID, idx, "Accepted ACC-501")
                store.record_repair(BEA, CID, idx, "Signed repair completion cert CERT-501")

                hold_record = store.cases[CID]["hazards"][idx]["hold"]
                sensor_gate = gates.safety_release_gate(
                    hold_record,
                    {"role": "Telemetry Consumer", "email": "iot@example.test"},
                    [RC["email"], BEA["email"]],
                    on=AS_OF,
                )
                self.assertEqual(sensor_gate.outcome, gates.FAIL)
                liaison_gate = gates.safety_release_gate(
                    hold_record, BO, [RC["email"], BEA["email"]], on=AS_OF
                )
                self.assertEqual(liaison_gate.outcome, gates.PASS)

                guarded_fields = (
                    "source",
                    "note",
                    "job",
                    "sent_evidence",
                    "receipt_evidence",
                    "acceptance_evidence",
                    "repair_evidence",
                )
                clean_hazard = copy.deepcopy(store.cases[CID]["hazards"][idx])
                for field_name in guarded_fields:
                    with store.lock:
                        tampered = copy.deepcopy(clean_hazard)
                        tampered[field_name] = "sensor:ZF-1:r1"
                        store._case(CID)["hazards"][idx] = tampered
                        store.save()
                    with self.assertRaises(ValueError) as ctx:
                        store.release_hazard(
                            BO,
                            CID,
                            idx,
                            note="Independent safety review complete",
                            evidence="Post-works signoff POST-501",
                        )
                    self.assertEqual(str(ctx.exception), _SENSOR_REFUSAL)
                    self.assertFalse(store.cases[CID]["hazards"][idx]["released"])
                    self.assertEqual(store.cases[CID]["hazards"][idx]["hold"]["status"], "Active")

    def test_legal_hold_refuses_sensor_references_actors_and_tampered_release(self) -> None:
        sig = _sample_signal()
        for sql in (False, True):
            with self.subTest(sql=sql):
                store = self._make_store(sql=sql)
                audits_before = self._audit_count(store)
                sensor_mgr = {**PM, "sensor_id": "SENS-SYN-1"}

                with self.assertRaises(PermissionError):
                    store.place_legal_hold(sensor_mgr, CID, "LGL-2026-10")
                for bad_ref in ("SENS-SYN-1", "SENSOR_REVIEW_DUE", "sensor:ZF-1:r1", sig):
                    with self.assertRaises(ValueError):
                        store.place_legal_hold(PM, CID, bad_ref)
                self.assertNotIn("legal_hold", store.cases[CID])
                self.assertEqual(self._audit_count(store), audits_before)

                placed = store.place_legal_hold(PM, CID, "LGL-2026-10")
                self.assertTrue(placed["active"])
                with self.assertRaises(PermissionError):
                    store.release_legal_hold(sensor_mgr, CID)
                with self.assertRaises(PermissionError):
                    store.release_legal_hold(QI, CID)

                with store.lock:
                    store._case(CID)["legal_hold"]["reference"] = "SENS-SYN-1"
                    store.save()
                with self.assertRaises(ValueError) as ctx:
                    store.release_legal_hold(PM, CID)
                self.assertEqual(str(ctx.exception), _SENSOR_REFUSAL)
                self.assertTrue(store.cases[CID]["legal_hold"]["active"])

    def test_ranking_is_invariant_to_injected_case_sensor_fields_and_rejects_sensor_rules(
        self,
    ) -> None:
        for sql in (False, True):
            with self.subTest(sql=sql):
                store = self._make_store(sql=sql)
                clean_cases = [copy.deepcopy(store.cases[cid]) for cid in sorted(store.cases)]
                base_rank = _rank(clean_cases, _CURRENT_POLICY, AS_OF)
                base_snap = ranking.snapshot(clean_cases, _CURRENT_POLICY, AS_OF)
                base_keys = [_sql_key(c, _CURRENT_POLICY) for c in clean_cases]
                base_reasons = [_reasons(c) for c in clean_cases]

                decorated = copy.deepcopy(clean_cases)
                decorated[0].update(
                    sensor_readings=[{"humidity_pct": "99.9", "sensor_id": "SENS-SYN-1"}],
                    sensor_signal=sa.as_dict(_sample_signal()),
                    sensor_review_drafts=[{"state": srd.STATE, "task_type": sa.TASK_TYPE}],
                    telemetry_consent="declined",
                    sensor_priority="Emergency",
                )
                self.assertEqual(_rank(decorated, _CURRENT_POLICY, AS_OF), base_rank)
                self.assertEqual(ranking.snapshot(decorated, _CURRENT_POLICY, AS_OF), base_snap)
                self.assertEqual([_sql_key(c, _CURRENT_POLICY) for c in decorated], base_keys)
                self.assertEqual([_reasons(c) for c in decorated], base_reasons)

                for bad_rule in ("sensor_signal", "sensor_humidity", "telemetry_alert"):
                    bad_policy = copy.deepcopy(_CURRENT_POLICY)
                    bad_policy["rules"] = [
                        {"code": bad_rule, "description": "Forbidden sensor rule"},
                        *bad_policy["rules"],
                    ]
                    with self.assertRaisesRegex(ValueError, f"Unknown ranking rule: {bad_rule}"):
                        _rank(clean_cases, bad_policy, AS_OF)
                    with self.assertRaisesRegex(ValueError, f"Unknown ranking rule: {bad_rule}"):
                        ranking.snapshot(clean_cases, bad_policy, AS_OF)
                    with self.assertRaisesRegex(ValueError, f"Unknown ranking rule: {bad_rule}"):
                        _sql_key(clean_cases[0], bad_policy)


if __name__ == "__main__":
    unittest.main()
