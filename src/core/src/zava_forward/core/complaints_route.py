"""Formal-complaints route boundary for resident service requests (issue 86).

A receiver is any object with ``submit(envelope) -> acknowledgement``. The only
receiver that ships is the unconfigured one: it sends nothing and says so. No
destination, credential or transport exists here; a real receiver needs a named
appointment, resident-consent source and DPO/Legal decision first. Choose with
ZF_COMPLAINTS_ROUTE=unconfigured (default).

Local recording and a receiver's receipt are different facts. An acknowledgement
is only a non-empty ``receipt_ref`` returned by the receiver. ``Failed`` means a
definite non-send (marked ``not_sent``); any other exception or an invalid reply is
``Unconfirmed``: receipt is unknown and a resend needs explicit reconciliation.
"""

from collections.abc import Mapping
from datetime import datetime
from typing import Any, NoReturn, Protocol

STATUSES = ("Pending", "Unconfigured", "Failed", "Unconfirmed", "Acknowledged")
NOT_SENT_REASON = "The request was not sent. Nothing reached the receiver."
UNCONFIRMED_REASON = (
    "Acknowledgement was not obtained. Whether the receiver has this request is unknown. "
    "Check with the receiver before sending again."
)
UNCONFIGURED_REASON = "No formal-complaints receiver is configured. Nothing was sent."
MALFORMED_REASON = UNCONFIRMED_REASON
RECEIPT_LIMIT = 100


class NotConfigured(RuntimeError):
    """No receiver is configured, so nothing leaves this system."""


class NotSent(RuntimeError):
    """A receiver raises this only when it knows nothing reached it."""


class ComplaintsReceiver(Protocol):
    """The receiver contract: one envelope in, the receiver's raw reply out."""

    def submit(self, envelope: dict[str, Any]) -> object: ...


class UnconfiguredReceiver:
    def submit(self, envelope: dict[str, Any]) -> NoReturn:
        raise NotConfigured(UNCONFIGURED_REASON)


def receiver_from_env(env: Mapping[str, str]) -> ComplaintsReceiver:
    kind = (env.get("ZF_COMPLAINTS_ROUTE") or "unconfigured").lower()
    if kind == "unconfigured":
        return UnconfiguredReceiver()
    raise ValueError(f"Unknown ZF_COMPLAINTS_ROUTE {kind!r}. No real receiver is approved.")


def build_envelope(
    case_id: str, req: Mapping[str, Any], route_key: str, attempt: int
) -> dict[str, Any]:
    """Exact minimal allow-list; owners, representative and safe-contact data stay local."""
    return dict(
        idempotency_key=route_key,
        case_ref=case_id,
        request_id=req["id"],
        route=req["route"],
        summary=req["summary"],
        desired_outcome=req["desired_outcome"],
        accessibility=list(req.get("accessibility") or []),
        review_reference=req.get("review_reference") or None,
        attempt=attempt,
    )


def parse_acknowledgement(value: Any) -> dict[str, Any]:
    ref = value.get("receipt_ref") if isinstance(value, dict) else None
    if not isinstance(ref, str) or not ref.strip() or len(ref.strip()) > RECEIPT_LIMIT:
        raise ValueError(MALFORMED_REASON)
    received = value.get("received_at")
    if received is not None:
        try:
            datetime.fromisoformat(received)
        except (TypeError, ValueError):
            raise ValueError(MALFORMED_REASON) from None
    return dict(receipt_ref=ref.strip(), received_at=received)
