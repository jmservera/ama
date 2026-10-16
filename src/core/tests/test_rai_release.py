"""Pure release-contract semantics; constructed evidence, not human approval."""

import copy
import unittest
from typing import Any

from zava_forward.core import rai_release as rai


class ReleaseContract(unittest.TestCase):
    def setUp(self) -> None:
        self.task: dict[str, Any] = {
            "intended_use": "Draft only",
            "prohibited_uses": ["No sending"],
            "affected": ["Residents", "Staff"],
        }
        self.binding = {"model_version": "model-1", "prompt_version": "prompt-1"}
        self.record: dict[str, Any] = {
            **self.binding,
            "id": "r1",
            "status": "active",
            "release_version": "v1",
            "intended_use": "Draft only",
            "prohibited_uses": ["No sending"],
            "affected_stakeholders": ["Residents", "Staff"],
            "accountable_owner": "Fixture owner",
            "impact_assessment": "Constructed proposal review scenario",
            "material_change_triggers": list(rai.CHANGE_TRIGGERS),
            "evaluation_decision": "Pass",
            "evidence": ["fixture:evaluation-1"],
            "residual_risk_decision": "Accept",
            "residual_risk_note": "Synthetic only",
            "approver": {"email": "fixture@example.test"},
            "evidence_class": "constructed-fixture",
            "serving_model": "model-1",
            "expires": 200,
        }

    def select(self, record: dict[str, Any], live: bool = False) -> list[str]:
        return rai.select([record], self.task, self.binding, tuple(self.binding), 100, live)[1]

    def test_complete_fixture_matches_but_is_not_actual_authorization(self) -> None:
        self.assertEqual(self.select(self.record), [])
        self.assertIn(
            "actual authorisation with serving-version attestation",
            self.select(self.record, live=True),
        )
        self.record["evidence_class"] = "actual"
        self.assertEqual(self.select(self.record, live=True), [])

    def test_every_required_contract_field_fails_closed_when_missing(self) -> None:
        for key in (
            "release_version",
            "intended_use",
            "prohibited_uses",
            "affected_stakeholders",
            "accountable_owner",
            "impact_assessment",
            "material_change_triggers",
            "evaluation_decision",
            "evidence",
            "residual_risk_decision",
            "residual_risk_note",
            "approver",
            "evidence_class",
            "serving_model",
            "expires",
        ):
            with self.subTest(field=key):
                rec = copy.deepcopy(self.record)
                del rec[key]
                self.assertTrue(self.select(rec))

    def test_invalid_evidence_unknown_owner_and_expiry_boundaries(self) -> None:
        for key, value in (
            ("accountable_owner", "unknown"),
            ("evidence", []),
            ("evidence", [""]),
            ("expires", 100),
            ("expires", float("nan")),
            ("expires", "tomorrow"),
            ("expires", True),
        ):
            with self.subTest(field=key, value=value):
                self.assertTrue(self.select(dict(self.record, **{key: value})))

    def test_all_bound_versions_and_suspension_are_denied(self) -> None:
        for key in self.binding:
            self.assertIn(key, self.select(dict(self.record, **{key: "changed"})))
        self.assertTrue(self.select(dict(self.record, status="suspended")))

    def test_reference_changes_when_evaluation_or_use_changes(self) -> None:
        original = rai.reference(self.record)
        for key, value in (("evidence", ["fixture:renewed"]), ("impact_assessment", "New impact")):
            self.assertNotEqual(original, rai.reference(dict(self.record, **{key: value})))
        self.assertEqual(set(original), {"id", "version", "digest"})
