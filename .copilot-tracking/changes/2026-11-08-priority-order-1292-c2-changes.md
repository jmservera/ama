<!-- markdownlint-disable-file -->
# Release Changes: priority order 1292, correction cycle C2

**Related Plan**: [.copilot-tracking/plans/2026-11-08-priority-order-1292-c2-plan.md](../plans/2026-11-08-priority-order-1292-c2-plan.md)
**Base**: C1 head `6fcf8368ae1fd731ecfc4fe198d59927dcc72dbb` (tree `1237f4733a68aaa252fa2089fd3f316610459d22`)
**Research and plan commit**: `8375f5ffc` (written before any source or test edit)

## Summary

Second correction after the independent C1 review (4 High, 5 Medium; all nine verified true in source).
Prior research, plans, reviews, C1 logs and earlier SQL results are unchanged and are historical for the new source.

## Changes

* `src/core/src/zava_forward/core/sqlstore.py`
  * F1: `_sync` reads seq, fetches, reads seq again (bounded `SYNC_RETRIES=8`), repairs fetched zero ordinals under the writer lock and re-reads; never caches a zero ordinal; fails closed on exhaustion.
  * F2: `_queue_candidates` synchronises before its transaction and re-checks seq inside it; the thread-local `writing` flag was removed, so a rollback cannot publish cache state.
  * F3: audit position leads the order for verified creation events, so a backward clock step is trusted; heuristic rows are merged by `created`.
  * F4/F5: unresolved ids (`rec_order_unresolved`) are read by `rec_order_unresolved()`; a creation event is trusted only if not contradicted by the insertion seq of an unedited row; a rolled-back save drops its unsaved proposals and pending creation events (`_drop_unsaved_recommendations`).
  * F6: audit evidence is verified against the retained head and digests (digest directory configured before migration).
  * F7: `_review_c0_backfill` flags same-second groups from the earlier candidate (`c0-review` batch) without changing an ordinal.
  * F8: evidence is cached per process and extended incrementally; one `rec_order_batch:<n>` key per batch instead of rewriting one JSON list.
* `src/core/src/zava_forward/core/store.py`: `rec_order_unresolved` default and `latest_priority` marking (`order_confirmed` false, `actionable` false, `order_note`) only for an unresolved newest eligible record. Employee and `ai_task` filters unchanged.
* `src/core/tests/sqlguard.py`: F9 manifest-based admission (private manifest, host, port and password digest), refused before any connection or DDL.
* `src/core/tests/test_priority_order.py`: new red/green tests for each finding plus manifest negatives.
* `src/core/README.md`: section "Priority recommendation creation order (#1292)" updated.

## Test-expectation corrections made during the green run (disclosed)

Three of my new tests had wrong expectations, not product defects, and were corrected before the final green run (attempt 1 retained as `green-attempt1`): the clock test counted the seeded earlier proposal so inversions are asserted `>= 1`; the second-employee record needed its body user set; the failed-publication test now counts only `ai_run_end` creation events.

## Evidence (logs under `.copilot-tracking/changes/logs/1292-2026-11-08-c2/`)

Run from `src/core` with `HOME=/tmp/ama-1292-scratch ZF_DATA=/tmp/ama-1292-scratch/none.json PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests python3 -m unittest <module> -q`; ruff 0.17.3, mypy in `/tmp/ama-1292-scratch/venv`.

| Check | Result |
| --- | --- |
| `test_priority_order` on unchanged C1 source (red) | exit 1; 54 run, 11 failures, 5 errors, 19 skipped (SQL Server class) (`red-priority-order.*`) |
| `test_priority_order` attempt 1 on C2 source | exit 1; 2 failures, 1 error, all test expectations (`green-attempt1.*`) |
| `test_priority_order` final (green) | exit 0; 54 run, OK, 19 skipped (SQL Server class, `ZF_RESIDENT_MSSQL` unset) (`green-final.*`) |
| `test_sqlstore` / `test_sqlqueues` / `test_sqlreads` / `test_taskqueues` | exit 0; 18 / 14 / 15 / 21 tests OK |
| `test_resident_decisions` (includes the two original selectors on SQLite only) | exit 0; 256 run, 93 skipped (SQL Server and related) |
| `ruff check src tests` | exit 0 |
| `ruff format --check` on the two test files (format-clean at HEAD) | exit 0; `sqlstore.py` and `store.py` were not format-clean at HEAD and were not reformatted |
| `mypy --config-file pyproject.toml src tests` | exit 0, 271 files |
| `git diff --check` | exit 0 |

The 19 and 93 skips are the SQL Server classes gated by `ZF_RESIDENT_MSSQL`; they are explained and not run.

## Source sha256

* `sqlstore.py` `569ef51b326cdcb70654154ecc58b83943b5823f012f89c19c3729e8292303ee` (before final commit, no later edits)
* `store.py` `6e159c06019f4ede61803ced47919fbb6f47680825d8e7b0f3e67226d3468284`
* `tests/test_priority_order.py` and `tests/sqlguard.py` are hashed by the commit tree.

## Not done and not proven

* SQL Server execution of the C2 source, the two original selectors on SQL Server, the ledger-enabled migration and SQL Server scale: PENDING coordinator admission (a cleanup holds the shared heavy lock; none started).
* The digest-anchored evidence path runs only on SQLite. Year-digest checks run only on the full verification path.
* The C0 review is tested by simulating C0 state, not by running C0 source. A manifest-provisioned SQL fixture was not exercised against a real server.
* FULL local gate with verified external receipt, independent exact-head review and hosted CI remain mandatory and pending.
* Human decisions: how the named data owner resolves flagged records (no mechanism added, none invented) and the rolling-release boundary.
