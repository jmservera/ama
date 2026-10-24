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
ADMIN_ROLE_NAME = "Application Administrator"
REGISTRY_KEY = "entra_people"
REGISTRY_LIMIT = 2000
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
    """Return a copy of an Entra principal only if its keys still match its tenant and object id or its verified roster binding."""
    if not is_entra(user):
        return None
    tid, oid = canonical_guid(user.get("tid")), canonical_guid(user.get("oid"))
    if not tid or not oid or user.get("oid") != oid:
        return None
    bound = user.get("bound")
    if bound is None:
        keys = (code_for(tid, oid), email_for(tid, oid))
    elif isinstance(bound, dict) and isinstance(bound.get("code"), str) and isinstance(bound.get("email"), str):
        keys = (bound["code"], bound["email"])
    else:
        return None
    if user.get("code") != keys[0] or user.get("email") != keys[1]:
        return None
    return deepcopy(user)


def _rows(store: Any) -> list[dict[str, Any]]:
    if hasattr(store, "db"):
        import json
        with store.dblock:
            return [json.loads(r[0]) for r in store.db.execute("SELECT body FROM staff")]
    return list(store.staff.values())


def matches(store: Any, oid: str) -> list[dict[str, Any]]:
    """Enabled roster rows carrying exactly this verified object id (an immutable key, never an email)."""
    return [r for r in _rows(store)
            if isinstance(r, dict) and canonical_guid(r.get("oid")) == oid and r.get("oid") == oid and not r.get("disabled")]


def bind(store: Any, user: dict[str, Any]) -> dict[str, Any] | None:
    """Post-authentication business-identity continuity; it can never grant a role or capability.

    A verified tenant and object id that uniquely match an existing roster row keep that row's code, email
    and name, so legacy ownership, handoffs, named owners and scoped authorities continue. Contractors also
    need exactly one company-bound row or are refused. Staff continuity fails soft to the derived identity.
    """
    u = verified(user)
    if not u:
        return None
    contractor = u.get("role") == "Contractor"
    if u.get("view_only") and not contractor:
        return u
    try:
        rows = matches(store, u["oid"])
    except Exception:
        rows = None
    if contractor:
        if not rows or len(rows) != 1 or rows[0].get("role") != "Contractor" or not str(rows[0].get("contractor") or "").strip():
            return None
    elif not rows or len(rows) != 1 or rows[0].get("role") == "Contractor":
        return u
    row = rows[0]
    if not isinstance(row.get("code"), str) or not isinstance(row.get("email"), str) or not row["code"] or not row["email"]:
        return None if contractor else u
    email = row["email"].strip().lower()
    out = dict(u, code=row["code"], email=email, name=display(row.get("name")) or row["code"],
               bound=dict(code=row["code"], email=email), derived_code=u["code"], derived_email=u["email"])
    if contractor:
        out["contractor"] = row["contractor"]
    return out


def _registry(store: Any) -> dict[str, Any]:
    if hasattr(store, "db"):
        import json
        with store.dblock:
            row = store.db.execute("SELECT value FROM meta WHERE key=?", (REGISTRY_KEY,)).fetchone()
        value = json.loads(row[0]) if row else {}
    else:
        value = store.data.get(REGISTRY_KEY, {})
    return value if isinstance(value, dict) else {}


def people(store: Any) -> list[dict[str, Any]]:
    """Signed-in Entra staff without a roster row, selectable as handoff recipients."""
    return [dict(v) for v in _registry(store).values() if isinstance(v, dict)]


def person(store: Any, email: Any) -> dict[str, Any] | None:
    if not isinstance(email, str) or not ENTRA_EMAIL.fullmatch(email.strip().lower()):
        return None
    found = _registry(store).get(email.strip().lower())
    return dict(found) if isinstance(found, dict) else None


def register(store: Any, user: dict[str, Any]) -> None:
    """Record a signed-in, acting, unbound Entra staff member as a recipient. Best effort; never affects access."""
    u = verified(user)
    if not u or u.get("bound") or u.get("view_only") or u.get("role") == "Contractor":
        return
    entry = dict(code=u["code"], email=u["email"], name=u["name"], role=u["role"], oid=u["oid"], tid=u["tid"],
                 identity_source=SOURCE, auth_provider=u.get("auth_provider"))
    try:
        current = _registry(store)
        if current.get(u["email"]) == entry or (u["email"] not in current and len(current) >= REGISTRY_LIMIT):
            return
        current = dict(current, **{u["email"]: entry})
        if hasattr(store, "db"):
            import json
            with store.dblock:
                store.db.execute("BEGIN IMMEDIATE")
                try:
                    store._meta_set(REGISTRY_KEY, json.dumps(current))
                    store.db.execute("COMMIT")
                except BaseException:
                    store.db.execute("ROLLBACK")
                    raise
        else:
            store.data[REGISTRY_KEY] = current
            store.save()
    except Exception:
        return
