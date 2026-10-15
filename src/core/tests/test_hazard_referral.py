"""Synthetic hazard-service evidence and separate retrofit-hold accountability."""

import copy
import json
import tempfile
import unittest
from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import Any
from unittest.mock import patch

from building_fixture import fixture, hold
from dataset import DATA
from zava_forward.core import ai_tasks, projection
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import GateError, Store

SOURCE = dict(source="SYN-SOURCE-CANARY", aware_at="2026-01-01T10:00:00+01:00")
SENT = dict(evidence="SYN-SENT-CANARY")


class JsonHazardReferral(unittest.TestCase):
    sql = False

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        data = copy.deepcopy(DATA)
        data["staff"].extend(
            [
                dict(
                    code="BS-1",
                    name="Bea Safe",
                    email="bea@example.test",
                    role="Building Safety Liaison",
                ),
                dict(
                    code="BS-2",
                    name="Bo Safe",
                    email="bo@example.test",
                    role="Building Safety Liaison",
                ),
                dict(
                    code="RC-1",
                    name="Rex Coordinator",
                    email="rex@example.test",
                    role="Retrofit Coordinator",
                ),
                dict(
                    code="CON-1",
                    name="Kim Builder",
                    email="kim@example.test",
                    role="Contractor",
                    contractor="Test Ltd",
                ),
            ]
        )
        self.sam, self.pam, self.bea, self.bo, self.rex, self.kim = data["staff"]
        self.path.write_text(json.dumps(data))
        self.store = self.open_store()

    def open_store(self) -> Store:
        if self.sql:
            store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
            self.addCleanup(store.db.close)
            return store
        return Store(str(self.path))

    def raise_report(self, cid: str = "ZF-3") -> int:
        idx = self.store.raise_hazard(
            self.sam, cid, "Damp and mould", "Emergency", "SYN-NOTE-CANARY", SOURCE
        )
        assert isinstance(idx, int)
        return idx

    def refer(self, idx: int = 0, cid: str = "ZF-3") -> None:
        self.store.refer_hazard(self.sam, cid, idx, self.bea["email"], "SYN-JOB-CANARY", SENT)

    def accept(self, idx: int = 0, cid: str = "ZF-3") -> None:
        self.store.receive_hazard(self.bea, cid, idx, "SYN-RECEIPT-CANARY")
        self.store.accept_hazard(self.bea, cid, idx, "SYN-ACCEPT-CANARY")

    def unchanged_failure(self, operation: Callable[[], object]) -> None:
        before = self.store.detail("ZF-3")
        audit = list(self.store.audit_entries())
        procurement = copy.deepcopy(self.store.data.get("procurement"))
        with self.assertRaises((ValueError, PermissionError, GateError)):
            operation()
        self.assertEqual(self.store.detail("ZF-3"), before)
        self.assertEqual(list(self.store.audit_entries()), audit)
        self.assertEqual(self.store.data.get("procurement"), procurement)

    def test_distinct_events_times_hold_and_restart_without_case_transfer(self) -> None:
        before = self.store.detail("ZF-3")
        self.raise_report()
        self.refer()
        h = self.store.detail("ZF-3")["hazards"][0]
        self.assertEqual(h["state"], "Sent")
        self.assertEqual(h["follow_up"]["code"], self.sam["code"])
        self.assertIsNone(h["received_at"])
        self.assertIsNone(h["accepted_at"])
        self.assertEqual(h["aware_at"], "2026-01-01T09:00+00:00")
        self.assertEqual(h["hold"]["case_id"], "ZF-3")
        self.assertEqual(h["hold"]["accountable_role"], self.bea["role"])
        sent_event = copy.deepcopy(h["history"][-1])
        self.accept()
        self.store.observe_hazard_times(
            self.bea,
            "ZF-3",
            0,
            dict(
                evidence="SYN-TIME-CANARY",
                response_due_at="2026-01-02T12:00:00Z",
                responded_at="2026-01-02T11:00:00Z",
                resident_update_due_at="2026-01-03T12:00:00Z",
                resident_updated_at="2026-01-03T11:00:00Z",
            ),
        )
        self.store.record_repair(self.bea, "ZF-3", 0, "SYN-REPAIR-CANARY")
        self.unchanged_failure(
            lambda: self.store.release_hazard(self.bea, "ZF-3", 0, "Reason", "SYN-CLEAR")
        )
        self.store.release_hazard(self.bo, "ZF-3", 0, "SYN-REASON-CANARY", "SYN-CLEAR-CANARY")
        detail = self.open_store().detail("ZF-3")
        h = detail["hazards"][0]
        self.assertEqual(h["state"], "Retrofit hold released")
        self.assertEqual(h["follow_up"]["code"], self.bea["code"])
        self.assertEqual(h["hold"]["decision"]["actor"]["role"], self.bo["role"])
        self.assertEqual(h["history"][1], sent_event)
        self.assertEqual(
            [e["action"] for e in h["history"]],
            [
                "safety_raised",
                "safety_referred",
                "safety_received",
                "safety_accepted",
                "safety_times_observed",
                "safety_repaired",
                "safety_released",
            ],
        )
        self.assertEqual([e["version"] for e in h["history"]], list(range(1, 8)))
        for field in ("owner_code", "owner", "decision", "stage", "closed"):
            self.assertEqual(detail[field], before[field])
        self.assertNotIn("service_status", h)
        self.assertTrue(self.store.verify_audit())
        self.store.advance(self.sam, "ZF-3")
        self.assertEqual(self.store.detail("ZF-3")["stage"], "Install booked")

    def test_invalid_provenance_actor_index_timing_and_replays_are_atomic(self) -> None:
        for metadata in (
            {},
            dict(SOURCE, aware_at="2026-01-01"),
            dict(SOURCE, aware_at="2099-01-01T00:00:00Z"),
            dict(SOURCE, source=123),
        ):
            self.unchanged_failure(
                partial(
                    self.store.raise_hazard,
                    self.sam,
                    "ZF-3",
                    "Electrical",
                    "Routine",
                    metadata=metadata,
                )
            )
        self.unchanged_failure(
            lambda: self.store.raise_hazard(
                self.kim, "ZF-3", "Electrical", "Routine", metadata=SOURCE
            )
        )
        self.raise_report()
        for idx in (-1, True, 0.5, "-1", "0.0", None, 999):
            self.unchanged_failure(
                partial(
                    self.store.refer_hazard,
                    self.sam,
                    "ZF-3",
                    idx,
                    self.bea["email"],
                    "SYN-JOB",
                    SENT,
                )
            )
        self.unchanged_failure(
            lambda: self.store.refer_hazard(self.sam, "ZF-3", 0, self.bea["email"], "SYN-JOB")
        )
        self.refer()
        for operation in (
            lambda: self.refer(),
            lambda: self.store.receive_hazard(self.bo, "ZF-3", 0, "SYN"),
            lambda: self.store.accept_hazard(self.bea, "ZF-3", 0, "SYN"),
            lambda: self.store.record_repair(self.bea, "ZF-3", 0, "SYN"),
            lambda: self.store.receive_hazard(self.bea, "ZF-3", 0, ""),
        ):
            self.unchanged_failure(operation)
        self.accept()
        for operation in (
            lambda: self.store.receive_hazard(self.bea, "ZF-3", 0, "Replay"),
            lambda: self.store.accept_hazard(self.bea, "ZF-3", 0, "Replay"),
            lambda: self.store.observe_hazard_times(self.bea, "ZF-3", 0, dict(evidence="SYN")),
            lambda: self.store.observe_hazard_times(
                self.bea, "ZF-3", 0, dict(evidence="SYN", responded_at="2099-01-01T00:00Z")
            ),
            lambda: self.store.observe_hazard_times(
                self.bea, "ZF-3", 0, dict(evidence="SYN", responded_at="2025-01-01T00:00Z")
            ),
        ):
            self.unchanged_failure(operation)
        self.store.observe_hazard_times(
            self.bea, "ZF-3", 0, dict(evidence="SYN", response_due_at="2026-01-02T00:00Z")
        )
        self.unchanged_failure(
            lambda: self.store.observe_hazard_times(
                self.bea, "ZF-3", 0, dict(evidence="SYN", response_due_at="2026-01-03T00:00Z")
            )
        )

    def test_closed_record_and_ai_outage_do_not_block_intake_or_reopen_retrofit(self) -> None:
        with self.store.lock:
            self.store._case("ZF-3").update(closed=True, stage="Completed")
            self.store.save()
        before = self.store.detail("ZF-3")
        with patch.object(self.store.ai, "run", side_effect=RuntimeError("Synthetic AI outage")):
            self.raise_report()
            self.refer()
        detail = self.open_store().detail("ZF-3")
        for field in ("closed", "stage", "owner_code", "decision"):
            self.assertEqual(detail[field], before[field])
        self.assertEqual(detail["hazards"][0]["state"], "Sent")
        self.assertNotIn("same day", json.dumps(list(self.store.audit_entries())))

    def test_external_updates_remain_recordable_after_retrofit_restart(self) -> None:
        self.raise_report()
        self.refer()
        self.accept()
        self.store.record_repair(self.bea, "ZF-3", 0, "SYN-REPAIR")
        self.store.release_hazard(self.bo, "ZF-3", 0, "Reason", "SYN-CLEAR")
        self.store.observe_hazard_times(
            self.bea,
            "ZF-3",
            0,
            dict(evidence="SYN-LATER-UPDATE", resident_updated_at="2026-01-04T12:00:00Z"),
        )
        h = self.open_store().detail("ZF-3")["hazards"][0]
        self.assertEqual(h["resident_updated_at"], "2026-01-04T12:00+00:00")
        self.assertTrue(h["released"])
        self.assertIsNone(h["response_due_at"])
        self.assertEqual(h["history"][-1]["action"], "safety_times_observed")

    def test_legacy_states_have_prospective_path_without_inventing_history(self) -> None:
        for state in ("raised", "referred", "repaired", "released"):
            with self.subTest(state=state):
                legacy = dict(
                    category="Damp",
                    priority="P1",
                    noticed="2025-01-01",
                    referred="2025-01-02" if state != "raised" else None,
                    repaired="2025-01-03" if state in ("repaired", "released") else None,
                    released=state == "released",
                    owner="Unverified display name",
                    job="OLD",
                )
                with self.store.lock:
                    self.store._case("ZF-3")["hazards"] = [copy.deepcopy(legacy)]
                    self.store.save()
                h = self.open_store().detail("ZF-3")["hazards"][0]
                self.assertIsNone(h["aware_at"])
                self.assertIsNone(h["received_at"])
                self.assertIsNone(h["accepted_at"])
                if state == "released":
                    self.unchanged_failure(lambda: self.refer())
                    self.assertTrue(h["released"])
                    continue
                self.unchanged_failure(
                    lambda: self.store.record_repair(self.bea, "ZF-3", 0, "SYN-REPAIR")
                )
                self.refer()
                self.accept()
                self.store.record_repair(self.bea, "ZF-3", 0, "SYN-REPAIR")
                self.store.release_hazard(self.bo, "ZF-3", 0, "Reason", "SYN-CLEAR")
                h = self.open_store().detail("ZF-3")["hazards"][0]
                if state in ("referred", "repaired"):
                    self.assertEqual(h["legacy_record"], legacy)
                self.assertIsNone(h.get("aware_at"))
                self.assertEqual(len(h["history"]), 5)

    def test_sensitive_evidence_is_withheld_and_never_added_to_model_sources(self) -> None:
        self.raise_report()
        self.refer()
        self.accept()
        self.store.record_repair(self.bea, "ZF-3", 0, "SYN-REPAIR-CANARY")
        self.store.release_hazard(self.bo, "ZF-3", 0, "SYN-REASON-CANARY", "SYN-CLEAR-CANARY")
        allowed = json.dumps(self.store.detail("ZF-3", self.sam))
        denied = json.dumps(self.store.detail("ZF-3", self.rex))
        contractor = json.dumps(self.store.detail("ZF-3", self.kim))
        labels = json.dumps(ai_tasks.source_labels(self.store.cases["ZF-3"]))
        for canary in (
            "SOURCE",
            "SENT",
            "RECEIPT",
            "ACCEPT",
            "REPAIR",
            "REASON",
            "CLEAR",
            "NOTE",
            "JOB",
        ):
            text = f"SYN-{canary}-CANARY"
            self.assertIn(text, allowed)
            self.assertNotIn(text, denied)
            self.assertNotIn(text, contractor)
            self.assertNotIn(text, labels)
        self.assertNotIn("hazards", contractor)
        self.assertIn(projection.NOTE_HELD, denied)

    def test_home_hold_blocks_all_controlled_progression_but_not_sibling_or_referral(self) -> None:
        data: dict[str, Any] = fixture()
        with self.store.lock:
            self.store._case("ZF-3")["quality"] = data["cases"][1]["quality"]
            self.store.data["procurement"] = data["procurement"]
            self.store.save()
        wid = self.store.issue_work_order(self.pam, "PKG-SHARED", "ZF-3")
        self.raise_report()
        for operation in (
            lambda: self.store.advance(self.sam, "ZF-3"),
            lambda: self.store.issue_work_order(self.pam, "PKG-OTHER", "ZF-3"),
            lambda: self.store.reissue_work_order(self.pam, wid, "Scope", "Reason"),
            lambda: self.store.record_wo_appointment(self.pam, wid, "Booked", "2099-01-01"),
            lambda: self.store.complete_work_order(self.pam, wid),
            lambda: self.store.correct_work_order(self.pam, wid, "Correction"),
            lambda: self.store.accept_quality(self.pam, "ZF-3", 0),
            lambda: self.store.hand_over_quality(self.pam, "ZF-3", 0, "Guarantees", True),
            lambda: self.store.technical_action(
                self.pam, "ZF-3", dict(action="signoff_give", type="coordination")
            ),
        ):
            self.unchanged_failure(operation)
        self.store.issue_work_order(self.pam, "PKG-SHARED", "ZF-2")
        self.refer()
        self.accept()
        self.store.record_repair(self.bea, "ZF-3", 0, "SYN-REPAIR")
        self.store.release_hazard(self.bo, "ZF-3", 0, "Reason", "SYN-CLEAR")
        with self.store.lock:
            self.store._case("ZF-3")["decision"]["status"] = "Withdrawn"
            self.store.save()
        self.unchanged_failure(lambda: self.store.advance(self.sam, "ZF-3"))
        self.assertIn("resident", " ".join(self.store.detail("ZF-3")["gate"]).lower())
        with self.store.lock:
            self.store._case("ZF-3")["building_id"] = "SYN-B1"
            data["buildings"][0]["holds"] = [dict(hold(), case_ids=["ZF-3"])]
            self.store.data["buildings"] = data["buildings"]
            self.store.save()
        self.unchanged_failure(lambda: self.store.issue_work_order(self.pam, "PKG-SHARED", "ZF-3"))


class SqlHazardReferral(JsonHazardReferral):
    sql = True
