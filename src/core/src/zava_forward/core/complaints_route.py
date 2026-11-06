"""Formal-complaints route boundary for resident service requests (issue 86).

A receiver is any object with ``submit(envelope) -> acknowledgement``. The only
receiver that ships is the unconfigured one: it sends nothing and says so. No
destination, credential or transport exists here; a real receiver needs a named
appointment, resident-consent source and DPO/Legal decision first. Choose with
ZF_COMPLAINTS_ROUTE=unconfigured (default).

Local recording and a receiver's receipt are different facts. An acknowledgement
is only a non-empty ``receipt_ref`` returned by the receiver; anything else is a
failure, never a receipt.
"""

from collections.abc import Mapping
from datetime import datetime
from typing import Any, NoReturn, Protocol

STATUSES = ("Pending", "Unconfigured", "Failed", "Acknowledged")
FAILURE_REASON = "The receiver did not acknowledge this request. It has not been received."
UNCONFIGURED_REASON = "No formal-complaints receiver is configured. Nothing was sent."
MALFORMED_REASON = (
    "The receiver reply had no valid receipt reference. It has not been treated as received."
)
RECEIPT_LIMIT = 100


class NotConfigured(RuntimeError):
    """No receiver is configured, so nothing leaves this system."""


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
