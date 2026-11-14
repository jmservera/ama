"""Issue #146: every AI limit and operational alert resolves to a runbook anchor naming an owner."""

import re
import unittest
from pathlib import Path

INFRA = Path(__file__).resolve().parents[1]
MODULE = (INFRA / "modules" / "operationalMonitoring.bicep").read_text(encoding="utf-8")
RUNBOOK = (INFRA / "monitoring-runbooks.md").read_text(encoding="utf-8")
LEDGER = INFRA.parents[0] / "src/core/src/zava_forward/core/ai_consumption.py"

OWNER_ROLES = ("owner", "Finance")


def _sections() -> dict[str, str]:
    parts = re.split(r"^#{2,4} .+$", RUNBOOK, flags=re.MULTILINE)
    heads = re.findall(r"^#{2,4} (.+)$", RUNBOOK, flags=re.MULTILINE)
    return {
        re.sub(r"[^a-z0-9 -]", "", h.lower()).strip().replace(" ", "-"): " ".join(
            body.split()
        )
        for h, body in zip(heads, parts[1:])
    }


class RunbookOwnershipTests(unittest.TestCase):
    def test_ai_limit_classes_have_owned_anchors_and_cover_ledger_reasons(self) -> None:
        sections = _sections()
        ledger = LEDGER.read_text(encoding="utf-8")
        classes = {
            "ai-limit-calls": ("call-budget-limit", "request-call-limit"),
            "ai-limit-tokens": ("token-budget-limit",),
            "ai-limit-budget": (
                "money-budget-limit",
                "liability-unknown",
                "price-unknown",
                "alert-unowned",
            ),
            "ai-limit-expiry": ("authority-expired", "authority-expiring"),
        }
        for anchor, reasons in classes.items():
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, sections)
                self.assertIn(f"Anchor: `{anchor}`", sections[anchor])
                self.assertIn("Accountable role:", sections[anchor])
                self.assertTrue(any(r in sections[anchor] for r in OWNER_ROLES))
                self.assertIn("appointment pending", sections[anchor])
                for reason in reasons:
                    self.assertIn(reason, sections[anchor])
                    self.assertIn(f'"{reason}"', ledger)

    def test_every_rule_runbook_link_resolves_to_owner_section(self) -> None:
        sections = _sections()
        linked = set(re.findall(r"\$\{runbookBase\}#([a-z-]+)", MODULE))
        linked |= {"job-orchestrator", "job-ledger", "job-import", "job-auth"}
        linked |= {
            "iot-ingress-throttle",
            "iot-routing-dropped",
            "iot-routing-invalid",
            "iot-routing-orphaned",
        }
        self.assertIn("ai-limits", linked)
        self.assertIn("agent-tasks-poison", linked)
        iot_owner = sections["new-disabled-iot-candidates"]
        for anchor in sorted(linked):
            with self.subTest(anchor=anchor):
                self.assertIn(anchor, sections)
                body = sections[anchor] + (
                    iot_owner if anchor.startswith("iot-") else ""
                )
                self.assertRegex(body, r"[Oo]wner")

    def test_ledger_digest_alerts_name_owner_and_anchor(self) -> None:
        sections = _sections()
        for anchor in ("ledger-digest-mismatch", "ledger-verify-missing"):
            with self.subTest(anchor=anchor):
                self.assertIn("Proposed owner: Digital service owner", sections[anchor])

    def test_no_invented_prices_or_signoffs(self) -> None:
        self.assertIn("OD-51", RUNBOOK)
        self.assertNotRegex(RUNBOOK, r"(?i)approved by [A-Z][a-z]+ [A-Z][a-z]+")


if __name__ == "__main__":
    unittest.main()
