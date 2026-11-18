import copy
import unittest
from collections.abc import Callable, Mapping, Sequence
from typing import Any

from zava_forward.core import paired_equity, ranking
from zava_forward.core.rai_release import digest

_policy_hash: Callable[[Mapping[str, Any]], str] = ranking.policy_hash
_rule_order_hash: Callable[[Mapping[str, Any]], str] = ranking.rule_order_hash
_rank_with_policy: Callable[
    [Sequence[Mapping[str, Any]], Mapping[str, Any]], list[dict[str, Any]]
] = ranking.rank
_BASE_POLICY: dict[str, Any] = ranking.CURRENT


def signed_policy(owner: str = "Priya Shah, Asset Lead") -> dict[str, Any]:
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


def case(case_id: str, days: int = 5, **resident: Any) -> dict[str, Any]:
    return {
        "id": case_id,
        "stage": "Home identified",
        "days_in_stage": days,
        "hazards": [],
        "resident": {"priority_support": False, "adjustment": "None", **resident},
        "source_record": "complete",
        "sensor_data": "present",
        "appointment_history": "confirmed",
    }


ANCHORS = [case("z1", 10), case("z2", 3), case("z3", 20)]


def pairs() -> list[dict[str, Any]]:
    base = case("p1", 6)
    sensor = copy.deepcopy(base)
    sensor["sensor_data"] = "declined"
    need = case("p2", 6)
    need_subject = case("p2", 6, priority_support=True, adjustment="Large print")
    appt = case("p3", 6)
    appt_subject = copy.deepcopy(appt)
    appt_subject["appointment_history"] = "prior_no_access"
    src = case("p4", 6)
    src_subject = copy.deepcopy(src)
    src_subject["source_record"] = "missing"
    return [
        {"id": "s1", "dimension": "sensor_completeness", "reference": base, "subject": sensor},
        {
            "id": "n1",
            "dimension": "support_or_contact_need",
            "reference": need,
            "subject": need_subject,
        },
        {
            "id": "h1",
            "dimension": "appointment_history",
            "reference": appt,
            "subject": appt_subject,
        },
        {"id": "r1", "dimension": "source_completeness", "reference": src, "subject": src_subject},
    ]


