"""Per-skill tokenomics exports split cached, uncached and reasoning tokens and name the tariff."""

from __future__ import annotations

import unittest
from typing import Any

import test_ai_consumption as base
from zava_forward.core.ai_consumption import (
    UNKNOWN,
    cost_per_accepted_outcome,
    reference,
    tariff_basis,
    token_breakdown,
    usage,
)


class SkillBreakdownTests(unittest.TestCase):
    def setUp(self) -> None:
        helper = base.ConsumptionTests("report")
        helper.setUp()
        self.addCleanup(helper.doCleanups)
        self.authorize, self.context = helper.authorize, helper.context
        self.complete, self.report = helper.complete, helper.report
        self.ledger = helper.ledger

    def run_call(self, root: str, capability: str, **tokens: int | dict[str, int]) -> None:
        self.authorize(capability=capability, authority=f"auth-{capability}")
        ticket = self.ledger.reserve(
            self.context(capability, root=reference(root), capability=capability),
            base.MODEL,
            1000,
            100,
        )
        self.complete(ticket, **tokens)

    def test_usage_reads_reasoning_tokens_and_rejects_invalid(self) -> None:
        base = dict(prompt_tokens=10, completion_tokens=5, total_tokens=15)
        self.assertNotIn("reasoning_tokens", usage(base) or {})
        nested = usage(base | {"completion_tokens_details": {"reasoning_tokens": 3}})
        self.assertEqual(nested["reasoning_tokens"], 3)  # type: ignore[index]
        for bad in (6, True, -1):
            with self.subTest(bad=bad):
                self.assertIsNone(usage(base | {"reasoning_tokens": bad}))

    def test_breakdown_separates_cached_uncached_and_reasoning(self) -> None:
        self.run_call("r1", "assessment", reasoning_tokens=7)
        self.run_call("r2", "funding-evidence", cached_tokens=0)
        rows = self.report()["by_capability"]
        self.assertEqual(
            rows["assessment"]["token_breakdown"],
            dict(
                input_tokens=100,
                cached_input_tokens=10,
                uncached_input_tokens=90,
                completion_tokens=20,
                reasoning_tokens=7,
            ),
        )
        other = rows["funding-evidence"]["token_breakdown"]
        self.assertEqual((other["cached_input_tokens"], other["uncached_input_tokens"]), (0, 100))
        self.assertEqual(other["reasoning_tokens"], UNKNOWN)

    def test_breakdown_is_unknown_when_any_call_lacks_a_field(self) -> None:
        self.assertEqual(token_breakdown([])["cached_input_tokens"], UNKNOWN)
        partial = token_breakdown(
            [
                dict(prompt_tokens=5, completion_tokens=1, cached_tokens=2),
                dict(prompt_tokens=5, completion_tokens=1, cached_tokens=None),
                None,
            ]
        )
        self.assertEqual(partial["cached_input_tokens"], UNKNOWN)
        self.assertEqual(partial["input_tokens"], UNKNOWN)

    def test_tariff_basis_labels_demo_live_and_mixed(self) -> None:
        self.assertEqual(tariff_basis(set()), UNKNOWN)
        self.assertEqual(tariff_basis({True}), "offline-demo-tariff")
        self.assertEqual(tariff_basis({False}), "live-tariff-supplied-unverified")
        self.assertEqual(tariff_basis({True, False}), "mixed-demo-and-live-tariff")

    def test_report_names_tariff_basis_per_skill_and_overall(self) -> None:
        self.run_call("r1", "assessment")
        report = self.report()
        self.assertEqual(report["tariff_basis"], "offline-demo-tariff")
        self.assertEqual(
            report["by_capability"]["assessment"]["tariff_basis"], "offline-demo-tariff"
        )


class CostPerAcceptedOutcomeTests(unittest.TestCase):
    ok: dict[str, Any] = dict(
        price_retrieved=[1793491200.0],
        financial_source="bill-1",
        reconciliation="reconciled",
        token_cost="0.0004",
        accepted=2,
        quality_status="Pass",
    )

    def test_priced_only_with_dated_price_and_reconciled_bill(self) -> None:
        got = cost_per_accepted_outcome(**self.ok)
        self.assertEqual((got["cost"], got["reason"]), ("0.0002", "priced"))
        self.assertEqual(got["quality_floor"], "met")

    def test_missing_evidence_is_unpriced_never_a_number(self) -> None:
        for change, reason in (
            (dict(price_retrieved=[]), "dated price"),
            (dict(price_retrieved=[None]), "dated price"),
            (dict(financial_source=None), "reconciled billing"),
            (dict(reconciliation="variance-alert"), "reconciled billing"),
            (dict(token_cost=UNKNOWN), "reconciled billing"),
            (dict(accepted=0), "no accepted"),
        ):
            with self.subTest(change=change):
                got = cost_per_accepted_outcome(**(self.ok | change))
                self.assertIsNone(got["cost"])
                self.assertIn(reason, got["reason"])

    def test_report_states_cost_only_when_billing_reconciles(self) -> None:
        helper = base.ConsumptionTests("report")
        helper.setUp()
        self.addCleanup(helper.doCleanups)
        helper.accepted()
        self.assertIsNone(helper.report()["cost_per_accepted_outcome"]["cost"])
        helper.bill()
        got = helper.report()["cost_per_accepted_outcome"]
        self.assertEqual(got["reason"], "priced")
        self.assertEqual(got["cost"], "0.000135")
