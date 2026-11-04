"""Synthetic fixtures for the freeze check; they are not held-out evidence."""

from __future__ import annotations

import copy
import unittest
from typing import Any

from zava_forward.agents.heldout_freeze import _digest, check_freeze


def manifest() -> dict[str, Any]:
    m: dict[str, Any] = dict(
        versions=dict(task="t-1", model="m-1", prompt="p-1", policy="pol-1", source="s-1"),
        held_out=dict(
            case_ids=["h1", "h2", "h3", "h4"],
            seed="seed-7",
            denominator=4,
            labelled_by="labeller a",
            prompt_author="author b",
            expected=dict(h1="accept", h2="refuse", h3="accept", h4="refuse"),
            critical_errors=["unsupported citation"],
        ),
        prompt_case_ids=["p1"],
        tuning_case_ids=[],
        thresholds=dict(max_critical_misses=0, min_accuracy=0.9, min_sample_per_cohort=2),
        cohorts=dict(a=["h1", "h2"], b=["h3", "h4"]),
    )
    m["threshold_approval"] = dict(by="owner", manifest_digest=_digest(m))
    return m


class FreezeTests(unittest.TestCase):
    def gaps(self, m: dict[str, Any]) -> str:
        result = check_freeze(m)
        self.assertEqual(result["outcome"], "insufficient")
        return " | ".join(result["gaps"])

    def test_complete_manifest_is_frozen_with_digest(self) -> None:
        result = check_freeze(manifest())
        self.assertEqual((result["outcome"], result["gaps"]), ("frozen", []))
        self.assertEqual(result["held_out_cases"], 4)
        self.assertEqual(len(result["manifest_digest"]), 64)

    def test_empty_manifest_is_insufficient_not_error(self) -> None:
        self.assertEqual(check_freeze({})["outcome"], "insufficient")

    def test_missing_version_is_named(self) -> None:
        m = manifest()
        del m["versions"]["prompt"]
        self.assertIn("versions.prompt", self.gaps(m))

    def test_overlap_with_prompt_or_tuning_cases_blocks(self) -> None:
        m = manifest()
        m["tuning_case_ids"] = ["h2"]
        self.assertIn("overlap prompt or tuning cases: h2", self.gaps(m))

    def test_unrecorded_prompt_cases_block(self) -> None:
        m = manifest()
        del m["prompt_case_ids"]
        self.assertIn("prompt_case_ids", self.gaps(m))

    def test_labeller_must_be_independent(self) -> None:
        m = manifest()
        m["held_out"]["labelled_by"] = " Author B "
        self.assertIn("not independent", self.gaps(m))

    def test_denominator_and_duplicates(self) -> None:
        m = manifest()
        m["held_out"]["denominator"] = 5
        m["held_out"]["case_ids"] = ["h1", "h1", "h3", "h4"]
        text = self.gaps(m)
        self.assertIn("denominator", text)
        self.assertIn("duplicates", text)

    def test_expected_outcome_and_critical_errors_required(self) -> None:
        m = manifest()
        del m["held_out"]["expected"]["h4"]
        m["held_out"]["critical_errors"] = []
        text = self.gaps(m)
        self.assertIn("expected outcome", text)
        self.assertIn("critical errors", text)

    def test_small_cohort_blocks(self) -> None:
        m = manifest()
        m["cohorts"]["a"] = ["h1"]
        self.assertIn("cohort a has 1 cases", self.gaps(m))

    def test_cohort_outside_split_blocks(self) -> None:
        m = manifest()
        m["cohorts"]["b"] = ["h3", "zzz"]
        self.assertIn("cohort b is not a subset", self.gaps(m))

    def test_unapproved_thresholds_block(self) -> None:
        m = manifest()
        del m["threshold_approval"]
        self.assertIn("lack named approval", self.gaps(m))

    def test_approval_is_invalidated_by_any_later_change(self) -> None:
        m = manifest()
        m["thresholds"]["min_accuracy"] = 0.5
        self.assertIn("lack named approval", self.gaps(m))

    def test_inputs_are_not_mutated(self) -> None:
        m = manifest()
        before = copy.deepcopy(m)
        check_freeze(m)
        self.assertEqual(m, before)


if __name__ == "__main__":
    unittest.main()
