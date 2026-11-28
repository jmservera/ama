"""Fail-closed reasons of the bounded-AI enablement and proposal-only gates (issue 104)."""

from __future__ import annotations

import copy
import unittest
from typing import Any

from zava_forward.core import ai_registry as _untyped_registry
from zava_forward.core import bounded_ai, rai_release

REGISTRY: Any = _untyped_registry
TASK = "briefing"
CHAT = "chat-case-conversation"


def entry_for(task_id: str = TASK, **changes: Any) -> dict[str, Any]:
    entry: dict[str, Any] = copy.deepcopy(dict(REGISTRY.get(task_id)))
    entry.update(
        enabled=True,
        approval_state="approved-2026-11-15",
        accountable_individual="Named Programme Director",
        delegation="Delegation Register DR-104",
        authority={role: f"Named Holder ({role})" for role in rai_release.AUTHORITY_ROLES},
    )
    entry.update(changes)
    return entry


def reasons(task_id: str = TASK, **kwargs: Any) -> list[str]:
    result = bounded_ai.verify_non_exercise_enablement(task_id, env={}, **kwargs)
    assert result["allowed"] is False
    return list(result["reasons"])


class EnablementReasons(unittest.TestCase):
    def test_unregistered_capability_is_the_only_reason(self) -> None:
        self.assertEqual(reasons("not-a-capability"), ["unregistered-capability"])

    def test_missing_release_and_ledger_always_block(self) -> None:
        found = reasons(task_entry=entry_for())
        self.assertIn("live-rai-release-missing", found)
        self.assertIn("consumption-ledger-missing", found)

    def test_registry_default_is_not_approved_for_live_use(self) -> None:
        self.assertIn("registry-approval-unapproved", reasons())

    def test_each_ownership_defect_has_its_own_reason(self) -> None:
        cases: dict[str, dict[str, Any]] = {
            "capability-disabled-in-registry": {"enabled": False},
            "accountable-individual-not-named-human": {
                "accountable_individual": "Copilot assistant"
            },
            "delegation-missing": {"delegation": ""},
            "registry-approval-unapproved": {"approval_state": None},
            "registry-authorities-missing": {"authority": {}},
            "registry-authority-holder-not-named-human": {
                "authority": {role: "Automation service" for role in rai_release.AUTHORITY_ROLES}
            },
        }
        for reason, change in cases.items():
            with self.subTest(reason=reason):
                self.assertIn(reason, reasons(task_entry=entry_for(**change)))

    def test_exercise_demo_activation_never_counts_as_enablement(self) -> None:
        rec = REGISTRY.get(CHAT)["demo_activation"]
        env = {
            REGISTRY.DEMO_SWITCH: rec["switch_value"],
            REGISTRY.DEMO_PROFILE: REGISTRY.DEMO_PROFILE_VALUE,
        }
        result = bounded_ai.verify_non_exercise_enablement(CHAT, env=env)
        self.assertFalse(result["allowed"])
        self.assertIn("demo-activation-is-exercise-only", result["reasons"])


class ProposalOnly(unittest.TestCase):
    def test_unregistered_capability_is_rejected(self) -> None:
        with self.assertRaises(bounded_ai.BoundedAiViolation):
            bounded_ai.enforce_proposal_only("not-a-capability", {})

    def test_controlled_status_is_rejected_in_any_case(self) -> None:
        for status in ("approved", "EXECUTED", "Submitted", "awarded", "closed", "Signed_Off"):
            with self.subTest(status=status), self.assertRaises(bounded_ai.BoundedAiViolation):
                bounded_ai.enforce_proposal_only(TASK, {"status": status})

    def test_approval_and_approved_flag_are_rejected(self) -> None:
        for payload in ({"approved": True}, {"approval": "approved"}, {"approval": 1}):
            with self.subTest(payload=payload), self.assertRaises(bounded_ai.BoundedAiViolation):
                bounded_ai.enforce_proposal_only(TASK, payload)

    def test_unapproved_states_and_plain_status_pass(self) -> None:
        for approval in (None, "Not reviewed", "pending", "pending_owner_review"):
            bounded_ai.enforce_proposal_only(TASK, {"approval": approval, "status": "draft"})


if __name__ == "__main__":
    unittest.main()
