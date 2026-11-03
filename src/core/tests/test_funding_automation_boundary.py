"""Issue 93: RULE-010 / AC-035 boundary. No automated path submits a bid,
approves match funding, certifies a claim or records cash receipt.

Synthetic fixtures only. These probes prove the boundary in the delivered
core and callers; they do not prove a real delegation of authority.
"""

import ast
import copy
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from test_grant_lifecycle_controls import GrantFixture
from zava_forward.core.finance import FINANCE_ACTIONS
from zava_forward.core.grants import GRANT_ACTIONS, GRANT_FLOW, GRANT_STATES

SRC = Path(__file__).resolve().parents[2]
GATED_CALLS = {"grant_action", "finance_action", "funding_step", "_financial_authority"}
# The only caller allowed to reach the gated methods is the authenticated API route.
HUMAN_ROUTE = SRC / "api" / "src" / "zava_forward" / "api" / "server.py"
AUTOMATED_AREAS = (
    SRC / "agents" / "src",
    SRC / "orchestrator" / "src",
    SRC / "importer" / "src",
)
AUTOMATED_CORE = (
    "ai.py",
    "ai_consumption.py",
    "ai_prompts.py",
    "ai_registry.py",
    "ai_tasks.py",
    "assistants.py",
    "chat_case_answers.py",
    "chat_isolation.py",
    "chat_panel.py",
    "coordinator.py",
    "resident_assistant.py",
    "workflows.py",
)
NO_EGRESS_CORE = ("finance.py", "grants.py", "forms.py", "form_review.py", "signoffs.py")
EGRESS_MODULES = {
    "urllib.request",
    "http.client",
    "requests",
    "httpx",
    "smtplib",
    "socket",
    "aiohttp",
}
AUTOMATIC_TERMS = ("submit_bid", "match_fund", "certify", "record_cash", "cash_receipt")


def attribute_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return {
        node.attr if isinstance(node, ast.Attribute) else node.id
        for node in ast.walk(tree)
        if isinstance(node, (ast.Attribute, ast.Name))
    }


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            found.add(node.module)
    return found


class StaticBoundary(unittest.TestCase):
    def test_no_action_name_offers_automatic_bid_match_certify_or_cash(self) -> None:
        names = (*GRANT_ACTIONS, *FINANCE_ACTIONS)
        for name in names:
            with self.subTest(action=name):
                self.assertFalse(any(term in name for term in AUTOMATIC_TERMS))

    def test_agent_and_automation_code_never_reaches_gated_methods(self) -> None:
        paths = [path for area in AUTOMATED_AREAS if area.exists() for path in area.rglob("*.py")]
        core = SRC / "core" / "src" / "zava_forward" / "core"
        paths += [core / name for name in AUTOMATED_CORE]
        self.assertGreater(len(paths), len(AUTOMATED_CORE))
        for path in paths:
            with self.subTest(path=str(path.relative_to(SRC))):
                self.assertEqual(attribute_names(path) & GATED_CALLS, set())

    def test_api_reaches_gated_methods_only_in_the_human_route(self) -> None:
        for path in (SRC / "api" / "src").rglob("*.py"):
            reached = attribute_names(path) & (GATED_CALLS - {"_financial_authority"})
            with self.subTest(path=str(path.relative_to(SRC))):
                if path == HUMAN_ROUTE:
                    self.assertTrue(reached)
                else:
                    self.assertEqual(reached, set())
        text = HUMAN_ROUTE.read_text(encoding="utf-8")
        self.assertIn('"finance": "finance_action"', text)
        self.assertIn("s.funding_step(", text)

    def test_finance_grant_and_form_modules_have_no_outbound_client(self) -> None:
        core = SRC / "core" / "src" / "zava_forward" / "core"
        for name in NO_EGRESS_CORE:
            with self.subTest(module=name):
                self.assertEqual(imported_modules(core / name) & EGRESS_MODULES, set())


class BoundaryProbes(GrantFixture, unittest.TestCase):
    def denied(self, user: dict[str, Any], action: str, **body: Any) -> None:
        with self.assertRaises(PermissionError):
            self.grant(user, action, **body)

    def test_every_grant_state_needs_its_own_human_designation(self) -> None:
        self.grant(self.a, "grant_open", scheme="SYN-95", source="SYN")
        gid = "GR-1"
        state = "Not recorded"
        proposer, approver = self.a, self.b
        while GRANT_FLOW[state]:
            target = GRANT_FLOW[state][0]
            if state != "Not recorded":
                self.grant(
                    proposer, "grant_propose", id=gid, to=target, source="SYN " + target, amount=1
                )
            before = self.record()
            self.denied(self.plain, "grant_approve", id=gid)
            self.denied(proposer, "grant_approve", id=gid)
            narrowed = copy.deepcopy(approver)
            narrowed["financial_authority"]["permissions"] = [
                p
                for p in narrowed["financial_authority"]["permissions"]
                if p["action"] != "grant:" + target
            ]
            self.staff(narrowed)
            self.denied(narrowed, "grant_approve", id=gid)
            self.staff(approver)
            self.assertEqual(self.record(), before, target)
            self.grant(approver, "grant_approve", id=gid)
            self.assertEqual(self.record()["grants"][0]["state"], target)
            state = target
        self.assertEqual(state, "Cash received")
        self.assertEqual(
            [h["state"] for h in self.record()["grants"][0]["history"]],
            [s for s in GRANT_STATES if s not in ("Not recorded", "Rejected")],
        )

    def test_grant_actions_cannot_leave_the_record_only_ledger(self) -> None:
        self.opportunity()
        before = self.record()
        self.grant(self.a, "grant_propose", id="GR-1", to="Award", source="SYN award")
        self.grant(self.b, "grant_approve", id="GR-1")
        after = self.record()
        self.assertEqual(after["funding"], before["funding"])
        self.assertNotIn("finance", after)
        self.assertEqual(after["grants"][0]["history"][-1]["source_status"], "Supplied, unverified")

    def test_ai_funding_draft_cannot_approve_submit_or_confirm(self) -> None:
        self.opportunity()
        grants = self.record()["grants"]
        with patch("zava_forward.core.ai_tasks.run_text_task") as run:
            run.return_value = dict(
                text="SYN draft", source="offline", model="none", verified=False
            )
            result = self.store.funding_draft(self.a, "ZF-1")
        funding = self.record()["funding"]
        self.assertIn("nothing is submitted until a person approves", result["label"])
        self.assertNotIn(funding["status"], ("Approved", "Submitted", "Confirmed"))
        self.assertFalse(funding.get("history"))
        self.assertNotEqual(self.record().get("funding_ok"), True)
        self.assertEqual(self.record()["grants"], grants)

    def test_application_steps_refuse_without_designation_in_order(self) -> None:
        with self.store.lock:
            self.store._case("ZF-1")["funding"].update(status="Draft ready", draft="SYN")
            self.store.save()
        with patch.object(self.store, "checklist", return_value=[]):
            for action in ("approve", "submit", "confirm"):
                before = self.record()
                with self.assertRaises(PermissionError):
                    self.store.funding_step(self.plain, "ZF-1", action, "SYN")
                self.assertEqual(self.record(), before)
            with self.assertRaises(ValueError):
                self.store.funding_step(self.a, "ZF-1", "submit", "SYN skip")


if __name__ == "__main__":
    unittest.main()
