import copy
import unittest
from collections.abc import Callable, Mapping
from typing import Any

from cohort_eval_fixture import approved, clean_observed, manifest, seeded
from zava_forward.core import cohort_eval, rai_release, ranking

_policy_hash: Callable[[Mapping[str, Any]], str] = ranking.policy_hash
_rule_order_hash: Callable[[Mapping[str, Any]], str] = ranking.rule_order_hash
_BASE_POLICY: dict[str, Any] = ranking.CURRENT


def signed_ranking_policy(owner: str = "Priya Shah, Asset Lead") -> dict[str, Any]:
    pol = copy.deepcopy(_BASE_POLICY)
    pol["owner"] = owner
    pol["status"] = "Signed off by named policy owner"
    pol["signoff"] = {
        "signed_by": owner,
        "signed_on": "2026-11-14",
        "rule_order_hash": _rule_order_hash(pol),
    }
    pol["content_hash"] = _policy_hash(pol)
    return pol


def codes(record: dict[str, Any]) -> set[str]:
    return {b["code"] for b in record["blockers"]}


class CohortEvalTests(unittest.TestCase):
    def test_clean_run_is_ready_but_never_fairness_evidence(self) -> None:
        m = manifest()
        rec = cohort_eval.evaluate(m, clean_observed(m))
        self.assertEqual(rec["status"], "ready")
        self.assertTrue(rec["activation_allowed"])
        self.assertFalse(rec["fairness_evidence"])
        self.assertEqual(
            rec["record_hash"], cohort_eval.evaluate(m, clean_observed(m))["record_hash"]
        )

    def test_all_seeded_defects_detected_and_block(self) -> None:
        m, obs = seeded()
        rec = cohort_eval.evaluate(m, obs)
        self.assertEqual(rec["detected_defects"], ["c03", "c10"])
        self.assertNotIn("seeded_defect_undetected", codes(rec))
        self.assertIn("unjustified_exclusion", codes(rec))
        self.assertEqual(rec["status"], "blocked")
        self.assertFalse(rec["activation_allowed"])

    def test_undetected_seeded_defect_is_reported(self) -> None:
        m, obs = seeded()
        m["seeded_defects"].append("c20")
        self.assertIn("seeded_defect_undetected", codes(cohort_eval.evaluate(m, obs)))

    def test_justified_exclusion_is_not_a_defect(self) -> None:
        m = manifest()
        m["cases"][0]["expected"] = "excluded"
        obs = clean_observed(m)
        obs[1]["outcome"] = "excluded"
        obs[1]["reason"] = "resident_opted_out"
        rec = cohort_eval.evaluate(m, obs)
        self.assertEqual(rec["detected_defects"], [])
        self.assertEqual(
            rec["dimensions"]["source_completeness"]["cohorts"]["complete"]["errors"], 1
        )

    def test_per_cohort_counts_reconcile(self) -> None:
        m, obs = seeded()
        rec = cohort_eval.evaluate(m, obs)
        for dim in rec["dimensions"].values():
            rows = dim["cohorts"].values()
            self.assertEqual(sum(r["n"] for r in rows), rec["total_cases"])
            self.assertEqual(sum(r["errors"] for r in rows), 2)
            self.assertEqual(sum(r["excluded"] + r["deprioritised"] for r in rows), 2)
            for r in rows:
                lo, hi = r["error_interval"]
                self.assertLessEqual(lo, r["error_rate"])
                self.assertLessEqual(r["error_rate"], hi)

    def test_reconciliation_failures_block(self) -> None:
        m = manifest()
        obs = clean_observed(m)[1:] + [{"id": "zzz", "outcome": "ranked"}]
        rec = cohort_eval.evaluate(m, obs)
        self.assertIn("reconciliation", codes(rec))
        self.assertFalse(rec["activation_allowed"])

    def test_small_or_missing_samples_stay_insufficient(self) -> None:
        m = manifest()
        m["thresholds"]["min_sample"] = 13
        m["cohorts"]["support_need"].append("not_recorded")
        rec = cohort_eval.evaluate(m, clean_observed(m))
        self.assertIn("insufficient_sample", codes(rec))
        row = rec["dimensions"]["support_need"]["cohorts"]["not_recorded"]
        self.assertEqual(
            (row["n"], row["sufficient"], row["error_rate"], row["error_interval"]),
            (0, False, None, None),
        )
        self.assertFalse(rec["activation_allowed"])

    def test_threshold_exceeded_is_per_cohort_not_averaged(self) -> None:
        m = manifest()
        obs = clean_observed(m)
        for o in obs[:3]:
            o["outcome"] = "review" if o["outcome"] == "ranked" else "ranked"
        m["thresholds"]["max_error_rate"] = 0.2
        approved(m)
        rec = cohort_eval.evaluate(m, obs)
        overall = 3 / rec["total_cases"]
        self.assertLess(overall, 0.2)
        self.assertIn("threshold_exceeded", codes(rec))
        self.assertEqual(rec["status"], "blocked")

    def test_unapproved_thresholds_block_and_disposition_cannot_clear(self) -> None:
        m = manifest()
        m["approval"] = {"cohorts_owner": "unapproved", "thresholds_owner": ""}
        disposition = {"by": "RAI owner", "decision": "accept", "rationale": "reviewed"}
        rec = cohort_eval.evaluate(m, clean_observed(m), disposition)
        self.assertIn("unapproved_thresholds", codes(rec))
        self.assertFalse(rec["activation_allowed"])

    def test_approval_must_be_complete_and_bound_to_manifest_content(self) -> None:
        def edits(m: dict[str, Any]) -> None:
            m["thresholds"]["max_error_rate"] = 0.9

        def drop_lawful(m: dict[str, Any]) -> None:
            del m["approval"]["lawful_fields_owner"]

        def stale_digest(m: dict[str, Any]) -> None:
            m["approval"]["manifest_digest"] = "0" * 64

        def no_digest(m: dict[str, Any]) -> None:
            del m["approval"]["manifest_digest"]

        disposition = {"by": "RAI owner", "decision": "accept", "rationale": "reviewed"}
        for change in (edits, drop_lawful, stale_digest, no_digest):
            m = manifest()
            self.assertNotIn(
                "unapproved_thresholds", codes(cohort_eval.evaluate(m, clean_observed(m)))
            )
            change(m)
            rec = cohort_eval.evaluate(m, clean_observed(m), disposition)
            self.assertIn("unapproved_thresholds", codes(rec), change.__name__)
            self.assertFalse(rec["activation_allowed"])
            self.assertFalse(rec["fairness_evidence"])

    def test_human_disposition_clears_only_exceedances(self) -> None:
        m, obs = seeded()
        self.assertFalse(
            cohort_eval.evaluate(m, obs, {"by": "x", "decision": "accept"})["activation_allowed"]
        )
        ok = {"by": "RAI owner", "decision": "accept", "rationale": "defects triaged"}
        rec = cohort_eval.evaluate(m, obs, ok)
        self.assertEqual(rec["status"], "dispositioned")
        self.assertTrue(rec["activation_allowed"])
        self.assertTrue(rec["blockers"])
        rejected = cohort_eval.evaluate(m, obs, {**ok, "decision": "reject"})
        self.assertFalse(rejected["activation_allowed"])

    def test_synthetic_flag_always_denies_fairness_evidence(self) -> None:
        m = copy.deepcopy(manifest())
        m["synthetic"] = True
        self.assertFalse(cohort_eval.evaluate(m, clean_observed(m))["fairness_evidence"])
        self.assertIn("OQ-018", cohort_eval.evaluate(m, clean_observed(m))["authority_gap"])

    def test_non_finite_or_boolean_thresholds_are_unapproved(self) -> None:
        for key, bad in (
            ("max_error_rate", float("nan")),
            ("max_error_rate", True),
            ("max_exclusion_gap", 1.5),
            ("min_sample", float("inf")),
            ("min_sample", True),
        ):
            m = manifest()
            m["thresholds"][key] = bad
            rec = cohort_eval.evaluate(m, clean_observed(m))
            self.assertIn("unapproved_thresholds", codes(rec), (key, bad))
            self.assertFalse(rec["activation_allowed"])

    def test_missing_observations_do_not_count_as_samples(self) -> None:
        m = manifest()
        rec = cohort_eval.evaluate(m, [])
        for dim in rec["dimensions"].values():
            for row in dim["cohorts"].values():
                self.assertEqual(row["n"], 0)
                self.assertGreater(row["missing"], 0)
                self.assertFalse(row["sufficient"])
                self.assertIsNone(row["error_interval"])
        self.assertFalse(rec["activation_allowed"])

    def test_duplicate_ids_block(self) -> None:
        m = manifest()
        obs = clean_observed(m)
        rec = cohort_eval.evaluate(m, [{**obs[0], "outcome": "excluded"}, *obs])
        self.assertIn("invalid_input", codes(rec))
        self.assertFalse(rec["activation_allowed"])
        m["cases"].append(dict(m["cases"][0]))
        self.assertIn("invalid_input", codes(cohort_eval.evaluate(m, obs)))

    def test_missing_outcome_blocks_without_disposition_path(self) -> None:
        m = manifest()
        obs = clean_observed(m)
        del obs[0]["outcome"]
        ok = {"by": "Reviewer", "rationale": "reviewed", "decision": "accept"}
        rec = cohort_eval.evaluate(m, obs, ok)
        self.assertIn("invalid_input", codes(rec))
        self.assertFalse(rec["activation_allowed"])

    def test_malformed_expectation_or_identity_blocks_without_disposition(self) -> None:
        ok = {"by": "Reviewer", "rationale": "reviewed", "decision": "accept"}
        for mutate in (
            lambda m: m["cases"][0].update(expected="unsupported"),
            lambda m: m["cases"][0].pop("expected"),
            lambda m: m.pop("task_id"),
            lambda m: m.pop("subject_version"),
            lambda m: m.pop("missing_data_treatment"),
            lambda m: m.update(missing_data_treatment="  "),
            lambda m: m["cases"][0].update(id=None),
            lambda m: m["cases"][0].pop("id"),
        ):
            m = manifest()
            mutate(m)  # type: ignore[no-untyped-call]
            rec = cohort_eval.evaluate(m, clean_observed(manifest()), ok)
            self.assertIn("invalid_input", codes(rec))
            self.assertFalse(rec["activation_allowed"])

    def test_malformed_shapes_return_blocked_record(self) -> None:
        ok = {"by": "Reviewer", "rationale": "reviewed", "decision": "accept"}
        for mutate in (
            lambda m: m["cases"][0].update(id=[]),
            lambda m: m["cases"][0].pop("cohorts"),
            lambda m: m["cases"][0].update(cohorts=None),
            lambda m: m.update(thresholds=None),
            lambda m: m.update(approval="unapproved"),
        ):
            m = manifest()
            mutate(m)  # type: ignore[no-untyped-call]
            rec = cohort_eval.evaluate(m, clean_observed(manifest()), ok)
            self.assertFalse(rec["activation_allowed"])
            self.assertEqual(rec["status"], "blocked")

    def test_null_identity_in_both_inputs_cannot_match(self) -> None:
        m = manifest()
        m["cases"][0]["id"] = None
        obs = clean_observed(manifest())
        obs[0]["id"] = None
        rec = cohort_eval.evaluate(m, obs)
        self.assertIn("invalid_input", codes(rec))
        self.assertFalse(rec["activation_allowed"])

    def test_non_boolean_synthetic_is_conservatively_synthetic(self) -> None:
        for value in (None, 0, "", "false"):
            m = manifest()
            m["synthetic"] = value
            rec = cohort_eval.evaluate(m, clean_observed(m))
            self.assertTrue(rec["synthetic"])
            self.assertFalse(rec["fairness_evidence"])

    def test_unmeasured_non_synthetic_run_is_not_fairness_evidence(self) -> None:
        m = manifest()
        m["synthetic"] = False
        approved(m)
        self.assertFalse(cohort_eval.evaluate(m, [])["fairness_evidence"])
        self.assertTrue(cohort_eval.evaluate(m, clean_observed(m))["fairness_evidence"])

    def test_empty_cohorts_block(self) -> None:
        m = manifest()
        m["cohorts"] = {}
        rec = cohort_eval.evaluate(m, clean_observed(m))
        self.assertIn("insufficient_sample", codes(rec))
        self.assertFalse(rec["activation_allowed"])

    def test_threshold_uses_unrounded_rates(self) -> None:
        m = manifest()
        m["thresholds"]["max_error_rate"] = 0.08331
        approved(m)
        obs = clean_observed(m)
        obs[0]["outcome"] = "review" if m["cases"][0]["expected"] != "review" else "ranked"
        rec = cohort_eval.evaluate(m, obs)
        self.assertIn("threshold_exceeded", codes(rec))

    def test_rejection_blocks_a_clean_run(self) -> None:
        m = manifest()
        rec = cohort_eval.evaluate(
            m, clean_observed(m), {"by": "Reviewer", "rationale": "no", "decision": "reject"}
        )
        self.assertFalse(rec["activation_allowed"])
        self.assertEqual(rec["status"], "blocked")

    def test_record_hash_binds_input_identity(self) -> None:
        m = manifest()
        obs = clean_observed(m)
        base = cohort_eval.evaluate(m, obs)
        m2 = copy.deepcopy(m)
        obs2 = copy.deepcopy(obs)
        m2["cases"][0]["id"] = "renamed"
        obs2[0]["id"] = "renamed"
        self.assertNotEqual(base["record_hash"], cohort_eval.evaluate(m2, obs2)["record_hash"])

    def test_default_unapproved_and_fictional_offline_records_enforce_oq018_boundary(self) -> None:
        raw = manifest()
        raw.pop("approval", None)
        unapproved = cohort_eval.evaluate(raw, clean_observed(raw))
        self.assertEqual(unapproved["owner_approval_status"], "unapproved")
        self.assertFalse(unapproved["lawful_analysis_fields_approved"])
        self.assertFalse(unapproved["live_activation_allowed"])
        self.assertTrue(unapproved["synthetic_not_fairness_evidence"])
        self.assertIn("OQ-018", unapproved["non_fairness_provenance_notice"])

        offline = cohort_eval.evaluate(manifest(), clean_observed(manifest()))
        self.assertEqual(offline["owner_approval_status"], "pending_owner_approval")
        self.assertFalse(offline["lawful_analysis_fields_approved"])
        self.assertFalse(offline["live_activation_allowed"])
        self.assertFalse(offline["fairness_evidence"])
        self.assertTrue(offline["synthetic_not_fairness_evidence"])
        self.assertEqual(
            set(offline["lawful_analysis_fields"]),
            set(manifest()["cohorts"]),
        )

    def test_dated_real_human_owner_approval_requires_non_synthetic_and_bound_lawful_fields(
        self,
    ) -> None:
        dated_owners = {
            "cohorts_owner": "Priya Shah, Data Lead",
            "lawful_fields_owner": "Tom Reed, DPO",
            "thresholds_owner": "Amina Okafor, RAI Owner",
            "approved_at": "2026-11-14",
        }
        synth = manifest()
        synth["lawful_analysis_fields"] = [
            "sensor_completeness",
            "support_need",
            "appointment_history",
        ]
        cohort_eval.approve(synth, dated_owners)
        synth_rec = cohort_eval.evaluate(synth, clean_observed(synth))
        self.assertEqual(synth_rec["owner_approval_status"], "pending_owner_approval")
        self.assertFalse(synth_rec["lawful_analysis_fields_approved"])
        self.assertFalse(synth_rec["live_activation_allowed"])
        self.assertFalse(synth_rec["fairness_evidence"])
        self.assertTrue(synth_rec["synthetic_not_fairness_evidence"])

        live_ready = copy.deepcopy(synth)
        live_ready["synthetic"] = False
        cohort_eval.approve(live_ready, dated_owners)
        ok_rec = cohort_eval.evaluate(live_ready, clean_observed(live_ready), live=True)
        self.assertEqual(ok_rec["owner_approval_status"], "approved")
        self.assertTrue(ok_rec["lawful_analysis_fields_approved"])
        self.assertTrue(ok_rec["live_activation_allowed"])
        self.assertTrue(ok_rec["activation_allowed"])
        self.assertTrue(ok_rec["fairness_evidence"])
        self.assertTrue(ok_rec["synthetic_not_fairness_evidence"])

        live_ready["lawful_analysis_fields"].append("contact_channel")
        edited = cohort_eval.evaluate(live_ready, clean_observed(live_ready), live=True)
        self.assertEqual(edited["owner_approval_status"], "unapproved")
        self.assertFalse(edited["lawful_analysis_fields_approved"])
        self.assertFalse(edited["live_activation_allowed"])
        self.assertFalse(edited["activation_allowed"])

    def test_invalid_lawful_analysis_fields_block_approval_and_fairness_evidence(self) -> None:
        for bad_fields in ([], [""], "sensor_completeness", None):
            m = manifest()
            m["synthetic"] = False
            m["lawful_analysis_fields"] = bad_fields
            cohort_eval.approve(
                m,
                {
                    "cohorts_owner": "Priya Shah, Data Lead",
                    "lawful_fields_owner": "Tom Reed, DPO",
                    "thresholds_owner": "Amina Okafor, RAI Owner",
                    "approved_at": "2026-11-14",
                },
            )
            rec = cohort_eval.evaluate(m, clean_observed(m))
            self.assertIn("unapproved_lawful_analysis_fields", codes(rec))
            self.assertEqual(rec["owner_approval_status"], "unapproved")
            self.assertFalse(rec["lawful_analysis_fields_approved"])
            self.assertFalse(rec["fairness_evidence"])
            self.assertFalse(rec["activation_allowed"])

    def test_export_record_enforces_hash_and_oq018_non_fairness_invariants(self) -> None:
        rec = cohort_eval.evaluate(manifest(), clean_observed(manifest()))
        exported = cohort_eval.export_record(rec)
        self.assertEqual(exported["record_hash"], rec["record_hash"])
        self.assertTrue(exported["synthetic_not_fairness_evidence"])
        self.assertFalse(exported["live_activation_allowed"])

        tampered_hash = dict(rec, owner_approval_status="approved")
        with self.assertRaises(ValueError):
            cohort_eval.export_record(tampered_hash)

        forged_body = {
            k: v
            for k, v in dict(
                rec,
                fairness_evidence=True,
                live_activation_allowed=True,
                owner_approval_status="approved",
                lawful_analysis_fields_approved=True,
            ).items()
            if k != "record_hash"
        }
        forged = {**forged_body, "record_hash": rai_release.digest(forged_body)}
        with self.assertRaises(ValueError):
            cohort_eval.export_record(forged)

    def test_retained_cohort_version_counts_and_abstention_accounting(self) -> None:
        m = manifest()
        m["cohort_version"] = "cohorts-2026-11"
        m["prompt_version"] = "triage-prompt-v2"
        m["model_version"] = "gpt-4o-2026-08"
        approved(m)
        obs = clean_observed(m)
        obs[0]["outcome"] = "abstained"
        m["cases"][0]["expected"] = "abstained"
        approved(m)
        rec = cohort_eval.evaluate(m, obs)
        self.assertEqual(rec["status"], "ready")
        self.assertEqual(rec["aggregation_rule"], "per_cohort_unaveraged")
        self.assertFalse(rec["population_fairness_established"])
        self.assertEqual(rec["cohort_definitions"]["cohorts"], m["cohorts"])
        self.assertEqual(rec["version_definitions"]["cohort_version"], "cohorts-2026-11")
        self.assertEqual(rec["version_definitions"]["prompt_version"], "triage-prompt-v2")
        self.assertEqual(rec["version_definitions"]["model_version"], "gpt-4o-2026-08")
        self.assertEqual(
            rec["counts"],
            {"eligible": 24, "tested": 24, "abstained": 1, "failed": 0, "missing": 0},
        )
        complete_row = rec["dimensions"]["source_completeness"]["cohorts"]["complete"]
        self.assertEqual(complete_row["eligible"], 12)
        self.assertEqual(complete_row["tested"], 12)
        self.assertEqual(complete_row["abstained"], 1)
        self.assertEqual(complete_row["failed"], 0)
        self.assertEqual(complete_row["abstention_rate"], round(1 / 12, 4))

    def test_ai_task_requires_signed_ranking_policy_and_transparent_non_ai_comparison(self) -> None:
        pol = signed_ranking_policy()
        m = manifest()
        m["task_kind"] = "ai_task"
        approved(m)
        base_obs = clean_observed(m)
        disposition = {"by": "Amina Okafor, RAI Owner", "decision": "accept", "rationale": "ok"}

        missing_both = cohort_eval.evaluate(m, base_obs, disposition)
        self.assertIn("unapproved_ranking_policy", codes(missing_both))
        self.assertIn("missing_non_ai_comparison", codes(missing_both))
        self.assertFalse(missing_both["activation_allowed"])

        tampered = copy.deepcopy(pol)
        tampered["rules"] = list(reversed(tampered["rules"]))
        tampered_rec = cohort_eval.evaluate(
            m,
            base_obs,
            disposition,
            ranking_policy=tampered,
            non_ai_observed=base_obs,
        )
        self.assertIn("invalid_ranking_policy_hash", codes(tampered_rec))
        self.assertFalse(tampered_rec["activation_allowed"])

        regressed_ai = copy.deepcopy(base_obs)
        regressed_ai[0]["outcome"] = "deprioritised"
        reg_rec = cohort_eval.evaluate(
            m,
            regressed_ai,
            disposition,
            ranking_policy=pol,
            non_ai_observed=base_obs,
        )
        self.assertIn("ai_regression_vs_non_ai", codes(reg_rec))
        self.assertTrue(reg_rec["non_ai_comparison"]["regression_detected"])
        self.assertFalse(reg_rec["activation_allowed"])

        ok_rec = cohort_eval.evaluate(
            m,
            base_obs,
            ranking_policy=pol,
            non_ai_observed=base_obs,
        )
        self.assertEqual(ok_rec["status"], "ready")
        self.assertTrue(ok_rec["activation_allowed"])
        self.assertFalse(ok_rec["non_ai_comparison"]["regression_detected"])
        self.assertEqual(ok_rec["version_definitions"]["ranking_policy_hash"], pol["content_hash"])
        self.assertIn("ranking_policy", ok_rec["input_digests"])
        self.assertIn("non_ai_observed", ok_rec["input_digests"])

    def test_missing_sensor_and_non_response_never_lower_service_or_allow_prohibited_inference(
        self,
    ) -> None:
        m = manifest()
        m["cohorts"]["sensor_completeness"] = ["present", "declined"]
        for idx, c in enumerate(m["cases"]):
            c["cohorts"]["sensor_completeness"] = "present" if idx % 2 == 0 else "declined"
        m["seeded_defects"] = ["c02"]
        approved(m)

        obs = clean_observed(m)
        obs[1]["service_level"] = "reduced"
        obs[3]["inferences"] = {"vulnerability": "inferred_frail", "refusal": "non_engaged"}
        disposition = {
            "by": "Amina Okafor, RAI Owner",
            "decision": "accept",
            "rationale": "reviewed",
        }
        rec = cohort_eval.evaluate(m, obs, disposition)
        self.assertIn("service_lowered", codes(rec))
        self.assertIn("prohibited_inference", codes(rec))
        self.assertIn("c02", rec["detected_defects"])
        declined_row = rec["dimensions"]["sensor_completeness"]["cohorts"]["declined"]
        self.assertEqual(declined_row["failed"], 2)
        self.assertEqual(declined_row["errors"], 2)
        self.assertFalse(rec["activation_allowed"])
        self.assertFalse(rec["fairness_evidence"])

    def test_non_human_or_placeholder_threshold_and_disposition_approvals_are_rejected(
        self,
    ) -> None:
        for bad_owner in ("Copilot Agent", "TBD", "to be named"):
            m = manifest()
            cohort_eval.approve(
                m,
                {
                    "cohorts_owner": "Priya Shah, Data Lead",
                    "lawful_fields_owner": "Tom Reed, DPO",
                    "thresholds_owner": bad_owner,
                },
            )
            rec = cohort_eval.evaluate(m, clean_observed(m))
            self.assertIn("unapproved_thresholds", codes(rec), bad_owner)
            self.assertFalse(rec["activation_allowed"])

        m_exp = manifest()
        cohort_eval.approve(
            m_exp,
            {
                "cohorts_owner": "Priya Shah, Data Lead",
                "lawful_fields_owner": "Tom Reed, DPO",
                "thresholds_owner": "Amina Okafor, RAI Owner",
                "expires": 50.0,
            },
        )
        exp_rec = cohort_eval.evaluate(m_exp, clean_observed(m_exp), now=100.0)
        self.assertIn("unapproved_thresholds", codes(exp_rec))
        self.assertFalse(exp_rec["activation_allowed"])

        m_seed, obs_seed = seeded()
        bot_disp = cohort_eval.evaluate(
            m_seed,
            obs_seed,
            {"by": "AI assistant", "decision": "accept", "rationale": "automated"},
        )
        self.assertIsNone(bot_disp["disposition"])
        self.assertFalse(bot_disp["activation_allowed"])

        m_abs = manifest()
        m_abs["thresholds"]["max_abstention_rate"] = 0.05
        m_abs["cases"][0]["expected"] = "abstained"
        approved(m_abs)
        obs_abs = clean_observed(m_abs)
        abs_rec = cohort_eval.evaluate(m_abs, obs_abs)
        self.assertIn("threshold_exceeded", codes(abs_rec))
        self.assertFalse(abs_rec["activation_allowed"])

    def test_protected_characteristic_fields_require_bound_dpo_minimum_necessary_approval(
        self,
    ) -> None:
        m = manifest()
        m["lawful_analysis_fields"] = [
            "source_completeness",
            "support_need",
            "appointment_history",
            "disability",
        ]
        approved(m)
        disposition = {
            "by": "Amina Okafor, RAI Owner",
            "decision": "accept",
            "rationale": "reviewed",
        }
        blocked = cohort_eval.evaluate(m, clean_observed(m), disposition)
        self.assertIn("unapproved_protected_characteristic", codes(blocked))
        self.assertFalse(blocked["activation_allowed"])

        cohort_eval.approve_protected_characteristics(
            m,
            {
                "dpo_owner": "Tom Reed, DPO",
                "lawful_basis": "Equality Act 2010 public-sector duty audit",
                "minimum_necessary_justification": "Approved disability adjustment parity check",
                "approved_at": "2026-11-14",
                "approved_fields": ["disability"],
            },
        )
        cleared = cohort_eval.evaluate(m, clean_observed(m))
        self.assertNotIn("unapproved_thresholds", codes(cleared))
        self.assertNotIn("unapproved_protected_characteristic", codes(cleared))
        self.assertTrue(cleared["activation_allowed"])
        self.assertFalse(cleared["fairness_evidence"])
        self.assertFalse(cleared["population_fairness_established"])

        gen = manifest()
        gen["synthetic"] = False
        gen["cohort_origin"] = "generated"
        cohort_eval.approve(
            gen,
            {
                "cohorts_owner": "Priya Shah, Data Lead",
                "lawful_fields_owner": "Tom Reed, DPO",
                "thresholds_owner": "Amina Okafor, RAI Owner",
                "approved_at": "2026-11-14",
            },
        )
        gen_rec = cohort_eval.evaluate(gen, clean_observed(gen), live=True)
        self.assertFalse(gen_rec["fairness_evidence"])
        self.assertFalse(gen_rec["live_activation_allowed"])
        self.assertFalse(gen_rec["population_fairness_established"])

    def test_geography_and_archetype_dimensions_require_bound_relevance_approval(self) -> None:
        m = manifest()
        m["cohorts"]["geography"] = ["urban_compact", "rural_dispersed"]
        m["cohorts"]["archetype"] = ["post_1945_masonry", "non_traditional_solid_wall"]
        for idx, c in enumerate(m["cases"]):
            c["cohorts"]["geography"] = "urban_compact" if idx % 2 == 0 else "rural_dispersed"
            c["cohorts"]["archetype"] = (
                "post_1945_masonry" if idx < 12 else "non_traditional_solid_wall"
            )
        approved(m)

        unapproved = cohort_eval.evaluate(m, clean_observed(m))
        self.assertIn("unapproved_context_dimension", codes(unapproved))
        self.assertFalse(unapproved["activation_allowed"])

        cohort_eval.approve_context_dimensions(
            m,
            {
                "geography": {
                    "approved_by": "Priya Shah, Data Lead",
                    "relevant": True,
                    "rationale": "Contractor travel dispersal audit",
                    "approved_at": "2026-11-14",
                },
                "archetype": {
                    "approved_by": "Priya Shah, Data Lead",
                    "relevant": True,
                    "rationale": "Solid-wall survey parity audit",
                    "approved_at": "2026-11-14",
                },
            },
        )
        ok_rec = cohort_eval.evaluate(m, clean_observed(m))
        self.assertNotIn("unapproved_thresholds", codes(ok_rec))
        self.assertNotIn("unapproved_context_dimension", codes(ok_rec))
        self.assertEqual(ok_rec["status"], "ready")
        self.assertTrue(ok_rec["activation_allowed"])

    def test_sensor_completeness_fixtures_reject_provisioning_and_invented_thresholds(
        self,
    ) -> None:
        m_prov = manifest()
        m_prov["cases"][0]["sensor_device_id"] = "SYN-1001"
        approved(m_prov)
        prov_rec = cohort_eval.evaluate(m_prov, clean_observed(m_prov))
        self.assertIn("sensor_fixture_provisions_device", codes(prov_rec))
        self.assertFalse(prov_rec["activation_allowed"])

        m_thresh = manifest()
        m_thresh["thresholds"]["dew_point_threshold_c"] = 11.8
        approved(m_thresh)
        thresh_rec = cohort_eval.evaluate(m_thresh, clean_observed(m_thresh))
        self.assertIn("sensor_fixture_invents_threshold", codes(thresh_rec))
        self.assertFalse(thresh_rec["activation_allowed"])


if __name__ == "__main__":
    unittest.main()
