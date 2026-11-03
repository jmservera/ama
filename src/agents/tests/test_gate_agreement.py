"""Synthetic unit fixtures for owner threshold agreement; not owner evidence."""

from __future__ import annotations

import unittest
from typing import Any

from zava_forward.agents.gate_agreement import apply_owner_agreement

SHA = "a" * 64
CHECKS: dict[str, dict[str, Any]] = {
    "citation_validity": dict(matched=7, total=7, failed_case_ids=[]),
    "refusal_accuracy": dict(matched=23, total=24, failed_case_ids=["x"]),
}
AGREEMENT: dict[str, Any] = dict(
    owner="Named Owner",
    independent_grader="Named Grader",
    agreed_on="2026-11-03",
    case_set_sha256=SHA,
    min_graded_cases=5,
    min_adversarial_cases=3,
    min_rates=dict(citation_validity=1.0, refusal_accuracy=0.9),
)


def run(agreement: dict[str, Any] | None, graded: int = 7, adversarial: int = 17) -> dict[str, Any]:
    return apply_owner_agreement(
        CHECKS,
        case_set_sha256=SHA,
        graded_cases=graded,
        adversarial_cases=adversarial,
        agreement=agreement,
    )


class GateAgreementTests(unittest.TestCase):
    def test_no_agreement_leaves_every_gate_unset(self) -> None:
        report = run(None)
        self.assertEqual({c["status"] for c in report["checks"]}, {"unset_pending_owner_agreement"})
        self.assertIsNone(report["overall_pass"])

    def test_gaps_are_named(self) -> None:
        bad = {**AGREEMENT, "owner": " ", "agreed_on": "soon", "case_set_sha256": "b" * 64}
        gaps = run(bad)["agreement"]["gaps"]
        self.assertIn("owner not a named person", gaps)
        self.assertIn("agreed_on not an ISO date", gaps)
        self.assertIn("agreement bound to a different case set", gaps)

    def test_grader_must_be_independent(self) -> None:
        gaps = run({**AGREEMENT, "independent_grader": "Named Owner"})["agreement"]["gaps"]
        self.assertIn("independent_grader must differ from owner", gaps)

    def test_rates_must_be_valid(self) -> None:
        bad = {**AGREEMENT, "min_rates": dict(citation_validity=0, refusal_accuracy=True)}
        self.assertEqual(len(run(bad)["agreement"]["gaps"]), 2)

    def test_results_are_per_gate_with_failures_not_passed(self) -> None:
        by_name = {c["name"]: c for c in run(AGREEMENT)["checks"]}
        self.assertEqual(by_name["citation_validity"]["status"], "owner_threshold_met")
        self.assertEqual(by_name["refusal_accuracy"]["status"], "owner_threshold_not_met")
        self.assertIn("failed cases remain", by_name["refusal_accuracy"]["reasons"])

    def test_set_size_minimums_block_a_met_result(self) -> None:
        by_name = {c["name"]: c for c in run(AGREEMENT, graded=1, adversarial=1)["checks"]}
        self.assertEqual(by_name["citation_validity"]["status"], "owner_threshold_not_met")

    def test_unmeasured_gate_is_not_met(self) -> None:
        report = apply_owner_agreement(
            {}, case_set_sha256=SHA, graded_cases=7, adversarial_cases=17, agreement=AGREEMENT
        )
        self.assertIn("gate not measured", report["checks"][0]["reasons"])


if __name__ == "__main__":
    unittest.main()
