---
title: Issue 1292 before-fix and closure-mapping plan
ms.date: 2026-11-11
task_id: 1292-before-fix-closure-1111
---

## Objective

One finite paired SQL campaign plus a literal AC matrix. Owner-selected demo-targeted tier: the selected existing methods only, not `--all`, not the full gate, no benchmark or load. No retry, no observer, no source/test/fixture/config edit, no Source E5.

## Phases

* P0 Preconditions without SQL. Verify tracked source/tests equal the pinned base commit (git diff --quiet HEAD on tracked paths; untracked allowlist: only the dated 2026-11-11 priority-before-fix research/plans/details/critique/state records), the four source blobs and test-file blob, image id present locally, no `DOCKER_HOST`, context `default`, no holder of `/tmp/ama-rpi-heavy.lock`, no leftover owned containers, memory and disk. Create an owned mktemp directory outside the repo. Build `git archive` snapshots of `src/core` at the old commit and at this head; create two venvs; `pip install "<snapshot>/src/core[sql]"` non-editable in each (only declared dependency `mssql-python==1.15.0`; no global install). Verify, per arm, that `zava_forward.core.{store,sqlstore,mssqlstore}` import from that venv's site-packages (never the worktree) and that installed file hashes equal the Git blobs of the arm. Record Python, pip, mssql-python and ODBC versions.
* P1 Admission. One non-queued `flock -n /tmp/ama-rpi-heavy.lock`; busy or missing prerequisite means report UNADMITTED with the real reason, no wait, no cloud fallback, no fake pass.
* P2 Disposable server. One labelled container from the image id (not the tag), `127.0.0.1` published port, random password never logged, `ACCEPT_EULA`, bounded readiness (at most 40 probes, not a test retry), existing `sqlguard.write_manifest`. Record the actual container `.Image` id, `docker context inspect` endpoint and SQL Server version.
* P3 Two sequential processes, each wrapped by the existing streaming-redaction runner, 600 s per-process budget (campaign inside an outer `timeout -k 10 1190` (per-process budgets 500 s each, readiness and cleanup inside the outer bound, so the sum stays under 1190 s), sanitized `env -i` environment (no PYTHONPATH, no inherited ZF_*/application settings) with sys.path and module file paths printed inside each test process), no retry after any failure; the second runs even if the first fails.
  * O (original source, venv-old): `python -m unittest -v` over the 5 `MssqlPriorityOrder` methods listed in research, cwd `src/core/tests`, `ZF_RESIDENT_MSSQL=1`. Retain actual assertion failures and exit; classify each failure by its message.
  * N (current source, venv-cur): the same 5 SQL methods plus the 5 SQLite and 4 JSON methods. Expected 14 tests, 0 skips, 5 on SQL Server, exit 0.
* P4 Cleanup. Only the exact container id captured (label and name verified before removal); leftover query for task prefixes `zf_priority1292_%` with its exit status retained; `docker ps -a` after removal retained as a receipt; only the resolved owned directory removed after hashing.
* P5 External verifier (session-only, derived from `verify-1292-cm.py`) that FAILS on: any missing receipt, container-id and cleanup-id mismatch, nonzero leftover-query status or non-empty leftover list, owned container still present, import-path or hash mismatch, skip lines, N not exactly 14/5 SQL/exit 0. O must show exactly the five selected SQL selector ids executed with consistent counts and exit; REPRODUCED-ORDERING is classified only from an identified wrong-recommendation assertion per method (the incremental method may fail at its initial cold-load assertion; report the actual assertion, not an inferred incremental failure); any setup, cleanup, import, DDL or bootstrap error is reported separately and mixed results are labelled MIXED. The four-failure prediction is plausible, not guaranteed. It reports O's outcome as an observation: REPRODUCED-ORDERING (assertion failures showing the wrong recommendation), NON-REPRODUCTION (all passed), or OTHER (error type stated). O is not gated as pass/fail because a failure is the expected evidence.
* P6 Records: changes, authored Review, state, compact dated subsection appended to the existing cut-over pack with index and log entries, literal AC-to-evidence matrix, handoff. Raw sanitized outputs and SHA-256 sums stay external in a new directory under the coordinator files.

## Not claimed whatever the outcome

Cause of the historical startup failure; whole-SQL acceptance; full-gate waiver; resident, human, live or Azure approval; any criterion tick or closure (the coordinator decides). A passing O arm is non-reproduction, not proof. If O errors for any reason other than ordering, that is reported as incompatibility. A new source defect or unsafe prerequisite stops the attempt.
