"""Person-approved envelope and downside limits with a pause signal, never a decision.

The module holds no company figures. Limits exist only when a person supplies them with an
approval record, and a breach only raises a signal for a named human decision.
"""

import json
import math
import re
from collections.abc import Iterable
from copy import deepcopy
from datetime import date, datetime
from pathlib import Path
from typing import Any, TypeGuard

type Record = dict[str, Any]

DIMENSIONS = ("safety", "resident", "quality", "capital", "grant", "capacity")
NOTICE = (
    "Signal for a human decision only. It does not approve, resume or accelerate "
    "delivery, and it does not contain or release live activity."
)
UNAPPROVED = "Pause for human decision"
MAX_AGE_DAYS = 366
BREACH_ACTION = "Escalate to the Board and control owners; restart needs their recorded approval."
_TOP_LEVEL_KEYS = frozenset({"approval", "envelope", "tolerances", "liquidity"})
_APPROVAL_KEYS = frozenset(
    {
        "approved_by",
        "approved_at",
        "approver",
        "approved_on",
        "role",
        "evidence_ref",
        "restart_owner",
    }
)
_ENVELOPE_KEYS = frozenset({"amount", "currency", "period", "annual_plan"})
_TOLERANCE_KEYS = frozenset({"maximum", "unit"})
_LIQUIDITY_KEYS = frozenset({"minimum", "currency", "covenant_minimum", "covenant_unit"})
_FLOOR_LIMITS = frozenset({"liquidity", "covenant"})


class LimitsError(ValueError):
    pass


def _check_keys(mapping: Record, allowed: frozenset[str], label: str) -> None:
    unknown = sorted(str(k) for k in mapping if k not in allowed)
    if unknown:
        raise LimitsError(f"Unknown {label} field: {', '.join(unknown)}.")


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LimitsError(f"{field} is required.")
    return value.strip()


def _number(value: object, field: str) -> float:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise LimitsError(f"{field} must be a finite number.")
    try:
        numeric = float(value)
    except OverflowError as exc:
        raise LimitsError(f"{field} must be a finite number.") from exc
    if not math.isfinite(numeric):
        raise LimitsError(f"{field} must be a finite number.")
    if value < 0:
        raise LimitsError(f"{field} must not be negative.")
    return numeric


def _finite_observation(value: object) -> TypeGuard[int | float]:
    # Integers are always finite; isfinite would overflow on very large ones.
    return type(value) is int or (type(value) is float and math.isfinite(value))


def _non_negative_finite_observation(value: object) -> TypeGuard[int | float]:
    return _finite_observation(value) and value >= 0


def _iso_date(text: str, field: str) -> str:
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text) is None:
        raise LimitsError(f"{field} must be an ISO date (YYYY-MM-DD).")
    try:
        date.fromisoformat(text)
    except ValueError as exc:
        raise LimitsError(f"{field} must be an ISO date (YYYY-MM-DD).") from exc
    return text


def _iso_date_or_timestamp(text: str, field: str) -> tuple[str, str]:
    if len(text) == 10:
        day = _iso_date(text, field)
        return day, day
    if len(text) <= 10 or text[10] != "T" or any(ch.isspace() for ch in text):
        raise LimitsError(f"{field} must be an ISO date or timestamp.")
    day = _iso_date(text[:10], field)
    try:
        datetime.fromisoformat(text)
    except ValueError as exc:
        raise LimitsError(f"{field} must be an ISO date or timestamp.") from exc
    return text, day


def _approval(value: object) -> Record:
    if not isinstance(value, dict):
        raise LimitsError("An approval record is required.")
    _check_keys(value, _APPROVAL_KEYS, "approval")
    # approved_by / approved_at are the canonical names; approver / approved_on remain accepted.
    raw_at = value.get("approved_at")
    raw_on = value.get("approved_on")
    if raw_at is not None and raw_on is not None:
        approved_at, approved_on = _iso_date_or_timestamp(
            _text(raw_at, "approved_at"), "approved_at"
        )
        explicit_on = _iso_date(_text(raw_on, "approved_on"), "approved_on")
        if explicit_on != approved_on:
            raise LimitsError("approved_at and approved_on must match when both are supplied.")
    elif raw_at is not None:
        approved_at, approved_on = _iso_date_or_timestamp(
            _text(raw_at, "approved_at"), "approved_at"
        )
    else:
        approved_on = _iso_date(_text(raw_on, "approved_at"), "approved_at")
        approved_at = approved_on

    raw_by = value.get("approved_by")
    raw_approver = value.get("approver")
    if raw_by is not None and raw_approver is not None:
        approved_by = _text(raw_by, "approved_by")
        if approved_by != _text(raw_approver, "approver"):
            raise LimitsError("approved_by and approver must match when both are supplied.")
    else:
        approved_by = _text(raw_by if raw_by is not None else raw_approver, "approved_by")

    return dict(
        approved_by=approved_by,
        approved_at=approved_at,
        approver=approved_by,
        role=_text(value.get("role"), "role"),
        approved_on=approved_on,
        evidence_ref=_text(value.get("evidence_ref"), "evidence_ref"),
        restart_owner=_text(value.get("restart_owner"), "restart_owner"),
    )


