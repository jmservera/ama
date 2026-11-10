---
title: Issue 1360 extension E1 changes
ms.date: 2026-11-10
task_id: 1360-extension1-1110
---

## Status

Implement executed 2026-11-10 (UTC) after plan-done (witness seq 3) and implement-start (seq 4). Changes record was persisted as a stub before implement-start and completed here in place. No plan amendment or divergence.

## Changes

| File | Change |
| --- | --- |
| `src/core/src/zava_forward/core/sqlstore.py` | `save`: the post-commit `_sync` translation now catches `(RuntimeError, OSError, ValueError)` and raises `CommittedReloadError` (chained, `_seq = -1`). One line. |
| `src/importer/tests/test_import_exceptions.py` | In `TransferFailureTests`: `stored` read-only probe; a real pre-commit control (`_append_audit` raising `OSError`, nothing stored, retry adds once); two real committed-then-reload tests (`OSError`, `ValueError`) using a real second `SqlStore` write, the real CLI, a probe at the reload proving the commit, exit and stderr, independent reopen, idempotent retry and ledger and source hashes. |
| `src/core/tests/test_priority_order.py` | `test_post_commit_reload_oserror_or_valueerror_is_a_committed_outcome`: `CommittedReloadError`, `committed`, `__cause__`, single row, repeat save writes nothing twice. |

No CLI, importer, docs, workflow, dependency or configuration change. Transfer semantics, permissions, consent and actions are unchanged.

## Red then green

Before the source change the two new committed-then-reload tests failed with the original defect message "the served store refused it (reload failed). Nothing was recorded." although the probe proved the commit (exit 2). The pre-commit control passed before and after. After the change they pass.

## Raw validation (own venv `/tmp/zf-1360-e1`, origins asserted under the worktree)

| Check | Result |
| --- | --- |
| Baseline `src/importer` discover (merged head) | 79 tests OK |
| `src/importer` discover after | 82 tests OK |
| Baseline `src/core` `test_import_refusals` and `test_priority_order` | 163 OK, 72 skipped |
| Same after | 165 OK, 73 skipped (opt-in MSSQL copy of the new test is skipped, unobserved) |
| `src/api` `test_case_journey` (existing CommittedReloadError consumer) | 31 OK |
| ruff check, ruff format check and mypy for `src/importer` | all pass |
| mypy for `src/core` | pass (296 files) |
| ruff format check for `src/core` `sqlstore.py` | reports an import-block reformat at line 21 that is identical on the unmodified file (pre-existing, not touched) |

Logs under the external evidence directory `phase1360-extension1-evidence-1110/logs`. Not run: full SQL, Docker, cloud, hosted CI, browser (no web surface changed).
