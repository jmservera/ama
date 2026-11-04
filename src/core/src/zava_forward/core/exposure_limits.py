"""Person-approved envelope and downside limits with a pause signal, never a decision.

The module holds no company figures. Limits exist only when a person supplies them with an
approval record, and a breach only raises a signal for a named human decision.
"""

import json
import math
import re
from collections.abc import Iterable
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any

type Record = dict[str, Any]

DIMENSIONS = ("safety", "resident", "quality", "capital", "grant", "capacity")
NOTICE = (
    "Signal for a human decision only. It does not approve, resume or accelerate "
    "delivery, and it does not contain or release live activity."
)
UNAPPROVED = "Pause for human decision"
MAX_AGE_DAYS = 366
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


def _held(reason: str) -> Record:
    return dict(status="Held", signal=UNAPPROVED, reason=reason, findings=[], notice=NOTICE)


def stale_reason(limits: Record, today: date | None = None) -> str | None:
    """Return a plain reason when approved limits are older than one year or dated in the future."""
    today = today or date.today()
    approved = date.fromisoformat(limits["approval"]["approved_on"])
    if approved > today:
        return "The approved limits are dated in the future, so they cannot be relied on."
    if (today - approved).days > MAX_AGE_DAYS:
        return (
            f"The approved limits were approved on {approved.isoformat()}, more than "
            f"{MAX_AGE_DAYS} days ago, so they are out of date and need re-approval."
        )
    return None


def assess(limits: Record | None, exposure: Record | None, today: date | None = None) -> Record:
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
    try:
        stale = stale_reason(limits, today)
    except (KeyError, TypeError, ValueError):
        stale = "The approved limits record is not readable, so it cannot be relied on."
    if stale:
        return _held(stale)
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


def load_limits(path: Path) -> Record | None:
    """Read limits a person supplied as a JSON file; a missing file means none are recorded."""
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as exc:
        raise LimitsError("The approved limits file cannot be read.") from exc
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise LimitsError("The approved limits file is not valid JSON.") from exc
    if not isinstance(data, dict):
        raise LimitsError("The approved limits file must hold one object.")
    return record_limits(data.get("approval"), data.get("envelope"), data.get("tolerances"))


def committed_exposure(cases: Iterable[Record], currency: str = "GBP") -> Record:
    """Sum non-cancelled commitments as recorded ; raises LimitsError on a non-numeric amount.

    Downside tolerances are not observed here.
    """
    committed = 0.0
    for case in cases:
        for commitment in (case.get("finance") or {}).get("commitments", []):
            if commitment.get("status") != "Cancelled":
                amount = commitment.get("amount")
                if amount is None:
                    continue
                if not isinstance(amount, int | float) or isinstance(amount, bool):
                    raise LimitsError("A recorded commitment amount is not a number.")
                if not math.isfinite(amount):
                    raise LimitsError("A recorded commitment amount is not a number.")
                committed += float(amount)
    return dict(committed=round(committed, 2), currency=currency, tolerances={})
