"""Issue #220: a challenge never retaliates, infers refusal or delays a hazard response."""

import copy
import json
import unittest
from collections.abc import Callable
from typing import Any
from unittest.mock import patch

from zava_forward.core import challenges, ranking

import test_resident_api

HAZARD = dict(source="SYN hazard report", aware_at="2026-01-01T10:00:00Z")


class NonRetaliationGuard(unittest.TestCase):
    def case(self) -> dict[str, Any]:
        return dict(
            stage="Survey",
            days_in_stage=4,
            closed=False,
            resident=dict(support="Yes"),
            hazards=[dict(released=False, response_due_at="2026-02-01T10:00:00Z")],
            measure_decisions={"Loft": [dict(status="Accepted")]},
        )

    def test_each_protected_change_is_refused(self) -> None:
        mutations: dict[str, Callable[[dict[str, Any]], object]] = {
            "priority": lambda c: c["hazards"].clear(),
            "queue rank": lambda c: c.update(days_in_stage=0),
            "eligibility": lambda c: c.update(tenure_review_required=True),
            "refused": lambda c: c["measure_decisions"]["Loft"].append(dict(status="Declined")),
            "withdrawn": lambda c: c["measure_decisions"]["Loft"][0].update(status="Withdrawn"),
            "hazard clock": lambda c: c["hazards"][0].update(
                response_due_at="2026-03-01T10:00:00Z"
            ),
            "hazard hold": lambda c: c["hazards"][0].update(released=True),
        }
        for name, mutate in mutations.items():
            with self.subTest(name):
                case = self.case()
                before = challenges.protected_snapshot(case)
                mutate(case)
                self.assertTrue(challenges.protected_changes(before, case))
                with self.assertRaisesRegex(ValueError, "Nothing was saved"):
                    challenges.assert_no_retaliation(before, case)

    def test_assurance_is_stamped_only_when_nothing_protected_changed(self) -> None:
        case = self.case()
        before = challenges.protected_snapshot(case)
        record: dict[str, Any] = {}
        challenges.stamp_assurance(before, case, record)
        self.assertIs(record["assurance"]["no_retaliation"], True)
        self.assertIs(record["assurance"]["inferred_refusal"], False)
        self.assertIs(record["assurance"]["hazard_response_delayed"], False)
        case["hazards"][0]["response_due_at"] = "2026-03-01T10:00:00Z"
        late: dict[str, Any] = {}
        with self.assertRaises(ValueError):
            challenges.stamp_assurance(before, case, late)
        self.assertNotIn("assurance", late)

    def test_unrelated_changes_pass(self) -> None:
        case = self.case()
        before = challenges.protected_snapshot(case)
        case["affected_challenges"] = [dict(id="CH-1")]
        challenges.assert_no_retaliation(before, case)

    def test_guarantees_cover_all_three_promises(self) -> None:
        text = " ".join(challenges.GUARANTEES).lower()
        for word in (
            "priority",
            "eligibility",
            "refusing",
            "withdrawing",
            "hazard",
            "safeguarding",
        ):
            self.assertIn(word, text)


