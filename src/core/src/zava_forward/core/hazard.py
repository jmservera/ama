"""Current actors and durable evidence for retrofit-only hazard holds."""

import logging
from collections.abc import Iterator
from contextlib import contextmanager
from copy import deepcopy
from typing import Any

from .change_provenance import _actor

Record = dict[str, Any]


def identity(actor: Record) -> Record:
    return {key: actor.get(key) for key in ("code", "email", "name", "role", "oid")}


def _context(store: Any) -> Record:
    result: Record = getattr(store, "local", store).hazard_decision
    return result


def subject(store: Any, candidate: Record) -> Record:
    actor = _actor(store, candidate)
    _context(store)["subjects"].append(deepcopy(actor))
    return actor


def validate_sql(store: Any) -> None:
    context = getattr(store.local, "hazard_decision", None)
    if context is not None:
        for expected in context["subjects"]:
            if _actor(store, expected) != expected:
                raise PermissionError(
                    "Safety referral authority changed. Reload before continuing."
                )


def mark_committed(store: Any) -> None:
    context = getattr(store.local, "hazard_decision", None)
    if context is not None:
        context["persisted"] = True


@contextmanager
def decision_scope(store: Any, user: Record, case_id: str) -> Iterator[tuple[Record, Record]]:
    with store.lock:
        holder = getattr(store, "local", store)
        previous = getattr(holder, "hazard_decision", None)
        sql = hasattr(store, "db")
        if sql:
            store._touched()
        pending = deepcopy(store.local.pending) if sql else []
        before = None
        context: Record = dict(subjects=[], persisted=False)
        holder.hazard_decision = context
        try:
            actor = subject(store, user)
            case = store._case(case_id)
            before = deepcopy(case)
            yield case, actor
        except BaseException as error:
            if sql:
                if context["persisted"]:
                    error.add_note(
                        "Safety evidence transaction committed, but synchronization failed. "
                        "Reload and reconcile before retrying."
                    )
                    logging.getLogger(__name__).exception(
                        "Committed safety evidence synchronization failed"
                    )
                try:
                    with store.dblock:
                        store._discard(() if context["persisted"] else pending)
                except Exception:
                    error.add_note(
                        "Safety evidence recovery failed; reload to establish the outcome."
                    )
                    logging.getLogger(__name__).exception("Safety evidence SQL recovery failed")
            elif context["persisted"]:
                error.add_note(
                    "Safety evidence was saved, but its audit may be incomplete. "
                    "Reload and reconcile before retrying."
                )
                logging.getLogger(__name__).exception("Saved safety evidence audit is incomplete")
            elif before is not None:
                case.clear()
                case.update(before)
            raise
        finally:
            holder.hazard_decision = previous


def persist_event(
    store: Any, actor: Record, case_id: str, action: str, detail: str, emergency: bool
) -> None:
    sql = hasattr(store, "db")
    if not sql:
        store.save()
        _context(store)["persisted"] = True
    if emergency:
        store.audit(
            actor["email"],
            "safety_emergency",
            case_id,
            "Reported emergency: use the existing hazard service immediately; "
            "retrofit and AI gates must not delay referral",
        )
    store.audit(actor["email"], action, case_id, detail)
    if sql:
        store.save()


def require_independent(actor: Record, report: Record) -> None:
    for prefix, action in (("raised", "safety_raised"), ("repaired", "safety_repaired")):
        recorded = report.get(f"{prefix}_identity")
        if not recorded:
            recorded = next(
                (
                    event["actor"]
                    for event in report.get("history", [])
                    if event["action"] == action
                ),
                {},
            )
        historical = dict(recorded)
        historical.setdefault("email", report.get(f"{prefix}_by_email"))
        historical.setdefault("name", report.get(f"{prefix}_by"))
        for key in ("email", "code", "oid"):
            old, current = historical.get(key), actor.get(key)
            if isinstance(old, str) and old.strip() and isinstance(current, str):
                if old.strip().casefold() == current.strip().casefold():
                    raise PermissionError(
                        "Someone other than the reporter and repair recorder must "
                        "release the retrofit hold."
                    )
        if not any(historical.get(key) for key in ("email", "code", "oid")):
            old_name = historical.get("name")
            if old_name and old_name.strip().casefold() == actor["name"].strip().casefold():
                raise PermissionError("A different person must release this legacy retrofit hold.")
