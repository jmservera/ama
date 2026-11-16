"""Bounded latest sensor summary per home for the employee map (issue 1818).

Read only and built on the retained-reading read model in `sensor_view`: one newest synthetic
reading per home (an indexed, one-row query), at most `HOME_CAP` homes per call, and the same
fail-closed recorded-consent check. No history leaves this module. Role projection is decided by
the caller: it passes only authorised homes here and uses `fixed` for everyone else.
"""

from collections.abc import Iterable
from datetime import UTC, datetime, timedelta
from typing import Any

from . import sensor_view

HOME_CAP = 100
OFFLINE_SECONDS = 86400
PROVENANCE = "Synthetic simulator reading. Not calibrated, so not a verified indoor measurement."
LABELS = dict(
    fresh="Recent reading (within 15 minutes)",
    stale="Reading out of date (older than 15 minutes)",
    offline="Sensor offline (no reading for over 24 hours)",
    **{
        "no-readings": "No sensor readings recorded",
        "consent-withheld": "Readings withheld: monitoring consent is not granted",
        "unavailable": "Sensor readings could not be read",
        "restricted": "Sensor readings are not shown for your role",
        "not-connected": "Sensor readings are not connected in this deployment",
        "not-loaded": "Sensor status not loaded. Zoom in or narrow the filters",
        "future-dated": "Latest reading is dated in the future and is not treated as recent",
    },
)
ALERT_STATES = ("stale", "offline")


def fixed(state: str) -> dict[str, Any]:
    """A summary that carries a state and its plain-language label, never a value."""
    return dict(state=state, label=LABELS[state], alert=False, calibrated=False)


def _classify(age: int) -> str:
    if age < 0:
        return "future-dated"
    if age <= sensor_view.FRESH_SECONDS:
        return "fresh"
    return "stale" if age <= OFFLINE_SECONDS else "offline"


def _latest(db: Any, mssql: bool, home_id: str, now: float) -> dict[str, Any] | None:
    as_of = datetime.fromtimestamp(int(now), UTC)
    rows = sensor_view._select(
        db,
        mssql,
        home_id,
        1,
        True,
        lower=as_of - timedelta(days=sensor_view.WINDOW_DAYS),
        upper=as_of + timedelta(seconds=1),
    )
    return rows[-1] if rows else None


def _number(value: object) -> float | None:
    try:
        return round(float(str(value)), 1)
    except ValueError:
        return None


def summary(db: Any, home_id: str, now: float, mssql: bool = False) -> dict[str, Any]:
    try:
        latest = _latest(db, mssql, home_id, now)
        if latest is None:
            return fixed("no-readings")
        if sensor_view.consent(db, home_id, {latest["sensor_id"]}, mssql) != "granted":
            return fixed("consent-withheld")
        observed = datetime.strptime(latest["observed_at"], sensor_view.STAMP).replace(tzinfo=UTC)
        age = int(now) - int(observed.timestamp())
    except Exception:
        return fixed("unavailable")
    state = _classify(age)
    out = dict(
        fixed(state),
        alert=state in ALERT_STATES,
        observed_at=latest["observed_at"],
        age_seconds=max(age, 0),
        source=PROVENANCE,
    )
    if state != "future-dated":
        out.update(
            temperature_c=_number(latest["temperature_c"]),
            humidity_pct=_number(latest["humidity_pct"]),
        )
    return out


def summaries(
    db: Any, home_ids: Iterable[str], now: float, mssql: bool = False
) -> dict[str, dict[str, Any]]:
    """Summaries for at most `HOME_CAP` homes; the rest are marked `not-loaded`."""
    ids = list(dict.fromkeys(home_ids))
    out = {home_id: summary(db, home_id, now, mssql) for home_id in ids[:HOME_CAP]}
    out.update({home_id: fixed("not-loaded") for home_id in ids[HOME_CAP:]})
    return out
