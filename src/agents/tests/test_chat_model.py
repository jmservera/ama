import json
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import dataset
from zava_forward.core.chat_isolation import ChatIsolation
from zava_forward.core.chat_panel import ChatPanel, ModelReply, ModelUnavailable
from zava_forward.core.store import Store

from zava_forward.agents.chat import ChatModel
from zava_forward.agents.dispatch import AgentWorker


def worker(result: Any) -> AgentWorker:
    def provider(system: str, prompt: str, max_tokens: int, timeout: int) -> dict[str, Any]:
        if isinstance(result, Exception):
            raise result
        return result  # type: ignore[no-any-return]

    return AgentWorker(provider)


class ChatModelTests(unittest.TestCase):
    def test_returns_text_from_a_returned_envelope(self) -> None:
        model = ChatModel(worker(dict(outcome="returned", text="hello")), admission=lambda: None)
        self.assertEqual(model("s", "p"), ModelReply("hello"))

    def test_every_failure_is_model_unavailable_without_provider_text(self) -> None:
        for result in (
            RuntimeError("secret provider detail"),
            dict(outcome="timeout", text=None),
            dict(outcome="disabled", text=None),
            dict(outcome="returned", text="  "),
            dict(outcome="returned", text=5),
            "not an envelope",
        ):
            with self.assertRaises(ModelUnavailable) as caught:
                ChatModel(worker(result), admission=lambda: None)("s", "p")
            self.assertNotIn("secret", str(caught.exception))

    def test_denied_admission_makes_no_provider_call(self) -> None:
        def forbidden(*args: Any) -> dict[str, Any]:
            self.fail("provider called without admission")

        for admission in (None, lambda: "not approved"):
            with self.assertRaises(ModelUnavailable) as caught:
                ChatModel(AgentWorker(forbidden), admission=admission)("s", "p")
            self.assertEqual(caught.exception.calls, 0)

    def test_completion_revocation_preserves_usage_but_not_text(self) -> None:
        allowed = True
        usage = dict(prompt_tokens=5, completion_tokens=2, total_tokens=7)

        def provider(*args: Any) -> dict[str, Any]:
            nonlocal allowed
            allowed = False
            return dict(outcome="returned", text="PRIVATE-ANSWER", usage=usage)

        with self.assertRaises(ModelUnavailable) as caught:
            ChatModel(AgentWorker(provider), admission=lambda: None if allowed else "revoked")(
                "s", "p"
            )
        self.assertEqual((caught.exception.calls, caught.exception.usage), (1, usage))
        self.assertNotIn("PRIVATE", str(caught.exception))

    def test_callback_exceptions_preserve_only_actual_provider_consumption(self) -> None:
        usage = dict(prompt_tokens=5, completion_tokens=2, total_tokens=7)
        for completion, disabled in ((False, False), (True, False), (True, True)):
            with self.subTest(completion=completion, disabled=disabled):
                provider = Mock(
                    return_value=dict(
                        outcome="disabled" if disabled else "returned",
                        text="PRIVATE-ANSWER",
                        usage=None if disabled else usage,
                    )
                )
                admission = Mock(
                    side_effect=[None, RuntimeError("PRIVATE-CALLBACK")]
                    if completion
                    else RuntimeError("PRIVATE-CALLBACK")
                )
                with self.assertLogs("zava_forward.agents.chat", level="WARNING") as logs:
                    with self.assertRaises(ModelUnavailable) as caught:
                        ChatModel(AgentWorker(provider), admission=admission)("s", "p")
                self.assertEqual(provider.call_count, int(completion))
                self.assertEqual(caught.exception.calls, int(completion and not disabled))
                self.assertEqual(
                    caught.exception.usage, usage if completion and not disabled else None
                )
                self.assertEqual(
                    caught.exception.outcome,
                    "completion-check-failed" if completion else "admission-check-failed",
                )
                self.assertNotIn("PRIVATE", str(caught.exception))
                self.assertNotIn("PRIVATE", " ".join(logs.output))

    def test_callback_exception_receipts_match_provider_and_audit(self) -> None:
        usage = dict(prompt_tokens=5, completion_tokens=2, total_tokens=7)
        for completion in (False, True):
            with self.subTest(completion=completion), tempfile.TemporaryDirectory() as work:
                path = Path(work) / "synthetic.json"
                path.write_text(json.dumps(dataset.DATA))
                store = Store(str(path))
                user = store.data["staff"][0]
                iso = ChatIsolation(
                    store,
                    env=dict(
                        CHAT_DPIA_REF="SYN-DPIA",
                        CHAT_LAWFUL_BASIS_REF="SYN-BASIS",
                        CHAT_NOTICE_REF="SYN-NOTICE",
                    ),
                )
                provider = Mock(
                    return_value=dict(outcome="returned", text="PRIVATE-ANSWER", usage=usage)
                )
                admission = Mock(
                    side_effect=[None, RuntimeError("PRIVATE-CALLBACK")]
                    if completion
                    else RuntimeError("PRIVATE-CALLBACK")
                )
                panel = ChatPanel(iso, ChatModel(AgentWorker(provider), admission=admission))
                tid = store.chat_create_thread(user)["id"]
                with self.assertLogs("zava_forward.agents.chat", level="WARNING"):
                    answer = panel.ask(user, tid, "What help is available?", skill="general")
                receipt = answer["consumption"]
                self.assertEqual(answer["kind"], "fallback")
                self.assertNotIn("PRIVATE", json.dumps(answer))
                self.assertEqual(receipt["model_calls"], provider.call_count)
                self.assertEqual(receipt["tokens"], usage if completion else None)
                self.assertEqual(
                    receipt["provider_outcome"],
                    "completion-check-failed" if completion else "admission-check-failed",
                )
                turns = [r for r in store.audit_entries() if r["action"] == "chat.turn"]
                self.assertEqual(json.loads(turns[-1]["detail"]), receipt)

    def test_usage_is_per_invocation_and_rejects_malformed_values(self) -> None:
        for usage in (
            dict(prompt_tokens=5, completion_tokens=2, total_tokens=7),
            dict(prompt_tokens=True, completion_tokens=2, total_tokens=3),
            dict(prompt_tokens=-1, completion_tokens=2, total_tokens=1),
            dict(prompt_tokens=5, completion_tokens=2, total_tokens=8),
            None,
        ):
            model = ChatModel(
                worker(dict(outcome="returned", text="ok", usage=usage)), admission=lambda: None
            )
            result = model("s", "p")
            self.assertEqual(result.usage, usage if usage and usage["total_tokens"] == 7 else None)


if __name__ == "__main__":
    unittest.main()
