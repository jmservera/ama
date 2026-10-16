"""Offline extractive regulatory answers. Data in, text out; no tools or store access."""

from __future__ import annotations

import re
from typing import Any

from zava_forward.core.chat_panel import normalise_policy_text, out_of_scope

OWNER = "Juan Manuel Servera"
LABEL = "synthetic-demo | source excerpts, not legal advice or approval"
SCHEMA = "regulatory-chat-v1"
LEGAL = re.compile(
    r"\b(?:compliant|compliance|lawful|legal|liab\w*|interpret\w*|must|should|"
    r"lease\w*|grant\w*|contract\w*|certif\w*|breach\w*|deadline\w*|"
    r"can\s+(?:we|i)|are\s+we\s+allowed|does\s+.+\s+apply)\b",
    re.I,
)
PURPOSES = {
    "hazard-awareness-clock": re.compile(r"\b(?:hazard|damp|mould|emergency|awareness)\b"),
    "automated-decision-safeguard": re.compile(
        r"\b(?:automated|automation|algorithm|human review)\b"
    ),
}
LOOKUP_WORDS = frozenset(
    "what do does the sources source say for this home show and recorded facts are is "
    "hazard hazards damp mould emergency awareness automated decision decisions automation "
    "algorithm human review provision provisions reference references please me about our "
    "case lookup look up cited citation citations card cards explain summarise summarize".split()
)
SOURCE_WORDS = frozenset(
    (
        "source sources provision provisions reference references "
        "cited citation citations card cards"
    ).split()
)


def purpose(question: str) -> str | None:
    text = normalise_policy_text(question).lower()
    matches = [key for key, pattern in PURPOSES.items() if pattern.search(text)]
    return matches[0] if len(matches) == 1 else None


def refusal(question: str) -> str | None:
    text = normalise_policy_text(question)
    if out_of_scope(text) or LEGAL.search(text):
        return "This question needs a human decision or legal interpretation."
    if purpose(text) is None:
        return "No supported, cited source lookup is available for this question."
    words = set(re.findall(r"[a-z0-9]+", text.lower()))
    if not words & SOURCE_WORDS or words - LOOKUP_WORDS:
        return (
            "This offline slice supports only source lookup and recorded home facts. "
            "Ask 'What do the hazard sources say for this home?' or ask the named owner."
        )
    return None


def answer(bundle: dict[str, Any]) -> dict[str, Any]:
    """Render only server-selected evidence, never generate assertions from user/source text."""
    sources = bundle["sources"]
    reason = bundle.get("refusal")
    if not sources and not reason:
        reason = "No approved synthetic card with an eligible cited provision supports an answer."
    conflict = bool(bundle.get("conflict"))
    kind = "refused" if reason else "conflict" if conflict else "answer"
    sections: dict[str, Any] = {
        "what_sources_say": []
        if reason
        else [{"citation": s["id"], "quote": s["text"]} for s in sources],
        "recorded_home_facts": [] if reason else bundle["facts"],
        "unknown_or_missing": [
            reason or "Legal applicability and satisfaction of any duty are not assessed."
        ],
        "safe_next_action": (
            "Potential source conflict: ask the named owner to compare both; "
            "do not resolve it here."
            if conflict
            else "Use the independent human emergency or hazard route for safety concerns. "
            "Ask the named owner if in doubt."
        ),
        "who_decides": f"{OWNER}, exercise Legal, Compliance and DPO owner (synthetic-demo).",
    }
    if conflict:
        sections["unknown_or_missing"].append(
            "The retrieved card instructions or source versions disagree; human review is required."
        )
    if bundle.get("unknown"):
        sections["unknown_or_missing"].append(bundle["unknown"])
    citations = [] if reason else sources + bundle["facts"]
    lines = [
        LABEL,
        "What the sources say:",
        *[f"Quoted source [{s['citation']}]: {s['quote']}" for s in sections["what_sources_say"]],
        "Recorded facts for this home (not a finding of legal applicability):",
        *[f"[{f['id']}] {f['text']}" for f in sections["recorded_home_facts"]],
        "Unknown or missing: " + " ".join(sections["unknown_or_missing"]),
        "Safe next action: " + sections["safe_next_action"],
        "Who decides: " + sections["who_decides"],
    ]
    return dict(
        schema=SCHEMA,
        kind=kind,
        label=LABEL,
        model="offline-extractive",
        reply="\n".join(lines),
        sections=sections,
        citations=citations,
        owner=OWNER,
        requires_human=kind != "answer",
        workflow_only=True,
        cards=bundle["cards"],
        as_of=bundle["as_of"],
    )
