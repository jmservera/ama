"""Capped real-AI acceptance harness refuses, stops at caps and never spends by accident (#107)."""

import unittest
from datetime import UTC, datetime, timedelta
from typing import Any

from checks import assistant_real_ai_acceptance as harness

AUTH: dict[str, Any] = dict(
    approved_by="Jordan Example",
    authority_ref="OWNER-CAP-1",
    model="gpt-test",
    expires_utc=(datetime.now(UTC) + timedelta(days=1)).isoformat(),
    max_calls=5,
    max_total_tokens=5000,
    max_prompt_tokens=500,
    max_completion_tokens=100,
    max_budget_usd="0.50",
    currency="USD",
    input_usd_per_1m="1",
    output_usd_per_1m="2",
)


def listing(ready: tuple[str, ...] = ()) -> dict[str, Any]:
    denied = dict(reason="Release admission denied: no approved release matches", missing=["x"])
    return dict(
        assistants=[
            dict(id=n, release=dict(id="rel-1") if n in ready else denied)
            for n in harness.ASSISTANTS
        ]
    )


class Counting:
    def __init__(self, usage: Any = None) -> None:
        self.calls = 0
        self.usage = usage or dict(prompt_tokens=40, completion_tokens=10, total_tokens=50)

    def __call__(self, system: str, prompt: str, max_tokens: int, timeout: int) -> dict[str, Any]:
        self.calls += 1
        return dict(outcome="returned", usage=self.usage)


class RealAiHarness(unittest.TestCase):
    def test_denied_listing_blocks_with_zero_calls(self) -> None:
        provider = Counting()
        report = harness.run(AUTH, listing(), "live", provider, True)
        self.assertEqual((report["outcome"], provider.calls), ("blocked", 0))
        self.assertEqual(len(report["blocked"]), 5)

    def test_invalid_authorization_refuses_before_any_call(self) -> None:
        provider = Counting()
        bad = dict(AUTH, approved_by="the agent", max_budget_usd="50")
        report = harness.run(bad, listing(harness.ASSISTANTS), "live", provider, True)
        self.assertEqual((report["outcome"], provider.calls), ("refused", 0))

    def test_live_needs_flag_and_provider(self) -> None:
        provider = Counting()
        ready = listing(harness.ASSISTANTS)
        self.assertEqual(harness.run(AUTH, ready, "live", provider, False)["outcome"], "refused")
        self.assertEqual(harness.run(AUTH, ready, "live", None, True)["outcome"], "refused")
        self.assertEqual(provider.calls, 0)

    def test_dry_run_is_labelled_and_uses_no_provider(self) -> None:
        report = harness.run(AUTH, listing(harness.ASSISTANTS[:2]))
        self.assertEqual(report["outcome"], "completed")
        self.assertEqual(len(report["calls"]), 2)
        self.assertIn("not measured evidence", report["label"])

    def test_live_runs_only_ready_assistants_and_sums_usage(self) -> None:
        provider = Counting()
        report = harness.run(AUTH, listing(harness.ASSISTANTS[:3]), "live", provider, True)
        self.assertEqual(
            (report["outcome"], provider.calls, report["tokens"]), ("completed", 3, 150)
        )

    def test_preflight_refuses_when_worst_case_exceeds_cap(self) -> None:
        small = dict(AUTH, max_total_tokens=1200)
        report = harness.run(small, listing(harness.ASSISTANTS), "dry-run")
        self.assertEqual(report["outcome"], "refused")
        self.assertTrue(any("max_total_tokens" in p for p in report["problems"]))

    def test_malformed_usage_stops_batch_at_worst_case(self) -> None:
        provider = Counting(usage=dict(prompt_tokens=9999, completion_tokens=1, total_tokens=10000))
        report = harness.run(AUTH, listing(harness.ASSISTANTS), "live", provider, True)
        self.assertEqual(
            (report["outcome"], provider.calls, report["tokens"]), ("stopped-bad-usage", 1, 600)
        )

    def test_release_without_id_or_with_denial_is_not_admitted(self) -> None:
        self.assertFalse(harness.admitted(dict(release=dict(reason="denied", id="r"))))
        self.assertFalse(harness.admitted(dict(release=dict())))
        self.assertFalse(harness.admitted(dict(release="in force")))


if __name__ == "__main__":
    unittest.main()
