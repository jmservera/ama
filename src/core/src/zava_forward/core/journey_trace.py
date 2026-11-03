"""Read-only same-home journey trace over audit entries (Refs #134).

Orders one home's recorded events through EPC conflict, correction, independent decisions,
handover and financial closure, and reports intervals as Unknown whenever a stage or timestamp
is missing. Entries of sibling homes and building records never create or complete a stage.
Constructed-fixture evidence only: it is not user validation and approves nothing.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import datetime
from typing import Any

STAGES = (
    "epc_conflict",
    "correction",
    "independent_decisions",
    "handover",
    "financial_closure",
)
DECISION_DOMAINS = {
    "resident_decision": "resident",
    "technical_signoff_give": "technical",
    "quality_accepted": "quality",
    "finance_disposition": "finance",
}
ACCEPT_DECISION = "Accept for payment"
PAID_STATUS = "Paid outside this system"
NOTICE = (
    "Constructed-fixture evidence, not user validation. Reading this trace approves nothing, "
    "contacts no resident, and makes or releases no payment."
)


def _parse(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _query_id(detail: object) -> str | None:
    parts = str(detail).split()
    return parts[1].rstrip(":") if len(parts) > 1 else None


def _epc_query(detail: object) -> str | None:
    parts = str(detail).split()
    return parts[0] if len(parts) > 1 and parts[1].rstrip(";") == "epc" else None


def _interval(first: Mapping[str, Any] | None, second: Mapping[str, Any] | None) -> dict[str, Any]:
    if first is None or second is None:
        return dict(seconds=None, status="Unknown", reason="A stage is not recorded.")
    start, end = _parse(first["at"]), _parse(second["at"])
    if start is None or end is None or (start.tzinfo is None) != (end.tzinfo is None):
        return dict(seconds=None, status="Unknown", reason="A timestamp is missing or unreadable.")
    seconds = int((end - start).total_seconds())
    if seconds < 0:
        return dict(seconds=None, status="Unknown", reason="Recorded order contradicts timestamps.")
    return dict(seconds=seconds, status="Recorded", reason=None)


def journey_trace(entries: Iterable[Mapping[str, Any]], case_id: str) -> dict[str, Any]:
    """Build the trace for one home. Entries for any other case id are ignored."""
    events: list[dict[str, Any]] = []
    open_epc: set[str] = set()
    for sequence, entry in enumerate(entries):
        if entry.get("case") != case_id:
            continue
        action = str(entry.get("action", ""))
        stages: list[str] = []
        if action == "stock_comparison":
            query = _epc_query(entry.get("detail"))
            if query:
                open_epc.add(query)
                stages.append("epc_conflict")
        elif action == "stock_query_resolve" and _query_id(entry.get("detail")) in open_epc:
            stages.append("correction")
        if action in DECISION_DOMAINS and (
            action != "finance_disposition"
            or str(entry.get("detail", "")).endswith(ACCEPT_DECISION)
        ):
            stages.append("independent_decisions")
        if action == "quality_handover":
            stages.append("handover")
        if action == "finance_payment_status" and str(entry.get("detail", "")).endswith(
            f"payment noted as {PAID_STATUS}"
        ):
            stages.append("financial_closure")
        for stage in stages:
            events.append(
                dict(
                    sequence=sequence,
                    stage=stage,
                    action=action,
                    at=entry.get("at"),
                    who=entry.get("who"),
                    detail=entry.get("detail"),
                )
            )

    first: dict[str, dict[str, Any] | None] = {
        stage: next((e for e in events if e["stage"] == stage), None) for stage in STAGES
    }
    stage_rows = [
        dict(
            stage=stage,
            status="Recorded" if first[stage] else "Not recorded",
            events=sum(1 for e in events if e["stage"] == stage),
            first_at=head["at"] if (head := first[stage]) else None,
        )
        for stage in STAGES
    ]
    intervals = [
        dict(from_stage=a, to_stage=b, **_interval(first[a], first[b]))
        for a, b in zip(STAGES, STAGES[1:], strict=False)
    ]
    order_findings = [
        f"{b} is recorded before {a}."
        for a, b in zip(STAGES, STAGES[1:], strict=False)
        if (earlier := first[a]) and (later := first[b]) and later["sequence"] < earlier["sequence"]
    ]

    actors: dict[str, set[str]] = {}
    for event in events:
        domain = DECISION_DOMAINS.get(event["action"])
        if domain and event["stage"] == "independent_decisions":
            actors.setdefault(domain, set()).add(str(event["who"]))
    shared = sorted(
        {
            who
            for domain, people in actors.items()
            for other, others in actors.items()
            if other != domain
            for who in people & others
        }
    )
    independent = len(actors) >= 2 and not shared
    return dict(
        case_id=case_id,
        evidence_class="constructed-fixture",
        user_validation="not-established",
        notice=NOTICE,
        events=events,
        stages=stage_rows,
        intervals=intervals,
        order_findings=order_findings,
        decision_domains={domain: sorted(people) for domain, people in sorted(actors.items())},
        shared_decision_actors=shared,
        independent_decisions=independent,
        complete=(all(first[stage] for stage in STAGES) and not order_findings and independent),
    )