def _liquidity(value: object) -> Record:
    if not isinstance(value, dict):
        raise LimitsError("liquidity limits must be a record.")
    _check_keys(value, _LIQUIDITY_KEYS, "liquidity")
    record: Record = dict(
        minimum=_number(value.get("minimum"), "liquidity minimum"),
        currency=_text(value.get("currency"), "liquidity currency"),
    )
    cov_min = value.get("covenant_minimum")
    cov_unit = value.get("covenant_unit")
    if cov_min is not None or cov_unit is not None:
        record["covenant_minimum"] = _number(cov_min, "covenant minimum")
        record["covenant_unit"] = _text(cov_unit, "covenant unit")
    return record


def record_limits(
    approval: object,
    envelope: object,
    tolerances: object,
    *,
    liquidity: object = None,
) -> Record:
    """Return a limits record from supplied, person-approved inputs.

    Authority of the approver is recorded as supplied; it is not verified here.
    """
    if not isinstance(envelope, dict):
        raise LimitsError("An investment envelope is required.")
    _check_keys(envelope, _ENVELOPE_KEYS, "envelope")
    if not isinstance(tolerances, dict) or not tolerances:
        raise LimitsError("At least one downside tolerance is required.")
    unknown = sorted(set(tolerances) - set(DIMENSIONS))
    if unknown:
        raise LimitsError(f"Unknown tolerance dimension: {', '.join(map(str, unknown))}.")
    envelope_record: Record = dict(
        amount=_number(envelope.get("amount"), "envelope amount"),
        currency=_text(envelope.get("currency"), "envelope currency"),
        period=_text(envelope.get("period"), "envelope period"),
    )
    if envelope.get("annual_plan") is not None:
        envelope_record["annual_plan"] = _number(
            envelope.get("annual_plan"), "envelope annual_plan"
        )
    tolerance_records: dict[str, Record] = {}
    for name, limit in sorted(tolerances.items()):
        if not isinstance(limit, dict):
            raise LimitsError(f"{name} tolerance must be a record.")
        _check_keys(limit, _TOLERANCE_KEYS, f"{name} tolerance")
        tolerance_records[name] = dict(
            maximum=_number(limit.get("maximum"), name),
            unit=_text(limit.get("unit"), f"{name} unit"),
        )
    recorded: Record = dict(
        approval=_approval(approval),
        envelope=envelope_record,
        tolerances=tolerance_records,
    )
    if liquidity is not None:
        recorded["liquidity"] = _liquidity(liquidity)
    return recorded


def pause_signal(paused: bool, reason: str, decision_owner: str | None = None) -> Record:
    """Deterministic signal for a named human decision; it never cuts or restarts anything."""
    return dict(
        paused=paused,
        decision_required=paused,
        decision_owner=decision_owner,
        automatic_cut=False,
        reason=reason,
    )


def held(reason: str) -> Record:
    return dict(
        status="Held",
        signal=UNAPPROVED,
        reason=reason,
        findings=[],
        notice=NOTICE,
        pause_signal=pause_signal(True, reason),
    )


