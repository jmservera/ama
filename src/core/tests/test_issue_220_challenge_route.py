"""Deterministic safeguard tests for Issue #220 affected-person challenge route.

Verifies that submitting, updating, escalating or resolving a challenge or correction request
against a source, policy, proposal version or human decision never triggers retaliation flags or
ranking penalties, never records an inferred resident refusal, and never delays or pauses any
statutory/safety hazard clock or emergency response across ChallengeRegister, JSON Store and
SQLite SqlStore.
"""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

import dataset as _dataset
from zava_forward.core import ranking as _ranking_mod
from zava_forward.core import resident_decisions as _rd_mod
from zava_forward.core.challenges import (
    FORBIDDEN_ADVERSE_FIELDS,
    NOT_INFERRED,
    PROTECTION,
    SAFEGUARDS,
    SUBJECT_KINDS,
    ChallengeRegister,
    ChallengeSafeguardError,
    Node,
    assert_no_adverse_challenge_effects,
)
from zava_forward.core.sqlstore import SqlStore as _SqlStore
from zava_forward.core.store import Store as _Store

DATA: dict[str, Any] = _dataset.DATA
STORE_CLS: Any = _Store
SQL_STORE_CLS: Any = _SqlStore
RANKING: Any = _ranking_mod
RESIDENT_DECISIONS: Any = _rd_mod
MEASURES = ("Loft insulation", "Cavity wall")


def _node(kind: str, item_id: str, version: str = "v1") -> Node:
    return (kind, item_id, version)


