"""Edge cases of the pure RAI release validator (issue 218); constructed evidence only."""

import copy
import unittest
from typing import Any

from zava_forward.core import monitoring_coverage as mc
from zava_forward.core import rai_release as rai


class ReleaseEdges(unittest.TestCase):
    def setUp(self) -> None:
        self.task: dict[str, Any] = {
            "intended_use": "Draft only",
            "prohibited_uses": ["No sending"],
            "affected": ["Residents"],
            "scope": "Constructed exercise only",
        }
        self.binding = {"model_version": "model-1", "prompt_version": "prompt-1"}
        self.record: dict[str, Any] = {
            **self.binding,
            "id": "r1",
            "status": "active",
            "release_version": "v1",
            "intended_use": "Draft only",
            "prohibited_uses": ["No sending"],
            "affected_stakeholders": ["Residents"],
            "accountable_owner": "Fixture owner",
            "impact_assessment": "Constructed review scenario",
            "material_change_triggers": list(rai.CHANGE_TRIGGERS),
            "evaluation_decision": "Pass",
            "evidence": ["fixture:evaluation-1"],
            "residual_risk_decision": "Accept",
            "residual_risk_note": "Synthetic only",
            "approver": {"email": "fixture@example.test"},
            "evidence_class": "constructed-fixture",
            "serving_model": "model-1",
            "expires": 200,
            "scope": "Constructed exercise only",
            "evaluation_summary": {
                "evaluation_version": rai.EVALUATION_VERSION,
                "decision": "Pass",
                "summary": "Frozen synthetic evaluation",
                "evidence_digest": rai.digest(["fixture:evaluation-1"]),
            },
            "consumption": {
                "max_calls": 100,
                "max_tokens": 200000,
                "alert_threshold_percent": 80,
                "alert_contact": "Fixture owner",
            },
            "monitoring_declaration": mc.task_declaration("stock-prioritisation"),
        }

    def select(self, records: list[dict[str, Any]], live: bool = False) -> Any:
        return rai.select(records, self.task, self.binding, tuple(self.binding), 100, live)

    def test_named_human_rejects_system_attributions(self) -> None:
        self.assertTrue(rai.named_human("Amina Okafor"))
        for value in (
            "Release Bot",
            "copilot",
            "AI-reviewer",
            "system@example.test",
            "unknown",
            " ",
        ):
            with self.subTest(value=value):
                self.assertFalse(rai.named_human(value))
        self.assertFalse(rai.named_human(None))

    def test_consumption_bounds_are_inclusive_and_typed(self) -> None:
        good = self.record["consumption"]
        self.assertTrue(
            rai.valid_consumption(dict(good, max_calls=10**9, alert_threshold_percent=100))
        )
        for key, value in (
            ("max_calls", 10**9 + 1),
            ("max_tokens", 10**12 + 1),
            ("alert_threshold_percent", 0),
            ("max_calls", 1.5),
        ):
            with self.subTest(key=key, value=value):
                self.assertFalse(rai.valid_consumption(dict(good, **{key: value})))
        self.assertFalse(rai.valid_consumption(["max_calls"]))

    def test_frozen_evaluation_needs_summary_text(self) -> None:
        self.assertTrue(rai.frozen_evaluation(self.record))
        empties: tuple[Any, ...] = (None, "", {})
        for summary in empties:
            with self.subTest(summary=summary):
                self.assertFalse(
                    rai.frozen_evaluation(dict(self.record, evaluation_summary=summary))
                )
        blank = dict(self.record["evaluation_summary"], summary=" ")
        self.assertFalse(rai.frozen_evaluation(dict(self.record, evaluation_summary=blank)))

    def test_contract_reports_the_specific_gap(self) -> None:
        self.assertEqual(rai.missing_contract(self.record, self.task), [])
        for key, value, gap in (
            (
                "material_change_triggers",
                list(reversed(rai.CHANGE_TRIGGERS)),
                "material_change_triggers",
            ),
            ("residual_risk_decision", "Reject", "residual-risk acceptance"),
            ("evidence_class", "guess", "evidence_class"),
            ("approver", {}, "named release approver"),
            ("evaluation_decision", "Fail", "approved evaluation evidence"),
        ):
            with self.subTest(key=key):
                self.assertEqual(
                    rai.missing_contract(dict(self.record, **{key: value}), self.task), [gap]
                )

    def test_each_trigger_family_is_detected_alone_in_canonical_order(self) -> None:
        for trigger, key in (
            ("model", "deployment"),
            ("prompt", "prompt_version"),
            ("policy", "policy_version"),
            ("data", "provenance_version"),
            ("permissions", "permission_version"),
            ("evidence", "schema_version"),
        ):
            with self.subTest(trigger=trigger):
                binding = dict(self.binding, **{key: "new"})
                if key != "prompt_version":
                    self.record.pop(key, None)
                self.assertEqual(rai.changed_triggers(self.record, self.task, binding), [trigger])
        binding = dict(self.binding, prompt_version="p2", policy_version="x", provider="y")
        self.assertEqual(
            rai.changed_triggers(self.record, self.task, binding), ["model", "prompt", "policy"]
        )

    def test_select_prefers_newest_valid_and_falls_back_when_newest_is_invalid(self) -> None:
        older = dict(self.record, id="old", release_version="v0")
        newer = dict(self.record, id="new", release_version="v2")
        chosen, gaps = self.select([older, newer])
        self.assertEqual((chosen["id"], gaps), ("new", []))
        broken = copy.deepcopy(newer)
        broken["evaluation_decision"] = "Fail"
        chosen, gaps = self.select([older, broken])
        self.assertEqual((chosen["id"], gaps), ("old", []))

    def test_select_ignores_inactive_and_reports_default_gap_when_empty(self) -> None:
        for records in ([], [dict(self.record, status="suspended")]):
            chosen, gaps = self.select(records)
            self.assertIsNone(chosen)
            self.assertEqual(gaps, ["approved, unexpired release record"])

    def test_live_binding_rejects_non_human_approver_and_bad_named_approval(self) -> None:
        live = dict(self.record, evidence_class="actual", approver={"email": "release-bot"})
        self.assertIn(
            "named human release approver",
            rai.missing_binding(live, self.binding, tuple(self.binding), 100, True),
        )
        live = dict(
            self.record, evidence_class="actual", approved_by="system", named_approval_id="x"
        )
        gaps = rai.missing_binding(live, self.binding, tuple(self.binding), 100, True)
        self.assertIn("named human approved_by (OQ-017)", gaps)
        self.assertIn("named_approval_id (OQ-017)", gaps)


if __name__ == "__main__":
    unittest.main()
