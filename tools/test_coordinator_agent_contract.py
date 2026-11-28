"""Contract tests tying the coordinator prompt to tools/check-tick-log.py (Issue #1204).

Covers the criterion: every tick has a real next action and bounded closure-review
progress when capacity is free, and approvals are reconciled without treating one
blocked lane as a global stop.
"""

from __future__ import annotations

import importlib.util
import re
import sys
import unittest
from pathlib import Path
from types import ModuleType

TOOLS_DIR = Path(__file__).resolve().parent
AGENT_PATH = TOOLS_DIR.parent / ".github" / "agents" / "ama-backlog-delivery-coordinator.agent.md"


def _load_checker() -> ModuleType:
    spec = importlib.util.spec_from_file_location("check_tick_log", TOOLS_DIR / "check-tick-log.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = _load_checker()


def prompt_text() -> str:
    return re.sub(r"\s+", " ", AGENT_PATH.read_text(encoding="utf-8"))


def rules(rows: list[dict[str, object]]) -> list[str]:
    return [str(v.rule) for v in checker.check_ticks(rows)]


def tick(n: int, **overrides: object) -> dict[str, object]:
    row: dict[str, object] = {
        "tick": n,
        "counts": {"ready": 1, "running": 2, "unassessed": 4, "human_blocked": 1},
        "action": "reviewed closure batch",
        "evidence": "tools/backlog-sync.py queue read",
    }
    row.update(overrides)
    return row


class PromptContractTests(unittest.TestCase):
    def test_prompt_states_each_clause_of_the_criterion(self) -> None:
        text = prompt_text()
        for phrase in (
            "Each tick then advances at least one real next action when capacity allows",
            "up to five `unassessed` items",
            "On a new or expired approval, reclassify the affected tasks the same tick",
            "an expired one returns its tasks to `human-blocked` for that scope only",
            "An unavailable owner blocks only the lane that needs the answer",
            "never a success claim or a global stop",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_prompt_limits_match_the_checker_constants(self) -> None:
        text = prompt_text()
        self.assertEqual(checker.CLOSURE_BATCH_MAX, 5)
        self.assertEqual(checker.SESSION_CAP, 8)
        self.assertIn("eight (owner, 2026-10-31) is the maximum number of live", text)
        for field in ("closure_batch", "approvals_granted", "approvals_expired", "reclassified"):
            with self.subTest(field=field):
                self.assertIn(f"`{field}`", text)
                self.assertIn(field, checker.OPTIONAL_COLUMNS)


class LaneScenarioTests(unittest.TestCase):
    def test_human_blocked_lane_beside_ready_work_still_needs_an_action(self) -> None:
        self.assertEqual(rules([tick(1)]), [])
        idle = tick(2, action="", evidence="")
        self.assertEqual(rules([idle]), ["no-progress"])

    def test_blocked_lane_does_not_justify_a_global_stop(self) -> None:
        self.assertEqual(rules([tick(1, global_stop=True)]), ["global-stop"])
        done = tick(2, counts={"ready": 0, "unassessed": 0, "human_blocked": 3}, global_stop=True)
        self.assertEqual(rules([done]), [])

    def test_free_capacity_requires_closure_progress_then_bounds_the_batch(self) -> None:
        self.assertEqual(rules([tick(1, closure_batch=[])]), ["closure-progress"])
        self.assertEqual(rules([tick(1, closure_batch=["1", "2", "3", "4", "5"])]), [])
        self.assertEqual(
            rules([tick(1, closure_batch=["1", "2", "3", "4", "5", "6"])]), ["closure-batch"]
        )
        full = tick(1, counts={"ready": 0, "running": 8, "unassessed": 4}, closure_batch=[])
        self.assertEqual(rules([full]), [])

    def test_expiry_and_grant_reconcile_each_scope_independently(self) -> None:
        expired = [{"scope": "azure-cap", "tasks": ["A"]}]
        granted = [{"scope": "send-live", "tasks": ["B"]}]
        moves: list[dict[str, str]] = [
            {"task": "A", "to": "human-blocked", "scope": "azure-cap"},
            {"task": "B", "to": "ready", "scope": "send-live"},
        ]
        row = tick(1, approvals_expired=expired, approvals_granted=granted, reclassified=moves)
        self.assertEqual(rules([row]), [])
        unreconciled = tick(
            1, approvals_expired=expired, approvals_granted=granted, reclassified=moves[:1]
        )
        self.assertEqual(rules([unreconciled]), ["approval"])

    def test_task_outside_the_expired_scope_is_not_blocked(self) -> None:
        expired = [{"scope": "azure-cap", "tasks": ["A"]}]
        moves: list[dict[str, str]] = [
            {"task": "A", "to": "human-blocked", "scope": "azure-cap"},
            {"task": "C", "to": "human-blocked", "scope": "azure-cap"},
        ]
        self.assertEqual(
            rules([tick(1, approvals_expired=expired, reclassified=moves)]), ["approval"]
        )


if __name__ == "__main__":
    unittest.main()