def penalise_missing(cases: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Seeded defect: cases with declined sensors are pushed to the back of the queue."""
    ordered = sorted(cases, key=lambda c: (c.get("sensor_data") == "declined", c["id"]))
    return [{"id": c["id"], "rank": n} for n, c in enumerate(ordered, start=1)]


def penalise_history(cases: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(
        cases, key=lambda c: (c.get("appointment_history") == "prior_no_access", c["id"])
    )
    return [{"id": c["id"], "rank": n} for n, c in enumerate(ordered, start=1)]


def penalise_source(cases: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    ordered = sorted(cases, key=lambda c: (c.get("source_record") == "missing", c["id"]))
    return [{"id": c["id"], "rank": n} for n, c in enumerate(ordered, start=1)]


class PairedEquityTests(unittest.TestCase):
    def test_current_policy_never_lowers_priority_for_any_dimension(self) -> None:
        rec = paired_equity.evaluate(pairs(), ANCHORS)
        self.assertEqual(rec["status"], "pass")
        self.assertEqual((rec["tested"], rec["failed"]), (4, 0))
        self.assertFalse(rec["fairness_evidence"])
        self.assertFalse(rec["activation_allowed"])
        self.assertEqual(
            rec["record_hash"], paired_equity.evaluate(pairs(), ANCHORS)["record_hash"]
        )

    def test_default_ranker_is_the_deterministic_policy(self) -> None:
        explicit = paired_equity.evaluate(pairs(), ANCHORS, rank=ranking.rank)
        self.assertEqual(
            explicit["record_hash"], paired_equity.evaluate(pairs(), ANCHORS)["record_hash"]
        )

    def test_seeded_sensor_defect_is_detected_in_its_dimension_only(self) -> None:
        rec = paired_equity.evaluate(pairs(), ANCHORS, ["s1"], rank=penalise_missing)
        self.assertEqual(rec["detected_defects"], ["s1"])
        self.assertEqual(rec["dimensions"]["sensor_completeness"]["failed"], 1)
        self.assertEqual(rec["dimensions"]["appointment_history"]["failed"], 0)
        self.assertIn("sensor_completeness:unjustified_deprioritisation", rec["blockers"])
        self.assertEqual(rec["status"], "blocked")

    def test_seeded_source_defect_is_detected_in_its_dimension_only(self) -> None:
        rec = paired_equity.evaluate(pairs(), ANCHORS, ["r1"], rank=penalise_source)
        self.assertEqual(rec["detected_defects"], ["r1"])
        self.assertEqual(rec["dimensions"]["source_completeness"]["failed"], 1)
        self.assertEqual(rec["dimensions"]["sensor_completeness"]["failed"], 0)
        self.assertIn("source_completeness:unjustified_deprioritisation", rec["blockers"])

    def test_seeded_exclusion_is_detected_not_a_crash(self) -> None:
        def drop_missing_source(cases: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
            kept = [c for c in cases if c.get("source_record") != "missing"]
            return [{"id": c["id"], "rank": n} for n, c in enumerate(kept, start=1)]

        rec = paired_equity.evaluate(pairs(), ANCHORS, ["r1"], rank=drop_missing_source)
        self.assertEqual(rec["detected_defects"], ["r1"])
        self.assertEqual(
            rec["dimensions"]["source_completeness"]["failures"],
            [{"pair": "r1", "problems": ["excluded"]}],
        )
        self.assertEqual(rec["status"], "blocked")

    def test_source_dimension_is_required_and_rejects_a_confounded_pair(self) -> None:
        without = [p for p in pairs() if p["dimension"] != "source_completeness"]
        rec = paired_equity.evaluate(without, ANCHORS)
        self.assertIn("source_completeness:no_pairs", rec["blockers"])
        p = pairs()
        p[3]["subject"]["days_in_stage"] = 30
        rec = paired_equity.evaluate(p, ANCHORS)
        self.assertIn("r1:invalid_comparison:confounded", rec["blockers"])
        self.assertEqual(rec["dimensions"]["source_completeness"]["tested"], 0)

    def test_failing_dimension_is_not_averaged_away(self) -> None:
        many = pairs() + [dict(p, id=f"{p['id']}x{i}") for i in range(20) for p in pairs()[1:]]
        rec = paired_equity.evaluate(many, ANCHORS, rank=penalise_history)
        self.assertEqual(rec["status"], "blocked")
        self.assertEqual(rec["dimensions"]["appointment_history"]["failed"], 21)
        self.assertEqual(rec["dimensions"]["sensor_completeness"]["failed"], 0)

    def test_undetected_seeded_defect_blocks(self) -> None:
        rec = paired_equity.evaluate(pairs(), ANCHORS, ["s1"])
        self.assertIn("s1:seeded_defect_undetected", rec["blockers"])

    def test_missing_dimension_and_invalid_pair_block(self) -> None:
        bad = [p for p in pairs() if p["dimension"] != "appointment_history"]
        bad.append({"id": "x", "dimension": "other", "reference": {}, "subject": {}})
        rec = paired_equity.evaluate(bad, ANCHORS)
        self.assertIn("appointment_history:no_pairs", rec["blockers"])
        self.assertIn("x:invalid_pair", rec["blockers"])
        self.assertEqual(rec["status"], "blocked")

    def test_differing_pair_ids_fail(self) -> None:
        p = pairs()
        p[0]["subject"] = dict(p[0]["subject"], id="other")
        rec = paired_equity.evaluate(p, ANCHORS)
        self.assertEqual(
            rec["dimensions"]["sensor_completeness"]["failures"][0]["problems"], ["pair_ids_differ"]
        )

    def test_confounded_days_in_stage_change_is_rejected_not_passed(self) -> None:
        p = pairs()
        p[0]["subject"]["days_in_stage"] = 30
        rec = paired_equity.evaluate(p, ANCHORS)
        self.assertEqual(rec["status"], "blocked")
        self.assertIn("s1:invalid_comparison:confounded", rec["blockers"])
        self.assertIn("sensor_completeness:no_pairs", rec["blockers"])
        self.assertEqual(rec["tested"], 3)
        self.assertEqual(
            rec["invalid_pairs"],
            [{"pair": "s1", "dimension": "sensor_completeness", "reason": "confounded"}],
        )
        self.assertFalse(rec["activation_allowed"])
        self.assertFalse(rec["fairness_evidence"])

    def test_pair_without_contrast_is_rejected(self) -> None:
        p = pairs()
        p[2]["subject"] = copy.deepcopy(p[2]["reference"])
        rec = paired_equity.evaluate(p, ANCHORS)
        self.assertIn("h1:invalid_comparison:no_contrast", rec["blockers"])
        self.assertEqual(rec["status"], "blocked")

    def test_mislabeled_dimension_is_rejected(self) -> None:
        p = pairs()
        p[0]["dimension"] = "appointment_history"
        rec = paired_equity.evaluate(p, ANCHORS)
        self.assertIn("s1:invalid_comparison:wrong_contrast", rec["blockers"])
        self.assertEqual(rec["dimensions"]["appointment_history"]["tested"], 1)

    def test_unrelated_nested_change_is_rejected(self) -> None:
        p = pairs()
        p[1]["subject"]["resident"]["contact_preference"] = "phone"
        rec = paired_equity.evaluate(p, ANCHORS)
        self.assertIn("n1:invalid_comparison:confounded", rec["blockers"])

    def test_partial_support_bundle_is_rejected(self) -> None:
        p = pairs()
        p[1]["subject"]["resident"]["adjustment"] = "None"
        rec = paired_equity.evaluate(p, ANCHORS)
        self.assertIn("n1:invalid_comparison:wrong_contrast", rec["blockers"])

    def test_type_coerced_values_and_empty_nested_change_are_rejected(self) -> None:
        p = pairs()
        p[1]["subject"]["resident"]["priority_support"] = 1
        p[0]["subject"]["extra"] = {}
        rec = paired_equity.evaluate(p, ANCHORS)
        self.assertIn("n1:invalid_comparison:wrong_contrast", rec["blockers"])
        self.assertIn("s1:invalid_comparison:confounded", rec["blockers"])

    def test_nested_type_change_is_rejected(self) -> None:
        p = pairs()
        p[0]["reference"]["resident"]["extra"] = [1]
        p[0]["subject"]["resident"]["extra"] = [True]
        rec = paired_equity.evaluate(p, ANCHORS)
        self.assertIn("s1:invalid_comparison:confounded", rec["blockers"])
        self.assertEqual(rec["tested"], 3)

    def test_dotted_key_cannot_shadow_nested_change(self) -> None:
        p = pairs()
        p[0]["reference"]["resident"].update({"extra": {"x": 1}, "extra.x": 1})
        p[0]["subject"]["resident"].update({"extra": {"x": 2}, "extra.x": 1})
        rec = paired_equity.evaluate(p, ANCHORS)
        self.assertIn("s1:invalid_comparison:confounded", rec["blockers"])
        self.assertEqual(rec["invalid_pairs"][0]["reason"], "confounded")

    def test_supported_support_and_adjustment_bundle_is_valid(self) -> None:
        rec = paired_equity.evaluate(pairs(), ANCHORS)
        self.assertEqual(rec["invalid_pairs"], [])
        self.assertEqual(rec["dimensions"]["support_or_contact_need"]["tested"], 1)

    def test_anchor_sharing_the_case_id_blocks_instead_of_passing(self) -> None:
        anchors = [*ANCHORS, case("p1")]
        for rank in (penalise_missing, None):
            with self.subTest(rank=rank):
                rec = paired_equity.evaluate(pairs(), anchors, rank=rank)
                self.assertEqual(rec["status"], "blocked")
                self.assertIn("s1:invalid_comparison:anchor_id_collision", rec["blockers"])
                self.assertEqual(
                    rec["invalid_pairs"],
                    [
                        {
                            "pair": "s1",
                            "dimension": "sensor_completeness",
                            "reason": "anchor_id_collision",
                        }
                    ],
                )
                self.assertEqual(rec["dimensions"]["sensor_completeness"]["tested"], 0)
                self.assertFalse(rec["fairness_evidence"])
                self.assertFalse(rec["activation_allowed"])

    def test_collision_with_several_anchors_and_a_seeded_defect_still_blocks(self) -> None:
        anchors = [*ANCHORS, case("p1"), case("p1", 9)]
        rec = paired_equity.evaluate(pairs(), anchors, ["s1"], rank=penalise_missing)
        self.assertIn("s1:invalid_comparison:anchor_id_collision", rec["blockers"])
        self.assertIn("s1:seeded_defect_undetected", rec["blockers"])
        self.assertEqual(rec["detected_defects"], [])

    def test_missing_or_non_string_case_id_is_blocked_not_an_error(self) -> None:
        for bad_id in (None, "", 5):
            with self.subTest(bad_id=bad_id):
                p = pairs()
                for side in ("reference", "subject"):
                    if bad_id is None:
                        del p[0][side]["id"]
                    else:
                        p[0][side]["id"] = bad_id
                rec = paired_equity.evaluate(p, ANCHORS)
                self.assertEqual(rec["status"], "blocked")
                self.assertIn("s1:invalid_comparison:missing_case_id", rec["blockers"])

    def test_confounded_collision_keeps_the_comparability_reason(self) -> None:
        p = pairs()
        p[0]["subject"]["days_in_stage"] = 7
        rec = paired_equity.evaluate(p, [*ANCHORS, case("p1")])
        self.assertIn("s1:invalid_comparison:confounded", rec["blockers"])
        self.assertNotIn("s1:invalid_comparison:anchor_id_collision", rec["blockers"])

    def test_differing_ids_keep_their_existing_failure_despite_an_anchor_match(self) -> None:
        p = pairs()
        p[0]["subject"] = dict(p[0]["subject"], id="other")
        rec = paired_equity.evaluate(p, [*ANCHORS, case("p1")])
        self.assertEqual(rec["invalid_pairs"], [])
        self.assertEqual(
            rec["dimensions"]["sensor_completeness"]["failures"][0]["problems"], ["pair_ids_differ"]
        )

    def test_distinct_anchor_ids_remain_a_valid_positive_control(self) -> None:
        rec = paired_equity.evaluate(pairs(), [*ANCHORS, case("z4", 8)], rank=penalise_history)
        self.assertEqual(rec["invalid_pairs"], [])
        self.assertEqual(rec["dimensions"]["sensor_completeness"]["tested"], 1)
        self.assertEqual(
            paired_equity.evaluate(pairs(), [*ANCHORS, case("z4", 8)])["status"], "pass"
        )

    def test_inputs_are_not_mutated(self) -> None:
        p, a = pairs(), copy.deepcopy(ANCHORS)
        before = copy.deepcopy(p)
        paired_equity.evaluate(p, a)
        self.assertEqual((p, a), (before, ANCHORS))

    def test_predeclared_cohorts_hold_relevant_facts_constant_across_all_contrasts(self) -> None:
        defs = paired_equity.predeclared_cohorts()
        self.assertEqual(set(defs), set(paired_equity.DIMENSIONS))
        self.assertGreaterEqual(
            set(defs["source_completeness"]["contrasts"]),
            {"missing_source", "partial_source", "stale_source"},
        )
        self.assertGreaterEqual(
            set(defs["sensor_completeness"]["contrasts"]),
            {"declined_sensor", "missing_sensor"},
        )
        self.assertGreaterEqual(
            set(defs["support_or_contact_need"]["contrasts"]),
            {"accessibility_adjustment", "contact_channel_need"},
        )
        self.assertGreaterEqual(
            set(defs["appointment_history"]["contrasts"]),
            {
                "prior_no_access",
                "provider_vs_resident",
                "provider_vs_resident_no_response",
                "non_response",
            },
        )

        extended = pairs()
        prov_ref = case("p5", 6)
        prov_ref["appointment_history"] = "provider_cancelled"
        res_sub = copy.deepcopy(prov_ref)
        res_sub["appointment_history"] = "resident_rescheduled"
        no_resp_sub = copy.deepcopy(prov_ref)
        no_resp_sub["appointment_history"] = "no_response"
        miss_sensor_ref = case("p6", 6)
        miss_sensor_sub = copy.deepcopy(miss_sensor_ref)
        miss_sensor_sub["sensor_data"] = "missing"
        partial_src_ref = case("p7", 6)
        partial_src_sub = copy.deepcopy(partial_src_ref)
        partial_src_sub["source_record"] = "partial"
        contact_ref = case("p8", 6, contact_need="digital")
        contact_sub = case("p8", 6, contact_need="assisted_non_digital")
        extended.extend(
            [
                {
                    "id": "h2",
                    "dimension": "appointment_history",
                    "contrast": "provider_vs_resident",
                    "reference": prov_ref,
                    "subject": res_sub,
                },
                {
                    "id": "h3",
                    "dimension": "appointment_history",
                    "contrast": "provider_vs_resident_no_response",
                    "reference": copy.deepcopy(prov_ref),
                    "subject": no_resp_sub,
                },
                {
                    "id": "s2",
                    "dimension": "sensor_completeness",
                    "contrast": "missing_sensor",
                    "reference": miss_sensor_ref,
                    "subject": miss_sensor_sub,
                },
                {
                    "id": "r2",
                    "dimension": "source_completeness",
                    "contrast": "partial_source",
                    "reference": partial_src_ref,
                    "subject": partial_src_sub,
                },
                {
                    "id": "n2",
                    "dimension": "support_or_contact_need",
                    "contrast": "contact_channel_need",
                    "reference": contact_ref,
                    "subject": contact_sub,
                },
            ]
        )
        rec = paired_equity.evaluate(extended, ANCHORS)
        self.assertEqual(rec["status"], "pass")
        self.assertEqual(rec["invalid_pairs"], [])
        self.assertEqual(rec["tested"], 9)

        weakened = copy.deepcopy(pairs())
        weakened[0]["expected"] = {"rank_relation": "lower_allowed"}
        bad_rec = paired_equity.evaluate(weakened, ANCHORS)
        self.assertIn(
            "s1:invalid_comparison:contradicts_predeclared_expectation",
            bad_rec["blockers"],
        )

    def test_ai_task_paired_evaluation_and_transparent_non_ai_comparison(self) -> None:
        pol = signed_policy()

        def clean_ai(items: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
            det = _rank_with_policy(items, pol)
            return {
                "status": "Proposed",
                "items": [
                    {"id": e["id"], "rank": e["rank"], "service_level": "standard"} for e in det
                ],
            }

        rec = paired_equity.evaluate(pairs(), ANCHORS, policy=pol, ai_task=clean_ai)
        self.assertEqual(rec["status"], "pass")
        self.assertTrue(rec["ranking_policy"]["signed"])
        self.assertEqual(rec["ranking_policy"]["owner"], "Priya Shah, Asset Lead")
        self.assertEqual(rec["ranking_policy"]["content_hash"], pol["content_hash"])
        self.assertFalse(rec["non_ai_comparison"]["regression_detected"])
        self.assertEqual(rec["non_ai_comparison"]["compared_pairs"], 4)

        tampered = copy.deepcopy(pol)
        tampered["rules"] = list(reversed(tampered["rules"]))
        tampered_rec = paired_equity.evaluate(pairs(), ANCHORS, policy=tampered, ai_task=clean_ai)
        self.assertIn("ranking_policy:content_hash_mismatch", tampered_rec["blockers"])
        self.assertFalse(tampered_rec["activation_allowed"])

        invalid_pol = copy.deepcopy(pol)
        invalid_pol["rules"] = [{"code": "invented_rule", "label": "Invalid"}]
        invalid_pol["signoff"]["rule_order_hash"] = _rule_order_hash(invalid_pol)
        invalid_pol["content_hash"] = _policy_hash(invalid_pol)
        invalid_rec = paired_equity.evaluate(pairs(), ANCHORS, policy=invalid_pol)
        self.assertIn("ranking_policy:invalid_policy", invalid_rec["blockers"])

        def biased_ai(items: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
            ordered = sorted(
                items,
                key=lambda c: (c.get("sensor_data") == "declined", str(c.get("id"))),
            )
            return {
                "status": "Approved",
                "items": [{"id": c["id"], "rank": idx} for idx, c in enumerate(ordered, start=1)],
            }

        biased = paired_equity.evaluate(
            pairs(), ANCHORS, seeded_defects=["s1"], policy=pol, ai_task=biased_ai
        )
        self.assertEqual(biased["status"], "blocked")
        self.assertTrue(biased["non_ai_comparison"]["regression_detected"])
        problems = biased["dimensions"]["sensor_completeness"]["failures"][0]["problems"]
        self.assertIn("ai_priority_lowered", problems)
        self.assertIn("ai_ranking_authority_violation", problems)

    def test_safe_ai_abstention_is_retained_while_service_lowering_or_prohibited_inference_fails(
        self,
    ) -> None:
        pol = signed_policy()

        def abstaining_ai(items: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
            det = _rank_with_policy(items, pol)
            rows = []
            for entry in det:
                case_obj = next(c for c in items if c["id"] == entry["id"])
                abstain = case_obj.get("sensor_data") in ("declined", "missing")
                rows.append(
                    {
                        "id": entry["id"],
                        "rank": entry["rank"],
                        "abstained": abstain,
                        "fallback_to_non_ai": abstain,
                        "service_level": "standard",
                    }
                )
            return {"status": "Proposed", "items": rows}

        ok_abstain = paired_equity.evaluate(pairs(), ANCHORS, policy=pol, ai_task=abstaining_ai)
        self.assertEqual(ok_abstain["status"], "pass")
        self.assertEqual(ok_abstain["counts"]["abstained"], 1)
        self.assertEqual(ok_abstain["dimensions"]["sensor_completeness"]["abstained"], 1)

        def penalising_service_and_inferring_ai(
            items: Sequence[Mapping[str, Any]],
        ) -> dict[str, Any]:
            det = _rank_with_policy(items, pol)
            rows = []
            for entry in det:
                case_obj = next(c for c in items if c["id"] == entry["id"])
                is_declined = case_obj.get("sensor_data") == "declined"
                is_no_access = case_obj.get("appointment_history") == "prior_no_access"
                rows.append(
                    {
                        "id": entry["id"],
                        "rank": entry["rank"],
                        "service_level": "reduced" if is_declined else "standard",
                        "inferences": (
                            {"vulnerability": "assumed_vulnerable", "refusal": "non_engaged"}
                            if is_no_access
                            else {}
                        ),
                    }
                )
            return {"status": "Proposed", "items": rows}

        bad = paired_equity.evaluate(
            pairs(),
            ANCHORS,
            seeded_defects=["s1", "h1"],
            policy=pol,
            ai_task=penalising_service_and_inferring_ai,
        )
        self.assertEqual(bad["status"], "blocked")
        self.assertEqual(bad["detected_defects"], ["h1", "s1"])
        self.assertIn(
            "service_lowered",
            bad["dimensions"]["sensor_completeness"]["failures"][0]["problems"],
        )
        self.assertIn(
            "prohibited_inference",
            bad["dimensions"]["appointment_history"]["failures"][0]["problems"],
        )

    def test_retained_cohort_version_counts_uncertainty_and_human_disposition(self) -> None:
        pol = signed_policy()
        p = pairs()
        in_dig = paired_equity.input_digest(p, ANCHORS)
        exp_approval = {
            "approved_by": "Amina Okafor, RAI Owner",
            "approved_at": "2026-11-14",
            "input_digest": in_dig,
        }
        thresholds = {
            "min_sample": 1,
            "max_error_rate": 0.0,
            "max_abstention_rate": 0.5,
            "approved_by": "Amina Okafor, RAI Owner",
            "approved_at": "2026-11-14",
            "thresholds_digest": digest(
                {"min_sample": 1, "max_error_rate": 0.0, "max_abstention_rate": 0.5}
            ),
        }
        rec = paired_equity.evaluate(
            p,
            ANCHORS,
            policy=pol,
            expectation_approval=exp_approval,
            thresholds=thresholds,
        )
        self.assertEqual(rec["status"], "pass")
        self.assertTrue(rec["activation_allowed"])
        self.assertFalse(rec["fairness_evidence"])
        self.assertFalse(rec["population_fairness_established"])
        self.assertEqual(rec["aggregation_rule"], "per_cohort_unaveraged")
        self.assertIn("cohort_definitions", rec)
        self.assertIn("version_definitions", rec)
        self.assertEqual(
            rec["counts"],
            {"eligible": 4, "tested": 4, "abstained": 0, "failed": 0},
        )
        sensor_row = rec["dimensions"]["sensor_completeness"]
        for key in (
            "eligible",
            "tested",
            "abstained",
            "failed",
            "excluded",
            "deprioritised",
            "review",
            "review_burden",
            "error_interval",
            "sufficient",
        ):
            self.assertIn(key, sensor_row)
        self.assertTrue(sensor_row["sufficient"])

        high_sample = {
            "min_sample": 3,
            "max_error_rate": 0.0,
            "max_abstention_rate": 0.5,
            "approved_by": "Amina Okafor, RAI Owner",
            "approved_at": "2026-11-14",
            "thresholds_digest": digest(
                {"min_sample": 3, "max_error_rate": 0.0, "max_abstention_rate": 0.5}
            ),
        }
        small_rec = paired_equity.evaluate(
            p,
            ANCHORS,
            policy=pol,
            expectation_approval=exp_approval,
            thresholds=high_sample,
            disposition={
                "by": "Amina Okafor, RAI Owner",
                "decision": "accept",
                "rationale": "reviewed",
            },
        )
        self.assertIn("sensor_completeness:insufficient_sample", small_rec["blockers"])
        self.assertFalse(small_rec["activation_allowed"])
        self.assertFalse(small_rec["fairness_evidence"])

        bot_disp = paired_equity.evaluate(
            p,
            ANCHORS,
            seeded_defects=["s1"],
            rank=penalise_missing,
            policy=pol,
            expectation_approval=exp_approval,
            thresholds=thresholds,
            disposition={"by": "Copilot Agent", "decision": "accept", "rationale": "auto"},
        )
        self.assertIsNone(bot_disp["disposition"])
        self.assertFalse(bot_disp["activation_allowed"])

    def test_protected_characteristic_fields_require_minimum_necessary_approval(self) -> None:
        p = pairs()
        p[0]["reference"]["resident"]["disability"] = "declared"
        p[0]["subject"]["resident"]["disability"] = "declared"
        blocked = paired_equity.evaluate(p, ANCHORS)
        self.assertIn("unapproved_protected_characteristic", blocked["blockers"])
        self.assertFalse(blocked["activation_allowed"])
        self.assertFalse(blocked["fairness_evidence"])

        in_dig = paired_equity.input_digest(p, ANCHORS)
        dpo_ok = {
            "dpo_owner": "Tom Reed, DPO",
            "lawful_basis": "Equality Act 2010 public-sector duty audit",
            "minimum_necessary_justification": "Single declared disability flag for support check",
            "approved_at": "2026-11-14",
            "approved_fields": ["disability"],
            "input_digest": in_dig,
        }
        cleared = paired_equity.evaluate(p, ANCHORS, protected_fields_approval=dpo_ok)
        self.assertNotIn("unapproved_protected_characteristic", cleared["blockers"])
        self.assertEqual(cleared["status"], "pass")
        self.assertFalse(cleared["fairness_evidence"])
        self.assertFalse(cleared["population_fairness_established"])

    def test_geography_and_archetype_dimensions_require_relevance_approval(self) -> None:
        geo_ref = case("g1", 6)
        geo_ref["geography"] = "urban_compact"
        geo_sub = copy.deepcopy(geo_ref)
        geo_sub["geography"] = "rural_dispersed"
        arch_ref = case("a1", 6)
        arch_ref["archetype"] = "post_1945_masonry"
        arch_sub = copy.deepcopy(arch_ref)
        arch_sub["archetype"] = "non_traditional_solid_wall"

        with_context = [
            *pairs(),
            {
                "id": "geo1",
                "dimension": "geography",
                "reference": geo_ref,
                "subject": geo_sub,
            },
            {
                "id": "arch1",
                "dimension": "archetype",
                "reference": arch_ref,
                "subject": arch_sub,
            },
        ]
        unapproved = paired_equity.evaluate(with_context, ANCHORS)
        self.assertIn("geography:unapproved_or_irrelevant_dimension", unapproved["blockers"])
        self.assertIn("archetype:unapproved_or_irrelevant_dimension", unapproved["blockers"])

        missing_geo_in_dig = paired_equity.input_digest(pairs(), ANCHORS)
        missing_geo = paired_equity.evaluate(
            pairs(),
            ANCHORS,
            context_approvals={
                "geography": {
                    "approved_by": "Priya Shah, Data Lead",
                    "relevant": True,
                    "rationale": "Rural contractor travel dispersal check",
                    "approved_at": "2026-11-14",
                    "input_digest": missing_geo_in_dig,
                }
            },
        )
        self.assertIn("geography:missing_dimension", missing_geo["blockers"])

        in_dig = paired_equity.input_digest(with_context, ANCHORS)
        approved_ctx = paired_equity.evaluate(
            with_context,
            ANCHORS,
            context_approvals={
                "geography": {
                    "approved_by": "Priya Shah, Data Lead",
                    "relevant": True,
                    "rationale": "Rural contractor travel dispersal check",
                    "approved_at": "2026-11-14",
                    "input_digest": in_dig,
                },
                "archetype": {
                    "approved_by": "Priya Shah, Data Lead",
                    "relevant": True,
                    "rationale": "Solid-wall retrofit survey complexity check",
                    "approved_at": "2026-11-14",
                    "input_digest": in_dig,
                },
            },
        )
        self.assertEqual(approved_ctx["status"], "pass")
        self.assertEqual(approved_ctx["dimensions"]["geography"]["tested"], 1)
        self.assertEqual(approved_ctx["dimensions"]["archetype"]["tested"], 1)

    def test_sensor_fixtures_reject_device_provisioning_and_invented_thresholds(self) -> None:
        prov_pairs = pairs()
        prov_pairs[0]["reference"]["sensor_device_id"] = "SYN-0042"
        prov_pairs[0]["subject"]["sensor_device_id"] = "SYN-0042"
        prov_rec = paired_equity.evaluate(prov_pairs, ANCHORS)
        self.assertIn("sensor_fixture_provisions_device", prov_rec["blockers"])
        self.assertFalse(prov_rec["activation_allowed"])

        thresh_pairs = pairs()
        thresh_pairs[0]["reference"]["dew_point_threshold_c"] = 12.5
        thresh_pairs[0]["subject"]["dew_point_threshold_c"] = 12.5
        thresh_rec = paired_equity.evaluate(thresh_pairs, ANCHORS)
        self.assertIn("sensor_fixture_invents_threshold", thresh_rec["blockers"])
        self.assertFalse(thresh_rec["activation_allowed"])


if __name__ == "__main__":
    unittest.main()
