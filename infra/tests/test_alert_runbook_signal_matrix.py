"""Issue #146: every declared alert signal maps to a runbook section with an accountable owner."""

import re
import unittest
from pathlib import Path

INFRA = Path(__file__).resolve().parents[1]
RUNBOOK = (INFRA / "monitoring-runbooks.md").read_text(encoding="utf-8")
MAIN = (INFRA / "main.bicep").read_text(encoding="utf-8")

ALERT_TYPES = (
    "Microsoft.Insights/metricAlerts",
    "Microsoft.Insights/scheduledQueryRules",
    "Microsoft.Insights/activityLogAlerts",
)
BUDGET_TYPE = "Microsoft.Consumption/budgets"
NOTIFICATIONS = ("actual80", "forecast100")

# Declared alert name template -> runbook anchor (heading slug) and criterion.
MATRIX = {
    "alert-${prefix}-foundry-throttle": "foundry-client-errors",
    "alert-${prefix}-sql-cpu": "sql-cpu",
    "alert-${applicationPrefix}-api-5xx": "api-errors",
    "alert-${applicationPrefix}-api-restarts": "api-restarts",
    "alert-${applicationPrefix}-ledger-digest-mismatch": "ledger-digest-mismatch",
    "alert-${applicationPrefix}-ledger-verify-missing": "ledger-verify-missing",
    "alert-${name}-secret-expiry": "vault-expiry",
    "alert-${name}-denied-access": "vault-denied",
    "alert-${jobName}-failed": "job-orchestrator|job-ledger|job-import|job-auth",
    "alert-${prefix}-${failure.suffix}": (
        "iot-ingress-throttle|iot-routing-dropped|iot-routing-invalid|iot-routing-orphaned"
    ),
    "alert-${prefix}-agent-tasks-poison": "agent-tasks-poison",
    "alert-${prefix}-ai-limits": "ai-limits",
}
BUDGET_ANCHORS = {
    ("budget-${prefix}", "actual80"): "budget-actual80",
    ("budget-${prefix}", "forecast100"): "budget-forecast100",
    ("budget-${name}", "actual80"): "iot-budget-actual80",
    ("budget-${name}", "forecast100"): "iot-budget-forecast100",
}
AI_LIMIT_ANCHORS = (
    "ai-limit-calls",
    "ai-limit-tokens",
    "ai-limit-budget",
    "ai-limit-expiry",
)
OWNER_PATTERN = r"(?:[Pp]roposed owner|Accountable role):? ?[^.]*?(?:owner|Finance)"


def _slug(heading: str) -> str:
    return re.sub(r"[^a-z0-9 -]", "", heading.lower()).strip().replace(" ", "-")


def _sections() -> dict[str, tuple[int, str]]:
    heads = list(re.finditer(r"^(#{2,4}) (.+)$", RUNBOOK, flags=re.MULTILINE))
    out: dict[str, tuple[int, str]] = {}
    for i, match in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(RUNBOOK)
        out[_slug(match.group(2))] = (
            len(match.group(1)),
            " ".join(RUNBOOK[match.end() : end].split()),
        )
    return out


def _declared() -> tuple[set[str], set[tuple[str, str]]]:
    alerts: set[str] = set()
    budgets: set[tuple[str, str]] = set()
    for path in sorted(INFRA.rglob("*.bicep")):
        text = path.read_text(encoding="utf-8")
        for kind, name in re.findall(
            r"^resource \w+ '([^'@]+)@[^']+'[^{]*\{\s*name: '([^']+)'",
            text,
            flags=re.MULTILINE,
        ):
            if kind in ALERT_TYPES:
                alerts.add(name)
            elif kind == BUDGET_TYPE:
                block = text[text.index(name) :]
                for note in NOTIFICATIONS:
                    if re.search(rf"\b{note}:\s*\{{", block):
                        budgets.add((name, note))
    return alerts, budgets


def _owned_body(anchor: str, sections: dict[str, tuple[int, str]]) -> str:
    """Section body plus any child subsections and a shared parent owner statement."""
    level, body = sections[anchor]
    keys = list(sections)
    for key in keys[keys.index(anchor) + 1 :]:
        if sections[key][0] <= level:
            break
        body += " " + sections[key][1]
    parent = next(
        (k for k in reversed(keys[: keys.index(anchor)]) if sections[k][0] < level),
        None,
    )
    return body + (" " + sections[parent][1] if parent else "")


class AlertRunbookSignalMatrixTests(unittest.TestCase):
    def test_every_declared_alert_is_in_the_matrix(self) -> None:
        alerts, budgets = _declared()
        self.assertEqual(set(MATRIX), alerts)
        self.assertEqual(set(BUDGET_ANCHORS), budgets)

    def test_every_signal_maps_to_runbook_section_with_owner(self) -> None:
        sections = _sections()
        anchors = {a for value in MATRIX.values() for a in value.split("|")}
        anchors |= set(BUDGET_ANCHORS.values()) | set(AI_LIMIT_ANCHORS)
        for anchor in sorted(anchors):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, sections)
                self.assertRegex(_owned_body(anchor, sections), OWNER_PATTERN)

    def test_matrix_names_and_runbook_agree_on_alert_source(self) -> None:
        for name, anchor in MATRIX.items():
            if anchor.startswith(("job-", "iot-")):
                continue
            with self.subTest(alert=name):
                self.assertIn(name.replace("${name}", "${vaultName}"), RUNBOOK)

    def test_rule_descriptions_link_runbook_and_owner(self) -> None:
        module = (INFRA / "modules/operationalMonitoring.bicep").read_text(
            encoding="utf-8"
        )
        sections = _sections()
        descriptions = re.findall(r"description: '([^\n]*Runbook:[^\n]*)'", module)
        self.assertEqual(len(descriptions), 4)
        for text in descriptions:
            with self.subTest(description=text[:60]):
                self.assertIn("proposed owner:", text)
                self.assertIn("${runbookBase}#", text)
        for anchor in re.findall(r"\$\{runbookBase\}#([a-z-]+)", module):
            self.assertIn(anchor, sections)

    def test_ai_limit_breach_covers_calls_tokens_budget_expiry(self) -> None:
        sections = _sections()
        self.assertIn("ai-limits", sections)
        summary = _owned_body("ai-limits", sections)
        for anchor in AI_LIMIT_ANCHORS:
            self.assertIn(anchor, sections)
            self.assertIn(f"Anchor: `{anchor}`", sections[anchor][1])
            self.assertIn("appointment pending", sections[anchor][1])
        self.assertRegex(summary, r"[Pp]roposed owner")

    def test_poison_ledger_job_and_iot_signals_are_covered(self) -> None:
        sections = _sections()
        for anchor in (
            "agent-tasks-poison",
            "import-jobs-poison",
            "ledger-digest-mismatch",
            "ledger-verify-missing",
            "job-orchestrator",
            "job-ledger",
            "job-import",
            "job-auth",
            "iot-routing-dropped",
        ):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, sections)
                self.assertRegex(_owned_body(anchor, sections), OWNER_PATTERN)

    def test_main_wires_operational_monitoring_with_action_group(self) -> None:
        self.assertIn("module operationalMonitoring", MAIN)
        self.assertIn("actionGroupId: monitoring.outputs.actionGroupId", MAIN)
        self.assertIn("enableAiLimitAlerts: enableAiLimitAlertCandidate", MAIN)
        self.assertIn("enablePoisonQueueAlerts: enablePoisonQueueAlertCandidate", MAIN)


if __name__ == "__main__":
    unittest.main()
