"""Meaningful human-review effectiveness gate and automation-bias tests (#223, AC-070)."""

from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from zava_forward.core.gates import FAIL, PASS, UNKNOWN, transition_allowed
from zava_forward.core.human_review_effectiveness import (
    DEFAULT_SCENARIOS,
    DEFECT_CLASSES,
    PROVISIONAL_AUTHORITY,
    SYNTHETIC_EVIDENCE_CLASS,
    SYNTHETIC_RELEASE,
    AuthorityPolicy,
    ReviewScenario,
    blank_worksheet,
    cites_memory,
    evaluate_panel,
    human_review_gate,
    is_valid_human_identity,
    pool_human_sessions,
    run_automation_bias_harness,
    score_human_session,
    synthetic_dataset,
)
from zava_forward.core.store import Store as _UntypedStore

Store: Any = _UntypedStore


def _make_store(root: Path) -> Any:
    data_path = root / "zavaforward.json"
    data_path.write_text(json.dumps(synthetic_dataset()), encoding="utf-8")
    store = Store(str(data_path))
    store.ai.fast = "synthetic-eval-223"
    store.ai.strong = "synthetic-eval-223"
    store.release_context = lambda _task, _dep=None: dict(SYNTHETIC_RELEASE)
    return store


def _seed_proposal(store: Any, reviewer: dict[str, Any], scenario: ReviewScenario) -> str:
    def _offline_run(
        _task: str,
        _sysmsg: str,
        _prompt: str,
        template: str,
        _strong: bool = False,
        _check: Any = None,
        *,
        off: bool = False,
    ) -> dict[str, Any]:
        if off:
            return {
                "text": template,
                "source": "template",
                "model": None,
                "reason": "workflow-only mode selected",
                "validated": True,
                "latency_ms": 1.0,
            }
        return {
            "text": scenario.proposal_text,
            "source": "ai",
            "model": "synthetic-eval-223",
            "release": dict(SYNTHETIC_RELEASE),
            "reason": None,
            "validated": True,
            "latency_ms": 10.0,
        }

    store.ai.run = _offline_run
    out = store.ai_run(reviewer, scenario.case_id, scenario.task)
    return str(out["record_id"])


