"""Synthetic exact-scope decisions, authority, release and independent redress."""

import copy
import json
import os
import sqlite3
import tempfile
import unittest
import uuid
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime
from functools import partial
from pathlib import Path
from threading import Barrier
from typing import Any
from unittest.mock import patch

from dataset import DATA, supplied_appointment_fixture, supplied_contract_fixture
from zava_forward.core import ai_tasks, assistants, controls, projection, resident_decisions
from zava_forward.core.quality import checklist_for
from zava_forward.core.resident_decisions import resident_gate
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import ConflictError, GateError, Store

MEASURES = ("Loft insulation", "Cavity wall")


class PriorityCorrectionQuery(unittest.TestCase):
    def test_writer_decodes_only_corrections_from_60000_generated_case_bodies(self) -> None:
        with sqlite3.connect(":memory:") as db:
            db.execute("CREATE TABLE cases (id TEXT, body TEXT, priority_correction INTEGER)")
            db.execute(
                "CREATE INDEX ix_cases_priority_correction ON cases (priority_correction, id)"
                " WHERE priority_correction=1"
            )
            target = dict(kind="policy", id="priority-ranking", version="SYN-policy")
            body = json.dumps(
                dict(
                    unrelated_body="SYN-generated-" * 100,
                    affected_challenges=[dict(id="CH-OPEN", target=target)],
                )
            )
            db.executemany(
                "INSERT INTO cases VALUES (?, ?, 0)", ((f"SYN-{i}", body) for i in range(60000))
            )
            db.execute(
                "INSERT INTO cases VALUES (?, ?, 1)",
                (
                    "SYN-CORRECTED",
                    json.dumps(
                        dict(
                            affected_challenges=[
                                dict(
                                    id="CH-1",
                                    target=target,
                                    resolution=dict(outcome="Correction recorded"),
                                ),
                                dict(
                                    id="CH-2",
                                    target=target,
                                    resolution=dict(outcome="Explanation recorded"),
                                ),
                            ]
                        )
                    ),
                ),
            )
            statements: list[str] = []
            db.set_trace_callback(statements.append)
            store = SqlStore.__new__(SqlStore)
            store.db = db
            with patch.object(json, "loads", wraps=json.loads) as decodes:
                rows = store._priority_correction_rows()
            self.assertEqual(rows, [("SYN-CORRECTED", "CH-1", target)])
            self.assertEqual(decodes.call_count, 1)
            self.assertEqual(len(statements), 1)
            self.assertIn("json_each", statements[0])
            self.assertNotIn("SELECT body FROM cases", statements[0])
            plan = db.execute("EXPLAIN QUERY PLAN " + statements[0]).fetchall()
            self.assertTrue(any("ix_cases_priority_correction" in row[3] for row in plan), plan)


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

    def nomination(self, **changes: Any) -> dict[str, Any]:
        return dict(
            dict(
                action="nomination_record",
                case_id="ZF-1",
                kind="Self-referral",
                reported_subject_ref="SYN-WRONG-PERSON",
                account="  SYN-ORIGINAL-ACCOUNT\n",
                source="SYN-NOM-SOURCE",
                channel="Phone",
                owner=self.sam["email"],
                acknowledgement_ref="SYN-ACK-RECORDED",
                next_update="2099-01-01",
                non_digital_route="SYN Phone Sam or write to the staffed office.",
                hazard_concern=False,
            ),
            **changes,
        )

    def tenure(self, **changes: Any) -> dict[str, Any]:
        return dict(
            dict(
                action="tenure_intake",
                case_id="ZF-1",
                household_ref="SYN-HOUSEHOLD",
                expected_version=0,
                reported_tenure="Shared owner",
                reported_lease_interest="SYN-LEASE-PRIVATE",
                identity_state="Ambiguous",
                source="SYN-TENURE-SOURCE",
                owner=self.sam["email"],
                next_update="2099-01-01",
            ),
            **changes,
        )

    def test_intake_original_subject_correction_and_manual_history(self) -> None:
        proposal = self.priority_fixture()
        self.store.resident_action(self.sam, "ZF-1", self.challenge_body(proposal))
        before = copy.deepcopy(self.store.cases["ZF-1"])
        ranking = self.store._ranking()
        for channel in resident_decisions.INTAKE_CHANNELS:
            self.store.resident_action(self.sam, "ZF-1", self.nomination(channel=channel))
        original = copy.deepcopy(self.store.cases["ZF-1"]["nomination_records"][0]["original"])
        body = dict(
            action="nomination_correct",
            case_id="ZF-1",
            id=self.store.cases["ZF-1"]["nomination_records"][0]["id"],
            expected_version=1,
            reported_subject_ref="SYN-CORRECTED-PERSON",
            account="SYN competing evidence",
            source="SYN correction evidence",
            channel="Trusted intermediary",
            next_update="2099-01-02",
            challenge_id="CH-1",
        )
        self.store.resident_action(self.sam, "ZF-1", body)
        self.unchanged_failure(lambda: self.store.resident_action(self.sam, "ZF-1", body))
        records = self.open_store().detail("ZF-1", self.sam)["nomination_records"]
        self.assertEqual(records[0]["original"], original)
        self.assertEqual(original["account"], "  SYN-ORIGINAL-ACCOUNT\n")
        self.assertEqual(
            records[0]["corrections"][0]["reported_subject_ref"], "SYN-CORRECTED-PERSON"
        )
        self.assertEqual(
            records[0]["corrections"][0]["challenge"], before["affected_challenges"][0]
        )
        self.assertEqual(records[0]["corrections"][0]["recorded_by"]["code"], self.sam["code"])
        self.assertEqual(
            records[0]["review_status"], "Re-review required; no priority or consent change"
        )
        self.assertEqual(
            [r["original"]["channel"] for r in records], list(resident_decisions.INTAKE_CHANNELS)
        )
        for record in records:
            self.assertEqual(record["identity_status"], "Unknown")
            self.assertEqual(record["support_needs"], "Unknown")
            self.assertEqual(record["risk_flags"], "Unknown")
            self.assertEqual(record["owner"]["code"], self.sam["code"])
            self.assertEqual(record["acknowledgement"]["delivery"], "Not verified by this system")
        after = copy.deepcopy(self.open_store().cases["ZF-1"])
        after.pop("nomination_records")
        self.assertEqual(after, before)
        self.assertEqual(self.store._ranking(), ranking)
        self.assertTrue(self.open_store().verify_audit())

    def test_intake_wrong_identity_hazard_and_closed_input_no_mutation(self) -> None:
        for invalid in (
            self.nomination(case_id="ZF-2"),
            self.nomination(account="X" * 4001),
            self.nomination(hazard_concern=True),
            self.nomination(hazard_concern=None),
            self.nomination(owner=self.kim["email"]),
            self.nomination(owner=self.rex["email"]),
            self.nomination(verification="Approved"),
            self.nomination(channel="Unknown"),
            self.tenure(decision_route="Approved"),
            self.tenure(case_id="ZF-2"),
        ):
            with self.subTest(invalid=invalid["action"]):
                self.unchanged_failure(
                    partial(self.store.resident_action, self.sam, "ZF-1", invalid)
                )
        self.unchanged_failure(
            lambda: self.store.resident_action(
                dict(self.sam, code="FORGED"), "ZF-1", self.nomination()
            )
        )
        self.store.raise_hazard(
            self.sam,
            "ZF-1",
            "Damp and mould",
            "Emergency",
            "SYN independent",
            dict(source="SYN human hazard report", aware_at="2026-01-01T10:00:00Z"),
        )
        self.assertTrue(
            self.open_store().cases["ZF-1"]["hazards"][-1]["hold"]["status"] == "Active"
        )
        self.assertNotIn("nomination_records", self.open_store().cases["ZF-1"])

    def test_intake_tenure_unknown_case_wide_hold_and_reopen(self) -> None:
        for measure in MEASURES:
            self.scope(measure)
            self.answer(measure)
        self.assertEqual(resident_gate(self.store.cases["ZF-1"]), [])
        before = copy.deepcopy(self.store.cases["ZF-1"])
        self.store.resident_action(self.sam, "ZF-1", self.tenure())
        self.store.resident_action(
            self.sam,
            "ZF-1",
            self.tenure(
                expected_version=1,
                household_ref="Unknown",
                reported_tenure="Unknown",
                reported_lease_interest="Unknown",
                identity_state="Unknown",
            ),
        )
        self.unchanged_failure(lambda: self.store.resident_action(self.sam, "ZF-1", self.tenure()))
        self.unchanged_failure(lambda: self.scope())
        current = self.open_store().cases["ZF-1"]
        self.assertEqual(len(current["tenure_reports"]), 2)
        self.assertEqual(current["tenure_reports"][0]["reported_tenure"], "Shared owner")
        for report in current["tenure_reports"]:
            self.assertEqual(report["verification"], "Unknown")
            self.assertEqual(report["decision_route"], "Unknown")
            self.assertEqual(report["legal_position"], "Unknown")
            self.assertEqual(report["cost_position"], "Unknown")
            self.assertEqual(len(report["responsibility_questions"]), 7)
        self.assertEqual(resident_gate(current), [resident_decisions.TENURE_HOLD])
        self.assertEqual(
            resident_gate(current, self.bind(MEASURES[1])), [resident_decisions.TENURE_HOLD]
        )
        after = copy.deepcopy(current)
        after.pop("tenure_reports")
        after.pop("tenure_review_required")
        self.assertEqual(after, before)
        self.assertFalse(
            resident_gate(self.store.cases["ZF-2"]) == [resident_decisions.TENURE_HOLD]
        )

    def test_intake_sensitive_deletion_never_releases_tenure_hold(self) -> None:
        self.store.resident_action(self.sam, "ZF-1", self.nomination())
        self.store.resident_action(self.sam, "ZF-1", self.tenure())
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident"]["first_contact_at"] = "2020-01-01"
            c["legal_hold"] = dict(active=True)
            self.store.save()
        self.unchanged_failure(
            lambda: self.store.delete_resident_records(self.pam, "ZF-1", "2040-01-01")
        )
        with self.store.lock:
            self.store._case("ZF-1")["legal_hold"]["active"] = False
            self.store.save()
        self.store.delete_resident_records(self.pam, "ZF-1", "2040-01-01")
        c = self.open_store().cases["ZF-1"]
        self.assertNotIn("nomination_records", c)
        self.assertNotIn("tenure_reports", c)
        self.assertTrue(c["tenure_review_required"])
        self.assertEqual(resident_gate(c), [resident_decisions.TENURE_HOLD])

    def test_tenure_intake_preserves_accepted_status_and_heuristic_priority(self) -> None:
        for measure in MEASURES:
            self.scope(measure)
            self.answer(measure)
        current = self.store.cases["ZF-1"]
        competitor = copy.deepcopy(current)
        competitor.update(id="ZF-COMPETITOR", days_in_stage=current["days_in_stage"] + 4)
        before = self.store._heuristic_priority([current, competitor], 2)
        self.assertEqual([item["case_id"] for item in before], ["ZF-COMPETITOR", "ZF-1"])
        self.assertEqual(resident_decisions.resident_status(current), "Accepted")
        decisions = copy.deepcopy(current["measure_decisions"])

        self.store.resident_action(self.sam, "ZF-1", self.tenure())
        self.store = self.open_store()
        current = self.store.cases["ZF-1"]
        self.assertEqual(current["measure_decisions"], decisions)
        self.assertEqual(resident_gate(current), [resident_decisions.TENURE_HOLD])
        self.assertEqual(
            resident_gate(current, self.bind(MEASURES[0])), [resident_decisions.TENURE_HOLD]
        )
        self.assertEqual(resident_decisions.resident_status(current), "Accepted")
        self.assertEqual(self.store._heuristic_priority([current, competitor], 2), before)

    def test_nomination_identity_survives_retention_deletion_and_failed_intake(self) -> None:
        self.store.resident_action(self.sam, "ZF-1", self.nomination())
        with self.store.lock:
            self.store._case("ZF-1")["nomination_records"][0]["id"] = "NOM-1"
            self.store.save()
        deleted_ids = set()
        for cycle in range(2):
            old_id = self.store.cases["ZF-1"]["nomination_records"][-1]["id"]
            deleted_ids.add(old_id)
            correction = dict(
                action="nomination_correct",
                case_id="ZF-1",
                id=old_id,
                expected_version=1,
                reported_subject_ref="SYN-DELETED-SUBJECT",
                account="SYN-DELETED-CORRECTION",
                source="SYN-DELETED-SOURCE",
                channel="Letter",
                next_update="2099-01-02",
                challenge_id=None,
            )
            with self.store.lock:
                c = self.store._case("ZF-1")
                c["resident"]["first_contact_at"] = f"{2020 + cycle * 20}-01-01"
                self.store.save()
            self.store.delete_resident_records(self.pam, "ZF-1", f"{2030 + cycle * 20}-01-01")
            self.store = self.open_store()
            self.assertNotIn("nomination_records", self.store.cases["ZF-1"])
            before = copy.deepcopy(self.store.cases["ZF-1"])
            audit = list(self.store.audit_entries())
            with patch.object(self.store, "save", side_effect=RuntimeError("SYN precommit")):
                with self.assertRaises(RuntimeError):
                    self.store.resident_action(self.sam, "ZF-1", self.nomination())
            self.assertEqual(self.store.cases["ZF-1"], before)
            self.assertEqual(self.open_store().cases["ZF-1"], before)
            self.assertEqual(list(self.store.audit_entries()), audit)

            self.store.resident_action(
                self.sam,
                "ZF-1",
                self.nomination(reported_subject_ref="SYN-NEW-SUBJECT", account="SYN-NEW-ACCOUNT"),
            )
            self.store = self.open_store()
            record = copy.deepcopy(self.store.cases["ZF-1"]["nomination_records"][0])
            self.assertNotIn(record["id"], deleted_ids)
            self.assertEqual(record["version"], 1)
            self.assertEqual(record["corrections"], [])
            before = copy.deepcopy(self.store.cases["ZF-1"])
            audit = list(self.store.audit_entries())
            with self.assertRaisesRegex(ValueError, "nomination was not found"):
                self.store.resident_action(self.sam, "ZF-1", correction)
            self.assertEqual(self.store.cases["ZF-1"], before)
            self.assertEqual(self.open_store().cases["ZF-1"], before)
            self.assertEqual(list(self.store.audit_entries()), audit)

        self.store.resident_action(self.sam, "ZF-1", dict(correction, id=record["id"]))
        record = self.open_store().cases["ZF-1"]["nomination_records"][0]
        self.assertEqual(record["version"], 2)
        self.assertEqual(record["corrections"][0]["account"], "SYN-DELETED-CORRECTION")
        self.assertEqual(record["original"]["reported_subject_ref"], "SYN-NEW-SUBJECT")
        self.assertTrue(self.open_store().verify_audit())

    def test_nomination_identity_after_legacy_deletion_without_high_water_mark(self) -> None:
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident_retention_deleted_at"] = "2025-01-01"
            c["resident_retention_tombstone"] = dict(contacts_before_deletion=0)
            self.store.save()
        self.store = self.open_store()
        self.store.resident_action(self.sam, "ZF-1", self.nomination())
        current = copy.deepcopy(self.store.cases["ZF-1"])
        record = current["nomination_records"][0]
        self.assertNotEqual(record["id"], "NOM-1")
        audit = list(self.store.audit_entries())
        with self.assertRaisesRegex(ValueError, "nomination was not found"):
            self.store.resident_action(
                self.sam,
                "ZF-1",
                dict(
                    action="nomination_correct",
                    case_id="ZF-1",
                    id="NOM-1",
                    expected_version=1,
                    reported_subject_ref="SYN-DELETED-SUBJECT",
                    account="SYN-DELETED-CORRECTION",
                    source="SYN-DELETED-SOURCE",
                    channel="Phone",
                    next_update="2099-01-02",
                    challenge_id=None,
                ),
            )
        self.assertEqual(self.store.cases["ZF-1"], current)
        self.assertEqual(self.open_store().cases["ZF-1"], current)
        self.assertEqual(list(self.store.audit_entries()), audit)

    def test_intake_private_projection_and_existing_authority_unchanged(self) -> None:
        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.authority(tasks=["Communicate"])
        authority = copy.deepcopy(self.store.cases["ZF-1"]["representative_authorities"])
        self.store.resident_action(
            self.sam, "ZF-1", self.nomination(channel="Trusted intermediary")
        )
        self.store.resident_action(self.sam, "ZF-1", self.tenure())
        for actor in (self.rex, self.kim):
            output = json.dumps(self.store.detail("ZF-1", actor))
            for canary in ("SYN-ORIGINAL-ACCOUNT", "SYN-LEASE-PRIVATE", "SYN-TENURE-SOURCE"):
                self.assertNotIn(canary, output)
            for field in resident_decisions.INTAKE_FIELDS:
                self.assertNotIn(field, self.store.detail("ZF-1", actor))
            self.unchanged_failure(
                partial(self.store.resident_action, actor, "ZF-1", self.nomination())
            )
        self.assertEqual(self.store.cases["ZF-1"]["representative_authorities"], authority)
        self.assertNotIn("measure_decisions", self.store.cases["ZF-1"])
        self.assertIn("nomination_records", self.store.detail("ZF-1", self.sam))
        for capability in assistants.REGISTRY:
            prompt = json.dumps(assistants.capture(capability, self.store.cases["ZF-1"]))
            for canary in ("SYN-ORIGINAL-ACCOUNT", "SYN-LEASE-PRIVATE", "SYN-TENURE-SOURCE"):
                self.assertNotIn(canary, prompt)

    def test_intake_precommit_failure_rolls_back_state_and_audit(self) -> None:
        for body in (self.nomination(), self.tenure()):
            before = copy.deepcopy(self.store.cases["ZF-1"])
            audit = list(self.store.audit_entries())
            with patch.object(self.store, "save", side_effect=RuntimeError("SYN precommit")):
                with self.assertRaises(RuntimeError):
                    self.store.resident_action(self.sam, "ZF-1", body)
            self.assertEqual(self.store.cases["ZF-1"], before)
            self.assertEqual(list(self.store.audit_entries()), audit)
            self.assertEqual(self.open_store().cases["ZF-1"], before)

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

    def priority_fixture(self, reviewed: str | None = None) -> dict[str, Any]:
        result = self.store.ai_priority(self.sam, mode="workflow-only")
        if reviewed:
            self.store.resolve_priority(
                self.sam,
                result["id"],
                reviewed,
                "SYN supplied draft review",
                [dict(case_id="ZF-1", reason="SYN human edit")],
            )
        return dict(result)

    def challenge_body(
        self, proposal: dict[str, Any], kind: str = "proposal", channel: str = "Digital"
    ) -> dict[str, Any]:
        target = next(
            item
            for item in self.store.detail("ZF-1", self.sam)["challenge_targets"]
            if item["proposal_id"] == proposal["id"]
        )
        return dict(
            action="challenge_open",
            proposal_id=proposal["id"],
            proposal_version=target["proposal_version"],
            decision_version=target["decision_version"],
            target_kind=kind,
            channel=channel,
            source="SYN supplied challenge reference",
            request="SYN Please check the information used.",
            explanation="SYN The suggestion uses the recorded case information and rules.",
            owner=self.sam["email"],
            non_digital_route="SYN Ask Sam by phone or letter.",
            next_update="2099-01-01",
        )

    def resolve_challenge(self, cid: str = "CH-1", correction: bool = True) -> None:
        self.action(
            "challenge_resolve",
            id=cid,
            expected_version=1,
            resolution="Correction recorded" if correction else "Explanation recorded",
            resolution_ref="SYN supplied human resolution evidence",
            explanation="SYN A person checked the information; use a fresh suggestion.",
            next_update="2099-01-02",
        )

    def stale_sets(self) -> tuple[set[str], set[str]]:
        views = [
            self.store._rec_view(r)
            for r in self.store.data["recommendations"]
            if r.get("kind") != "ai_task"
        ]
        return (
            {r["id"] for r in views if r["stale"]},
            {r["id"] for r in views if r["review_stale"]},
        )

    def test_challenge_channels_explanation_and_negative_boundaries(self) -> None:
        proposal = self.priority_fixture("accept")
        before = copy.deepcopy(self.store.cases["ZF-1"])
        ranking = self.store._ranking()
        original = copy.deepcopy(self.store.data["recommendations"])
        for channel in ("Digital", "Phone", "Letter", "In person"):
            self.store.resident_action(
                self.sam, "ZF-1", self.challenge_body(proposal, channel=channel)
            )
        self.resolve_challenge(correction=False)
        again = self.open_store()
        records = again.detail("ZF-1", self.sam)["affected_challenges"]
        self.assertEqual(
            [r["channel"] for r in records], ["Digital", "Phone", "Letter", "In person"]
        )
        self.assertEqual(records[0]["human_decision"]["status"], "Accepted")
        self.assertEqual(records[0]["recorded_by"]["code"], self.sam["code"])
        self.assertEqual(records[0]["owner"]["email"], self.sam["email"])
        self.assertEqual(
            records[0]["resolution"]["reference"], "SYN supplied human resolution evidence"
        )
        self.assertEqual(self.stale_sets(), (set(), set()))
        after = copy.deepcopy(again.cases["ZF-1"])
        after.pop("affected_challenges")
        self.assertEqual(after, before)
        self.assertEqual(self.store._ranking(), ranking)
        self.assertEqual(again.data["recommendations"], original)
        self.assertTrue(again.verify_audit())

    def test_challenge_proposal_identity_and_terminal_resolution(self) -> None:
        first, second = self.priority_fixture("accept"), self.priority_fixture("edit")
        self.store.resident_action(self.sam, "ZF-1", self.challenge_body(first))
        self.resolve_challenge()
        self.assertEqual(self.stale_sets(), ({first["id"]}, {first["id"]}))
        with self.assertRaises(ValueError):
            self.action(
                "challenge_resolve",
                id="CH-1",
                expected_version=2,
                resolution="Explanation recorded",
                resolution_ref="SYN cannot erase correction",
                explanation="SYN",
                next_update="2099-01-03",
            )
        self.assertNotIn(second["id"], self.stale_sets()[0])
        self.assertEqual(self.open_store().cases["ZF-1"]["affected_challenges"][0]["version"], 2)

    def test_challenge_source_exact_dependency_manifest_and_original_reviews(self) -> None:
        first, second = self.priority_fixture("accept"), self.priority_fixture("edit")
        original = copy.deepcopy(self.store.data["recommendations"])
        body = self.challenge_body(first, "source")
        with self.store.lock:
            self.store._case("ZF-1")["home"]["epc"] = "B"
            self.store.save()
        fresh = self.priority_fixture()
        self.store.resident_action(self.sam, "ZF-1", body)
        self.resolve_challenge()
        self.assertEqual(
            self.stale_sets(), ({first["id"], second["id"]}, {first["id"], second["id"]})
        )
        self.assertNotIn(fresh["id"], self.stale_sets()[0])
        self.assertEqual(self.store.data["recommendations"][:2], original)
        self.assertEqual(self.open_store().latest_priority(self.sam)["stale"], False)

    def test_challenge_policy_cross_case_and_other_version_manifest(self) -> None:
        first = self.priority_fixture("accept")
        with self.store.lock:
            self.store._case("ZF-5")["owner_code"] = self.rae["code"]
            self.store.save()
        other_case = self.store.ai_priority(self.rae, mode="workflow-only")
        self.store.resolve_priority(self.rae, other_case["id"], "accept")
        distinct = self.priority_fixture()
        with self.store.lock:
            record = self.store.data["recommendations"][-1]
            record["policy_version"] = "SYN-different-policy-version"
            self.store.save()
        self.store.resident_action(self.sam, "ZF-1", self.challenge_body(first, "policy"))
        self.resolve_challenge()
        expected = {first["id"], other_case["id"]}
        self.assertEqual(self.stale_sets(), (expected, expected))
        self.assertNotIn(distinct["id"], expected)
        self.assertFalse(self.store.latest_priority(self.rae)["actionable"])
        self.assertFalse(self.store.latest_priority(self.rae)["relied_on"])

    def test_challenge_unknown_legacy_source_and_closed_input(self) -> None:
        proposal = self.priority_fixture()
        with self.store.lock:
            self.store.data["recommendations"][-1].pop("source_versions", None)
            self.store.save()
        for body in (
            self.challenge_body(proposal, "source"),
            dict(self.challenge_body(proposal), recorded_by=self.pam),
            dict(self.challenge_body(proposal), owner=self.kim["email"]),
            dict(self.challenge_body(proposal), proposal_version="stale"),
        ):

            def attempt(body: dict[str, Any] = body) -> None:
                self.store.resident_action(self.sam, "ZF-1", body)

            self.unchanged_failure(attempt)
        self.store.resident_action(self.sam, "ZF-1", self.challenge_body(proposal))
        self.resolve_challenge()
        with self.assertRaises(PermissionError):
            self.store.resolve_priority(self.sam, proposal["id"], "accept")
        with self.assertRaises(PermissionError):
            self.store.resolve_priority(
                self.sam, proposal["id"], "edit", "SYN", [dict(case_id="ZF-1", reason="SYN")]
            )
        self.assertEqual(
            self.store.resolve_priority(self.sam, proposal["id"], "reject", "SYN")["status"],
            "Rejected",
        )
        self.store.log_call(self.sam, "ZF-1", "SYN manual", "SYN unrelated manual work")
        self.assertTrue(self.store.cases["ZF-1"]["contacts"])
        hazards = copy.deepcopy(self.store.cases["ZF-1"]["hazards"])
        idx = self.store.raise_hazard(
            self.sam,
            "ZF-1",
            "Damp and mould",
            "Emergency",
            "SYN immediate human intake",
            dict(source="SYN independent hazard", aware_at="2026-01-01T10:00:00+01:00"),
        )
        after = self.open_store().cases["ZF-1"]["hazards"]
        self.assertEqual(after[:idx], hazards)
        self.assertEqual(after[idx]["source"], "SYN independent hazard")
        self.assertEqual(after[idx]["aware_at"], "2026-01-01T09:00+00:00")
        self.assertEqual(after[idx]["hold"]["status"], "Active")

    def test_challenge_edited_in_case_outside_generation_candidates(self) -> None:
        data = copy.deepcopy(DATA)
        data["staff"] = copy.deepcopy(self.store.data["staff"])
        for index in range(41):
            case = copy.deepcopy(self.store.cases["ZF-1"])
            case["id"] = f"SYN-EDIT-{index:02}"
            data["cases"].append(case)
        self.path = Path(self.tmp.name) / "edited-in" / "synthetic.json"
        self.path.parent.mkdir()
        self.path.write_text(json.dumps(data))
        self.store = self.open_store()
        proposal = self.priority_fixture()
        original = copy.deepcopy(self.store.data["recommendations"][-1])
        self.assertEqual(len(original["case_ids"]), 40)
        outside = next(
            c["id"]
            for c in self.store.cases.values()
            if c["owner_code"] == self.sam["code"]
            and not c["closed"]
            and c["id"] not in original["case_ids"]
        )
        original_version = resident_decisions.priority_binding(original)[0]
        self.store.resolve_priority(
            self.sam,
            proposal["id"],
            "edit",
            "SYN supplied outside-candidate human edit",
            [dict(case_id=outside, reason="SYN human-selected case")],
        )
        retained = copy.deepcopy(self.store.data["recommendations"][-1])
        target = next(
            t
            for t in self.store.detail(outside, self.sam)["challenge_targets"]
            if t["proposal_id"] == proposal["id"]
        )
        self.assertEqual(target["proposal_version"], original_version)
        self.assertIsNone(target["source_version"])
        self.assertEqual(target["human_decision"]["status"], "Edited")
        self.assertEqual(target["human_decision"]["final_items"], retained["final_items"])
        body = dict(
            action="challenge_open",
            proposal_id=proposal["id"],
            proposal_version=target["proposal_version"],
            decision_version=target["decision_version"],
            target_kind="proposal",
            channel="Phone",
            source="SYN supplied edited-case challenge",
            request="SYN Please check the retained human edit.",
            explanation="SYN The case was selected by a person after generation.",
            owner=self.sam["email"],
            non_digital_route="SYN Ask Sam by phone or letter.",
            next_update="2099-01-01",
        )
        before = copy.deepcopy(self.store.cases[outside])
        audit = list(self.store.audit_entries())
        for actor, invalid in (
            (self.sam, dict(body, proposal_version="wrong")),
            (self.sam, dict(body, decision_version="wrong")),
            (self.sam, dict(body, target_kind="source")),
            (self.rex, body),
            (self.kim, body),
        ):
            with self.subTest(actor=actor["email"], target=invalid["target_kind"]):
                with self.assertRaises((ValueError, PermissionError)):
                    self.store.resident_action(actor, outside, invalid)
                self.assertEqual(self.store.cases[outside], before)
                self.assertEqual(list(self.store.audit_entries()), audit)
        self.assertNotIn("challenge_targets", self.store.detail(outside, self.rex))
        self.assertNotIn("challenge_targets", self.store.detail(outside, self.kim))
        self.store.resident_action(self.sam, outside, body)
        reopened = self.open_store()
        record = reopened.detail(outside, self.sam)["affected_challenges"][0]
        self.assertEqual(
            record["target"], dict(kind="proposal", id=proposal["id"], version=original_version)
        )
        self.assertEqual(record["human_decision"], target["human_decision"])
        saved = next(r for r in reopened.data["recommendations"] if r["id"] == proposal["id"])
        self.assertEqual(saved, retained)
        for key in ("case_ids", "source_versions", "items", "workflow_items"):
            self.assertEqual(saved[key], original[key])
        self.assertNotIn(outside, saved["source_versions"])
        self.assertNotIn(outside, saved["case_ids"])

    def test_challenge_source_capture_precedes_generation(self) -> None:
        before = ai_tasks.source_hashes(self.store, self.sam, ["ZF-1"])
        run = self.store.ai.run

        def change_during_generation(*args: Any, **kwargs: Any) -> Any:
            with self.store.lock:
                self.store._case("ZF-1")["home"]["epc"] = "B"
                self.store.save()
            return run(*args, **kwargs)

        with patch.object(self.store.ai, "run", side_effect=change_during_generation):
            self.priority_fixture()
        self.assertEqual(
            self.store.data["recommendations"][-1]["source_versions"]["ZF-1"], before["ZF-1"]
        )
        self.priority_fixture()
        self.assertNotEqual(
            self.store.data["recommendations"][-1]["source_versions"]["ZF-1"], before["ZF-1"]
        )

    def test_challenge_multiple_causes_source_case_isolation_and_export(self) -> None:
        first, second = self.priority_fixture("accept"), self.priority_fixture("edit")
        with self.store.lock:
            self.store._case("ZF-5")["owner_code"] = self.rae["code"]
            self.store.save()
        other = self.store.ai_priority(self.rae, mode="workflow-only")
        # Deliberately identical hash on a distinct case tests the namespace boundary.
        with self.store.lock:
            self.store.data["recommendations"][-1]["source_versions"]["ZF-5"] = self.store.data[
                "recommendations"
            ][0]["source_versions"]["ZF-1"]
            self.store.save()
        self.store.resident_action(self.sam, "ZF-1", self.challenge_body(first, "source"))
        self.store.resident_action(self.sam, "ZF-1", self.challenge_body(second, "proposal"))
        self.resolve_challenge("CH-1")
        self.resolve_challenge("CH-2")
        self.assertEqual(
            self.stale_sets(), ({first["id"], second["id"]}, {first["id"], second["id"]})
        )
        self.assertNotIn(other["id"], self.stale_sets()[0])
        bundle = self.store.continuity_export(self.pam)
        exported = next(r for r in bundle["ai_records"] if r["id"] == second["id"])
        self.assertTrue(exported["review_stale"])
        self.assertEqual(exported["status"], "Edited")
        self.assertFalse(exported["relied_on"])
        self.assertEqual(len(exported["challenge_ids"]), 2)
        self.assertNotIn("SYN Please check", json.dumps(bundle))

    def test_challenge_priority_responses_use_current_dual_entitlement(self) -> None:
        proposal = self.priority_fixture()
        self.store.resident_action(self.sam, "ZF-1", self.challenge_body(proposal, "policy"))
        self.resolve_challenge()
        with self.store.lock:
            self.store._case("ZF-5")["owner_code"] = self.rex["code"]
            self.store.save()
        generated = self.store.ai_priority(self.rex, mode="workflow-only")
        for result in (
            generated,
            self.store.latest_priority(self.rex),
            self.store.resolve_priority(self.rex, generated["id"], "reject", "SYN manual"),
        ):
            self.assertTrue(result["stale"])
            self.assertFalse(result["actionable"])
            self.assertFalse(result["relied_on"])
            self.assertEqual(result["challenge_ids"], [])
            self.assertNotIn("ZF-1/CH-1", json.dumps(result))
        self.assertEqual(self.store.latest_priority(self.sam)["challenge_ids"], ["ZF-1/CH-1"])
        with patch.dict(os.environ, ZF_REASON_ROLES="Retrofit Programme Manager"):
            self.assertTrue(self.store.latest_priority(self.sam)["stale"])
            self.assertEqual(self.store.latest_priority(self.sam)["challenge_ids"], [])
        downgraded = dict(self.sam, role="Retrofit Coordinator")
        if self.sql:
            assert isinstance(self.store, SqlStore)
            self.store.db.execute(
                "UPDATE staff SET body=? WHERE email=?",
                (json.dumps(downgraded), self.sam["email"]),
            )
        else:
            self.store.staff[self.sam["email"]] = downgraded
        self.assertTrue(self.store.latest_priority(self.sam)["stale"])
        self.assertEqual(self.store.latest_priority(self.sam)["challenge_ids"], [])
        reopened = self.open_store() if self.sql else self.store
        self.assertEqual(reopened.latest_priority(downgraded)["challenge_ids"], [])

    def test_challenge_detail_cached_reader_registry_downgrade_and_removal(self) -> None:
        proposal = self.priority_fixture("accept")
        self.store.resident_action(self.sam, "ZF-1", self.challenge_body(proposal))
        cached = copy.deepcopy(self.sam)
        expected = self.store.detail("ZF-1", cached)
        self.assertEqual(
            expected["affected_challenges"][0]["request"], "SYN Please check the information used."
        )
        self.assertEqual(expected["challenge_targets"][0]["proposal_id"], proposal["id"])
        for registered in (dict(self.sam, role="Retrofit Coordinator"), None):
            with self.subTest(registry=registered):
                if self.sql:
                    assert isinstance(self.store, SqlStore)
                    if registered is None:
                        self.store.db.execute(
                            "DELETE FROM staff WHERE email=?", (self.sam["email"],)
                        )
                    else:
                        self.store.db.execute(
                            "UPDATE staff SET body=? WHERE email=?",
                            (json.dumps(registered), self.sam["email"]),
                        )
                    self.assertEqual(self.store.staff[self.sam["email"]], cached)
                elif registered is None:
                    self.store.staff.pop(self.sam["email"])
                else:
                    self.store.staff[self.sam["email"]] = registered
                denied = self.store.detail("ZF-1", cached)
                self.assertEqual(denied["id"], "ZF-1")
                self.assertEqual(denied["home"], expected["home"])
                self.assertNotIn("affected_challenges", denied)
                self.assertNotIn("challenge_targets", denied)
                self.assertNotIn("SYN Please check", json.dumps(denied))
                self.assertEqual(
                    self.store.detail("ZF-1", self.pam)["affected_challenges"],
                    expected["affected_challenges"],
                )
                self.assertEqual(
                    self.store.detail("ZF-1")["affected_challenges"],
                    expected["affected_challenges"],
                )
                self.assertNotIn("challenge_targets", self.store.detail("ZF-1"))
        if self.sql:
            assert isinstance(self.store, SqlStore)
            self.store.db.execute(
                "INSERT INTO staff (email, body) VALUES (?, ?)",
                (self.sam["email"], json.dumps(cached)),
            )
        else:
            self.store.staff[self.sam["email"]] = cached
        self.assertEqual(self.store.detail("ZF-1", cached), expected)
        with patch.dict(os.environ, ZF_REASON_ROLES="Retrofit Programme Manager"):
            self.assertNotIn("affected_challenges", self.store.detail("ZF-1", cached))
            self.assertNotIn("challenge_targets", self.store.detail("ZF-1", cached))
        self.assertIsNone(self.store.detail("SYN-MISSING", cached))

    def test_failed_priority_accept_edit_remove_disposition_and_audit(self) -> None:
        for action in ("accept", "edit"):
            proposal = self.priority_fixture()
            before = copy.deepcopy(self.store.data["recommendations"])
            audit = list(self.store.audit_entries())
            with (
                patch.object(self.store, "save", side_effect=RuntimeError("SYN before commit")),
                self.assertRaisesRegex(RuntimeError, "SYN before commit"),
            ):
                self.store.resolve_priority(
                    self.sam,
                    proposal["id"],
                    action,
                    "SYN",
                    [dict(case_id="ZF-1", reason="SYN human edit")],
                )
            self.assertEqual(self.store.data["recommendations"], before)
            self.assertEqual(list(self.store.audit_entries()), audit)
            self.assertEqual(self.open_store().data["recommendations"], before)
            self.assertTrue(self.store.verify_audit())

    def test_challenge_lookup_is_once_per_read_for_60000_generated_homes(self) -> None:
        proposal = self.priority_fixture()
        rec = self.store.data["recommendations"][-1]
        records = [dict(copy.deepcopy(rec), id=f"SYN-{i}") for i in range(52)]
        generated: dict[str, dict[str, Any]] = {
            f"SYN-HOME-{i}": dict(id=f"SYN-HOME-{i}") for i in range(60000)
        }
        generated["SYN-HOME-59999"]["affected_challenges"] = [
            dict(
                id="CH-1",
                target=dict(kind="policy", id="priority-ranking", version=rec["policy_version"]),
                resolution=dict(outcome="Correction recorded"),
            ),
            dict(
                id="CH-2",
                target=dict(kind="policy", id="priority-ranking", version="SYN-other-version"),
                resolution=dict(outcome="Correction recorded"),
            ),
            dict(
                id="CH-3",
                target=dict(kind="policy", id="priority-ranking", version=rec["policy_version"]),
                resolution=dict(outcome="Explanation recorded"),
            ),
        ]
        lookup = resident_decisions.priority_correction_lookup
        with (
            patch.object(self.store, "cases", generated),
            patch.dict(self.store.data, recommendations=records),
            patch.object(resident_decisions, "priority_correction_lookup", wraps=lookup) as calls,
        ):
            catalog = resident_decisions.challenge_catalog(self.store, "ZF-1")
            self.assertEqual(calls.call_count, 1)
            self.assertEqual(len(catalog), 52)
            for row in catalog:
                self.assertTrue(row["stale"])
                self.assertEqual(row["challenge_ids"], ["SYN-HOME-59999/CH-1"])
            calls.reset_mock()
            bundle = self.store.continuity_export(self.pam)
            self.assertEqual(calls.call_count, 1)
            self.assertEqual(len(bundle["ai_records"]), 52)
            self.assertTrue(all(row["stale"] for row in bundle["ai_records"]))
        self.assertEqual(proposal["stale"], False)

    def test_first_contact_retention_withdrawn_expired_and_purge(self) -> None:
        from datetime import date

        from zava_forward.core.resident_decisions import retention_schedule

        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.authority(review_date="2026-02-01")
        self.answer(status="Withdrawn")
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["contacts"] = [dict(at="2020-02-29T10:00", channel="Phone", outcome="SYN")]
            c["resident"]["first_contact_at"] = "2020-02-29"
            c["service_requests"] = [
                dict(representative_ref="SYN-REP", outcome="SYN-COMPLAINT-OUTCOME")
            ]
            self.store.save()
        with patch("zava_forward.core.controls.today", return_value="2025-02-27"):
            schedule = retention_schedule(self.store.cases["ZF-1"])
            self.assertEqual(schedule["due"], "2025-02-28")
            self.assertFalse(schedule["expired"])
        with patch("zava_forward.core.controls.today", return_value="2025-02-28"):
            schedule = retention_schedule(self.store.cases["ZF-1"])
            self.assertTrue(schedule["expired"])
            rows = self.store.retention_due(self.pam, today=date(2025, 2, 28))["records"]
            self.assertTrue(any(r["doc_id"] == "resident-decisions" for r in rows))
            self.store.approve_retention_deletion(
                self.pam, "ZF-1", "resident-decisions", today=date(2025, 2, 28)
            )
        again = self.open_store()
        c = again.cases["ZF-1"]
        for key in ("measure_decisions", "representative_authorities", "resident_safe_contact"):
            self.assertNotIn(key, c)
        self.assertNotIn("first_contact_at", c["resident"])
        self.assertEqual(c["decision"]["status"], "Not recorded")
        self.assertNotIn("SYN-WISHES-CANARY", json.dumps(c))
        self.assertEqual(len(c["contacts"]), 1)
        self.assertEqual(c["service_requests"], [dict(outcome="SYN-COMPLAINT-OUTCOME")])
        self.assertTrue(again.verify_audit())

    def test_returning_resident_general_contact_restarts_after_deletion(self) -> None:
        from zava_forward.core.resident_decisions import retention_schedule

        self.scope()
        self.answer()
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident"]["first_contact_at"] = "2020-02-29"
            c["contacts"] = [
                dict(at="2020-02-29T10:00"),
                dict(at="2025-02-28T10:00", note="SYN-OLD-CONTACT"),
            ]
            self.store.save()
        with patch("zava_forward.core.controls.today", return_value="2025-02-28"):
            self.store.approve_retention_deletion(
                self.pam, "ZF-1", "resident-decisions", today=date(2025, 2, 28)
            )
            self.store = self.open_store()
            c = self.store.cases["ZF-1"]
            self.assertIsNone(retention_schedule(c)["first_contact"])
            self.assertIsNone(retention_schedule(c)["due"])
            self.assertFalse(retention_schedule(c)["expired"])
            self.assertTrue(resident_gate(c, self.bind(MEASURES[0])))
            self.unchanged_failure(lambda: self.answer())
            with patch("zava_forward.core.store.datetime") as clock:
                clock.now.return_value = datetime(2025, 2, 28, 10)
                self.store.log_call(self.sam, "ZF-1", "SYN-RETURN", "SYN-NEW-CONTACT")
            self.scope()
            self.answer()
            self.store = self.open_store()
            c = self.store.cases["ZF-1"]
            self.assertEqual(retention_schedule(c)["first_contact"], "2025-02-28")
            self.assertEqual(retention_schedule(c)["due"], "2030-02-28")
            self.assertFalse(resident_gate(c, self.bind(MEASURES[0])))
            self.assertEqual(len(c["contacts"]), 3)
            self.assertEqual(len(c["measure_decisions"][MEASURES[0]]), 1)
            self.assertTrue(self.store.verify_audit())

    def test_returning_resident_safe_contact_starts_once_not_at_deletion(self) -> None:
        from zava_forward.core.resident_decisions import retention_schedule

        self.scope()
        self.answer(status="Withdrawn")
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident"]["first_contact_at"] = "2020-02-29"
            c["contacts"] = [dict(at="2020-02-29T10:00")]
            self.store.save()
        self.store.approve_retention_deletion(
            self.pam, "ZF-1", "resident-decisions", today=date(2025, 2, 28)
        )
        with patch.object(controls, "today", return_value="2026-02-28"):
            self.assertIsNone(retention_schedule(self.open_store().cases["ZF-1"])["due"])
            self.scope()
            self.assertIsNone(retention_schedule(self.store.cases["ZF-1"])["due"])
            with patch.object(controls, "now", return_value="2026-02-28T10:00"):
                self.action("safe_contact_record", safe_contact_ref="SYN-NEW-SAFE", source="SYN")
            self.assertTrue(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
            self.answer()
            self.store = self.open_store()
            self.assertEqual(retention_schedule(self.store.cases["ZF-1"])["due"], "2031-02-28")
            self.assertFalse(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        with (
            patch.object(controls, "today", return_value="2027-03-01"),
            patch.object(controls, "now", return_value="2027-03-01T10:00"),
        ):
            self.action("safe_contact_record", safe_contact_ref="SYN-LATER-SAFE", source="SYN")
            self.answer(status="Withdrawn")
            c = self.open_store().cases["ZF-1"]
            self.assertEqual(retention_schedule(c)["first_contact"], "2026-02-28")
            self.assertEqual(retention_schedule(c)["due"], "2031-02-28")

    def test_renewed_period_expires_and_contact_cannot_reset_before_next_deletion(self) -> None:
        from zava_forward.core.resident_decisions import retention_schedule

        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident"]["first_contact_at"] = "2016-02-29"
            c["contacts"] = [dict(at="2016-02-29")]
            self.store.save()
        for deletion_day, contact_day, due_day in (
            ("2021-02-28", "2024-02-29", "2029-02-28"),
            ("2029-02-28", "2030-03-01", "2035-03-01"),
        ):
            with patch.object(controls, "today", return_value=deletion_day):
                self.assertTrue(retention_schedule(self.store.cases["ZF-1"])["expired"])
                with patch.object(controls, "now", return_value=deletion_day + "T09:00"):
                    self.action("safe_contact_record", safe_contact_ref="SYN-EXPIRED", source="SYN")
                self.scope()
                with self.assertRaises(GateError):
                    self.store.require_resident_clear(
                        self.store.cases["ZF-1"], self.bind(MEASURES[0])
                    )
                self.assertTrue(retention_schedule(self.store.cases["ZF-1"])["expired"])
                self.store.approve_retention_deletion(
                    self.pam, "ZF-1", "resident-decisions", today=date.fromisoformat(deletion_day)
                )
                self.assertIsNone(retention_schedule(self.open_store().cases["ZF-1"])["due"])
            with (
                patch.object(controls, "today", return_value=contact_day),
                patch("zava_forward.core.store.datetime") as clock,
            ):
                clock.now.return_value = datetime.fromisoformat(contact_day + "T10:00")
                self.store.log_call(self.sam, "ZF-1", "SYN-RETURN", "SYN")
                self.scope()
                self.answer()
                self.store = self.open_store()
                schedule = retention_schedule(self.store.cases["ZF-1"])
                self.assertEqual(schedule["first_contact"], contact_day)
                self.assertEqual(schedule["due"], due_day)
                self.assertFalse(schedule["expired"])
                self.assertFalse(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        with patch.object(controls, "today", return_value="2035-03-01"):
            self.assertTrue(retention_schedule(self.store.cases["ZF-1"])["expired"])
            self.assertTrue(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))

    def test_legacy_deletion_ignores_old_contacts_and_allows_later_contact(self) -> None:
        from zava_forward.core.resident_decisions import retention_schedule

        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident"]["first_contact_at"] = "2020-02-29"
            c["resident_retention_deleted_at"] = "2025-02-28"
            c["contacts"] = [
                dict(at="2020-02-29"),
                dict(at="2025-02-28T10:00"),
                dict(at="invalid"),
                dict(at="2099-01-01"),
            ]
            self.store.save()
        with (
            patch.object(controls, "today", return_value="2025-03-01"),
            patch("zava_forward.core.store.datetime") as clock,
        ):
            self.assertIsNone(retention_schedule(self.open_store().cases["ZF-1"])["due"])
            clock.now.return_value = datetime(2025, 3, 1, 10)
            self.store.log_call(self.sam, "ZF-1", "SYN-RETURN", "SYN")
            self.scope()
            self.answer()
            c = self.open_store().cases["ZF-1"]
            self.assertEqual(retention_schedule(c)["first_contact"], "2025-03-01")
            self.assertEqual(retention_schedule(c)["due"], "2030-03-01")
            self.assertFalse(resident_gate(c, self.bind(MEASURES[0])))

    def test_deletion_tombstone_contains_only_boundary_metadata(self) -> None:
        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.authority()
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident"]["first_contact_at"] = "2020-02-29"
            c["contacts"] = [dict(at="2020-02-29", note="SYN-PERSONAL-CONTACT")]
            self.store.save()
        self.store.approve_retention_deletion(
            self.pam, "ZF-1", "resident-decisions", today=date(2025, 2, 28)
        )
        c = self.open_store().cases["ZF-1"]
        tombstone = {
            key: value for key, value in c.items() if key.startswith("resident_retention_")
        }
        self.assertEqual(
            tombstone,
            {
                "resident_retention_deleted_at": "2025-02-28",
                "resident_retention_tombstone": {"contacts_before_deletion": 1},
            },
        )
        self.assertIs(
            type(tombstone["resident_retention_tombstone"]["contacts_before_deletion"]), int
        )
        for personal in (
            "SYN-SAFE-CANARY",
            "SYN-WISHES-CANARY",
            "SYN-AUTH-CANARY",
            "SYN-REP-A",
            "SYN-NOTE-CANARY",
            "SYN-PERSONAL-CONTACT",
            self.sam["name"],
            self.sam["email"],
        ):
            self.assertNotIn(personal, json.dumps(tombstone))
        self.assertNotIn("first_contact_at", c["resident"])
        for key in (
            "resident_scopes",
            "measure_decisions",
            "representative_authorities",
            "resident_safe_contact",
            "resident_contact_history",
            "resident_reviews",
        ):
            self.assertNotIn(key, c)
        self.assertEqual(c["contacts"][0]["note"], "SYN-PERSONAL-CONTACT")
        self.assertTrue(self.store.verify_audit())

    def test_matrix_registered_writer_and_exact_private_fields(self) -> None:
        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.authority()
        self.answer()
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident"]["adjustment"] = "SYN-VULNERABILITY"
            c["contacts"] = [
                dict(
                    at="2026-10-16",
                    channel="Phone",
                    outcome="SYN-CONTACT-OUTCOME",
                    note="SYN-CONTACT-NOTE",
                    by="Sam Example",
                )
            ]
            self.store.save()
        with patch.dict("os.environ", {"ZF_REASON_ROLES": ""}):
            for role in controls.RESIDENT_VIEW_ROLES:
                text = json.dumps(self.store.detail("ZF-1", dict(self.sam, role=role)))
                for visible in ("SYN-WISHES-CANARY", "SYN-SAFE-CANARY", "SYN-NOTE-CANARY"):
                    self.assertIn(visible, text)
                for held in ("SYN-VULNERABILITY", "SYN-CONTACT-NOTE", "SYN-CONTACT-OUTCOME"):
                    self.assertNotIn(held, text)
        self.assertNotIn(
            "SYN-WISHES-CANARY",
            json.dumps(self.store.detail("ZF-1", dict(self.sam, role="Quality Inspector"))),
        )
        for actor in (self.pam, dict(self.sam, email="agent@example.test")):
            self.unchanged_failure(
                partial(
                    self.store.resident_action,
                    actor,
                    "ZF-1",
                    dict(action="safe_contact_record", safe_contact_ref="FORGED", source="FORGED"),
                )
            )
            self.unchanged_failure(partial(self.store.set_decision, actor, "ZF-1", "Accepted"))
        detail = self.store.detail("ZF-1", self.rex)
        self.assertEqual(detail["resident_safe_contact"], "SYN-SAFE-CANARY")
        self.assertEqual(detail["measure_decisions"][0]["versions"][0]["note"], "SYN-NOTE-CANARY")
        self.assertIn("SYN-WISHES-CANARY", json.dumps(detail))
        flags = self.store.detail("ZF-1", self.kim)["resident_readiness"]
        self.assertEqual(
            flags,
            [dict(measure=MEASURES[0], flag="Proceed"), dict(measure=MEASURES[1], flag="Hold")],
        )

    def test_first_contact_evidence_is_not_decision_date_and_stays_until_deletion(self) -> None:
        from zava_forward.core.resident_decisions import retention_schedule

        with patch.object(controls, "today", return_value="2026-10-16"):
            c = copy.deepcopy(self.store.cases["ZF-1"])
            c["decision"]["at"] = "2020-01-01"
            c["contacts"] = [dict(at="invalid"), dict(at="2099-01-01")]
            self.assertIsNone(retention_schedule(c)["due"])
            c["contacts"].append(dict(at="2022-10-17T10:00"))
            self.assertEqual(retention_schedule(c)["due"], "2027-10-17")
            c["resident"]["first_contact_at"] = "2024-01-01"
            self.assertEqual(retention_schedule(c)["due"], "2027-10-17")
            with patch("zava_forward.core.resident_decisions.RESIDENT_RETENTION_YEARS", 2):
                self.assertEqual(retention_schedule(c)["due"], "2024-10-17")
        with (
            patch.object(controls, "today", return_value="2026-10-16"),
            patch.object(controls, "now", return_value="2026-10-16T10:00"),
        ):
            self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.assertEqual(retention_schedule(self.store.cases["ZF-1"])["due"], "2031-10-16")
        self.store.log_call(self.sam, "ZF-1", "SYN", "SYN")
        self.assertEqual(
            self.open_store().cases["ZF-1"]["resident"]["first_contact_at"], "2026-10-16"
        )

    def test_retention_anniversary_holds_disclosure_and_legal_hold_blocks_purge(self) -> None:
        from datetime import date

        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.authority()
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident"]["first_contact_at"] = "2021-10-16"
            self.store.save()
        disclosure = dict(
            measure=MEASURES[0],
            context_revision=1,
            representative_ref="SYN-REP-A",
            task="Receive information",
        )
        with patch.object(controls, "today", return_value="2026-10-15"):
            self.action("disclosure_check", **disclosure)
            self.assertFalse(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
        with patch.object(controls, "today", return_value="2026-10-16"):
            for held in (False, True):
                with self.store.lock:
                    self.store._case("ZF-1")["legal_hold"] = dict(active=held)
                    self.store.save()
                self.unchanged_failure(lambda: self.action("disclosure_check", **disclosure))
                self.assertTrue(resident_gate(self.store.cases["ZF-1"], self.bind(MEASURES[0])))
            self.unchanged_failure(
                lambda: self.store.approve_retention_deletion(
                    self.pam, "ZF-1", "resident-decisions", today=date(2026, 10, 16)
                )
            )

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
        self.authority(review_date="2027-01-01")
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        for today, held in (("2026-12-31", False), ("2027-01-01", True)):
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
            self.pam, "SYN", "2026-01-01", "2099-01-01", "SYN-SCOPE", "SYN-CONTRACT", "SYN-1"
        )
        details = supplied_contract_fixture(self.store, pid, self.pam)
        self.store.set_capacity(self.pam, pid, "Test Ltd", 5, 5, "SYN-CAPACITY", details)
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
        supplied_appointment_fixture(self.store, self.pam, wid_b, "2098-01-01")
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
        supplied_appointment_fixture(self.store, self.pam, wid_a, "2098-01-01")
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

    def commitment(self, **kw: Any) -> None:
        body = dict(
            expected_version=0,
            purpose="SYN update about remedy",
            owner=self.sam["email"],
            due_at="2099-01-01T12:00:00Z",
            basis="SYN human-selected fixture date",
            safe_contact_ref="Unknown",
            status="Outstanding",
        )
        body.update(kw)
        self.action("update_record", **body)

    def request(self, route: str = "Complaint") -> None:
        self.action(
            "service_open",
            route=route,
            summary="SYN issue",
            desired_outcome="SYN remedy requested",
            service_owner=self.sam["email"],
            redress_owner=self.rae["email"],
            next_update="2099-01-01",
        )

    def register_followup_actor(self, actor: dict[str, Any]) -> None:
        if self.sql:
            assert isinstance(self.store, SqlStore)
            self.store.db.execute(
                "UPDATE staff SET body=? WHERE email=?", (json.dumps(actor), actor["email"])
            )
        else:
            self.store.staff[actor["email"]] = copy.deepcopy(actor)
            for index, current in enumerate(self.store.data["staff"]):
                if current["email"] == actor["email"]:
                    self.store.data["staff"][index] = copy.deepcopy(actor)
            self.store.save()

    def review_body(self, **kw: Any) -> dict[str, Any]:
        return dict(
            dict(
                action="service_open",
                route="Independent review",
                review_measure=MEASURES[0],
                review_decision_version=1,
                review_reference="SYN recorded decision",
                summary="SYN review",
                desired_outcome="SYN independent person",
                service_owner=self.pam["email"],
                redress_owner=self.rae["email"],
                next_update="2099-01-01",
            ),
            **kw,
        )

    def change_staff_email(self, actor: dict[str, Any], **kw: Any) -> dict[str, Any]:
        changed = dict(actor, email="changed@example.test", **kw)
        if self.sql:
            assert isinstance(self.store, SqlStore)
            self.store.db.execute(
                "UPDATE staff SET email=?, body=? WHERE email=?",
                (changed["email"], json.dumps(changed), actor["email"]),
            )
        else:
            self.store.staff.pop(actor["email"])
            self.store.staff[changed["email"]] = copy.deepcopy(changed)
            for index, current in enumerate(self.store.data["staff"]):
                if current["email"] == actor["email"]:
                    self.store.data["staff"][index] = copy.deepcopy(changed)
            self.store.save()
        return changed

    def test_decision_recorder_snapshot_is_server_derived_and_immutable(self) -> None:
        self.sam["oid"] = "SYN-RECORDER-OID"
        self.register_followup_actor(self.sam)
        self.scope()
        forged = dict(self.rae)
        self.answer(
            recorder_identity=forged,
            recorded_by_email=forged["email"],
            recorded_by=forged["name"],
        )
        first = copy.deepcopy(self.store.cases["ZF-1"]["measure_decisions"][MEASURES[0]][0])
        self.assertEqual(
            first["recorder_identity"],
            {key: self.sam.get(key) for key in ("email", "code", "name", "role", "oid")},
        )
        body = dict(
            action="decision_record",
            measure=MEASURES[0],
            context_revision=1,
            status="Accepted",
            answered_by="The resident",
            source="SYN",
        )
        for actor in (dict(self.sam, oid="FORGED"), dict(self.sam, code="FORGED"), self.pam):
            self.unchanged_failure(partial(self.store.resident_action, actor, "ZF-1", body))
        self.store.resident_action(self.rex, "ZF-1", body)
        again = self.open_store()
        self.assertEqual(again.cases["ZF-1"]["measure_decisions"][MEASURES[0]][0], first)
        self.assertEqual(
            again.detail("ZF-1", self.sam)["measure_decisions"][0]["versions"][0][
                "recorder_identity_status"
            ],
            "Known",
        )

    def test_changed_email_recorder_denied_open_and_reassignment_by_code_or_oid(self) -> None:
        self.sam["oid"] = "SYN-ORIGINAL-OID"
        self.register_followup_actor(self.sam)
        self.scope()
        self.answer()
        self.store.resident_action(self.pam, "ZF-1", self.review_body())
        historical = copy.deepcopy(self.store.cases["ZF-1"]["measure_decisions"])
        for stable in ("code", "oid"):
            with self.subTest(stable=stable):
                changed = self.change_staff_email(
                    self.sam,
                    code=self.sam["code"] if stable == "code" else "SYN-NEW-CODE",
                    oid="SYN-NEW-OID" if stable == "code" else self.sam["oid"].swapcase(),
                )
                self.store = self.open_store()
                self.unchanged_failure(
                    partial(
                        self.store.resident_action,
                        self.pam,
                        "ZF-1",
                        self.review_body(
                            redress_owner=changed["email"], reviewed_identity=dict(self.rae)
                        ),
                    )
                )
                self.unchanged_failure(
                    partial(
                        self.store.resident_action,
                        self.pam,
                        "ZF-1",
                        dict(
                            action="service_reassign",
                            id="SR-1",
                            expected_version=1,
                            responsibility="redress",
                            owner=changed["email"],
                            reviewed_identity=dict(self.rae),
                            note="SYN",
                        ),
                    )
                )
                self.assertEqual(self.store.cases["ZF-1"]["measure_decisions"], historical)
                # Restore the current registry only, never the historical snapshot.
                if self.sql:
                    assert isinstance(self.store, SqlStore)
                    self.store.db.execute(
                        "UPDATE staff SET email=?, body=? WHERE email=?",
                        (self.sam["email"], json.dumps(self.sam), changed["email"]),
                    )
                else:
                    self.store.staff.pop(changed["email"])
                    for index, current in enumerate(self.store.data["staff"]):
                        if current["email"] == changed["email"]:
                            self.store.data["staff"][index] = copy.deepcopy(self.sam)
                    self.register_followup_actor(self.sam)
        self.store.resident_action(
            self.pam,
            "ZF-1",
            dict(
                action="service_reassign",
                id="SR-1",
                expected_version=1,
                responsibility="redress",
                owner=self.rex["email"],
                note="SYN genuinely distinct reviewer",
            ),
        )
        self.assertEqual(
            self.open_store().cases["ZF-1"]["service_requests"][0]["redress_identity"]["code"],
            self.rex["code"],
        )
        self.assertTrue(self.store.verify_audit())

    def test_review_binding_survives_new_versions_and_retention_ordinal_reuse(self) -> None:
        self.scope()
        self.answer()
        original = copy.deepcopy(self.store.cases["ZF-1"]["measure_decisions"][MEASURES[0]][0])
        for _ in range(2):
            self.store.resident_action(self.pam, "ZF-1", self.review_body())
        with self.store.lock:
            case = self.store._case("ZF-1")
            case["service_requests"][1].pop("reviewed_identity")
            self.store.save()
        self.store.resident_action(
            self.rex,
            "ZF-1",
            dict(
                action="decision_record",
                measure=MEASURES[0],
                context_revision=1,
                status="Accepted",
                answered_by="The resident",
                source="SYN newer version by different recorder",
            ),
        )
        self.store.resident_action(self.pam, "ZF-1", self.review_body())
        self.assertEqual(
            self.store.cases["ZF-1"]["service_requests"][2]["reviewed_identity"],
            original["recorder_identity"],
        )
        changed = self.change_staff_email(self.sam)
        self.store = self.open_store()
        for after_deletion in (False, True):
            if after_deletion:
                with self.store.lock:
                    case = self.store._case("ZF-1")
                    case["resident"]["first_contact_at"] = "2020-01-01"
                    self.store.save()
                with patch.object(controls, "today", return_value="2026-10-18"):
                    self.store.approve_retention_deletion(
                        self.pam, "ZF-1", "resident-decisions", today=date(2026, 10, 18)
                    )
                self.store.resident_action(
                    self.rex,
                    "ZF-1",
                    dict(
                        action="scope_record",
                        measure=MEASURES[0],
                        design_version=1,
                        scope="SYN recreated",
                        source="SYN",
                    ),
                )
                self.store.resident_action(
                    self.rex,
                    "ZF-1",
                    dict(
                        action="decision_record",
                        measure=MEASURES[0],
                        context_revision=1,
                        status="Accepted",
                        answered_by="The resident",
                        source="SYN recreated version one",
                    ),
                )
                self.store = self.open_store()
                self.assertEqual(
                    self.store.cases["ZF-1"]["measure_decisions"][MEASURES[0]][0]["version"], 1
                )
            for request_id in ("SR-1", "SR-2", "SR-3"):
                with self.subTest(after_deletion=after_deletion, request=request_id):
                    self.unchanged_failure(
                        partial(
                            self.store.resident_action,
                            self.pam,
                            "ZF-1",
                            dict(
                                action="service_reassign",
                                id=request_id,
                                expected_version=1,
                                responsibility="redress",
                                owner=changed["email"],
                                note="SYN",
                            ),
                        )
                    )
        self.unchanged_failure(
            lambda: self.store.resident_action(
                self.pam,
                "ZF-1",
                dict(
                    action="service_reassign",
                    id="SR-2",
                    expected_version=1,
                    responsibility="redress",
                    owner=self.rex["email"],
                    note="SYN cannot adopt recreated recorder",
                ),
            )
        )
        self.store.resident_action(
            self.pam,
            "ZF-1",
            dict(
                action="service_reassign",
                id="SR-1",
                expected_version=1,
                responsibility="redress",
                owner=self.rex["email"],
                note="SYN distinct from original, even after deletion",
            ),
        )
        self.store.resident_action(
            self.pam,
            "ZF-1",
            dict(
                action="service_reassign",
                id="SR-2",
                expected_version=1,
                responsibility="service",
                owner=changed["email"],
                note="SYN unrelated handler reassignment remains possible",
            ),
        )
        requests = self.store.detail("ZF-1", self.pam)["service_requests"]
        self.assertEqual(requests[0]["reviewed_identity"], original["recorder_identity"])
        self.assertEqual(requests[0]["reviewed_identity_status"], "Known")
        self.assertNotIn("reviewed_identity", requests[1])
        self.assertEqual(requests[1]["reviewed_identity_status"], "Unknown")
        self.assertEqual(requests[0]["remedy"]["status"], "Open")

    def test_legacy_recorder_unknown_never_backfilled_or_blocks_unrelated_service(self) -> None:
        self.scope()
        self.answer()
        original = copy.deepcopy(self.store.cases["ZF-1"]["measure_decisions"][MEASURES[0]][0])
        for unknown in (None, {}, "invalid", {"email": self.sam["email"]}, {"code": " "}):
            with self.subTest(unknown=unknown):
                with self.store.lock:
                    decision = self.store._case("ZF-1")["measure_decisions"][MEASURES[0]][0]
                    if unknown is None:
                        decision.pop("recorder_identity", None)
                    else:
                        decision["recorder_identity"] = unknown
                    self.store.save()
                self.store = self.open_store()
                before = copy.deepcopy(self.store.cases["ZF-1"]["measure_decisions"])
                self.assertEqual(
                    self.store.detail("ZF-1", self.sam)["measure_decisions"][0]["versions"][0][
                        "recorder_identity_status"
                    ],
                    "Unknown",
                )
                self.unchanged_failure(
                    lambda: self.store.resident_action(
                        self.pam, "ZF-1", self.review_body(reviewed_identity=dict(self.sam))
                    )
                )
                self.assertEqual(self.store.cases["ZF-1"]["measure_decisions"], before)
        # Today's owner of the historical email cannot become historical evidence.
        rebound = dict(self.rex, email=self.sam["email"])
        self.register_followup_actor(rebound)
        self.unchanged_failure(
            lambda: self.store.resident_action(self.pam, "ZF-1", self.review_body())
        )
        for route in ("Service request", "Complaint"):
            self.store.resident_action(self.pam, "ZF-1", self.review_body(route=route))
        self.register_followup_actor(self.sam)
        self.answer()
        self.assertEqual(
            self.store.cases["ZF-1"]["measure_decisions"][MEASURES[0]][0]["recorded_by_email"],
            original["recorded_by_email"],
        )
        self.assertEqual(
            self.store.cases["ZF-1"]["measure_decisions"][MEASURES[0]][0]["recorder_identity"],
            {"code": " "},
        )

    def test_historical_recorder_identity_projection_and_model_canary(self) -> None:
        self.sam["oid"] = "SYN-PRIVATE-RECORDER-IDENTITY-CANARY"
        self.register_followup_actor(self.sam)
        self.scope()
        self.answer()
        self.store.resident_action(self.pam, "ZF-1", self.review_body())
        before = copy.deepcopy(self.store.cases["ZF-1"])
        for role in projection.STAFF_ROLES + ("Contractor",):
            user = dict(self.kim, role=role)
            detail = self.store.detail("ZF-1", user)
            if role in controls.RESIDENT_VIEW_ROLES:
                self.assertIn(self.sam["oid"], json.dumps(detail))
            else:
                self.assertNotIn(self.sam["oid"], json.dumps(detail))
                self.assertNotIn('recorder_identity"', json.dumps(detail))
                self.assertNotIn('reviewed_identity"', json.dumps(detail))
        self.assertNotIn(self.sam["oid"], self.store._facts(before))
        self.assertNotIn(self.sam["oid"], json.dumps(list(self.store.audit_entries())))
        self.assertEqual(self.store.cases["ZF-1"], before)
        self.assertEqual(self.open_store().cases["ZF-1"], before)

    def test_response_reassignment_status_clock_follows_responsibility_not_shared_person(
        self,
    ) -> None:
        self.scope()
        self.answer()
        for route in ("Service request", "Complaint", "Independent review"):
            service_owner = self.rae if route == "Service request" else self.sam
            for status in ("Open", "Closed"):
                for responsibility in ("service", "redress"):
                    for legacy in (False, True):
                        with self.subTest(
                            route=route, status=status, responsibility=responsibility, legacy=legacy
                        ):
                            self.store.resident_action(
                                self.pam,
                                "ZF-1",
                                dict(
                                    action="service_open",
                                    route=route,
                                    summary="SYN responsibility clock",
                                    desired_outcome="SYN separate remedy",
                                    service_owner=service_owner["email"],
                                    redress_owner=self.rae["email"],
                                    next_update="2099-01-01",
                                    review_measure=MEASURES[0],
                                    review_decision_version=1,
                                    review_reference="SYN recorded decision",
                                ),
                            )
                            req = self.store.cases["ZF-1"]["service_requests"][-1]
                            request_id = req["id"]
                            if status == "Closed":
                                self.store.resident_action(
                                    self.rae,
                                    "ZF-1",
                                    dict(
                                        action="service_update",
                                        id=request_id,
                                        status="Resolved",
                                        next_update="2099-01-01",
                                    ),
                                )
                                self.store.resident_action(
                                    self.rae,
                                    "ZF-1",
                                    dict(
                                        action="service_close",
                                        id=request_id,
                                        note="SYN response only",
                                    ),
                                )
                            if legacy:
                                with self.store.lock:
                                    req = self.store._case("ZF-1")["service_requests"][-1]
                                    req.pop("status_owner")
                                    req.pop("status_at")
                                    self.store.save()
                            before = copy.deepcopy(self.store.cases["ZF-1"]["service_requests"][-1])
                            self.store.resident_action(
                                self.pam,
                                "ZF-1",
                                dict(
                                    action="service_reassign",
                                    id=request_id,
                                    expected_version=before["version"],
                                    responsibility=responsibility,
                                    owner=self.rex["email"],
                                    note="SYN explicit responsibility",
                                ),
                            )
                            current = self.open_store().cases["ZF-1"]["service_requests"][-1]
                            status_key = (
                                "redress"
                                if status == "Closed" or route == "Independent review"
                                else "service"
                            )
                            if responsibility == status_key:
                                self.assertEqual(
                                    current["status_owner"]["email"], self.rex["email"]
                                )
                                self.assertNotEqual(current["status_at"], before.get("status_at"))
                                self.assertEqual(current["status_at"], current["history"][-1]["at"])
                            else:
                                for field in ("status_owner", "status_at"):
                                    self.assertEqual(current.get(field), before.get(field))
                                    self.assertEqual(field in current, field in before)
                            other = "redress" if responsibility == "service" else "service"
                            for suffix in ("_owner", "_owner_email", "_identity"):
                                self.assertEqual(current[other + suffix], before[other + suffix])
                            self.assertEqual(
                                current[responsibility + "_identity"]["email"], self.rex["email"]
                            )
                            self.assertEqual(current["remedy"], before["remedy"])
                            self.assertEqual(current["opened_at"], before["opened_at"])
                            self.assertEqual(current["status"], before["status"])
                            self.assertEqual(current["version"], before["version"] + 1)
                            self.assertEqual(current["history"][:-1], before["history"])
                            self.assertEqual(
                                current["history"][-1]["old_status_owner"],
                                before.get("status_owner"),
                            )
                            self.assertEqual(
                                current["history"][-1]["old_status_at"], before.get("status_at")
                            )
                            self.assertTrue(self.store.verify_audit())

    def test_departed_response_owners_explicit_recovery_keeps_other_clocks(self) -> None:
        self.request()
        original = copy.deepcopy(self.store.cases["ZF-1"]["service_requests"][0])
        self.register_followup_actor(dict(self.sam, role="Contractor"))
        for actor in (self.pam, self.rae):
            self.unchanged_failure(
                partial(
                    self.store.resident_action,
                    actor,
                    "ZF-1",
                    dict(
                        action="service_update",
                        id="SR-1",
                        status="Resolved",
                        next_update="2099-01-01",
                    ),
                )
            )
        self.store.resident_action(
            self.pam,
            "ZF-1",
            dict(
                action="service_reassign",
                id="SR-1",
                expected_version=1,
                responsibility="service",
                owner=self.rex["email"],
                note="SYN officer departure",
            ),
        )
        recovered = self.open_store().cases["ZF-1"]["service_requests"][0]
        self.assertEqual(recovered["service_identity"]["email"], self.rex["email"])
        self.assertEqual(recovered["status_owner"]["email"], self.rex["email"])
        self.assertNotEqual(recovered["status_at"], original["status_at"])
        self.assertEqual(recovered["remedy"], original["remedy"])
        event = recovered["history"][-1]
        self.assertEqual(event["changes"]["old"], original["service_identity"])
        self.assertEqual(event["changes"]["new"], recovered["service_identity"])
        self.assertEqual(event["actor"]["email"], self.pam["email"])
        self.assertEqual(event["note"], "SYN officer departure")
        self.assertEqual(event["old_status_at"], original["status_at"])
        self.store.resident_action(
            self.rex,
            "ZF-1",
            dict(action="service_update", id="SR-1", status="Resolved", next_update="2099-01-01"),
        )
        self.store.resident_action(
            self.rae, "ZF-1", dict(action="service_close", id="SR-1", note="SYN response")
        )
        closed = copy.deepcopy(self.store.cases["ZF-1"]["service_requests"][0])
        self.register_followup_actor(dict(self.rae, role="Quality Inspector"))
        self.store.resident_action(
            self.pam,
            "ZF-1",
            dict(
                action="service_reassign",
                id="SR-1",
                expected_version=closed["version"],
                responsibility="redress",
                owner=self.pam["email"],
                note="SYN reviewer departure",
            ),
        )
        current = self.store.cases["ZF-1"]["service_requests"][0]
        self.assertEqual(current["status"], "Closed")
        self.assertEqual(current["history"][-1]["changes"]["old"], original["redress_identity"])
        self.store.resident_action(
            self.pam,
            "ZF-1",
            dict(
                action="service_reopen",
                id="SR-1",
                expected_version=current["version"],
                note="SYN reopen",
            ),
        )
        self.store.resident_action(
            self.rex,
            "ZF-1",
            dict(action="service_update", id="SR-1", status="Resolved", next_update="2099-01-01"),
        )
        self.store.resident_action(
            self.pam, "ZF-1", dict(action="service_close", id="SR-1", note="SYN second response")
        )
        final = self.open_store().cases["ZF-1"]["service_requests"][0]
        self.assertEqual(final["status_owner"]["email"], self.pam["email"])
        self.assertEqual(final["remedy"], original["remedy"])
        self.assertEqual(final["opened_at"], original["opened_at"])
        self.assertEqual(final["history"][: len(closed["history"])], closed["history"])
        self.assertTrue(self.store.verify_audit())

    def test_response_reassignment_requires_current_manager_version_and_independence(self) -> None:
        self.request()
        body = dict(
            action="service_reassign",
            id="SR-1",
            expected_version=1,
            responsibility="service",
            owner=self.rex["email"],
            note="SYN recovery",
        )
        for actor, changes in (
            (self.sam, {}),
            (self.kim, {}),
            (self.pam, {"expected_version": 0}),
            (self.pam, {"expected_version": True}),
            (self.pam, {"owner": ""}),
            (self.pam, {"owner": "unknown@example.test"}),
            (self.pam, {"owner": self.kim["email"]}),
            (self.pam, {"owner": self.rae["email"]}),
            (self.pam, {"note": ""}),
            (self.pam, {"responsibility": "remedy"}),
        ):
            with self.subTest(actor=actor["code"], changes=changes):
                self.unchanged_failure(
                    partial(self.store.resident_action, actor, "ZF-1", dict(body, **changes))
                )
        self.register_followup_actor(dict(self.pam, role="Contractor"))
        self.unchanged_failure(lambda: self.store.resident_action(self.pam, "ZF-1", body))
        self.register_followup_actor(self.pam)
        self.scope()
        self.answer()
        self.action(
            "service_open",
            route="Independent review",
            summary="SYN review",
            desired_outcome="SYN independent response",
            service_owner=self.rex["email"],
            redress_owner=self.rae["email"],
            next_update="2099-01-01",
            review_measure=MEASURES[0],
            review_decision_version=1,
            review_reference="SYN decision",
        )
        review_body = dict(body, id="SR-2", responsibility="redress")
        for owner in (self.sam["email"], self.rex["email"]):
            self.unchanged_failure(
                partial(
                    self.store.resident_action, self.pam, "ZF-1", dict(review_body, owner=owner)
                )
            )
        self.register_followup_actor(dict(self.rae, role="Contractor"))
        self.store.resident_action(self.pam, "ZF-1", dict(review_body, owner=self.pam["email"]))
        review = self.store.cases["ZF-1"]["service_requests"][1]
        self.assertEqual(review["status_owner"]["email"], self.pam["email"])
        self.unchanged_failure(
            lambda: self.store.resident_action(
                self.rex,
                "ZF-1",
                dict(
                    action="service_update", id="SR-2", status="Resolved", next_update="2099-01-01"
                ),
            )
        )
        for action, changes in (
            ("service_update", dict(status="Resolved", next_update="2099-01-01")),
            ("service_close", dict(note="SYN independent outcome")),
            ("service_reopen", dict(expected_version=4, note="SYN independent reopen")),
        ):
            self.store.resident_action(self.pam, "ZF-1", dict(action=action, id="SR-2", **changes))
        self.assertEqual(
            self.store.cases["ZF-1"]["service_requests"][1]["status_owner"]["email"],
            self.pam["email"],
        )
        with self.store.lock:
            req = self.store._case("ZF-1")["service_requests"][0]
            req.pop("service_identity")
            req.pop("status_owner")
            req.pop("status_at")
            self.store.save()
        self.store.resident_action(self.pam, "ZF-1", body)
        event = self.open_store().cases["ZF-1"]["service_requests"][0]["history"][-1]
        self.assertIsNone(event["changes"]["old"])
        self.assertEqual(event["old_owner_email"], self.sam["email"])
        self.assertIsNone(event["old_status_at"])
        self.assertEqual(event["changes"]["new"]["email"], self.rex["email"])

    def test_complete_update_and_explicit_reassignment_preserve_history(self) -> None:
        self.commitment()
        first = copy.deepcopy(self.store.cases["ZF-1"]["resident_update"])
        self.commitment(expected_version=1, owner=self.rae["email"], status="Proposed")
        update = self.open_store().detail("ZF-1")["resident_update"]
        self.assertEqual(update["version"], 2)
        self.assertEqual(update["owner_identity"]["email"], self.rae["email"])
        first.pop("history")
        self.assertEqual(update["history"][-1]["old"], first)
        self.assertEqual(update["due_at"], "2099-01-01T12:00:00+00:00")
        self.assertNotIn("sent_at", update)
        self.assertNotIn("completed_at", update)
        self.assertEqual(update["basis"], "SYN human-selected fixture date")
        self.unchanged_failure(lambda: self.commitment(expected_version=1))
        self.unchanged_failure(lambda: self.commitment(expected_version=2))
        self.assertTrue(self.store.verify_audit())

    def test_incomplete_commitments_dates_and_identity_fail_without_mutation(self) -> None:
        for field, value in (
            ("purpose", ""),
            ("basis", ""),
            ("owner", "missing@example.test"),
            ("due_at", "2099-01-01"),
            ("due_at", "2099-02-30T12:00:00Z"),
            ("expected_version", True),
            ("status", "Sent"),
        ):
            with self.subTest(field=field, value=value):
                self.unchanged_failure(partial(self.commitment, **{field: value}))
        self.unchanged_failure(
            lambda: self.store.resident_action(
                dict(self.sam, oid="SYN-forged"), "ZF-1", dict(action="update_record")
            )
        )
        self.unchanged_failure(
            lambda: self.action(
                "service_open",
                route="Complaint",
                service_owner=self.sam["email"],
                redress_owner=self.rae["email"],
                summary="SYN",
                desired_outcome="SYN",
                next_update="2099-02-30",
            )
        )

    def test_response_and_remedy_close_and_reopen_are_independent(self) -> None:
        self.request()
        original = copy.deepcopy(self.store.cases["ZF-1"]["service_requests"][0]["remedy"])
        self.action("service_update", id="SR-1", status="Resolved", next_update="2099-01-01")
        self.store.resident_action(
            self.rae, "ZF-1", dict(action="service_close", id="SR-1", note="SYN response")
        )
        req = self.open_store().cases["ZF-1"]["service_requests"][0]
        self.assertEqual(req["status"], "Closed")
        self.assertEqual(req["remedy"], original)
        self.assertEqual(req["status_owner"]["email"], self.rae["email"])
        self.assertTrue(req["status_at"])
        self.unchanged_failure(
            lambda: self.action(
                "remedy_update", id="SR-1", expected_version=1, status="Resolved", note="SYN"
            )
        )
        for version, status in ((1, "Resolved"), (2, "Closed"), (3, "Open")):
            self.store.resident_action(
                self.rae,
                "ZF-1",
                dict(
                    action="remedy_update",
                    id="SR-1",
                    expected_version=version,
                    status=status,
                    note="SYN remedy",
                ),
            )
            current = self.open_store().cases["ZF-1"]["service_requests"][0]
            self.assertEqual(current["status"], "Closed")
            self.assertEqual(current["remedy"]["opened_at"], original["opened_at"])
            self.assertEqual(current["remedy"]["status"], status)
        remedy = copy.deepcopy(current["remedy"])
        self.action("service_reopen", id="SR-1", expected_version=3, note="SYN response only")
        self.assertEqual(self.store.cases["ZF-1"]["service_requests"][0]["remedy"], remedy)
        self.assertEqual(self.store.cases["ZF-1"]["service_requests"][0]["status"], "Open")

    def test_legacy_confirmation_preserves_unknown_history_and_closed_response(self) -> None:
        with self.store.lock:
            c = self.store._case("ZF-1")
            c["resident_update"] = dict(owner="Legacy unknown person", due_at=None)
            c["service_requests"] = [
                dict(
                    id="SR-1",
                    route="Complaint",
                    status="Closed",
                    service_owner="Old",
                    service_owner_email="absent@example.test",
                    redress_owner="Old",
                    redress_owner_email="absent@example.test",
                    history=[],
                )
            ]
            self.store.save()
        old = copy.deepcopy(self.store.cases["ZF-1"]["resident_update"])
        projected = self.store.detail("ZF-1")
        self.assertIsNone(projected["service_requests"][0]["remedy"]["opened_at"])
        self.assertEqual(projected["service_requests"][0]["remedy"]["status"], "Unknown")
        self.unchanged_failure(
            lambda: self.action(
                "remedy_update", id="SR-1", expected_version=0, status="Resolved", note="SYN"
            )
        )
        self.commitment()
        update = self.store.cases["ZF-1"]["resident_update"]
        self.assertEqual(update["history"][0]["old"], old)
        self.assertIsNone(update["opened_at"])
        self.store.resident_action(
            self.pam,
            "ZF-1",
            dict(
                action="remedy_confirm",
                id="SR-1",
                expected_version=0,
                owner=self.rae["email"],
                basis="SYN new responsibility",
            ),
        )
        req = self.open_store().detail("ZF-1")["service_requests"][0]
        self.assertEqual(req["status"], "Closed")
        self.assertIsNone(req["status_owner"])
        self.assertIsNone(req["status_at"])
        self.assertIsNone(req["remedy"]["opened_at"])
        self.assertEqual(req["remedy"]["history"][0]["old"], None)
        self.unchanged_failure(
            lambda: self.store.resident_action(
                self.pam,
                "ZF-1",
                dict(
                    action="remedy_confirm",
                    id="SR-1",
                    expected_version=0,
                    owner=self.rae["email"],
                    basis="SYN",
                ),
            )
        )

    def test_actionable_owner_roles_projection_and_captured_identity(self) -> None:
        self.unchanged_failure(lambda: self.commitment(owner=self.kim["email"]))
        self.unchanged_failure(lambda: self.commitment(owner=self.rex["role"]))
        self.commitment()
        self.request()
        for actor in (self.sam, self.pam, self.rae):
            self.assertIn("resident_update", self.store.detail("ZF-1", actor))
        self.assertNotIn("resident_update", self.store.detail("ZF-1", self.kim))
        self.assertNotIn("service_requests", self.store.detail("ZF-1", self.kim))
        self.assertNotIn("SYN update about remedy", self.store._facts(self.store.cases["ZF-1"]))
        # A current manager may explicitly take responsibility, not impersonate the old owner.
        self.store.resident_action(
            self.pam,
            "ZF-1",
            dict(
                action="remedy_update",
                id="SR-1",
                expected_version=1,
                status="In progress",
                owner=self.sam["email"],
                note="SYN reassign",
            ),
        )
        req = self.store.cases["ZF-1"]["service_requests"][0]
        self.assertEqual(req["remedy"]["owner"]["email"], self.sam["email"])
        self.assertEqual(req["remedy"]["history"][-1]["old"]["owner"]["email"], self.rae["email"])
        self.assertEqual(req["remedy"]["history"][-1]["actor"]["email"], self.pam["email"])

    def test_mixed_closure_clocks_survive_unrelated_transitions_and_restart(self) -> None:
        self.commitment()
        for route in ("Complaint", "Defect", "Charge query"):
            self.request(route)
        self.action("service_update", id="SR-1", status="Resolved", next_update="2099-01-01")
        self.store.resident_action(
            self.rae, "ZF-1", dict(action="service_close", id="SR-1", note="SYN response only")
        )
        expected = copy.deepcopy(self.store.cases["ZF-1"]["service_requests"])
        commitment = copy.deepcopy(self.store.cases["ZF-1"]["resident_update"])

        def retained() -> None:
            case = self.open_store().detail("ZF-1")
            self.assertEqual(case["service_requests"], expected)
            self.assertEqual(case["resident_update"], commitment)
            self.assertEqual(case["service_requests"][0]["status"], "Closed")
            self.assertEqual(case["service_requests"][0]["remedy"]["status"], "Open")

        for measure in MEASURES:
            self.scope(measure)
            self.answer(measure)
        pid = self.package()
        wid = self.store.issue_work_order(
            self.pam, pid, "ZF-1", resident_bindings=self.bind(MEASURES[0])
        )
        supplied_appointment_fixture(self.store, self.pam, wid)
        self.store.record_wo_appointment(self.pam, wid, "Booked", "2099-01-01")
        self.store.complete_work_order(self.pam, wid, "SYN physical completion only")
        order = self.store._work_order(wid)
        self.assertEqual(order["completed_by"], self.pam["name"])
        self.assertTrue(order["completed_at"])
        retained()
        for index, measure in enumerate(MEASURES):
            self.store.submit_quality(
                self.sam,
                "ZF-1",
                measure,
                "Synthetic installer",
                "Installer",
                {label: "SYN evidence" for label in checklist_for(measure)["items"]},
                context_revision=1,
            )
            if index == 0:
                self.store.accept_quality(self.pam, "ZF-1", index)
                self.store.hand_over_quality(self.pam, "ZF-1", index, "SYN guarantees", True)
                handed = self.store.cases["ZF-1"]["quality"][0]["handover"]
                self.assertEqual(handed["by"], self.pam["name"])
                self.assertTrue(handed["at"])
            else:
                self.store.return_quality(
                    self.pam, "ZF-1", index, "SYN return", "SYN defect", self.rae["name"]
                )
                defect = copy.deepcopy(self.store.cases["ZF-1"]["quality"][index]["defect"])
                self.assertEqual(defect["owner"], self.rae["name"])
                self.assertTrue(defect["raised_at"])
            retained()
        self.store.finance_action(
            self.pam,
            "ZF-1",
            dict(
                action="invoice_receive",
                supplier="Test Ltd",
                work_order=wid,
                ref="SYN-INV",
                kind="Invoice",
                lines=[dict(measure=MEASURES[0], quantity=1, amount=10, milestone_ref="SYN")],
            ),
        )
        self.store.finance_action(
            self.pam, "ZF-1", dict(action="payment_status", id="INV-1", status="Not payable yet")
        )
        invoice = self.store.cases["ZF-1"]["finance"]["invoices"][0]
        self.assertEqual(invoice["payment_status_owner"]["email"], self.pam["email"])
        self.assertTrue(invoice["payment_status_at"])
        retained()
        with self.store.lock:
            self.store._case("ZF-1").update(stage="Completed", closed=True)
            self.store.save()
        self.store.reopen_case(
            self.pam,
            "ZF-1",
            "SYN reopening",
            metadata=dict(source="SYN", next_action="SYN aftercare"),
        )
        retained()
        self.store.return_case(
            self.sam,
            "ZF-1",
            "Contacting resident",
            "SYN return",
            metadata=dict(source="SYN", next_action="SYN next action"),
        )
        retained()
        self.assertEqual(self.open_store().cases["ZF-1"]["quality"][1]["defect"], defect)
        self.store.resident_action(
            self.rae,
            "ZF-1",
            dict(
                action="remedy_update",
                id="SR-3",
                expected_version=1,
                status="Resolved",
                note="SYN charge query progress",
            ),
        )
        current = self.open_store().cases["ZF-1"]["service_requests"]
        self.assertEqual(current[:2], expected[:2])
        self.assertEqual(current[2]["status"], "Open")
        self.assertEqual(current[2]["remedy"]["status"], "Resolved")

    def test_handoff_cannot_create_partial_commitment_or_clear_existing_one(self) -> None:
        from dataset import change_metadata

        before = copy.deepcopy(self.store.cases["ZF-1"])
        with self.assertRaises(ValueError):
            self.store.offer_handoff(
                self.sam,
                "ZF-1",
                self.rae["email"],
                metadata={
                    **change_metadata(self.store, "ZF-1"),
                    "resident_update_to": self.sam["email"],
                },
            )
        self.assertEqual(self.store.cases["ZF-1"], before)
        self.assertEqual(list(self.store.audit_entries())[-1]["action"], "handoff_offered_rejected")
        self.commitment()
        expected = copy.deepcopy(self.store.cases["ZF-1"]["resident_update"])
        self.store.offer_handoff(
            self.sam,
            "ZF-1",
            self.rae["email"],
            metadata=change_metadata(self.store, "ZF-1"),
        )
        self.store.receive_handoff(self.rae, "ZF-1")
        self.store.decline_handoff(self.rae, "ZF-1", "SYN return to sender")
        self.assertEqual(self.open_store().cases["ZF-1"]["resident_update"], expected)
        denied = self.store.detail("ZF-1", dict(self.rex, role="Quality Inspector"))
        self.assertNotIn("SYN human-selected fixture date", json.dumps(denied))

    def test_json_followup_failure_restores_record_and_ledger(self) -> None:
        if self.sql:
            self.skipTest("JSON file rollback only")
        self.commitment()
        before = copy.deepcopy(self.store.cases["ZF-1"])
        audit = list(self.store.audit_entries())
        for target in ("save", "audit"):
            with self.subTest(target=target):
                original = getattr(self.store, target)

                def failed(
                    *args: Any,
                    target: str = target,
                    original: Callable[..., Any] = original,
                    **kwargs: Any,
                ) -> None:
                    if target == "audit":
                        original(*args, **kwargs)
                    raise OSError("SYN persistence fault")

                with patch.object(self.store, target, side_effect=failed):
                    with self.assertRaises(OSError):
                        self.commitment(expected_version=1)
                self.assertEqual(self.open_store().cases["ZF-1"], before)
                self.assertEqual(list(self.store.audit_entries()), audit)
                self.assertTrue(self.store.verify_audit())

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
        self.unchanged_failure(
            lambda: self.store.submit_quality(
                self.sam,
                "ZF-1",
                MEASURES[1],
                "Synthetic installer",
                "Installer",
                {label: "Synthetic evidence" for label in checklist_for(MEASURES[1])["items"]},
            )
        )

    def test_detached_projection_persistence_audit_and_model_minimisation(self) -> None:
        self.scope()
        self.action("safe_contact_record", safe_contact_ref="SYN-SAFE-CANARY", source="SYN")
        self.authority()
        self.answer(answered_by="Their representative", representative_ref="SYN-REP-A")
        before = copy.deepcopy(self.store.cases["ZF-1"])
        audit = list(self.store.audit_entries())
        for actor in (self.sam, self.pam, self.rex, self.kim):
            detail = self.store.detail("ZF-1", actor)
            if actor == self.kim:
                text = json.dumps(detail)
                for sentinel in ("SYN-AUTH-CANARY", "SYN-WISHES-CANARY", "SYN-SOURCE-CANARY"):
                    self.assertNotIn(sentinel, text)
            self.assertEqual(self.store.cases["ZF-1"], before)
        with patch.dict("os.environ", {"ZF_REASON_ROLES": "Retrofit Coordinator"}):
            detail = self.store.detail("ZF-1", self.sam)
            self.assertIn("representative_authorities", detail)
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


@unittest.skipUnless(
    os.environ.get("ZF_RESIDENT_AZURE_TEST") == "1",
    "Explicit isolated synthetic Azure SQL database required",
)
class AzureResidentDecisions(unittest.TestCase):
    def test_synthetic_sqlstore_persistence_permissions_retention_and_audit(self) -> None:
        from datetime import date

        from zava_forward.core.mssqlstore import MssqlStore
        from zava_forward.core.resident_decisions import retention_schedule

        self.assertTrue(os.environ["ZF_SQL_DATABASE"].startswith("resident86test"))
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "synthetic.json"
            data = copy.deepcopy(DATA)
            data["cases"][0]["contacts"] = [
                dict(
                    at="2021-10-17T10:00",
                    channel="Phone",
                    outcome="SYN",
                    note="SYN",
                    by="Sam Example",
                )
            ]
            coordinator = dict(
                code="RC-86",
                name="Synthetic Coordinator",
                email="rc86@example.test",
                role="Retrofit Coordinator",
            )
            contractor = dict(
                code="CON-86",
                name="Synthetic Contractor",
                email="con86@example.test",
                role="Contractor",
                contractor="Test Ltd",
            )
            data["staff"].extend([coordinator, contractor])
            path.write_text(json.dumps(data))
            store = MssqlStore(str(path), state_dir=root)
            self.addCleanup(store.db.close)
            self.assertIsInstance(store, SqlStore)
            self.assertEqual(len(store.cases), len(DATA["cases"]))
            sam, manager = data["staff"][:2]
            store.technical_action(manager, "ZF-1", dict(action="design_submit", note="SYN"))

            def action(name: str, **body: Any) -> None:
                store.resident_action(sam, "ZF-1", dict(action=name, **body))

            action(
                "scope_record",
                measure="Loft insulation",
                design_version=1,
                scope="SYN-SCOPE",
                source="SYN",
            )
            action("safe_contact_record", safe_contact_ref="SYN-SAFE", source="SYN")
            binding = dict(measure="Loft insulation", context_revision=1)
            action(
                "representative_record",
                **binding,
                representative_ref="SYN-REP",
                status="Confirmed",
                tasks=["Works decision", "Receive information"],
                authority_date="2026-01-01",
                review_date="2027-01-01",
                safe_contact_ref="SYN-SAFE",
                source="SYN-AUTH",
                resident_wishes="SYN-WISHES",
            )
            answer = dict(**binding, status="Accepted", answered_by="The resident", source="SYN")
            action("decision_record", **answer)
            self.assertEqual(
                store.detail("ZF-1", contractor)["resident_readiness"],
                [dict(measure="Loft insulation", flag="Proceed")],
            )
            action("decision_record", **dict(answer, status="Withdrawn", note="SYN-WITHDRAWN"))
            self.assertEqual(
                store.detail("ZF-1", contractor)["resident_readiness"],
                [dict(measure="Loft insulation", flag="Hold")],
            )
            before = copy.deepcopy(store.cases["ZF-1"])
            with self.assertRaises(PermissionError):
                store.resident_action(manager, "ZF-1", dict(action="safe_contact_record"))
            self.assertEqual(store.cases["ZF-1"], before)
            self.assertIn("SYN-WISHES", json.dumps(store.detail("ZF-1", coordinator)))
            self.assertNotIn("SYN-WISHES", json.dumps(store.detail("ZF-1", contractor)))
            reopened = MssqlStore(str(path), state_dir=root)
            self.addCleanup(reopened.db.close)
            self.assertEqual(reopened.cases["ZF-1"], before)
            with patch.object(controls, "today", return_value="2026-10-16"):
                self.assertEqual(retention_schedule(reopened.cases["ZF-1"])["due"], "2026-10-17")
                self.assertFalse(retention_schedule(reopened.cases["ZF-1"])["expired"])
            with patch.object(controls, "today", return_value="2026-10-17"):
                self.assertTrue(retention_schedule(reopened.cases["ZF-1"])["expired"])
                with self.assertRaises(ValueError):
                    reopened.resident_action(
                        sam,
                        "ZF-1",
                        dict(
                            action="disclosure_check",
                            **binding,
                            representative_ref="SYN-REP",
                            task="Receive information",
                        ),
                    )
                reopened.approve_retention_deletion(
                    manager, "ZF-1", "resident-decisions", today=date(2026, 10, 17)
                )
            final = MssqlStore(str(path), state_dir=root)
            self.addCleanup(final.db.close)
            for key in ("measure_decisions", "resident_safe_contact", "representative_authorities"):
                self.assertNotIn(key, final.cases["ZF-1"])
            self.assertNotIn("SYN-WISHES", json.dumps(final.cases["ZF-1"]))
            self.assertNotIn("first_contact_at", final.cases["ZF-1"]["resident"])
            self.assertTrue(final.verify_audit())
            mode = final.db.execute(
                "SELECT is_ledger_on FROM sys.databases WHERE name=DB_NAME()"
            ).fetchone()[0]
            print(
                json.dumps(
                    dict(
                        platform="Azure SQL",
                        ledger_mode=bool(mode),
                        current_payload_purged=True,
                        restart_verified=True,
                        audit_intact=True,
                        synthetic_only=True,
                    )
                )
            )


class SqlResidentDecisions(JsonResidentDecisions):
    sql = True

    def test_intake_writer_rechecks_actor_and_named_owner(self) -> None:
        for subject in (self.sam, self.rae):
            for body in (
                self.nomination(owner=self.rae["email"]),
                self.tenure(owner=self.rae["email"]),
            ):
                save = self.store.save

                def revoke(
                    subject: dict[str, Any] = subject, save: Callable[[], None] = save
                ) -> None:
                    other = self.store.assistant_connection()
                    try:
                        other.execute(
                            "UPDATE staff SET body=? WHERE email=?",
                            (json.dumps(dict(subject, role="Contractor")), subject["email"]),
                        )
                    finally:
                        other.close()
                    save()

                with patch.object(self.store, "save", side_effect=revoke):
                    self.unchanged_failure(
                        partial(self.store.resident_action, self.sam, "ZF-1", body)
                    )
                self.register_followup_actor(subject)
                current = self.open_store().cases["ZF-1"]
                self.assertNotIn("nomination_records", current)
                self.assertNotIn("tenure_reports", current)
                self.assertNotIn("tenure_review_required", current)

    def test_intake_competing_tenure_revision_one_durable_success(self) -> None:
        other = self.open_store()
        save = self.store.save
        body = self.tenure()

        def compete() -> None:
            other.resident_action(self.sam, "ZF-1", body)
            save()

        with patch.object(self.store, "save", side_effect=compete):
            with self.assertRaises(ConflictError):
                self.store.resident_action(self.sam, "ZF-1", body)
        current = self.open_store()
        self.assertEqual(len(current.cases["ZF-1"]["tenure_reports"]), 1)
        self.assertTrue(current.cases["ZF-1"]["tenure_review_required"])
        self.assertEqual(
            sum(e["action"] == "resident_tenure_intake" for e in current.audit_entries()), 1
        )

    def test_intake_committed_acknowledgement_failure_is_truthful(self) -> None:
        save = self.store.save

        def committed() -> None:
            save()
            raise OSError("SYN postcommit acknowledgement")

        with (
            patch.object(self.store, "save", side_effect=committed),
            self.assertLogs("zava_forward.core.resident_decisions", level="ERROR"),
            self.assertRaises(resident_decisions.ResidentCommittedError),
        ):
            self.store.resident_action(self.sam, "ZF-1", self.nomination())
        current = self.open_store()
        self.assertEqual(len(current.cases["ZF-1"]["nomination_records"]), 1)
        self.assertEqual(
            sum(e["action"] == "resident_nomination_record" for e in current.audit_entries()), 1
        )

    store: SqlStore

    def test_challenge_adjacent_release_denial_is_persisted_without_disposition(self) -> None:
        for action in ("accept", "edit"):
            proposal = self.priority_fixture()
            with self.store.lock:
                record = next(
                    r for r in self.store.data["recommendations"] if r["id"] == proposal["id"]
                )
                record.update(source="ai", model=self.store.ai.strong)
                record.pop("release", None)
                self.store.save()
            before = copy.deepcopy(record)
            audit = list(self.store.audit_entries())
            with self.assertRaises(PermissionError):
                self.store.resolve_priority(
                    self.sam, proposal["id"], action, "SYN", proposal["items"]
                )
            reopened = self.open_store()
            events = list(reopened.audit_entries())[len(audit) :]
            self.assertEqual([entry["action"] for entry in events], ["ai_release_denied"])
            self.assertIn(proposal["id"], events[0]["detail"])
            self.assertEqual(
                next(r for r in reopened.data["recommendations"] if r["id"] == proposal["id"]),
                before,
            )
            self.assertTrue(reopened.verify_audit())

    def test_challenge_correction_flag_tracks_committed_resolution_and_rollback(self) -> None:
        proposal = self.priority_fixture()
        self.store.resident_action(self.sam, "ZF-1", self.challenge_body(proposal))
        self.resolve_challenge(correction=False)
        self.assertEqual(
            self.store.db.execute(
                "SELECT priority_correction FROM cases WHERE id='ZF-1'"
            ).fetchone()[0],
            0,
        )
        self.store.resident_action(self.sam, "ZF-1", self.challenge_body(proposal, "policy"))
        append = self.store._append_audit
        with patch.object(self.store, "_append_audit", side_effect=RuntimeError("SYN rollback")):
            with self.assertRaisesRegex(RuntimeError, "SYN rollback"):
                self.resolve_challenge("CH-2")
        self.assertEqual(
            self.store.db.execute(
                "SELECT priority_correction FROM cases WHERE id='ZF-1'"
            ).fetchone()[0],
            0,
        )
        self.assertEqual(self.store._priority_correction_rows(), [])
        self.assertEqual(self.store._append_audit, append)
        self.resolve_challenge("CH-2")
        reopened = self.open_store()
        assert isinstance(reopened, SqlStore)
        self.assertEqual(
            reopened.db.execute("SELECT priority_correction FROM cases WHERE id='ZF-1'").fetchone()[
                0
            ],
            1,
        )
        self.assertEqual(
            reopened._priority_correction_rows(),
            [
                (
                    "ZF-1",
                    "CH-2",
                    dict(kind="policy", id="priority-ranking", version=proposal["policy_version"]),
                )
            ],
        )

    def test_challenge_correction_flag_migrates_existing_cases(self) -> None:
        proposal = self.priority_fixture()
        self.store.resident_action(self.sam, "ZF-1", self.challenge_body(proposal))
        self.resolve_challenge()
        if type(self.store) is SqlStore:
            self.store.db.execute("DROP INDEX ix_cases_priority_correction")
        else:
            self.store.db.execute("DROP INDEX ix_cases_priority_correction ON cases")
            constraint = self.store.db.execute("""
                SELECT d.name FROM sys.default_constraints AS d
                JOIN sys.columns AS c ON c.object_id=d.parent_object_id
                    AND c.column_id=d.parent_column_id
                WHERE d.parent_object_id=OBJECT_ID(N'cases') AND c.name='priority_correction'
            """).fetchone()
            self.assertIsNotNone(constraint)
            self.store.db.execute(f"ALTER TABLE cases DROP CONSTRAINT [{constraint[0]}]")
        self.store.db.execute("ALTER TABLE cases DROP COLUMN priority_correction")
        before = self.store.db.execute(
            "SELECT id, rowversion, seq, body FROM cases ORDER BY id"
        ).fetchall()
        with patch.object(type(self.store), "_row", side_effect=RuntimeError("SYN backfill")):
            with self.assertRaisesRegex(RuntimeError, "SYN backfill"):
                self.open_store()
        self.assertNotIn("priority_correction", self.store._columns())
        self.assertEqual(
            self.store.db.execute(
                "SELECT id, rowversion, seq, body FROM cases ORDER BY id"
            ).fetchall(),
            before,
        )
        reopened = self.open_store()
        assert isinstance(reopened, SqlStore)
        self.assertEqual(
            reopened.db.execute(
                "SELECT id, rowversion, seq, body FROM cases ORDER BY id"
            ).fetchall(),
            before,
        )
        self.assertEqual(
            reopened.db.execute("SELECT priority_correction FROM cases WHERE id='ZF-1'").fetchone()[
                0
            ],
            1,
        )
        self.assertEqual(len(reopened._priority_correction_rows()), 1)

    def test_challenge_accept_edit_writer_race_refuses_after_other_store_correction(self) -> None:
        for action in ("accept", "edit"):
            proposal = self.priority_fixture()
            self.store.resident_action(self.sam, "ZF-1", self.challenge_body(proposal))
            record_id = self.store.cases["ZF-1"]["affected_challenges"][-1]["id"]
            other = self.open_store()
            save = self.store.save

            def correct_before_save(
                other: Any = other,
                record_id: str = record_id,
                save: Callable[[], None] = save,
            ) -> None:
                other.resident_action(
                    self.sam,
                    "ZF-1",
                    dict(
                        action="challenge_resolve",
                        id=record_id,
                        expected_version=1,
                        resolution="Correction recorded",
                        resolution_ref="SYN competing human correction",
                        explanation="SYN",
                        next_update="2099-01-02",
                    ),
                )
                save()

            with patch.object(self.store, "save", side_effect=correct_before_save):
                with self.assertRaises(PermissionError):
                    self.store.resolve_priority(
                        self.sam,
                        proposal["id"],
                        action,
                        "SYN",
                        [dict(case_id="ZF-1", reason="SYN")],
                    )
            reopened = self.open_store()
            rec = next(r for r in reopened.data["recommendations"] if r["id"] == proposal["id"])
            self.assertEqual(rec["status"], "Proposed")
            self.assertFalse(
                any(
                    e["action"] == "ai_priority_" + action and proposal["id"] in e["detail"]
                    for e in reopened.audit_entries()
                )
            )
            self.assertTrue(reopened._rec_view(rec)["stale"])
            self.assertEqual(
                self.store.resolve_priority(self.sam, proposal["id"], "reject", "SYN")["status"],
                "Rejected",
            )

    def test_challenge_open_rechecks_decision_and_owner_in_writer(self) -> None:
        proposal = self.priority_fixture()
        body = self.challenge_body(proposal)
        other = self.open_store()
        assert isinstance(other, SqlStore)
        save = self.store.save

        def review_before_save() -> None:
            other.resolve_priority(self.sam, proposal["id"], "accept")
            save()

        with patch.object(self.store, "save", side_effect=review_before_save):
            with self.assertRaises(ValueError):
                self.store.resident_action(self.sam, "ZF-1", body)
        self.assertNotIn("affected_challenges", self.open_store().cases["ZF-1"])
        body = self.challenge_body(proposal)

        def revoke_before_save() -> None:
            other.db.execute(
                "UPDATE staff SET body=? WHERE email=?",
                (json.dumps(dict(self.sam, code="SYN-revoked")), self.sam["email"]),
            )
            save()

        with patch.object(self.store, "save", side_effect=revoke_before_save):
            with self.assertRaises(PermissionError):
                self.store.resident_action(self.sam, "ZF-1", body)
        self.assertNotIn("affected_challenges", self.open_store().cases["ZF-1"])

    def test_challenge_cross_case_policy_writer_fence(self) -> None:
        first = self.priority_fixture()
        self.store.resident_action(self.sam, "ZF-1", self.challenge_body(first, "policy"))
        with self.store.lock:
            self.store._case("ZF-5")["owner_code"] = self.rae["code"]
            self.store.save()
        other_proposal = self.store.ai_priority(self.rae, mode="workflow-only")
        other = self.open_store()
        save = self.store.save

        def correct_policy() -> None:
            other.resident_action(
                self.sam,
                "ZF-1",
                dict(
                    action="challenge_resolve",
                    id="CH-1",
                    expected_version=1,
                    resolution="Correction recorded",
                    resolution_ref="SYN other-case policy",
                    explanation="SYN",
                    next_update="2099-01-02",
                ),
            )
            save()

        with patch.object(self.store, "save", side_effect=correct_policy):
            with self.assertRaises(PermissionError):
                self.store.resolve_priority(self.rae, other_proposal["id"], "accept")
        reopened = self.open_store()
        self.assertEqual(reopened.latest_priority(self.rae)["status"], "Proposed")
        self.assertTrue(reopened.latest_priority(self.rae)["stale"])

    def test_decision_snapshot_rechecks_registered_actor_in_writer_transaction(self) -> None:
        self.scope()
        save = self.store.save
        for field in ("code", "oid"):
            with self.subTest(field=field):

                def change_registry(field: str = field) -> None:
                    other = self.store.assistant_connection()
                    try:
                        other.execute(
                            "UPDATE staff SET body=? WHERE email=?",
                            (
                                json.dumps(dict(self.sam, **{field: "SYN changed"})),
                                self.sam["email"],
                            ),
                        )
                    finally:
                        other.close()
                    save()

                with patch.object(self.store, "save", side_effect=change_registry):
                    self.unchanged_failure(lambda: self.answer())
                self.register_followup_actor(self.sam)
                self.assertNotIn("measure_decisions", self.open_store().cases["ZF-1"])

    def test_response_reassignment_rechecks_writer_actor_assignee_and_version(self) -> None:
        self.request()
        body = dict(
            action="service_reassign",
            id="SR-1",
            expected_version=1,
            responsibility="service",
            owner=self.rex["email"],
            note="SYN recovery",
        )
        for subject in (self.pam, self.rex):
            for field, value in (("role", "Contractor"), ("oid", "SYN rebound identity")):
                with self.subTest(subject=subject["code"], field=field):
                    save = self.store.save

                    def change_registry(
                        subject: dict[str, Any] = subject,
                        field: str = field,
                        value: str = value,
                        save: Callable[[], None] = save,
                    ) -> None:
                        other = self.store.assistant_connection()
                        try:
                            other.execute(
                                "UPDATE staff SET body=? WHERE email=?",
                                (json.dumps(dict(subject, **{field: value})), subject["email"]),
                            )
                        finally:
                            other.close()
                        save()

                    with patch.object(self.store, "save", side_effect=change_registry):
                        self.unchanged_failure(
                            lambda: self.store.resident_action(self.pam, "ZF-1", body)
                        )
                    self.register_followup_actor(subject)
        other = self.open_store()
        save = self.store.save

        def competing_owner() -> None:
            other.resident_action(self.pam, "ZF-1", dict(body, owner=self.pam["email"]))
            save()

        with patch.object(self.store, "save", side_effect=competing_owner):
            with self.assertRaises(ConflictError):
                self.store.resident_action(self.pam, "ZF-1", body)
        current = self.open_store()
        self.assertEqual(
            current.cases["ZF-1"]["service_requests"][0]["service_identity"]["email"],
            self.pam["email"],
        )
        self.assertEqual(
            sum(e["action"] == "resident_service_reassign" for e in current.audit_entries()), 1
        )
        self.unchanged_failure(lambda: self.store.resident_action(self.pam, "ZF-1", body))

    def test_response_reassignment_faults_preserve_history_and_exactly_once_outcome(self) -> None:
        from zava_forward.core.resident_decisions import ResidentCommittedError

        self.request()
        body = dict(
            action="service_reassign",
            id="SR-1",
            expected_version=1,
            responsibility="service",
            owner=self.rex["email"],
            note="SYN recovery",
        )
        before = copy.deepcopy(self.store.cases["ZF-1"])
        for persistent in (False, True):
            audit = list(self.store.audit_entries())
            append = self.store._append_audit
            original = OSError("SYN response assignment audit failure")

            class RecoveryFault:
                armed = False
                failures = 0

                def __init__(self, db: Any, persistent: bool) -> None:
                    self.db = db
                    self.persistent = persistent

                def execute(self, sql: str, args: Any = ()) -> Any:
                    if self.armed and sql.startswith("SELECT rowversion, body FROM cases"):
                        if self.persistent or self.failures == 0:
                            self.failures += 1
                            raise OSError("SYN response assignment recovery read")
                    return self.db.execute(sql, args)

                def __getattr__(self, name: str) -> Any:
                    return getattr(self.db, name)

            fault = RecoveryFault(self.store.db, persistent)

            def failed_audit(
                entries: Any,
                append: Callable[..., Any] = append,
                fault: RecoveryFault = fault,
                original: OSError = original,
            ) -> None:
                append(entries)
                fault.armed = True
                raise original

            with self.store.lock:
                self.store.audit(self.pam["email"], "prior_assignment_event", "ZF-2", "SYN")
                prior = list(self.store.local.pending)
                with (
                    patch.object(self.store, "db", fault),
                    patch.object(self.store, "_append_audit", side_effect=failed_audit),
                    self.assertLogs("zava_forward.core.resident_decisions", level="ERROR"),
                    self.assertRaises(OSError) as caught,
                ):
                    self.store.resident_action(self.pam, "ZF-1", body)
                self.assertIs(caught.exception, original)
                self.assertEqual(self.store.local.pending, prior)
                self.assertFalse(self.store.local.touched)
            current = self.open_store()
            self.assertEqual(current.cases["ZF-1"], before)
            self.assertEqual(
                [e["action"] for e in current.audit_entries()],
                [e["action"] for e in audit] + ["prior_assignment_event"],
            )
        other = self.open_store()
        save, sync = self.store.save, self.store._sync
        armed = False

        def committed_save() -> None:
            nonlocal armed
            other.log_call(self.sam, "ZF-2", "SYN", "SYN different writer")
            armed = True
            save()

        def unavailable_sync() -> None:
            if armed:
                raise OSError("SYN response assignment committed sync")
            sync()

        with self.store.lock:
            self.store.audit(self.pam["email"], "committed_assignment_prefix", "ZF-2", "SYN")
            with (
                patch.object(self.store, "save", side_effect=committed_save),
                patch.object(self.store, "_sync", side_effect=unavailable_sync),
                self.assertLogs("zava_forward.core.resident_decisions", level="ERROR"),
                self.assertRaises(ResidentCommittedError) as caught_committed,
            ):
                self.store.resident_action(self.pam, "ZF-1", body)
            self.assertIsInstance(caught_committed.exception.__cause__, OSError)
            self.assertFalse(self.store.local.pending)
        current = self.open_store()
        self.assertEqual(current.cases["ZF-1"]["service_requests"][0]["version"], 2)
        audit = list(current.audit_entries())
        self.store.save()
        self.assertEqual(list(self.store.audit_entries()), audit)
        self.assertEqual(sum(e["action"] == "resident_service_reassign" for e in audit), 1)
        self.assertEqual(sum(e["action"] == "committed_assignment_prefix" for e in audit), 1)
        self.assertTrue(current.verify_audit())

    def test_followup_writer_rechecks_current_actor_assignee_and_legacy_identity(self) -> None:
        assert isinstance(self.store, SqlStore)
        for subject in (self.sam, self.rae):
            for key, value in (("oid", "SYN-rebound"), ("role", "Quality Inspector")):
                with self.subTest(subject=subject["code"], field=key):
                    save = self.store.save

                    def changed(
                        subject: dict[str, Any] = subject,
                        key: str = key,
                        value: str = value,
                        save: Callable[[], None] = save,
                    ) -> None:
                        connection = self.store.assistant_connection()
                        try:
                            connection.execute(
                                "UPDATE staff SET body=? WHERE email=?",
                                (json.dumps(dict(subject, **{key: value})), subject["email"]),
                            )
                        finally:
                            connection.close()
                        save()

                    with patch.object(self.store, "save", side_effect=changed):
                        self.unchanged_failure(lambda: self.commitment(owner=self.rae["email"]))
                    self.store.db.execute(
                        "UPDATE staff SET body=? WHERE email=?",
                        (json.dumps(subject), subject["email"]),
                    )
        self.request()
        self.action("service_update", id="SR-1", status="Resolved", next_update="2099-01-01")
        with self.store.lock:
            self.store._case("ZF-1")["service_requests"][0].pop("service_identity")
            self.store.save()
        save = self.store.save

        def rebound() -> None:
            self.store.db.execute(
                "UPDATE staff SET body=? WHERE email=?",
                (json.dumps(dict(self.sam, code=self.rae["code"])), self.sam["email"]),
            )
            save()

        with patch.object(self.store, "save", side_effect=rebound):
            self.unchanged_failure(
                lambda: self.store.resident_action(
                    self.rae, "ZF-1", dict(action="service_close", id="SR-1", note="SYN")
                )
            )
        self.store.db.execute(
            "UPDATE staff SET body=? WHERE email=?", (json.dumps(self.sam), self.sam["email"])
        )
        self.store.resident_action(
            self.rae, "ZF-1", dict(action="service_close", id="SR-1", note="SYN response")
        )

    def test_concurrent_followup_writers_one_version_one_success_event(self) -> None:
        self.commitment()
        other = self.open_store()
        barrier = Barrier(2)

        def record(store: Store, owner: dict[str, Any]) -> str:
            with store.lock:
                barrier.wait(timeout=20)
                try:
                    store.resident_action(
                        self.sam,
                        "ZF-1",
                        dict(
                            action="update_record",
                            expected_version=1,
                            owner=owner["email"],
                            purpose="SYN concurrent",
                            due_at="2099-01-01T12:00:00Z",
                            basis="SYN",
                            status="Outstanding",
                        ),
                    )
                    return "recorded"
                except ConflictError:
                    return "conflict"

        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [
                pool.submit(record, self.store, self.sam),
                pool.submit(record, other, self.rae),
            ]
            self.assertCountEqual([f.result(timeout=40) for f in futures], ["recorded", "conflict"])
        current = self.open_store()
        self.assertEqual(current.cases["ZF-1"]["resident_update"]["version"], 2)
        self.assertEqual(
            sum(e["action"] == "resident_update_record" for e in current.audit_entries()), 2
        )
        self.assertTrue(current.verify_audit())

    def test_followup_audit_insert_and_recovery_faults_never_replay_success(self) -> None:
        assert isinstance(self.store, SqlStore)
        self.commitment()
        for persistent in (False, True):
            with self.subTest(persistent=persistent):
                before = copy.deepcopy(self.store.cases["ZF-1"])
                audit = list(self.store.audit_entries())
                db, append = self.store.db, self.store._append_audit
                original = OSError("SYN after real audit insert")

                class ReadFault:
                    armed = False
                    count = 0

                    def __init__(self, db: Any, persistent: bool) -> None:
                        self.db = db
                        self.persistent = persistent

                    def execute(self, sql: str, args: Any = ()) -> Any:
                        if self.armed and sql.startswith("SELECT rowversion, body FROM cases"):
                            if self.persistent or self.count == 0:
                                self.count += 1
                                raise OSError("SYN recovery read")
                        return self.db.execute(sql, args)

                    def __getattr__(self, name: str) -> Any:
                        return getattr(self.db, name)

                fault = ReadFault(db, persistent)

                def audit_failure(
                    entries: Any,
                    append: Callable[..., Any] = append,
                    fault: ReadFault = fault,
                    original: OSError = original,
                ) -> None:
                    append(entries)
                    fault.armed = True
                    raise original

                with self.store.lock:
                    self.store.audit(self.sam["email"], "prior_event", "ZF-2", "SYN")
                    prior = list(self.store.local.pending)
                    with (
                        patch.object(self.store, "_append_audit", side_effect=audit_failure),
                        patch.object(self.store, "db", fault),
                        self.assertLogs("zava_forward.core.resident_decisions", level="ERROR"),
                    ):
                        with self.assertRaises(OSError) as caught:
                            self.commitment(expected_version=1)
                    self.assertIs(caught.exception, original)
                    self.assertEqual(self.store.local.pending, prior)
                    self.assertEqual(self.store.local.touched, set())
                    self.assertIsNone(self.store.local.resident_validation)
                current = self.open_store()
                self.assertEqual(current.cases["ZF-1"], before)
                self.assertEqual(
                    [e["action"] for e in current.audit_entries()],
                    [e["action"] for e in audit] + ["prior_event"],
                )
                self.assertTrue(current.verify_audit())
        self.commitment(expected_version=1)

    def test_followup_postcommit_sync_fault_is_truthful_and_not_replayed(self) -> None:
        from zava_forward.core.resident_decisions import ResidentCommittedError

        assert isinstance(self.store, SqlStore)
        self.commitment()
        other = self.open_store()
        save, sync = self.store.save, self.store._sync
        fault = dict(armed=False)

        def interleave() -> None:
            other.log_call(self.sam, "ZF-2", "SYN", "SYN concurrent unrelated write")
            fault["armed"] = True
            save()

        def failed_sync() -> None:
            if fault["armed"]:
                raise OSError("SYN persistent postcommit synchronization")
            sync()

        with self.store.lock:
            self.store.audit(self.sam["email"], "prior_event", "ZF-2", "SYN")
            with (
                patch.object(self.store, "save", side_effect=interleave),
                patch.object(self.store, "_sync", side_effect=failed_sync),
                self.assertLogs("zava_forward.core.resident_decisions", level="ERROR"),
                self.assertRaises(ResidentCommittedError) as caught,
            ):
                self.commitment(expected_version=1)
            self.assertIn("recorded", str(caught.exception))
            self.assertIsInstance(caught.exception.__cause__, OSError)
            self.assertEqual(self.store.local.pending, [])
        current = self.open_store()
        self.assertEqual(current.cases["ZF-1"]["resident_update"]["version"], 2)
        audit = list(current.audit_entries())
        self.store.save()
        self.assertEqual(list(self.store.audit_entries()), audit)
        self.assertEqual(sum(e["action"] == "resident_update_record" for e in audit), 2)
        self.assertEqual(sum(e["action"] == "prior_event" for e in audit), 1)
        self.assertTrue(current.verify_audit())

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


@unittest.skipUnless(os.environ.get("ZF_RESIDENT_MSSQL") == "1", "opt-in owned loopback SQL Server")
class MssqlResidentControls(SqlResidentDecisions):
    def setUp(self) -> None:
        from zava_forward.core.mssqlstore import _Conn, connection_string

        self.database = "zf_resident88_" + uuid.uuid4().hex
        environment = patch.dict(os.environ, ZF_SQL_DATABASE="master")
        environment.start()
        self.addCleanup(environment.stop)
        admin = _Conn(connection_string())
        self.addCleanup(admin.close)
        admin.execute(f"CREATE DATABASE [{self.database}]")

        def drop_owned_database() -> None:
            admin.execute(
                f"ALTER DATABASE [{self.database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE"
            )
            admin.execute(f"DROP DATABASE [{self.database}]")

        self.addCleanup(drop_owned_database)
        os.environ["ZF_SQL_DATABASE"] = self.database
        super().setUp()

    def open_store(self) -> Any:
        from zava_forward.core.mssqlstore import MssqlStore

        store = MssqlStore(str(self.path), state_dir=self.tmp.name)
        self.addCleanup(store.db.close)
        return store
