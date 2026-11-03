"""Person-approved envelope and downside limits with a pause signal, never a decision.

The module holds no company figures. Limits exist only when a person supplies them with an
approval record, and a breach only raises a signal for a named human decision.
"""

import math
import re
from copy import deepcopy
from datetime import date
from typing import Any

type Record = dict[str, Any]

DIMENSIONS = ("safety", "resident", "quality", "capital", "grant", "capacity")
NOTICE = (
    "Signal for a human decision only. It does not approve, resume or accelerate "
    "delivery, and it does not contain or release live activity."
)
UNAPPROVED = "Pause for human decision"
BREACH_ACTION = "Escalate to the Board and control owners; restart needs their recorded approval."


class LimitsError(ValueError):
    pass


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LimitsError(f"{field} is required.")
    return value.strip()


def _number(value: object, field: str) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool) or not math.isfinite(value):
        raise LimitsError(f"{field} must be a finite number.")
    if value < 0:
        raise LimitsError(f"{field} must not be negative.")
    return float(value)


def _approval(value: object) -> Record:
    if not isinstance(value, dict):
        raise LimitsError("An approval record is required.")
    approved_on = _text(value.get("approved_on"), "approved_on")
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", approved_on) is None:
        raise LimitsError("approved_on must be an ISO date.")
    try:
        date.fromisoformat(approved_on)
    except ValueError as exc:
        raise LimitsError("approved_on must be an ISO date.") from exc
    return dict(
        approver=_text(value.get("approver"), "approver"),
        role=_text(value.get("role"), "role"),
        approved_on=approved_on,
        evidence_ref=_text(value.get("evidence_ref"), "evidence_ref"),
        restart_owner=_text(value.get("restart_owner"), "restart_owner"),
    )


def record_limits(approval: object, envelope: object, tolerances: object) -> Record:
    """Return a limits record from supplied, person-approved inputs.

    Authority of the approver is recorded as supplied; it is not verified here.
    """
    if not isinstance(envelope, dict):
        raise LimitsError("An investment envelope is required.")
    if not isinstance(tolerances, dict) or not tolerances:
        raise LimitsError("At least one downside tolerance is required.")
    unknown = sorted(set(tolerances) - set(DIMENSIONS))
    if unknown:
        raise LimitsError(f"Unknown tolerance dimension: {', '.join(map(str, unknown))}.")
    return dict(
        approval=_approval(approval),
        envelope=dict(
            amount=_number(envelope.get("amount"), "envelope amount"),
            currency=_text(envelope.get("currency"), "envelope currency"),
            period=_text(envelope.get("period"), "envelope period"),
        ),
        tolerances={
            name: dict(
                maximum=_number(limit.get("maximum") if isinstance(limit, dict) else None, name),
                unit=_text(limit.get("unit") if isinstance(limit, dict) else None, f"{name} unit"),
            )
            for name, limit in sorted(tolerances.items())
        },
    )


def assess(limits: Record | None, exposure: Record | None) -> Record:
    """Compare observed exposure with approved limits and return a pause signal.

    Without approved limits the result is held and nothing is evaluated. A missing or
    mismatched observation is Unknown, never treated as within limits.
    """
    if limits is None:
        return dict(
            status="Held",
            signal=UNAPPROVED,
            reason="No person-approved envelope or tolerances are recorded.",
            findings=[],
            notice=NOTICE,
        )
    exposure = exposure or {}
    findings: list[Record] = []
    committed = exposure.get("committed")
    envelope = limits["envelope"]
    if (
        type(committed) not in (int, float)
        or committed != committed
        or exposure.get("currency") != envelope["currency"]
    ):
        findings.append(dict(limit="envelope", state="Unknown"))
    else:
        findings.append(
            dict(
                limit="envelope",
                state="Breach" if committed > envelope["amount"] else "Within",
                observed=committed,
                maximum=envelope["amount"],
                unit=envelope["currency"],
            )
        )
    observed = exposure.get("tolerances")
    observed = observed if isinstance(observed, dict) else {}
    for name, limit in limits["tolerances"].items():
        value = observed.get(name)
        if type(value) not in (int, float) or value != value:
            findings.append(dict(limit=name, state="Unknown"))
            continue
        findings.append(
            dict(
                limit=name,
                state="Breach" if value > limit["maximum"] else "Within",
                observed=value,
                maximum=limit["maximum"],
                unit=limit["unit"],
            )
        )
    breached = [f["limit"] for f in findings if f["state"] == "Breach"]
    unknown = [f["limit"] for f in findings if f["state"] == "Unknown"]
    if breached:
        status, signal = "Breach", UNAPPROVED
        reason = f"Over approved limit: {', '.join(breached)}."
    elif unknown:
        status, signal = "Unknown", UNAPPROVED
        reason = f"Exposure not supplied or not comparable: {', '.join(unknown)}."
    else:
        status, signal = "Within limits", "No pause signal"
        reason = (
            "Observed exposure is within every approved limit; this is not approval to accelerate."
        )
    return dict(
        status=status,
        signal=signal,
        reason=reason,
        findings=findings,
        approval=deepcopy(limits["approval"]),
        action=BREACH_ACTION if status != "Within limits" else None,
        notice=NOTICE,
    )
