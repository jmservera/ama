"""Model adapter for the conversation panel: the agents side of issue #159.

The panel (core `chat_panel`) calls an injected `(system, prompt) -> ModelReply`
function. This adapter turns the bounded `AgentWorker.provider_call` envelope
into that function without dropping per-call usage. Admission is server owned
and denied by default. It has no database, blob or Key Vault access (ADR 0001),
never raises provider text, and signals every failure with `ModelUnavailable`
so the panel can fall back to workflow-only handling.
"""

from __future__ import annotations

import logging
from collections.abc import Callable

from zava_forward.core.chat_panel import ModelReply, ModelUnavailable, valid_usage

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
        admission: Callable[[], str | None] | None = None,
    ) -> None:
        self.worker = worker
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.admission = admission

    def __call__(self, system: str, prompt: str) -> ModelReply:
        if self.admission is None:
            raise ModelUnavailable("activation-not-approved")
        try:
            denied = self.admission()
        except Exception as error:
            logging.getLogger(__name__).warning(
                "Employee chat admission check failed (%s)", type(error).__name__
            )
            raise ModelUnavailable("admission-check-failed") from None
        if denied:
            raise ModelUnavailable("activation-not-approved")
        envelope = self.worker.provider_call(system, prompt, self.max_tokens, self.timeout)
        usage = valid_usage(envelope.get("usage"))
        calls = 0 if envelope.get("outcome") == "disabled" else 1
        try:
            denied = self.admission()
        except Exception as error:
            logging.getLogger(__name__).warning(
                "Employee chat completion check failed (%s)", type(error).__name__
            )
            raise ModelUnavailable("completion-check-failed", calls=calls, usage=usage) from None
        if denied:
            raise ModelUnavailable("activation-revoked", calls=calls, usage=usage)
        text = envelope.get("text")
        if envelope.get("outcome") != "returned" or not isinstance(text, str) or not text.strip():
            outcome = envelope.get("outcome")
            safe = outcome if outcome in ("timeout", "disabled") else "provider-unavailable"
            raise ModelUnavailable(safe, calls=calls, usage=usage)
        return ModelReply(text, usage, calls)


__all__ = ["ChatModel"]
