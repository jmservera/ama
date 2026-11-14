"""Issue #146 monitoring regressions: alert owners, runbook links, gates and workbook panels."""

import json
import re
import subprocess
import unittest
from pathlib import Path

INFRA = Path(__file__).resolve().parents[1]
MODULE = INFRA / "modules" / "operationalMonitoring.bicep"
RUNBOOK = INFRA / "monitoring-runbooks.md"


def _anchors(text: str) -> set[str]:
    heads = re.findall(r"^#{2,4} (.+)$", text, flags=re.MULTILINE)
    return {re.sub(r"[^a-z0-9 -]", "", h.lower()).strip().replace(" ", "-") for h in heads}


def _workbook_queries() -> dict[str, str]:
    workbook = json.loads((INFRA / "monitoring-workbook.json").read_text(encoding="utf-8"))
    return {i["name"]: i["content"]["query"] for i in workbook["items"] if i["type"] == 3}


class AlertOwnerAndRunbookTests(unittest.TestCase):
    def test_new_rules_name_owner_and_resolvable_runbook(self) -> None:
        source = MODULE.read_text(encoding="utf-8")
        anchors = _anchors(RUNBOOK.read_text(encoding="utf-8"))
        for rule, anchor in (
            ("agent-tasks-poison", "agent-tasks-poison"),
            ("ai-limits", "ai-limits"),
        ):
            with self.subTest(rule=rule):
                self.assertIn(f"alert-${{prefix}}-{rule}", source)
                self.assertIn(f"${{runbookBase}}#{anchor}", source)
                self.assertIn(anchor, anchors)
        self.assertEqual(source.count("proposed owner"), source.count("Runbook: ${runbookBase}#"))

    def test_new_rules_have_separate_disabled_by_default_gates(self) -> None:
        main = (INFRA / "main.bicep").read_text(encoding="utf-8")
        source = MODULE.read_text(encoding="utf-8")
        for gate in ("enablePoisonQueueAlertCandidate", "enableAiLimitAlertCandidate"):
            self.assertRegex(main, rf"param {gate} bool = false")
        self.assertIn("candidateAlertsEnabled && enablePoisonQueueAlerts", source)
        self.assertIn("candidateAlertsEnabled && enableAiLimitAlerts", source)

    def test_queue_diagnostics_use_resource_specific_tables(self) -> None:
        storage = (INFRA / "modules" / "storage.bicep").read_text(encoding="utf-8")
        self.assertIn("logAnalyticsDestinationType: 'Dedicated'", storage)

    def test_compiled_rules_are_disabled_by_default(self) -> None:
        result = subprocess.run(
            ["az", "bicep", "build", "--file", str(MODULE), "--stdout"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            self.skipTest("az bicep unavailable")
        template = json.loads(result.stdout)
        rules = {
            r["name"]: r
            for r in template["resources"]
            if r["type"] == "Microsoft.Insights/scheduledQueryRules"
        }
        named = [n for n in rules if "agent-tasks-poison" in n or "ai-limits" in n]
        self.assertEqual(len(named), 2)
        for name in named:
            self.assertIn(
                "candidateAlertsEnabled", json.dumps(rules[name]["properties"]["enabled"])
            )


class WorkbookPanelTests(unittest.TestCase):
    def test_cost_vs_budget_shows_unreconciled_variance(self) -> None:
        query = _workbook_queries()["cost-vs-budget"]
        for text in ("ConfiguredMonthlyBudget", "AzureActualCost='Unknown'", "Unreconciled"):
            self.assertIn(text, query)

    def test_ai_usage_by_capability_and_period_beside_cost_record(self) -> None:
        query = _workbook_queries()["ai-usage-by-capability"]
        for text in (
            "by Capability, Period",
            "AzureCostRecord",
            "UnreconciledVariance",
            "Non-authoritative",
        ):
            self.assertIn(text, query)

    def test_ai_limit_holds_name_owner_and_runbook(self) -> None:
        query = _workbook_queries()["ai-limit-breaches"]
        self.assertIn("AI_LIMIT_BREACH", query)
        self.assertIn("monitoring-runbooks.md#ai-limits", query)
        self.assertIn("Owner=", query)

    def test_panels_never_report_missing_data_as_zero(self) -> None:
        workbook = json.loads((INFRA / "monitoring-workbook.json").read_text(encoding="utf-8"))
        for item in workbook["items"]:
            if item["name"] in ("ai-usage-by-capability", "ai-limit-breaches"):
                self.assertTrue(item["content"]["noDataMessage"].startswith("Insufficient"))


if __name__ == "__main__":
    unittest.main()
