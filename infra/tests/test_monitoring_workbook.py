"""Source-shape regressions for optional telemetry tables in the operations workbook."""

import json
import unittest
from pathlib import Path

INFRA = Path(__file__).resolve().parents[1]


class MonitoringWorkbookTests(unittest.TestCase):
    def test_optional_tables_are_bare_union_sources_with_projection_after_union(self) -> None:
        workbook = json.loads((INFRA / "monitoring-workbook.json").read_text(encoding="utf-8"))
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


if __name__ == "__main__":
    unittest.main()
