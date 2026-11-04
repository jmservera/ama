"""Deterministic calculation with draft-only narrative for the discovery assistant (issue 125).

Pure and offline: no store, network or clock access. Durations come only from deterministic code.
An optional drafter (for example a language model, passed in by the caller) may only phrase the
result; every draft is checked so each number it quotes matches a calculated figure and each
statement cites a source event. If the drafter is absent, fails or is rejected, a plain
deterministic sentence is used, so the analysis never depends on a model. Output is always a draft
for human review and is never a validated company finding.
"""

import re
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
from datetime import datetime

DRAFTING_VERSION = "discovery-assistant-drafting-v1"
DRAFT_FOR_HUMAN_REVIEW = "DRAFT_FOR_HUMAN_REVIEW"
MANUAL_PATH = (
    "Manual analysis, conventional reporting and export remain available; "
    "nothing here needs a model."
)

Drafter = Callable[[Mapping[str, float], tuple[str, ...]], str]


@dataclass(frozen=True)
class StageEvent:
    """One source event for a property; the source reference is a human-supplied pointer."""

    property_id: str
    stage: str
    timestamp: str
    source_reference: str


@dataclass(frozen=True)
class StageDurations:
    hours: dict[str, float]
    source_references: tuple[str, ...]
    gaps: tuple[str, ...]


def _parse(value: str) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed.tzinfo is not None else None


def calculate_stage_durations(events: Iterable[StageEvent]) -> StageDurations:
    """Hours between consecutive events of one property, summed by the stage that was left.

    Events with missing, unparsable or timezone-less timestamps, or without a source reference,
    are reported as gaps and never guessed. The last event of a property has no end, so it adds
    no duration.
    """
    gaps: list[str] = []
    by_property: dict[str, list[tuple[datetime, StageEvent]]] = {}
    for event in events:
        moment = _parse(event.timestamp)
        if moment is None:
            gaps.append(f"unusable-timestamp:{event.property_id}/{event.stage}")
        elif not event.source_reference.strip():
            gaps.append(f"missing-source:{event.property_id}/{event.stage}")
        else:
            by_property.setdefault(event.property_id, []).append((moment, event))
    totals: dict[str, float] = {}
    refs: list[str] = []
    for rows in by_property.values():
        rows.sort(key=lambda row: row[0])
        for (start, left), (end, entered) in zip(rows, rows[1:], strict=False):
            totals[left.stage] = totals.get(left.stage, 0.0) + (end - start).total_seconds() / 3600
            refs.extend((left.source_reference, entered.source_reference))
    return StageDurations(
        hours={k: round(v, 2) for k, v in sorted(totals.items())},
        source_references=tuple(sorted(set(refs))),
        gaps=tuple(gaps),
    )


@dataclass(frozen=True)
class DraftReport:
    drafting_version: str
    status: str
    text: str
    model_used: bool
    rejected_reason: str
    source_references: tuple[str, ...]
    validated_finding: bool = False
    manual_path: str = MANUAL_PATH
    notes: tuple[str, ...] = field(default_factory=tuple)


_NUMBER = re.compile(r"\d+(?:\.\d+)?")


def _plain(durations: StageDurations) -> str:
    if not durations.hours:
        return "No stage durations could be calculated from the supplied events."
    return "; ".join(f"{stage}: {hours:g} hours" for stage, hours in durations.hours.items()) + "."


def _check(text: str, durations: StageDurations) -> str:
    if not text.strip():
        return "EMPTY_DRAFT"
    allowed = {f"{v:g}" for v in durations.hours.values()}
    if not any(ref in text for ref in durations.source_references):
        return "NO_SOURCE_CITED"
    quoted = text
    for ref in sorted(durations.source_references, key=len, reverse=True):
        quoted = quoted.replace(ref, " ")
    if any(f"{float(n):g}" not in allowed for n in _NUMBER.findall(quoted)):
        return "NUMBER_NOT_CALCULATED"
    return ""


def draft_evidence(durations: StageDurations, drafter: Drafter | None = None) -> DraftReport:
    """Draft a narrative; fall back to a deterministic sentence if no usable model draft exists."""
    plain = _plain(durations)
    cited = f"{plain} Sources: {', '.join(durations.source_references) or 'none'}."
    reason = "NO_DRAFTER" if drafter is None else ""
    text, used = cited, False
    if drafter is not None:
        try:
            candidate = drafter(durations.hours, durations.source_references)
        except Exception:
            candidate = ""
            reason = "DRAFTER_UNAVAILABLE"
        else:
            reason = _check(candidate, durations)
        if not reason:
            text, used = candidate, True
    return DraftReport(
        drafting_version=DRAFTING_VERSION,
        status=DRAFT_FOR_HUMAN_REVIEW,
        text=text,
        model_used=used,
        rejected_reason=reason,
        source_references=durations.source_references,
        notes=("A named human reviews every draft; it is not a validated company finding.",),
    )
