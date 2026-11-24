---
title: Issue 145 live details (2026-11-24)
description: Phase details for the release-change register.
ms.date: 2026-11-24
---

## P2 recovery.py

* `RELEASE_REGISTER_CASE = "_release_changes"`.
* `record_release_change(store, db, rid, status)`: returns False when the release is absent or already revoked or (for `suspended`) not active; otherwise writes one write-once entry `{release, status, at}` (no free text) and returns True. Raises the document-store error when the write fails, so nothing changes.
* `reapply_release_changes(db, now, store, actor="system-restore")`: for each entry oldest first, compare to the row; active to suspended or revoked, suspended to revoked, via `assistant_release.change(..., system=True)`; unknown releases skipped. Returns ids changed.

## P3 assistants.py

* `change_release`: after `authorize`, call `recovery.record_release_change`; then `rel.change`.
* Attestation suspension loop: call `record_release_change` before `rel.change`.

## P4 tests

* Restored database returns the release to active; `reapply_release_changes` suspends it; revoked outranks suspended; a second run changes nothing.
* Register write failure blocks the change; invalid or unknown id writes no entry; entry has no free text.
