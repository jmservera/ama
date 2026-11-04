"""Deterministic, rules-based resident case summary pieces for the synthetic showcase (#462).

Pure functions over already allowlisted facts. Nothing here calls AI, reads a store or decides
anything: it only restates recorded stage, document and measure facts in plain language.
"""

from typing import Any

from .resident_documents import SCAN_TEXT, DocumentFacts

RULES_LABEL = "Summary by rules. Not an instruction."
STEPS = (
    "Survey",
    "Assessment and design",
    "Resident agreement",
    "Funding and final checks",
    "Installation works",
    "Quality and handover",
)
STAGE_STEP = {
    "Home identified": 0,
    "Checking lease": 0,
    "Rescheduled": 0,
    "Contacting resident": 0,
    "Contact paused": 0,
    "Survey being booked": 0,
    "Survey booked": 0,
    "Survey write-up": 0,
    "Design starting": 1,
    "Design in progress": 1,
    "Design awaiting approval": 1,
    "Design being corrected": 1,
    "Waiting on other works": 1,
    "Waiting for resident decision": 2,
    "Resident paused works": 2,
    "Funding check": 3,
    "Final checks before ordering": 3,
    "Waiting for block programme": 3,
    "With contractor": 4,
    "Install booked": 4,
    "Works under way": 4,
    "Handover to arrange": 5,
    "Quality check": 5,
    "Closing down": 5,
    "Aftercare issue": 5,
}
SOURCES = (
    ("Current status and next step", "#sec-status"),
    ("What is needed from you", "#sec-actions"),
    ("Case timeline and planned improvements", "#sec-timeline"),
    ("Documents and checks", "#sec-documents"),
)


def timeline(stage: str, closed: bool) -> list[dict[str, str]]:
    """Six programme steps with a state each. An unknown stage marks no step as current."""
    current = STAGE_STEP.get(stage)
    steps = []
    for index, name in enumerate(STEPS):
        if closed:
            state = "completed"
        elif current is None:
            state = "unknown"
        elif index < current:
            state = "completed"
        elif index == current:
            state = "current"
        else:
            state = "upcoming"
        steps.append({"name": name, "state": state})
    return steps


def _request_state(facts: DocumentFacts, kind: str) -> str:
    if facts.documents is None:
        return "unknown"
    return (
        "provided"
        if any(d.kind == kind and not d.generated for d in facts.documents)
        else "missing"
    )


REQUEST_LABEL = {
    "unknown": "Whether a document has been provided is unknown",
    "provided": "A presented document is recorded. Staff still need to check it",
    "missing": "Missing from the presented documents in this view",
}


def documents_view(facts: DocumentFacts) -> dict[str, Any]:
    requests = None
    if facts.requests is not None:
        requests = []
        for r in facts.requests:
            state = _request_state(facts, r.kind)
            requests.append(
                {
                    "id": r.id,
                    "kind": r.kind,
                    "state": state,
                    "state_label": REQUEST_LABEL[state],
                    "how_to_provide": r.how_to_provide,
                }
            )
    presented = None
    if facts.documents is not None:
        presented = []
        for d in facts.documents:
            presented.append(
                {
                    "id": d.id,
                    "kind": d.kind,
                    "generated": d.generated,
                    "status_label": (
                        "A generated placeholder, not a presented document"
                        if d.generated
                        else "Recorded as presented, not accepted or approved"
                    ),
                    "scan_status": d.scan_status or "unknown",
                    "scan_label": SCAN_TEXT.get(
                        d.scan_status or "",
                        "The file check result is unknown in this view. Ask staff to check it.",
                    ),
                    "issues": (
                        None
                        if d.issues is None
                        else [{"severity": i.severity, "message": i.message} for i in d.issues]
                    ),
                }
            )
    return {"requests": requests, "presented": presented}


def needed_from_you(stage: str, closed: bool, documents: dict[str, Any]) -> list[dict[str, str]]:
    """Recorded items that wait on the resident. An empty list means nothing is recorded."""
    items: list[dict[str, str]] = []
    if not closed and stage == "Waiting for resident decision":
        items.append(
            {
                "kind": "decision",
                "text": (
                    "We are waiting for your decision on your planned improvements. "
                    "Reason: works cannot move on until you tell a person your choice. "
                    "Owner: your housing officer. Next action: speak to your housing officer "
                    "using the help options below. This showcase cannot record decisions."
                ),
            }
        )
    for request in documents["requests"] or []:
        if request["state"] == "missing":
            items.append(
                {
                    "kind": "document",
                    "text": (
                        f"Document request {request['id']} ({request['kind']}): "
                        f"{request['state_label']}. How to provide it: {request['how_to_provide']}"
                    ),
                }
            )
    for document in documents["presented"] or []:
        if document["scan_status"] in ("pending", "infected", "mismatch"):
            items.append(
                {
                    "kind": "document",
                    "text": (
                        f"Document {document['id']} ({document['kind']}): {document['scan_label']}"
                    ),
                }
            )
    return items


def _plural(n: int, noun: str) -> str:
    return f"{n} {noun}" if n == 1 else f"{n} {noun}s"


def rules_summary(
    address: str,
    stage: str,
    progress: str,
    next_step: str,
    closed: bool,
    measures: list[str],
    documents: dict[str, Any],
    needed: list[dict[str, str]],
) -> dict[str, Any]:
    where = address or "your home"
    parts = [
        f"Your home at {where} is at the {stage} stage." if stage else f"Your home at {where}."
    ]
    parts.append(progress)
    if closed:
        parts.append("This case is recorded as closed.")
    else:
        parts.append(f"Next step: {next_step}")
    parts.append(f"Planned improvements: {', '.join(measures) if measures else 'none listed'}.")
    requests = documents["requests"]
    if requests is None:
        parts.append("Document requests are not shown in this view.")
    elif not requests:
        parts.append("Documents: no document requests recorded.")
    else:
        waiting = sum(1 for r in requests if r["state"] == "missing")
        parts.append(
            f"Documents: {_plural(len(requests), 'request')} recorded, "
            f"{waiting} missing in this view."
        )
    parts.append(
        f"{_plural(len(needed), 'item')} may need your attention."
        if needed
        else "Nothing is recorded as needed from you right now."
    )
    return {
        "label": RULES_LABEL,
        "text": " ".join(parts),
        "sources": [{"label": label, "href": href} for label, href in SOURCES],
    }
