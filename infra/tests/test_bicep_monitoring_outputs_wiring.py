"""Source-shape contract for main.bicep -> operationalMonitoring.bicep wiring (issue 146)."""

import re
import unittest
from pathlib import Path

INFRA = Path(__file__).resolve().parents[1]
MAIN = (INFRA / "main.bicep").read_text(encoding="utf-8")
MODULE = (INFRA / "modules" / "operationalMonitoring.bicep").read_text(encoding="utf-8")
MONITORING = (INFRA / "modules" / "monitoring.bicep").read_text(encoding="utf-8")
WORKBOOK = (INFRA / "monitoring-workbook.json").read_text(encoding="utf-8")


def module_params(text: str) -> dict[str, bool]:
    """Map each param name to whether it declares a default value."""
    return {
        m.group(1): m.group(2) is not None
        for m in re.finditer(r"^param (\w+) [^=\n]+?(?: (=) .*)?$", text, re.MULTILINE)
    }


def call_args(text: str, module: str) -> dict[str, str]:
    block = re.search(
        rf"^module {module} '[^']+' = \{{.*?^  params: \{{\n(.*?)^  \}}\n\}}",
        text,
        re.MULTILINE | re.DOTALL,
    )
    assert block, module
    return dict(re.findall(r"^    (\w+): (.+)$", block.group(1), re.MULTILINE))


class MonitoringOutputsWiringTests(unittest.TestCase):
    def test_main_supplies_every_required_module_param_and_no_unknown_ones(
        self,
    ) -> None:
        params = module_params(MODULE)
        args = call_args(MAIN, "operationalMonitoring")
        required = {name for name, has_default in params.items() if not has_default}
        self.assertFalse(required - args.keys())
        self.assertFalse(args.keys() - params.keys())

    def test_resource_ids_come_from_monitoring_module_outputs(self) -> None:
        args = call_args(MAIN, "operationalMonitoring")
        outputs = set(re.findall(r"^output (\w+) string", MONITORING, re.MULTILINE))
        for param, output in (
            ("workspaceId", "workspaceId"),
            ("appInsightsId", "appInsightsId"),
            ("actionGroupId", "actionGroupId"),
        ):
            with self.subTest(param=param):
                self.assertEqual(args[param], f"monitoring.outputs.{output}")
                self.assertIn(output, outputs)

    def test_budget_and_amount_flow_to_workbook_placeholders(self) -> None:
        args = call_args(MAIN, "operationalMonitoring")
        self.assertEqual(args["budgetName"], "budget.name")
        self.assertEqual(args["monthlyBudget"], "monthlyBudget")
        self.assertIn("resource budget 'Microsoft.Consumption/budgets", MAIN)
        self.assertIn("amount: monthlyBudget", MAIN)

    def test_every_workbook_placeholder_is_replaced_by_the_module(self) -> None:
        placeholders = set(re.findall(r"__[A-Z_]+__", WORKBOOK))
        replaced = set(re.findall(r"'(__[A-Z_]+__)'", MODULE))
        self.assertEqual(placeholders, replaced)

    def test_alert_gates_are_default_false_and_forwarded_from_main(self) -> None:
        args = call_args(MAIN, "operationalMonitoring")
        for param, source in (
            ("enablePoisonQueueAlerts", "enablePoisonQueueAlertCandidate"),
            ("enableAiLimitAlerts", "enableAiLimitAlertCandidate"),
            ("enableCandidateAlerts", "enableCandidateMonitoringAlerts"),
            ("approvalReference", "monitoringApprovalReference"),
        ):
            with self.subTest(param=param):
                self.assertEqual(args[param], source)
                self.assertRegex(MODULE, rf"param {param} \w+ = (false|'')")
                self.assertRegex(MAIN, rf"param {source} \w+ = (false|'')")

    def test_workbook_output_is_exposed_through_main(self) -> None:
        self.assertIn("output workbookId string = workbook.id", MODULE)
        self.assertIn(
            "output operationsWorkbookId string = "
            "operationalMonitoring.outputs.workbookId",
            MAIN,
        )

    def test_every_alert_resource_targets_the_action_group_param(self) -> None:
        resources = re.findall(
            r"^resource (\w+) 'Microsoft\.Insights/(\w+)@", MODULE, re.MULTILINE
        )
        alerts = [name for name, kind in resources if kind != "workbooks"]
        self.assertGreaterEqual(len(alerts), 4)
        actions = re.findall(
            r"actions: (?:\[\{ actionGroupId: actionGroupId \}\]"
            r"|\{ actionGroups: \[actionGroupId\] \})",
            MODULE,
        )
        self.assertEqual(len(actions), len(alerts))


if __name__ == "__main__":
    unittest.main()
