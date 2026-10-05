"""Strictly reconstruct a canonical card from score choices and details JSON."""

from __future__ import annotations

import json
from typing import Any

DETAIL_FIELDS = {"evidence", "rationale", "change_reason"}
SCORES = {str(score): score for score in range(1, 6)}


def from_inputs(inputs: dict[str, Any], criterion_ids: list[str]) -> dict[str, Any]:
    """Validate every input and detail explicitly; never coerce or fill gaps."""
    expected = {"summary", "details"} | {f"{cid}_score" for cid in criterion_ids}
    missing = expected - inputs.keys()
    extra = inputs.keys() - expected
    if missing:
        raise ValueError("missing scorecard inputs: " + ", ".join(sorted(missing)))
    if extra:
        raise ValueError("unknown scorecard inputs: " + ", ".join(sorted(extra)))
    if not all(isinstance(value, str) for value in inputs.values()):
        raise ValueError("all scorecard inputs must be strings")
    try:
        details = json.loads(inputs["details"], object_pairs_hook=unique_object)
    except json.JSONDecodeError as error:
        raise ValueError(f"details is not valid JSON: {error}") from error
    if not isinstance(details, dict):
        raise ValueError("details must encode an object")
    if set(details) != set(criterion_ids):
        raise ValueError("details must contain exactly the 20 rubric criterion IDs")
    criteria = {}
    for cid in criterion_ids:
        score = inputs[f"{cid}_score"]
        if score not in SCORES:
            raise ValueError(f"{cid}_score must be exactly one of '1', '2', '3', '4', '5'")
        entry = details[cid]
        if not isinstance(entry, dict) or set(entry) != DETAIL_FIELDS:
            raise ValueError(f"{cid} details must contain exactly evidence, rationale, change_reason")
        evidence = entry["evidence"]
        if not isinstance(evidence, list) or not all(isinstance(ref, str) for ref in evidence):
            raise ValueError(f"{cid} evidence must be an array of strings")
        if not isinstance(entry["rationale"], str) or not isinstance(entry["change_reason"], str):
            raise ValueError(f"{cid} rationale and change_reason must be strings")
        criteria[cid] = {
            "score": SCORES[score],
            "evidence": evidence,
            "rationale": entry["rationale"],
            "change_reason": entry["change_reason"],
        }
    return {"criteria": criteria, "summary": inputs["summary"]}


def to_inputs(scorecard: dict[str, Any], criterion_ids: list[str]) -> dict[str, Any]:
    """Flatten a trusted context scaffold, retaining unscored null placeholders."""
    inputs: dict[str, Any] = {}
    details = {}
    for cid in criterion_ids:
        entry = scorecard["criteria"][cid]
        score = entry["score"]
        inputs[f"{cid}_score"] = str(score) if score is not None else None
        details[cid] = {field: entry[field] for field in sorted(DETAIL_FIELDS)}
    inputs["details"] = json.dumps(details, ensure_ascii=True)
    inputs["summary"] = scorecard["summary"]
    return inputs


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Reject duplicate JSON keys instead of silently discarding submitted data."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate details key: {key}")
        result[key] = value
    return result
