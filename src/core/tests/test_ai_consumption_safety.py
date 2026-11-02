"""A stopped AI request leaves hazard response and statutory clocks untouched (#432, AC-109).

Constructed data only: no credentials, private data or paid calls.
"""

from __future__ import annotations

import ast
import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from dataset import DATA
from test_ai_consumption import CONFIG, END, MODEL, START, Port
from zava_forward.core import hazard, taskqueues, workflows
from zava_forward.core.ai_consumption import CallContext, Consumption, DispatchHeld, reference
from zava_forward.core.store import Store as UntypedStore

SOURCE = dict(source="SYN-SOURCE-CANARY", aware_at="2026-01-01T10:00:00+01:00")
Store: Any = UntypedStore
AI_MODULES = {"ai", "ai_consumption", "ai_prompts", "ai_tasks", "assistants", "chat_panel"}


def imported_core_modules(module: Any) -> set[str]:
    tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            names.add((node.module or "").split(".")[0])
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.Import):
            names.update(alias.name.split(".")[-1] for alias in node.names)
    return names


class StoppedRequestKeepsSafetyPath(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.port = Port(root / "ledger.sqlite")
        self.ledger = Consumption(self.port)
        price = self.ledger.price(
            source="https://prices.azure.com/api/retail/prices",
            source_hash=reference("constructed-price-response"),
            retrieved=START,
            version="constructed-v1",
            model=MODEL,
            currency="USD",
            start=START,
            end=END,
            input_rate="1",
            output_rate="2",
            cached_rate="0.5",
            synthetic=True,
        )
        self.ledger.authorize(
            authority="constructed-authority",
            owner="constructed-finance-owner",
            evidence="constructed-no-paid-spend",
            price=price,
            capability="assessment",
            configuration=CONFIG,
            start=START,
            end=END,
            max_calls=1,
            max_depth=1,
            budgets=[dict(id=reference("period"), calls=100, tokens=100000, amount="100")],
        )
        data = copy.deepcopy(DATA)
        path = root / "synthetic.json"
        path.write_text(json.dumps(data))
        self.staff = data["staff"][0]
        self.store: Any = Store(str(path))

    def context(self, attempt: str) -> CallContext:
        return CallContext(
            root=reference("loop"),
            attempt=reference(attempt),
            capability="assessment",
            case_type="retrofit-case",
            configuration=CONFIG,
            prompt=reference("template-v1"),
        )

    def test_safety_and_clock_code_never_depends_on_a_model_call(self) -> None:
        for module in (hazard, workflows, taskqueues):
            with self.subTest(module=module.__name__):
                self.assertFalse(AI_MODULES & imported_core_modules(module))

    def test_looping_request_stops_while_hazard_recording_and_clocks_continue(self) -> None:
        rid = self.ledger.reserve(self.context("first"), MODEL, 1000, 100)
        self.ledger.complete(
            rid, dict(prompt_tokens=10, completion_tokens=5, total_tokens=15), MODEL, "returned"
        )
        with self.assertRaisesRegex(DispatchHeld, "request-call-limit"):
            self.ledger.reserve(self.context("loop"), MODEL, 1000, 100)
        with self.port.transaction() as db:
            alert = [r for r in self.ledger._read(db) if r["kind"] == "alert"][-1]
        self.assertEqual(alert["route"], "workflow-only")

        index = self.store.raise_hazard(
            self.staff, "ZF-3", "Damp and mould", "Emergency", "SYN-NOTE", SOURCE
        )
        raised = self.store.detail("ZF-3")["hazards"][index]
        self.assertEqual(raised["state"], "Raised")
        self.assertEqual(raised["priority"], "Emergency")
        self.assertEqual(raised["aware_at"], "2026-01-01T09:00+00:00")
        self.assertEqual(raised["hold"]["status"], "Active")


if __name__ == "__main__":
    unittest.main()
