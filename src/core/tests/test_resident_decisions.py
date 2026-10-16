"""Synthetic exact-scope decisions, authority, release and independent redress."""

import copy
import json
import tempfile
import unittest
from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import Any
from unittest.mock import patch

from dataset import DATA
from zava_forward.core import ai_tasks, controls, projection
from zava_forward.core.quality import checklist_for
from zava_forward.core.resident_decisions import resident_gate
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, GateError, Store

MEASURES = ("Loft insulation", "Cavity wall")


class JsonResidentDecisions(unittest.TestCase):
    sql = False

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        data = copy.deepcopy(DATA)
        data["cases"][0]["measures"] = list(MEASURES)
        data["staff"].extend(
            [
                dict(
                    code="RLO-2",
                    name="Rae Reviewer",
                    email="rae@example.test",
                    role="Resident Liaison Officer",
                ),
                dict(
                    code="RC-1",
                    name="Rex Coordinator",
                    email="rex@example.test",
                    role="Retrofit Coordinator",
                ),
                dict(
                    code="CON-1",
                    name="Kim Contractor",
                    email="kim@example.test",
                    role="Contractor",
                    contractor="Test Ltd",
                ),
            ]
        )
        self.sam, self.pam, self.rae, self.rex, self.kim = data["staff"]
        self.path.write_text(json.dumps(data))
        self.store = self.open_store()
        self.store.technical_action(self.pam, "ZF-1", dict(action="design_submit", note="SYN"))

    def open_store(self) -> Store:
        if self.sql:
            store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
            self.addCleanup(store.db.close)
            return store
        return Store(str(self.path))

    def action(self, action: str, **body: Any) -> None:
        self.store.resident_action(self.sam, "ZF-1", dict(action=action, **body))

    def scope(self, measure: str = MEASURES[0], design: int = 1) -> None:
        self.action(
            "scope_record", measure=measure, design_version=design, scope="SYN-SCOPE", source="SYN"
        )

    def answer(self, measure: str = MEASURES[0], status: str = "Accepted", **kw: Any) -> None:
        body = dict(
            measure=measure,
            context_revision=1,
            status=status,
            answered_by="The resident",
            source="SYN-SOURCE-CANARY",
            note="SYN-NOTE-CANARY",
        )
        body.update(kw)
        self.action("decision_record", **body)

    def authority(self, **kw: Any) -> None:
        body = dict(
            measure=MEASURES[0],
            context_revision=1,
            representative_ref="SYN-REP-A",
            status="Confirmed",
            tasks=["Works decision", "Receive information"],
            source="SYN-AUTH-CANARY",
            authority_date="2026-01-01",
            review_date="2099-01-01",
            resident_wishes="SYN-WISHES-CANARY",
            safe_contact_ref="SYN-SAFE-CANARY",
        )
        body.update(kw)
        self.action("representative_record", **body)

    def bind(self, *measures: str) -> list[dict[str, Any]]:
        return [dict(measure=m, context_revision=1) for m in measures]

    def unchanged_failure(self, operation: Callable[[], object]) -> None:
        before = copy.deepcopy(self.store.cases["ZF-1"])
        audit = list(self.store.audit_entries())
        with self.assertRaises((ValueError, PermissionError, GateError, ConflictError)):
            operation()
        self.assertEqual(self.store.cases["ZF-1"], before)
        self.assertEqual(list(self.store.audit_entries()), audit)

    def test_unknown_scope_source_and_no_contact_or_legacy_inference(self) -> None:
        self.store.log_call(self.sam, "ZF-1", "Happy to go ahead", "Access agreed")
        self.store.set_decision(self.sam, "ZF-1", "Accepted")
        d = self.store.detail("ZF-1")
        self.assertEqual([m["status"] for m in d["measure_decisions"]], ["Not recorded"] * 2)
        self.assertTrue(resident_gate(self.store.cases["ZF-1"]))
        self.unchanged_failure(lambda: self.answer())
        self.scope()
        self.unchanged_failure(lambda: self.answer(source=""))
        self.unchanged_failure(lambda: self.answer(status=""))
        self.unchanged_failure(lambda: self.answer(context_revision=True))
        self.unchanged_failure(lambda: self.answer(context_revision=2))
        self.answer()
        d = self.store.detail("ZF-1")
        self.assertEqual(
            [m["status"] for m in d["measure_decisions"]], ["Accepted", "Not recorded"]
        )
        a = d["measure_decisions"][0]["versions"][0]
        self.assertEqual(
            (a["case_id"], a["measure"], a["scope"], a["design_version"], a["source"]),
            ("ZF-1", MEASURES[0], "SYN-SCOPE", 1, "SYN-SOURCE-CANARY"),
        )
        self.assertFalse(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        self.unchanged_failure(
            lambda: self.store.resident_action(
                self.kim, "ZF-1", dict(action="decision_record", measure=MEASURES[0])
            )
        )

    def test_design_change_and_switch_back_never_restore_old_acceptance(self) -> None:
        self.scope()
        self.answer()
        history = copy.deepcopy(self.store.cases["ZF-1"]["measure_decisions"])
        self.store.technical_action(
            self.pam, "ZF-1", dict(action="design_change", note="SYN-CHANGED")
        )
        self.assertIsNone(self.store.detail("ZF-1")["measure_decisions"][0]["context"])
        self.assertTrue(resident_gate(self.store.cases["ZF-1"]))
        self.unchanged_failure(lambda: self.scope(design=1))
        self.unchanged_failure(lambda: self.scope(design=3))
        self.scope(design=2)
        self.assertEqual(
            self.store.detail("ZF-1")["measure_decisions"][0]["status"], "Not recorded"
        )
        self.scope(design=2)
        self.assertEqual(self.store.cases["ZF-1"]["measure_decisions"], history)
        self.answer(context_revision=3)
        self.assertFalse(
            resident_gate(self.store.cases["ZF-1"], [dict(measure=MEASURES[0], context_revision=3)])
        )

    def test_authority_tasks_versions_dates_safe_contact_and_multiple_representatives(self) -> None:
        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN-CONTACT")
        self.authority(tasks=["Attend", "Communicate"])
        self.unchanged_failure(
            lambda: self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        )
        self.authority()
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        self.assertFalse(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        self.authority(representative_ref="SYN-REP-B", tasks=["Attend"])
        self.assertFalse(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        for status in ("Disputed", "Unclear", "Revoked"):
            self.authority(status=status)
            self.assertTrue(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
            self.unchanged_failure(
                lambda: self.action(
                    "disclosure_check",
                    measure=MEASURES[0],
                    context_revision=1,
                    representative_ref="SYN-REP-A",
                    task="Receive information",
                )
            )
        self.authority()
        self.assertTrue(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        for today, held in (("2098-12-31", False), ("2099-01-01", True)):
            with patch.object(controls, "today", return_value=today):
                self.assertEqual(
                    bool(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0]))), held
                )
        self.action("safe_contact_record", safe_contact_ref="SYN-NEW-SAFE", source="SYN-CHANGE")
        self.assertTrue(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN-RETURN")
        self.assertTrue(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        self.answer()
        self.assertFalse(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        for bad in (
            dict(authority_date="2099-01-01"),
            dict(review_date="2025-01-01"),
            dict(review_date="invalid"),
            dict(tasks=["Approve everything"]),
            dict(source=""),
            dict(resident_wishes=""),
        ):
            self.unchanged_failure(partial(self.authority, **bad))

    def package(self) -> str:
        pid = self.store.create_package(
            self.pam, "SYN", "2026-01-01", "2099-01-01", "SYN-SCOPE", "SYN-CONTRACT"
        )
        self.store.set_capacity(self.pam, pid, "Test Ltd", 5, 5, "SYN-CAPACITY")
        assert isinstance(pid, str)
        return pid

    def test_pause_withdrawal_dependency_isolation_and_evidenced_restart(self) -> None:
        for measure in MEASURES:
            self.scope(measure)
            self.answer(measure)
        pid = self.package()
        wid_a = self.store.issue_work_order(
            self.pam, pid, "ZF-1", resident_bindings=self.bind(MEASURES[0])
        )
        # Separate packages permit independent work orders on this same home.
        pid_b = self.package()
        wid_b = self.store.issue_work_order(
            self.pam, pid_b, "ZF-1", resident_bindings=self.bind(MEASURES[1])
        )
        sibling = copy.deepcopy(self.store.cases["ZF-1"]["measure_decisions"][MEASURES[1]])
        for status in ("Paused", "Withdrawn"):
            self.answer(status=status)
            self.assertEqual(self.store.cases["ZF-1"]["measure_decisions"][MEASURES[1]], sibling)
            for bindings in ([], self.bind(MEASURES[0]), self.bind(*MEASURES)):
                self.assertTrue(resident_gate(self.store.cases["ZF-1"], bindings))
            self.unchanged_failure(
                lambda: self.store.record_wo_appointment(self.pam, wid_a, "Booked", "2098-01-01")
            )
        self.store.record_wo_appointment(self.pam, wid_b, "Booked", "2098-01-01")
        self.store.complete_work_order(self.pam, wid_b)
        self.unchanged_failure(
            lambda: self.store.correct_work_order(
                self.pam, wid_b, "SYN", resident_bindings=self.bind(MEASURES[0])
            )
        )
        self.unchanged_failure(
            lambda: self.store.reissue_work_order(self.pam, wid_a, "Changed", "SYN")
        )
        self.unchanged_failure(lambda: self.answer())
        self.answer(review_ref="SYN-HUMAN-REVIEW")
        self.store.record_wo_appointment(self.pam, wid_a, "Booked", "2098-01-01")
        self.assertEqual(
            self.store.cases["ZF-1"]["resident_reviews"][MEASURES[0]]["status"],
            "Reviewed with supplied acceptance",
        )
        self.assertTrue(self.store.verify_audit())

    def test_resident_acceptance_never_clears_technical_or_hazard_gates(self) -> None:
        for measure in MEASURES:
            self.scope(measure)
            self.answer(measure)
        with self.store.lock:
            c = self.store._case("ZF-1")
            c.update(stage="Final checks before ordering", funding_ok=True)
            self.store.save()
        self.assertFalse(resident_gate(self.store.cases["ZF-1"]))
        self.assertIn("sign-off", " ".join(self.store.detail("ZF-1")["gate"]))
        self.unchanged_failure(lambda: self.store.advance(self.pam, "ZF-1"))
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["technical"]["signoffs"] = {
                key: dict(status="Signed off", history=[])
                for key in ("assessment", "design", "building", "coordination")
            }
            c["documents"] = [
                dict(id=f"SYN-{kind}", kind=kind, generated=False) for kind in self.store.EVIDENCE
            ]
            self.store.save()
        self.assertEqual(self.store.detail("ZF-1")["gate"], [])
        self.store.technical_action(
            self.pam, "ZF-1", dict(action="signoff_return", type="coordination", reason="SYN")
        )
        technical = copy.deepcopy(self.store.cases["ZF-1"]["technical"])
        self.answer(status="Withdrawn")
        self.answer(review_ref="SYN-HUMAN-REVIEW")
        self.assertEqual(self.store.cases["ZF-1"]["technical"], technical)
        self.unchanged_failure(lambda: self.store.advance(self.pam, "ZF-1"))
        self.store.raise_hazard(
            self.sam,
            "ZF-1",
            "Electrical",
            "Emergency",
            metadata=dict(source="SYN", aware_at="2026-01-01T10:00:00Z"),
        )
        hazards = copy.deepcopy(self.store.cases["ZF-1"]["hazards"])
        self.answer(status="Withdrawn")
        self.answer(review_ref="SYN-HUMAN-REVIEW")
        self.assertEqual(self.store.cases["ZF-1"]["hazards"], hazards)
        self.assertEqual(self.store.cases["ZF-1"]["technical"], technical)
        self.assertFalse(resident_gate(self.store.cases["ZF-1"]))
        self.unchanged_failure(lambda: self.store.advance(self.pam, "ZF-1"))
        pid = self.package()
        self.unchanged_failure(
            lambda: self.store.issue_work_order(
                self.pam, pid, "ZF-1", resident_bindings=self.bind(MEASURES[1])
            )
        )

    def test_redress_independence_no_detriment_and_closed_case_access(self) -> None:
        self.scope()
        self.answer(status="Paused")
        before = copy.deepcopy(self.store.cases["ZF-1"])
        base = dict(
            route="Independent review",
            review_measure=MEASURES[0],
            review_decision_version=1,
            review_reference="SYN-REVIEW",
            summary="SYN",
            desired_outcome="Speak to a person",
            next_update="2099-01-01",
            service_owner=self.pam["email"],
            redress_owner=self.rae["email"],
        )
        self.unchanged_failure(
            lambda: self.action("service_open", **dict(base, redress_owner=self.sam["email"]))
        )
        self.action("service_open", **base)
        update = dict(
            action="service_update", id="SR-1", status="Resolved", next_update="2099-01-01"
        )
        self.unchanged_failure(lambda: self.store.resident_action(self.pam, "ZF-1", update))
        self.store.resident_action(self.rae, "ZF-1", update)
        self.unchanged_failure(lambda: self.action("service_close", id="SR-1", note="SYN"))
        self.store.resident_action(
            self.rae, "ZF-1", dict(action="service_close", id="SR-1", note="SYN")
        )
        with self.store.lock:
            self.store._case("ZF-1")["closed"] = True
            self.store.save()
        self.action("service_open", **dict(base, route="Complaint"))
        for key in ("measure_decisions", "resident_reviews", "decision", "hazards", "stage"):
            self.assertEqual(self.store.cases["ZF-1"][key], before[key])
        self.store.raise_hazard(
            self.sam,
            "ZF-1",
            "Electrical",
            "Emergency",
            metadata=dict(source="SYN", aware_at="2026-01-01T10:00:00Z"),
        )
        self.assertTrue(self.store.cases["ZF-1"]["closed"])

    def test_quality_dependencies_are_scoped_and_unknown_evidence_cannot_release(self) -> None:
        for measure in MEASURES:
            self.scope(measure)
            self.answer(measure)
        ids = []
        for measure in MEASURES:
            items = {label: "Synthetic evidence" for label in checklist_for(measure)["items"]}
            ids.append(
                self.store.submit_quality(
                    self.sam,
                    "ZF-1",
                    measure,
                    "Synthetic installer",
                    "Installer",
                    items,
                    context_revision=1,
                )
            )
        self.answer(status="Withdrawn")
        self.unchanged_failure(lambda: self.store.accept_quality(self.pam, "ZF-1", ids[0]))
        self.store.accept_quality(self.pam, "ZF-1", ids[1])
        self.store.hand_over_quality(self.pam, "ZF-1", ids[1], "Synthetic handover", True)
        self.store.submit_quality(
            self.sam,
            "ZF-1",
            MEASURES[1],
            "Synthetic installer",
            "Installer",
            {label: "Synthetic evidence" for label in checklist_for(MEASURES[1])["items"]},
        )
        self.unchanged_failure(lambda: self.store.accept_quality(self.pam, "ZF-1", 2))

    def test_detached_projection_persistence_audit_and_model_minimisation(self) -> None:
        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.authority()
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        before = copy.deepcopy(self.store.cases["ZF-1"])
        audit = list(self.store.audit_entries())
        for actor in (self.sam, self.pam, self.rex, self.kim):
            detail = self.store.detail("ZF-1", actor)
            if actor in (self.rex, self.kim):
                text = json.dumps(detail)
                for sentinel in ("SYN-AUTH-CANARY", "SYN-WISHES-CANARY", "SYN-SOURCE-CANARY"):
                    self.assertNotIn(sentinel, text)
            self.assertEqual(self.store.cases["ZF-1"], before)
        with patch.dict("os.environ", {"ZF_REASON_ROLES": "Retrofit Coordinator"}):
            detail = self.store.detail("ZF-1", self.sam)
            self.assertNotIn("representative_authorities", detail)
        self.assertEqual(list(self.store.audit_entries()), audit)
        self.store.log_call(self.sam, "ZF-1", "SYN", "SYN")
        again = self.open_store()
        for key in ("representative_authorities", "measure_decisions", "resident_scopes"):
            self.assertEqual(again.cases["ZF-1"][key], before[key])
        self.assertNotIn("SYN-WISHES-CANARY", json.dumps(audit))
        self.assertNotIn("SYN-SOURCE-CANARY", json.dumps(audit))
        source = self.store._facts(self.store.cases["ZF-1"])
        self.assertNotIn("SYN-AUTH-CANARY", source)
        self.assertNotIn("SYN-WISHES-CANARY", source)
        self.assertEqual(
            projection.contractor_detail(before, before).get("measure_decisions"), None
        )

    def test_unchecked_addressed_draft_refused_but_enabled_ai_proposals_survive(self) -> None:
        with self.store.lock:
            self.store._case("ZF-1")["resident"]["representative"] = dict(name="SYN-REP")
            self.store.save()
        before = copy.deepcopy(self.store.cases["ZF-1"])
        self.unchanged_failure(lambda: self.store.draft("ZF-1", "visit"))
        result = dict(source="ai", model="synthetic-adapter", validated=True, verified=True)
        with patch.object(ai_tasks, "run_text_task", return_value=result) as service:
            for task in ("message", "summary"):
                proposal = self.store.ai_run(self.sam, "ZF-1", task)
                self.assertIn("not approved", proposal["label"])
            self.assertEqual(service.call_count, 2)
        self.assertEqual(self.store.cases["ZF-1"], before)


class SqlResidentDecisions(JsonResidentDecisions):
    sql = True

    def test_save_clears_scoped_dependencies_inside_outer_lock(self) -> None:
        assert isinstance(self.store, SqlStore)
        self.scope()
        self.answer()
        pid = self.package()
        with self.store.lock:
            self.store.require_stock_clear(self.store.cases["ZF-1"])
            self.store.issue_work_order(
                self.pam, pid, "ZF-1", resident_bindings=self.bind(MEASURES[0])
            )
            self.assertEqual(self.store.local.resident_clear, [])
            self.assertEqual(self.store.local.safety_clear, set())
            self.assertEqual(self.store.local.stock_clear, set())

    def test_stock_race_rechecks_all_dependencies_and_clears_them_after_rollback(self) -> None:
        assert isinstance(self.store, SqlStore)
        self.scope()
        self.answer()
        other = self.open_store()
        before = copy.deepcopy(self.store.cases["ZF-1"])
        with self.store.lock:
            self.store.require_safety_clear(self.store.cases["ZF-1"])
            self.store.require_stock_clear(self.store.cases["ZF-1"])
            self.store.require_resident_clear(self.store.cases["ZF-1"], self.bind(MEASURES[0]))
            other.stock_reconcile(
                self.sam,
                "ZF-1",
                dict(
                    field="epc",
                    query_owner=self.sam["email"],
                    left=dict(
                        value="D",
                        source_id="SYN-REGISTER",
                        date="2026-01-01",
                        version="1",
                        validation_state="Unvalidated",
                    ),
                    right=dict(
                        value="E",
                        source_id="SYN-SURVEY",
                        date="2026-01-01",
                        version="1",
                        validation_state="Disputed",
                    ),
                ),
            )
            self.store._case("ZF-1")["reason"] = "Must not persist"
            self.store.audit(self.pam["email"], "synthetic_refused", "ZF-1", "SYN")
            with self.assertRaises(GateError):
                self.store.save()
            self.assertEqual(self.store.local.resident_clear, [])
            self.assertEqual(self.store.local.safety_clear, set())
            self.assertEqual(self.store.local.stock_clear, set())
            self.store.log_call(self.sam, "ZF-2", "Spoke", "Independent home")
        self.assertEqual(self.store.cases["ZF-1"]["reason"], before["reason"])
        self.assertEqual(self.store.cases["ZF-1"]["measure_decisions"], before["measure_decisions"])
        self.assertNotIn("synthetic_refused", [e["action"] for e in self.store.audit_entries()])
        self.assertTrue(self.store.verify_audit())

    def test_competing_pause_and_authority_change_refuse_stale_release_commit(self) -> None:
        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.authority()
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        pid = self.package()
        other = self.open_store()
        original = self.store.save

        def competing_pause() -> None:
            other.resident_action(
                self.sam,
                "ZF-1",
                dict(
                    action="decision_record",
                    measure=MEASURES[0],
                    context_revision=1,
                    status="Paused",
                    answered_by="The resident",
                    source="SYN",
                    note="SYN",
                ),
            )
            original()

        with patch.object(self.store, "save", side_effect=competing_pause):
            with self.assertRaises((GateError, ConflictError)):
                self.store.issue_work_order(
                    self.pam, pid, "ZF-1", resident_bindings=self.bind(MEASURES[0])
                )
        self.assertEqual(self.store.list_work_orders(self.pam), [])
        self.assertNotIn("workorder_issued", [e["action"] for e in self.store.audit_entries()])
        self.answer(review_ref="SYN-REVIEW")
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")

        def competing_authority() -> None:
            other.resident_action(
                self.sam,
                "ZF-1",
                dict(action="safe_contact_record", safe_contact_ref="SYN-NEW", source="SYN"),
            )
            original()

        with patch.object(self.store, "save", side_effect=competing_authority):
            with self.assertRaises((GateError, ConflictError)):
                self.store.issue_work_order(
                    self.pam, pid, "ZF-1", resident_bindings=self.bind(MEASURES[0])
                )
        self.assertEqual(self.store.list_work_orders(self.pam), [])
