"""Read-only retention review, aligned with chat settings; never a DPO approval or purge."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

OWNER = "Juan Manuel Servera"
CLASSES = (
    ("law_source", "reg_source, reg_version, reg_provision, source candidates and snapshots"),
    ("rule_card", "rule_card_version, rule_card_event and source-review records"),
    ("check", "reg_check and reg_checkpoint; case linkage and input hashes"),
    ("alert", "reg_alert and reg_alert_event; named owner dispositions"),
    ("audit", "Append-only rule/check/alert records and chat metadata ledger"),
    (
        "usage",
        "Content-free regulatory turn audit metadata and reg_check/reg_alert usage; "
        "inherits parent record access, retention and audit review",
    ),
)


def retention_report(threads: list[dict[str, Any]], env: Any, now: datetime) -> dict[str, Any]:
    """List review-due own threads, never infer a deletion entitlement from age."""
    if now.tzinfo is None:
        raise ValueError("Retention review needs a timezone-aware clock.")
    ref = str(env.get("CHAT_RETENTION_REF") or "").strip()
    raw = str(env.get("CHAT_RETENTION_DAYS") or "").strip()
    days = None
    if ref or raw:
        if not ref.startswith("SYNTH-") or not raw.isascii() or not raw.isdigit():
            raise ValueError("Synthetic retention needs a SYNTH- reference and positive days.")
        days = int(raw)
        if not 1 <= days <= 36500:
            raise ValueError("Synthetic retention days must be between 1 and 36500.")
    rows = []
    for thread in threads:
        due = None
        if days is not None:
            created = datetime.fromisoformat(thread["created_at"])
            if created.tzinfo is None:
                raise ValueError("Thread creation time lacks a timezone; DPO review required.")
            due = created.astimezone(UTC) + timedelta(days=days)
        rows.append(
            dict(
                thread_id=thread["id"],
                messages=thread["message_count"],
                review_due=due.isoformat() if due else None,
                due_for_review=due <= now if due else None,
            )
        )
    return dict(
        label="synthetic-demo",
        owner=OWNER,
        dpia_status="Draft for DPO review; not completed",
        dpo_reviewed=False,
        deletion_enabled=False,
        chat=dict(
            storage="chat_thread and chat_message (reg_chat_turn equivalent)",
            trigger="Thread creation, including archived threads; simulated review only",
            status="simulated" if days else "unknown",
            days=days,
            reference=ref or None,
            records=rows,
        ),
        other_classes=[
            dict(
                record_class=name,
                storage=storage,
                status="unknown",
                days=None,
                reference=None,
            )
            for name, storage in CLASSES
        ],
        action="DPO must set periods, triggers, holds, rights and disposal approval. "
        "No records are deleted or marked lawfully retained by this report.",
    )
