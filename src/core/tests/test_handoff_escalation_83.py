"""Focused unit tests for Issue #83 BG-010 unaccepted handoff visibility and timely escalation."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

import dataset as _dataset
from zava_forward.core import change_provenance, projection
from zava_forward.core import workflows as _workflows
from zava_forward.core.sqlstore import SqlStore as _SqlStore
from zava_forward.core.store import Store as _Store

DATA: dict[str, Any] = _dataset.DATA
CHANGE_METADATA: Any = _dataset.change_metadata
STORE_CLS: Any = _Store
SQL_STORE_CLS: Any = _SqlStore
WORKFLOWS: Any = _workflows

APPROVED_POLICY: dict[str, Any] = {
    "status": "Approved",
    "owner": "Pam Lead",
    "policy_id": "BG-010-v1",
    "acceptance_hours": 24,
    "urgent_acceptance_hours": 4,
    "escalation_role": "Retrofit Programme Manager",
}


class HandoffSlaHelpersTests(unittest.TestCase):
    def _case_with_handoff(self, **overrides: Any) -> dict[str, Any]:
        case: dict[str, Any] = copy.deepcopy(DATA["cases"][0])
        handoff: dict[str, Any] = {
            "state": "Offered",
            "from_code": "RLO-01",
            "from_name": "Sam Example",
            "to_code": "RC-01",
            "to_name": "Rex Coordinator",
            "to_role": "Retrofit Coordinator",
            "offered_by": "Sam Example",
            "offered_at": "2026-10-15T00:00:00+00:00",
            "answered_at": None,
            "answer_note": "",
            "due_at": None,
            "urgency": "Routine",
            "note": "PRIVATE-NOTE",
            "next_action": "PRIVATE-NEXT",
        }
        handoff.update(overrides)
        case["handoff"] = handoff
        return case

    def test_unapproved_or_malformed_policy_preserves_od09_non_fabrication(self) -> None:
        bad_policies: tuple[Any, ...] = (
            None,
            {},
            {"status": "Draft", "owner": "Pam Lead", "acceptance_hours": 24},
            {"status": "Approved", "owner": "Unknown", "acceptance_hours": 24},
            {"status": "Approved", "owner": "to be named", "acceptance_hours": 24},
            {"status": "Approved", "owner": "Pam Lead", "acceptance_hours": 0},
            {"status": "Approved", "owner": "Pam Lead", "acceptance_hours": -8},
            {"status": "Approved", "owner": "Pam Lead", "acceptance_hours": True},
            {"status": "Approved", "owner": "Pam Lead", "acceptance_hours": float("nan")},
            {
                "status": "Approved",
                "owner": "Pam Lead",
                "acceptance_hours": 24,
                "urgent_acceptance_hours": 0,
            },
        )
        case = self._case_with_handoff()
        as_of = "2026-10-18T00:00:00+00:00"
        for bad in bad_policies:
            with self.subTest(policy=bad):
                self.assertIsNone(WORKFLOWS.approved_handoff_policy(bad))
                self.assertIsNone(WORKFLOWS.approved_handoff_limit_hours(bad, urgency="Urgent"))
                view = WORKFLOWS.handoff_view(case, as_of=as_of, policy=bad)
                self.assertIsNone(view["approved_limit_hours"])
                self.assertIsNone(view["sla_due_at"])
                self.assertFalse(view["overdue"])
                self.assertFalse(view["needs_escalation"])
                self.assertEqual(
                    view["escalation_status"], "Pending acceptance (unbounded - OD-09)"
                )
                ageing = WORKFLOWS.handoff_ageing(case, as_of, policy=bad)
                self.assertEqual(len(ageing), 13)
                self.assertFalse(ageing["needs_escalation"])
                self.assertIsNone(ageing["approved_limit_hours"])
                self.assertEqual(ageing["limit_note"], "Approved escalation time not set (OD-09)")

    def test_routine_and_urgent_exact_second_boundaries_and_earlier_effective_due_at(self) -> None:
        routine = self._case_with_handoff(offered_at="2026-10-15T00:00:00+00:00", urgency="Routine")
        at_limit = WORKFLOWS.handoff_view(
            routine, as_of="2026-10-16T00:00:00+00:00", policy=APPROVED_POLICY
        )
        self.assertFalse(at_limit["overdue"])
        self.assertEqual(at_limit["overdue_hours"], 0.0)
        self.assertEqual(at_limit["escalation_status"], "Within approved window")

        plus_one_sec = WORKFLOWS.handoff_view(
            routine, as_of="2026-10-16T00:00:01+00:00", policy=APPROVED_POLICY
        )
        self.assertTrue(plus_one_sec["overdue"])
        self.assertTrue(plus_one_sec["needs_escalation"])
        self.assertEqual(plus_one_sec["escalation_status"], "Overdue - escalation required")
        ageing = WORKFLOWS.handoff_ageing(
            routine, "2026-10-16T00:00:01+00:00", policy=APPROVED_POLICY
        )
        self.assertTrue(ageing["needs_escalation"])
        self.assertIn("Unaccepted for more than the approved 24.0 hours", ageing["reasons"])
        self.assertEqual(ageing["limit_note"], "Approved escalation limit: 24.0h (BG-010-v1)")

        urgent = self._case_with_handoff(
            offered_at="2026-10-15T08:00:00+00:00",
            urgency="Urgent",
            due_at="2026-10-17T08:00:00+00:00",
        )
        urgent_ok = WORKFLOWS.handoff_view(
            urgent, as_of="2026-10-15T12:00:00+00:00", policy=APPROVED_POLICY
        )
        self.assertFalse(urgent_ok["overdue"])
        self.assertEqual(urgent_ok["approved_limit_hours"], 4.0)
        self.assertEqual(urgent_ok["effective_due_at"], "2026-10-15T12:00:00+00:00")

        urgent_breach = WORKFLOWS.handoff_view(
            urgent, as_of="2026-10-15T12:00:01+00:00", policy=APPROVED_POLICY
        )
        self.assertTrue(urgent_breach["overdue"])
        self.assertTrue(urgent_breach["needs_escalation"])

        for terminal in ("Accepted", "Declined", "Withdrawn", "Completed"):
            done = self._case_with_handoff(state=terminal, answered_at="2026-10-15T02:00:00+00:00")
            view = WORKFLOWS.handoff_view(
                done, as_of="2026-10-18T00:00:00+00:00", policy=APPROVED_POLICY
            )
            self.assertFalse(view["overdue"])
            self.assertFalse(view["needs_escalation"])

    def test_missing_offered_at_is_tolerated_in_view_and_ageing_reports_unknown(self) -> None:
        legacy = self._case_with_handoff()
        legacy["handoff"].pop("offered_at")
        view = WORKFLOWS.handoff_view(
            legacy, as_of="2026-10-16T00:00:00+00:00", policy=APPROVED_POLICY
        )
        self.assertIsNone(view["elapsed_hours"])
        self.assertFalse(view["overdue"])
        row = WORKFLOWS.handoff_ageing(legacy, "2026-10-16T00:00:00+00:00", policy=APPROVED_POLICY)
        self.assertIsNone(row["age_hours"])
        self.assertFalse(row["needs_escalation"])


class JsonHandoffEscalation83Tests(unittest.TestCase):
    sql = False

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "seed.json"
        data: dict[str, Any] = copy.deepcopy(DATA)
        data["as_of"] = "2026-10-18"
        data["staff"].extend(
            [
                {
                    "code": "RLO-02",
                    "name": "Rae Other",
                    "email": "rae@example.test",
                    "role": "Resident Liaison Officer",
                },
                {
                    "code": "RC-01",
                    "name": "Rex Coordinator",
                    "email": "rex@example.test",
                    "role": "Retrofit Coordinator",
                },
                {
                    "code": "RC-02",
                    "name": "Rory Coordinator",
                    "email": "rory@example.test",
                    "role": "Retrofit Coordinator",
                },
                {
                    "code": "PSO-01",
                    "name": "Pia Support",
                    "email": "pso@example.test",
                    "role": "Programme Support Officer",
                },
                {
                    "code": "QI-01",
                    "name": "Quinn Inspector",
                    "email": "quinn@example.test",
                    "role": "Quality Inspector",
                },
                {
                    "code": "CON-01",
                    "name": "Kim Builder",
                    "email": "kim@example.test",
                    "role": "Contractor",
                    "contractor": "Test Ltd",
                },
            ]
        )
        data["cases"][0]["stage"] = "Install booked"
        data["cases"][0]["resident"]["name"] = "PRIVATE-RESIDENT"
        data["cases"][0]["home"]["address"] = "PRIVATE-ADDRESS"
        data["cases"][1]["stage"] = "Survey booked"
        self.actors: dict[str, dict[str, Any]] = {
            row["email"].split("@")[0]: row for row in data["staff"]
        }
        self.path.write_text(json.dumps(data), encoding="utf-8")
        self.store: Any = self._open_store()

    def _open_store(self) -> Any:
        if self.sql:
            store = SQL_STORE_CLS(str(self.path), str(self.path.with_suffix(".sqlite")))
            self.addCleanup(store.db.close)
            return store
        return STORE_CLS(str(self.path))

    def _offer_aged(
        self,
        case_id: str,
        sender: dict[str, Any],
        to_email: str,
        offered_at: str,
        *,
        urgency: str = "Routine",
        receive_by: dict[str, Any] | None = None,
    ) -> None:
        self.store.offer_handoff(
            sender,
            case_id,
            to_email,
            "PRIVATE-NOTE",
            metadata={
                **CHANGE_METADATA(self.store, case_id),
                "urgency": urgency,
                "next_action": "PRIVATE-NEXT",
            },
        )
        if receive_by is not None:
            self.store.receive_handoff(receive_by, case_id)
        with change_provenance.controlled(self.store, sender, case_id) as (c, actor):
            c["handoff"]["offered_at"] = offered_at
            self.store._save_workflow(actor, "test_age_handoff", case_id, offered_at)

    def test_policy_activation_updates_case_work_and_overdue_queues_deterministically(self) -> None:
        sam = self.actors["sam"]
        pam = self.actors["pam"]
        rex = self.actors["rex"]
        self._offer_aged("ZF-1", sam, "rex@example.test", "2026-10-15T10:00:00+00:00")

        before_overdue = {
            row["id"] for row in self.store.list_cases(pam, "all", filters={"queue": "overdue"})
        }
        self.assertNotIn("ZF-1", before_overdue)
        self.assertIn(
            "ZF-1",
            {row["id"] for row in self.store.list_cases(pam, "all", filters={"queue": "unowned"})},
        )

        with self.store.lock:
            self.store.data["handoff_policy"] = copy.deepcopy(APPROVED_POLICY)
            self.store.save()

        reader = self._open_store() if self.sql else self.store
        overdue_ids = {
            row["id"] for row in reader.list_cases(pam, "all", filters={"queue": "overdue"})
        }
        self.assertIn("ZF-1", overdue_ids)

        pam_detail = reader.detail("ZF-1", pam)
        self.assertTrue(pam_detail["handoff"]["overdue"])
        self.assertTrue(pam_detail["handoff"]["needs_escalation"])
        self.assertEqual(
            pam_detail["handoff"]["escalation_status"], "Overdue - escalation required"
        )
        self.assertEqual(pam_detail["handoff"]["escalation_target"], "Pam Lead")
        self.assertEqual(pam_detail["handoff"]["accountable_owner"], "Sam Example")
        self.assertEqual(
            pam_detail["work"]["handoff"]["escalation_status"], "Overdue - escalation required"
        )
        self.assertTrue(
            any(item["task"] == "Handoff acceptance" for item in pam_detail["work"]["overdue"])
        )

        rex_detail = reader.detail("ZF-1", rex)
        self.assertEqual(rex_detail["work"]["next_action"], projection.NOTE_HELD)
        self.assertIn("Pam Lead", rex_detail["work"]["handoff"]["escalation_next_action"])
        self.assertNotIn("PRIVATE-NEXT", json.dumps(rex_detail))

    def test_unaccepted_handoffs_lists_a_handoff_with_an_offered_time_that_cannot_be_aged(
        self,
    ) -> None:
        sam = self.actors["sam"]
        rex = self.actors["rex"]
        as_of = "2026-10-16T18:00:00+00:00"
        self._offer_aged("ZF-1", sam, "rex@example.test", "2026-10-15T10:00:00+00:00")
        self._offer_aged("ZF-2", sam, "rex@example.test", "2026-10-13T09:00")

        rows = self.store.unaccepted_handoffs(rex, as_of=as_of)
        self.assertEqual([row["case_id"] for row in rows], ["ZF-1", "ZF-2"])
        unknown = rows[1]
        self.assertIsNone(unknown["age_hours"])
        self.assertEqual(unknown["chase_owner"], "Sam Example")
        self.assertFalse(unknown["needs_escalation"])

    def test_role_queues_surface_unowned_and_escalated_handoffs_without_leaking_canaries(
        self,
    ) -> None:
        sam = self.actors["sam"]
        pam = self.actors["pam"]
        pso = self.actors["pso"]
        rex = self.actors["rex"]
        rory = self.actors["rory"]
        quinn = self.actors["quinn"]
        kim = self.actors["kim"]
        with self.store.lock:
            self.store.data["handoff_policy"] = copy.deepcopy(APPROVED_POLICY)
            self.store.save()

        as_of = "2026-10-16T18:00:00+00:00"
        self._offer_aged(
            "ZF-1",
            sam,
            "rex@example.test",
            "2026-10-15T10:00:00+00:00",
            receive_by=rex,
        )
        self._offer_aged(
            "ZF-2",
            sam,
            "rex@example.test",
            "2026-10-16T10:00:00+00:00",
        )

        with self.assertRaises(PermissionError):
            self.store.unowned_handoffs(kim, as_of=as_of)
        with self.assertRaises(PermissionError):
            self.store.escalated_handoffs(kim, as_of=as_of)

        # Named-colleague unaccepted_handoffs keeps direct sender/receiver/manager scope.
        self.assertEqual(self.store.unaccepted_handoffs(rory, as_of=as_of), [])
        self.assertEqual(len(self.store.unaccepted_handoffs(rex, as_of=as_of)), 2)

        # Shared destination-role unowned_handoffs makes both handoffs visible to peer RC-02 (Rory)
        # while excluding unrelated Quality Inspector Quinn, ordered overdue-first.
        rory_unowned = self.store.unowned_handoffs(rory, as_of=as_of)
        self.assertEqual([row["case_id"] for row in rory_unowned], ["ZF-1", "ZF-2"])
        self.assertEqual(rory_unowned[0]["note"], projection.NOTE_HELD)
        self.assertEqual(rory_unowned[0]["next_action"], projection.NOTE_HELD)
        self.assertIn("Pam Lead", rory_unowned[0]["escalation_next_action"])
        for forbidden in ("PRIVATE-RESIDENT", "PRIVATE-ADDRESS", "PRIVATE-NOTE", "PRIVATE-NEXT"):
            self.assertNotIn(forbidden, json.dumps(rory_unowned))
        self.assertEqual(self.store.unowned_handoffs(quinn, as_of=as_of), [])

        # Escalated/overdue queue shows only overdue ZF-1 before sweep for Rory, PSO, and Pam.
        for viewer in (sam, rex, rory, pso, pam):
            esc_rows = self.store.escalated_handoffs(viewer, as_of=as_of)
            self.assertEqual([row["case_id"] for row in esc_rows], ["ZF-1"])

        # Accepting ZF-1 removes it from unowned, unaccepted, and escalated queues.
        self.store.accept_handoff(rex, "ZF-1", metadata=CHANGE_METADATA(self.store, "ZF-1"))
        self.assertEqual(
            [row["case_id"] for row in self.store.unowned_handoffs(rory, as_of=as_of)], ["ZF-2"]
        )
        self.assertEqual(self.store.escalated_handoffs(pam, as_of=as_of), [])

    def test_overdue_sweep_transitions_retains_sender_ownership_audits_and_is_idempotent(
        self,
    ) -> None:
        sam = self.actors["sam"]
        pam = self.actors["pam"]
        pso = self.actors["pso"]
        rex = self.actors["rex"]
        as_of = "2026-10-17T12:00:00+00:00"
        self._offer_aged("ZF-1", sam, "rex@example.test", "2026-10-15T10:00:00+00:00")
        self._offer_aged(
            "ZF-2",
            sam,
            "rex@example.test",
            "2026-10-17T06:00:00+00:00",
            urgency="Urgent",
            receive_by=rex,
        )

        for non_mgr in (sam, rex):
            with self.assertRaises(PermissionError):
                self.store.escalate_overdue_handoffs(non_mgr, as_of=as_of)

        # Without an approved policy, sweep never fabricates a threshold (OD-09).
        no_policy = self.store.escalate_overdue_handoffs(pam, as_of=as_of)
        self.assertEqual(no_policy["escalated_count"], 0)
        self.assertEqual(no_policy["evaluated_count"], 2)

        with self.store.lock:
            self.store.data["handoff_policy"] = copy.deepcopy(APPROVED_POLICY)
            self.store.save()

        swept = self.store.escalate_overdue_handoffs(
            pso, as_of=as_of, reason="PRIVATE-SWEEP-REASON"
        )
        self.assertEqual(swept["escalated_case_ids"], ["ZF-1", "ZF-2"])
        self.assertEqual(swept["escalated_count"], 2)
        # PSO lacks reason access, so custom reason is held in returned items.
        self.assertEqual(swept["items"][0]["answer_note"], projection.NOTE_HELD)
        self.assertNotIn("PRIVATE-SWEEP-REASON", json.dumps(swept))

        for cid in ("ZF-1", "ZF-2"):
            detail = self.store.detail(cid, pam)
            self.assertEqual(detail["owner_code"], "RLO-01")
            self.assertEqual(detail["handoff"]["state"], "Escalated")
            self.assertEqual(detail["handoff"]["escalation_status"], "Escalated")
            self.assertEqual(detail["handoff"]["escalation_owner"], "Pam Lead")
            self.assertEqual(detail["handoff"]["escalation_owner_code"], "PM-01")
            self.assertTrue(detail["handoff"]["auto_escalated"])
            self.assertEqual(detail["handoff"]["accountable_owner"], "Sam Example")
            self.assertEqual(detail["handoff_history"][-1]["event_type"], "handoff_escalated")

        self.assertTrue(self.store.verify_ledger()["intact"])

        repeat = self.store.escalate_overdue_handoffs(pam, as_of=as_of)
        self.assertEqual(repeat["escalated_count"], 0)
        self.assertEqual(repeat["already_escalated_count"], 2)

    def test_exception_register_routes_bg010_overdue_handoff_to_digital_operator(self) -> None:
        sam = self.actors["sam"]
        quinn = self.actors["quinn"]
        with self.store.lock:
            self.store.data["handoff_policy"] = copy.deepcopy(APPROVED_POLICY)
            self.store.save()
        self._offer_aged("ZF-1", sam, "rex@example.test", "2026-10-15T08:00:00+00:00")
        reg = self.store.exception_register(
            quinn,
            {quinn["email"]: ("digital_operator",)},
            as_of="2026-10-16T12:00:00+00:00",
        )
        self.assertEqual(reg["state"], "ok")
        stranded = [
            item
            for item in reg["items"]
            if item.get("kind") == "stranded_task"
            and (item.get("original_source") or {}).get("case_id") == "ZF-1"
        ]
        self.assertGreaterEqual(len(stranded), 1)


class SqlHandoffEscalation83Tests(JsonHandoffEscalation83Tests):
    sql = True


if __name__ == "__main__":
    unittest.main()
