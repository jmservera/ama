"""Issue #146: the cost panel reconciles Azure cost export rows or stays unreconciled."""

import json
import unittest
from pathlib import Path

INFRA = Path(__file__).resolve().parents[1]


class MonitoringWorkbookCostReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        workbook = json.loads(
            (INFRA / "monitoring-workbook.json").read_text(encoding="utf-8")
        )
        items = {item["name"]: item["content"] for item in workbook["items"]}
        cls.query = items["cost-vs-budget"]["query"]
        cls.text = items["cost-and-budget"]["json"]

    def test_reads_optional_cost_export_tables_fuzzily(self) -> None:
        self.assertIn("union isfuzzy=true", self.query)
        self.assertIn("AzureCostExport_CL", self.query)
        self.assertIn("FocusCost_CL", self.query)
        self.assertGreaterEqual(self.query.count("datatable("), 2)

    def test_requires_same_period_and_currency(self) -> None:
        for token in (
            "startofmonth({TimeRange:start}) == startofmonth({TimeRange:end})",
            "BillingPeriodStart == PeriodStart",
            "Currency =~ ExpectedCurrency",
        ):
            self.assertIn(token, self.query)

    def test_computes_reconciliation_columns(self) -> None:
        for column in (
            "ConfiguredMonthlyBudget=__MONTHLY_BUDGET__",
            "AzureActualCost",
            "AzureForecast",
            "PercentOfBudget",
            "VarianceAgainstBudget",
        ):
            self.assertIn(column, self.query)

    def test_unmatched_rows_fall_back_to_unknown_never_zero(self) -> None:
        for token in (
            "AzureActualCost='Unknown'",
            "AzureForecast='Unknown'",
            "VarianceAgainstBudget='Unreconciled'",
            "MatchedRows > 0",
            "this is not zero spend",
        ):
            self.assertIn(token, self.query)

    def test_notification_is_not_a_hard_cap(self) -> None:
        for token in ("80% actual", "100% forecast", "not a hard cap"):
            self.assertIn(token, self.text)


if __name__ == "__main__":
    unittest.main()
