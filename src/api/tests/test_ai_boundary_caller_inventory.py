"""Inventory of callers of the Ai provider-boundary methods (Refs #116).

A new caller of Ai.run, Ai.look_at, Ai.evidence or Ai._chat fails here until it
is classified, so no route reaches the provider without being reviewed against
the task/field allowlists.
"""

from __future__ import annotations

import ast
import unittest
from collections import Counter
from pathlib import Path

SRC = Path(__file__).resolve().parents[2]
METHODS = {"run", "look_at", "evidence", "_chat"}

# (file, method) -> number of call sites
INVENTORY = {
    ("agents/src/zava_forward/agents/dispatch.py", "evidence"): 1,
    ("core/src/zava_forward/core/ai_tasks.py", "run"): 1,
    ("core/src/zava_forward/core/ai_tasks.py", "look_at"): 2,
    ("core/src/zava_forward/core/simulation_lane.py", "evidence"): 1,
    ("core/src/zava_forward/core/assistants.py", "evidence"): 1,
    ("core/src/zava_forward/core/store.py", "run"): 1,
    ("api/src/zava_forward/api/server.py", "evidence"): 2,
}
PRIVATE_CALLERS: set[str] = set()


def _receiver_is_ai(node: ast.expr) -> bool:
    name = node.attr if isinstance(node, ast.Attribute) else getattr(node, "id", "")
    return name == "ai" or name == "_ai"


def callers() -> Counter[tuple[str, str]]:
    found: Counter[tuple[str, str]] = Counter()
    for path in SRC.glob("*/src/**/*.py"):
        rel = path.relative_to(SRC).as_posix()
        if rel == "core/src/zava_forward/core/ai.py":
            continue
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in METHODS
                and _receiver_is_ai(node.func.value)
            ):
                found[(rel, node.func.attr)] += 1
    return found


class ProviderBoundaryCallerInventory(unittest.TestCase):
    def test_every_boundary_caller_is_classified(self) -> None:
        self.assertEqual(dict(callers()), INVENTORY)

    def test_private_chat_has_no_caller_outside_the_ai_module(self) -> None:
        files = {rel for (rel, method) in callers() if method == "_chat"}
        self.assertEqual(files, PRIVATE_CALLERS)


if __name__ == "__main__":
    unittest.main()
