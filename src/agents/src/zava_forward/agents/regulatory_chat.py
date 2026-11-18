"""Offline extractive regulatory answers. Data in, text out; no tools or store access."""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

from zava_forward.core.chat_panel import normalise_policy_text, out_of_scope
from zava_forward.core.regulatory_output_guard import (
    ADVISORY_REVIEW_TEXT,
    GuardDecision,
    ViolationCategory,
    advisory_review_summary,
    inspect_regulatory_output,
)

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


_ELIGIBLE_ANSWER_STATUSES = frozenset({"in_force", "guidance", "recorded-synthetic-demo"})
_INACTIVE_CARD_STATUSES = frozenset({"draft", "retired", "rejected", "superseded"})


def _bundle_answer_activated(bundle: Mapping[str, Any]) -> tuple[bool, str | None]:
    as_of_raw = bundle.get("as_of")
    as_of_day = as_of_raw[:10] if isinstance(as_of_raw, str) and len(as_of_raw) >= 10 else None
    sources = bundle.get("sources")
    if not isinstance(sources, list) or not sources:
        return False, None
    first_sid: str | None = None
    for src in sources:
        if not isinstance(src, Mapping):
            return False, first_sid
        sid = str(src["id"]) if isinstance(src.get("id"), str) and src.get("id") else None
        if first_sid is None:
            first_sid = sid
        if src.get("status") not in _ELIGIBLE_ANSWER_STATUSES:
            return False, sid
        if src.get("review_status") in ("not_reviewed", "historical"):
            return False, sid
        eff = src.get("effective")
        if isinstance(eff, str) and eff and as_of_day is not None and eff > as_of_day:
            return False, sid
    cards = bundle.get("cards")
    if not isinstance(cards, list) or not cards:
        return False, first_sid
    for card in cards:
        if not isinstance(card, Mapping):
            return False, first_sid
        card_state = str(card.get("status") or card.get("state") or "").strip().lower()
        if card_state in _INACTIVE_CARD_STATUSES:
            return False, first_sid
        if card.get("active") is False or card.get("approved") is False:
            return False, first_sid
        if "approved_by" in card and not str(card.get("approved_by") or "").strip():
            return False, first_sid
        card_eff = card.get("effective")
        if (
            isinstance(card_eff, str)
            and card_eff
            and as_of_day is not None
            and card_eff > as_of_day
        ):
            return False, first_sid
    return True, None


def _format_reply_lines(sections: Mapping[str, Any]) -> list[str]:
    return [
        LABEL,
        "What the sources say:",
        *[f"Quoted source [{s['citation']}]: {s['quote']}" for s in sections["what_sources_say"]],
        "Recorded facts for this home (not a finding of legal applicability):",
        *[f"[{f['id']}] {f['text']}" for f in sections["recorded_home_facts"]],
        "Unknown or missing: " + " ".join(sections["unknown_or_missing"]),
        "Safe next action: " + str(sections["safe_next_action"]),
        "Who decides: " + str(sections["who_decides"]),
    ]


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

    violations: list[ViolationCategory] = []
    reasons: list[str] = []
    if kind == "answer":
        activated, offending_sid = _bundle_answer_activated(bundle)
        if not activated:
            violations.append("future_law_applied_as_active")
            reasons.append(f"unactivated_answer:{offending_sid or 'bundle'}")
            kind = "refused"
            citations = []
            sections["what_sources_say"] = []
            sections["recorded_home_facts"] = []
            sections["unknown_or_missing"] = [
                advisory_review_summary(
                    source_id=offending_sid,
                    human_rule_activated=False,
                )
            ]

    rewritten_unknowns: list[str] = []
    for item in sections["unknown_or_missing"]:
        dec = inspect_regulatory_output(str(item), on_violation="rewrite")
        if not dec.passed:
            for v in dec.violations:
                if v not in violations:
                    violations.append(v)
            for r in dec.reasons:
                if r not in reasons:
                    reasons.append(r)
            rewritten_unknowns.append(dec.rewritten_text or ADVISORY_REVIEW_TEXT)
            kind = "refused"
            citations = []
            sections["what_sources_say"] = []
            sections["recorded_home_facts"] = []
        else:
            rewritten_unknowns.append(str(item))
    sections["unknown_or_missing"] = rewritten_unknowns

    for section_key in ("safe_next_action", "who_decides"):
        dec = inspect_regulatory_output(str(sections[section_key]), on_violation="rewrite")
        if not dec.passed:
            for v in dec.violations:
                if v not in violations:
                    violations.append(v)
            for r in dec.reasons:
                if r not in reasons:
                    reasons.append(r)
            sections[section_key] = dec.rewritten_text or ADVISORY_REVIEW_TEXT
            kind = "refused"
            citations = []
            sections["what_sources_say"] = []
            sections["recorded_home_facts"] = []

    lines = _format_reply_lines(sections)
    guard_decision = (
        GuardDecision(
            checked=True,
            passed=False,
            action="rewritten",
            violations=tuple(violations),
            reasons=tuple(reasons),
            rewritten_text=None,
        )
        if violations
        else GuardDecision(
            checked=True,
            passed=True,
            action="passed",
            violations=(),
            reasons=(),
            rewritten_text=None,
        )
    )
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
        output_guard=guard_decision.to_status_dict(),
    )
