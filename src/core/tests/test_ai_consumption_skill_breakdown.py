"""Per-skill tokenomics exports split cached, uncached and reasoning tokens and name the tariff."""

from __future__ import annotations

import unittest

from tests import test_ai_consumption as base

from zava_forward.core.ai_consumption import UNKNOWN, tariff_basis, token_breakdown, usage


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
            self.context(capability, root=base.reference(root), capability=capability),
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
