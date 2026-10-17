"""Synthetic hazard-service evidence and separate retrofit-hold accountability."""

import copy
import json
import tempfile
import unittest
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from functools import partial
from pathlib import Path
from threading import Event
from typing import Any
from unittest.mock import patch

from building_fixture import fixture, hold
from dataset import DATA, RESIDENT_BINDINGS, supplied_contract_fixture, supplied_resident_fixture
from zava_forward.core import ai_tasks, projection
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, GateError, Store

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

    def register(self, actor: dict[str, Any]) -> None:
        if self.sql:
            assert isinstance(self.store, SqlStore)
            with self.store.dblock:
                self.store.db.execute("DELETE FROM staff WHERE email=?", (actor["email"].lower(),))
                self.store.db.execute(
                    "INSERT INTO staff (email, body) VALUES (?, ?)",
                    (actor["email"].lower(), json.dumps(actor)),
                )
        else:
            self.store.staff[actor["email"].lower()] = copy.deepcopy(actor)

    def ready_for_release(self) -> None:
        self.raise_report()
        self.refer()
        self.accept()
        self.store.record_repair(self.bea, "ZF-3", 0, "SYN-REPAIR")

    def test_current_registered_actors_and_destinations_are_required(self) -> None:
        for actor in (
            dict(self.sam, email="absent@example.test"),
            dict(self.sam, code="FORGED"),
            dict(self.sam, oid="SYN-CHANGED-OID"),
        ):
            with self.subTest(actor=actor):
                self.unchanged_failure(
                    partial(
                        self.store.raise_hazard,
                        actor,
                        "ZF-3",
                        "Electrical",
                        "Routine",
                        metadata=SOURCE,
                    )
                )
        self.raise_report()
        if self.sql:
            assert isinstance(self.store, SqlStore)
            self.store.db.execute("DELETE FROM staff WHERE email=?", (self.bea["email"],))
        else:
            self.store.staff.pop(self.bea["email"])
        self.unchanged_failure(self.refer)
        self.register(self.bea)
        for role in ("Contractor", "Resident Liaison Officer"):
            with self.subTest(destination_role=role):
                self.register(dict(self.bea, role=role))
                self.unchanged_failure(self.refer)
        self.register(self.bea)
        self.refer()
        self.store.receive_hazard(self.bea, "ZF-3", 0, "SYN-RECEIPT")
        self.store.accept_hazard(self.bea, "ZF-3", 0, "SYN-ACCEPT")

    def test_stale_actor_is_refused_for_every_hazard_event(self) -> None:
        steps: tuple[tuple[dict[str, Any], Callable[[], object]], ...] = (
            (self.sam, self.raise_report),
            (self.sam, self.refer),
            (self.bea, lambda: self.store.receive_hazard(self.bea, "ZF-3", 0, "SYN-RECEIPT")),
            (self.bea, lambda: self.store.accept_hazard(self.bea, "ZF-3", 0, "SYN-ACCEPT")),
            (
                self.bea,
                lambda: self.store.observe_hazard_times(
                    self.bea,
                    "ZF-3",
                    0,
                    dict(evidence="SYN-TIMES", response_due_at="2026-01-02T00:00:00Z"),
                ),
            ),
            (self.bea, lambda: self.store.record_repair(self.bea, "ZF-3", 0, "SYN-REPAIR")),
            (
                self.bo,
                lambda: self.store.release_hazard(self.bo, "ZF-3", 0, "SYN-REASON", "SYN-DECISION"),
            ),
        )
        for actor, operation in steps:
            with self.subTest(actor=actor["code"], operation=operation):
                self.register(dict(actor, oid="SYN-REVOKED-SESSION"))
                self.unchanged_failure(operation)
                self.register(actor)
                operation()

    def test_receiver_binding_rejects_recycled_code(self) -> None:
        self.raise_report()
        self.refer()
        replacement = dict(self.bea, email="replacement@example.test", oid="SYN-REPLACEMENT")
        self.register(replacement)
        self.unchanged_failure(
            lambda: self.store.receive_hazard(replacement, "ZF-3", 0, "SYN-RECEIPT")
        )
        self.accept()

    def test_release_independence_uses_recorded_email_code_and_oid(self) -> None:
        self.register(dict(self.bea, oid="SYN-REPAIRER"))
        self.bea = dict(self.bea, oid="SYN-REPAIRER")
        self.store.staff[self.bea["email"]] = copy.deepcopy(self.bea)
        self.ready_for_release()
        aliases = (
            dict(self.bea, email=self.bea["email"].upper()),
            dict(self.bea, email="renamed@example.test", oid="SYN-DIFFERENT"),
            dict(self.bo, oid="SYN-REPAIRER"),
        )
        for actor in aliases:
            with self.subTest(actor=actor):
                self.register(actor)
                self.unchanged_failure(
                    partial(
                        self.store.release_hazard, actor, "ZF-3", 0, "SYN-REASON", "SYN-DECISION"
                    )
                )
        self.register(self.bo)
        self.store.release_hazard(self.bo, "ZF-3", 0, "SYN-REASON", "SYN-DECISION")
        h = self.open_store().detail("ZF-3")["hazards"][0]
        self.assertEqual(h["hold"]["case_id"], "ZF-3")
        self.assertEqual(h["hold"]["decision"]["actor"]["code"], self.bo["code"])

    def test_failed_save_has_no_success_audit_or_ghost_hazard(self) -> None:
        before = self.store.detail("ZF-3")
        audit = list(self.store.audit_entries())
        original = OSError("Synthetic precommit failure")
        targets: list[tuple[Any, str]] = [(self.store, "save")]
        if not self.sql:
            import os

            targets.append((os, "replace"))
        for owner, target in targets:
            with self.subTest(target=target):
                with patch.object(owner, target, side_effect=original):
                    with self.assertRaises(OSError) as caught:
                        self.raise_report()
                self.assertIs(caught.exception, original)
                self.assertEqual(self.store.detail("ZF-3"), before)
                self.assertEqual(self.open_store().detail("ZF-3"), before)
                self.assertEqual(list(self.store.audit_entries()), audit)
        self.assertIsNone(getattr(getattr(self.store, "local", None), "hazard_decision", None))
        self.store.log_call(self.sam, "ZF-2", "Contacted", "SYN-AFTER-FAILURE")
        self.assertEqual(list(self.store.audit_entries())[-1]["action"], "log_contact")
        self.assertTrue(self.store.verify_audit())

    def test_json_postsave_audit_failure_reports_persisted_uncertainty(self) -> None:
        if self.sql:
            self.skipTest("JSON-only separate-file audit ordering")
        original = OSError("Synthetic audit failure after JSON save")
        with (
            patch.object(self.store, "audit", side_effect=original),
            self.assertLogs("zava_forward.core.hazard", level="ERROR"),
            self.assertRaises(OSError) as caught,
        ):
            self.raise_report()
        self.assertIs(caught.exception, original)
        self.assertIn("audit may be incomplete", " ".join(original.__notes__))
        self.assertEqual(len(self.open_store().detail("ZF-3")["hazards"]), 1)
        self.assertEqual(
            self.store.detail("ZF-3")["hazards"], self.open_store().detail("ZF-3")["hazards"]
        )
        self.assertEqual(list(self.store.audit_entries()), [])

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
        pid = self.store.create_package(
            self.pam, "SYN", "2026-01-01", "2099-12-31", "Loft", "SYN", "SYN-1"
        )
        details = supplied_contract_fixture(self.store, pid, self.pam)
        self.store.set_capacity(self.pam, pid, "Test Ltd", 1, 1, "SYN-CAPACITY", details)
        wid = self.store.issue_work_order(
            self.pam, pid, "ZF-3", resident_bindings=RESIDENT_BINDINGS
        )
        self.store.record_wo_appointment(self.pam, wid, "Booked", "2099-01-01")
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
        for package in data["procurement"]["packages"]:
            details = supplied_contract_fixture(self.store, package["id"], self.pam)
            self.store.set_capacity(
                self.pam, package["id"], "Test Ltd", 5, 5, "SYN-CAPACITY", details
            )
        wid = self.store.issue_work_order(
            self.pam, "PKG-SHARED", "ZF-3", resident_bindings=RESIDENT_BINDINGS
        )
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
        with self.store.lock:
            supplied_resident_fixture(self.store._case("ZF-2"))
            self.store.save()
        self.store.issue_work_order(
            self.pam, "PKG-SHARED", "ZF-2", resident_bindings=RESIDENT_BINDINGS
        )
        self.refer()
        self.accept()
        self.store.record_repair(self.bea, "ZF-3", 0, "SYN-REPAIR")
        self.store.release_hazard(self.bo, "ZF-3", 0, "Reason", "SYN-CLEAR")
        with self.store.lock:
            self.store._case("ZF-3")["decision"]["status"] = "Withdrawn"
            self.store._case("ZF-3")["measure_decisions"]["Loft insulation"][-1]["status"] = (
                "Withdrawn"
            )
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
    store: SqlStore

    def sql_store(self, name: str) -> SqlStore:
        store = SqlStore(str(self.path), str(self.path.parent / f"{name}.sqlite"))
        self.addCleanup(store.db.close)
        return store

    def test_authority_changes_rechecked_at_transaction_for_caller_and_destination(self) -> None:
        self.raise_report()
        for who in ("caller", "destination"):
            expected = self.sam if who == "caller" else self.bea
            for change in ("removed", "role", "oid", "email"):
                with self.subTest(who=who, change=change):
                    self.register(expected)
                    before = copy.deepcopy(self.store.cases["ZF-3"])
                    audit = list(self.store.audit_entries())
                    save = self.store.save

                    def changed_save(
                        expected: dict[str, Any] = expected,
                        change: str = change,
                        save: Callable[[], None] = save,
                    ) -> None:
                        other = self.store.assistant_connection()
                        try:
                            other.execute(
                                "DELETE FROM staff WHERE email=?", (expected["email"].lower(),)
                            )
                            if change != "removed":
                                replaced = dict(expected)
                                replaced[change] = {
                                    "role": "Contractor",
                                    "oid": "SYN-REPLACED",
                                    "email": "substitute@example.test",
                                }[change]
                                other.execute(
                                    "INSERT INTO staff (email, body) VALUES (?, ?)",
                                    (expected["email"].lower(), json.dumps(replaced)),
                                )
                        finally:
                            other.close()
                        save()

                    with patch.object(self.store, "save", side_effect=changed_save):
                        with self.assertRaises(PermissionError):
                            self.refer()
                    reopened = self.open_store()
                    self.assertEqual(reopened.cases["ZF-3"], before)
                    self.assertEqual(list(self.store.audit_entries()), audit)
                    self.assertIsNone(self.store.local.hazard_decision)
                    self.register(expected)
        self.refer()
        self.accept()

    def test_failed_writes_preserve_prior_pending_audit_and_original_error(self) -> None:
        self.ready_for_release()
        for target, original in (
            ("save", OSError("Synthetic precommit save failure")),
            ("_append_audit", OSError("Synthetic transaction audit failure")),
            ("_validate_safety_clear", PermissionError("Synthetic commit refusal")),
            ("_validate_safety_clear", ConflictError("ZF-3")),
        ):
            with self.subTest(target=target, error=type(original).__name__):
                before = self.store.detail("ZF-3")
                audit = list(self.store.audit_entries())
                with self.store.lock:
                    self.store.audit(self.sam["email"], "prior_event", "ZF-2", "SYN-PRIOR")
                    prior = copy.deepcopy(self.store.local.pending)
                    with patch.object(self.store, target, side_effect=original):
                        with self.assertRaises(type(original)) as caught:
                            self.store.release_hazard(
                                self.bo, "ZF-3", 0, "SYN-REASON", "SYN-DECISION"
                            )
                    self.assertIs(caught.exception, original)
                    self.assertEqual(self.store.local.pending, prior)
                    self.assertIsNone(self.store.local.hazard_decision)
                reopened = self.open_store()
                self.assertEqual(reopened.detail("ZF-3"), before)
                self.assertEqual(
                    [event["action"] for event in reopened.audit_entries()],
                    [event["action"] for event in audit] + ["prior_event"],
                )
                self.assertTrue(reopened.verify_audit())
        self.store.release_hazard(self.bo, "ZF-3", 0, "SYN-REASON", "SYN-DECISION")

        for persistent in (False, True):
            with self.subTest(postcommit_sync_failure=True, persistent=persistent):
                idx = self.raise_report()
                self.refer(idx)
                self.accept(idx)
                self.store.record_repair(self.bea, "ZF-3", idx, "SYN-REPAIR")
                other = self.open_store()
                audit = list(self.store.audit_entries())
                original = OSError("Synthetic postcommit synchronization failure")
                save, sync = self.store.save, self.store._sync
                fault_state = dict(armed=0, failures=0)

                def interleaved_save(
                    other: Store = other,
                    save: Callable[[], None] = save,
                    state: dict[str, int] = fault_state,
                ) -> None:
                    other.log_call(self.sam, "ZF-2", "Contacted", "SYN-OTHER-WRITER")
                    state["armed"] = 1
                    save()

                def failed_sync(
                    original: OSError = original,
                    sync: Callable[[], None] = sync,
                    persistent: bool = persistent,
                    state: dict[str, int] = fault_state,
                ) -> None:
                    if state["armed"] and (persistent or state["failures"] == 0):
                        state["failures"] += 1
                        raise original
                    sync()

                with self.store.lock:
                    self.store.audit(self.sam["email"], "prior_event", "ZF-2", "SYN-PRIOR")
                    with (
                        patch.object(self.store, "save", side_effect=interleaved_save),
                        patch.object(self.store, "_sync", side_effect=failed_sync),
                        patch("zava_forward.core.hazard.logging.getLogger") as logger,
                        self.assertRaises(OSError) as postcommit_error,
                    ):
                        self.store.release_hazard(
                            self.bo, "ZF-3", idx, "SYN-REASON", "SYN-DECISION"
                        )
                    self.assertIs(postcommit_error.exception, original)
                    self.assertIsNone(self.store.local.hazard_decision)
                reopened = self.open_store()
                self.assertTrue(reopened.detail("ZF-3")["hazards"][idx]["released"])
                prior = [event["action"] for event in audit]
                after = [event["action"] for event in reopened.audit_entries()]
                self.assertEqual(after.count("prior_event"), prior.count("prior_event") + 1)
                self.assertEqual(after.count("safety_released"), prior.count("safety_released") + 1)
                self.assertEqual(len(after), len(prior) + 3)
                self.assertIn("committed", " ".join(original.__notes__))
                logger.return_value.exception.assert_called()
                self.assertTrue(reopened.verify_audit())
                self.store.save()
                self.assertEqual(list(self.store.audit_entries()), list(reopened.audit_entries()))

    def test_recovery_read_failure_quarantines_hazard_and_keeps_prior_audit(self) -> None:
        self.ready_for_release()
        for persistent, target in (
            (False, "save"),
            (True, "save"),
            (False, "_validate_safety_clear"),
            (True, "_validate_safety_clear"),
        ):
            with self.subTest(persistent=persistent, target=target):
                before = self.store.detail("ZF-3")
                audit = list(self.store.audit_entries())
                original = (
                    OSError("Synthetic original save failure")
                    if target == "save"
                    else PermissionError("Synthetic commit refusal")
                )
                db = self.store.db

                class ReadFault:
                    armed = False
                    failures = 0

                    def __init__(self, db: Any, persistent: bool) -> None:
                        self.db = db
                        self.persistent = persistent

                    def execute(self, sql: str, args: Any = ()) -> Any:
                        if (
                            self.armed
                            and sql.startswith("SELECT rowversion, body FROM cases")
                            and (self.persistent or self.failures == 0)
                        ):
                            self.failures += 1
                            raise OSError("Synthetic recovery read failure")
                        return self.db.execute(sql, args)

                    def __getattr__(self, name: str) -> Any:
                        return getattr(self.db, name)

                fault = ReadFault(db, persistent)

                def failed_save(fault: ReadFault = fault, original: Exception = original) -> None:
                    fault.armed = True
                    raise original

                with self.store.lock:
                    self.store.audit(self.sam["email"], "prior_event", "ZF-2", "SYN-PRIOR")
                    with (
                        patch.object(self.store, "db", fault),
                        patch.object(self.store, target, side_effect=failed_save),
                        self.assertLogs("zava_forward.core.hazard", level="ERROR"),
                        self.assertRaises(type(original)) as caught,
                    ):
                        self.store.release_hazard(self.bo, "ZF-3", 0, "SYN-REASON", "SYN-DECISION")
                    self.assertIs(caught.exception, original)
                    self.assertTrue(original.__notes__)
                    self.assertEqual(self.store.local.touched, set())
                    self.assertIsNone(self.store.local.hazard_decision)
                reopened = self.open_store()
                self.assertEqual(reopened.detail("ZF-3"), before)
                self.assertEqual(
                    [event["action"] for event in reopened.audit_entries()],
                    [event["action"] for event in audit] + ["prior_event"],
                )
                self.store.save()
                self.assertEqual(self.store.detail("ZF-3"), before)
                self.assertTrue(reopened.verify_audit())

    def test_interleaved_emergency_hold_blocks_every_guarded_commit(self) -> None:
        def intake_before_commit(
            other: SqlStore, commit: Callable[[], None], expected: list[dict[str, Any]]
        ) -> None:
            other.raise_hazard(self.sam, "ZF-3", "Electrical", "Emergency", metadata=SOURCE)
            expected.extend(other.audit_entries())
            commit()

        for transition in (
            "issue",
            "reissue",
            "book",
            "complete",
            "correct",
            "accept",
            "handover",
            "signoff",
            "advance",
        ):
            with self.subTest(transition=transition):
                a = self.sql_store(transition)
                pid = a.create_package(
                    self.pam, "Synthetic race", "2026-01-01", "2099-12-31", "Loft", "SYN", "SYN-1"
                )
                details = supplied_contract_fixture(a, pid, self.pam)
                a.set_capacity(self.pam, pid, "Test Ltd", 5, 5, "SYN-CAPACITY", details)
                wid = ""
                if transition != "issue":
                    wid = a.issue_work_order(
                        self.pam, pid, "ZF-3", resident_bindings=RESIDENT_BINDINGS
                    )
                    a.record_wo_appointment(self.pam, wid, "Booked", "2099-01-01")
                if transition == "correct":
                    a.complete_work_order(self.pam, wid)
                if transition in ("accept", "handover", "signoff"):
                    with a.lock:
                        c = a._case("ZF-3")
                        if transition == "signoff":
                            c["technical"] = dict(
                                design_by=self.rex["email"], design_version=1, signoffs={}
                            )
                        else:
                            c["quality"] = copy.deepcopy(fixture()["cases"][1]["quality"])
                            if transition == "accept":
                                c["quality"][0].update(
                                    state="Submitted",
                                    recorded_by=self.sam["name"],
                                    recorded_by_code=self.sam["code"],
                                )
                        a.save()
                inspector = self.bo
                operations: dict[str, Callable[[], object]] = {
                    "issue": partial(
                        a.issue_work_order,
                        self.pam,
                        pid,
                        "ZF-3",
                        resident_bindings=RESIDENT_BINDINGS,
                    ),
                    "reissue": partial(
                        a.reissue_work_order,
                        self.pam,
                        wid,
                        "Loft",
                        "Reason",
                        resident_bindings=RESIDENT_BINDINGS,
                    ),
                    "book": partial(a.record_wo_appointment, self.pam, wid, "Booked", "2099-01-02"),
                    "complete": partial(a.complete_work_order, self.pam, wid, "SYN-DONE"),
                    "correct": partial(
                        a.correct_work_order,
                        self.pam,
                        wid,
                        "SYN-CORRECTION",
                        resident_bindings=RESIDENT_BINDINGS,
                    ),
                    "accept": partial(a.accept_quality, self.pam, "ZF-3", 0),
                    "handover": partial(
                        a.hand_over_quality, self.pam, "ZF-3", 0, "Guarantees", True
                    ),
                    "signoff": partial(
                        a.technical_action,
                        inspector,
                        "ZF-3",
                        dict(action="signoff_give", type="building"),
                    ),
                    "advance": partial(a.advance, self.sam, "ZF-3"),
                }
                before_case = a.detail("ZF-3")
                before_proc = copy.deepcopy(a.data["procurement"])
                b = self.sql_store(transition)
                save = a.save
                expected_audit: list[dict[str, Any]] = []

                with patch.object(
                    a, "save", side_effect=partial(intake_before_commit, b, save, expected_audit)
                ):
                    with self.assertRaises(GateError):
                        operations[transition]()
                self.assertEqual(a.data["procurement"], before_proc)
                reopened = self.sql_store(transition)
                self.assertEqual(reopened.data["procurement"], before_proc)
                after_case = reopened.detail("ZF-3")
                for key in ("stage", "closed", "quality", "technical"):
                    self.assertEqual(after_case.get(key), before_case.get(key))
                self.assertEqual(sum(not h["released"] for h in after_case["hazards"]), 1)
                self.assertEqual(list(reopened.audit_entries()), expected_audit)
                self.assertTrue(reopened.verify_audit())

    def test_stale_clear_dependency_refuses_procurement_and_discards_audit(self) -> None:
        a = self.sql_store("stale")
        pid = a.create_package(
            self.pam, "Synthetic race", "2026-01-01", "2099-12-31", "Loft", "SYN", "SYN-1"
        )
        details = supplied_contract_fixture(a, pid, self.pam)
        a.set_capacity(self.pam, pid, "Test Ltd", 5, 5, "SYN-CAPACITY", details)
        wid = a.issue_work_order(self.pam, pid, "ZF-3", resident_bindings=RESIDENT_BINDINGS)
        a.record_wo_appointment(self.pam, wid, "Booked", "2099-01-01")
        before = copy.deepcopy(a.data["procurement"])
        b = self.sql_store("stale")
        save = a.save

        def change_before_commit() -> None:
            b.log_call(self.sam, "ZF-3", "Contacted", "SYN-CONCURRENT")
            save()

        with patch.object(a, "save", side_effect=change_before_commit):
            with self.assertRaises(ConflictError):
                a.complete_work_order(self.pam, wid)
        self.assertEqual(a.data["procurement"], before)
        self.assertEqual(list(a.audit_entries())[-1]["action"], "log_contact")
        b.raise_hazard(self.sam, "ZF-3", "Electrical", "Emergency", metadata=SOURCE)
        # A refused request must not poison an unrelated home or a safe withdrawal.
        with a.lock:
            supplied_resident_fixture(a._case("ZF-2"))
            a.save()
        a.issue_work_order(self.pam, pid, "ZF-2", resident_bindings=RESIDENT_BINDINGS)
        a.withdraw_work_order(self.pam, wid, "Safety hold")
        self.assertTrue(a.verify_audit())

    def test_unsaved_precheck_does_not_leak_to_next_request(self) -> None:
        a = self.sql_store("aborted")
        b = self.sql_store("aborted")
        with self.assertRaisesRegex(ValueError, "Synthetic cancellation"):
            with a.lock:
                a.require_safety_clear(a.cases["ZF-3"])
                raise ValueError("Synthetic cancellation")
        b.raise_hazard(self.sam, "ZF-3", "Electrical", "Emergency", metadata=SOURCE)
        a.log_call(self.sam, "ZF-2", "Contacted", "Unrelated home")
        self.assertEqual(list(a.audit_entries())[-1]["action"], "log_contact")

    def test_transaction_reload_and_writer_lock_cover_validation_to_commit(self) -> None:
        a = self.sql_store("serialized")
        pid = a.create_package(
            self.pam, "Synthetic race", "2026-01-01", "2099-12-31", "Loft", "SYN", "SYN-1"
        )
        details = supplied_contract_fixture(a, pid, self.pam)
        a.set_capacity(self.pam, pid, "Test Ltd", 5, 5, "SYN-CAPACITY", details)
        wid = a.issue_work_order(self.pam, pid, "ZF-3", resident_bindings=RESIDENT_BINDINGS)
        a.record_wo_appointment(self.pam, wid, "Booked", "2099-01-01")
        b = self.sql_store("serialized")
        statements: list[str] = []
        a.db.set_trace_callback(statements.append)
        entered = Event()
        save = b.save
        validate = a._validate_safety_clear
        futures: list[Future[object]] = []

        def announced_save() -> None:
            entered.set()
            save()

        with ThreadPoolExecutor(max_workers=1) as pool:

            def intake_after_transaction_check() -> None:
                validate()
                self.assertTrue(a.db.in_transaction)
                futures.append(
                    pool.submit(
                        b.raise_hazard,
                        self.sam,
                        "ZF-3",
                        "Electrical",
                        "Emergency",
                        metadata=SOURCE,
                    )
                )
                self.assertTrue(entered.wait(timeout=5))
                self.assertFalse(futures[0].done())

            with (
                patch.object(b, "save", side_effect=announced_save),
                patch.object(
                    a, "_validate_safety_clear", side_effect=intake_after_transaction_check
                ),
            ):
                a.complete_work_order(self.pam, wid)
                futures[0].result(timeout=10)
        reload_at = statements.index("SELECT rowversion, body FROM cases WHERE id='ZF-3'")
        self.assertLess(statements.index("BEGIN IMMEDIATE"), reload_at)
        self.assertLess(reload_at, statements.index("COMMIT"))
        actions = [e["action"] for e in a.audit_entries()]
        self.assertLess(actions.index("workorder_completed"), actions.index("safety_raised"))
        with self.assertRaises(GateError):
            a.correct_work_order(self.pam, wid, "Cannot restart held work")
        self.assertTrue(a.verify_audit())
