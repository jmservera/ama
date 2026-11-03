"""Versioned home case: explicit links and retained prior versions (issue 74).

A home case is one existing case record. Each recorded version freezes the
explicit links to its building, scheme, work packages and related records, with
who recorded it and why. Building-level shared context stays in `buildings`;
this module only references it. A shared building ID never carries a home's
evidence, decision or approval.
"""

import hashlib
import json
from copy import deepcopy
from typing import Any

from . import buildings, change_provenance, projection

Record = dict[str, Any]
HISTORY = "home_case_versions"
UNKNOWN = "Unknown"


def _staff(user: Record, action: str) -> None:
    if user.get("role") not in projection.STAFF_ROLES:
        raise PermissionError(f"Only authorised staff can {action}.")


def schemes(data: Record) -> dict[str, Record]:
    rows = data.get("schemes", [])
    if not isinstance(rows, list):
        raise ValueError("Scheme registry must be a list.")
    out: dict[str, Record] = {}
    for row in rows:
        if (
            not isinstance(row, dict)
            or set(row) != {"id", "name", "source"}
            or any(not isinstance(row[k], str) or not row[k].strip() for k in row)
            or row["id"] in out
        ):
            raise ValueError("Each scheme needs a unique ID, name and source reference.")
        out[row["id"]] = row
    return out


def current_version(case: Record) -> int:
    return len(case.get(HISTORY, []))


def links(data: Record, case: Record) -> Record:
    """Explicit references only; unknown links stay unknown and are never inferred."""
    orders = [
        w
        for w in data.get("procurement", {}).get("work_orders", [])
        if w.get("case_id") == case["id"]
    ]
    return {
        "building_id": case.get("building_id"),
        "scheme_id": case.get("scheme_id"),
        "work_packages": [
            {"package_id": w["package"], "work_order_id": w["id"]}
            for w in sorted(orders, key=lambda w: (w["package"], w["id"]))
        ],
        "hazard_ids": sorted(str(h.get("id", f"index-{i}")) for i, h in enumerate(case["hazards"])),
        "document_ids": sorted(str(d["id"]) for d in case.get("documents", [])),
        "quality_measures": sorted(str(q["measure"]) for q in case.get("quality", [])),
        "resident_service_ids": sorted(
            str(r["id"]) for r in case.get("service_requests", []) if "id" in r
        ),
        "provider": (case.get("contractor") or {}).get("name"),
        "finance": {
            "funding_reference": (case.get("funding") or {}).get("reference") or None,
            "shared_cost_ids": sorted(
                str(a["shared_cost_id"]) for a in case.get("cost_allocation", [])
            ),
        },
    }


def fingerprint(value: Record) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def record_version(store: Any, user: Record, case_id: str, metadata: object) -> Record:
    """Append the next immutable version; the caller must supply the version it read."""
    from .store import ConflictError

    _staff(user, "record a version")
    if not isinstance(metadata, dict):
        raise ValueError("Enter the source reference, source version and reason for this change.")
    expected = metadata.get("expected_version")
    if type(expected) is not int or expected < 0:
        raise ValueError("Reload the home case to supply its current version.")
    supplied = {k: v for k, v in metadata.items() if k != "expected_version"}
    scheme = supplied.pop("scheme_id", None)
    with change_provenance.operation(
        store, user, case_id, "home_case_version_recorded", supplied, HISTORY
    ) as (case, event):
        if current_version(case) != expected:
            raise ConflictError("The home case changed. Reload and check the current version.")
        if case["closed"]:
            raise ValueError("This case is closed; its versions are retained as they were.")
        old_scheme = case.get("scheme_id")
        if scheme is not None:
            if scheme not in schemes(store.data):
                raise ValueError("Choose a scheme from the scheme register.")
            case["scheme_id"] = scheme
        frozen = links(store.data, case)
        event["links"] = frozen
        event["links_sha256"] = fingerprint(frozen)
        event["stage"] = case["stage"]
        event["changes"] = {"scheme_id": {"old": old_scheme, "new": case.get("scheme_id")}}
        building_id = case.get("building_id")
        found = next(
            (b for b in store.data.get("buildings", []) if b.get("id") == building_id), None
        )
        event["building_record_version"] = found.get("version") if found else None
    return deepcopy(store._case(case_id)[HISTORY][-1])


def view(store: Any, user: Record, case_id: str) -> Record:
    """Per-home facts, shared building context and retained versions, kept apart."""
    _staff(user, "view a home case")
    with store.lock:
        case = store.cases.get(case_id)
        if case is None:
            raise KeyError(case_id)
        data = store.data
        live = links(data, case)
        prior = case.get(HISTORY, [])
        latest = prior[-1] if prior else None
        scheme = schemes(data).get(case.get("scheme_id") or "")
        building_id = case.get("building_id")
        shared: Record | None = None
        if building_id:
            try:
                shared = buildings.view(data, store.cases, building_id, user)
                shared.pop("homes", None)
            except (KeyError, ValueError):
                shared = {"id": building_id, "status": UNKNOWN}
        allocation = deepcopy(case.get("cost_allocation", []))
        if user["role"] not in projection.FINANCE_VIEW:
            allocation = None
        return {
            "case_id": case_id,
            "version": len(prior),
            "version_status": (
                "No version recorded yet" if latest is None else f"Version {len(prior)} recorded"
            ),
            "changed_since_version": latest is not None
            and latest["links_sha256"] != fingerprint(live),
            "links": live,
            "scheme": scheme or {"status": UNKNOWN},
            "home": {
                "decision": deepcopy(case["decision"]),
                "stage": case["stage"],
                "closed": case["closed"],
                "funding_confirmed": case["funding_ok"],
                "documents": [
                    {k: d.get(k) for k in ("id", "name", "kind")} for d in case.get("documents", [])
                ],
                "quality": [
                    {"measure": q["measure"], "state": q["state"]} for q in case.get("quality", [])
                ],
                "cost_allocation": allocation,
                "cost_allocation_restricted": allocation is None,
            },
            "building": shared,
            "versions": [deepcopy(v) for v in reversed(prior)],
            "notice": (
                "A shared building ID links records only. It does not transfer this home's "
                "evidence, consent, decision or approval to another home, or theirs to this one. "
                "Recording a version is not an approval, safety release, works instruction "
                "or payment. Every field is also available from the existing case and building "
                "screens if this view is unavailable."
            ),
        }
