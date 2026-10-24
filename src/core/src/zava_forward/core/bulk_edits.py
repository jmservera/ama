"""Closed administrative edit contract; decisions and ownership are never bulk edits."""

import hashlib
import json
import uuid
from copy import deepcopy
from datetime import UTC, datetime
from typing import Any

from . import identity, projection
from .store import ConflictError
from .workflows import HANDOFF_ACTIVE, MANAGER_ROLES, _due

Record = dict[str, Any]
FIELDS = {
    "case_reason": (None, "reason"),
    "handoff_due_at": ("handoff", "due_at"),
    "handoff_next_action": ("handoff", "next_action"),
}
REQUEST_KEYS = {"case_ids", "changes", "source", "source_version", "reason"}


def _canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(value: object) -> str:
    return hashlib.sha256(_canonical(value).encode()).hexdigest()


def _text(value: object, label: str, limit: int = 300) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"Enter {label}, from 1 to {limit} characters.")
    return value.strip()


def _request(body: object) -> Record:
    if not isinstance(body, dict) or set(body) != REQUEST_KEYS:
        raise ValueError("Use only case_ids, changes, source, source_version and reason.")
    ids, changes = body["case_ids"], body["changes"]
    if (
        not isinstance(ids, list)
        or not 1 <= len(ids) <= 100
        or any(not isinstance(cid, str) or not cid.strip() or len(cid) > 100 for cid in ids)
        or len(set(ids)) != len(ids)
    ):
        raise ValueError("Choose between 1 and 100 distinct case identifiers.")
    if not isinstance(changes, dict) or not changes or set(changes) - FIELDS.keys():
        raise ValueError("Only case_reason, handoff_due_at and handoff_next_action can be edited.")
    normalized = {}
    for field, value in changes.items():
        normalized[field] = (
            _due(_text(value, "a handoff due date", 80))
            if field == "handoff_due_at"
            else _text(value, field)
        )
    return dict(
        case_ids=list(ids),
        changes=normalized,
        source=_text(body["source"], "the source reference", 200),
        source_version=_text(body["source_version"], "the source version", 100),
        reason=_text(body["reason"], "the reason for this edit"),
    )


def _identity(user: Record) -> Record:
    return {key: user.get(key) for key in ("email", "code", "name", "role", "oid", "auth_provider")}


def _fresh_actor(store: Any, user: Record) -> Record:
    email = user.get("email")
    actor = None
    if identity.is_entra(user):
        actor = identity.verified(user)
    elif isinstance(email, str):
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
        or any(actor.get(key) != user.get(key) for key in ("email", "code", "name", "role", "oid"))
        or not projection.can_see_reason(user)
    ):
        raise PermissionError("Current named staff authority and case-note access are required.")
    return deepcopy(actor)


def _eligible(store: Any, user: Record, case: Record, changes: Record) -> None:
    if case["owner_code"] != user["code"] and user["role"] not in MANAGER_ROLES:
        raise PermissionError("Only the case owner or a programme manager can edit these fields.")
    if case["closed"]:
        raise ValueError("This case is closed.")
    store.guard_case_event(case)
    if any(field.startswith("handoff_") for field in changes) and (
        not case.get("handoff") or case["handoff"]["state"] not in HANDOFF_ACTIVE
    ):
        raise ValueError(
            "An active handoff is required; ownership and commitments cannot be edited."
        )


def _anchor(store: Any, preview_id: str, issued: Record) -> None:
    expected = dict(preview_id=preview_id, digest=_digest(issued))
    if not any(
        entry["action"] == "bulk_preview_issued" and json.loads(entry["detail"]) == expected
        for entry in store.audit_entries()
        if entry["action"] == "bulk_preview_issued"
    ):
        raise ConflictError("The issued preview changed. Request a fresh preview.")


def _unused(store: Any, preview_id: str) -> None:
    if any(
        entry["action"] == "bulk_edit_applied"
        and json.loads(entry["detail"]).get("preview_id") == preview_id
        for entry in store.audit_entries()
        if entry["action"] == "bulk_edit_applied"
    ):
        raise ConflictError("Preview already applied. Request a fresh preview.")


