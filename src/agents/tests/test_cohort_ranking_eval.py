import contextlib
import copy
import io
import unittest
from typing import Any

from zava_forward.core import cohort_eval, ranking

from zava_forward.agents import cohort_ranking_eval as cre


def codes(record: dict[str, Any]) -> set[str]:
    return {b["code"] for b in record["blockers"]}


class CohortRankingEvalTests(unittest.TestCase):
    def test_clean_approved_run_is_ready_but_never_fairness_evidence(self) -> None:
        rec = cre._run(approval=cre.MOCK_APPROVAL)
        self.assertEqual(rec["status"], "ready")
        self.assertEqual(rec["total_cases"], 48)
        self.assertTrue(rec["synthetic"])
        self.assertFalse(rec["fairness_evidence"])

    def test_run_has_no_approval_path_and_stays_blocked(self) -> None:
        for defects in (False, True):
            rec = cre.run(defects=defects)
            self.assertFalse(rec["activation_allowed"])
            self.assertIn("unapproved_thresholds", codes(rec))
        self.assertEqual(cre.main(["--approved"]), 0)

    def test_default_run_blocks_on_unapproved_thresholds(self) -> None:
        rec = cre.run()
        self.assertEqual(rec["status"], "blocked")
        self.assertFalse(rec["activation_allowed"])
        self.assertEqual(codes(rec), {"unapproved_thresholds", "insufficient_sample"})

    def test_all_seeded_defects_detected_and_block(self) -> None:
        rec = cre._run(defects=True, approval=cre.MOCK_APPROVAL)
        expected = sorted(cre.SEEDED_DROPPED + cre.SEEDED_DEMOTED)
        self.assertEqual(rec["detected_defects"], expected)
        self.assertNotIn("seeded_defect_undetected", codes(rec))
        self.assertIn("unjustified_exclusion", codes(rec))
        self.assertFalse(rec["activation_allowed"])

    def test_exceedance_is_reported_per_cohort_not_averaged(self) -> None:
        rec = cre._run(defects=True, approval=cre.MOCK_APPROVAL)
        sensor = rec["dimensions"]["sensor_completeness"]["cohorts"]
        self.assertEqual(sensor["partial"]["errors"], 2)
        self.assertEqual(sensor["complete"]["errors"], 2)  # history defects, kept separate
        self.assertTrue(any("sensor_completeness/partial" in b["detail"] for b in rec["blockers"]))

    def test_per_cohort_counts_reconcile_in_every_dimension(self) -> None:
        rec = cre._run(defects=True, approval=cre.MOCK_APPROVAL)
        self.assertNotIn("reconciliation", codes(rec))
        for body in rec["dimensions"].values():
            total = sum(r["n"] + r["missing"] for r in body["cohorts"].values())
            self.assertEqual(total, rec["total_cases"])

    def test_partial_source_routes_to_review_never_exclusion(self) -> None:
        cases, manifest = cre.build()
        outcomes = {o["id"]: o["outcome"] for o in cre.observe(cases, manifest)}
        partial = [c["id"] for c in manifest["cases"] if c["expected"] == "review"]
        self.assertEqual(len(partial), cre.PAIRS)
        self.assertEqual({outcomes[i] for i in partial}, {"review"})

    def test_small_sample_stays_insufficient(self) -> None:
        cases, manifest = cre.build()
        manifest["approval"] = {"cohorts_owner": "Owner", "thresholds_owner": "Owner"}
        manifest["cases"] = [
            c
            for c in manifest["cases"]
            if not (c["cohorts"]["sensor_completeness"] == "partial" and c["id"].endswith("-4-b"))
        ]
        kept = {c["id"] for c in manifest["cases"]}
        observed = [o for o in cre.observe(cases, manifest) if o["id"] in kept]
        rec = cohort_eval.evaluate(manifest, observed)
        row = rec["dimensions"]["sensor_completeness"]["cohorts"]["partial"]
        self.assertFalse(row["sufficient"])
        self.assertIn("insufficient_sample", codes(rec))
        self.assertFalse(rec["activation_allowed"])

    def test_human_disposition_clears_exceedance_only_with_approval(self) -> None:
        cases, manifest = cre.build()
        disposition = {
            "by": "Reviewer",
            "rationale": "Seeded defect demonstration",
            "decision": "accept",
        }
        unapproved = cohort_eval.evaluate(manifest, cre.observe(cases, manifest), disposition)
        self.assertFalse(unapproved["activation_allowed"])
        self.assertIn("unapproved_thresholds", codes(unapproved))

    def test_cases_carry_field_based_inputs(self) -> None:
        cases, manifest = cre.build()
        by_id = {c["id"]: c for c in cases}
        self.assertNotEqual(by_id["sensor-0-a"]["sensor_data"], by_id["sensor-0-b"]["sensor_data"])
        self.assertNotEqual(
            by_id["source-0-a"]["source_record"], by_id["source-0-b"]["source_record"]
        )
        self.assertNotEqual(
            by_id["history-0-a"]["appointment_history"], by_id["history-0-b"]["appointment_history"]
        )

    def test_field_sensitive_negative_controls_are_detected(self) -> None:
        def exclude_missing(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
            kept = [
                c
                for c in cases
                if {c["sensor_data"], c["source_record"]}.isdisjoint({"missing", "stale"})
            ]
            return list(ranking.rank(kept))

        def penalise_appointments(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
            bad = [c for c in cases if c["appointment_history"] == "prior_no_access"]
            good = [c for c in cases if c["appointment_history"] != "prior_no_access"]
            out = list(ranking.rank(good))
            return out + [dict(e, rank=len(out) + i) for i, e in enumerate(ranking.rank(bad), 1)]

        def ignore_support(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
            plain = [
                dict(c, resident={"adjustment": "None", "priority_support": False}) for c in cases
            ]
            return list(ranking.rank(plain))

        for name, fn in (
            ("exclude_missing", exclude_missing),
            ("penalise_appointments", penalise_appointments),
            ("ignore_support", ignore_support),
        ):
            rec = cohort_eval.evaluate(*self._manifest_and_observed(fn))
            self.assertGreater(
                sum(r["errors"] for b in rec["dimensions"].values() for r in b["cohorts"].values()),
                0,
                name,
            )
        # Control: the real ranker has zero errors.
        rec = cre._run(approval=cre.MOCK_APPROVAL)
        self.assertEqual(rec["status"], "ready")

    def _manifest_and_observed(self, fn: Any) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        cases, manifest = cre.build()
        manifest["approval"] = dict(cre.MOCK_APPROVAL)
        return manifest, cre.observe(cases, manifest, fn)

    def test_accessibility_pairs_share_waiting_days(self) -> None:
        cases, _ = cre.build()
        days = {c["id"]: c["days_in_stage"] for c in cases}
        for i in range(cre.PAIRS):
            self.assertEqual(days[f"access-yes-{i}"], days[f"access-no-{i}"])

    def test_exclusion_cannot_cancel_a_later_demotion(self) -> None:
        cases, manifest = cre.build()
        dropped = {"sensor-0-b", "sensor-1-b"}
        out = [copy.deepcopy(c) for c in cases if c["id"] not in dropped]
        demoted = next(c for c in out if c["id"] == "history-2-b")
        demoted["days_in_stage"] -= 15  # behind the next two-case unit; two exclusions offset it
        outcomes = {o["id"]: o["outcome"] for o in cre.observe(out, manifest)}
        self.assertEqual(outcomes["sensor-0-b"], "excluded")
        self.assertEqual(outcomes["history-2-b"], "deprioritised")

    def test_main_prints_summary(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(cre.main(["--defects"]), 0)
            self.assertEqual(cre.main(["--json"]), 0)
        self.assertIn("seeded", out.getvalue())


if __name__ == "__main__":
    unittest.main()
