"""Offline evaluation harness over a frozen manifest (#2312, refs #108 and #223).

``validate_manifest`` checks a manifest against the checked-in JSON schema and the freeze rules in
``heldout_freeze``. ``run_eval`` scores supplied predictions against the held-out expected
outcomes and reports pass or fail for every threshold and every defined critical error.
``verify_recorded`` invalidates a recorded result when the manifest digest or any frozen version
differs. The harness is deterministic and offline: it makes no model call, reads no clock and
approves no threshold. Approvals stay under #108; synthetic data is not held-out evidence.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from zava_forward.agents.heldout_freeze import VERSION_KEYS, check_freeze

SCHEMA_PATH = Path(__file__).resolve().parents[3] / "evals" / "eval-manifest.schema.json"
NOTE = (
    "Offline harness result on supplied predictions. It makes no live model call and claims no "
    "approved threshold; approvals stay under #108. Synthetic data is not held-out evidence."
)


def load_schema() -> dict[str, Any]:
    schema: dict[str, Any] = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return schema


_TYPES: dict[str, tuple[type, ...]] = dict(
    object=(dict,), array=(list,), string=(str,), integer=(int,), number=(int, float)
)


def _check(value: Any, node: Mapping[str, Any], root: Mapping[str, Any], path: str) -> list[str]:
    """Validate the subset of JSON Schema the manifest schema uses; no extra dependency."""
    if "$ref" in node:
        target: Any = root
        for part in node["$ref"].lstrip("#/").split("/"):
            target = target[part]
        return _check(value, target, root, path)
    kind = node.get("type")
    if kind and (
        not isinstance(value, _TYPES[kind]) or isinstance(value, bool) and kind != "boolean"
    ):
        return [f"schema {path}: expected {kind}"]
    found: list[str] = []
    if isinstance(value, str):
        if len(value) < node.get("minLength", 0) or len(value) > node.get("maxLength", 10**9):
            found.append(f"schema {path}: string length out of range")
        if "pattern" in node and not re.search(node["pattern"], value):
            found.append(f"schema {path}: does not match pattern")
    elif isinstance(value, int | float):
        if value < node.get("minimum", value) or value > node.get("maximum", value):
            found.append(f"schema {path}: number out of range")
    elif isinstance(value, list):
        if len(value) < node.get("minItems", 0):
            found.append(f"schema {path}: too few items")
        for i, item in enumerate(value):
            found += _check(item, node.get("items", {}), root, f"{path}/{i}")
    elif isinstance(value, dict):
        props = node.get("properties", {})
        found += [f"schema {path}: missing {k}" for k in node.get("required", []) if k not in value]
        if len(value) < node.get("minProperties", 0):
            found.append(f"schema {path}: too few properties")
        extra = node.get("additionalProperties", True)
        for key, item in value.items():
            if key in props:
                found += _check(item, props[key], root, f"{path}/{key}")
            elif extra is False:
                found.append(f"schema {path}: unexpected {key}")
            elif isinstance(extra, dict):
                found += _check(item, extra, root, f"{path}/{key}")
    return found


def validate_manifest(manifest: Mapping[str, Any]) -> list[str]:
    """Return schema violations followed by freeze gaps; empty means valid and frozen."""
    schema = load_schema()
    return sorted(_check(manifest, schema, schema, "")) + list(check_freeze(manifest)["gaps"])


def _versions(manifest: Mapping[str, Any]) -> dict[str, str]:
    versions = manifest.get("versions", {})
    return {key: str(versions.get(key)) for key in VERSION_KEYS}


def run_eval(manifest: Mapping[str, Any], predictions: Mapping[str, Any]) -> dict[str, Any]:
    """Score predictions against a frozen manifest; refuse when the manifest is not valid."""
    problems = validate_manifest(manifest)
    freeze = check_freeze(manifest)
    base: dict[str, Any] = dict(
        manifest_digest=freeze["manifest_digest"], versions=_versions(manifest), note=NOTE
    )
    if problems:
        return dict(base, outcome="not_frozen", problems=problems)
    held = manifest["held_out"]
    expected: Mapping[str, str] = held["expected"]
    declared = list(held["critical_errors"])
    errors = [f"prediction for unknown case {c}" for c in sorted(set(predictions) - set(expected))]
    correct = 0
    seen = {name: 0 for name in declared}
    for case, want in expected.items():
        got = predictions.get(case)
        if not isinstance(got, Mapping):
            continue
        correct += got.get("answer") == want
        for name in got.get("critical_errors", []):
            if name in seen:
                seen[name] += 1
            else:
                errors.append(f"case {case} reports undeclared critical error {name}")
    total = len(expected)
    accuracy = correct / total
    limits = manifest["thresholds"]
    smallest = min(len(members) for members in manifest["cohorts"].values())
    observed_critical = sum(seen.values())
    thresholds = [
        dict(
            name="max_critical_misses",
            limit=limits["max_critical_misses"],
            observed=observed_critical,
            passed=observed_critical <= limits["max_critical_misses"],
        ),
        dict(
            name="min_accuracy",
            limit=limits["min_accuracy"],
            observed=round(accuracy, 6),
            passed=accuracy >= limits["min_accuracy"],
        ),
        dict(
            name="min_sample_per_cohort",
            limit=limits["min_sample_per_cohort"],
            observed=smallest,
            passed=smallest >= limits["min_sample_per_cohort"],
        ),
    ]
    critical = [dict(name=n, observed=seen[n], passed=seen[n] == 0) for n in sorted(seen)]
    passed = not errors and all(t["passed"] for t in thresholds + critical)
    return dict(
        base,
        outcome="pass" if passed else "fail",
        denominator=total,
        correct=correct,
        thresholds=thresholds,
        critical_errors=critical,
        input_errors=sorted(errors),
    )


def verify_recorded(manifest: Mapping[str, Any], recorded: Mapping[str, Any]) -> dict[str, Any]:
    """A recorded result is valid only for the exact manifest digest and versions it ran against."""
    reasons = []
    current = _versions(manifest)
    before = recorded.get("versions")
    for key in VERSION_KEYS:
        was = before.get(key) if isinstance(before, Mapping) else None
        if was != current[key]:
            reasons.append(f"versions.{key} changed from {was} to {current[key]}")
    if recorded.get("manifest_digest") != check_freeze(manifest)["manifest_digest"]:
        reasons.append("manifest digest changed")
    return dict(outcome="invalidated" if reasons else "valid", reasons=reasons)
