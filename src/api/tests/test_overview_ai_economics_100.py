"""Overview AI consumption economics keep Unknown, not zero (issue 100, tokenomics criterion)."""

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path
from typing import Any, cast

from zava_forward.core import tokenomics

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
APP = (WEB / "app.js").read_text()


def _rows(econ: object) -> dict[str, Any]:
    found = re.search(
        r"// Formats the server's AI consumption economics.*?\nfunction aiEconomicsRows.*?\n}\n",
        APP,
        re.DOTALL,
    )
    assert found
    script = found.group(0) + f"console.log(JSON.stringify(aiEconomicsRows({json.dumps(econ)})));"
    out = subprocess.run(["node", "-e", script], capture_output=True, text=True, check=True)
    return cast(dict[str, Any], json.loads(out.stdout))


@unittest.skipUnless(shutil.which("node"), "node is required")
class OverviewAiEconomicsTests(unittest.TestCase):
    def test_unpriced_server_summary_renders_every_cost_as_unknown_with_zero_denominators(
        self,
    ) -> None:
        rows = _rows(tokenomics.summarize_ai_consumption_economics(recommendations=[]))
        self.assertTrue(rows["available"])
        self.assertEqual({value for _, value in rows["costs"]}, {"Unknown"})
        self.assertEqual({value for _, value in rows["denominators"]}, {"0"})
        self.assertEqual(rows["priceSource"], "Unknown")
        self.assertIn("never evidence of efficiency", rows["notice"])

    def test_missing_summary_is_all_unknown_not_blank_or_zero(self) -> None:
        cases: list[object] = [None, {}]
        for econ in cases:
            with self.subTest(econ=econ):
                rows = _rows(econ)
                self.assertEqual({value for _, value in rows["costs"]}, {"Unknown"})
                self.assertEqual({value for _, value in rows["denominators"]}, {"Unknown"})
        self.assertFalse(_rows(None)["available"])

    def test_zero_valued_decimal_strings_render_unknown_not_zero(self) -> None:
        zeros = ["0", "0.0", "0.000000", " 0.00 ", "-0", ".0"]
        for zero in zeros:
            with self.subTest(zero=zero):
                rows = _rows({"currency": "GBP", "token_cost": zero, "booked_value": "12.50"})
                costs = dict(rows["costs"])
                self.assertEqual(costs["Token cost"], "Unknown")
                self.assertEqual(costs["Booked value"], "GBP 12.50")

    def test_per_outcome_costs_are_unknown_without_an_accepted_outcome_count(self) -> None:
        per_outcome = {
            "token_cost_per_accepted_outcome": "0.5",
            "cost_per_accepted_outcome": "1.5",
            "quality_qualified_cost_per_accepted_outcome": "2.5",
        }
        for denominators in ({"accepted_outcome_count": 0}, {}, {"accepted_outcome_count": None}):
            with self.subTest(denominators=denominators):
                rows = _rows(
                    {
                        "currency": "GBP",
                        "token_cost": "9.00",
                        **per_outcome,
                        "denominators": denominators,
                    }
                )
                costs = dict(rows["costs"])
                self.assertEqual(costs["Token cost"], "GBP 9.00")
                for label in (
                    "Token cost per accepted outcome",
                    "Cost per accepted outcome",
                    "Quality-qualified cost per accepted outcome",
                ):
                    self.assertEqual(costs[label], "Unknown")

    def test_every_cost_is_unknown_when_no_price_source_is_configured(self) -> None:
        rows = _rows(
            {
                "currency": "GBP",
                "price_source_configured": False,
                "token_cost": "9.00",
                "total_cost_of_ai": "9.00",
                "cost_per_accepted_outcome": "3.00",
                "booked_value": "20.00",
                "denominators": {"accepted_outcome_count": 3},
            }
        )
        self.assertEqual({value for _, value in rows["costs"]}, {"Unknown"})

    def test_priced_values_show_currency_and_zero_cost_is_not_displayed_as_a_number(self) -> None:
        rows = _rows(
            {
                "currency": "USD",
                "price_source": "https://prices.azure.com/api/retail/prices",
                "token_cost": "0.0125",
                "total_cost_of_ai": 0,
                "cost_per_accepted_outcome": None,
                "denominators": {"proposal_count": 1200, "accepted_outcome_count": 3},
            }
        )
        costs = dict(rows["costs"])
        self.assertEqual(costs["Token cost"], "USD 0.0125")
        self.assertEqual(costs["Total cost of AI"], "Unknown")
        self.assertEqual(costs["Cost per accepted outcome"], "Unknown")
        self.assertEqual(dict(rows["denominators"])["AI proposals"], "1,200")
        self.assertIn("overviewView", APP)
        self.assertIn("aiEconomicsCard(st.ai_consumption_economics)", APP)
