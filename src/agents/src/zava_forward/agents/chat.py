"""Model adapter for the conversation panel: the agents side of issue #159.

The panel (core `chat_panel`) calls an injected `(system, prompt) -> text`
function. This adapter turns the bounded `AgentWorker.provider_call` envelope
into that function. It has no database, blob or Key Vault access (ADR 0001),
never raises provider text, and signals every failure with `ModelUnavailable`
so the panel can fall back to workflow-only handling.
"""

from __future__ import annotations

from zava_forward.core.chat_panel import ModelUnavailable

from zava_forward.agents.dispatch import AgentWorker

CHAT_MAX_TOKENS = 600
CHAT_TIMEOUT = 20


class ChatModel:
    name = "azure-openai"

    def __init__(
        self,
        worker: AgentWorker,
        max_tokens: int = CHAT_MAX_TOKENS,
        timeout: int = CHAT_TIMEOUT,
    ) -> None:
        self.worker = worker
        self.max_tokens = max_tokens
        self.timeout = timeout

    def __call__(self, system: str, prompt: str) -> str:
        envelope = self.worker.provider_call(system, prompt, self.max_tokens, self.timeout)
        text = envelope.get("text")
        if envelope.get("outcome") != "returned" or not isinstance(text, str) or not text.strip():
            raise ModelUnavailable(str(envelope.get("outcome") or "unavailable"))
        return text


__all__ = ["ChatModel"]
