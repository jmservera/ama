"""Plain-language freshness and calibration badges for the employee sensor response (issue 1288).

Pure and read-only. Every state carries a text label, so status never relies on colour alone, and
the response states that the telemetry is advisory.
"""

from collections.abc import Mapping
from typing import Any

ADVISORY = "Advisory telemetry \u2014 officer review required"

_FRESHNESS = {
    "withheld": ("Withheld", "Readings are withheld because monitoring consent is not granted."),
    "unavailable": ("Unavailable", "No reading is shown for this home."),
    "offline": ("Offline", "No recent reading has arrived. The sensor may be offline."),
    "stale": ("Stale", "The latest reading is older than 15 minutes."),
    "fresh": ("Fresh", "The latest reading is within 15 minutes."),
    "unknown": ("Freshness unknown", "The age of the latest reading cannot be shown."),
}


_HEALTH = {
    "fault": ("Sensor fault", "The latest reading is missing a value or cannot be read."),
    "out_of_range": ("Out of range", "The latest reading is outside the possible range."),
}

_NEXT_ACTION = {
    "withheld": "Use the ordinary quality check. Do not ask for the readings without consent.",
    "unavailable": "Use the ordinary quality check. Ask the quality team if you need the readings.",
    "offline": "Use the ordinary quality check, then ask the quality team to check the sensor.",
    "fault": "Do not use this reading. Use the ordinary quality check and report the sensor fault.",
    "out_of_range": "Do not use this reading. Use the ordinary quality check and ask for a check.",
    "stale": "Treat the reading as out of date. Use the ordinary quality check for now.",
}


def freshness_state(view: Mapping[str, Any]) -> str:
    if view.get("state") == "consent-withheld":
        return "withheld"
    if view.get("state") == "unavailable":
        return "unavailable"
    if view.get("state") == "no-readings" or not view.get("latest"):
        return "offline"
    freshness = view.get("freshness")
    return str(freshness) if freshness in ("fresh", "stale") else "unknown"


def health_state(view: Mapping[str, Any]) -> str:
    """fault or out_of_range only when a reading is shown; withheld or empty views have none."""
    if freshness_state(view) in ("withheld", "unavailable", "offline"):
        return "ok"
    state = (view.get("health") or {}).get("state")
    return str(state) if state in _HEALTH else "ok"


def next_action(view: Mapping[str, Any]) -> str | None:
    """One plain operator step, most serious state first. None when the reading is usable."""
    freshness = freshness_state(view)
    health = health_state(view)
    for key in (
        freshness if freshness in ("withheld", "unavailable", "offline") else None,
        health,
        freshness,
    ):
        if key in _NEXT_ACTION:
            return _NEXT_ACTION[key]
    return None


def badges(view: Mapping[str, Any]) -> list[dict[str, str]]:
    state = freshness_state(view)
    label, text = _FRESHNESS[state]
    out = [dict(kind="freshness", state=state, label=label, text=text)]
    health = health_state(view)
    if health in _HEALTH:
        out.append(
            dict(kind="health", state=health, label=_HEALTH[health][0], text=_HEALTH[health][1])
        )
    return out + [
        dict(
            kind="calibration",
            state="uncalibrated",
            label="Uncalibrated",
            text="Not calibrated. Not a verified indoor measurement.",
        ),
    ]


def annotate(view: Mapping[str, Any]) -> dict[str, Any]:
    """The sensor response with text badges and advisory provenance added."""
    return dict(view, badges=badges(view), advisory=ADVISORY, next_action=next_action(view))