def _applicable_request(issued: Record) -> Record:
    request = _request(issued["request"])
    ids, records, snapshots = request["case_ids"], issued["records"], issued["snapshots"]
    if (
        not isinstance(records, list)
        or not all(isinstance(record, dict) for record in records)
        or [record.get("case_id") for record in records] != ids
        or not isinstance(snapshots, dict)
        or set(snapshots) != set(ids)
    ):
        raise ConflictError("Preview target coverage is incomplete. Request a fresh preview.")
    for record in records:
        changes = record.get("changes")
        if (
            record.get("failures") != []
            or record.get("outcome") not in ("would_apply", "no_change")
            or not isinstance(changes, dict)
            or set(changes) != set(request["changes"])
            or any(
                not isinstance(values, dict)
                or set(values) != {"old", "new"}
                or values["new"] != request["changes"][field]
                for field, values in changes.items()
            )
        ):
            raise ConflictError("Issued preview is not applicable. Request a fresh preview.")
        outcome = (
            "would_apply"
            if any(values["old"] != values["new"] for values in changes.values())
            else "no_change"
        )
        if record["outcome"] != outcome:
            raise ConflictError("Issued preview outcomes disagree. Request a fresh preview.")
    return request


def _changes(case: Record, proposed: Record) -> Record:
    changes = {}
    for field, value in proposed.items():
        parent, key = FIELDS[field]
        old = (case[parent] if parent else case).get(key)
        changes[field] = dict(old=deepcopy(old), new=value)
    return changes


def validate_sql(store: Any) -> None:
    """Called after BEGIN IMMEDIATE, before any writes in the existing save transaction."""
    context = getattr(store.local, "bulk_validation", None)
    if context is None:
        return
    actor = _fresh_actor(store, context["user"])
    if actor != context["staff"]:
        raise PermissionError("Staff authority changed. Request a fresh preview.")
    guard = store.db.execute("SELECT value FROM meta WHERE key='governance'").fetchone()
    if (guard[0] if guard else None) != context["guard_snapshot"]:
        raise ConflictError("Case guardrails changed. Request a fresh preview.")
    issued = context.get("issued")
    request = None
    if issued is not None:
        _anchor(store, context["preview_id"], issued)
        _unused(store, context["preview_id"])
        request = _applicable_request(issued)
    ids = request["case_ids"] if request else list(context["snapshots"])
    for index, cid in enumerate(ids):
        snapshot = context["snapshots"][cid]
        row = store.db.execute("SELECT rowversion, body FROM cases WHERE id=?", (cid,)).fetchone()
        if (
            row is None
            or row[0] != snapshot["rowversion"]
            or _digest(json.loads(row[1])) != snapshot["digest"]
        ):
            raise ConflictError("A target changed. Request a fresh preview.")
        case = json.loads(row[1])
        _eligible(store, context["user"], case, context["changes"])
        if (
            issued is not None
            and _changes(case, context["changes"]) != issued["records"][index]["changes"]
        ):
            raise ConflictError(
                "Preview changes disagree with the target. Request a fresh preview."
            )


def _save(store: Any, context: Record) -> None:
    if hasattr(store, "local"):
        context["guard_snapshot"] = store._proc_snap.get("governance")
        store.local.bulk_validation = context
    try:
        store.save()
    finally:
        if hasattr(store, "local"):
            store.local.bulk_validation = None


def _recover(store: Any, before: Record) -> None:
    if hasattr(store, "db"):
        with store.dblock:
            store._discard()
            for key in store.DOCS:
                row = store.db.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
                if row:
                    store.data[key] = json.loads(row[0])
                else:
                    store.data.pop(key, None)
        store.local.bulk_validation = None
    else:
        for cid, case in before["cases"].items():
            store.cases[cid].clear()
            store.cases[cid].update(case)
        if before["bulk_edits"] is None:
            store.data.pop("bulk_edits", None)
        else:
            store.data["bulk_edits"] = before["bulk_edits"]


def _execute(store: Any, user: Record, body: object, applying: bool) -> Record:
    with store.lock:
        before = dict(cases={}, bulk_edits=deepcopy(store.data.get("bulk_edits")))
        try:
            actor = _fresh_actor(store, user)
            return (
                _apply(store, user, actor, body, before)
                if applying
                else _preview(store, user, actor, body)
            )
        except Exception as error:
            _recover(store, before)
            refusal = dict(
                phase="apply" if applying else "preview",
                error=type(error).__name__,
                reason=str(error)
                if isinstance(error, (ValueError, PermissionError, ConflictError))
                else "Storage failure; outcome may be unknown. Reload before retrying.",
            )
            store.audit(
                str(user.get("email", "unknown")),
                "bulk_edit_rejected",
                "-",
                _canonical(refusal),
            )
            raise


def preview(store: Any, user: Record, body: object) -> Record:
    return _execute(store, user, body, False)


def apply(store: Any, user: Record, body: object) -> Record:
    return _execute(store, user, body, True)


