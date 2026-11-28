"""Per-task data contracts, enforced before a prompt is built (Refs #121, #2311).

Each registered AI task declares its purpose, audience, the permitted field
names with type and length, the content that must never reach a prompt, and a
minimum-necessary rationale. A prompt build with an undeclared field, a wrong
type, an over-long value or prohibited content is refused with a plain message
and no value echoed.

A person's permission to see or use data never satisfies a contract: the
contract limits what the task may receive, whoever asks. This module records
the engineering control only. It does not claim DPO or Legal approval, which
stays under #121.
"""

import re
from collections.abc import Mapping
from typing import Any

CONTRACT_VERSION = "2026-11-23.1"
NOT_CLAIMED = "DPO and Legal approval is not claimed; it stays under #121."


class ContractRefusal(ValueError):
    """A prompt build that the task's data contract does not allow."""


PROHIBITED = {
    "email address": re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"),
    "telephone number": re.compile(r"(?<![\w+])(?:\+44|0044|0)[\s-]?\d(?:[\s-]?\d){8,10}(?!\w)"),
    "national insurance number": re.compile(
        r"\b[A-CEGHJ-PR-TW-Z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-D]\b", re.I
    ),
    "bank details": re.compile(r"\b\d{2}-\d{2}-\d{2}\b|\b[A-Z]{2}\d{2}(?:\s?[A-Z0-9]{4}){3,7}\b"),
    "payment card number": re.compile(r"\b(?:\d[ -]?){15}\d\b"),
}
PROHIBITED_NAMES = tuple(PROHIBITED)

_SHORT: tuple[str, int] = ("str", 255)


def _contract(
    purpose: str, audience: str, fields: dict[str, tuple[str, int]], rationale: str
) -> dict[str, Any]:
    return dict(
        version=CONTRACT_VERSION,
        purpose=purpose,
        audience=audience,
        fields={k: dict(type=t, max_length=n) for k, (t, n) in fields.items()},
        prohibited_content=list(PROHIBITED_NAMES),
        minimum_necessary=rationale,
        permission_note="A user's permission does not widen this contract.",
        approval_claim=NOT_CLAIMED,
    )


def _assistant(purpose: str, audience: str, rationale: str) -> dict[str, Any]:
    return _contract(
        purpose, audience, dict(case_id=("str", 64), source_snapshot=("str", 40000)), rationale
    )


CONTRACTS = {
    "briefing": _contract(
        "Draft a morning briefing for a housing officer",
        "Retrofit Coordinator, Resident Liaison Officer",
        dict(facts=("str", 30000)),
        "Stage, wait and safety facts only; no contact detail or free-text notes are needed.",
    ),
    "message": _contract(
        "Draft a resident visit or update message",
        "Retrofit Coordinator, Resident Liaison Officer",
        dict(owner=("str", 120), facts=("str", 8000)),
        "Officer name and the case facts the message needs; a person sends it.",
    ),
    "summary": _contract(
        "Catch-me-up summary for a colleague taking over a case",
        "Retrofit Coordinator, Resident Liaison Officer",
        dict(owner=("str", 120), facts=("str", 8000)),
        "Case stage, history and contacts for one case; nothing from other cases.",
    ),
    "priority": _contract(
        "Explain a suggested order of work for a person to accept or reject",
        "Retrofit Coordinator, Retrofit Programme Manager",
        dict(n=("int", 50), facts=("str", 60000)),
        "Ranking and safety facts per listed case; ranking and queue membership are not changed.",
    ),
    "funding_draft": _contract(
        "Draft funding application wording",
        "Grants and Evidence Officer, Retrofit Programme Manager",
        dict(route=("str", 120), facts=("str", 8000), missing=("str", 2000)),
        "Measures, funding route and missing documents; no eligibility decision or contact detail.",
    ),
    "read_document": _contract(
        "Describe an uploaded document",
        "Retrofit Coordinator, Grants and Evidence Officer, Quality Inspector",
        dict(name=_SHORT),
        "File name only reaches the template; content has its own hold.",
    ),
    "stock-prioritisation": _assistant(
        "Propose stock prioritisation for a person to verify",
        "Retrofit Coordinator",
        "Home, survey and ranking facts for one case.",
    ),
    "assessment-preparation": _assistant(
        "Propose assessment preparation notes",
        "Retrofit Coordinator",
        "Home, survey, measures, technical and document facts for one case.",
    ),
    "funding-evidence": _assistant(
        "Propose funding evidence checks",
        "Grants and Evidence Officer",
        "Home, measures, funding, finance, grant and document facts for one case.",
    ),
    "works-resident-coordination": _assistant(
        "Propose works and resident coordination follow-ups",
        "Retrofit Coordinator, Resident Liaison Officer",
        "Handoff, appointment and service request facts for one case.",
    ),
    "quality-evidence": _assistant(
        "Propose quality evidence review flags",
        "Quality Inspector",
        "Quality, checklist and consented reading facts for one case.",
    ),
    "chat-case-conversation": _contract(
        "Answer questions about a case with cited sources",
        "Retrofit Coordinator, Retrofit Programme Manager",
        dict(question=("str", 2000), case_facts=("str", 30000)),
        "The question and the cited case facts for one case.",
    ),
    "aftercare-concern-pack": _contract(
        "Draft an optional aftercare concern pack for the named owner",
        "Retrofit Coordinator, Retrofit Programme Manager",
        dict(concern_id=("str", 64), facts=("str", 8000)),
        "Home, request and history facts for one concern; a sensor reading is never a basis.",
    ),
}


def get(task_id: str) -> dict[str, Any] | None:
    return CONTRACTS.get(task_id) if isinstance(task_id, str) else None


def prohibited_in(task_id: str, *texts: object) -> str | None:
    """Label of the first prohibited content in a contracted task's final prompt text, else None."""
    contract = get(task_id)
    if contract is None:
        return None
    for text in texts:
        if isinstance(text, str):
            for label, pattern in PROHIBITED.items():
                if label in contract["prohibited_content"] and pattern.search(text):
                    return label
    return None


def enforce(task_id: str, values: Mapping[str, object], *, user_permission: bool = False) -> None:
    """Refuse before a prompt is built. user_permission is accepted and deliberately ignored."""
    contract = get(task_id)
    if contract is None:
        raise ContractRefusal("This AI feature has no data contract. Use the manual route.")
    allowed = contract["fields"]
    extra = sorted(set(values) - set(allowed))
    if extra:
        raise ContractRefusal(
            f"Field not declared in the {task_id} data contract: {', '.join(map(str, extra))}."
        )
    for name, value in values.items():
        spec = allowed[name]
        if spec["type"] == "int":
            if type(value) is not int or not 1 <= value <= spec["max_length"]:
                raise ContractRefusal(
                    f"Field {name} must be a whole number from 1 to {spec['max_length']}."
                )
            continue
        if not isinstance(value, str):
            raise ContractRefusal(f"Field {name} must be text.")
        if len(value) > spec["max_length"]:
            raise ContractRefusal(f"Field {name} is longer than {spec['max_length']} characters.")
        for label, pattern in PROHIBITED.items():
            if label in contract["prohibited_content"] and pattern.search(value):
                raise ContractRefusal(
                    f"Field {name} holds prohibited content ({label}); it is not sent to AI."
                )
