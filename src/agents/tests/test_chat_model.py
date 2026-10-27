import unittest
from typing import Any

from zava_forward.core.chat_panel import ModelReply, ModelUnavailable

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
