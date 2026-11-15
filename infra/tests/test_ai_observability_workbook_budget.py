"""Issue #146: workbook budget-vs-metered AI usage, disabled-task status and variance."""

import json
import re
import unittest
from pathlib import Path

INFRA = Path(__file__).resolve().parents[1]
RAW_CONTENT_PROJECTION = re.compile(
    r"\b(prompt|completion|messages?|email|phone|userid|user_id|upn|"
    r"address|postcode|resident_name)\b",
    re.IGNORECASE,
)


class AiObservabilityWorkbookBudgetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        workbook = json.loads(
            (INFRA / "monitoring-workbook.json").read_text(encoding="utf-8")
        )
        cls.items = {item["name"]: item["content"] for item in workbook["items"]}

    def test_capability_level_metered_tokens_and_calls(self) -> None:
        query = self.items["ai-usage-by-capability"]["query"]
        for token in (
            "by Capability, Period",
            "MeteredCalls=sum(Calls)",
            "MeteredTokens=sumif(Tokens, UsageState == 'known')",
            "CallsWithUnknownUsage",
            "ConfiguredMonthlyBudget=__MONTHLY_BUDGET__",
        ):
            self.assertIn(token, query)

    def test_unreconciled_cost_variance_is_explicit_not_zero(self) -> None:
        for name in ("ai-usage-by-capability", "ai-variance-by-period"):
            self.assertIn("Unreconciled, not zero", self.items[name]["query"])
        variance = self.items["ai-variance-by-period"]["query"]
        self.assertIn("BilledCost=real(null)", variance)
        self.assertIn("Variance=real(null)", variance)
        self.assertIn("UnattributedUsageRows", variance)
        budget = self.items["cost-vs-budget"]["query"]
        self.assertIn("AzureActualCost='Unknown'", budget)
        self.assertIn("VarianceAgainstBudget='Unreconciled'", budget)

    def test_disabled_task_status_is_blocked_not_assumed_healthy(self) -> None:
        text = self.items["ai-usage-and-harm"]["json"]
        self.assertRegex(text, r"Disabled task monitoring \|[^|]*\| Blocked")
        self.assertIn("disabled by default", text)

    def test_no_raw_prompts_or_pii_projected(self) -> None:
        for name in (
            "ai-usage-by-capability",
            "ai-variance-by-period",
            "ai-limit-breaches",
        ):
            projected = self.items[name]["query"].split("| parse", 1)[1]
            self.assertIsNone(RAW_CONTENT_PROJECTION.search(projected), name)
        text = self.items["ai-usage-and-harm"]["json"]
        self.assertIn("Do not copy prompts", text)


if __name__ == "__main__":
    unittest.main()
