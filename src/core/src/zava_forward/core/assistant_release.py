"""Release admission for AI tasks (issue #107, RAI delta). SQL owns the record; no process caches it.

A release binds one task/purpose to the provider, endpoint, deployment, expected serving model and the
prompt, policy, data, provenance and permission versions. Absent, expired, suspended, revoked or
mismatched releases deny dispatch. A revoked or suspended release is terminal: a new record is needed.
This module records what a named human decides; it never approves, and it grants no domain write.
"""
import json
import uuid
import logging
import sqlite3
from datetime import datetime, timezone
from . import rai_release

OWNER = "RAI task owner not appointed (OQ-017; project contact: Juan Manuel Servera)"
CLASSES = ("constructed-fixture", "actual")
BOUND = ("registry_version", "schema_version", "provider", "endpoint", "deployment", "prompt_version",
         "policy_version", "data_version", "provenance_version", "permission_version",
         "model_version", "task_contract_version", "evaluation_version")
STATUSES = ("active", "suspended", "revoked")
SQLITE_DDL = (
    "CREATE TABLE IF NOT EXISTS assistant_releases (id TEXT PRIMARY KEY, capability TEXT NOT NULL, status TEXT NOT NULL, body TEXT NOT NULL, revision INTEGER NOT NULL)",
)
MSSQL_DDL = (
    "CREATE TABLE assistant_releases (id VARCHAR(64) PRIMARY KEY, capability VARCHAR(128) NOT NULL, status VARCHAR(16) NOT NULL, body NVARCHAR(MAX) NOT NULL, revision BIGINT NOT NULL)",
)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def text(value, label, limit=240):
    if not isinstance(value, str) or not 1 <= len(value.strip()) <= limit:
        raise ValueError(f"Record {label} (1 to {limit} characters).")
    return value.strip()


def parse_expiry(value):
    try:
        when = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        raise ValueError("Record an ISO 8601 expiry.") from None
    return (when if when.tzinfo else when.replace(tzinfo=timezone.utc)).timestamp()


def denial(reason, missing, task):
    return dict(reason=f"Release admission denied: {reason}. Owner: {OWNER}. Manual route: use the ordinary case controls.",
                missing=missing, owner=OWNER, manual="Use the ordinary case controls.", task=task,
                authority_gap=rai_release.AUTHORITY_GAP, authority_holders=rai_release.authority_register())


def release_body(raw):
    """Decode a retained release object without coercing invalid JSON shapes."""
    try:
        body = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError("Release body contains malformed JSON.") from None
    if not isinstance(body, dict):
        raise ValueError("Release body must be a JSON object.")
    return body


def releases(db, task):
    rows = db.execute("SELECT id,status,body FROM assistant_releases WHERE capability=? ORDER BY id", (task,)).fetchall()
    return [dict(release_body(b), id=i, status=s) for i, s, b in rows]


def invalidate_changed(db, now, spec, binding, found, live):
    """Revoke active records whose bound versions or intended use changed; return the records still held."""
    kept = []
    for rec in found:
        triggers = rai_release.changed_triggers(rec, spec, binding) if rec["status"] == "active" else []
        if triggers:
            fields = rai_release.missing_contract(rec, spec) + rai_release.missing_binding(rec, binding, BOUND, now, live)
            cause = dict(at=now, triggers=triggers, fields=fields or triggers)
            change(db, now, None, rec["id"], "revoked", "Material change invalidated release: " + ", ".join(triggers),
                   system=True, invalidated=cause)
            rec.update(status="revoked", invalidated=cause)
        else:
            kept.append(rec)
    return kept


def invalidation_cause(found):
    """Mismatched fields of the newest record when it was revoked by a material change."""
    latest = max(found, key=lambda r: r.get("recorded_at") or 0, default=None)
    cause = latest.get("invalidated") if latest and latest.get("status") == "revoked" else None
    fields = cause.get("fields") if isinstance(cause, dict) else None
    return [f for f in fields if isinstance(f, str)] if isinstance(fields, list) else []


def assessment(db, task, binding, now, live=False):
    """Return the selected record and no denial, or no record and an explicit denial."""
    from . import ai_registry
    spec = ai_registry.get(task.removeprefix("legacy:"))
    if spec is None:
        return None, denial("task is not registered", ["registered task"], task)
    store_error = db.driver.Error if hasattr(db, "driver") else sqlite3.Error
    try:
        found = releases(db, task)
    except store_error:
        logging.getLogger(__name__).warning("Release record store unavailable; dispatch denied.")
        return None, denial("release records are unavailable", ["release record store"], task)
    except (ValueError, TypeError):
        logging.getLogger(__name__).warning("Malformed release record; dispatch denied.")
        return None, denial("malformed release record", ["valid release record"], task)
    held = found
    if not task.startswith("legacy:"):
        try:
            found = invalidate_changed(db, now, spec, binding, found, live)
        except (store_error, ValueError):
            logging.getLogger(__name__).warning("Release invalidation not recorded; dispatch denied.")
            return None, denial("release invalidation could not be recorded", ["release record store"], task)
    selected, missing = rai_release.select(found, spec, binding, BOUND, now, live)
    if not selected and not any(r["status"] == "active" for r in found):
        missing = invalidation_cause(held) or missing
    return (selected, None) if selected else (
        None, denial("no approved release matches (" + ", ".join(missing) + ")", missing, task))


