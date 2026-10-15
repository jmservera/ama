import unittest
from typing import Any

from zava_forward.core.chat_panel import ModelUnavailable

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
        model = ChatModel(worker(dict(outcome="returned", text="hello")))
        self.assertEqual(model("s", "p"), "hello")

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
                ChatModel(worker(result))("s", "p")
            self.assertNotIn("secret", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
