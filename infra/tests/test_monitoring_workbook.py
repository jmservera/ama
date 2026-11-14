"""Source-shape regressions for optional telemetry tables in the operations workbook."""

import json
import re
import unittest
from pathlib import Path

INFRA = Path(__file__).resolve().parents[1]


class MonitoringWorkbookTests(unittest.TestCase):
    def test_optional_tables_are_bare_union_sources_with_projection_after_union(
        self,
    ) -> None:
        workbook = json.loads(
            (INFRA / "monitoring-workbook.json").read_text(encoding="utf-8")
        )
        queries = {
            item["name"]: item["content"]["query"]
            for item in workbook["items"]
            if item["type"] == 3
        }
        cases = (
            ("requests", "AppRequests", ", DurationMs:real", ", DurationMs"),
            ("availability", "AppAvailabilityResults", "", ""),
        )
        for panel, table, extra_schema, extra_projection in cases:
            with self.subTest(panel=panel, table=table):
                expected = (
                    "let samples = union isfuzzy=true "
                    "(datatable(TimeGenerated:datetime, _ResourceId:string, ItemCount:int, "
                    f"Success:bool{extra_schema})[]), {table} "
                    f"| project TimeGenerated, _ResourceId, ItemCount, Success{extra_projection}"
                )
                self.assertEqual(queries[panel].split(";", 1)[0], expected)

    def _items(self) -> dict:
        workbook = json.loads(
            (INFRA / "monitoring-workbook.json").read_text(encoding="utf-8")
        )
        return {item["name"]: item for item in workbook["items"]}

    def test_required_panels_and_columns_are_present(self) -> None:
        items = self._items()
        required = {
            "availability": ("TestSuccessPercent",),
            "requests": ("FailurePercent", "P95Ms"),
            "operation-errors-latency": ("ErrorPercent", "P95Ms", "OperationName"),
            "cost-vs-budget": ("ConfiguredMonthlyBudget", "VarianceAgainstBudget"),
            "ai-usage-by-capability": ("Capability", "Period", "UnreconciledVariance"),
            "ai-variance-by-period": (
                "Period",
                "MeteredCost",
                "BilledCost",
                "Variance",
                "UnattributedUsageRows",
                "AzureCostRows",
                "UnreconciledVariance",
            ),
        }
        for name, columns in required.items():
            with self.subTest(panel=name):
                query = items[name]["content"]["query"]
                for column in columns:
                    self.assertIn(column, query)

    def test_budget_is_notification_not_cap(self) -> None:
        text = self._items()["cost-and-budget"]["content"]["json"]
        for phrase in ("80% actual", "100% forecast", "not a hard cap"):
            self.assertIn(phrase, text)
        self.assertNotRegex(text, r"OD-51")

    def test_no_raw_prompt_or_personal_data_projected(self) -> None:
        forbidden = re.compile(
            r"prompt|completion|chat|message|email|username|userprincipal|clientip|"
            r"UserId|reading|SourceText",
            re.IGNORECASE,
        )
        for name, item in self._items().items():
            if item["type"] != 3:
                continue
            with self.subTest(panel=name):
                query = item["content"]["query"]
                self.assertIsNone(forbidden.search(query.replace("Log has", "")))

    def test_workbook_placeholders_are_declared_in_bicep(self) -> None:
        bicep = (INFRA / "modules" / "operationalMonitoring.bicep").read_text(
            encoding="utf-8"
        )
        raw = (INFRA / "monitoring-workbook.json").read_text(encoding="utf-8")
        for placeholder in set(re.findall(r"__[A-Z_]+__", raw)):
            self.assertIn(placeholder, bicep)


if __name__ == "__main__":
    unittest.main()
