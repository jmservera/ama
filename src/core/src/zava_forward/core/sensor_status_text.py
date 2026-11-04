"""Plain-language status text for sensor signals, one source for map and list (issue 111, AC-067).

Pure and read-only. The same text feeds the map status and the accessible list, so the list always
mirrors the map and never relies on colour alone. The text carries no reading, device identifier,
diagnosis or priority change; every state names the manual route that stays available.
"""

from collections.abc import Sequence
from dataclasses import dataclass

from .sensor_analysis import DECLINED, INSUFFICIENT, REVIEW, STALE, SUFFICIENT, Signal

MANUAL_ROUTE = "You can still ask for a home check in the usual way."
_NO_EFFECT = "This does not change your repairs or your place in any queue."

_TEXT = {
    "review": (
        "Check suggested",
        "Humidity stayed high for a while. A person may check the home. "
        "This is not a finding of damp or mould.",
    ),
    "normal": ("No concern seen", "Humidity looked normal in this period."),
    "declined": (
        "Monitoring is off",
        "Monitoring is switched off for this home, so no reading is used.",
    ),
    "stale": (
        "Readings are out of date",
        "We have no recent readings, so we cannot say how the home is.",
    ),
    "insufficient": (
        "Not enough readings",
        "There are not enough readings to say how the home is.",
    ),
}


@dataclass(frozen=True)
class StatusText:
    """Status shown identically on the map and in the list; text is the non-colour signal."""

    home_id: str
    state: str
    label: str
    text: str


def status_text(signal: Signal) -> StatusText:
    """Map a signal to its status text; anything not clearly sufficient reads as unknown."""
    if signal.sufficiency == DECLINED:
        key = "declined"
    elif signal.sufficiency == STALE:
        key = "stale"
    elif signal.sufficiency != SUFFICIENT or signal.outcome == INSUFFICIENT:
        key = "insufficient"
    elif signal.outcome == REVIEW:
        key = "review"
    else:
        key = "normal"
    label, body = _TEXT[key]
    return StatusText(signal.home_id, key, label, f"{body} {_NO_EFFECT} {MANUAL_ROUTE}")


def map_and_list(signals: Sequence[Signal]) -> tuple[list[StatusText], list[StatusText]]:
    """Return map statuses and the accessible list built from the same entries, same order."""
    entries = sorted((status_text(s) for s in signals), key=lambda e: e.home_id)
    return list(entries), list(entries)
