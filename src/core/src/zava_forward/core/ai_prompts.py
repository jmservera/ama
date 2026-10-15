"""Canonical retained-task instructions shared by dispatch and release binding."""

import hashlib
import json

VERSION = "2026-10-15.2"
TEXT_SYSTEM = (
    "You assist a UK housing association retrofit team. Use only the facts given. "
    "Never invent dates, "
    "amounts, names or promises. Never say anything has been sent. "
    "Plain English, short, warm, no jargon."
)
PROMPTS = {
    "message": (
        TEXT_SYSTEM,
        "Draft a short letter or email from {owner} to the resident offering to arrange a visit or "
        "giving an update, respecting their adjustments and preferred contact. "
        "Sign off with the officer's name.\n\nFacts:\n{facts}",
    ),
    "summary": (
        TEXT_SYSTEM,
        "Catch up a colleague taking over this case in at most 5 short bullets: where it is, "
        "what is stuck, what to do next, anything about the resident they must know."
        "\n\nFacts:\n{facts}",
    ),
    "briefing": (
        "You write a friendly three-sentence morning briefing for a housing officer. "
        "Use only the facts. Safety issues first, then longest waits. No invented facts.",
        "{facts}",
    ),
    "priority": (
        "You advise a UK housing association retrofit officer which of their cases to work on "
        "first today. You only recommend; a person decides. Use only the facts given and "
        "only the case ids "
        "listed. Never invent facts. Reply with JSON only: a list of exactly {n} objects with keys "
        "case_id and reason (one short plain sentence citing a fact such as an open safety issue, "
        "extra support need, days waiting or a missing resident decision) and cites, a list of the "
        "facts it relies on copied exactly from that case's citable facts. "
        "Always include every case with an open safety issue.",
        "Pick the top {n}.\n\nCases:\n{facts}",
    ),
    "funding_draft": (
        "You draft the narrative part of a social housing retrofit funding application. "
        "Use only the facts given. Do not invent costs, eligibility results or evidence. "
        "Where something is missing write 'Needs: ...'. Headings: Property, Proposed work, "
        "Evidence held, Evidence still needed. "
        "Under 250 words.",
        "Route: {route}\n{facts}\nMissing documents: {missing}",
    ),
    "read_document": (
        "You help a housing association retrofit team file documents. Say what kind of document "
        "this is (for example EPC, survey, photo of damp, consent form, invoice), "
        "list the key facts "
        "you can see in at most six short bullet points, and flag anything unclear. "
        "Do not guess. Plain English.",
        "File name: {name}",
    ),
}
CITATION_RULE = (
    "\nAfter each claim add its source in double square brackets, ",
    "prefixed with the case id, for example [[CASE-ID: Stage: Survey booked]].",
    "for example [[Stage: Survey booked]].",
)


def render(task: str, **values: str | int) -> tuple[str, str]:
    system, user = PROMPTS[task]
    return system.format(**values), user.format(**values)


def version(task: str) -> str:
    body = json.dumps([VERSION, PROMPTS[task], CITATION_RULE], separators=(",", ":"))
    return hashlib.sha256(body.encode()).hexdigest()[:16]
