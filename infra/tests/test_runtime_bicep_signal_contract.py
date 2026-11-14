"""Issue #146: Bicep alert queries match the signals the runtime emits (no naming drift, no PII fields)."""

import re
import unittest
from pathlib import Path

from zava_forward.core import ai_consumption
from zava_forward.orchestrator import digest_blob

REPO = Path(__file__).resolve().parents[2]
INFRA = REPO / "infra"
MAIN = (INFRA / "main.bicep").read_text(encoding="utf-8")
MODULE = (INFRA / "modules" / "operationalMonitoring.bicep").read_text(encoding="utf-8")
RUNBOOK = (INFRA / "monitoring-runbooks.md").read_text(encoding="utf-8")
AI_SOURCE = Path(ai_consumption.__file__).read_text(encoding="utf-8")
FORBIDDEN_FIELDS = re.compile(
    r"\b(patient|resident_?name|email|phone|address|reading|payload|prompt|completion|message|body|chat|utterance)\b",
    re.IGNORECASE,
)


def _queries(source: str) -> list[str]:
    return re.findall(r"query: '([^']*)'", source)


def _markers(query: str) -> set[str]:
    return set(re.findall(r'Log has "([A-Z_]+)"', query))


def _emitted_ai_reasons() -> set[str]:
    reasons = set(re.findall(r'held = "([a-z-]+)"', AI_SOURCE))
    reasons |= set(re.findall(r'held = "[a-z-]+" if \w+ else "([a-z-]+)"', AI_SOURCE))
    reasons |= set(re.findall(r'reason = "(liability-[a-z]+)"', AI_SOURCE))
    reasons |= set(re.findall(r'return "(budget-currency-[a-z]+)"', AI_SOURCE))
    return reasons


def _runbook_ai_reasons() -> set[str]:
    section = RUNBOOK.split("#### AI limit calls", 1)[1].split(
        "## Explicit Missing-Signal", 1
    )[0]
    return set(re.findall(r"`([a-z]+(?:-[a-z]+)+)`", section)) - {
        "ai-limit-calls",
        "ai-limit-tokens",
        "ai-limit-budget",
        "ai-limit-expiry",
    }


class RuntimeBicepSignalContractTests(unittest.TestCase):
    def test_ledger_digest_markers_match_orchestrator_constants(self) -> None:
        ledger = [q for q in _queries(MAIN) if "LEDGER_DIGEST" in q]
        self.assertEqual(len(ledger), 2)
        queried = set().union(*(_markers(q) for q in ledger))
        self.assertEqual(queried, {digest_blob.ALERT_MARKER, digest_blob.OK_MARKER})
        source = _digest_source()
        self.assertIn('out(f"{ALERT_MARKER} ', source)
        self.assertIn('out(f"{OK_MARKER} ', source)

    def test_ai_limit_marker_matches_core_emitter(self) -> None:
        queried = set().union(*(_markers(q) for q in _queries(MODULE)))
        self.assertEqual(queried, {"AI_LIMIT_BREACH"})
        self.assertIn('LOG.warning("AI_LIMIT_BREACH reason=%s route=%s"', AI_SOURCE)

    def test_runbook_ai_reason_codes_match_emitted_reasons(self) -> None:
        emitted = _emitted_ai_reasons()
        documented = _runbook_ai_reasons()
        self.assertIn("`budget-currency-*`", RUNBOOK)
        emitted = {r for r in emitted if not r.startswith("budget-currency-")}
        self.assertEqual(emitted - documented, set())
        self.assertEqual(documented - emitted, set())

    def test_ai_classes_cover_calls_tokens_budget_and_expiry(self) -> None:
        for reason in (
            "call-budget-limit",
            "token-budget-limit",
            "money-budget-limit",
            "authority-expired",
        ):
            self.assertIn(f'"{reason}"', AI_SOURCE)
            self.assertIn(f"`{reason}`", RUNBOOK)

    def test_job_failure_and_iot_queries_use_platform_signals_only(self) -> None:
        self.assertIn("metricName: 'Executions'", MODULE)
        self.assertIn("values: ['Failed']", MODULE)
        for metric in re.findall(r"metric: '([^']+)'", MODULE):
            self.assertRegex(metric, r"^d2c\.telemetry\.(ingress|egress)\.[A-Za-z]+$")
        poison = next(q for q in _queries(MODULE) if "StorageQueueLogs" in q)
        self.assertIn("agent-tasks-poison", MODULE)
        self.assertIn('OperationName == "PutMessage"', poison)

    def test_alert_queries_carry_no_pii_or_content_fields(self) -> None:
        queries = _queries(MAIN) + _queries(MODULE)
        self.assertTrue(queries)
        for query in queries:
            with self.subTest(query=query):
                self.assertIsNone(FORBIDDEN_FIELDS.search(query))
                self.assertNotIn("project ", query)


def _digest_source() -> str:
    return Path(digest_blob.__file__).read_text(encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
