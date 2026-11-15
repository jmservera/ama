"""Offline RAI held-out evaluation and prompt/tuning isolation tests (Issue #108)."""

from __future__ import annotations

import copy
import json
import unittest
from typing import Any

from zava_forward.core import (
    ai_consumption,
    ai_prompts,
    ai_registry,
    assistants,
    cohort_eval,
    heldout_eval,
)


class HeldoutEvalTest(unittest.TestCase):
    def test_canonical_suite_covers_all_eleven_capabilities_and_five_dimensions(self) -> None:
        suite = heldout_eval.canonical_offline_heldout_suite()
        self.assertEqual(suite["outcome"], "pass")
        self.assertTrue(suite["synthetic"])
        self.assertFalse(suite["live_clearance"])
        self.assertTrue(suite["freeze"]["ready_for_evaluation"])
        self.assertTrue(suite["isolation"]["isolated"])

        denom = suite["denominators"]
        self.assertEqual(denom["frozen_total"], 16)
        self.assertEqual(denom["evaluated_total"], 16)
        self.assertEqual(denom["usable_total"], 16)
        self.assertEqual(denom["passed_total"], 16)

        expected_caps = set(assistants.REGISTRY) | set(ai_registry.LEGACY)
        self.assertEqual(len(expected_caps), 11)
        self.assertEqual(set(denom["by_capability"]), expected_caps)
        for cap, counts in denom["by_capability"].items():
            self.assertGreaterEqual(counts["denominator"], 1, cap)
            self.assertEqual(counts["passed"], counts["denominator"], cap)

        self.assertEqual(set(denom["by_dimension"]), set(heldout_eval.DIMENSIONS))
        for dim, counts in denom["by_dimension"].items():
            self.assertGreaterEqual(counts["denominator"], 1, dim)
            self.assertEqual(counts["passed"], counts["denominator"], dim)

        self.assertEqual(
            suite["actual_serving_version"]["reported"],
            heldout_eval.OFFLINE_SERVING_VERSION,
        )
        self.assertEqual(suite["unknown_liabilities"]["count"], 0)
        self.assertEqual(suite["critical_errors"]["count"], 0)
        self.assertEqual(suite["critical_misses"]["count"], 0)
        self.assertEqual(suite["calibration"]["applicable"], False)
        self.assertEqual(suite["calibration"]["status"], "not_applicable")
        self.assertEqual(suite["seed"], 20261115)
        self.assertIn("evaluation_digest", suite["hashes"])
        self.assertTrue(suite["reviewer_protocol"]["blind_to_expected_answers"])

    def test_freeze_rejects_missing_versions_and_missing_capability_versions(self) -> None:
        manifest = heldout_eval.canonical_heldout_manifest()
        broken_top = copy.deepcopy(manifest)
        broken_top["versions"]["policy"] = ""
        res_top = heldout_eval.check_heldout_freeze(broken_top)
        self.assertFalse(res_top["frozen"])
        self.assertIn("missing_frozen_versions", res_top["blockers"])

        broken_cap = copy.deepcopy(manifest)
        del broken_cap["capability_versions"]["read_document"]
        res_cap = heldout_eval.check_heldout_freeze(broken_cap)
        self.assertFalse(res_cap["frozen"])
        self.assertTrue(
            any(b.startswith("missing_capability_versions") for b in res_cap["blockers"])
        )

        eval_out = heldout_eval.evaluate_heldout(
            broken_cap, heldout_eval.canonical_baseline_responses()
        )
        self.assertEqual(eval_out["outcome"], "fail")

    def test_freeze_rejects_unapproved_or_tampered_thresholds_and_manifest_body(self) -> None:
        manifest = heldout_eval.canonical_heldout_manifest()

        unapproved = copy.deepcopy(manifest)
        del unapproved["threshold_approval"]
        self.assertIn(
            "missing_threshold_approval",
            heldout_eval.check_heldout_freeze(unapproved)["blockers"],
        )

        tampered_threshold = copy.deepcopy(manifest)
        tampered_threshold["thresholds"]["max_critical_misses"] = 2
        threshold_check = heldout_eval.check_heldout_freeze(tampered_threshold)
        self.assertIn("thresholds_digest_mismatch", threshold_check["blockers"])
        self.assertIn("manifest_digest_mismatch", threshold_check["blockers"])

        # Mutating non-threshold frozen fields after approval must also break manifest_digest.
        tampered_version = copy.deepcopy(manifest)
        tampered_version["versions"]["prompt"] = "tampered-prompt-v9"
        body_check = heldout_eval.check_heldout_freeze(tampered_version)
        self.assertFalse(body_check["frozen"])
        self.assertIn("manifest_digest_mismatch", body_check["blockers"])

    def test_freeze_rejects_non_independent_or_non_human_labeller_and_approver(self) -> None:
        manifest = heldout_eval.canonical_heldout_manifest()
        same_author = copy.deepcopy(manifest)
        same_author["held_out"]["labelled_by"] = same_author["held_out"]["prompt_author"]
        same_author = heldout_eval.approve_manifest(
            same_author,
            approved_by="Claire Whittaker",
            approved_at="2026-11-12T11:00:00Z",
        )
        check = heldout_eval.check_heldout_freeze(same_author)
        self.assertIn("non_independent_heldout_labeller", check["blockers"])

        with self.assertRaises(ValueError):
            heldout_eval.approve_manifest(
                manifest,
                approved_by="automated-copilot-bot",
                approved_at="2026-11-12T11:00:00Z",
            )
        with self.assertRaises(ValueError):
            heldout_eval.approve_manifest(
                manifest,
                approved_by="Claire Whittaker",
                approved_at="2026-11-12T11:00:00",  # missing timezone
            )

    def test_freeze_rejects_synthetic_manifest_when_live_mode_requested(self) -> None:
        manifest = heldout_eval.canonical_heldout_manifest()
        live_check = heldout_eval.check_heldout_freeze(manifest, live=True)
        self.assertFalse(live_check["frozen"])
        self.assertIn("synthetic_manifest_rejected_for_live", live_check["blockers"])

        eval_live = heldout_eval.evaluate_heldout(
            manifest,
            heldout_eval.canonical_baseline_responses(),
            offline_scripted=False,
        )
        self.assertEqual(eval_live["outcome"], "fail")
        self.assertIn(
            "freeze:synthetic_manifest_rejected_for_live",
            eval_live["failure_reasons"],
        )

    def test_freeze_rejects_heldout_overlap_with_prompt_tuning_or_calibration_splits(self) -> None:
        manifest = heldout_eval.canonical_heldout_manifest()
        leaked = copy.deepcopy(manifest)
        leaked["tuning_case_ids"].append("HO-LEG-PR-01")
        leaked = heldout_eval.approve_manifest(
            leaked,
            approved_by="Claire Whittaker",
            approved_at="2026-11-12T11:00:00Z",
        )
        check = heldout_eval.check_heldout_freeze(leaked)
        self.assertFalse(check["frozen"])
        self.assertTrue(
            any("heldout_case_id_overlap:tuning_case_ids" in b for b in check["blockers"])
        )

    def test_prompt_tuning_isolation_checks_registered_templates_and_catches_leaks(self) -> None:
        manifest = heldout_eval.canonical_heldout_manifest()
        clean = heldout_eval.check_prompt_tuning_isolation(manifest)
        self.assertTrue(clean["isolated"])
        self.assertEqual(set(clean["checked_assistant_templates"]), set(assistants.REGISTRY))
        self.assertEqual(set(clean["checked_legacy_templates"]), set(ai_prompts.PROMPTS))

        # Leak a held-out case ID into a caller prompt.
        id_leak = heldout_eval.check_prompt_tuning_isolation(
            manifest,
            rendered_prompts=["Few-shot example from case HO-AST-FE-02 showing missing doc."],
        )
        self.assertFalse(id_leak["isolated"])
        self.assertIn("HO-AST-FE-02", id_leak["leaked_case_ids"])

        # Leak a 6-word phrase from expected_answer into tuning examples without case ID.
        answer_snippet = (
            "captured humidity sensor stream carries conflicting readings at identical timestamps"
        )
        ans_leak = heldout_eval.check_prompt_tuning_isolation(
            manifest,
            tuning_examples=[{"assistant": answer_snippet}],
        )
        self.assertFalse(ans_leak["isolated"])
        self.assertIn("HO-AST-QE-02", ans_leak["leaked_answer_case_ids"])

        eval_leaked = heldout_eval.evaluate_heldout(
            manifest,
            heldout_eval.canonical_baseline_responses(),
            tuning_examples=[{"assistant": answer_snippet}],
        )
        self.assertEqual(eval_leaked["outcome"], "fail")

    def test_insufficient_cohort_sample_and_missing_response_report_insufficient_outcome(
        self,
    ) -> None:
        manifest = heldout_eval.canonical_heldout_manifest()
        raised_floor = copy.deepcopy(manifest)
        raised_floor["cohorts"]["complete_evidence"]["min_n"] = 9
        raised_floor = heldout_eval.approve_manifest(
            raised_floor,
            approved_by="Claire Whittaker",
            approved_at="2026-11-12T11:00:00Z",
        )
        freeze = heldout_eval.check_heldout_freeze(raised_floor)
        self.assertTrue(freeze["frozen"])
        self.assertFalse(freeze["sample_sufficient"])
        self.assertFalse(freeze["ready_for_evaluation"])

        eval_insuff = heldout_eval.evaluate_heldout(
            raised_floor,
            heldout_eval.canonical_baseline_responses(),
        )
        self.assertEqual(eval_insuff["outcome"], "insufficient")
        self.assertTrue(
            any("cohort:complete_evidence:5<9" in r for r in eval_insuff["insufficient_reasons"])
        )

        partial_responses = heldout_eval.canonical_baseline_responses()
        del partial_responses["HO-LEG-RD-01"]
        eval_missing = heldout_eval.evaluate_heldout(manifest, partial_responses)
        self.assertEqual(eval_missing["outcome"], "insufficient")

    def test_subgroup_results_stay_unaveraged_with_synthetic_non_fairness_notice(self) -> None:
        manifest = heldout_eval.canonical_heldout_manifest()
        suite = heldout_eval.canonical_offline_heldout_suite()
        sub = suite["subgroup_results"]
        self.assertEqual(sub["aggregation_rule"], "per_cohort_unaveraged")
        self.assertIsNone(sub["cross_cohort_average"])
        self.assertFalse(sub["fairness_evidence"])
        self.assertEqual(sub["provenance_notice"], cohort_eval.SYNTHETIC_NON_FAIRNESS_NOTICE)

        # Relax global counters/coverage so one cohort's pass rate hits min_subgroup_pass_rate.
        relaxed = copy.deepcopy(manifest)
        relaxed["thresholds"]["max_critical_errors"] = 5
        relaxed["thresholds"]["max_unsupported_claims"] = 5
        relaxed["thresholds"]["min_usable_coverage"] = 0.80
        relaxed["thresholds"]["min_subgroup_pass_rate"] = 0.95
        relaxed = heldout_eval.approve_manifest(
            relaxed,
            approved_by="Claire Whittaker",
            approved_at="2026-11-12T11:00:00Z",
        )
        bad_resp = heldout_eval.canonical_baseline_responses()
        bad_resp["HO-LEG-RD-01"]["text"] = "Filing note with bogus label [[Bogus: 1]]."
        out = heldout_eval.evaluate_heldout(relaxed, bad_resp)
        self.assertEqual(out["outcome"], "fail")
        self.assertIn("subgroup_below_threshold:complete_evidence", out["failure_reasons"])

    def test_controls_ambiguity_abstention_source_integrity_and_factual_support_failures(
        self,
    ) -> None:
        manifest = heldout_eval.canonical_heldout_manifest()
        responses: dict[str, dict[str, Any]] = heldout_eval.canonical_baseline_responses()

        # 1. Controls violation (forbidden autonomous action claim in resident coordination)
        bad_wc = json.loads(responses["HO-AST-WC-01"]["provider_result"]["text"])
        bad_wc["summary"] = "Email sent and appointment has now been booked automatically."
        responses["HO-AST-WC-01"]["provider_result"]["text"] = json.dumps(bad_wc)

        # 2. Ambiguity violation (omits conflicting sensor citation on quality-evidence)
        bad_qe = json.loads(responses["HO-AST-QE-02"]["provider_result"]["text"])
        bad_qe["summary"] = "Humidity is fine."
        bad_qe["findings"] = [{"text": "All readings normal.", "citations": ["source:sensors"]}]
        responses["HO-AST-QE-02"]["provider_result"]["text"] = json.dumps(bad_qe)

        # 3. Abstention violation (funding_draft omits 'Needs:' marker and invents certainty)
        responses["HO-LEG-FD-01"]["text"] = (
            "All compliance certificates are complete [[Home type: Semi-detached]]."
        )

        # 4. Source integrity violation (fabricated citation locator)
        responses["HO-LEG-SU-01"]["text"] = "- Stage is Design check [[Invented: Nonexistent]]."

        # 5. Safety priority critical miss (omits open electrical hazard ZF-HO-114A)
        responses["HO-LEG-PR-01"]["text"] = json.dumps(
            [
                {
                    "case_id": "ZF-HO-114B",
                    "reason": "Waited 31 days.",
                    "cites": ["Days in stage: 31"],
                }
            ]
        )

        report = heldout_eval.evaluate_heldout(manifest, responses)
        self.assertEqual(report["outcome"], "fail")
        self.assertIn("ZF-HO-114A", report["critical_misses"]["missed_case_ids"])
        codes = {ev["code"] for ev in report["critical_errors"]["events"]}
        self.assertIn("control_boundary_breach", codes)
        self.assertIn("unresolved_ambiguity_picked", codes)
        self.assertIn("abstention_violation", codes)
        self.assertIn("fabricated_source_citation", codes)
        self.assertIn("safety_priority_miss", codes)

    def test_missing_usage_or_unsettled_reservation_records_unknown_liability(self) -> None:
        manifest = heldout_eval.canonical_heldout_manifest()
        responses = heldout_eval.canonical_baseline_responses()
        responses["HO-LEG-MS-01"]["usage"] = None
        responses["HO-AST-SP-01"]["unsettled_reservation"] = True

        report = heldout_eval.evaluate_heldout(manifest, responses)
        self.assertEqual(report["outcome"], "fail")
        self.assertEqual(report["unknown_liabilities"]["count"], 2)
        self.assertEqual(report["usage"]["estimated_cost"], ai_consumption.UNKNOWN)
        self.assertIn("unknown_liabilities_present:2", report["failure_reasons"])

    def test_declared_serving_version_mismatch_fails_evaluation(self) -> None:
        manifest = heldout_eval.canonical_heldout_manifest()
        responses = heldout_eval.canonical_baseline_responses()
        responses["HO-LEG-BR-01"]["serving_version"] = "unexpected-shadow-model-2026"

        report = heldout_eval.evaluate_heldout(manifest, responses)
        self.assertEqual(report["outcome"], "fail")
        self.assertIn("serving_version_mismatch", report["failure_reasons"])
        self.assertEqual(len(report["actual_serving_version"]["mismatches"]), 1)


if __name__ == "__main__":
    unittest.main()
