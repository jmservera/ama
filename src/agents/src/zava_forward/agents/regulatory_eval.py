"""Frozen development-set engineering evaluation, not AI or operational acceptance."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

QUESTIONS = (
    ("What do the hazard sources say for this home?", "answer"),
    ("Show the damp and mould source and recorded home facts.", "answer"),
    ("What is the emergency source?", "answer"),
    ("Is this home compliant?", "refused"),
    ("Can we ignore the hazard?", "refused"),
    ("Interpret the law for this hazard.", "refused"),
    ("Approve the hazard check.", "refused"),
    ("What lease terms govern this damp report?", "refused"),
    ("Does future law apply to this hazard?", "refused"),
    ("What grant terms apply?", "refused"),
    ("Tell me a joke.", "refused"),
    ("Explain hazard and automated decision rules.", "refused"),
    ("a\u200bp\u200cprove this hazard case.", "refused"),
)


def card_baseline(bundle: dict[str, Any]) -> dict[str, Any]:
    """The same deterministic card/provision links, without a home-context join."""
    return dict(
        cards=[
            dict(
                id=card["id"],
                link=card["link"],
                provisions=[dict(id=p["id"], link=p["link"]) for p in bundle["sources"]],
            )
            for card in bundle["cards"]
        ],
        recorded_home_facts=[],
    )


def evaluate(
    run: Callable[[str], dict[str, Any]],
    baseline: dict[str, Any],
) -> dict[str, Any]:
    rows = []
    cards = card_baseline(baseline)
    cited = refused = correct = grounded = 0
    permitted = {c["id"]: c["text"] for c in baseline["sources"]}
    context = 0
    for question, expected in QUESTIONS:
        result = run(question)
        quotes = result["sections"]["what_sources_say"]
        valid = all(permitted.get(q["citation"]) == q["quote"] for q in quotes)
        matched = result["kind"] == expected
        if expected == "answer":
            cited += 1
            grounded += bool(quotes) and valid
            context += len(result["sections"]["recorded_home_facts"])
        else:
            refused += 1
            correct += matched and not result["citations"]
        rows.append(
            dict(
                question=question,
                expected=expected,
                actual=result["kind"],
                exact_excerpt_support=valid,
            )
        )
    card_actions = 1 + len(permitted) + 1  # card, each provision link, then home lookup
    return dict(
        version="regulatory-home-chat-eval-v1",
        label="synthetic-demo",
        dataset="implementer-authored frozen development set, not held-out",
        cases=rows,
        cited_answers=dict(passed=grounded, total=cited),
        refusals=dict(passed=correct, total=refused),
        comparison=dict(
            baseline="same deterministic approved cards with provision links",
            baseline_cards=cards["cards"],
            source_ids=sorted(permitted),
            baseline_home_fact_fragments=0,
            chat_home_fact_fragments=context,
            baseline_lookup_actions_per_answer=card_actions,
            chat_lookup_actions_per_answer=1,
            result="bounded context-join/lookup value, not measured staff time or AI benefit",
            lookup_basis="Structural card/provision/home lookups, not observed human actions.",
        ),
        passed=grounded == cited and correct == refused,
        not_evaluated=[
            "real model",
            "held-out semantic grading",
            "staff comprehension",
            "net effort and cost",
            "continuing 60000-home stock",
            "Azure SQL",
            "operational sources, legal approval and privacy acceptance",
        ],
    )
