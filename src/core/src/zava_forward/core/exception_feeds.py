"""Read-only feeds that route existing records into the exception queue (FR-029, AC-040).

Each feed only reads records the product already keeps and raises queue items. It never edits,
replays, re-sends or releases anything, and a repeated read does not duplicate an item.
"""

from collections.abc import Iterable, Mapping
from typing import Any

from .exception_queue import ExceptionQueue, Record

QUARANTINED = "Quarantined"
UNKNOWN = "Unknown"


def _ai_failure_reason(rec: Mapping[str, Any]) -> str | None:
    """Why an AI task gave no model result, or None (also when workflow-only was chosen)."""
    if rec.get("kind") != "ai_task":
        return None
    reason = rec.get("fallback_reason")
    if rec.get("status") == QUARANTINED:
        return str(reason or "Result quarantined.")
    if rec.get("mode") == "ai" and rec.get("source") != "ai" and reason:
        return str(reason)
    return None


def feed_failed_ai_runs(
    queue: ExceptionQueue, records: Iterable[Mapping[str, Any]], owner: str
) -> list[Record]:
    """Raise a failed_ai_run item for each AI task that fell back or was quarantined.

    The item keeps record ids and the stated reason only, not the AI or workflow text. A person
    decides whether to ask for a re-run.
    """
    raised: list[Record] = []
    for rec in records:
        reason = _ai_failure_reason(rec)
        if reason is None:
            continue
        record_id = str(rec.get("id", ""))
        raised.append(
            queue.raise_failure(
                "failed_ai_run",
                owner,
                f"AI task {rec.get('task', UNKNOWN)} did not deliver a model result.",
                {
                    "record_id": record_id,
                    "task": rec.get("task"),
                    "case_ids": list(rec.get("case_ids") or []),
                    "status": rec.get("status"),
                    "created": rec.get("created"),
                },
                reason,
                ref=record_id,
            )
        )
    return raised


def feed_stranded_tasks(
    queue: ExceptionQueue, overdue: Iterable[Mapping[str, Any]], owner: str
) -> list[Record]:
    """Raise a stranded_task item for each overdue task (taskqueues.overdue_tasks) with no owner."""
    raised: list[Record] = []
    for task in overdue:
        named = task.get("owner")
        if isinstance(named, str) and named.strip() and named != UNKNOWN:
            continue
        source = str(task.get("source", ""))
        raised.append(
            queue.raise_failure(
                "stranded_task",
                owner,
                f"Overdue task has no named owner: {task.get('task', UNKNOWN)}.",
                {
                    "source": source,
                    "case_id": task.get("case_id"),
                    "due_at": task.get("due_at"),
                    "as_of": task.get("as_of"),
                },
                f"No named owner; completion {task.get('completion', 'Not evidenced')}.",
                ref=source or None,
            )
        )
    return raised


def feed_unaccepted_handoffs(
    queue: ExceptionQueue, ageing: Iterable[Mapping[str, Any]], owner: str
) -> list[Record]:
    """Raise a stranded_task item per handoff flagged needs_escalation (workflows.handoff_ageing).

    Raising only makes the unaccepted handoff visible to the exception owner; a named manager
    still escalates or reassigns it by hand.
    """
    raised: list[Record] = []
    for row in ageing:
        if not row.get("needs_escalation"):
            continue
        case_id = str(row.get("case_id", ""))
        raised.append(
            queue.raise_failure(
                "stranded_task",
                owner,
                f"Handoff not accepted in time for case {case_id or UNKNOWN}.",
                {
                    "case_id": case_id,
                    "chase_owner": row.get("chase_owner"),
                    "age_hours": row.get("age_hours"),
                    "due_at": row.get("due_at"),
                    "as_of": row.get("as_of"),
                },
                "; ".join(row.get("reasons") or ["Unaccepted handoff"]),
                ref=f"handoff:{case_id}:{row.get('as_of', '')[:10]}",
            )
        )
    return raised


def feed_failed_imports(
    queue: ExceptionQueue,
    batches: Iterable[Mapping[str, Any]],
    owner: str,
    refusals: Iterable[Mapping[str, Any]] = (),
) -> list[Record]:
    """Raise a failed_import item for each rejected batch and each refused import file.

    Batches are importer batch records (status rejected means the data never went live).
    Refusals are files the importer would not preview or stage: source_name, source_sha256,
    reason and optional at. Only source identity, version and the stated reason are kept, never
    row or cell values. The original file stays where it was; nothing is retried or approved.
    """
    raised: list[Record] = []
    for batch in batches:
        if batch.get("status") != "rejected":
            continue
        batch_id = str(batch.get("batch_id", ""))
        raised.append(
            queue.raise_failure(
                "failed_import",
                owner,
                f"Import batch {batch_id or UNKNOWN} was rejected and did not go live.",
                {
                    "batch_id": batch_id,
                    "structure": batch.get("structure"),
                    "version": batch.get("version"),
                    "source_name": batch.get("source_name"),
                    "source_sha256": batch.get("source_sha256"),
                    "staged_by": batch.get("staged_by"),
                    "staged_at": batch.get("staged_at"),
                },
                f"Rejected by {batch.get('decided_by') or UNKNOWN}: "
                f"{batch.get('decision_note') or 'no note recorded'}.",
                ref=f"batch:{batch_id}",
            )
        )
    for refusal in refusals:
        digest = str(refusal.get("source_sha256", ""))
        name = refusal.get("source_name")
        raised.append(
            queue.raise_failure(
                "failed_import",
                owner,
                f"Import file {name or UNKNOWN} was refused.",
                {
                    "source_name": name,
                    "source_sha256": digest or None,
                    "at": refusal.get("at"),
                },
                str(refusal.get("reason") or "No reason recorded."),
                ref=f"file:{digest or name}",
            )
        )
    return raised


def feed_stock_conflicts(
    queue: ExceptionQueue, cases: Iterable[Mapping[str, Any]], owner: str
) -> list[Record]:
    """Raise a source_conflict item per unresolved stock query on an open home (stock.py, #84).

    Both competing values keep their source, date and version. The queue picks no winner and
    changes nothing on the case; the named steward owns the resolution and the case keeps the
    original query. Eligibility stays Unknown.
    """
    from .stock import query_status

    raised: list[Record] = []
    for case in cases:
        if case.get("closed"):
            continue
        case_id = str(case.get("id", ""))
        for query in case.get("stock_reconciliation", []):
            if query_status(case, query["id"]) != "Unresolved":
                continue
            sides = [query["left"], query["right"]]
            raised.append(
                queue.raise_conflict(
                    "source_conflict",
                    owner,
                    f"Stock {query['field']} differs between sources "
                    f"for case {case_id or UNKNOWN}.",
                    [
                        {
                            "value": str(s["value"]),
                            "source": str(s["source_id"]),
                            "date": str(s["date"]),
                            "version": str(s["version"]),
                        }
                        for s in sides
                    ],
                    {
                        "case_id": case_id,
                        "query_id": query["id"],
                        "field": query["field"],
                        "query_owner": (query.get("query_owner") or {}).get("name"),
                        "left": dict(query["left"]),
                        "right": dict(query["right"]),
                    },
                    ref=f"stock:{case_id}:{query['id']}",
                )
            )
    return raised