class HumanReviewEffectiveness223Tests(unittest.TestCase):
    def test_seeded_defects_all_carry_valid_citations_across_tasks_and_classes(self) -> None:
        report = evaluate_panel("competent")
        rows = report["scenarios"]
        self.assertEqual(len(rows), 8)
        self.assertEqual(
            {row["defect_class"] for row in rows},
            {"wrong", "stale", "unsupported", "incomplete", "none"},
        )
        self.assertEqual({row["task"] for row in rows}, {"summary", "message"})
        # Every seeded defect and control carries resolving inline citations (verified == True),
        # proving citation validity alone cannot separate defective from accurate drafts.
        self.assertTrue(all(row["citation_verified"] is True for row in rows))

    def test_competent_panel_detects_all_defects_retains_evidence_and_compares_effort(self) -> None:
        report = evaluate_panel("competent")
        self.assertEqual(report["evidence_class"], SYNTHETIC_EVIDENCE_CLASS)
        self.assertFalse(report["human_trial_complete"])
        self.assertEqual(report["seeded_defect_count"], 6)
        self.assertEqual(report["detected_count"], 6)
        self.assertEqual(report["detection_rate"], 1.0)
        for cls in DEFECT_CLASSES:
            self.assertEqual(report["by_defect_class"][cls]["detection_rate"], 1.0)
        self.assertEqual(report["corrections"], 3)
        self.assertEqual(report["rejections"], 3)
        self.assertEqual(report["false_rejects"], 0)
        self.assertEqual(report["gate_passed_count"], 8)
        self.assertEqual(report["gate_leakage"], 0)
        self.assertTrue(report["retained_evidence_complete"])
        self.assertTrue(report["audit_verified"])

        expected_wf = sum(s.workflow_seconds for s in DEFAULT_SCENARIOS)
        expected_ai = sum(s.competent_review_seconds for s in DEFAULT_SCENARIOS)
        self.assertEqual(report["total_workflow_seconds"], expected_wf)
        self.assertEqual(report["total_ai_review_seconds"], expected_ai)
        self.assertEqual(report["net_effort_delta_seconds"], expected_ai - expected_wf)

        for row in report["scenarios"]:
            self.assertEqual(row["reviewer"], "amina.patel@example.test")
            self.assertTrue(row["reviewer_reason"])
            self.assertTrue(row["source_hashes"])
            self.assertTrue(row["workflow_text"])
            self.assertTrue(row["retained_evidence"])
            self.assertTrue(row["transition_allowed"])
            self.assertEqual(row["gate"]["outcome"], PASS)

    def test_automation_bias_default_accept_citation_only_and_unauthorised_fail_gate(self) -> None:
        harness = run_automation_bias_harness()
        self.assertTrue(harness["automation_bias_exposed"])
        self.assertFalse(harness["human_trial_complete"])
        panels = harness["panels"]

        default_acc = panels["default_accept"]
        self.assertEqual(default_acc["detection_rate"], 0.0)
        self.assertEqual(default_acc["gate_passed_count"], 0)
        self.assertEqual(default_acc["gate_leakage"], 0)

        cite_only = panels["citation_only"]
        self.assertEqual(cite_only["detection_rate"], 0.0)
        self.assertEqual(cite_only["gate_passed_count"], 0)
        self.assertEqual(cite_only["gate_leakage"], 0)
        for row in cite_only["scenarios"]:
            self.assertFalse(row["transition_allowed"])
            self.assertEqual(row["gate"]["outcome"], FAIL)
            if row["defect_class"] != "none":
                self.assertIn("citation_validity_alone_insufficient", row["gate"]["reason"])

        biased = panels["automation_bias"]
        # Checks hedged proposals (catching S-223-05 and verifying S-223-07) while rubber-stamping
        # all 5 confident citation-valid defects and confident control S-223-08.
        self.assertEqual(biased["detected_count"], 1)
        self.assertEqual(biased["seeded_defect_count"], 6)
        self.assertAlmostEqual(biased["detection_rate"], round(1 / 6, 4))
        self.assertEqual(biased["gate_leakage"], 0)
        self.assertEqual(biased["gate_passed_count"], 2)

        unauthorised = panels["unauthorised_competent"]
        self.assertEqual(unauthorised["detection_rate"], 1.0)
        self.assertEqual(unauthorised["gate_passed_count"], 0)
        self.assertEqual(unauthorised["gate_leakage"], 0)
        for row in unauthorised["scenarios"]:
            self.assertIn("reviewer_role_not_authorised", row["gate"]["reason"])

    def test_adversarial_gate_bypasses_and_staleness_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store = _make_store(Path(tmp))
            rlo = dict(store.staff["amina.patel@example.test"])
            bsl = dict(store.staff["bea.safe@example.test"])
            wrong_scenario = DEFAULT_SCENARIOS[0]  # S-223-01 (summary, wrong)
            valid_msg = DEFAULT_SCENARIOS[7]  # S-223-08 (message, none)

            # 1. Unreviewed proposal -> UNKNOWN
            rec_id = _seed_proposal(store, rlo, wrong_scenario)
            unreviewed = next(r for r in store.data["recommendations"] if r["id"] == rec_id)
            gate_unrev = human_review_gate(unreviewed, store=store, scenario=wrong_scenario)
            self.assertEqual(gate_unrev.outcome, UNKNOWN)
            self.assertFalse(transition_allowed([gate_unrev]))

            # 2. Missing authority policy or future effective date -> UNKNOWN
            self.assertEqual(
                human_review_gate(unreviewed, store=store, authority=None).outcome, UNKNOWN
            )
            self.assertEqual(
                human_review_gate(unreviewed, store=store, on="2025-12-31").outcome, UNKNOWN
            )

            # 3. Cosmetic edit retaining the wrong "hazard is resolved" claim -> FAIL
            cosmetic = store.review_ai(
                rlo,
                rec_id,
                "edit",
                "Checked Open safety issues: 1 and Safety issue: Damp and mould carefully.",
                wrong_scenario.proposal_text
                + "\n- Extra support is needed. [[Extra support: needed]]",
            )
            gate_cosmetic = human_review_gate(
                cosmetic, store=store, staff_member=rlo, scenario=wrong_scenario
            )
            self.assertEqual(gate_cosmetic.outcome, FAIL)
            self.assertIn("ineffective_edit_retains_or_introduces_defect", gate_cosmetic.reason)

            # 4. Edit introducing an unresolved inline citation -> FAIL
            rec_bad_cite_id = _seed_proposal(store, rlo, wrong_scenario)
            bad_cite_rev = store.review_ai(
                rlo,
                rec_bad_cite_id,
                "edit",
                "Checked Open safety issues: 1 and Safety issue: Damp and mould on file.",
                (
                    "- Case at Final checks before ordering with 1 open Damp and mould safety "
                    "issue and extra support needed. [[Fabricated source: clear]]"
                ),
            )
            gate_bad_cite = human_review_gate(
                bad_cite_rev, store=store, staff_member=rlo, scenario=wrong_scenario
            )
            self.assertEqual(gate_bad_cite.outcome, FAIL)
            self.assertIn("unresolved_or_missing_case_citations", gate_bad_cite.reason)

            # 5. Reason citing an unrelated case field instead of resolving safety source -> FAIL
            rec_unrel_id = _seed_proposal(store, rlo, wrong_scenario)
            unrel_rev = store.review_ai(
                rlo,
                rec_unrel_id,
                "reject",
                "Rejected after checking Address: 223 Synthetic Terrace and EPC band: D.",
            )
            gate_unrel = human_review_gate(
                unrel_rev, store=store, staff_member=rlo, scenario=wrong_scenario
            )
            self.assertEqual(gate_unrel.outcome, FAIL)
            self.assertIn("missing_resolving_case_source_in_reason", gate_unrel.reason)

            # 6. Canonical and conversational chat-memory reasons -> FAIL
            for mem_reason in (
                "Rejected per CM-abcdef0123456789 and Open safety issues: 1.",
                "Rejected because earlier in chat the assistant said Open safety issues: 1.",
            ):
                self.assertTrue(cites_memory(mem_reason))
                rec_mem_id = _seed_proposal(store, rlo, wrong_scenario)
                mem_rev = store.review_ai(rlo, rec_mem_id, "reject", mem_reason)
                gate_mem = human_review_gate(
                    mem_rev, store=store, staff_member=rlo, scenario=wrong_scenario
                )
                self.assertEqual(gate_mem.outcome, FAIL)
                self.assertIn("memory_reference_not_authoritative_source", gate_mem.reason)

            # 7. Placeholder and non-human reviewer identities -> FAIL
            for bad_actor in ("TBD", "pending", "copilot@example.test", "workflow-agent", "n/a"):
                self.assertFalse(is_valid_human_identity(bad_actor))
                forged = copy.deepcopy(unrel_rev)
                forged["resolved_by"] = bad_actor
                forged["review_evidence"]["reviewer"] = bad_actor
                gate_actor = human_review_gate(forged, store=store, scenario=wrong_scenario)
                self.assertEqual(gate_actor.outcome, FAIL)
                self.assertIn("unnamed_or_non_human_reviewer", gate_actor.reason)

            # 8. Task-scope mismatch (Building Safety Liaison authorised for summary, not message)
            rec_msg_id = _seed_proposal(store, bsl, valid_msg)
            msg_rev = store.review_ai(
                bsl,
                rec_msg_id,
                "accept",
                valid_msg.competent_reason,
            )
            gate_scope = human_review_gate(
                msg_rev, store=store, staff_member=bsl, scenario=valid_msg
            )
            self.assertEqual(gate_scope.outcome, FAIL)
            self.assertIn("reviewer_not_authorised_for_task", gate_scope.reason)

            # 9. Pre-review case mutation triggers Store Hold -> FAIL
            rec_hold_id = _seed_proposal(store, rlo, wrong_scenario)
            store._case(wrong_scenario.case_id)["stage"] = "Install booked"
            with self.assertRaises(ValueError):
                store.review_ai(rlo, rec_hold_id, "reject", wrong_scenario.competent_reason)
            held_rec = next(r for r in store.data["recommendations"] if r["id"] == rec_hold_id)
            self.assertEqual(held_rec["status"], "Hold")
            gate_held = human_review_gate(held_rec, store=store, staff_member=rlo)
            self.assertEqual(gate_held.outcome, FAIL)
            self.assertIn("stale_or_quarantined_proposal", gate_held.reason)

            # 10. Post-review case mutation invalidates previously passing review -> FAIL
            store._case(wrong_scenario.case_id)["stage"] = "Final checks before ordering"
            rec_fresh_id = _seed_proposal(store, rlo, wrong_scenario)
            good_rev = store.review_ai(
                rlo,
                rec_fresh_id,
                "edit",
                wrong_scenario.competent_reason,
                wrong_scenario.competent_text,
            )
            self.assertEqual(
                human_review_gate(
                    good_rev, store=store, staff_member=rlo, scenario=wrong_scenario
                ).outcome,
                PASS,
            )
            store._case(wrong_scenario.case_id)["days_in_stage"] = 99
            gate_stale_after = human_review_gate(
                good_rev, store=store, staff_member=rlo, scenario=wrong_scenario
            )
            self.assertEqual(gate_stale_after.outcome, FAIL)
            self.assertIn("stale_case_sources", gate_stale_after.reason)
            self.assertTrue(store.verify_audit())

    def test_live_mode_fails_closed_until_named_human_oq017_approval(self) -> None:
        provisional_live = evaluate_panel("competent", authority=PROVISIONAL_AUTHORITY, live=True)
        self.assertEqual(provisional_live["gate_passed_count"], 0)
        for row in provisional_live["scenarios"]:
            self.assertEqual(row["gate"]["outcome"], FAIL)
            self.assertIn("provisional_authority_unapproved_for_live_gate", row["gate"]["reason"])

        placeholder_auth = AuthorityPolicy(
            policy_id="bad-live-auth",
            provisional=False,
            authority_gap="OQ-017",
            allowed_roles=PROVISIONAL_AUTHORITY.allowed_roles,
            approved_by="TBD",
            approved_on="2026-01-20",
        )
        bad_live = evaluate_panel("competent", authority=placeholder_auth, live=True)
        self.assertEqual(bad_live["gate_passed_count"], 0)

        approved_fixture = AuthorityPolicy(
            policy_id="synthetic-approved-auth-fixture",
            provisional=False,
            authority_gap="Synthetic test fixture only",
            allowed_roles=PROVISIONAL_AUTHORITY.allowed_roles,
            approved_by="Clara Example",
            approved_on="2026-01-20",
        )
        good_live = evaluate_panel("competent", authority=approved_fixture, live=True)
        self.assertEqual(good_live["gate_passed_count"], 8)
        self.assertEqual(good_live["gate_leakage"], 0)

    def test_blank_worksheet_has_no_spoilers_and_human_sessions_pool_safely(self) -> None:
        sheet = blank_worksheet()
        self.assertEqual(len(sheet["items"]), 8)
        dumped = json.dumps(sheet)
        for spoiler in (
            "defect_class",
            "confidence",
            "forbidden_claims",
            "required_facts",
            "competent_reason",
            "resolving_sources",
        ):
            self.assertNotIn(spoiler, dumped)

        sub_one: dict[str, Any] = {
            "reviewer": {
                "name": "Priya Nair",
                "email": "priya.nair@example.test",
                "role": "Resident Liaison Officer",
            },
            "items": [
                {
                    "scenario_id": s.scenario_id,
                    "response": {
                        "disposition": s.competent_action,
                        "edited_text": s.competent_text,
                        "reason": s.competent_reason,
                        "review_seconds": s.competent_review_seconds,
                    },
                }
                for s in DEFAULT_SCENARIOS
            ],
        }
        sub_two: dict[str, Any] = {
            "reviewer": {
                "name": "Liam Brooks",
                "email": "liam.brooks@example.test",
                "role": "Retrofit Coordinator",
            },
            "items": [
                {
                    "scenario_id": s.scenario_id,
                    "response": {
                        "disposition": (
                            "accept" if s.confidence == "confident" else s.competent_action
                        ),
                        "edited_text": None if s.confidence == "confident" else s.competent_text,
                        "reason": (
                            "Quickly accepted confident citation-verified draft."
                            if s.confidence == "confident"
                            else s.competent_reason
                        ),
                        "review_seconds": s.biased_review_seconds,
                    },
                }
                for s in DEFAULT_SCENARIOS
            ],
        }

        pooled = pool_human_sessions([sub_one, sub_two])
        self.assertEqual(pooled["participant_count"], 2)
        self.assertFalse(pooled["oq017_live_approved"])
        self.assertEqual(pooled["evidence_class"], "pooled_human_sessions_provisional_oq017")
        self.assertEqual(pooled["total_seeded_defects"], 12)
        self.assertEqual(pooled["total_detected_defects"], 7)
        self.assertEqual(pooled["total_gate_leakage"], 0)

        with self.assertRaises(ValueError):
            pool_human_sessions([sub_one, copy.deepcopy(sub_one)])

        bad_timing = copy.deepcopy(sub_one)
        bad_timing["items"][0]["response"]["review_seconds"] = 0
        with self.assertRaises(ValueError):
            score_human_session(bad_timing)

        bool_timing = copy.deepcopy(sub_one)
        bool_timing["items"][0]["response"]["review_seconds"] = True
        with self.assertRaises(ValueError):
            score_human_session(bool_timing)

    def test_reviewer_identity_must_be_a_concrete_human(self) -> None:
        for bad in ("TBD", "unassigned", "Workflow Agent", "model reviewer", "", None, 42):
            self.assertFalse(is_valid_human_identity(bad), bad)
        self.assertTrue(is_valid_human_identity("Priya Nair"))
        self.assertTrue(is_valid_human_identity("priya.nair@example.test"))

    def test_memory_citations_are_detected_but_plain_reasons_are_not(self) -> None:
        for text in (
            "As the assistant said earlier",
            "taken from memory",
            "Per the previous prompt",
        ):
            self.assertTrue(cites_memory(text), text)
        self.assertFalse(cites_memory("Checked the survey record and the EPC certificate."))
        self.assertFalse(cites_memory(None))

    def test_human_session_scoring_refuses_malformed_submissions(self) -> None:
        def good() -> dict[str, Any]:
            return {
                "reviewer": {
                    "name": "Priya Nair",
                    "email": "priya.nair@example.test",
                    "role": "Resident Liaison Officer",
                },
                "items": [
                    {
                        "scenario_id": s.scenario_id,
                        "response": {
                            "disposition": s.competent_action,
                            "edited_text": s.competent_text,
                            "reason": s.competent_reason,
                            "review_seconds": s.competent_review_seconds,
                        },
                    }
                    for s in DEFAULT_SCENARIOS
                ],
            }

        score_human_session(good())

        def broken(mutate: Any) -> dict[str, Any]:
            sub = good()
            mutate(sub)
            return sub

        cases = {
            "no reviewer": lambda s: s.pop("reviewer"),
            "agent name": lambda s: s["reviewer"].update(name="Workflow Agent"),
            "no at sign": lambda s: s["reviewer"].update(email="priya.nair"),
            "no role": lambda s: s["reviewer"].update(role=" "),
            "items string": lambda s: s.update(items="all"),
            "omitted scenario": lambda s: s["items"].pop(),
            "duplicate scenario": lambda s: s["items"].append(copy.deepcopy(s["items"][0])),
            "unknown scenario": lambda s: s["items"][0].update(scenario_id="not-a-scenario"),
            "bad disposition": lambda s: s["items"][0]["response"].update(disposition="approve"),
        }
        for label, mutate in cases.items():
            with self.subTest(label), self.assertRaises(ValueError):
                score_human_session(broken(mutate))


if __name__ == "__main__":
    unittest.main()
