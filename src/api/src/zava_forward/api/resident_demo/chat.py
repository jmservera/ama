"""Host-owned routing and dated explanations; raw resident questions never reach AI."""

import re
from typing import Any

from zava_forward.core.resident_assistant import Advice, Topic

from .agenda import MANUAL, NOTICE

REGULATORY_SOURCE = (
    "docs/reference/regulatory/social-housing-regulation/"
    "social-housing-safety-and-quality-standard-2024.md; "
    "Safety and Quality Standard, sections 2.3.1, 2.3.2 and 2.3.3; "
    "regulatory standard; source date 2024-04-01; retrieved 2026-09-19."
    " Selected provisions checked against https://www.gov.uk/government/publications/"
    "safety-and-quality-standard on 2026-10-28."
)
REGULATORY_ANSWER = (
    "The local copy of the Safety and Quality Standard says providers must make it easy to "
    "report repairs, tell tenants repair timescales and keep tenants informed about work. "
    "This is an explanation of a dated local copy, not legal advice. "
    "These selected provisions match the official publication checked on 2026-10-28. "
    "Currentness has not been verified for the wider rules. "
    "Other rules or later changes may apply. "
    "I cannot decide that a legal duty is met, that your home is safe, or that a provider "
    "has complied. Ask your housing officer to arrange a qualified legal or compliance review."
)
SAFETY = (
    "Do not wait for chat or a callback if someone may be in danger. "
    "For an immediate emergency, call 999. Report damp, mould or another safety concern "
    "to your housing officer or emergency repairs service using your usual contact details. "
    "A person must handle safety reports. This chat has not sent a report or alerted anyone."
)


def route(question: str) -> Topic | str:
    words = set(re.findall(r"[a-z]+", question.lower()))
    if words & {"danger", "unsafe", "hazard", "safety", "mould", "mold", "damp", "fire", "gas"}:
        return "safety"
    if words & {
        "ignore",
        "instructions",
        "system",
        "prompt",
        "another",
        "other",
        "neighbour",
        "neighbor",
        "approve",
        "diagnose",
        "decide",
        "submit",
        "book",
        "cancel",
    }:
        return "unknown"
    if words & {"documents", "document", "paperwork"}:
        return Topic.DOCUMENTS
    if "send" in words:
        return "unknown"
    if words & {"law", "laws", "legal", "regulation", "regulations", "rules", "compliant", "duty"}:
        return "regulations"
    if words & {"appointment", "appointments", "callback", "agenda", "slots"}:
        return "appointments"
    if words & {"consent", "consents", "permission"}:
        return "consents"
    if words & {"home", "address", "improvements"}:
        return "home"
    if words & {"status", "case", "progress"}:
        return Topic.STATUS
    if words & {"form", "forms"}:
        return Topic.FORMS
    return "unknown"


def answer(topic: str, view: dict[str, Any]) -> Advice:
    sources: tuple[str, ...]
    if topic == "home":
        home = view["home"]
        answer = (
            "Your recorded home: "
            + ", ".join(home[k] for k in ("address", "town", "postcode") if home[k])
            + ". Planned improvements: "
            + (", ".join(view["measures"]) if view["measures"] else "not recorded")
            + "."
        )
        sources = ("Your signed-in home record and planned improvements",)
    elif topic == "consents":
        answer = (
            "Works consent is not available in this showcase. I cannot say whether you have "
            "given consent. Agreeing to use your record in chat is not consent to works. "
            "Ask your housing officer to check your consent record."
        )
        sources = ("Showcase limit: operational consent records are not available",)
    elif topic == "appointments":
        answer = (
            NOTICE + " Use Find callback times below to search the local agenda. "
            "You choose a time and confirm before anything is reserved. " + MANUAL
        )
        sources = ("Local synthetic callback agenda, not operational appointment history",)
    elif topic == "regulations":
        answer, sources = REGULATORY_ANSWER, (REGULATORY_SOURCE,)
    elif topic == "safety":
        answer, sources = SAFETY, ("Human emergency and repairs route, not a safety assessment",)
    else:
        answer = (
            "I cannot answer that or act on instructions in a message. "
            "Ask about your case, home, documents, forms, consent, appointments or rules. "
            "I cannot approve, decide, diagnose, give consent, book from chat text or "
            "access anyone else's record. A person can help through your housing officer."
        )
        sources = ("Assistant task limits",)
    return Advice(answer, sources, "Summary by rules - workflow only, no AI used")
