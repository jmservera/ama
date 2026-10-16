"""Private roster format and tenant-person checks shared by setup helpers."""

from __future__ import annotations

import re
import uuid
from typing import Any


def roster_rows(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        if (
            type(value.get("version")) is not int
            or value["version"] != 1
            or type(value.get("seed")) is not int
            or value["seed"] < 0
        ):
            raise ValueError("Generated roster version or seed is invalid.")
        value = value.get("staff")
    if not isinstance(value, list) or not value or not all(isinstance(r, dict) for r in value):
        raise ValueError("Roster must contain a nonempty array of staff objects.")
    return value


def person(user: dict[str, Any]) -> dict[str, str]:
    if (
        user.get("@odata.type", "#microsoft.graph.user") != "#microsoft.graph.user"
        or user.get("accountEnabled") is not True
        or user.get("userType") != "Member"
    ):
        raise ValueError("Selected account is not an enabled member person.")
    name, upn = user.get("displayName"), user.get("userPrincipalName")
    if (
        not isinstance(name, str)
        or not name.strip()
        or not isinstance(upn, str)
        or not upn.strip()
        or len(upn) > 200
        or "@" not in upn
    ):
        raise ValueError("Selected account is missing a usable display name or UPN.")
    resource = r"(?:^|[^a-z])(?:room|desk|workspace|wksp|shared|equipment|service|svc)(?:[^a-z]|$)"
    if (
        "confrm" in name.lower()
        or re.search(resource, name.lower())
        or re.search(resource, upn.split("@")[0].lower())
    ):
        raise ValueError("Resource, shared mailbox and service accounts cannot be staff.")
    principal = str(uuid.UUID(user["id"]))
    if principal == str(uuid.UUID(int=0)):
        raise ValueError("Selected account has an invalid identifier.")
    return {"oid": principal, "name": name, "email": upn.lower()}


def staff_candidates(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Expose only position metadata, never existing names, UPNs or object IDs."""
    return [
        {
            "code": row["code"],
            "role": row["role"],
            "bound": bool(row.get("oid")),
            **({"contractor": row.get("contractor")} if row["role"] == "Contractor" else {}),
        }
        for row in rows
    ]
