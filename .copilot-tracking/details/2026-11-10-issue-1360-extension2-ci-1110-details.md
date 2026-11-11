---
title: Issue 1360 extension 2 CI regression details
ms.date: 2026-11-10
task_id: 1360-extension2-ci-1110
---

## Source

`src/core/src/zava_forward/core/sqlstore.py`: in `save`, choose the post-commit error tuple as `(RuntimeError, OSError, ValueError)` only while `self.local.translate_committed_sync` is set, else `RuntimeError`. `_persist_import_refusals` sets the marker before `self.save()` and clears it in `finally`. The `except CommittedReloadError: raise` and rollback branches stay as they are.

## Tests

* `src/core/tests/test_priority_order.py`: replace the direct-`save` OSError/ValueError test with one through `_persist_import_refusals` (committed, one row, retry idempotent) and a control that a plain `save()` still raises the original OSError/ValueError unchanged.
* Importer tests unchanged (they must still pass).

## Validation (own venv `/tmp/zf-1360-e1`, origins asserted under the worktree)

* Red: the four reported Core selectors before the fix.
* Core: complete `discover` from `src/core` with `PYTHONPATH=tests`; Importer: discover from `src/importer`; API: affected modules from `src/api` with `PYTHONPATH=../core/tests:../agents/tests`.
* ruff check/format of changed files and mypy for core and importer.
* MSSQL: selectors `test_mssqlstore.MssqlHazardReferral...` and `MssqlProcurement...` only with an existing owned local fixture and a free non-queued heavy lock; otherwise blocked and reported.