_held = held


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
        return held("No person-approved investment limit or tolerances are recorded.")
    if not isinstance(limits, dict):
        return _held("The approved limits record is not readable, so it cannot be relied on.")
    try:
        _check_keys(limits, _TOP_LEVEL_KEYS, "limits")
        canonical = record_limits(
            limits.get("approval"),
            limits.get("envelope"),
            limits.get("tolerances"),
            liquidity=limits.get("liquidity"),
        )
        stale = stale_reason(canonical, today)
    except (LimitsError, KeyError, TypeError, ValueError):
        return _held("The approved limits record is not readable, so it cannot be relied on.")
    if stale:
        return _held(stale)
    obs_exposure: Record = exposure if isinstance(exposure, dict) else {}
    findings: list[Record] = []
    committed = obs_exposure.get("committed")
    envelope = canonical["envelope"]
    currency_matches = obs_exposure.get("currency") == envelope["currency"]
    if not _non_negative_finite_observation(committed) or not currency_matches:
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
    if "annual_plan" in envelope:
        annual_obs = obs_exposure.get("annual_committed", committed)
        if not _non_negative_finite_observation(annual_obs) or not currency_matches:
            findings.append(dict(limit="annual_plan", state="Unknown"))
        else:
            findings.append(
                dict(
                    limit="annual_plan",
                    state="Breach" if annual_obs > envelope["annual_plan"] else "Within",
                    observed=annual_obs,
                    maximum=envelope["annual_plan"],
                    unit=envelope["currency"],
                )
            )
    if "liquidity" in canonical:
        liq = canonical["liquidity"]
        raw_liq = obs_exposure.get("liquidity")
        liq_value: object
        liq_currency: object
        if isinstance(raw_liq, dict) and set(raw_liq) <= {"available", "currency"}:
            liq_value = raw_liq.get("available")
            liq_currency = raw_liq.get("currency")
        elif not isinstance(raw_liq, dict):
            liq_value = raw_liq
            liq_currency = obs_exposure.get("liquidity_currency", obs_exposure.get("currency"))
        else:
            liq_value, liq_currency = None, None
        if not _finite_observation(liq_value) or liq_currency != liq["currency"]:
            findings.append(dict(limit="liquidity", state="Unknown"))
        else:
            findings.append(
                dict(
                    limit="liquidity",
                    state="Breach" if liq_value < liq["minimum"] else "Within",
                    observed=liq_value,
                    minimum=liq["minimum"],
                    unit=liq["currency"],
                )
            )
        if "covenant_minimum" in liq:
            raw_cov = obs_exposure.get("covenant")
            cov_value: object
            cov_unit: object
            if isinstance(raw_cov, dict) and set(raw_cov) <= {"headroom", "unit"}:
                cov_value = raw_cov.get("headroom")
                cov_unit = raw_cov.get("unit")
            elif not isinstance(raw_cov, dict):
                cov_value = raw_cov
                cov_unit = obs_exposure.get("covenant_unit")
            else:
                cov_value, cov_unit = None, None
            if not _finite_observation(cov_value) or cov_unit != liq["covenant_unit"]:
                findings.append(dict(limit="covenant", state="Unknown"))
            else:
                findings.append(
                    dict(
                        limit="covenant",
                        state="Breach" if cov_value < liq["covenant_minimum"] else "Within",
                        observed=cov_value,
                        minimum=liq["covenant_minimum"],
                        unit=liq["covenant_unit"],
                    )
                )
    raw_tolerances = obs_exposure.get("tolerances")
    observed = raw_tolerances if isinstance(raw_tolerances, dict) else {}
    for name, limit in canonical["tolerances"].items():
        value = observed.get(name)
        if not _non_negative_finite_observation(value):
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
    upper_breached = [
        f["limit"] for f in findings if f["state"] == "Breach" and f["limit"] not in _FLOOR_LIMITS
    ]
    floor_breached = [
        f["limit"] for f in findings if f["state"] == "Breach" and f["limit"] in _FLOOR_LIMITS
    ]
    unknown = [f["limit"] for f in findings if f["state"] == "Unknown"]
    if upper_breached or floor_breached:
        status, signal = "Breach", UNAPPROVED
        parts: list[str] = []
        if upper_breached:
            parts.append(f"Over approved limit: {', '.join(upper_breached)}")
        if floor_breached:
            prefix = "below" if parts else "Below"
            parts.append(f"{prefix} approved minimum: {', '.join(floor_breached)}")
        reason = f"{'; '.join(parts)}."
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
        approval=deepcopy(canonical["approval"]),
        action=BREACH_ACTION if status != "Within limits" else None,
        notice=NOTICE,
        pause_signal=pause_signal(
            signal == UNAPPROVED, reason, canonical["approval"]["restart_owner"]
        ),
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
    _check_keys(data, _TOP_LEVEL_KEYS, "limits")
    return record_limits(
        data.get("approval"),
        data.get("envelope"),
        data.get("tolerances"),
        liquidity=data.get("liquidity"),
    )


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
