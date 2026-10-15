"""Backup, restore and deletion re-application for the SQL store (PRD DH-005).

Erasure redacts a resident's personal fields in the case and appends the case id to a deletion register
kept outside the database. A restore returns the database to an older state, so the register is the only
thing that remembers what must stay deleted: reapply_deletions() runs after every restore, before the
store serves traffic. The register holds no personal data.

Local drill uses the SQLite backup API. On Azure SQL the same order applies to a point-in-time restore;
that drill is an open item until it is run against the dev database (see the PRD DH-005 evidence note).
"""
import json
import os
import sqlite3
from datetime import datetime

REDACTED = "[erased]"
PERSONAL = ("title", "name", "formal", "phone", "email", "adjustment", "unavailable")


def register_path(store):
    return os.path.join(os.path.dirname(store.digest_dir) or ".", "erasures.jsonl")


def read_register(store):
    path = register_path(store)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def _redact(c):
    r = c["resident"]
    changed = any(r.get(k) not in (REDACTED, "") for k in PERSONAL) or r.get("representative") is not None
    for k in PERSONAL:
        if k in r:
            r[k] = REDACTED
    r["representative"] = None
    for contact in c.get("contacts", []):
        if contact.get("note") != REDACTED:
            changed = True
        contact["note"] = REDACTED
    return changed


def erase_resident(store, user, case_id, reason):
    """Redact the resident, record it in the register and the audit ledger. Returns the register entry."""
    reason = (reason or "").strip()[:200]
    if not reason:
        raise ValueError("Record why the data is being erased.")
    with store.lock:
        c = store._case(case_id)
        _redact(c)
        store.audit(user["email"], "erase_resident", case_id, reason)
        store.save()
    entry = dict(case=case_id, reason=reason, at=datetime.now().isoformat(timespec="seconds"))
    with open(register_path(store), "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry


def reapply_deletions(store, actor="system-restore"):
    """Redact again every register entry the restored database still holds in the clear. Returns the case ids changed."""
    done = []
    for entry in read_register(store):
        with store.lock:
            try:
                c = store._case(entry["case"])
            except KeyError:
                continue
            if _redact(c):
                store.audit(actor, "erasure_reapplied", entry["case"], entry["reason"])
                store.save()
                done.append(entry["case"])
    return done


def backup(store, dest):
    """Consistent copy of the SQLite database (online backup API)."""
    with store.dblock:
        out = sqlite3.connect(dest)
        try:
            store.db.backup(out)
        finally:
            out.close()
    return dest
