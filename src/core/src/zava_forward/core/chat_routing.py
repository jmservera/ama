"""Visible question routing for employee chat (issue #2195).

The general agent picks the specialist agent whose focus matches the question and says
so in plain language. Routing is deterministic: no model call, no stored state. It only
chooses which agent's evidence lens the existing chat path uses. A question that matches
no agent, matches two equally, or falls outside the user's role stays with the general agent.
"""

from __future__ import annotations

import re
from typing import Any

from zava_forward.core.assistants import REGISTRY

GENERAL = "general"
GENERAL_NAME = "General agent"

AGENT_NAMES = {
    "stock-prioritisation": "Stock prioritisation agent",
    "assessment-preparation": "Assessment preparation agent",
    "funding-evidence": "Funding evidence agent",
    "works-resident-coordination": "Works and resident coordination agent",
    "quality-evidence": "Quality evidence agent",
}

FOCUS = {
    "stock-prioritisation": "stock facts and which homes to look at first",
    "assessment-preparation": "survey and design evidence for an assessment",
    "funding-evidence": "grant, claim and funding evidence",
    "works-resident-coordination": "appointments and updates for residents",
    "quality-evidence": "quality checks and inspection evidence",
}

KEYWORDS = {
    "stock-prioritisation": (
        "stock",
        "epc",
        "ranking",
        "prioritise",
        "prioritisation",
        "archetype",
    ),
    "assessment-preparation": ("assessment", "survey", "design", "technical", "pas"),
    "funding-evidence": ("funding", "grant", "grants", "claim", "invoice", "budget", "milestone"),
    "works-resident-coordination": (
        "appointment",
        "appointments",
        "handoff",
        "capacity",
        "schedule",
        "access",
    ),
    "quality-evidence": (
        "quality",
        "inspection",
        "inspect",
        "defect",
        "defects",
        "acceptance",
        "sensor",
        "reading",
        "readings",
        "discrepancy",
    ),
}

_WORDS = re.compile(r"[a-z0-9]+")


def _result(agent: str, routed: bool, reason: str) -> dict[str, Any]:
    name = AGENT_NAMES.get(agent, GENERAL_NAME)
    head = f"Routed to the {name}" if routed else f"Handled by the {name}"
    return dict(
        agent=agent, agent_name=name, routed=routed, reason=reason, text=f"{head}. {reason}"
    )


def route_question(
    question: object, skill: object, role: object = None, *, refused: bool = False
) -> dict[str, Any]:
    """Routing decision for one question. Only the general skill is ever re-routed."""
    if isinstance(skill, str) and skill in REGISTRY:
        return _result(skill, False, "You chose this agent.")
    if refused:
        return _result(
            GENERAL,
            False,
            "No agent can do this. A person takes that action in the workflow.",
        )
    words = _WORDS.findall(str(question or "").lower())
    scores: dict[str, list[str]] = {}
    for agent, keys in KEYWORDS.items():
        hits = sorted({w for w in words if w in keys})
        if hits:
            scores[agent] = hits
    if not scores:
        return _result(
            GENERAL,
            False,
            "No specialist agent matches this question, so the general agent answers it.",
        )
    best = max(len(v) for v in scores.values())
    top = [a for a, v in scores.items() if len(v) == best]
    if len(top) > 1:
        names = " and ".join(AGENT_NAMES[a] for a in top[:2])
        return _result(
            GENERAL,
            False,
            f"The question fits more than one agent ({names}), so the general agent answers it. "
            "Choose an agent in the list to focus the answer.",
        )
    agent = top[0]
    if role not in REGISTRY[agent]["roles"]:
        return _result(
            GENERAL,
            False,
            f"The {AGENT_NAMES[agent]} is for other roles, so the general agent answers it.",
        )
    return _result(agent, True, f"The question is about {FOCUS[agent]}.")
