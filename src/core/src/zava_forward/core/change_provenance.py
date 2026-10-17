"""Explicit caller sources and atomic evidence for single-record changes."""

import json
from collections.abc import Iterator
from contextlib import contextmanager
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any

from . import projection

Record = dict[str, Any]


def _actor(store: Any, user: Record) -> Record:
    email = user.get("email")
    actor = None
    if isinstance(email, str):
        if hasattr(store, "db"):
            with store.dblock:
                row = store.db.execute(
                    "SELECT body FROM staff WHERE email=?", (email.lower(),)
                ).fetchone()
            actor = json.loads(row[0]) if row else None
        else:
            actor = store.staff.get(email.lower())
    if (
        not actor
        or actor.get("role") not in projection.STAFF_ROLES
        or not isinstance(actor.get("name"), str)
        or not actor["name"].strip()
        or any(actor.get(k) != user.get(k) for k in ("email", "code", "name", "role", "oid"))
    ):
        raise PermissionError("Current registered named staff must record this change.")
    return deepcopy(actor)


def validate_sql(store: Any) -> None:
    """Recheck the recorded actor under the existing SQL writer transaction."""
    context = getattr(store.local, "change_validation", None)
    if context is not None and _actor(store, context["user"]) != context["actor"]:
        raise PermissionError("Staff authority changed. Reload before recording this change.")


def document_refs(case: Record) -> list[Record]:
    return [
        {k: deepcopy(doc.get(k)) for k in ("id", "name", "kind", "content_sha256", "version")}
        for doc in case["documents"]
    ]


def ownership(case: Record) -> Record:
    return {k: deepcopy(case.get(k)) for k in ("owner", "owner_code", "owner_role", "waiting_on")}


@contextmanager
def operation(
    store: Any,
    user: Record,
    case_id: str,
    action: str,
    metadata: object,
    history: str,
) -> Iterator[tuple[Record, Record]]:
    from .store import ConflictError

    with store.lock:
        before = None
        saved = False
        try:
            actor = _actor(store, user)
            if not isinstance(metadata, dict):
                raise ValueError(
                    "Enter the source reference, source version and reason for this change."
                )
            if {"actor", "at", "version", "changes"} & metadata.keys():
                raise ValueError(
                    "Actor, time, change version and old/new values are recorded by the server."
                )
            supplied = {}
            for key, label, limit in (
                ("source", "source reference", 200),
                ("source_version", "source version", 100),
                ("reason", "reason for this change", 300),
            ):
                value = metadata.get(key)
                if not isinstance(value, str) or not value.strip() or len(value) > limit:
                    raise ValueError(f"Enter the {label}, from 1 to {limit} characters.")
                supplied[key] = value.strip()
            case = store._case(case_id)
            if history == "handoff_history":
                version = metadata.get("handoff_version")
                if type(version) is not int or version < 0:
                    raise ValueError("Reload the case to supply its current handoff version.")
                if version != len(case.get(history, [])):
                    raise ConflictError("The handoff changed. Reload and check the current offer.")
            before = deepcopy(case)
            event = dict(
                supplied,
                actor={k: actor.get(k) for k in ("email", "code", "name", "role", "oid")},
                at=datetime.now(UTC).isoformat(),
                version=len(case.get(history, [])) + 1,
                changes={},
            )
            yield case, event
            # A source scan can save and clear SQL touched-case tracking.
            case = store._case(case_id)
            case.setdefault(history, []).append(deepcopy(event))
            detail = json.dumps(event, sort_keys=True, separators=(",", ":"))
            if hasattr(store, "local"):
                store.local.change_validation = dict(user=user, actor=actor)
            if hasattr(store, "db"):
                store.audit(actor["email"], action, case_id, detail)
                store.save()
            else:
                store.save()
                saved = True
                store.audit(actor["email"], action, case_id, detail)
        except Exception as error:
            if hasattr(store, "db"):
                with store.dblock:
                    store._discard()
            elif before is not None:
                store.cases[case_id].clear()
                store.cases[case_id].update(before)
                if saved:
                    store.save()
            reason = (
                str(error)
                if isinstance(error, (ValueError, PermissionError, ConflictError))
                else "Change failed; the outcome may be unknown. Reload before retrying."
            )
            store.audit(
                str(user.get("email", "unknown")),
                action + "_rejected",
                case_id,
                json.dumps(dict(error=type(error).__name__, reason=reason)),
            )
            raise
        finally:
            if hasattr(store, "local"):
                store.local.change_validation = None
