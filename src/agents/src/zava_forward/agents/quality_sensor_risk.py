"""Explainable damp and mould inspection risk from retained sensor evidence.

Advisory only. It combines retained humidity readings with the age of the last
inspection into ranked, named factors. Thresholds are labelled exercise values,
not approved sensor rules (issue #111, R1 to R3 not complete). Missing or stale
telemetry is reported as insufficient and never lowers priority: the inspection
age factor still applies. Nothing here schedules, closes or signs off an
inspection; a named human inspector decides.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import datetime, timedelta
from typing import Any

METHOD_VERSION = "exercise-quality-risk-1"
THRESHOLD_STATUS = "exercise value, not an approved sensor rule"
HUMIDITY_HIGH_PCT = 70.0
HUMIDITY_SHARE_MIN = 0.25
MIN_READINGS = 6
STALE_AFTER = timedelta(hours=48)
INSPECTION_DUE_DAYS = 365
NEVER_INSPECTED_DAYS = INSPECTION_DUE_DAYS * 2


def _moment(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else None


def _humidity(
    readings: Iterable[Mapping[str, Any]], as_of: datetime
) -> list[tuple[datetime, float]]:
    out = []
    for row in readings or ():
        when, rh = _moment(row.get("observed_at")), row.get("relative_humidity")
        if when is None or when > as_of or isinstance(rh, bool) or not isinstance(rh, (int, float)):
            continue
        if 0 <= rh <= 100:
            out.append((when, float(rh)))
    return out


def _sensor_factors(
    valid: list[tuple[datetime, float]], as_of: datetime
) -> tuple[str, str, list[dict]]:
    if len(valid) < MIN_READINGS:
        return "insufficient", f"fewer than {MIN_READINGS} valid retained readings", []
    if as_of - max(when for when, _ in valid) > STALE_AFTER:
        return "insufficient", "latest retained reading is stale", []
    high = sum(1 for _, rh in valid if rh >= HUMIDITY_HIGH_PCT)
    share = high / len(valid)
    factors = []
    if share >= HUMIDITY_SHARE_MIN:
        factors.append(
            dict(
                factor="sustained_high_humidity",
                score=round(min(share, 1.0) * 60, 1),
                evidence=(
                    f"{high} of {len(valid)} retained readings at or above {HUMIDITY_HIGH_PCT}% RH"
                ),
            )
        )
    return "sufficient", "", factors


def explain_inspection_risk(
    home_id: str,
    readings: Iterable[Mapping[str, Any]] | None,
    last_inspected_at: str | None,
    as_of: str,
) -> dict[str, Any]:
    """Return an advisory, ranked factor explanation for one home."""
    now = _moment(as_of)
    if now is None:
        raise ValueError("as_of must be a timezone-aware ISO time")
    status, gap, factors = _sensor_factors(_humidity(readings or (), now), now)
    last = _moment(last_inspected_at)
    if last is None or last > now:
        age, evidence = NEVER_INSPECTED_DAYS, "no valid previous inspection recorded"
    else:
        age = (now - last).days
        evidence = f"last inspection {age} days before {as_of}"
    if age >= INSPECTION_DUE_DAYS:
        score = round(min(age / NEVER_INSPECTED_DAYS, 1.0) * 40, 1)
        factors.append(dict(factor="inspection_age", score=score, evidence=evidence))
    factors.sort(key=lambda f: (-f["score"], f["factor"]))
    for rank, item in enumerate(factors, 1):
        item["rank"] = rank
    return dict(
        home_id=home_id,
        method_version=METHOD_VERSION,
        threshold_status=THRESHOLD_STATUS,
        advisory_only=True,
        requires_inspector_signoff=True,
        signoff_state="pending_human_inspector",
        telemetry_status=status,
        telemetry_gap=gap or None,
        total_score=round(sum(f["score"] for f in factors), 1),
        factors=factors,
    )


def rank_homes(explanations: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    """Order for human review; on equal score, insufficient telemetry ranks first."""
    return sorted(
        (dict(e) for e in explanations),
        key=lambda e: (-e["total_score"], e["telemetry_status"] != "insufficient", e["home_id"]),
    )
