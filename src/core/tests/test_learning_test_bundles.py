import unittest
from typing import Any

from zava_forward.core import learning_test_bundles as ltb

EFFORT = dict.fromkeys(ltb.COMPONENTS, 2.0)


def case(
    name: str, comp: float = 2.0, flow: float = 1.0, counts: dict[str, int] | None = None
) -> dict[str, Any]:
    counts = counts or {}
    return {
        "case": name,
        "arms": {
            "comparator": {"effort": dict.fromkeys(ltb.COMPONENTS, comp), "counts": counts},
            "workflow": {"effort": dict.fromkeys(ltb.COMPONENTS, flow), "counts": counts},
        },
    }


class LearningTestBundles(unittest.TestCase):
    def test_five_bundles_exclude_out_of_scope(self) -> None:
        self.assertEqual(len(ltb.BUNDLES), 5)
        for bundle in ltb.BUNDLES.values():
            self.assertFalse(ltb.OUT_OF_SCOPE & set(bundle.atlas_ids))

    def test_net_effort_sums_six_components(self) -> None:
        self.assertEqual(ltb.case_net_effort(EFFORT), 12.0)

    def test_rejects_missing_unknown_or_negative(self) -> None:
        with self.assertRaises(ValueError):
            ltb.case_net_effort({"preparation": 1})
        with self.assertRaises(ValueError):
            ltb.case_net_effort({**EFFORT, "other": 1})
        with self.assertRaises(ValueError):
            ltb.case_net_effort({**EFFORT, "checking": -1})

    def test_median_range_and_capacity_label(self) -> None:
        zero = {"inferred_submissions": 0}
        out = ltb.compare_bundle(
            "funding-evidence",
            [case("a", 2, 1, zero), case("b", 3, 1, zero), case("c", 5, 2, zero)],
        )
        self.assertEqual(out["comparator"]["median_minutes"], 18.0)
        self.assertEqual(out["workflow"]["max_minutes"], 12.0)
        self.assertEqual(out["workflow"]["cases"], 3)
        self.assertFalse(out["stop"])
        self.assertIn("capacity", out["capacity_note"])
        self.assertEqual(out["evidence_label"], "constructed-case evidence")

    def test_comparator_win_is_valid_outcome(self) -> None:
        out = ltb.compare_bundle(
            "handover-aftercare", [case("a", 1, 3, {"open_remedies_hidden": 0})]
        )
        self.assertEqual(out["direction"], "comparator lower or equal")
        self.assertFalse(out["stop"])

    def test_nonzero_target_zero_count_stops_bundle(self) -> None:
        out = ltb.compare_bundle(
            "change-impact", [case("a", 2, 1, {"approvals_wrongly_carried_over": 1})]
        )
        self.assertTrue(out["stop"])
        self.assertIn("a/workflow/approvals_wrongly_carried_over", out["breaches"])

    def test_missing_count_arm_or_case_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ltb.compare_bundle("pre-visit-pack", [case("a")])
        with self.assertRaises(ValueError):
            ltb.compare_bundle("pre-visit-pack", [])
        with self.assertRaises(ValueError):
            ltb.compare_bundle("nope", [case("a")])
        one_arm = {"case": "x", "arms": {"comparator": case("x")["arms"]["comparator"]}}
        with self.assertRaises(ValueError):
            ltb.compare_bundle("pre-visit-pack", [one_arm])


if __name__ == "__main__":
    unittest.main()
