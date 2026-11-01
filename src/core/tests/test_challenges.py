"""Affected-person challenge route on constructed challenges (FR-052, AC-071)."""

import unittest
from copy import deepcopy
from typing import Any

from zava_forward.core.challenges import ACCESSIBLE_ROUTE, NOT_INFERRED, ChallengeRegister


def n(kind: str, item: str, version: str = "v1") -> tuple[str, str, str]:
    return (kind, item, version)


S1 = n("source", "SRC-1", "v3")
GRAPH = {
    n("proposal", "PROP-1"): [S1],
    n("proposal", "CALC-1"): [n("proposal", "PROP-1")],
    n("proposal", "REVIEW-1"): [n("proposal", "CALC-1")],
    n("proposal", "PROP-2"): [n("source", "SRC-2")],
    n("proposal", "REVIEW-2"): [n("proposal", "PROP-2")],
}
SUBJECT = {"kind": "source", "id": "SRC-1", "version": "v3"}
EXPLANATIONS = [
    {"kind": "ai", "text": "The assistant drafted this from the survey.", "permitted": True},
    {"kind": "policy", "text": "Policy P-7 sets the eligibility rule.", "permitted": True},
    {"kind": "internal", "text": "Internal triage note.", "permitted": False},
]


def digital(reg: ChallengeRegister) -> dict[str, Any]:
    return reg.record_digital(
        SUBJECT, "DEC-1", "My boiler age is wrong.", "Pat Owner", "2026-11-10", EXPLANATIONS
    )


def staff(reg: ChallengeRegister) -> dict[str, Any]:
    return reg.record_staff(
        "Sam Staff",
        "phone",
        SUBJECT,
        "DEC-1",
        "My boiler age is wrong.",
        "Pat Owner",
        "2026-11-10",
        EXPLANATIONS,
    )


class ChallengeRoutes(unittest.TestCase):
    def test_both_routes_record_with_owner_and_next_update(self) -> None:
        reg = ChallengeRegister(GRAPH)
        d, s = digital(reg), staff(reg)
        self.assertEqual((d["route"], s["route"]), ("digital", "staff_recorded"))
        self.assertEqual(s["recorded_by"], "Sam Staff")
        self.assertEqual(s["channel"], "phone")
        for rec in (d, s):
            self.assertEqual(rec["owner"], "Pat Owner")
            self.assertEqual(rec["next_update"], "2026-11-10")
            self.assertEqual(rec["accessible_route"], ACCESSIBLE_ROUTE)
            self.assertEqual(rec["subject"], SUBJECT)
            self.assertEqual(rec["decision_ref"], "DEC-1")

    def test_staff_route_needs_named_staff_and_non_digital_channel(self) -> None:
        reg = ChallengeRegister(GRAPH)
        with self.assertRaises(ValueError):
            reg.record_staff("", "phone", SUBJECT, "D", "s", "o", "2026-11-10")
        with self.assertRaises(ValueError):
            reg.record_staff("Sam", "email", SUBJECT, "D", "s", "o", "2026-11-10")

    def test_owner_and_next_update_are_mandatory(self) -> None:
        reg = ChallengeRegister(GRAPH)
        with self.assertRaises(ValueError):
            reg.record_digital(SUBJECT, "D", "s", " ", "2026-11-10")
        with self.assertRaises(ValueError):
            reg.record_digital(SUBJECT, "D", "s", "o", "soon")


class Visibility(unittest.TestCase):
    def test_only_permitted_explanations_visible_and_resolution_shown(self) -> None:
        reg = ChallengeRegister(GRAPH)
        cid = digital(reg)["id"]
        shown = reg.view(cid)
        self.assertEqual([e["kind"] for e in shown["explanations"]], ["ai", "policy"])
        reg.review(cid, "Pat Owner", "2026-11-17")
        self.assertEqual(reg.view(cid)["next_update"], "2026-11-17")
        reg.resolve(cid, "Pat Owner", "corrected", "Survey re-read on 2026-11-12")
        done = reg.view(cid)
        self.assertEqual(done["status"], "corrected")
        self.assertEqual(done["resolution"]["evidence"], "Survey re-read on 2026-11-12")

    def test_only_named_owner_resolves_with_evidence(self) -> None:
        reg = ChallengeRegister(GRAPH)
        cid = digital(reg)["id"]
        with self.assertRaises(PermissionError):
            reg.resolve(cid, "Someone Else", "upheld", "x")
        with self.assertRaises(ValueError):
            reg.resolve(cid, "Pat Owner", "upheld", "")
        with self.assertRaises(ValueError):
            reg.resolve(cid, "Pat Owner", "closed", "x")


