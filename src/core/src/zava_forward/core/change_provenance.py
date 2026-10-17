"""Explicit caller sources and atomic evidence for single-record changes."""

import json
import logging
import os
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


class CommittedOutcomeError(RuntimeError):
    """The change committed, but its refreshed view or acknowledgement failed."""


def append_event(
    case: Record, history: str, actor: Record, action: str, source: str, **values: Any
) -> Record:
    rows = case.setdefault(history, [])
    at = values.pop("at", None) or datetime.now(UTC).isoformat(timespec="microseconds")
    event = dict(
        values,
        schema="controlled-event/v1",
        event_type=action,
        version=len(rows) + 1,
        at=at,
        actor={k: actor.get(k) for k in ("email", "code", "name", "role", "oid")},
        receiving_owner=ownership(case),
        source=source,
        source_version="1",
    )
    rows.append(event)
    return event


@contextmanager
def controlled(store: Any, user: Record, case_id: str) -> Iterator[tuple[Record, Record]]:
    """Reuse the case writer and registered-actor guard, quarantining failed audit."""
    with store.lock:
        sql = hasattr(store, "db")
        if sql:
            store._touched()
        prior = list(store.local.pending) if sql else []
        validation = getattr(store.local, "change_validation", None) if sql else None
        before = None
        snapshot = None
        audit_size = (
            None
            if sql
            else (os.path.getsize(store.audit_path) if os.path.exists(store.audit_path) else 0)
        )
        audit_head = None if sql else store.last_hash
        try:
            actor = _actor(store, user)
            case = store._case(case_id)
            before = deepcopy(case)
            snapshot = store._snap.get(case_id) if sql else None
            if sql:
                store.local.change_validation = dict(user=deepcopy(user), actor=actor)
            yield case, actor
        except BaseException as error:
            if sql:
                if before is not None and store._snap.get(case_id) != snapshot:
                    logging.getLogger(__name__).exception(
                        "Controlled change committed; refresh failed"
                    )
                    raise CommittedOutcomeError(
                        "The change was committed, but its current view could not refresh. "
                        "Reload and check its history before retrying."
                    ) from error
                try:
                    with store.dblock:
                        store._discard(prior)
                except Exception:
                    error.add_note("Change recovery failed; reload to establish the outcome.")
                    logging.getLogger(__name__).exception("Controlled change SQL recovery failed")
            elif before is not None:
                case.clear()
                case.update(before)
                try:
                    if os.path.exists(store.audit_path):
                        with open(store.audit_path, "r+b") as audit:
                            audit.truncate(audit_size)
                    store.last_hash = audit_head
                    from .store import Store

                    Store.save(store)
                except Exception as recovery_error:
                    error.add_note("Change restoration failed; the durable outcome may be unknown.")
                    logging.getLogger(__name__).exception("Controlled change JSON recovery failed")
                    raise RuntimeError(
                        "Change restoration failed; reload to establish the durable outcome."
                    ) from recovery_error
            raise
        finally:
            if sql:
                store.local.change_validation = validation


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
        try:
            with controlled(store, user, case_id) as (case, actor):
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
                if history == "handoff_history":
                    version = metadata.get("handoff_version")
                    if type(version) is not int or version < 0:
                        raise ValueError("Reload the case to supply its current handoff version.")
                    if version != len(case.get(history, [])):
                        raise ConflictError(
                            "The handoff changed. Reload and check the current offer."
                        )
                event = dict(
                    supplied,
                    actor={k: actor.get(k) for k in ("email", "code", "name", "role", "oid")},
                    at=datetime.now(UTC).isoformat(timespec="microseconds"),
                    version=len(case.get(history, [])) + 1,
                    receiving_owner=ownership(case),
                    event_type=action,
                    changes={},
                )
                yield case, event
                # A source scan can save and clear SQL touched-case tracking.
                case = store._case(case_id)
                event["receiving_owner"] = ownership(case)
                case.setdefault(history, []).append(deepcopy(event))
                detail = json.dumps(event, sort_keys=True, separators=(",", ":"))
                if hasattr(store, "db"):
                    store.audit(actor["email"], action, case_id, detail)
                    store.save()
                else:
                    store.save()
                    store.audit(actor["email"], action, case_id, detail)
        except CommittedOutcomeError:
            raise
        except (ValueError, PermissionError, ConflictError) as error:
            store.audit(
                str(user.get("email", "unknown")),
                action + "_rejected",
                case_id,
                json.dumps(dict(error=type(error).__name__, reason=str(error))),
            )
            raise
