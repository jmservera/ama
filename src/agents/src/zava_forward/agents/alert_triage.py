"""Staff alert precision and acknowledgement time scoring.

Scores recorded staff classifications and acknowledgements only. It reports each
check separately, never an overall pass, and never invents evidence: with no
staff observations or no owner-agreed thresholds the checks stay unmeasured or
unthresholded. A recorded human classification and acknowledgement is the only
accepted source; nothing here acknowledges or classifies an alert.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import datetime
from math import isfinite
from statistics import median
from typing import Any

from zava_forward.agents.regulatory_gates import OWNER

CLASSES = ("true_positive", "false_positive")
THRESHOLD_KEYS = ("owner", "agreed_on", "min_alerts", "min_precision", "max_median_ack_seconds")


def _moment(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else None


def valid_alert(row: Mapping[str, Any]) -> str | None:
    """Return the reason an alert record cannot be scored, or None."""
    for key in ("alert_id", "reviewer"):
        if not isinstance(row.get(key), str) or not row[key].strip():
            return f"{key} missing"
    if _moment(row.get("published_at")) is None:
        return "published_at not a timezone-aware ISO time"
    if row.get("classification") not in (*CLASSES, None):
        return "classification not true_positive, false_positive or unrecorded"
    ack = row.get("acknowledged_at")
    if ack is not None:
        moment, start = _moment(ack), _moment(row["published_at"])
        if moment is None or start is None:
            return "acknowledged_at not a timezone-aware ISO time"
        if moment < start:
            return "acknowledged_at before published_at"
    return None


def _threshold_gaps(thresholds: Mapping[str, Any] | None) -> list[str]:
    if not thresholds:
        return ["no owner-agreed thresholds recorded"]
    gaps = [f"{key} missing" for key in THRESHOLD_KEYS if thresholds.get(key) is None]
    owner = thresholds.get("owner")
    if owner is not None and (not isinstance(owner, str) or not owner.strip()):
        gaps.append("owner not a named person")
    if thresholds.get("agreed_on") is not None:
        try:
            datetime.fromisoformat(str(thresholds["agreed_on"]))
        except ValueError:
            gaps.append("agreed_on not an ISO date")
    for key in THRESHOLD_KEYS[2:]:
        value = thresholds.get(key)
        if value is not None and not (
            isinstance(value, int | float)
            and not isinstance(value, bool)
            and isfinite(value)
            and value >= 0
        ):
            gaps.append(f"{key} not a non-negative number")
    return gaps


def evaluate_alert_triage(
    observations: Iterable[Mapping[str, Any]],
    *,
    thresholds: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Score alert precision and acknowledgement time as two separate checks."""
    valid, invalid = [], []
    for index, row in enumerate(observations):
        reason = valid_alert(row)
        (invalid.append(dict(index=index, reason=reason)) if reason else valid.append(row))
    gaps = _threshold_gaps(thresholds)
    agreed = not gaps and thresholds is not None
    classified = [row for row in valid if row.get("classification")]
    true_positives = sum(1 for row in classified if row["classification"] == "true_positive")
    seconds = [
        (_moment(row["acknowledged_at"]) - _moment(row["published_at"])).total_seconds()  # type: ignore[operator]
        for row in valid
        if row.get("acknowledged_at") is not None
    ]
    precision_reasons = list(gaps)
    ack_reasons = list(gaps)
    precision = true_positives / len(classified) if classified else None
    median_ack = median(seconds) if seconds else None
    if invalid:
        precision_reasons.append("invalid alert records excluded; observations must be repaired")
        ack_reasons.append("invalid alert records excluded; observations must be repaired")
    if agreed and thresholds is not None:
        if len(classified) < thresholds["min_alerts"]:
            precision_reasons.append("fewer classified alerts than the agreed minimum")
        elif precision is not None and precision < thresholds["min_precision"]:
            precision_reasons.append("precision below agreed threshold")
        if len(seconds) < thresholds["min_alerts"]:
            ack_reasons.append("fewer acknowledged alerts than the agreed minimum")
        elif median_ack is not None and median_ack > thresholds["max_median_ack_seconds"]:
            ack_reasons.append("median acknowledgement time above agreed maximum")
    precision_check = dict(
        name="staff_alert_precision",
        status="not_evaluated" if not classified else "measured",
        precision=precision,
        classified=len(classified),
        true_positives=true_positives,
        false_positives=len(classified) - true_positives,
        unclassified=len(valid) - len(classified),
        reasons=precision_reasons,
    )
    ack_check = dict(
        name="staff_acknowledgement_time",
        status="not_evaluated" if not seconds else "measured",
        acknowledged=len(seconds),
        unacknowledged=len(valid) - len(seconds),
        median_seconds=median_ack,
        max_seconds=max(seconds) if seconds else None,
        reasons=ack_reasons,
    )
    return dict(
        checks=[precision_check, ack_check],
        invalid_observations=invalid,
        threshold=dict(
            value=dict(thresholds) if agreed and thresholds else None,
            status="owner_agreed" if agreed else "unset_pending_owner_agreement",
            gaps=gaps,
            owner=OWNER,
        ),
        overall_pass=None,
        approval="Measurements only; thresholds and alert rules stay with named owners.",
    )