class Staleness(unittest.TestCase):
    def test_only_transitive_dependents_become_stale(self) -> None:
        reg = ChallengeRegister(GRAPH)
        cid = staff(reg)["id"]
        self.assertEqual(reg.stale, {})
        reg.resolve(cid, "Pat Owner", "corrected", "Evidence")
        self.assertEqual(sorted(i for _, i, _ in reg.stale), ["CALC-1", "PROP-1", "REVIEW-1"])
        self.assertTrue(all(v["prior_version_preserved"] for v in reg.stale.values()))

    def test_upheld_or_withdrawn_marks_nothing_stale(self) -> None:
        for outcome in ("upheld", "withdrawn"):
            reg = ChallengeRegister(GRAPH)
            reg.resolve(digital(reg)["id"], "Pat Owner", outcome, "Evidence")
            self.assertEqual(reg.stale, {})

    def test_cycle_in_graph_terminates(self) -> None:
        a, b = n("proposal", "A"), n("proposal", "B")
        reg = ChallengeRegister({a: [S1, b], b: [a]})
        self.assertEqual(reg.dependents(S1), [a, b])

    def test_other_versions_of_subject_stay_current(self) -> None:
        old = n("policy", "POL-1", "v1")
        on_v1, on_v2 = n("proposal", "P-A"), n("proposal", "P-B")
        reg = ChallengeRegister({on_v1: [old], on_v2: [n("policy", "POL-1", "v2")]})
        cid = reg.record_digital(
            {"kind": "policy", "id": "POL-1", "version": "v1"},
            "DEC-1",
            "Wrong rule.",
            "Pat Owner",
            "2026-11-10",
        )["id"]
        reg.resolve(cid, "Pat Owner", "corrected", "Evidence")
        self.assertEqual(list(reg.stale), [on_v1])


class NoInference(unittest.TestCase):
    def test_surrounding_state_is_untouched(self) -> None:
        state = {
            "consent": "not given",
            "refusal": None,
            "sanction": None,
            "closed": ["CASE-9"],
            "hazard_clock": {"HZ-1": "2026-11-03T09:00"},
        }
        before = deepcopy(state)
        reg = ChallengeRegister(GRAPH)
        for rec in (digital(reg), staff(reg)):
            reg.review(rec["id"], "Pat Owner", "2026-11-17")
            reg.resolve(rec["id"], "Pat Owner", "corrected", "Evidence")
        self.assertEqual(state, before)
        self.assertNotIn(n("proposal", "PROP-2"), reg.stale)
        self.assertNotIn(n("proposal", "REVIEW-2"), reg.stale)
        self.assertEqual(set(reg.view("CH-001")["not_inferred"]), set(NOT_INFERRED))
        for key in ("consent", "refusal", "sanction", "hazard_clock", "closed"):
            self.assertNotIn(key, reg.challenges["CH-001"])


class Robustness(unittest.TestCase):
    def test_generator_parents_are_reusable(self) -> None:
        a, b = n("proposal", "A"), n("proposal", "B")
        reg = ChallengeRegister({a: (p for p in [S1]), b: (p for p in [a])})
        self.assertEqual(reg.dependents(S1), [a, b])
        self.assertEqual(reg.dependents(S1), [a, b])

    def test_prepopulated_register_never_overwrites(self) -> None:
        keep = {"CH-001": {"id": "CH-001"}, "CH-003": {"id": "CH-003"}}
        reg = ChallengeRegister(GRAPH, challenges=dict(keep))
        new = digital(reg)
        self.assertEqual(new["id"], "CH-004")
        self.assertEqual({k: reg.challenges[k] for k in keep}, keep)


class HazardConcern(unittest.TestCase):
    def test_hazard_concern_is_referred_on_receipt_without_clock_or_sanction(self) -> None:
        reg = ChallengeRegister(GRAPH)
        args = (SUBJECT, "DEC-1", "Mould is making us ill.", "Pat Owner", "2026-11-10")
        urgent = reg.record_digital(*args, hazard_concern=True)
        routine = reg.record_digital(*args)
        self.assertEqual(urgent["hazard_referral"]["to"], "Pat Owner")
        self.assertNotIn("hazard_referral", routine)
        self.assertEqual([r["id"] for r in reg.hazard_referrals()], [urgent["id"]])
        for key in ("hazard_clock", "sanction", "refusal", "consent"):
            self.assertNotIn(key, urgent)

    def test_resolution_keeps_referral_listed_until_evidenced_handoff(self) -> None:
        reg = ChallengeRegister(GRAPH)
        rec = reg.record_staff(
            "Sam Staff",
            "phone",
            SUBJECT,
            "DEC-1",
            "Gas smell.",
            "Pat Owner",
            "2026-11-10",
            hazard_concern=True,
        )
        self.assertEqual(len(reg.hazard_referrals()), 1)
        reg.resolve(rec["id"], "Pat Owner", "upheld", "Checked.")
        self.assertEqual(len(reg.hazard_referrals()), 1)
        with self.assertRaises(PermissionError):
            reg.confirm_hazard_handoff(rec["id"], "Other", "Called out.")
        with self.assertRaises(ValueError):
            reg.confirm_hazard_handoff(rec["id"], "Pat Owner", " ")
        reg.confirm_hazard_handoff(rec["id"], "Pat Owner", "Engineer called out 09:10.")
        self.assertEqual(reg.hazard_referrals(), [])


if __name__ == "__main__":
    unittest.main()
