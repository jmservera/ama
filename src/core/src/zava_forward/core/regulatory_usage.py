"""Content-free accounting for the closed, model-free regulatory paths."""

from __future__ import annotations

import json
from collections import Counter
from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

SCHEMA = "regulatory-usage-v1"
MAX_POSITIONS = 1000
MAX_BYTES = 256 * 1024
TASKS = {
    "regulatory-home-chat": ("answer", "refused", "conflict"),
    "regulatory-check": ("clear", "attention", "breach risk", "unknown", "not applicable"),
}


def offline_usage(task: str, version: str, outcome: str, at: str) -> dict[str, Any]:
    if task not in TASKS or outcome not in TASKS[task]:
        raise ValueError("Unsupported offline regulatory task or outcome.")
    parsed = datetime.fromisoformat(at)
    if parsed.tzinfo is None:
        raise ValueError("Usage needs a timezone-aware recorded time.")
    return dict(
        schema=SCHEMA,
        task=task,
        task_version=version,
        model="none",
        outcome=outcome,
        period=parsed.astimezone(UTC).date().isoformat(),
        period_basis="UTC day",
        model_calls=0,
        input_tokens=0,
        output_tokens=0,
        cached_tokens=0,
        retries=0,
        model_call_limit_per_role_period=0,
        limit_basis="Inference disabled for every role; not a paid budget approval.",
    )


def economics() -> dict[str, Any]:
    return dict(
        cost="Unknown",
        ai_cost_per_accepted_check="Unknown",
        missing_inputs=[
            "Owner-agreed accepted-check definition and human acceptance count",
            "Dated versioned price source",
            "Attributable billing and shared-service allocation",
            "Measured human review effort",
        ],
        execution=dict(
            model_calls=0,
            input_tokens=0,
            output_tokens=0,
            model_call_limit=0,
            token_limit=0,
            paid_budget_limit=0,
            paid_authority="none",
            paid_authority_expires_at=None,
            reason="Offline only; no model dispatch or spend authority exists.",
        ),
    )


def summarize(details: Iterable[str], role: str, day: str, *, truncated: bool) -> dict[str, Any]:
    outcomes: Counter[str] = Counter()
    unmetered = 0
    for text in details:
        record = json.loads(text)
        if record.get("role") != role:
            continue
        usage = record.get("usage")
        if usage is None:
            unmetered += 1
            continue
        expected = offline_usage(
            "regulatory-home-chat",
            "regulatory-chat-v1",
            usage.get("outcome"),
            usage.get("period", "") + "T00:00:00+00:00",
        )
        if usage != expected or any(
            type(usage[key]) is not type(value) for key, value in expected.items()
        ):
            raise ValueError("Stored regulatory usage is invalid; audit review required.")
        if usage["period"] == day:
            outcomes[usage["outcome"]] += 1
    return dict(
        schema=SCHEMA,
        role=role,
        period=day,
        period_basis="UTC day",
        coverage="bounded_partial" if truncated else "recorded_audit_only",
        coverage_note=(
            "Recorded audit events only, not exact turn totals. Historical unmetered "
            "events and post-save JSON audit failures cannot be reconstructed."
        ),
        max_audit_positions=MAX_POSITIONS,
        max_json_bytes=MAX_BYTES,
        recorded_turns=sum(outcomes.values()),
        outcomes={name: outcomes[name] for name in TASKS["regulatory-home-chat"]},
        unmetered_events_in_window=unmetered,
        model_calls=0,
        model_call_limit_per_role_period=0,
        economics=economics(),
    )
