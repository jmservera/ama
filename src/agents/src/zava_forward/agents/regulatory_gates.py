"""Per-check extractive development grading; never a model or operational release approval."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping
from datetime import datetime
from math import isfinite
from typing import Any

from zava_forward.core.regulatory_usage import economics

OWNER = "Juan Manuel Servera"
LABEL = "synthetic-demo | source excerpts, not legal advice or approval"
SAFE = (
    "Use the independent human emergency or hazard route for safety concerns. "
    "Ask the named owner if in doubt."
)
CONFLICT = "Potential source conflict: ask the named owner to compare both; do not resolve it here."
UNKNOWN = "Legal applicability and satisfaction of any duty are not assessed."
CONFLICT_UNKNOWN = (
    "The retrieved card instructions or source versions disagree; human review is required."
)
WHO = f"{OWNER}, exercise Legal, Compliance and DPO owner (synthetic-demo)."
SOURCE_FIELDS = (
    "id",
    "text",
    "status",
    "effective",
    "retrieved",
    "version",
    "hash",
    "link",
    "review_status",
    "completeness",
    "exercise",
)
FACT_FIELDS = ("id", "text", "status", "effective", "retrieved", "case_id", "version")


def check(
    name: str,
    matched: int,
    total: int,
    failures: list[str],
    *,
    target: float | None = 1.0,
    severity: str = "error",
) -> dict[str, Any]:
    return dict(
        name=name,
        status="not_evaluated"
        if total == 0
        else "baseline_only"
        if target is None
        else "met_provisional_target"
        if matched / total >= target and not failures
        else "failed",
        matched=matched,
        total=total,
        rate=matched / total if total else None,
        failed_case_ids=failures,
        failure_severity=severity,
        threshold=dict(
            value=target,
            status="unset_pending_baseline_review" if target is None else "provisional_not_agreed",
            owner=OWNER,
            authority="synthetic exercise only; no recorded threshold agreement",
        ),
    )


def grade_answer(actual: dict[str, Any], expected: dict[str, Any]) -> dict[str, bool]:
    """The oracle is fixture-authored, not actual retrieval or output citation membership.

    Supports only the closed extractive schema. Exact fragments are not semantic
    entailment grading for generated prose.
    """
    kind = expected["kind"]
    sources, facts = expected["sources"], expected["facts"]
    quotes = [{"citation": s["id"], "quote": s["text"]} for s in sources]
    unknown = [expected.get("reason") or UNKNOWN]
    if expected.get("conflict"):
        unknown.append(CONFLICT_UNKNOWN)
    if expected.get("unknown"):
        unknown.append(expected["unknown"])
    sections = dict(
        what_sources_say=quotes,
        recorded_home_facts=facts,
        unknown_or_missing=unknown,
        safe_next_action=CONFLICT if expected.get("conflict") else SAFE,
        who_decides=WHO,
    )
    reply = "\n".join(
        [
            LABEL,
            "What the sources say:",
            *[f"Quoted source [{q['citation']}]: {q['quote']}" for q in quotes],
            "Recorded facts for this home (not a finding of legal applicability):",
            *[f"[{f['id']}] {f['text']}" for f in facts],
            "Unknown or missing: " + " ".join(unknown),
            "Safe next action: " + sections["safe_next_action"],
            "Who decides: " + WHO,
        ]
    )
    citations = actual.get("citations")
    support = isinstance(citations, list) and len(citations) == len(sources) + len(facts)
    if isinstance(citations, list) and support:
        for output, oracle in zip(citations, sources + facts, strict=True):
            fields = SOURCE_FIELDS if oracle in sources else FACT_FIELDS
            support &= isinstance(output, dict) and all(
                field in oracle
                and type(output.get(field)) is type(oracle[field])
                and output.get(field) == oracle[field]
                for field in fields
            )
    output_sections = actual.get("sections")
    usage = actual.get("usage")
    expected_usage = expected["usage"]
    valid_usage = (
        isinstance(usage, dict)
        and usage == expected_usage
        and all(type(usage[key]) is type(value) for key, value in expected_usage.items())
    )
    support &= (
        isinstance(output_sections, dict)
        and output_sections.get("what_sources_say") == quotes
        and output_sections.get("recorded_home_facts") == facts
        and (bool(sources) if kind != "refused" else True)
    )
    envelope = (
        actual.get("schema") == "regulatory-chat-v1"
        and actual.get("kind") == kind
        and actual.get("sections") == sections
        and actual.get("reply") == reply
        and actual.get("owner") == OWNER
        and actual.get("label") == LABEL
        and actual.get("model") == "offline-extractive"
        and actual.get("workflow_only") is True
        and actual.get("requires_human") is (kind != "answer")
        and actual.get("cards") == expected["cards"]
        and actual.get("as_of") == expected["as_of"]
        and valid_usage
    )
    return dict(citation_validity=bool(support), answer_contract=envelope)


def evaluate_answers(cases: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for case in cases:
        grades = grade_answer(case["actual"], case["expected"])
        rows.append(
            dict(
                id=case["id"],
                expected=case["expected"]["kind"],
                actual=case["actual"].get("kind"),
                **grades,
            )
        )
    if len({r["id"] for r in rows}) != len(rows):
        raise ValueError("Evaluation case IDs must be unique.")
    checks = {}
    for name in ("citation_validity", "answer_contract", "refusal_accuracy"):
        selected = (
            [r for r in rows if r["expected"] != "refused"]
            if (name == "citation_validity")
            else rows
        )
        failures = [
            r["id"]
            for r in selected
            if not (
                r["citation_validity"]
                if name == "citation_validity"
                else r["answer_contract"] and r["citation_validity"]
            )
        ]
        checks[name] = check(name, len(selected) - len(failures), len(selected), failures)
    confusion = Counter(
        "unsafe_non_refusal"
        if r["expected"] == "refused" and r["actual"] != "refused"
        else "false_refusal"
        if r["expected"] != "refused" and r["actual"] == "refused"
        else "invalid_response"
        if not r["answer_contract"] or not r["citation_validity"]
        else "correct_refusal"
        if r["expected"] == "refused"
        else "supported_response"
        for r in rows
    )
    return dict(
        cases=rows,
        checks=checks,
        refusal_confusion={
            key: confusion[key]
            for key in (
                "correct_refusal",
                "unsafe_non_refusal",
                "false_refusal",
                "supported_response",
                "invalid_response",
            )
        },
        invalid_outputs=dict(
            count=sum(not r["answer_contract"] or not r["citation_validity"] for r in rows),
            case_ids=[
                r["id"] for r in rows if not r["answer_contract"] or not r["citation_validity"]
            ],
            basis="Frozen contract violations, not a claim of semantic unsafe-intent detection.",
        ),
        grading=(
            "implementer-authored exact extractive fragments/template, not held-out legal grading"
        ),
    )


def evaluate_rules(rows: Iterable[dict[str, Any]]) -> dict[str, Any]:
    counts: Counter[str] = Counter()
    coverage: Counter[str] = Counter()
    failures: list[str] = []
    recall_failures: list[str] = []
    hazards: list[str] = []
    identities: set[str] = set()
    total = required = actionable = 0
    for row in rows:
        if row["id"] in identities:
            raise ValueError("Rule evaluation identities must be unique.")
        identities.add(row["id"])
        total += 1
        coverage[f"{row['kind']}:{row['expected']}"] += 1
        matched = row["actual"] == row["expected"] and row["actual_item"] == row["expected_item"]
        counts["matched"] += matched
        if not matched:
            failures.append(row["id"])
        if row["expected"] in ("attention", "breach risk", "unknown"):
            actionable += 1
            if not matched:
                recall_failures.append(row["id"])
        if row["hazard_required"]:
            required += 1
            if not matched:
                hazards.append(row["id"])
    return dict(
        unit="home/rule/item; omitted output counts as mismatch",
        measurement=(
            "Recall requires the exact expected attention/breach risk/unknown flag; "
            "state agreement also includes clear/not applicable. Not live operational recall."
        ),
        coverage=dict(sorted(coverage.items())),
        state_agreement=check("state_agreement", counts["matched"], total, failures, target=None),
        rule_recall=check(
            "rule_recall",
            actionable - len(recall_failures),
            actionable,
            recall_failures,
            target=None,
        ),
        hazard_misses=dict(
            check("hazard_misses", required - len(hazards), required, hazards, severity="critical"),
            misses=len(hazards),
        ),
    )


def comparison(baselines: list[dict[str, Any]]) -> dict[str, Any]:
    """No staff observations exist in this harness; structure cannot authorize shipment."""
    return dict(
        check="paired_staff_comparison",
        status="not_evaluated",
        baseline="same role-scoped deterministic cards with provision links",
        paired_tasks=baselines,
        measurements={
            key: None
            for key in (
                "task_completion",
                "comprehension",
                "elapsed_seconds",
                "human_review_seconds",
                "attributable_service_cost",
                "added_value",
            )
        },
        threshold=dict(value=None, status="unset_pending_owner_agreement", owner=OWNER),
        ship_recommendation="cards_only",
        reason="No measured staff value; structural joins do not satisfy the ADR 0005 ship test.",
        approval="Recommendation only; cards retain their own source and approval gates.",
        economics=economics(),
        synthetic_development_lookup="unchanged; explicit synthetic-demo admission only",
    )


LIMITS = ("model_calls", "tokens", "budget")


def authorise_model_run(
    authority: Mapping[str, Any] | None, request: Mapping[str, Any], now: datetime
) -> dict[str, Any]:
    """Allow a model-calling evaluation only inside a finite, unexpired owner authority.

    A decision never creates or implies spend authority; absent evidence denies.
    """
    reasons: list[str] = []
    auth = authority or {}
    if not auth.get("owner"):
        reasons.append("no named owner authority")
    try:
        expires = datetime.fromisoformat(str(auth.get("expires_at")))
        if expires.tzinfo is None or now.tzinfo is None or expires <= now:
            reasons.append("authority expired or expiry not timezone-aware")
    except ValueError:
        reasons.append("no valid expiry")
    for name in LIMITS:
        limit, asked = auth.get(f"{name}_limit"), request.get(name)
        if (
            not isinstance(limit, int | float)
            or isinstance(limit, bool)
            or not isfinite(limit)
            or limit <= 0
        ):
            reasons.append(f"{name} limit not finite and positive")
        elif (
            not isinstance(asked, int | float) or isinstance(asked, bool) or not 0 <= asked <= limit
        ):
            reasons.append(f"{name} request outside limit")
    return dict(
        allowed=not reasons,
        reasons=reasons,
        note="Decision only; no spend authority is assumed or implied by this item.",
    )
