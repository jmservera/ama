"""Synthetic AI-state fixture and expected text for the data-operator register check (#229).

Playwright-free so unit tests can use it. All values are constructed synthetic text: they
do not show a serving model, employee effectiveness, accessibility acceptance, resident
consent or named approval.
"""

from __future__ import annotations

import json
from typing import Any

OPERATOR_EMAIL = "pam@example.test"
STAFF_ENV = {"ZF_EXCEPTION_STAFF": json.dumps({OPERATOR_EMAIL: ["data_steward", "digital_operator"]})}

QUARANTINED_ID = "SYN-AI-QUARANTINED"
FALLBACK_ID = "SYN-AI-FALLBACK"
WORKFLOW_ID = "SYN-AI-WORKFLOW"
QUARANTINED_REASON = "SYN late result quarantined"
FALLBACK_REASON = "SYN model timeout"

NOT_A_MODEL_RESULT = "Requested AI help did not deliver a model result."
# Kind column label for failed_ai_run in role-screens.js; it does not depend on the outcome text.
FAILED_AI_KIND = "Requested AI help did not deliver a model result"
KIND_COLUMN = 1
HAPPENED_COLUMN = 4
QUARANTINED_TEXT = f"Quarantined. {NOT_A_MODEL_RESULT} Reason: {QUARANTINED_REASON}"
FALLBACK_TEXT = f"Fell back to rules or template. {NOT_A_MODEL_RESULT} Reason: {FALLBACK_REASON}"



def failed_ai_rows(rows: list[list[str]]) -> list[list[str]]:
    """Rows of the Items table whose Kind cell is the failed-AI label."""
    return [row for row in rows if len(row) > HAPPENED_COLUMN and row[KIND_COLUMN].strip() == FAILED_AI_KIND]


def says_failure_outcome(happened: str) -> bool:
    """True when a What happened cell starts with Quarantined or Fell back and is not a model result."""
    return any(happened.startswith(f"{lead} {NOT_A_MODEL_RESULT}")
               for lead in ("Quarantined.", "Fell back to rules or template."))


REGISTER_EXPECTED = (
    "Read-only list returned by the server for your signed-in access.",
    "no AI call is made",
    "Recovery guidance below is placeholder text, not an approved runbook.",
    "Recovery is a recorded human request made elsewhere; nothing is replayed.",
    "Deliberate rules-and-template processing (workflow-only) is not a failure and is not a model result.",
    "It is never listed here, so an empty list does not show that a model succeeded",
    "Service state Unknown",
    "No service health check feeds this register, so service state is Unknown.",
    "Failed imports are not connected to this register yet",
    "Placeholder guidance, not an approved runbook",
    "from configuration, not an appointment",
)
CONFLICT_EXPECTED = (
    "Source conflicts with every returned value",
    "No winning source is selected.",
)
REGISTER_FORBIDDEN = ("No outage recorded", "audit trail", "audit history", WORKFLOW_ID)
UNAVAILABLE_TEXT = (
    "The exception register could not be shown, so nothing is known about open exceptions. "
    "Do not read this as all clear."
)
EMPTY_TEXT = "No exception items were returned. This is not an all clear"
REGISTER_TABLES = (
    "Exception items returned for you",
    "Source conflicts with every returned value",
)

# Constructed empty contract for an intercepted GET, shaped like exception_register output.
EMPTY_CONTRACT: dict[str, Any] = {
    "state": "ok",
    "items": [],
    "unrouted": [],
    "sources": [],
    "banner": {
        "state": "unknown",
        "text": "Service state has not been checked recently. Do not assume it is healthy.",
        "components": {},
        "last_checked": None,
    },
    "access": {"roles": {OPERATOR_EMAIL: ["digital_operator"]}, "scope": {}},
    "note": "Read-only. Recovery is a recorded human request made elsewhere; nothing is replayed.",
}


def ai_records() -> list[dict[str, Any]]:
    """Quarantined, fallback and deliberate workflow-only AI task records."""
    base = {"kind": "ai_task", "task": "briefing", "created": "2026-11-01"}
    return [
        dict(base, id=QUARANTINED_ID, mode="ai", source="template", status="Quarantined",
             fallback_reason=QUARANTINED_REASON),
        dict(base, id=FALLBACK_ID, mode="ai", source="template", status="Not reviewed",
             fallback_reason=FALLBACK_REASON),
        dict(base, id=WORKFLOW_ID, mode="workflow", source="template", status="Not reviewed"),
    ]


def add_ai_records(data: dict[str, Any]) -> dict[str, Any]:
    data.setdefault("recommendations", []).extend(ai_records())
    return data
