"""Rebuild RAI metrics from persisted SQL audit records (issue 146, criterion 5).

The append-only `assistant_events` table is the source: each row has a unique id, an epoch time
and a content-free JSON body. A restarted API or Orchestrator holds nothing in memory, so the
persisted ids of the window are the `prior_event_ids` of `reconcile_events`, and any replayed
telemetry batch is deduplicated against them before it is counted. Counts are derived from opaque
fields only (kind, state, outcome, action, token counts); no prompt, source text or identity is
read.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime
from typing import Any

from zava_forward.core.monitoring_coverage import (
    BLOCKED,
    COUNTED,
    INSUFFICIENT,
    MAX_CHECKPOINT,
    reconcile_events,
)

METRICS = (
    "invocation",
    "refusal",
    "withheld",
    "validation_failure",
    "fallback",
    "human_review",
    "override",
    "consumption",
    "latency_samples",
)
_INVOCATION = frozenset({"invocation", "direct-call-claimed"})
_REFUSAL = frozenset({"send-refused", "permit-denied", "throttled", "result-rejected"})
_FALLBACK = frozenset({"disabled", "exhausted"})
_COMPLETED = frozenset({"completed", "direct-call-completed"})
_OVERRIDE = frozenset({"reject", "edit-accept"})


def parse_window(start: Any, end: Any) -> tuple[datetime, datetime] | None:
    """The aware half-open window, or None when either bound is unusable."""
    bounds = []
    for value in (start, end):
        if not isinstance(value, str):
            return None
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        if parsed.tzinfo is None:
            return None
        bounds.append(parsed)
    return (bounds[0], bounds[1]) if bounds[0] < bounds[1] else None


def classify(event: Mapping[str, Any]) -> tuple[str, ...]:
    """Metric names one audit event contributes to; unknown kinds contribute to none."""
    kind = event.get("kind")
    if kind in _INVOCATION:
        return ("invocation",)
    if kind in _REFUSAL:
        return ("refusal",)
    if kind in _FALLBACK:
        return ("fallback",)
    if kind == "review":
        return (
            ("human_review", "override") if event.get("action") in _OVERRIDE else ("human_review",)
        )
    if kind == "completed":
        if event.get("state") == "quarantined" or event.get("financial_attribution"):
            return ("withheld", "consumption")
        if event.get("state") == "ready":
            return ("consumption",)
        envelope = event.get("envelope")
        outcome = envelope.get("outcome") if isinstance(envelope, Mapping) else None
        return ("validation_failure" if outcome == "returned" else "fallback", "consumption")
    if kind in _COMPLETED:
        return ("consumption",)
    return ()


def _at(event: Mapping[str, Any]) -> datetime:
    return datetime.fromisoformat(event["observed_at"].replace("Z", "+00:00"))


def _tokens(event: Mapping[str, Any]) -> int:
    value = event.get("actual_tokens")
    return value if event.get("kind") in _COMPLETED and type(value) is int and value >= 0 else 0


def _latencies(events: Sequence[Mapping[str, Any]]) -> list[float]:
    """Seconds from each task claim to its completion, matched by task and fence."""
    claimed: dict[tuple[Any, Any], datetime] = {}
    for event in events:
        if event.get("kind") == "claimed" and event.get("task_id") is not None:
            claimed[(event["task_id"], event.get("fence"))] = _at(event)
    samples = []
    for event in events:
        start = claimed.get((event.get("task_id"), event.get("fence")))
        if event.get("kind") == "completed" and start is not None:
            seconds = (_at(event) - start).total_seconds()
            if seconds >= 0:
                samples.append(seconds)
    return samples


def reconstruct(
    persisted: Sequence[Mapping[str, Any]],
    *,
    window_start: Any,
    window_end: Any,
    replay: Iterable[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Distinct-event metric counts for a window.

    `persisted` are SQL audit events (`event_id`, `observed_at`, body fields) inside the window.
    `replay` is any re-sent telemetry batch; ids already persisted count as duplicates, never twice.
    The result is blocked, with no counts, for an unusable window, an invalid replay id or a window
    with more distinct events than the reconcile checkpoint allows.
    """
    replayed = list(replay) if replay is not None else []
    ids = [str(e["event_id"]) for e in persisted]
    check = reconcile_events(
        replayed, window_start=window_start, window_end=window_end, prior_event_ids=ids
    )
    out: dict[str, Any] = {
        "status": check["status"],
        "metrics": None,
        "latency_seconds_total": None,
        "persisted": len(ids),
        "replay": {k: check[k] for k in ("duplicates", "new", "outside_window", "invalid")},
    }
    if check["count"] is None or check["invalid"] or len(ids) > MAX_CHECKPOINT:
        out["status"] = BLOCKED
        return out
    persisted_ids = set(ids)
    window = parse_window(window_start, window_end)
    if window is None:
        out["status"] = BLOCKED
        return out
    accepted: list[Mapping[str, Any]] = list(persisted)
    for event in replayed:
        eid = event["event_id"]
        if eid in persisted_ids:
            continue
        at = _at(event)
        if window[0] <= at < window[1]:
            persisted_ids.add(eid)
            accepted.append(event)
    counts = dict.fromkeys((*METRICS, "tokens"), 0)
    for event in accepted:
        for name in classify(event):
            counts[name] += 1
    samples = _latencies(accepted)
    counts["latency_samples"] = len(samples)
    counts["tokens"] = sum(_tokens(e) for e in accepted)
    out["metrics"] = counts
    out["latency_seconds_total"] = round(sum(samples), 3)
    out["status"] = COUNTED if accepted else INSUFFICIENT
    return out