class NonRetaliationApi(test_resident_api.ResidentApi):
    def protected(self) -> dict[str, Any]:
        case = self.store.cases["ZF-1"]
        rank = ranking.rank(
            [c for c in self.store.cases.values() if not c["closed"]], ranking.CURRENT
        )
        return dict(
            state=copy.deepcopy(challenges.protected_snapshot(case)),
            ranks={e["id"]: e["rank"] for e in rank},
        )

    def seed_hazard_and_consent(self) -> None:
        self.store.raise_hazard(
            self.store.staff["sam@example.test"],
            "ZF-1",
            "Damp and mould",
            "Emergency",
            "SYN",
            HAZARD,
        )
        self.context()
        code, detail = self.action(
            "decision_record",
            measure="Loft insulation",
            context_revision=1,
            status="Accepted",
            answered_by="The resident",
            source="SYN-STATEMENT",
        )
        self.assertEqual(code, 200, detail)

    def test_challenge_open_and_resolve_leave_protected_state_unchanged(self) -> None:
        self.seed_hazard_and_consent()
        payload = self.challenge_payload()
        before = self.protected()
        self.assertTrue(before["state"]["hazards"])
        for channel in ("Digital", "Phone"):
            code, detail = self.call(
                "/api/cases/ZF-1/resident", "sam", dict(payload, channel=channel)
            )
            self.assertEqual(code, 200, detail)
        code, detail = self.action(
            "challenge_resolve",
            id="CH-1",
            expected_version=1,
            resolution="Correction recorded",
            resolution_ref="SYN supplied human correction",
            explanation="SYN checked by a person",
            next_update="2099-01-02",
        )
        self.assertEqual(code, 200, detail)
        self.assertEqual(self.protected(), before)
        statuses = [
            v["status"] for v in self.store.cases["ZF-1"]["measure_decisions"]["Loft insulation"]
        ]
        self.assertEqual(statuses, ["Accepted"])

    def test_hazard_concern_is_routed_to_hazard_intake_and_saves_nothing(self) -> None:
        self.seed_hazard_and_consent()
        before = self.protected()
        hazards = copy.deepcopy(self.store.cases["ZF-1"]["hazards"])
        code, detail = self.call(
            "/api/cases/ZF-1/resident",
            "sam",
            dict(self.challenge_payload(), hazard_concern=True),
        )
        self.assertEqual(code, 400, detail)
        self.assertEqual(detail["route"], "independent_hazard_intake")
        self.assertTrue(detail["immediate"])
        self.assertIn("Nothing was saved", detail["message"])
        self.assertNotIn("affected_challenges", self.store.cases["ZF-1"])
        self.assertEqual(self.protected(), before)
        self.assertEqual(self.store.cases["ZF-1"]["hazards"], hazards)

    def test_raised_challenge_carries_explicit_assurance(self) -> None:
        self.seed_hazard_and_consent()
        hazards = copy.deepcopy(self.store.cases["ZF-1"]["hazards"])
        code, detail = self.call("/api/cases/ZF-1/resident", "sam", self.challenge_payload())
        self.assertEqual(code, 200, detail)
        self.assertEqual(self.store.cases["ZF-1"]["hazards"], hazards)
        record = self.store.cases["ZF-1"]["affected_challenges"][0]
        flags = ("no_retaliation", "inferred_refusal", "hazard_response_delayed")
        self.assertEqual(
            {k: record["assurance"][k] for k in flags},
            dict(no_retaliation=True, inferred_refusal=False, hazard_response_delayed=False),
        )

    def test_retaliating_writer_is_refused_and_nothing_saved(self) -> None:
        self.seed_hazard_and_consent()
        payload = self.challenge_payload()
        before = self.protected()
        original = challenges.protected_snapshot

        def snapshot_then_delay(c: Any) -> dict[str, Any]:
            snap: dict[str, Any] = original(c)
            c["hazards"][0]["response_due_at"] = "2099-01-01T00:00:00Z"
            return snap

        with patch.object(challenges, "protected_snapshot", snapshot_then_delay):
            code, refused = self.call("/api/cases/ZF-1/resident", "sam", payload)
        self.assertEqual(code, 400, refused)
        self.assertIn("Nothing was saved", json.dumps(refused))
        self.assertNotIn("affected_challenges", self.store.cases["ZF-1"])
        self.assertEqual(self.protected(), before)

    def test_api_and_ui_show_the_guarantees_only_to_permitted_readers(self) -> None:
        code, detail = self.call("/api/cases/ZF-1", "sam")
        self.assertEqual(code, 200)
        self.assertEqual(detail["challenge_guarantees"], list(challenges.GUARANTEES))
        for actor in ("rex", "bea", "kim"):
            denied = self.call("/api/cases/ZF-1", actor)[1]
            self.assertNotIn("challenge_guarantees", denied)
        self.assertEqual(detail["challenge_assurance"], challenges.assurance())
        self.assertNotIn("challenge_assurance", self.call("/api/cases/ZF-1", "rex")[1])
        script = self.call("/panels.js")[1]
        self.assertIn('id: "challenge-assurance"', script)
        self.assertIn("challenge_guarantees", script)
        self.assertIn('id: "challenge-guarantees"', script)
        self.assertNotIn("aria-invalid", script.split("challenge-guarantees")[1][:200])


for _name in dir(test_resident_api.ResidentApi):
    if _name.startswith("test_") and _name not in NonRetaliationApi.__dict__:
        setattr(NonRetaliationApi, _name, None)

if __name__ == "__main__":
    unittest.main()
