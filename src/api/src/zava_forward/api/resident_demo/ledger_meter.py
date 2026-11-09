"""Joins the optional resident topic adapter to the core consumption ledger (#432).

The ledger admits, prices and closes each call with its capability, case type,
configuration, prompt version, counts, outcome and alert owner. Nothing here
holds raw resident text, supplies a price or authority, or enables the adapter.
A held or unavailable meter refuses the call, so the resident keeps the
workflow-only path.
"""

from __future__ import annotations

import threading
import uuid
from collections.abc import Callable

from zava_forward.core import ai_consumption
from zava_forward.core.ai_consumption import CallContext, Consumption, DispatchHeld

from .assistant import RequestEnvelope

CAPABILITY = "resident-topic"
CASE_TYPE = "resident-chat"
# Chat framing adds tokens beyond the ASCII prompt bytes; an overrun is held, not hidden.
FRAMING_TOKENS = 32


class LedgerTopicMeter:
    def __init__(
        self,
        consumption: Consumption,
        *,
        model: str,
        configuration: str,
        prompt: str,
        capability: str = CAPABILITY,
        case_type: str = CASE_TYPE,
        new_id: Callable[[], str] = lambda: uuid.uuid4().hex,
    ) -> None:
        self.consumption, self.model = consumption, model
        self.configuration, self.prompt, self.new_id = configuration, prompt, new_id
        self.capability, self.case_type = capability, case_type
        self._open = threading.local()

    def reserve(self, envelope: RequestEnvelope) -> bool:
        self._open.rid = None
        root = ai_consumption.reference(self.new_id())
        context = CallContext(
            root,
            ai_consumption.reference(self.new_id()),
            self.capability,
            self.case_type,
            self.configuration,
            self.prompt,
        )
        bound = len(envelope.prompt.encode("ascii")) + FRAMING_TOKENS
        try:
            self._open.rid = self.consumption.reserve(
                context, self.model, bound, envelope.max_output_tokens, live=True
            )
        except DispatchHeld:
            return False
        return True

    def token(self, acquire: Callable[[], str]) -> Callable[[], str]:
        """Wrap credential acquisition so expiry is rechecked just before the network."""

        def guarded() -> str:
            value = acquire()
            rid = getattr(self._open, "rid", None)
            if rid is None:
                raise ValueError("No admitted reservation.")
            try:
                self.consumption.dispatch_check(rid)
            except DispatchHeld as held:
                self._open.rid = None
                raise ValueError("Dispatch held.") from held
            return value

        return guarded

    def close(self, outcome: str, counts: dict[str, int | None] | None, model: object) -> None:
        rid = getattr(self._open, "rid", None)
        if rid is None:
            return
        self._open.rid = None
        self.consumption.complete(rid, counts, model, outcome)


ADVISOR_CAPABILITIES = {"guidance": "resident-guidance", "question": "resident-question"}


def advisor_meters(
    consumption: Consumption, *, model: str, configuration: str, prompts: dict[str, str]
) -> dict[str, LedgerTopicMeter]:
    """One meter per advisor request kind; each needs its own prompt version reference."""
    if set(prompts) != set(ADVISOR_CAPABILITIES):
        raise ValueError("A prompt version is required for each advisor request kind.")
    return {
        kind: LedgerTopicMeter(
            consumption,
            model=model,
            configuration=configuration,
            prompt=prompts[kind],
            capability=capability,
            case_type=CASE_TYPE,
        )
        for kind, capability in ADVISOR_CAPABILITIES.items()
    }