class ChallengeRegisterLifecycleAndSafeguardsTests(unittest.TestCase):
    def test_submit_update_escalate_resolve_across_all_four_subjects_and_channels(self) -> None:
        self.assertEqual(
            SUBJECT_KINDS,
            ("source", "policy", "proposal", "human_decision"),
        )
        src = _node("source", "SRC-220", "v2")
        pol = _node("policy", "POL-220", "v4")
        prop = _node("proposal", "PROP-220", "v1")
        dec_v1 = _node("human_decision", "DEC-220", "d1")
        dec_v2 = _node("human_decision", "DEC-220", "d2")
        downstream_d1 = _node("proposal", "WORKPACK-D1", "v1")
        downstream_d2 = _node("proposal", "WORKPACK-D2", "v1")
        graph: dict[Node, list[Node]] = {
            prop: [src, pol],
            dec_v1: [prop],
            downstream_d1: [dec_v1],
            downstream_d2: [dec_v2],
        }
        reg = ChallengeRegister(graph)

        # Exercise all 4 subject kinds across digital + all 4 non-digital staff channels.
        recorded_ids: list[str] = []
        d_rec = reg.record_digital(
            {"kind": "human_decision", "id": "DEC-220", "version": "d1"},
            "DEC-220#d1",
            "Human review relied on outdated occupancy count.",
            "Pat Owner",
            "2026-11-18",
            explanations=[
                {"kind": "policy", "text": "Priority rule v4 was applied.", "permitted": True},
                {"kind": "internal", "text": "Internal staff draft note.", "permitted": False},
            ],
        )
        recorded_ids.append(d_rec["id"])

        channels_and_subjects = [
            ("phone", {"kind": "source", "id": "SRC-220", "version": "v2"}),
            ("in_person", {"kind": "policy", "id": "POL-220", "version": "v4"}),
            ("paper", {"kind": "proposal", "id": "PROP-220", "version": "v1"}),
            ("assisted_visit", {"kind": "human_decision", "id": "DEC-220", "version": "d2"}),
        ]
        for channel, subj in channels_and_subjects:
            rec = reg.record_staff(
                "Sam Liaison",
                channel,
                subj,
                "DEC-220#d1",
                f"Challenge recorded via {channel}.",
                "Pat Owner",
                "2026-11-18",
            )
            recorded_ids.append(rec["id"])

        cid = d_rec["id"]
        # Update via digital and staff_recorded routes; internal explanation must stay hidden.
        reg.update(
            cid,
            "Added council tax household confirmation.",
            "2026-11-19",
            route="digital",
            explanations=[
                {"kind": "source", "text": "Household size re-checked.", "permitted": True},
                {"kind": "internal", "text": "Hidden update triage note.", "permitted": False},
            ],
        )
        updated = reg.update(
            cid,
            "Resident brought paper tenancy schedule to office.",
            "2026-11-20",
            route="staff_recorded",
            recorded_by="Sam Liaison",
            channel="in_person",
        )
        self.assertEqual(updated["statement"], "Human review relied on outdated occupancy count.")
        self.assertEqual(len(updated["updates"]), 2)

        shown = reg.view(cid)
        self.assertEqual(shown["protection"], PROTECTION)
        self.assertEqual(shown["safeguards"], SAFEGUARDS)
        self.assertEqual(set(shown["not_inferred"]), set(NOT_INFERRED))
        self.assertEqual([e["kind"] for e in shown["explanations"]], ["policy", "source"])
        self.assertEqual([e["kind"] for e in shown["updates"][0]["explanations"]], ["source"])
        for forbidden in FORBIDDEN_ADVERSE_FIELDS:
            self.assertNotIn(forbidden, shown)

        # Review, reject self-escalation and memory reference, then escalate to distinct owner.
        reg.review(cid, "Pat Owner", "2026-11-21")
        with self.assertRaises(ValueError):
            reg.escalate(cid, "Pat Owner", "Same owner.", "2026-11-22")
        with self.assertRaises(ValueError):
            reg.escalate(cid, "Rae Lead", "memory:CM-18f1a2b3c4d5e6f71a2b", "2026-11-22")
        escalated = reg.escalate(
            cid,
            "Rae Lead",
            "Independent review of human priority disposition requested.",
            "2026-11-22",
            escalated_by="Sam Liaison",
        )
        self.assertEqual(escalated["status"], "escalated")
        self.assertEqual(escalated["owner"], "Rae Lead")

        # Previous owner can no longer resolve; escalated owner resolves as corrected.
        with self.assertRaises(PermissionError):
            reg.resolve(cid, "Pat Owner", "corrected", "Occupancy schedule verified.")
        with self.assertRaises(ValueError):
            reg.resolve(cid, "Rae Lead", "corrected", "memory:CM-18f1a2b3c4d5e6f71a2b")
        resolved = reg.resolve(
            cid,
            "Rae Lead",
            "corrected",
            "Occupancy schedule verified on 2026-11-14.",
        )
        self.assertEqual(resolved["status"], "corrected")
        # Exact versioned dependent of human_decision d1 becomes stale; d2 stays untouched.
        self.assertEqual(list(reg.stale), [downstream_d1])
        self.assertTrue(reg.stale[downstream_d1]["prior_version_preserved"])
        self.assertNotIn(downstream_d2, reg.stale)

        # Resolved challenges refuse post-resolution updates or escalations.
        with self.assertRaises(ValueError):
            reg.update(cid, "Late update after resolution.")
        with self.assertRaises(ValueError):
            reg.escalate(cid, "Pat Owner", "Late escalation.", "2026-11-25")

        # Upheld and withdrawn resolutions on remaining challenges mark nothing additional stale.
        reg.resolve(recorded_ids[1], "Pat Owner", "upheld", "Survey record confirmed.")
        reg.resolve(recorded_ids[2], "Pat Owner", "withdrawn", "Withdrawn by resident.")
        self.assertEqual(list(reg.stale), [downstream_d1])

    def test_hazard_referral_never_delayed_or_reset_across_update_escalate_and_resolve(
        self,
    ) -> None:
        reg = ChallengeRegister()
        subj = {"kind": "proposal", "id": "PROP-HZ", "version": "v1"}
        dated = reg.record_digital(
            subj,
            "DEC-HZ",
            "Black mould in bedroom while challenging proposal.",
            "Pat Owner",
            "2026-11-18",
            hazard_concern=True,
            received_on="2026-11-01",
        )
        unknown_age = reg.record_staff(
            "Sam Liaison",
            "phone",
            subj,
            "DEC-HZ",
            "Electrical burning smell reported during call.",
            "Pat Owner",
            "2026-11-18",
            hazard_concern=True,
        )

        # Invalid received_on on update still fails validation.
        with self.assertRaises(ValueError):
            reg.update(
                dated["id"],
                "More mould photos.",
                hazard_concern=True,
                received_on="not-a-date",
            )

        # Updating with a newer received_on MUST NOT reset original received_on (dated or None).
        reg.update(
            dated["id"],
            "Resident added bedroom humidity note.",
            hazard_concern=True,
            received_on="2026-11-13",
        )
        reg.update(
            unknown_age["id"],
            "Resident added hallway socket detail.",
            hazard_concern=True,
            received_on="2026-11-13",
        )

        # Escalating transfers `to` while preserving `originally_referred_to` and `received_on`.
        esc_dated = reg.escalate(
            dated["id"],
            "Bea Safety",
            "Escalating challenge owner while safety referral stays active.",
            "2026-11-19",
        )
        esc_unknown = reg.escalate(
            unknown_age["id"],
            "Bea Safety",
            "Escalating phone challenge.",
            "2026-11-19",
        )
        self.assertEqual(esc_dated["hazard_referral"]["to"], "Bea Safety")
        self.assertEqual(esc_dated["hazard_referral"]["originally_referred_to"], "Pat Owner")
        self.assertEqual(esc_dated["hazard_referral"]["received_on"], "2026-11-01")
        self.assertIsNone(esc_unknown["hazard_referral"]["received_on"])

        # Resolving the challenge keeps unhanded hazard referrals active and overdue-flagged.
        reg.resolve(dated["id"], "Bea Safety", "upheld", "Proposal checked.")
        flagged = {
            r["id"]: r["referral_age_days"]
            for r in reg.hazard_referrals_overdue("2026-11-14", max_days=3)
        }
        self.assertEqual(flagged, {dated["id"]: 13, unknown_age["id"]: None})

        # Confirming handoff on `unknown_age` then reporting a NEW hazard concern on update
        # preserves prior handoff evidence and opens an immediate fresh referral.
        reg.confirm_hazard_handoff(
            unknown_age["id"],
            "Bea Safety",
            "Emergency electrician dispatched ref E-901.",
        )
        reopened_hz = reg.update(
            unknown_age["id"],
            "Separate damp patch noticed in kitchen.",
            hazard_concern=True,
            received_on="2026-11-14",
        )
        self.assertEqual(len(reopened_hz["previous_hazard_handoffs"]), 1)
        self.assertEqual(
            reopened_hz["previous_hazard_handoffs"][0]["handoff_evidence"],
            "Emergency electrician dispatched ref E-901.",
        )
        self.assertEqual(reopened_hz["hazard_referral"]["status"], "referred_on_receipt")
        self.assertEqual(reopened_hz["hazard_referral"]["received_on"], "2026-11-14")

    def test_fail_closed_safeguard_errors_on_adverse_inputs_and_case_tampering(self) -> None:
        reg = ChallengeRegister()
        with self.assertRaises(ChallengeSafeguardError):
            reg.record_digital(
                {"kind": "source", "id": "S", "version": "1", "retaliation": "flag"},
                "D-1",
                "Check source.",
                "Pat Owner",
                "2026-11-18",
            )
        with self.assertRaises(ChallengeSafeguardError):
            reg.record_digital(
                {"kind": "source", "id": "S", "version": "1"},
                "D-1",
                "Check source.",
                "Pat Owner",
                "2026-11-18",
                explanations=[
                    {"kind": "ai", "text": "x", "permitted": True, "inferred_refusal": True}
                ],
            )

        base_case: dict[str, Any] = {
            "id": "ZF-1",
            "closed": False,
            "wave": "Wave 1",
            "stage": "Contacting resident",
            "days_in_stage": 10,
            "resident": {"name": "Alex Resident", "vulnerability": True},
            "funding": {"route": "SHDF"},
            "decision": {"status": "Waiting", "by": None, "at": None},
            "measure_decisions": {"Loft insulation": [{"version": 1, "status": "Accepted"}]},
            "resident_reviews": [],
            "service_requests": [{"id": "SR-1", "status": "Open"}],
            "appointments": [{"date": "2026-11-20", "outcome": "Booked"}],
            "sensors": [{"id": "SEN-1", "consent": "explicit"}],
            "hazards": [
                {
                    "category": "Damp and mould",
                    "priority": "Emergency",
                    "aware_at": "2026-11-14T08:00+00:00",
                    "response_due_at": "2026-11-15T08:00+00:00",
                    "resident_update_due_at": "2026-11-16T08:00+00:00",
                    "released": False,
                    "hold": {"status": "Active", "scope": "Home"},
                }
            ],
            "affected_challenges": [],
        }

        # Legitimate challenge addition with untouched pre-existing sensor `consent` key passes.
        valid_after = copy.deepcopy(base_case)
        valid_after["affected_challenges"].append({"id": "CH-1", "status": "Open", "version": 1})
        assert_no_adverse_challenge_effects(base_case, valid_after)

        # Every prohibited side effect fails closed with ChallengeSafeguardError.
        tamper_mutations: list[tuple[str, Any]] = [
            ("top_adverse_flag", lambda c: c.__setitem__("retaliation_flag", True)),
            (
                "nested_adverse_flag",
                lambda c: c["affected_challenges"].append({"id": "CH-1", "priority_penalty": 5}),
            ),
            (
                "priority_support_downgrade",
                lambda c: c["resident"].__setitem__("vulnerability", False),
            ),
            ("unrelated_case_closure", lambda c: c.__setitem__("closed", True)),
            (
                "unrelated_service_closure",
                lambda c: c["service_requests"][0].__setitem__("status", "Closed"),
            ),
            (
                "appointment_cancelled",
                lambda c: c["appointments"][0].__setitem__("outcome", "Cancelled"),
            ),
            ("inferred_case_refusal", lambda c: c["decision"].__setitem__("status", "Declined")),
            (
                "inferred_measure_refusal",
                lambda c: c["measure_decisions"]["Loft insulation"].append(
                    {"version": 2, "status": "Declined"}
                ),
            ),
            (
                "delayed_hazard_response_due",
                lambda c: c["hazards"][0].__setitem__("response_due_at", "2026-11-25T08:00+00:00"),
            ),
            (
                "paused_hazard_hold",
                lambda c: c["hazards"][0]["hold"].__setitem__("status", "Paused"),
            ),
        ]
        for label, mutate in tamper_mutations:
            with self.subTest(tamper=label):
                tampered = copy.deepcopy(valid_after)
                mutate(tampered)
                with self.assertRaises(ChallengeSafeguardError):
                    assert_no_adverse_challenge_effects(base_case, tampered)


