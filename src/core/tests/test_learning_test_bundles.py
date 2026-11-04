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


def run(bundle: str, counts: dict[str, int], **extra: Any) -> dict[str, Any]:
    return {
        "bundle": bundle,
        "representative_data_retained": False,
        "cases": [case("a", 2, 1, counts)],
        **extra,
    }


class RunReports(unittest.TestCase):
    def test_o16_bundle_must_name_owner(self) -> None:
        zero = {"inferred_submissions": 0}
        with self.assertRaises(ValueError):
            ltb.run_report(run("funding-evidence", zero))
        with self.assertRaises(ValueError):
            ltb.run_report(run("funding-evidence", zero, o16_counted_under="other"))
        out = ltb.run_report(run("funding-evidence", zero, o16_counted_under="change-impact"))
        self.assertEqual(out["o16_counted_under"], "change-impact")

    def test_owner_rejected_for_bundle_without_o16(self) -> None:
        zero = {"offers_misread_as_commitments": 0}
        with self.assertRaises(ValueError):
            ltb.run_report(run("pre-visit-pack", zero, o16_counted_under="change-impact"))
        self.assertIsNone(ltb.run_report(run("pre-visit-pack", zero))["o16_counted_under"])

    def test_retention_must_be_stated_false(self) -> None:
        bad = run("pre-visit-pack", {"offers_misread_as_commitments": 0})
        bad["representative_data_retained"] = True
        with self.assertRaises(ValueError):
            ltb.run_report(bad)
        del bad["representative_data_retained"]
        with self.assertRaises(ValueError):
            ltb.run_report(bad)

    def test_reconcile_o16_rejects_conflict(self) -> None:
        a = {"bundle": "change-impact", "o16_counted_under": "change-impact"}
        b = {"bundle": "funding-evidence", "o16_counted_under": "funding-evidence"}
        c = {"bundle": "funding-evidence", "o16_counted_under": "change-impact"}
        self.assertEqual(ltb.reconcile_o16([a, c]), "change-impact")
        self.assertIsNone(ltb.reconcile_o16([{"bundle": "pre-visit-pack"}]))
        with self.assertRaises(ValueError):
            ltb.reconcile_o16([a, b])
        with self.assertRaises(ValueError):
            ltb.reconcile_o16([a, {"bundle": "funding-evidence"}, a])
        with self.assertRaises(ValueError):
            ltb.reconcile_o16([{"bundle": "change-impact"}])
        with self.assertRaises(ValueError):
            ltb.reconcile_o16([{"bundle": "change-impact", "o16_counted_under": "bogus"}])
        with self.assertRaises(ValueError):
            ltb.reconcile_o16([{"bundle": "pre-visit-pack", "o16_counted_under": "change-impact"}])
        with self.assertRaises(ValueError):
            ltb.reconcile_o16([{"bundle": "nope"}])

    def test_render_states_stop_first_and_capacity(self) -> None:
        report = ltb.run_report(
            run(
                "change-impact",
                {"approvals_wrongly_carried_over": 1},
                o16_counted_under="change-impact",
            )
        )
        lines = ltb.render_report(report).splitlines()
        self.assertTrue(lines[1].startswith("STOP:"))
        text = "\n".join(lines)
        self.assertIn("capacity", text)
        self.assertIn("constructed-case evidence", text)
        self.assertIn("O16 counted under: change-impact", text)
        ok = ltb.render_report(
            ltb.run_report(run("pre-visit-pack", {"offers_misread_as_commitments": 0}))
        )
        self.assertIn("no breach recorded", ok)


if __name__ == "__main__":
    unittest.main()