def admission(db, task, binding, now, live=False):
    return assessment(db, task, binding, now, live)[1]


def record(db, now, user, body, approvers, task_ids):
    if user.get("role") != "Retrofit Programme Manager":
        raise PermissionError("Only a Retrofit Programme Manager can record a release.")
    if user.get("email", "").lower() not in approvers:
        raise PermissionError("You are not a named release approver; use the manual route.")
    task = body.get("task")
    if task not in task_ids:
        raise ValueError("Choose a registered task.")
    cls = body.get("evidence_class")
    if cls not in CLASSES:
        raise ValueError("State evidence_class: constructed-fixture or actual.")
    if body.get("residual_risk_decision") != "Accept":
        raise ValueError("A release needs an explicit residual risk decision of Accept; otherwise the task stays denied.")
    evidence = body.get("evidence")
    if not isinstance(evidence, list) or not 1 <= len(evidence) <= 20:
        raise ValueError("List 1 to 20 evidence references.")
    rec = dict(task=task, evidence_class=cls, evidence=[text(e, "an evidence reference") for e in evidence],
               residual_risk_decision="Accept", residual_risk_note=text(body.get("residual_risk_note"), "the residual risk note", 400),
               serving_model=text(body.get("serving_model"), "the actual serving model version", 120),
               approver=dict(name=user.get("name", ""), email=user["email"], role=user["role"]),
               expires=parse_expiry(body.get("expires")), recorded_at=now,
               actual_authorisation=cls == "actual")
    for k in BOUND:
        rec[k] = text(body.get(k), k, 200)
    from . import ai_registry
    spec = ai_registry.get(task.removeprefix("legacy:"))
    for k in ("release_version", "intended_use", "prohibited_uses", "affected_stakeholders",
              "accountable_owner", "impact_assessment", "material_change_triggers", "evaluation_decision"):
        rec[k] = body.get(k)
    missing = rai_release.missing_contract(rec, spec)
    if missing:
        raise ValueError("Release record missing or mismatched: " + ", ".join(missing))
    if rec["expires"] <= now:
        raise ValueError("Expiry must be in the future.")
    rid = uuid.uuid4().hex
    for prior in releases(db, task):
        if prior["status"] == "active":
            change(db, now, user, prior["id"], "revoked", f"Superseded by release {rid}.")
    db.execute("INSERT INTO assistant_releases (id,capability,status,body,revision) VALUES (?,?,'active',?,1)",
               (rid, task, canonical(rec)))
    event(db, now, rid, kind="release-recorded", task=task, approver=user["email"], evidence_class=cls)
    return rid


def change(db, now, user, rid, status, reason, system=False, invalidated=None):
    if not system and user.get("role") != "Retrofit Programme Manager":
        raise PermissionError("Only a Retrofit Programme Manager can change a release.")
    if status not in ("suspended", "revoked"):
        raise ValueError("Choose suspended or revoked.")
    reason = text(reason, "a reason", 400)
    mssql = hasattr(db, "driver")
    db.execute("SAVE TRANSACTION release_change" if mssql else "SAVEPOINT release_change")
    try:
        res = db.execute("UPDATE assistant_releases SET status=?,revision=revision+1 WHERE id=? AND status IN ('active','suspended')",
                         (status, rid))
        if res.rowcount != 1:
            raise ValueError("Release is unknown or already revoked.")
        if invalidated:
            raw = db.execute("SELECT body FROM assistant_releases WHERE id=?", (rid,)).fetchone()[0]
            body = release_body(raw)
            if body:
                db.execute("UPDATE assistant_releases SET body=? WHERE id=?",
                           (canonical(dict(body, invalidated=invalidated)), rid))
        event(db, now, rid, kind=f"release-{status}", by=user["email"] if user else "system", reason=reason)
    except BaseException:
        db.execute("ROLLBACK TRANSACTION release_change" if mssql else "ROLLBACK TO release_change")
        raise
    finally:
        if not mssql:
            db.execute("RELEASE release_change")


def event(db, now, rid, **body):
    db.execute("INSERT INTO assistant_events (id, task_id, at, body) VALUES (?,?,?,?)",
               (uuid.uuid4().hex, rid, now, canonical(body)))