class JsonStoreChallengeSafeguardTests(unittest.TestCase):
    sql = False

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        data = copy.deepcopy(DATA)
        data["as_of"] = "2026-11-14T12:00:00+00:00"
        data["cases"][0]["measures"] = list(MEASURES)
        data["cases"][0]["resident"]["vulnerability"] = True
        data["cases"][0]["appointments"] = [
            {"date": "2026-11-20", "slot": "AM", "outcome": "Booked"}
        ]
        data["staff"].extend(
            [
                {
                    "code": "RLO-02",
                    "name": "Rae Reviewer",
                    "email": "rae@example.test",
                    "role": "Resident Liaison Officer",
                },
                {
                    "code": "BSL-01",
                    "name": "Bea Safety",
                    "email": "bea@example.test",
                    "role": "Building Safety Liaison",
                },
            ]
        )
        self.sam, self.pam, self.rae, self.bea = data["staff"]
        self.path.write_text(json.dumps(data))
        self.store: Any = self._open_store()
        self.store.technical_action(self.pam, "ZF-1", {"action": "design_submit", "note": "SYN"})

    def _open_store(self) -> Any:
        if self.sql:
            store = SQL_STORE_CLS(str(self.path), str(self.path.with_suffix(".sqlite")))
            self.addCleanup(store.db.close)
            return store
        return STORE_CLS(str(self.path))

    def _priority_fixture(self, reviewed: str | None = None) -> dict[str, Any]:
        result: dict[str, Any] = dict(self.store.ai_priority(self.sam, mode="workflow-only"))
        if reviewed is not None:
            self.store.resolve_priority(
                self.sam,
                result["id"],
                reviewed,
                "SYN human priority disposition",
                [{"case_id": "ZF-1", "reason": "SYN human review note"}],
            )
        return result

    def _open_body(
        self,
        proposal_id: str,
        target_kind: str = "proposal",
        channel: str = "Digital",
    ) -> dict[str, Any]:
        target = next(
            item
            for item in self.store.detail("ZF-1", self.sam)["challenge_targets"]
            if item["proposal_id"] == proposal_id
        )
        return {
            "action": "challenge_open",
            "proposal_id": proposal_id,
            "proposal_version": target["proposal_version"],
            "decision_version": target["decision_version"],
            "target_kind": target_kind,
            "channel": channel,
            "source": f"SYN-{target_kind}-ref",
            "request": f"SYN challenge against {target_kind}.",
            "explanation": "SYN plain-language explanation of inputs and rules.",
            "owner": self.sam["email"],
            "non_digital_route": "SYN Phone or visit the staffed housing office.",
            "next_update": "2026-11-21",
        }

    def _stale_ids(self) -> tuple[set[str], set[str]]:
        views = [
            self.store._rec_view(r)
            for r in self.store.data["recommendations"]
            if r.get("kind") != "ai_task"
        ]
        return (
            {r["id"] for r in views if r["stale"]},
            {r["id"] for r in views if r["review_stale"]},
        )


class SqlStoreChallengeSafeguardTests(JsonStoreChallengeSafeguardTests):
    sql = True


if __name__ == "__main__":
    unittest.main()
