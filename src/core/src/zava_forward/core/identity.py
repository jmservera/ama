"""Entra-authoritative staff identity (issue 360).

A signed-in principal is identified only by its canonical tenant and object id.
The derived code and pseudonymous email are the stable authorization and audit
keys. Display name and email claims are never used to authorize anything.
"""
import hashlib
import json
import re
import threading
import uuid
from copy import deepcopy
from typing import Any

SOURCE = "entra"
ADMIN_ROLE_NAME = "Application Administrator"
REGISTRY_KEY = "entra_people"
REGISTRY_LIMIT = 2000
LEGACY_TENANT_KEY = "legacy_roster_tenant"
_json_lock = threading.RLock()
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
        with store.dblock:
            return [json.loads(r[0]) for r in store.db.execute("SELECT body FROM staff")]
    return list(store.staff.values())


def _meta(store: Any, key: str) -> Any:
    if hasattr(store, "db"):
        with store.dblock:
            row = store.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else None
    return store.data.get(key)


def legacy_tenant(store: Any) -> str | None:
    """Tenant that verifiably owns roster rows carrying no tenant id (store provenance; never assumed)."""
    try:
        value = _meta(store, LEGACY_TENANT_KEY)
    except Exception:
        return None
    return canonical_guid(value)


def key_of(tid: str, oid: str) -> str:
    return f"{tid}:{oid}"


def matches(store: Any, tid: str, oid: str) -> list[dict[str, Any]]:
    """Enabled roster rows for exactly this verified tenant and object id (immutable keys, never an email).

    A row naming another tenant never matches. A row without a tenant matches only the tenant the store
    records as owning legacy rows.
    """
    legacy = legacy_tenant(store)
    out = []
    for r in _rows(store):
        if not isinstance(r, dict) or r.get("disabled") or r.get("oid") != oid or canonical_guid(r.get("oid")) != oid:
            continue
        row_tid = r.get("tid")
        if row_tid in (None, ""):
            if legacy == tid:
                out.append(r)
        elif canonical_guid(row_tid) == tid and row_tid == tid:
            out.append(r)
    return out


def bind(store: Any, user: dict[str, Any]) -> dict[str, Any] | None:
    """Post-authentication business-identity continuity; it can never grant a role or capability.

    A verified tenant and object id that uniquely match an existing roster row keep that row's code, email
    and name, so legacy ownership, handoffs, named owners and scoped authorities continue. Contractors also
    need exactly one company-bound row or are refused. Staff continuity fails soft to the derived identity;
    person independence is judged on the canonical tenant and object id (see `canonical`), so the derived
    identity is never a different person.
    """
    u = verified(user)
    if not u:
        return None
    contractor = u.get("role") == "Contractor"
    if u.get("view_only") and not contractor:
        return u
    try:
        rows = matches(store, u["tid"], u["oid"])
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


def _aliases(u: dict[str, Any]) -> list[str]:
    values = [u.get("code"), u.get("email"), u.get("derived_code"), u.get("derived_email")]
    return sorted({" ".join(v.split()).casefold() for v in values if isinstance(v, str) and v.strip()})


def _entry(u: dict[str, Any], old: dict[str, Any] | None) -> dict[str, Any]:
    aliases = sorted(set(_aliases(u)) | set((old or {}).get("aliases") or []))
    return dict(key=key_of(u["tid"], u["oid"]), tid=u["tid"], oid=u["oid"], code=u["code"], email=u["email"], name=u["name"],
                role=u["role"], bound=bool(u.get("bound")), aliases=aliases, identity_source=SOURCE,
                auth_provider=u.get("auth_provider"))


