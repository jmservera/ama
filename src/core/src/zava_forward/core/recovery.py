"""Backup, restore and deletion re-application for the SQL store (PRD DH-005).

Erasure redacts a resident's personal fields in the case and records the case id in a deletion register
kept outside the database. A restore returns the database to an older state, so the register is the only
thing that remembers what must stay deleted: reapply_deletions() runs after every restore, before the
store serves traffic. The register holds no personal data.

The register lives in the store's document backend (store.docstore), one write-once entry per erasure under
the reserved case id "_erasures". With ZF_DOC_STORE=azure-blob it is therefore in Azure Blob Storage, outside
the database and so not rewound by a restore; the local folder backend is the local-test backend only. The
entry is written BEFORE the redaction, so a crash between the two leaves an erasure that reapply_deletions()
completes, never an unrecorded one.

Local drill uses the SQLite backup API. On Azure SQL the same order applies to a point-in-time restore;
that drill is an open item until it is run against the dev database (see the PRD DH-005 evidence note).
"""
import json
import sqlite3
import uuid
from datetime import datetime

REDACTED = "[erased]"
PERSONAL = ("title", "name", "formal", "phone", "email", "adjustment", "unavailable")


REGISTER_CASE = "_erasures"


def read_register(store):
    """All register entries, oldest first. A backend failure raises; it is never read as an empty register."""
    entries = [json.loads(store.docstore.get(REGISTER_CASE, name)) for name in store.docstore.list_ids(REGISTER_CASE)]
    return sorted(entries, key=lambda e: (e["at"], e["case"]))


def _write_entry(store, entry):
    store.docstore.put(REGISTER_CASE, f"{entry['at'].replace(':', '')}-{uuid.uuid4().hex[:12]}", json.dumps(entry, sort_keys=True).encode(), "application/json")


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
    """Record the erasure in the durable register, then redact the case and write the audit ledger.
    Returns the register entry. If the register write fails nothing is redacted."""
    reason = (reason or "").strip()[:200]
    if not reason:
        raise ValueError("Record why the data is being erased.")
    with store.lock:
        c = store._case(case_id)
        entry = dict(case=case_id, reason=reason, at=datetime.now().isoformat(timespec="seconds"))
        _write_entry(store, entry)
        _redact(c)
        store.audit(user["email"], "erase_resident", case_id, reason)
        store.save()
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
