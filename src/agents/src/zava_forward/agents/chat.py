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
from typing import Any

from zava_forward.core.ai import count_dispatches
from zava_forward.core.chat_panel import ModelReply, ModelUnavailable, valid_usage

from zava_forward.agents.dispatch import AgentWorker

CHAT_MAX_TOKENS = 600
CHAT_TIMEOUT = 20


def unavailable(
    outcome: str,
    envelope: dict[str, Any] | None = None,
    *,
    calls: int = 0,
    usage: dict[str, int] | None = None,
) -> ModelUnavailable:
    """Build the failure with the meter reference so the panel can settle it as ineligible."""
    error = ModelUnavailable(outcome, calls=calls, usage=usage)
    values = envelope or {}
    for name in ("meter_id", "meter_root"):
        value = values.get(name)
        setattr(error, name, value if isinstance(value, str) else None)
    return error


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
            raise unavailable("activation-not-approved")
        try:
            denied = self.admission()
        except Exception as error:
            logging.getLogger(__name__).warning(
                "Employee chat admission check failed (%s)", type(error).__name__
            )
            raise unavailable("admission-check-failed") from None
        if denied:
            raise unavailable("activation-not-approved")
        with count_dispatches() as witness:
            envelope = self.worker.provider_call(system, prompt, self.max_tokens, self.timeout)
        usage = valid_usage(envelope.get("usage"))
        calls = witness.attempts
        if not witness.witnessed:
            # The provider is not core `Ai.evidence` here, so no trusted dispatch record exists.
            logging.getLogger(__name__).warning(
                "Employee chat provider dispatch count is unverified; assuming one call"
            )
            calls = 1
        try:
            denied = self.admission()
        except Exception as error:
            logging.getLogger(__name__).warning(
                "Employee chat completion check failed (%s)", type(error).__name__
            )
            raise unavailable(
                "completion-check-failed", envelope, calls=calls, usage=usage
            ) from None
        if denied:
            raise unavailable("activation-revoked", envelope, calls=calls, usage=usage)
        text = envelope.get("text")
        if envelope.get("outcome") != "returned" or not isinstance(text, str) or not text.strip():
            outcome = envelope.get("outcome")
            safe = outcome if outcome in ("timeout", "disabled") else "provider-unavailable"
            raise unavailable(safe, envelope, calls=calls, usage=usage)
        return ModelReply(
            text,
            usage,
            calls,
            meter_id=envelope.get("meter_id"),
            meter_root=envelope.get("meter_root"),
        )


__all__ = ["ChatModel"]
