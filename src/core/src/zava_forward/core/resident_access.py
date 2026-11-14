"""Resident journey alternatives and task-limited representative views (#154).

Pure functions over supplied records. Nothing here stores, sends or decides anything: it states
the non-digital route and needs each journey step must offer, and it projects what a
representative may currently see from recorded authority versions.
"""

from datetime import date
from typing import Any

# Needs a resident may state. They describe how to communicate, never capacity.
SUPPORT_NEEDS = (
    "Language or interpreter",
    "Easy Read or plain language",
    "Large print or other format",
    "Phone only",
    "Contact times",
    "Adjustment",
    "Representative contact",
    "Safe route needed",
)
NON_DIGITAL_CHANNELS = ("Phone", "Letter", "In person", "Trusted intermediary")
NO_INFERENCE = "A stated need changes how we communicate. It is never read as lack of capacity."

JOURNEY_ALTERNATIVES = {
    "J1": (
        "Read the same version on a safe call or visit with accessible paper. "
        "Silence is not consent."
    ),
    "J2": "Pause or withdraw by phone, letter or visit. Your other choices have not changed.",
    "J3": "Compare appointment offers by phone, letter or visit. Offers are not bookings.",
    "J4": "Hear the update owner, date and basis aloud or on safe paper.",
    "J5": "Take a home demonstration and printed instructions. Declining practice changes nothing.",
    "J6": "Raise a complaint or challenge by phone, letter or visit with read-back.",
    "R1": "Staff check current permissions privately before each call or visit.",
}
DENIED = (
    "Authority could not be confirmed. "
    "A member of staff will review it through the safe contact route."
)


def step_alternative(code: str, needs: list[str] | None = None) -> dict[str, Any]:
    """Return the non-digital route for a journey step with the resident's stated needs."""
    if code not in JOURNEY_ALTERNATIVES:
        raise ValueError("Unknown journey step.")
    needs = list(needs or [])
    unknown = [n for n in needs if n not in SUPPORT_NEEDS]
    if unknown:
        raise ValueError("Choose needs from the list.")
    return dict(
        step=code,
        non_digital=JOURNEY_ALTERNATIVES[code],
        channels=list(NON_DIGITAL_CHANNELS),
        needs=needs,
        note=NO_INFERENCE,
        capacity_inferred=False,
    )


def representative_view(
    versions: list[dict[str, Any]] | None, today: str | None = None
) -> dict[str, Any]:
    """Show only the current version's tasks while confirmed and before its review date."""
    today = today or date.today().isoformat()
    current = (versions or [None])[-1]
    if not current or current.get("status") != "Confirmed":
        return dict(allowed=False, tasks=[], message=DENIED)
    start, review = current.get("authority_date"), current.get("review_date")
    if not (isinstance(start, str) and isinstance(review, str) and start <= today < review):
        return dict(allowed=False, tasks=[], message=DENIED)
    return dict(
        allowed=True,
        tasks=sorted(current.get("tasks", [])),
        measure=current.get("measure"),
        unavailable_from=review,
        message=f"Authority covers only these tasks and is unavailable from {review}.",
    )