def link(store: Any, user: dict[str, Any], *, strict: bool = False) -> bool:
    """Record the verified person's aliases and last-seen business identity in one serialized transaction.

    Read, merge and write happen together, so concurrent sign-ins each keep their own entry. Aliases are
    append-only, which keeps author and approver independence stable if a roster binding is later disabled or
    unreadable. Access never depends on this record; with strict=True a failure raises for callers that need it.
    """
    u = verified(user)
    if not u or u.get("view_only") or u.get("role") == "Contractor":
        return False
    key = key_of(u["tid"], u["oid"])
    try:
        if _merge(_registry(store), key, u) is None:
            return True  # already recorded: avoid a write transaction on every request
        if hasattr(store, "db"):
            with store.dblock:
                store.db.execute("BEGIN IMMEDIATE")
                try:
                    row = store.db.execute("SELECT value FROM meta WHERE key=?", (REGISTRY_KEY,)).fetchone()
                    current = json.loads(row[0]) if row else {}
                    merged = _merge(current, key, u)
                    if merged is not None:
                        store._meta_set(REGISTRY_KEY, json.dumps(merged))
                    store.db.execute("COMMIT")
                except BaseException:
                    store.db.execute("ROLLBACK")
                    raise
        else:
            with _json_lock:
                merged = _merge(store.data.get(REGISTRY_KEY, {}), key, u)
                if merged is not None:
                    store.data[REGISTRY_KEY] = merged
                    store.save()
        return True
    except Exception:
        if strict:
            raise
        return False


def _merge(current: Any, key: str, u: dict[str, Any]) -> dict[str, Any] | None:
    current = current if isinstance(current, dict) else {}
    if key not in current and len(current) >= REGISTRY_LIMIT:
        raise OverflowError("identity registry is full")
    entry = _entry(u, current.get(key))
    return None if current.get(key) == entry else dict(current, **{key: entry})


def _registry(store: Any) -> dict[str, Any]:
    try:
        value = _meta(store, REGISTRY_KEY)
    except Exception:
        return {}
    return value if isinstance(value, dict) else {}


def _recipient(e: dict[str, Any]) -> dict[str, Any]:
    return dict(code=e["code"], email=e["email"], name=e["name"], role=e["role"], oid=e["oid"], tid=e["tid"],
                identity_source=SOURCE, auth_provider=e.get("auth_provider"))


def people(store: Any) -> list[dict[str, Any]]:
    """Signed-in Entra staff without a roster binding, selectable as handoff recipients."""
    return [_recipient(e) for e in _registry(store).values()
            if isinstance(e, dict) and not e.get("bound") and isinstance(e.get("code"), str)]


def person(store: Any, alias: Any) -> dict[str, Any] | None:
    """The recipient a recorded alias refers to, with its last-seen business identity."""
    if not isinstance(alias, str):
        return None
    wanted = " ".join(alias.split()).casefold()
    for e in _registry(store).values():
        if isinstance(e, dict) and wanted in (e.get("aliases") or []) and isinstance(e.get("code"), str):
            return _recipient(e)
    return None


def canonical(store: Any, name: Any, *, strict: bool = False) -> str:
    """Canonical person key for a recorded alias, else the normalized text.

    Two names for one verified tenant and object id (legacy and derived) canonicalize identically, so
    independence checks cannot be passed by switching aliases. With strict=True the registry must be readable.
    """
    text = " ".join(str(name).split()).casefold()
    try:
        registry = _meta(store, REGISTRY_KEY)
    except Exception:
        if strict:
            raise
        registry = None
    for e in (registry or {}).values() if isinstance(registry, dict) else ():
        if isinstance(e, dict) and text in (e.get("aliases") or []):
            return "entra:" + str(e.get("key"))
    return text


def distinct(store: Any, actor: Any, author: Any) -> bool:
    """True only when the actor is demonstrably a different person from the recorded author.

    Storage availability and resolution completeness are separate: an unreadable registry raises, and an
    author who cannot be tied to a person (no alias record, no roster row with a different verified object
    id) is unresolved and never counts as distinct from an Entra actor. Plain names are compared as text.
    """
    a, b = canonical(store, actor, strict=True), canonical(store, author, strict=True)
    if not a.startswith("entra:"):
        return a != b and not ENTRA_EMAIL.fullmatch(a)
    if b.startswith("entra:"):
        return a != b
    oid = a.rsplit(":", 1)[-1]
    text = " ".join(str(author).split()).casefold()
    found = [r for r in _rows(store) if isinstance(r, dict) and text in (
        " ".join(str(r.get("email", "")).split()).casefold(), " ".join(str(r.get("code", "")).split()).casefold())]
    return len(found) == 1 and canonical_guid(found[0].get("oid")) not in (None, oid) and found[0].get("oid") != oid
