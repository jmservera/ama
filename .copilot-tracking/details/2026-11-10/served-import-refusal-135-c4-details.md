---
title: Details, served import refusal correction (#135 C4/5)
ms.date: 2026-11-10
---

## Phase 1: store-owned persistence

* `import_refusals.py`: add `PartiallyRecordedError(RuntimeError)`. `record_import_refusals` keeps validation and the cap, then calls `self._persist_import_refusals({"refusals": kept}, f"added={added}")` instead of publishing and auditing inline.
* Generic (JSON `Store`) `_persist_import_refusals`: remember the previous document, publish, call `save()`; on any exception restore the previous document (pop when absent) and re-raise; only after a durable save write the audit. If the audit write fails raise `PartiallyRecordedError` (document is durable, success audit is not). No claim of two-file atomicity.
* `SqlStore._persist_import_refusals` override: snapshot `local.pending`, publish, queue the audit with `self.audit`, call `save()`. `CommittedReloadError` propagates untouched (committed). Any other exception: `_discard(pending_before)` to restore snapshot documents, drop the queued success audit and resync; attach a note if recovery fails; re-raise. Covers MSSQL by inheritance.

## Phase 2: CLI contract

* Read the ledger in its own `try` (sqlite3.Error is a ledger read failure only there).
* Open the target in its own `try` for `OSError`, `ValueError`, `SystemExit`, and the driver error class chosen from `ZF_STORE` (sqlite3.Error, or `mssql_python.Error` when mssql).
* Call `transfer` with explicit handlers, all exit 2, empty stdout:
  * `ConflictError`: another writer changed the document first; this run rolled back and recorded nothing; run again.
  * `CommittedReloadError`: saved but refresh did not settle; do not assume nothing recorded; rerun is safe because transfer is idempotent.
  * `PartiallyRecordedError`: refusals saved, success audit not written.
  * target driver error: not confirmed either way; rerun is safe.
  * `ValueError`/`OSError`: refused before commit, nothing recorded.

## Phase 3: register status from one snapshot

* Read the projection once per call (stored list or None or damaged). Build sources after items are known. Visible count is the number of `failed_import` items in the returned queue. Message states stored count, shown count and that display needs the configured data steward; unchanged NOT_CONNECTED when no valid projection.

## Phase 4: web

* Before the edit: read installed web skills (`web-design-guidelines`, `redesign-existing-projects`) and fetch the current guideline source. After: review the changed file against it with `file:line` findings.
* Replace the static empty-state sentence with one that is true whether or not failed imports are connected and points to the Sources list.

## Phase 5: tests (must fail on 67ad4680)

* New `src/core/tests/test_import_refusals.py`: JSON save failure (memory, audit, retry, disk), JSON audit failure (partial error), SQLite trigger (rollback, no success audit, retry persists once, reopen), pending audit preserved, 500/501 cap, duplicate ref, opt-in `ZF_IMPORT135_MSSQL` class (persist, reload, idempotent, rollback via trigger, concurrent conflict) using `sqlguard`.
* `src/importer/tests/test_import_exceptions.py`: CLI ConflictError, committed uncertain, partial, driver error, real SQLite two-store conflict, source/ledger unchanged.
* `src/api/tests/test_exception_register.py`: sources text for steward, separate operator, operator-only, unnamed manager, all from one snapshot.
* `src/api/tests/test_exception_register_screen.py`: empty-state copy covers the connected case; no stale "not connected" claim.

## Phase 6: validation

Commands in the handoff. MSSQL: unique disposable container with label `zf.task=1292-sql-disposable`, loopback port, random password, manifest through `sqlguard`, serial under `flock -n /tmp/ama-rpi-heavy.lock`, removed at the end; image kept.
