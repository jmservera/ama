---
title: Research, served import refusal correction (#135 C4/5)
ms.date: 2026-11-10
---

Opened 2026-11-10T04:04:22Z at frozen head 67ad4680, clean tree, before any investigation or source edit.

## Order record

* Order observed in this session: state and research opened, then evidence read, then this research completed, then plan, details and critique, then the changes record, then the first source edit. The coordinator's external kernel observation is the authority on that order; this file does not prove it.
* C3 adverse preserved unchanged: C3 wrote implementation before research and plan. C4 does not cure it and it remains a publication blocker.
* Research disposition: executed (evidence root reading plus source tracing). Planning readiness: Ready.

## Evidence read

* `independent-135-served-c3-1110/functional-findings.json`, `repro_functional.py`, `repro-instructions.txt` under the evidence root.
* C3 handoff and C3 artifacts; sources `import_refusals.py`, `sqlstore.py` (`_SyncLock`, `save`, `_finish`, `_discard`, `_proc_write`, `_proc_sync`, `audit`), `store.py` (`save`, `audit`), `exception_register.py`, importer `__main__._transfer`, `role-screens.js` line 919.
* Baseline: the external probe script run against frozen 67ad4680 (venv `/tmp/issue135-c3-1110-venv`, output `/tmp/issue135-c4-red-before.out`) gave exit 1, 4 tests, 10 failing subtests: JSON memory, audit and retry; SQLite memory, audit and retry; CLI conflict; operator-only, separate operator and unnamed manager source text. This reproduces the coordinator's 10 subtest failures.

## Root causes (traced and confirmed by the baseline run)

1. `record_import_refusals` publishes the document and appends the success audit before `save()`.
   * JSON `Store.audit` appends to the audit file durably, `Store.save` writes later. A save failure leaves the audit event and the in-memory document; the same-instance retry sees the ref as present and reports `added=0`.
   * `SqlStore.audit` inside the lock only queues in `local.pending`. `save()` rolls back on a generic driver error but does not call `_discard`, so the document stays in memory and `_finish` at lock exit commits the queued success audit. `_discard(pending)` already exists, restores `_proc_snap` documents and re-syncs, and is used only on ConflictError, GateError and PermissionError.
   * `CommittedReloadError` means committed but refresh failed. It must not be treated as a failure to record.
2. CLI `_transfer` opens the ledger and the store in one `try`. It catches `sqlite3.Error`, `OSError`, `ValueError` and `SystemExit` only. `ConflictError` (documented from `_proc_write`), `CommittedReloadError` and `mssql_python.Error` (via `store.dberror`) escape as a traceback. A `sqlite3.Error` raised by the target store would also be reported as a ledger read failure.
3. `_exception_sources` chooses the connected text from document existence. The text claims items are shown, which is false for operator-only, separate operator and unnamed manager. It also re-reads `self.data` after routing, outside the snapshot used for the queue.
4. `role-screens.js:919` has a static empty text claiming failed imports are not connected. Backend sources text may say connected, so the screen contradicts itself.

## Design constraints found

* `MssqlStore` inherits `SqlStore`, `DOCS`, `save`, `_discard`. A fix in `SqlStore` covers MSSQL. Actual MSSQL evidence needs the disposable owned container path: image `mcr.microsoft.com/mssql/server:2022-latest` is present locally, no container is running, `/tmp/ama-rpi-heavy.lock` had no holder, the `sqlguard.write_manifest` pattern and the `ZF_*_MSSQL` opt-in tests are the existing mechanism. The 16 existing skips are not that evidence.
* JSON store persists two files (live and audit) that cannot be made atomic. Fix: save first, then audit; a failed audit after a durable save becomes an explicit partial outcome, never "nothing recorded". No two-file atomicity is claimed.
* A JSON-store process keeps no reload; the README stop-before-transfer caveat stays.
* Web: only one copy string in `role-screens.js` is coupled. Web skills and a fresh `web-design-guidelines` fetch are required before that edit.

## Out of scope (unchanged)

Rejected batches, other failure classes, replay or recovery, roles, default owner, procurement, quality, aftercare, 132 and 133 semantics, Bicep and cloud.

## Open limits that remain regardless

* C3 order adverse. Browser sign-in proof and MSSQL proof are required in C4 and are blockers if not completed.
