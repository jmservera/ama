import copy
import unittest
from collections.abc import Mapping, Sequence
from typing import Any

from zava_forward.core import paired_equity, ranking


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


class PairedEquityTests(unittest.TestCase):
    def test_current_policy_never_lowers_priority_for_any_dimension(self) -> None:
        rec = paired_equity.evaluate(pairs(), ANCHORS)
        self.assertEqual(rec["status"], "pass")
        self.assertEqual((rec["tested"], rec["failed"]), (3, 0))
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
        self.assertEqual(rec["tested"], 2)
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
        self.assertEqual(rec["tested"], 2)

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

    def test_inputs_are_not_mutated(self) -> None:
        p, a = pairs(), copy.deepcopy(ANCHORS)
        before = copy.deepcopy(p)
        paired_equity.evaluate(p, a)
        self.assertEqual((p, a), (before, ANCHORS))


if __name__ == "__main__":
    unittest.main()
