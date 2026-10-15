"""Read-only, source-backed shared context; never an approval for a home."""

from copy import deepcopy
from decimal import Decimal, InvalidOperation
from typing import Any

from .projection import FINANCE_VIEW, STAFF_ROLES

Record = dict[str, Any]
CATEGORIES = ("systems", "dependencies", "holds", "works", "costs")


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Building data needs {label}.")
    return value


def _fields(row: object, fields: set[str], label: str) -> Record:
    if not isinstance(row, dict) or set(row) != fields:
        raise ValueError(f"Building {label} must contain exactly: {', '.join(sorted(fields))}.")
    return row


def _scope(value: object, known: set[str], label: str) -> None:
    if value is None:
        return
    if (
        not isinstance(value, list)
        or any(not isinstance(item, str) or item not in known for item in value)
        or len(value) != len(set(value))
    ):
        raise ValueError(f"Building {label} must be null or a unique list of valid explicit IDs.")


def record(data: Record, cases: Record, building_id: str) -> Record:
    registry = data.get("buildings", [])
    if not isinstance(registry, list):
        raise ValueError("Building registry must be a list.")
    ids = [_text(b.get("id"), "an ID") for b in registry if isinstance(b, dict)]
    if len(ids) != len(registry) or len(set(ids)) != len(ids):
        raise ValueError("Building registry needs unique IDs.")
    found: Record | None = next((b for b in registry if b["id"] == building_id), None)
    if found is None:
        raise KeyError(building_id)
    _fields(found, {"id", "name", "version", "source", *CATEGORIES}, "record")
    for key in ("id", "name", "source"):
        _text(found[key], key)
    if type(found["version"]) is not int or found["version"] < 1:
        raise ValueError("Building version must be a positive integer.")
    homes = {cid for cid, c in cases.items() if c.get("building_id") == building_id}
    packages = {p["id"] for p in data.get("procurement", {}).get("packages", [])}
    work_ids: set[str] = set()
    for category in CATEGORIES:
        rows = found[category]
        if rows is None:
            continue
        if not isinstance(rows, list):
            raise ValueError(f"Building {category} must be null (unknown) or a list.")
        seen: set[str] = set()
        for row in rows:
            fields = {"id", "label", "source"}
            if category in ("dependencies", "holds", "works"):
                fields |= {"status", "owner", "case_ids", "package_ids"}
            elif category == "costs":
                fields = {"id", "work_id", "amount_gbp", "source"}
            _fields(row, fields, category)
            rid = _text(row["id"], f"{category} ID")
            if rid in seen:
                raise ValueError(f"Building {category} IDs must be unique.")
            seen.add(rid)
            _text(row["source"], f"{category} source reference")
            if category != "costs":
                _text(row["label"], f"{category} label")
            if category in ("dependencies", "holds", "works"):
                _text(row["owner"], f"{category} owner")
                statuses = (
                    ("Proposed", "In progress", "Completed")
                    if category == "works"
                    else (
                        "Open",
                        "Resolved",
                        "Unknown",
                    )
                )
                if row["status"] not in statuses:
                    raise ValueError(f"Building {category} has an invalid recorded status.")
                _scope(row["case_ids"], homes, "case scope")
                _scope(row["package_ids"], packages, "package scope")
            if category == "works":
                work_ids.add(rid)
            if category == "costs":
                if _text(row["work_id"], "shared work ID") not in work_ids:
                    raise ValueError("Building cost needs an explicit shared work ID.")
                amount = row["amount_gbp"]
                if not isinstance(amount, str):
                    raise ValueError("Building GBP cost must be an exact decimal string.")
                try:
                    money = Decimal(amount)
                except InvalidOperation as exc:
                    raise ValueError("Building GBP cost is invalid.") from exc
                if (
                    not money.is_finite()
                    or money < 0
                    or money > Decimal("100000000")
                    or money != money.quantize(Decimal("0.01"))
                ):
                    raise ValueError("Building GBP cost must be finite, nonnegative, with pence.")
    return found


def blockers(data: Record, cases: Record, home: Record, package_id: str | None = None) -> list[str]:
    building_id = home.get("building_id")
    if not building_id:
        return []
    try:
        building = record(data, cases, building_id)
    except KeyError:
        return [
            f"Building {building_id}: shared context is unknown. Owner: {home['owner']}. "
            "Next action: obtain the source-backed building record."
        ]
    except ValueError as exc:
        return [
            f"Building {building_id}: {exc} Owner: {home['owner']}. "
            "Next action: correct the source-backed building record."
        ]
    reasons = []
    for category in ("dependencies", "holds"):
        rows = building[category]
        if rows is None:
            reasons.append(
                f"Building {building_id}: {category} are unknown. Owner: {home['owner']}. "
                "Next action: obtain accountable human review."
            )
            continue
        for row in rows:
            homes, packages = row["case_ids"], row["package_ids"]
            if packages == []:
                continue
            if homes is not None and home["id"] not in homes:
                continue
            if package_id is not None and packages is not None and package_id not in packages:
                continue
            if row["status"] == "Resolved" and homes is not None and packages is not None:
                continue
            reasons.append(
                f"Building {building_id} {category}: {row['label']} "
                f"({row['status']}; applicability "
                f"{'unknown' if homes is None or packages is None else 'explicit'}). "
                f"Owner: {row['owner']}. Next action: obtain accountable human review."
            )
    return reasons


def view(data: Record, cases: Record, building_id: str, user: Record) -> Record:
    if user.get("role") not in STAFF_ROLES:
        raise PermissionError("Only authorised staff can view shared building context.")
    result = deepcopy(record(data, cases, building_id))
    if user["role"] not in FINANCE_VIEW:
        result.pop("costs")
        result["costs_restricted"] = True
    result["homes"] = [
        {"id": cid, "stage": c["stage"], "closed": c["closed"]}
        for cid, c in sorted(cases.items())
        if c.get("building_id") == building_id
    ]
    result["notice"] = (
        "Source-backed shared context only. Home evidence, consent, approvals, allocations "
        "and outcomes stay on each home. Shared identity does not establish package applicability. "
        "No safety release, works instruction, payment or resident contact is available here."
    )
    return result
