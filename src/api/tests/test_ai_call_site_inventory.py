"""Inventory of model-provider call sites and their metering join status (#432).

A new chat-completions call site fails here until it is classified, so the
claim that each model call is joined cannot drift from the source.
"""

from __future__ import annotations

import ast
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from zava_forward.core import ai as ai_module
from zava_forward.core import ai_consumption

SRC = Path(__file__).resolve().parents[2]
URL_FRAGMENTS = ("chat/completions", "/openai/deployments", "/responses?api-version")
SDK_MODULES = ("openai", "azure.ai.inference", "azure.ai.projects", "azure.ai.openai")
SDK_NAMES = {"AzureOpenAI", "OpenAI", "AsyncAzureOpenAI", "AsyncOpenAI", "ChatCompletionsClient"}

# file -> (join status, what it records). "ledger" means the call is admitted,
# priced and completed in the core consumption ledger with its call context.
INVENTORY = {
    "core/src/zava_forward/core/ai.py": ("ledger", "admission, call context, counts, outcome"),
    "api/src/zava_forward/api/resident_demo/aoai.py": (
        "own-accounting",
        "reserved and closed token accounting for the resident demo; not the ledger",
    ),
    "api/src/zava_forward/api/resident_demo/assistant.py": (
        "counts-only-sink",
        "optional validated counts; no ledger, price or context; adapter disabled by default",
    ),
}


def _is_sdk(module: str) -> bool:
    return any(module == m or module.startswith(m + ".") for m in SDK_MODULES)


def _file_is_call_site(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if any(fragment in node.value for fragment in URL_FRAGMENTS):
                return True
        elif isinstance(node, ast.Import):
            if any(_is_sdk(alias.name) for alias in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            if _is_sdk(node.module or "") or any(alias.name in SDK_NAMES for alias in node.names):
                return True
        elif isinstance(node, ast.Name) and node.id in SDK_NAMES:
            return True
    return False


def call_sites() -> set[str]:
    found = set()
    for path in SRC.glob("*/src/**/*.py"):
        if _file_is_call_site(ast.parse(path.read_text(encoding="utf-8"))):
            found.add(path.relative_to(SRC).as_posix())
    return found


def _chat_call_enclosing_function(path: Path) -> ast.FunctionDef:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for fn in ast.walk(tree):
        if isinstance(fn, ast.FunctionDef):
            for node in ast.walk(fn):
                if (
                    isinstance(node, ast.Constant)
                    and isinstance(node.value, str)
                    and "chat/completions" in node.value
                ):
                    return fn
                if isinstance(node, ast.JoinedStr) and "chat/completions" in ast.unparse(node):
                    return fn
    raise AssertionError("no chat/completions call site found")


class AiCallSiteInventoryTest(unittest.TestCase):
    def test_every_provider_call_site_is_classified(self) -> None:
        self.assertEqual(call_sites(), set(INVENTORY))

    def test_ledger_status_follows_the_admission_calls_in_source(self) -> None:
        for path, (status, _) in INVENTORY.items():
            tree = ast.parse((SRC / path).read_text(encoding="utf-8"))
            admits = any(
                isinstance(n, ast.Call)
                and "consumption." in ast.unparse(n.func)
                and ast.unparse(n.func).rsplit(".", 1)[1] in {"reserve", "dispatch_check"}
                for n in ast.walk(tree)
            )
            self.assertEqual(admits, status == "ledger", path)

    def test_ledger_call_is_inside_the_admission_and_completion_path(self) -> None:
        fn = _chat_call_enclosing_function(SRC / "core/src/zava_forward/core/ai.py")
        first_line: dict[str, int] = {}
        for n in ast.walk(fn):
            if isinstance(n, ast.Call):
                first_line[ast.unparse(n.func)] = min(
                    n.lineno, first_line.get(ast.unparse(n.func), n.lineno)
                )
        names = (
            "self.consumption.reserve",
            "self.consumption.dispatch_check",
            "urllib.request.urlopen",
            "self.consumption.complete",
        )
        for name in names:
            self.assertIn(name, first_line)
        lines = [first_line[name] for name in names]
        self.assertEqual(lines, sorted(lines))


class FakeLedger:
    def __init__(self, hold: bool = False) -> None:
        self.events: list[tuple[object, ...]] = []
        self.hold = hold

    def reserve(self, context: object, model: str, bound: int, max_tokens: int, live: bool) -> str:
        self.events.append(("reserve", context, model))
        return "rid-1"

    def dispatch_check(self, rid: str) -> None:
        if self.hold:
            raise ai_consumption.DispatchHeld("held")
        self.events.append(("dispatch", rid))

    def complete(self, rid: str, usage: object, model: object, outcome: str) -> None:
        self.events.append(("complete", rid, usage, outcome))


class LedgerJoinBehaviourTest(unittest.TestCase):
    def _ai(self, ledger: FakeLedger | None) -> ai_module.Ai:
        with patch.dict("os.environ", {"AI_ENDPOINT": "http://127.0.0.1:1"}):
            ai = ai_module.Ai()
        ai.consumption = ledger
        ai.token = "t"
        ai.expires = 1e12
        return ai

    def _call(self, ai: ai_module.Ai, receipt: dict[str, object]) -> dict[str, object]:
        result: dict[str, object] = ai._request("standard", "sys", "user", 10, 1, 0, receipt)
        return result

    def test_join_fields_are_recorded_and_call_is_completed(self) -> None:
        ledger = FakeLedger()
        body = json.dumps(
            {"model": "unattested", "usage": {"prompt_tokens": 1, "completion_tokens": 2}}
        ).encode()
        receipt: dict[str, object] = {}
        with patch("urllib.request.urlopen", return_value=io.BytesIO(body)) as opened:
            self._call(self._ai(ledger), receipt)
        self.assertIn("chat/completions", opened.call_args.args[0].full_url)
        for key in ("meter_id", "meter_root", "configuration", "prompt_hash"):
            self.assertTrue(receipt[key], key)
        self.assertEqual([e[0] for e in ledger.events], ["reserve", "dispatch", "complete"])
        self.assertEqual(ledger.events[-1][3], "returned")

    def test_call_fails_closed_without_a_ledger(self) -> None:
        with patch("urllib.request.urlopen") as opened:
            with self.assertRaises(ai_consumption.DispatchHeld):
                self._call(self._ai(None), {})
        opened.assert_not_called()

    def test_held_dispatch_sends_nothing_and_closes_the_reservation(self) -> None:
        ledger = FakeLedger(hold=True)
        with patch("urllib.request.urlopen") as opened:
            with self.assertRaises(ai_consumption.DispatchHeld):
                self._call(self._ai(ledger), {})
        opened.assert_not_called()
        self.assertEqual(ledger.events[-1][0], "complete")
        self.assertEqual(ledger.events[-1][3], "provider-unavailable")


if __name__ == "__main__":
    unittest.main()
