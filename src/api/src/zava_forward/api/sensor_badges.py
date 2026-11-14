"""Plain-language freshness and calibration badges for the employee sensor response (issue 1288).

Pure and read-only. Every state carries a text label, so status never relies on colour alone, and
the response states that the telemetry is advisory.
"""

from collections.abc import Mapping
from typing import Any

ADVISORY = "Advisory telemetry \u2014 officer review required"

_FRESHNESS = {
    "unavailable": ("Unavailable", "No reading is shown for this home."),
    "offline": ("Offline", "No recent reading has arrived. The sensor may be offline."),
    "stale": ("Stale", "The latest reading is older than 15 minutes."),
    "fresh": ("Fresh", "The latest reading is within 15 minutes."),
    "unknown": ("Freshness unknown", "The age of the latest reading cannot be shown."),
}


def freshness_state(view: Mapping[str, Any]) -> str:
    if view.get("state") in ("consent-withheld", "unavailable"):
        return "unavailable"
    if view.get("state") == "no-readings" or not view.get("latest"):
        return "offline"
    freshness = view.get("freshness")
    return str(freshness) if freshness in ("fresh", "stale") else "unknown"


def badges(view: Mapping[str, Any]) -> list[dict[str, str]]:
    state = freshness_state(view)
    label, text = _FRESHNESS[state]
    return [
        dict(kind="freshness", state=state, label=label, text=text),
        dict(
            kind="calibration",
            state="uncalibrated",
            label="Uncalibrated",
            text="Not calibrated. Not a verified indoor measurement.",
        ),
    ]


def annotate(view: Mapping[str, Any]) -> dict[str, Any]:
    """The sensor response with text badges and advisory provenance added."""
    return dict(view, badges=badges(view), advisory=ADVISORY)
