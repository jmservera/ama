"""Current-page CSV summary of the resident-choice queue.

One row per home the store returned for this page. Only closed vocabularies, integers and the
home id are written: no notes, identities, scope text, contact, address, purpose, owner, due
date or history. Missing or malformed evidence is stated as unknown, never as an absence,
consent or readiness claim.
"""

import csv
import io
from typing import Any

from zava_forward.core import quality
from zava_forward.core.list_export import safe_cell

FILENAME = "resident-choice-queue-page.csv"
FIELDS = (
    "Home reference",
    "Measure choices (latest recorded version)",
    "Paused, withdrawn or retained human review",
    "Update commitment status",
    "Homes skipped before this page",
    "Page size limit",
    "Homes in this file",
    "Open homes in total",
)
UNKNOWN = "Unknown"
UNAVAILABLE = "Unknown (evidence unavailable)"
WITHHELD = "Measure name withheld"
NO_CHOICES = "No measure choices recorded"
NONE_RECORDED = "None recorded"
NO_COMMITMENT = "No commitment recorded"
REVIEW = "Needs human review"
REVIEW_STATUSES = (REVIEW, "Reviewed with supplied acceptance")
STOP_STATUSES = ("Paused", "Withdrawn")
# "Not recorded" is accepted only because the projection supplies it for a current answer.
STATUSES = ("Waiting", "Accepted", "Declined", "Paused", "Withdrawn")
CURRENT_STATUSES = STATUSES + ("Not recorded",)
UPDATE_STATUSES = ("Outstanding", "Proposed")


def _status(value: Any, allowed: tuple[str, ...]) -> str:
    return value if isinstance(value, str) and value in allowed else UNKNOWN


def _int(value: Any) -> str:
    return str(value) if type(value) is int else UNKNOWN


def _name(value: Any) -> str:
    return value if isinstance(value, str) and value in quality.CHECKLISTS else WITHHELD


def _binding(version: dict[str, Any]) -> str:
    revision = _int(version.get("context_revision"))
    return f"revision {revision}, design {_int(version.get('design_version'))}"


def _version(version: dict[str, Any]) -> str:
    return f"v{version['version']}" if type(version.get("version")) is int else "version Unknown"


def _complete(measure: dict[str, Any]) -> bool:
    """A measure whose current status, version list and review can all be read."""
    review = measure.get("review")
    return (
        isinstance(measure.get("versions"), list)
        and all(isinstance(v, dict) and v.get("status") in STATUSES for v in measure["versions"])
        and (
            review is None or (isinstance(review, dict) and review.get("status") in REVIEW_STATUSES)
        )
    )


def _choice(measure: dict[str, Any]) -> str:
    name = _name(measure.get("measure"))
    current = _status(measure.get("status"), CURRENT_STATUSES)
    text = f"{name}: current {current}"
    versions = measure.get("versions")
    if not isinstance(versions, list) or not all(isinstance(v, dict) for v in versions):
        return f"{text}; latest recorded version {UNKNOWN}"
    if versions:
        latest = versions[-1]
        state = _status(latest.get("status"), STATUSES)
        text += f"; latest recorded {_version(latest)} {state} ({_binding(latest)})"
    return text


def _review_version(measure: dict[str, Any]) -> dict[str, Any] | None:
    review = measure.get("review")
    if not isinstance(review, dict) or review.get("status") != REVIEW:
        return None
    for version in measure["versions"]:
        if version.get("version") == review.get("decision_version"):
            found: dict[str, Any] = version
            return found
    return {}


def _held(measure: dict[str, Any]) -> str | None:
    """Return the stopped or review-retained summary for one measure, or None when there is none."""
    name = _name(measure.get("measure"))
    if not _complete(measure):
        return f"{name}: {UNAVAILABLE}"
    current = _status(measure.get("status"), CURRENT_STATUSES)
    held = _review_version(measure)
    if held is None:
        if current == UNKNOWN:
            return f"{name}: {UNAVAILABLE}"
        if current not in STOP_STATUSES:
            return None
        latest = measure["versions"][-1] if measure["versions"] else None
        return f"{name}: {current}" + (
            f" ({_version(latest)}, {_binding(latest)})" if latest else ""
        )
    status = _status(held.get("status"), STOP_STATUSES + ("Declined",))
    if status == UNKNOWN:
        return f"{name}: {UNAVAILABLE}, needs human review"
    state = status if status == current else f"{status} (current answer {current})"
    ending = (
        ", needs human review before any restart"
        if status in STOP_STATUSES
        else ", human review retained after a Declined answer"
    )
    return f"{name}: {state} ({_version(held)}, {_binding(held)}){ending}"


def _summaries(item: dict[str, Any]) -> tuple[str, str]:
    measures = item.get("measure_decisions")
    if not isinstance(measures, list) or not all(isinstance(m, dict) for m in measures):
        return UNAVAILABLE, UNAVAILABLE
    if not measures:
        return NO_CHOICES, NONE_RECORDED
    held = [h for h in map(_held, measures) if h]
    return "; ".join(map(_choice, measures)), "; ".join(held) if held else NONE_RECORDED


def _commitment(item: dict[str, Any]) -> str:
    if "resident_update" not in item:
        return UNKNOWN
    update = item["resident_update"]
    if update is None:
        return NO_COMMITMENT
    return _status(update.get("status"), UPDATE_STATUSES) if isinstance(update, dict) else UNKNOWN


def choice_queue_csv(page: dict[str, Any]) -> str:
    """Serialize the store result. Raises TypeError for a page that is not the expected shape."""
    items = page["items"]
    if not isinstance(items, list) or not all(isinstance(i, dict) for i in items):
        raise TypeError("items")
    context = [page[key] for key in ("offset", "limit")] + [len(items), page["total"]]
    if any(type(v) is not int for v in context):
        raise TypeError("page counts")
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(FIELDS)
    for item in items:
        home = item.get("id")
        choices, held = _summaries(item)
        writer.writerow(
            [
                safe_cell(v)
                for v in (
                    home if isinstance(home, str) and home else UNKNOWN,
                    choices,
                    held,
                    _commitment(item),
                    *context,
                )
            ]
        )
    return out.getvalue()
