"""Pure RAI record validation and selection; no store or workload dependencies."""

from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Mapping, Sequence
from typing import Any

EVALUATION_VERSION = "task-release-evaluation-v1"
CHANGE_TRIGGERS = (
    "intended_use",
    "model",
    "prompt",
    "policy",
    "data",
    "evidence",
    "permissions",
)
AUTHORITY_GAP = (
    "OQ-017: named live release, residual-risk acceptance, suspension and restart "
    "holders and competent-review delegations are not evidenced."
)


AUTHORITY_ROLES = (
    "release",
    "residual-risk acceptance",
    "suspension",
    "restart",
)


def authority_register() -> list[dict[str, Any]]:
    """Itemise each OQ-017 authority; every holder stays unset until a human names one."""
    return [
        {"authority": role, "holder": None, "status": "gap", "reference": "OQ-017"}
        for role in AUTHORITY_ROLES
    ]


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    ).hexdigest()


def named(value: object) -> bool:
    return (
        isinstance(value, str)
        and 0 < len(value.strip()) <= 400
        and value.strip().casefold() not in {"unknown", "unavailable", "none", "unapproved"}
    )


def strings(value: object) -> bool:
    return isinstance(value, list) and 1 <= len(value) <= 20 and all(named(v) for v in value)


def missing_contract(record: Mapping[str, Any], task: Mapping[str, Any]) -> list[str]:
    missing = [
        key
        for key in ("release_version", "accountable_owner", "impact_assessment")
        if not named(record.get(key))
    ]
    for field, expected in (
        ("intended_use", task.get("intended_use")),
        ("prohibited_uses", task.get("prohibited_uses")),
        ("affected_stakeholders", task.get("affected")),
    ):
        if record.get(field) != expected:
            missing.append(field)
    if record.get("material_change_triggers") != list(CHANGE_TRIGGERS):
        missing.append("material_change_triggers")
    if not strings(record.get("evidence")) or record.get("evaluation_decision") != "Pass":
        missing.append("approved evaluation evidence")
    if record.get("residual_risk_decision") != "Accept" or not named(
        record.get("residual_risk_note")
    ):
        missing.append("residual-risk acceptance")
    approver = record.get("approver")
    if not isinstance(approver, dict) or not named(approver.get("email")):
        missing.append("named release approver")
    if record.get("evidence_class") not in ("constructed-fixture", "actual"):
        missing.append("evidence_class")
    if record.get("scope") != task.get("scope"):
        missing.append("scope")
    if not frozen_evaluation(record):
        missing.append("frozen evaluation summary")
    if not valid_consumption(record.get("consumption")):
        missing.append("consumption configuration")
    return missing


def frozen_evaluation(record: Mapping[str, Any]) -> bool:
    """The summary must be frozen to the exact evidence list the approver recorded."""
    summary = record.get("evaluation_summary")
    return (
        isinstance(summary, dict)
        and summary.get("evaluation_version") == EVALUATION_VERSION
        and summary.get("decision") == "Pass"
        and named(summary.get("summary"))
        and summary.get("evidence_digest") == digest(record.get("evidence"))
    )


def valid_consumption(value: object) -> bool:
    """Budget and alert configuration: bounded positive limits and a named alert contact."""
    if not isinstance(value, dict):
        return False

    def whole(key: str, low: int, high: int) -> bool:
        number = value.get(key)
        return isinstance(number, int) and not isinstance(number, bool) and low <= number <= high

    return (
        whole("max_calls", 1, 10**9)
        and whole("max_tokens", 1, 10**12)
        and whole("alert_threshold_percent", 1, 100)
        and named(value.get("alert_contact"))
    )


def attest_serving(record: Mapping[str, Any], returned: object) -> dict[str, Any]:
    """Exact comparison of the returned model with the released serving model."""
    expected = record.get("serving_model")
    if not named(returned):
        outcome = "unattested"
    else:
        outcome = "matched" if returned == expected else "mismatch"
    return {
        "expected": expected,
        "returned": returned if named(returned) else None,
        "outcome": outcome,
    }


def missing_binding(
    record: Mapping[str, Any],
    binding: Mapping[str, Any],
    bound: Sequence[str],
    now: float,
    live: bool,
) -> list[str]:
    missing = [key for key in bound if record.get(key) != binding.get(key)]
    expires = record.get("expires")
    if (
        not isinstance(expires, (int, float))
        or isinstance(expires, bool)
        or not math.isfinite(expires)
        or expires <= now
    ):
        missing.append("unexpired release")
    if not named(record.get("serving_model")):
        missing.append("serving_model")
    if live and (
        record.get("evidence_class") != "actual"
        or binding.get("model_version") in (None, "", "unattested")
        or record.get("serving_model") != binding.get("model_version")
    ):
        missing.append("actual authorisation with serving-version attestation")
    return missing


TRIGGER_KEYS = {
    "model": ("provider", "endpoint", "deployment", "model_version"),
    "prompt": ("prompt_version",),
    "policy": ("policy_version",),
    "data": ("data_version", "provenance_version"),
    "permissions": ("permission_version",),
    "evidence": (
        "registry_version",
        "schema_version",
        "task_contract_version",
        "evaluation_version",
    ),
}


def changed_triggers(
    record: Mapping[str, Any], task: Mapping[str, Any], binding: Mapping[str, Any]
) -> list[str]:
    """Material-change triggers that no longer match the current task and binding."""
    changed = [
        trigger
        for trigger, keys in TRIGGER_KEYS.items()
        if any(record.get(key) != binding.get(key) for key in keys)
    ]
    if any(
        record.get(field) != task.get(source)
        for field, source in (
            ("intended_use", "intended_use"),
            ("prohibited_uses", "prohibited_uses"),
            ("affected_stakeholders", "affected"),
            ("scope", "scope"),
        )
    ):
        changed.append("intended_use")
    return [t for t in CHANGE_TRIGGERS if t in changed]


def reference(record: Mapping[str, Any]) -> dict[str, str]:
    return {
        "id": str(record["id"]),
        "version": str(record["release_version"]),
        "digest": digest({k: v for k, v in record.items() if k != "invalidated"}),
    }


def select(
    records: Sequence[dict[str, Any]],
    task: Mapping[str, Any],
    binding: Mapping[str, Any],
    bound: Sequence[str],
    now: float,
    live: bool,
) -> tuple[dict[str, Any] | None, list[str]]:
    """Select only a fully valid record; malformed older records fail closed."""
    missing = ["approved, unexpired release record"]
    for rec in reversed(records):
        if rec.get("status") != "active":
            continue
        gaps = missing_contract(rec, task) + missing_binding(rec, binding, bound, now, live)
        if not gaps:
            return rec, []
        missing = gaps
    return None, missing
