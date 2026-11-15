"""Plain-language mode for chat replies (#215): a summary added beside the cited reply."""

from __future__ import annotations

from typing import Any

from zava_forward.core.regulatory_output_guard import (
    ADVISORY_REVIEW_TEXT,
    GuardTelemetry,
    inspect_regulatory_output,
    merge_guard_statuses,
)

FIELD = "plain_language"

_SUMMARIES = {
    "answer": (
        "This answer quotes {sources}. Check each source before you act. "
        "Chat does not approve or change anything."
    ),
    "conflict": (
        "The sources disagree. Do not pick one. The named owner compares them and decides."
    ),
    "withheld": (
        "The assistant held the answer back because the sources do not support it. "
        "Ask the named owner what to do next."
    ),
    "fallback": (
        "This is fixed workflow help, not an AI answer. Ask the named owner if you need more."
    ),
    "refused": (
        "The assistant cannot do this. It explains recorded facts and sources only. "
        "Use the normal workflow or ask the named owner."
    ),
}


def split_flag(body: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
    """The validated plain-language flag (default off) and the body without it."""
    flag = body.get(FIELD, False)
    if type(flag) is not bool:
        raise ValueError("plain_language must be true or false.")
    return flag, {key: value for key, value in body.items() if key != FIELD}


def apply(
    reply: dict[str, Any],
    enabled: bool,
    *,
    telemetry: GuardTelemetry | None = None,
) -> dict[str, Any]:
    """Add the summary; the reply text, citations and provenance stay as produced."""
    if not enabled:
        return reply
    count = len(reply.get("citations") or [])
    sources = "1 cited source" if count == 1 else f"{count} cited sources"
    template = _SUMMARIES.get(str(reply.get("kind")), _SUMMARIES["refused"])
    summary = template.format(sources=sources)
    if reply.get("kind") == "answer" and not count:
        summary = "This answer has no cited source. Treat it as open and ask the named owner."
    decision = inspect_regulatory_output(summary, on_violation="rewrite", telemetry=telemetry)
    if not decision.passed:
        summary = decision.rewritten_text or ADVISORY_REVIEW_TEXT
    out = dict(reply, plain_language=True, plain_summary=summary)
    if isinstance(reply.get("output_guard"), dict):
        out["output_guard"] = merge_guard_statuses(
            [reply["output_guard"], decision.to_status_dict()]
        )
    elif not decision.passed:
        out["output_guard"] = decision.to_status_dict()
    return out
