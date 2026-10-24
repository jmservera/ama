"""Entra-authoritative staff identity (issue 360).

A signed-in principal is identified only by its canonical tenant and object id.
The derived code and pseudonymous email are the stable authorization and audit
keys. Display name and email claims are never used to authorize anything.
"""
import hashlib
import re
import uuid
from copy import deepcopy
from typing import Any

SOURCE = "entra"
ENTRA_EMAIL = re.compile(r"e-[0-9a-f]{12}@entra\.invalid")
_CONTROL = re.compile(r"[\x00-\x1f\x7f-\x9f\u200b-\u200f\u2028-\u202e\u2066-\u2069\ufeff]")


def canonical_guid(value: Any) -> str | None:
    """Return the lowercase canonical UUID text, or None when the value is not a UUID."""
    if not isinstance(value, str):
        return None
    try:
        parsed = uuid.UUID(value.strip())
    except ValueError:
        return None
    return str(parsed) if str(parsed) == value.strip().lower() else None


def code_for(tid: str, oid: str) -> str:
    return "E-" + hashlib.sha256(f"{tid}:{oid}".encode()).hexdigest()[:12]


def email_for(tid: str, oid: str) -> str:
    return code_for(tid, oid).lower() + "@entra.invalid"


def display(value: Any, limit: int = 120) -> str:
    """Strip control characters and cap a display-only claim."""
    if not isinstance(value, str):
        return ""
    return _CONTROL.sub("", value).strip()[:limit]


def principal(tid: str, oid: str, role: str, *, name: str = "", email: str = "",
              roles: tuple[str, ...] = (), app_admin: bool = False, view_only: bool = False, provider: str = "trusted-proxy") -> dict[str, Any]:
    tid, oid = canonical_guid(tid), canonical_guid(oid)
    if not tid or not oid:
        raise ValueError("A tenant and object id are required.")
    code = code_for(tid, oid)
    return dict(code=code, name=display(name) or code, email=email_for(tid, oid), role=role, oid=oid, tid=tid,
                identity_source=SOURCE, display_email=display(email, 200), app_admin=bool(app_admin), view_only=bool(view_only),
                app_roles=sorted(roles), auth_provider=provider)


def is_entra(user: Any) -> bool:
    return isinstance(user, dict) and user.get("identity_source") == SOURCE


def verified(user: dict[str, Any]) -> dict[str, Any] | None:
    """Return a copy of an Entra principal only if its derived keys still match its tenant and object id."""
    if not is_entra(user):
        return None
    tid, oid = canonical_guid(user.get("tid")), canonical_guid(user.get("oid"))
    if (not tid or not oid or user.get("code") != code_for(tid, oid)
            or user.get("email") != email_for(tid, oid) or user.get("oid") != oid):
        return None
    return deepcopy(user)