def _preview(store: Any, user: Record, actor: Record, body: object) -> Record:
    request = _request(body)
    records, snapshots = [], {}
    for cid in request["case_ids"]:
        record: Record = dict(case_id=cid, changes={}, failures=[], outcome="blocked")
        case = store.cases.get(cid)
        try:
            if case is None:
                raise ValueError("Case unavailable for this edit.")
            _eligible(store, user, case, request["changes"])
        except (PermissionError, ValueError) as error:
            record["failures"] = [str(error)]
        else:
            snapshots[cid] = dict(
                digest=_digest(case),
                rowversion=store._rv[cid] if hasattr(store, "_rv") else None,
            )
            record["changes"] = _changes(case, request["changes"])
            record["outcome"] = (
                "would_apply"
                if any(item["old"] != item["new"] for item in record["changes"].values())
                else "no_change"
            )
        records.append(record)
    blocked = any(record["failures"] for record in records)
    if blocked:
        for record in records:
            if record["outcome"] == "would_apply":
                record["outcome"] = "batch_blocked"
    preview_id = str(uuid.uuid4())
    issued = dict(
        request=request,
        actor=_identity(user),
        at=datetime.now(UTC).isoformat(timespec="seconds"),
        records=records,
        snapshots=snapshots,
        staff=actor,
    )
    entry = dict(issued=issued, status="blocked" if blocked else "pending")
    store.data.setdefault("bulk_edits", {})[preview_id] = entry
    store.audit(
        user["email"],
        "bulk_preview_issued",
        "-",
        _canonical(dict(preview_id=preview_id, digest=_digest(issued))),
    )
    _save(
        store,
        dict(user=user, staff=actor, snapshots=snapshots, changes=request["changes"]),
    )
    return _response(preview_id, entry)


def _response(preview_id: str, entry: Record) -> Record:
    issued = entry["issued"]
    return deepcopy(
        dict(
            preview_id=preview_id,
            status=entry["status"],
            actor=issued["actor"],
            source=issued["request"]["source"],
            source_version=issued["request"]["source_version"],
            reason=issued["request"]["reason"],
            records=entry.get("result", issued["records"]),
        )
    )


def _apply(store: Any, user: Record, actor: Record, body: object, before: Record) -> Record:
    if not isinstance(body, dict) or set(body) != {"preview_id"}:
        raise ValueError("Apply accepts only preview_id from an inspected preview.")
    preview_id = _text(body["preview_id"], "the preview identifier", 100)
    entry = store.data.get("bulk_edits", {}).get(preview_id)
    if entry is None:
        raise ConflictError("Preview unavailable. Request a fresh preview.")
    issued = entry["issued"]
    _anchor(store, preview_id, issued)
    _unused(store, preview_id)
    if issued["actor"] != _identity(user):
        raise PermissionError("Only the preview's current creator can apply it.")
    if entry["status"] != "pending":
        raise ConflictError("Preview blocked or already applied. Request a fresh preview.")
    request = _applicable_request(issued)
    if actor != issued["staff"]:
        raise PermissionError("Staff authority changed. Request a fresh preview.")
    for index, cid in enumerate(request["case_ids"]):
        snapshot = issued["snapshots"][cid]
        case = store.cases.get(cid)
        if (
            case is None
            or _digest(case) != snapshot["digest"]
            or (hasattr(store, "_rv") and store._rv[cid] != snapshot["rowversion"])
        ):
            raise ConflictError("A target changed. Request a fresh preview.")
        _eligible(store, user, case, request["changes"])
        if _changes(case, request["changes"]) != issued["records"][index]["changes"]:
            raise ConflictError(
                "Preview changes disagree with the target. Request a fresh preview."
            )
    records = deepcopy(issued["records"])
    for record in records:
        if record["outcome"] == "no_change":
            continue
        cid = record["case_id"]
        case = store._case(cid)
        before["cases"][cid] = deepcopy(case)
        for field, values in record["changes"].items():
            parent, key = FIELDS[field]
            (case[parent] if parent else case)[key] = values["new"]
        history = case.setdefault("edit_history", [])
        event = dict(
            preview_id=preview_id,
            version=len(history) + 1,
            actor=_identity(user),
            at=datetime.now(UTC).isoformat(timespec="seconds"),
            source=request["source"],
            source_version=request["source_version"],
            reason=request["reason"],
            changes=deepcopy(record["changes"]),
        )
        history.append(event)
        store.audit(user["email"], "bulk_case_edited", cid, _canonical(event))
        record["outcome"] = "applied"
    entry.update(status="applied", result=records)
    store.audit(user["email"], "bulk_edit_applied", "-", _canonical(dict(preview_id=preview_id)))
    _save(
        store,
        dict(
            user=user,
            staff=actor,
            snapshots=issued["snapshots"],
            changes=request["changes"],
            preview_id=preview_id,
            issued=issued,
        ),
    )
    return _response(preview_id, entry)
