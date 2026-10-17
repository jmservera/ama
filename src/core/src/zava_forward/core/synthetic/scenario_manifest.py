"""Offline integrity checks for the public constructed-scenario manifest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

PACK = Path("docs/reference/research/retrofit-synthetic-data")
PROFILE_IDS = (
    "asset-investment",
    "programme-coordinator",
    "retrofit-case-team",
    "assessor-designer",
    "housing-resident-engagement",
    "repairs-building-safety",
    "procurement-contracts",
    "provider-contractor",
    "quality-assurance",
    "finance-grants",
    "digital-auditor",
)
WORKFLOW_IDS = (
    "stock-safety-prioritisation",
    "technical-readiness",
    "resident-service",
    "procurement-release",
    "hazard-response",
    "quality-handover",
    "finance-grants-cash",
    "programme-handoffs",
    "portfolio-decisions",
)
SOURCES = {
    "workbench": "src/api/checks/workbench-manifest.json",
    "recipe": "src/api/checks/workbench_browser_check.py",
    "fixture": "src/core/tests/dataset.py",
    "navigation-tests": "src/api/tests/test_workbench.py",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(f"Scenario manifest: {message}")


def _public_file(root: Path, relative: str) -> Path:
    path = root / relative
    _require(path.resolve().is_relative_to(root.resolve()), f"non-public path: {relative}")
    _require(path.is_file(), f"missing public source: {relative}")
    return path


def _rows(value: Any, keys: set[str], label: str) -> list[dict[str, Any]]:
    _require(isinstance(value, list), f"{label} must be an array")
    result: list[dict[str, Any]] = []
    for row in value:
        _require(isinstance(row, dict) and set(row) == keys, f"malformed {label} row")
        _require(isinstance(row.get("id"), str), f"{label} row needs a string ID")
        result.append(row)
    return result


def validate_manifest(manifest: dict[str, Any], root: Path) -> None:
    """Reject incomplete or stale metadata against fixed public sources only.

    This verifies the current offline slice, not application or human acceptance.
    A future represented journey needs a new evidence contract, not a status edit
    against the partial IA sources accepted here.
    """
    for field in ("version", "iteration", "active_slice", "applicable_checks", "deferred_checks"):
        _require(bool(manifest.get(field)), f"missing {field}")
    _require(manifest.get("is_synthetic") is True, "is_synthetic must be true")
    _require(manifest.get("contains_real_data") is False, "contains_real_data must be false")
    _require(manifest.get("status") == "offline-coverage-audit", "unknown slice evidence contract")
    _require(
        manifest.get("inventory_authority")
        == {
            "source": (
                "docs/prds/zava-forward-retrofit-programme-demonstrator.md"
                "#profile-journey-contract-for-the-next-prototype"
            ),
            "roles": "provisional-product-roles",
            "journeys": "proposed-constructed-walkthroughs",
            "customer_approval": "not-established",
            "owner_approval": "not-established",
        },
        "inventory authority must retain PRD proposal status; coverage cannot grant approval",
    )

    sources = _rows(manifest.get("sources"), {"id", "path", "sha256"}, "sources")
    _require(
        len(sources) == len(SOURCES)
        and all(SOURCES.get(source["id"]) == source["path"] for source in sources)
        and len({source["id"] for source in sources}) == len(SOURCES),
        "source set must match the reviewed public fixture recipe",
    )
    for source in sources:
        digest = hashlib.sha256(_public_file(root, source["path"]).read_bytes()).hexdigest()
        _require(source.get("sha256") == digest, f"stale source hash: {source['path']}")

    workbench = json.loads(_public_file(root, SOURCES["workbench"]).read_text())
    expected_fixture = {
        "version": workbench["version"],
        "case_ids": workbench["all_case_ids"],
        "default_sort": workbench["default_sort"],
        "default_selection": workbench["default_selection"],
        "role_defaults": [
            {"role": role["role"], "ids": role["ids"], "count": len(role["ids"])}
            for role in workbench["roles"]
        ],
    }
    _require(manifest.get("fixture_contract") == expected_fixture, "fixture defaults/version drift")
    role_defaults = {
        role["email"]: {"ids": role["ids"], "count": len(role["ids"]), "selection": None}
        for role in workbench["roles"]
    }
    _require(
        manifest.get("profile_defaults")
        == {
            profile_id: role_defaults.get(profile.get("identity"))
            for profile_id, profile in zip(PROFILE_IDS, workbench["profiles"], strict=True)
        },
        "per-profile own-queue defaults drift; absent role must remain unknown",
    )
    for key, expected_ids, label in (
        ("profiles", PROFILE_IDS, "perspective"),
        ("workflows", WORKFLOW_IDS, "name"),
    ):
        entries = _rows(
            manifest.get(key),
            {"id", label, "status", "reason", "path", "safe_endpoint", "evidence_index"},
            key,
        )
        _require(
            [entry["id"] for entry in entries] == list(expected_ids),
            f"{key} must list each PRD-proposed inventory ID once in canonical order",
        )
        for index, entry in enumerate(entries):
            name = entry["id"]
            _require(
                entry["status"] in ("represented", "unavailable", "deferred"),
                f"{name}: invalid status",
            )
            # These sources contain partial IA, not approved deferrals or complete journeys.
            _require(
                entry["status"] == "unavailable",
                f"{name}: current evidence cannot support represented or deferred; "
                "supply a newly reviewed/versioned evidence contract first",
            )
            _require(
                isinstance(entry["reason"], str) and bool(entry["reason"].strip()),
                f"{name}: missing unavailable reason",
            )
            _require(
                isinstance(entry["path"], list)
                and bool(entry["path"])
                and all(isinstance(step, str) and step.strip() for step in entry["path"]),
                f"{name}: missing profile/workflow path",
            )
            _require(
                isinstance(entry["safe_endpoint"], str) and bool(entry["safe_endpoint"].strip()),
                f"{name}: missing safe endpoint or unknown",
            )
            _require(
                type(entry["evidence_index"]) is int and entry["evidence_index"] == index,
                f"{name}: incorrect partial IA evidence pointer",
            )
            evidence = workbench[key][index]
            _require(entry[label] == evidence[label], f"{name}: partial IA identity mismatch")

    inventory = json.loads(_public_file(root, str(PACK / "needs-inventory.json")).read_text())
    binding = manifest.get("inventory")
    if not isinstance(binding, dict):
        raise ValueError("Scenario manifest: inventory binding must be an object")
    _require(
        binding.get("path") == "needs-inventory.json"
        and inventory["scenario_manifest"] == "scenario-manifest.json",
        "broken reciprocal inventory link",
    )
    for field in ("version", "review_date"):
        _require(binding.get(field) == inventory[field], f"stale inventory {field}")
    _require(
        binding.get("reviewed_rows") == [row["id"] for row in inventory["needs"]],
        "inventory reviewed row set/order differs",
    )
    _require(
        binding.get("owner_review") == "pending"
        and binding.get("review_kind") == "automated-engineering-review"
        and inventory["status"] == "draft-awaiting-owner-review",
        "automated evidence cannot grant inventory approval",
    )
    _require(
        manifest.get("fixture_references") == list(SOURCES.values()), "fixture reference drift"
    )
    _require(
        manifest.get("evaluation_registry") == "src/agents/evals/registry.json",
        "reuse the existing #174 evaluation registry",
    )
