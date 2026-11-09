---
title: Issue 1292 startup lock diagnostic changes
ms.date: 2026-11-09
---

## Changes

* No source, test, workflow or infrastructure change. Only this task's `.copilot-tracking` records were added (research, plan, details, critique, state, changes, review), the planning four committed first as `8aea86f8b`.
* Raw evidence (not committed): `/home/azureuser/source/ama-demo-wt/logs-1292-startup-diagnostic/` with `SHA256SUMS` (29 entries), `attempt.sh`, `observer_run.py`, per-attempt `.log`, `.meta`, `.observer.json`, `analysis.txt` and `harness-defect/`.

## Environment and identities

* Base `ef28d4da42d83b111d48f14df9b70e3c4932a477`. Owned venv directory `/tmp/i1292sd-*` (stdlib plus nothing installed; no pip install was needed). Project imports from the worktree via `PYTHONPATH` (`tests:../core/src:../agents/src:../api/src`), bytecode writes disabled. Import origins: `zava_forward.core|api|agents` namespace paths all under `src/*/src/zava_forward/*` of this worktree; `sqlstore.py` sha256 prefix `0b0caf62802d`.
* Host: 4 cores, load average 2.5-4.8 throughout (other sessions share it).

## Attempts (cap 3 isolated plus 3 concurrent; all six used, no retry)

* Command (all): `cd src/core; PYTHONPATH=... python -m unittest -v tests.test_priority_order.SqliteLegacyEdges.test_large_legacy_backfill_is_linear_and_survives_concurrent_openers` (OBSERVER runs use `observer_run.py`, which loads the same test name).
* I1 plain isolated: exit 0, `Ran 1 test in 15.853s`, OK.
* I2 OBSERVER isolated: exit 0, 15.161s (observer wall 15.29s), OK.
* I3 OBSERVER isolated: exit 0, 15.597s, OK.
* C1 plain concurrent with API `tests.test_auth` (41 tests, exit 0, 21.2s, started 3 s before): exit 0, 15.768s, OK.
* C2 OBSERVER concurrent: exit 0, 15.918s, API exit 0, OK.
* C3 OBSERVER concurrent: exit 0, 16.097s, API exit 0, OK.
* Harness defect, not an attempt: the first I2 attempt executed no test (`ModuleNotFoundError: tests`, 0.000s) because the script directory, not the cwd, was on `sys.path`. The observer was corrected (`sys.path.insert(0, os.getcwd())`) and I2 was rerun; the defective log is retained in `harness-defect/`.
* The API companion overlapped the opener phase in C1-C3 (the companion ran about 21 s from 3 s before the Core test), but it was light: load average stayed below 5, below the 5.4 of the failing run, and the companion was one 41-test module rather than the six-module selection of that run.

## Observer findings (OBSERVER, inference from `set_trace_callback` events; trace fires at statement start)

* No exception was raised in any of the six attempts; the observer recorded zero raises.
* In each observed run one opener thread holds the SQLite write lock in `_migrate_recommendations` (`BEGIN IMMEDIATE`, `_review_priority_order`, `_backfill_zero_ordinals`, `COMMIT`) while the other waits in its own `BEGIN IMMEDIATE`. Upper bound of the write-lock hold, from the holder's `BEGIN IMMEDIATE` to the waiter's first statement inside the section: I2 3.13 s, I3 3.15 s, C2 3.25 s, C3 3.05 s. Of this, the Python backfill is 1.10-1.17 s and the `COMMIT` of the 30000 updated rows is 1.80-2.03 s. The "waiter_blocked" field in `analysis.txt` is unreliable for I3, C2 and C3 (trace ordering) and is not used.
* The product wait limit is 5.0 s (`sqlite3.connect` default timeout, then `PRAGMA busy_timeout=5000`). The observed hold is therefore about 61-65 percent of the limit. A stretch of roughly 1.6 times in the holder (CPU contention or slow commit I/O) would make the waiter's `BEGIN IMMEDIATE` exceed 5 s and raise `OperationalError: database is locked`, exactly the retained error class. This is a candidate mechanism consistent with the evidence (H1), not a reproduction.

## Unchanged-source proof

* `git status --short --ignored` empty before and after; `git diff --stat ef28d4da4 -- src infra tools .github pyproject.toml` empty. Committed HEAD changes only `.copilot-tracking`. Nontracking source equivalence: same `ef28d4da4` tree for those paths.

## Hypotheses status

* H1 (hold above the 5 s wait limit under load): supported by measured margin only; not reproduced. H2, H3, H4: no evidence for or against; no `BUSY_SNAPSHOT` or off-section lock wait was observed.
