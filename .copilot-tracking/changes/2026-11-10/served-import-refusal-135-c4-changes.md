---
title: Changes, served import refusal correction (#135 C4/5)
ms.date: 2026-11-10
---

Opened before the first source edit, after research, plan, details and critique existed.

## Source edits

* `src/core/src/zava_forward/core/import_refusals.py`: `PartiallyRecordedError`; `record_import_refusals` delegates to a store-owned `_persist_import_refusals`; the JSON default restores the previous document (or removes the key) when `save()` fails and writes the audit only after a durable save (audit failure after save raises `PartiallyRecordedError`). No two-file atomicity is claimed.
* `src/core/src/zava_forward/core/sqlstore.py`: `SqlStore._persist_import_refusals` snapshots pending audit, publishes, queues the audit and saves; `CommittedReloadError` is re-raised untouched; any other failure calls `_discard(pending_before)` so the phantom document, success audit and idempotency poison are removed and an earlier pending audit survives once. MssqlStore inherits it.
* `src/core/src/zava_forward/core/exception_register.py`: source text reports stored and shown counts read from one snapshot under the lock; says items are shown only to the configured data steward; roles_not_named passes shown 0.
* `src/importer/src/zava_forward/importer/__main__.py`: `transfer` keeps exit 2 for ledger read errors, target open errors, `ConflictError`, `CommittedReloadError`, `PartiallyRecordedError`, `OSError`/`ValueError` and driver errors, each with a truthful message (nothing recorded only where that is known).
* `src/api/src/zava_forward/api/web/role-screens.js` line 919: empty-state sentence no longer says failed imports are unconnected. Copy only; no layout, semantics or harness change.
* `src/importer/README.md`: transfer outcomes, stored versus shown status, MSSQL evidence statement.

## Tests added or changed

* NEW `src/core/tests/test_import_refusals.py`: JSON, SQLite and opt-in disposable MSSQL (`ZF_IMPORT135_MSSQL=1`) regressions; 8 failures and 1 error on 67ad4680 for the non-MSSQL set.
* `src/importer/tests/test_import_exceptions.py`: `TransferFailureTests` (real competing SQLite writer, committed-unconfirmed, partial, driver error, rolled back).
* `src/api/tests/test_exception_register.py`: stored versus shown per scope for SQLite and JSON.
* `src/api/tests/test_exception_register_screen.py`: empty text no longer says failed imports are not connected.

## Ordering note

The state file recorded `source_edits_started` false at open; the first source edit followed at about 04:07Z, after this record existed. The flag was not flipped at that moment and is corrected in the final state.
