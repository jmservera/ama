---
title: Issue 1360 extension E1 phase details
ms.date: 2026-11-10
task_id: 1360-extension1-1110
---

## Owned hunks

| File | Hunk | Why |
| --- | --- | --- |
| `src/core/src/zava_forward/core/sqlstore.py` | `save`, the `except RuntimeError as error:` around the post-commit `self._sync()` becomes `except (RuntimeError, OSError, ValueError) as error:` | the only place that knows `COMMIT` already returned |
| `src/importer/tests/test_import_exceptions.py` | new test in `TransferFailureTests` using real `SQLite`, real `SqlStore`, the real CLI | proves durable commit plus post-commit failure, pre-commit control, retry |
| `src/core/tests/test_priority_order.py` | a sibling of `test_post_commit_reload_exhaustion_is_a_committed_outcome` for `OSError` and `ValueError` (subTest) | core contract for every caller |

No other source, doc, workflow or config path is owned. Shared integration dependency: `sqlstore.py` (changed on main; ordinary merge already done).

## Test design

* Importer test, post-commit: a second real `SqlStore` on the same database commits an unrelated write (seq moves), so the transfer save sees `cur != self._seq` and calls `_sync`. A wrapper on `SqlStore._sync` raises the injected error only when called from `save` after a read-only connection has shown the refusal document and audit entry committed. Run the real CLI, assert exit 2, empty stdout, stderr contains "saved" and "may be recorded" and not "Nothing was recorded", no traceback. Reopen independently: document present once, one audit entry. Run the CLI again with no injection: exit 0, `added=0`, audit count still one. Ledger db and source files hash unchanged. Parametrise over `OSError` and `ValueError`.
* Importer control, pre-commit: existing `test_refused_before_commit_says_nothing_was_recorded` keeps patching `record_import_refusals`; add a real `SqlStore` case where the error is raised from the validation before `COMMIT` and assert nothing is stored and the message still says "Nothing was recorded".
* Distinct branches kept: the existing conflict, `CommittedReloadError`, partial and driver tests must stay unchanged and green.
* Core test: inject into `_sync` after commit, assert `CommittedReloadError`, `committed` true, `__cause__` is the original error, a retry of the same save writes nothing twice.

## Risk and rollback

Risk: callers that caught a raw `OSError` from the post-commit reload now see `CommittedReloadError` (a `RuntimeError`). Search shows only committed-outcome handlers consume it. Rollback is reverting the one tuple.
