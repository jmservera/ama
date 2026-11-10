---
title: Issue 1292 current-main priority SQL regression validation details
ms.date: 2026-11-09
task_id: 1292-current-main-sql-1109
---

## Exact selectors (run from `src/core`, with `-m unittest -v`)

Environment for the unittest processes only: `ZF_RESIDENT_MSSQL=1`, `ZF_SQL_SERVER=127.0.0.1`, `ZF_SQL_PORT=<published port>`, `ZF_SQL_DATABASE=master`, `ZF_SQL_AUTH=password`, `ZF_SQL_USER=sa`, `ZF_SQL_PASSWORD=<generated, not logged>`, `ZF_SQL_TRUST_CERT=1`, `ZF_SQL_TASK_MANIFEST=<own manifest>`, `HOME` and `ZF_DATA` redirected into the own owned output directory. `PYTHONPATH` is this worktree's `src/core/src:src/core/tests:src/agents/src:src/agents/tests`. Interpreter: this worktree's `.venv/bin/python`.

Process A (108 expected):

* `test_priority_order.JsonPriorityOrder test_priority_order.LegacyMetadata test_priority_order.LoopbackGuard test_priority_order.MssqlBeginRecovery test_priority_order.SqlitePriorityOrder test_priority_order.SqliteLegacyEdges test_priority_order.SqliteC3Corrections test_priority_order.SqliteC4Corrections test_priority_order.MssqlPriorityOrder test_priority_order.MssqlLegacyMetadata test_priority_order.MssqlLegacyEdges test_priority_order.MssqlLockTimeoutBegin`

Process B (34 expected):

* `test_priority_order.MssqlC3Corrections test_priority_order.MssqlC4Corrections`

Process C (6 expected):

* `test_resident_decisions.MssqlResidentControls.test_challenge_source_exact_dependency_manifest_and_original_reviews`
* `test_resident_decisions.MssqlResidentControls.test_failed_priority_accept_edit_remove_disposition_and_audit`
* the same two method names on `test_resident_decisions.SqlResidentDecisions` and `test_resident_decisions.JsonResidentDecisions`.

A + B equals the 142-test module exactly (counts verified by loading: 108 + 34 = 142; no overlap). Skips are verified from the unittest summary line (`skipped=`), not inferred.

## Admission, timing and evidence

* Admission: `timeout -k 10 1190 flock -n /tmp/ama-rpi-heavy.lock sql-1292-current-main-v2.sh <outdir>` once; exit code recorded; busy lock exits non-zero immediately and is reported as unadmitted.
* Per-process bound 600 s including kill grace (`run-redacted.py`: TERM at 570 s, KILL by 595 s); exit 124 is recorded as a timeout failure with its partial stdout and stderr, never retried. Prior full-module durations were 536.7 s and 558.0 s; a split lowers the expected per-process duration to about half.
* Outputs in the new external directory: meta, pre-admission (holder, memory, disk), versions (image id and digest, SQL Server `@@VERSION`, `mssql-python` and ODBC package versions, Python), source identity (commit, tree, blob ids), per-process imports (module path and sha256), stdout, stderr, exit, start and end epochs, leftover-database list, container cleanup, sanitized SHA256SUMS manifest.
* Import check: the `zava_forward.core.sqlstore` and `mssqlstore` files must resolve under this worktree's `src/core/src`; any other path stops the run before tests.

## Retention and cleanup

* Raw outputs are retained in the external directory and are not committed; the changes record holds counts, exits, durations and hashes.
* Remove only: the exact container by recorded name, the own manifest file, the own `home` directory, and the explicit own `.venv` path after resolving it. No `docker system prune`, no wildcard removal.

## Review input

Review is authored (not independent); the coordinator owns independent exact-head review, the literal AC mapping and any ticking.
