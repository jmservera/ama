import unittest
from collections.abc import Callable
from typing import Any

from zava_forward.agents import ai_eval

confirm: Callable[[dict[str, Any]], dict[str, Any]] = ai_eval.region_confirmation


def deployment(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = dict(
        name="d",
        model="gpt-4.1-nano",
        version="2025-04-14",
        sku="Standard",
        capacity=10,
        rate_limits=dict(requests_per_minute=10, tokens_per_minute=10000),
        state="Succeeded",
    )
    base.update(overrides)
    return base


def record(*deployments: dict[str, Any], quota: str = "confirmed") -> dict[str, Any]:
    return dict(
        region="uksouth",
        account="a",
        retrieved_on="2026-11-28",
        source="az",
        deployments=list(deployments),
        quota_headroom=dict(status=quota),
    )


class RegionConfirmationBranchTests(unittest.TestCase):
    def test_non_succeeded_state_alone_is_incomplete_and_named(self) -> None:
        result = confirm(record(deployment(state="Creating")))
        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["missing"], ["d: state Creating"])

    def test_empty_deployments_stay_incomplete_even_with_confirmed_quota(self) -> None:
        result = confirm(record())
        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["missing"], ["deployments"])

    def test_empty_rate_limits_count_as_absent(self) -> None:
        result = confirm(record(deployment(rate_limits={})))
        self.assertEqual(result["status"], "incomplete")
        self.assertIn("rate_limits", result["missing"][0])

    def test_unnamed_deployment_is_labelled(self) -> None:
        result = confirm(record(deployment(name="")))
        self.assertTrue(result["missing"][0].startswith("unnamed deployment: name"))

    def test_unconfirmed_quota_never_upgrades_incomplete_to_partial(self) -> None:
        result = confirm(record(deployment(state="Failed"), quota="unavailable"))
        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["missing"], ["d: state Failed", "quota headroom"])


if __name__ == "__main__":
    unittest.main()
