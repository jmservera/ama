"""Issue #146: workbook shows availability, errors, latency and cost against budget."""

import json
import re
import unittest
from pathlib import Path

INFRA = Path(__file__).resolve().parents[1]
FORBIDDEN_PROJECTIONS = re.compile(
    r"\b(prompt|completion|message|messages|email|phone|userid|user_id|"
    r"upn|name_of_resident|address|postcode)\b",
    re.IGNORECASE,
)


class MonitoringWorkbookSlaBudgetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.workbook = json.loads(
            (INFRA / "monitoring-workbook.json").read_text(encoding="utf-8")
        )
        cls.items = {item["name"]: item for item in cls.workbook["items"]}

    def _query(self, name: str) -> str:
        return self.items[name]["content"]["query"]

    def test_arm_workbook_shape(self) -> None:
        self.assertEqual(self.workbook["version"], "Notebook/1.0")
        self.assertIn("workbook", self.workbook["$schema"])
        self.assertIsInstance(self.workbook["items"], list)
        self.assertEqual(len(self.items), len(self.workbook["items"]))
        for item in self.workbook["items"]:
            self.assertIn(item["type"], {1, 3, 9})
            self.assertTrue(item["name"])

    def test_availability_errors_and_latency_tiles(self) -> None:
        availability = self._query("availability")
        self.assertIn("AppAvailabilityResults", availability)
        self.assertIn("TestSuccessPercent", availability)
        requests = self._query("requests")
        self.assertIn("FailurePercent", requests)
        self.assertIn("percentilew", requests)
        self.assertIn("P95Ms", requests)
        per_operation = self._query("operation-errors-latency")
        self.assertIn("ErrorPercent", per_operation)
        self.assertIn("percentilew", per_operation)

    def test_cost_against_budget_is_explicit_and_unfabricated(self) -> None:
        text = self.items["cost-and-budget"]["content"]["json"]
        self.assertIn("80% actual", text)
        self.assertIn("100% forecast", text)
        self.assertIn("not a hard cap", text)
        query = self._query("cost-vs-budget")
        for token in (
            "ConfiguredMonthlyBudget=__MONTHLY_BUDGET__",
            "AzureActualCost='Unknown'",
            "AzureForecast='Unknown'",
            "VarianceAgainstBudget='Unreconciled'",
        ):
            self.assertIn(token, query)

    def test_metered_ai_usage_variance_preserved(self) -> None:
        self.assertIn("ai-usage-by-capability", self.items)
        self.assertIn("ai-variance-by-period", self.items)
        self.assertIn("ai-limit-breaches", self.items)

    def test_queries_do_not_project_raw_prompts_or_pii(self) -> None:
        for name, item in self.items.items():
            if item["type"] != 3:
                continue
            query = item["content"]["query"]
            projected = " ".join(
                re.findall(r"\b(?:project|by)\b([^|]*)", query, re.IGNORECASE)
            )
            with self.subTest(panel=name):
                self.assertIsNone(FORBIDDEN_PROJECTIONS.search(projected))


if __name__ == "__main__":
    unittest.main()
