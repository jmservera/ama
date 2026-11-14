"""Issue #146 criteria 1, 3 and 5: Bicep alert classes each name an owner and a valid runbook anchor."""

import re
import unittest
from pathlib import Path

INFRA = Path(__file__).resolve().parents[1]
MAIN = (INFRA / "main.bicep").read_text(encoding="utf-8")
MODULE = (INFRA / "modules" / "operationalMonitoring.bicep").read_text(encoding="utf-8")
RUNBOOK = (INFRA / "monitoring-runbooks.md").read_text(encoding="utf-8")
LINK = re.compile(r"monitoring-runbooks\.md#|\$\{runbookBase\}#")


def _anchors() -> dict[str, str]:
    heads = re.findall(r"^#{2,4} (.+)$", RUNBOOK, flags=re.MULTILINE)
    bodies = re.split(r"^#{2,4} .+$", RUNBOOK, flags=re.MULTILINE)[1:]
    return {
        re.sub(r"[^a-z0-9 -]", "", h.lower()).strip().replace(" ", "-"): " ".join(
            b.split()
        )
        for h, b in zip(heads, bodies)
    }


def _resource(source: str, symbol: str) -> str:
    match = re.search(
        rf"^resource {symbol} .*?^}}", source, flags=re.MULTILINE | re.DOTALL
    )
    assert match, symbol
    return match.group(0)


def _description(block: str) -> str:
    match = re.search(r"description: '(.*)'", block)
    assert match
    return match.group(1)


class AlertCoverageTests(unittest.TestCase):
    def test_required_alert_classes_exist_in_bicep(self) -> None:
        self.assertIn("'Microsoft.App/jobs'", MODULE)
        self.assertIn("name: 'alert-${jobName}-failed'", MODULE)
        self.assertIn("alert-${prefix}-agent-tasks-poison", MODULE)
        self.assertIn("LEDGER_DIGEST_ALERT", MAIN)
        self.assertIn("LEDGER_DIGEST_OK", MAIN)
        self.assertIn("'Microsoft.Devices/IotHubs'", MODULE)
        self.assertIn("module iotHub 'modules/iothub.bicep'", MAIN)
        self.assertIn("AI_LIMIT_BREACH", MODULE)

    def test_rules_name_owner_and_link_valid_runbook_anchor(self) -> None:
        anchors = _anchors()
        rules = [
            (MAIN, "ledgerDigestMismatch", "ledger-digest-mismatch"),
            (MAIN, "ledgerVerifyMissing", "ledger-verify-missing"),
            (MODULE, "agentTasksPoison", "agent-tasks-poison"),
            (MODULE, "aiLimitBreach", "ai-limits"),
        ]
        for source, symbol, anchor in rules:
            with self.subTest(rule=symbol):
                text = _description(_resource(source, symbol))
                self.assertRegex(text, r"(?i)owner")
                self.assertIn("appointment pending", text)
                self.assertRegex(text, rf"{LINK.pattern}{anchor}\b")
                self.assertIn(anchor, anchors)
                self.assertIn("owner", anchors[anchor].lower())

    def test_job_and_iot_rules_resolve_to_owned_anchors(self) -> None:
        anchors = _anchors()
        for symbol in ("jobFailures", "iotFailureAlerts"):
            text = _description(_resource(MODULE, symbol))
            self.assertIn("proposed owner: Digital service owner", text)
        for anchor in (
            "job-orchestrator",
            "job-ledger",
            "job-import",
            "job-auth",
            "iot-ingress-throttle",
            "iot-routing-dropped",
            "iot-routing-invalid",
            "iot-routing-orphaned",
        ):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, anchors)
                self.assertIn(anchor, MODULE)
                self.assertRegex(
                    anchors[anchor] + anchors["new-disabled-iot-candidates"],
                    r"[Oo]wner",
                )
        self.assertIn("#${failure.suffix}", MODULE)

    def test_ai_limit_classes_link_owned_anchors(self) -> None:
        anchors = _anchors()
        text = _description(_resource(MODULE, "aiLimitBreach"))
        for anchor in ("calls", "tokens", "budget", "expiry"):
            name = f"ai-limit-{anchor}"
            with self.subTest(anchor=name):
                self.assertIn(f"${{runbookBase}}#{name}", text)
                self.assertIn(f"Anchor: `{name}`", anchors[name])
                self.assertIn("Accountable role:", anchors[name])
                self.assertIn("appointment pending", anchors[name])

    def test_candidates_stay_disabled_by_default(self) -> None:
        for symbol in (
            "jobFailures",
            "iotFailureAlerts",
            "agentTasksPoison",
            "aiLimitBreach",
        ):
            self.assertIn("candidateAlertsEnabled", _resource(MODULE, symbol))
        for gate in (
            "enableCandidateAlerts",
            "enablePoisonQueueAlerts",
            "enableAiLimitAlerts",
        ):
            self.assertRegex(MODULE, rf"param {gate} bool = false")


if __name__ == "__main__":
    unittest.main()
