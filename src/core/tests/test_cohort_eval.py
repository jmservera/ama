import copy
import unittest
from typing import Any

from cohort_eval_fixture import clean_observed, manifest, seeded
from zava_forward.core import cohort_eval


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


if __name__ == "__main__":
    unittest.main()
