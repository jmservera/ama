---
title: Issue 1292 original-load diagnostic research
ms.date: 2026-11-09
task_id: 1292-original-load-diagnostic-1109
---

## Status

* Research disposition: executed. Planning Readiness: Ready, with one bounded limit (RL-3, start offset of the original overlap is not retained).
* Task: second bounded, unchanged-source diagnosis for #1292. It is not an E5 source correction and not extra correction authority. E4 source corrections are spent (history immutable); one productive source correction remains and is neither spent nor changed here. No source, test, observer or harness behavioural fix is authorized.
* Branch `test/demo-startup-diagnostic-1292-1109`, frozen head `72ca1c9aac6396e19174352a3503f9b5e4ee8643`, local only. Refs #1292 only; every acceptance criterion stays unticked.

## Question

* RQ-1: does the original targeted Core selection, run together with the original six-module API selection, reproduce the SQLite `database is locked` failure on the unchanged pinned runtime (source `8d6f029ca`, equal to base `ef28d4da4` for `src`)?
* RQ-2: if it reproduces, what is the full original exception traceback, `sqlite_errorcode` and raising location at the existing captured-errors seam?

## Why this question

* The prior six-attempt campaign (3 isolated, 3 concurrent with one small `tests.test_auth` companion; 4 observer runs) did not reproduce. It varied neither the original six-module API workload nor I/O load, so it does not show that either is necessary or sufficient (qualification Q1, `.copilot-tracking/changes/2026-11-09-startup-diagnostic-1292-qual-changes.md`).
* The raised exception location (thread, statement, traceback) of the retained failure is unknown because the test asserts `errors == []` and prints only the list.

## Original command and runtime evidence (resolved, not inferred from counts)

* Source of the commands: the retained tmux log `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/rpi-440-sql-wave-checkpoint.log` (lines 290-360), the 440 changes record in worktree `issue-440-sql-checkpoint` (`.copilot-tracking/changes/2026-11-09-sql-wave-checkpoint-440-changes.md`), and raw logs `/home/azureuser/source/ama-demo-wt/logs-440-sqlwave/`.
* Original source: worktree `issue-440-sql-checkpoint`, HEAD `06f408dd7`, base `8d6f029cac004506953f36606862168bbe9d9412`. `git diff --stat 8d6f029ca HEAD -- src` is empty in both that worktree and this one, so `src` is byte-equal.
* Original environment: Python 3.12.3, owned venv `/tmp/i440sw-TmmdQe/venv` created with `python3 -m venv` and `pip install -q -e src/core -e src/agents -e src/api` (empty `pip.log`); `mssql_python` importable from that venv, `pyodbc` not importable; the venv is removed and its package versions were not retained.
* Original Core command (cwd `src/core`): `env -u ZF_TEST_MSSQL -u ZF_SQL_TASK_MANIFEST PYTHONPATH=tests $PY -m unittest -v tests.test_priority_order tests.test_resident_decisions tests.test_sqlstore tests.test_journey_store`, output to `core-store-priority.log`.
  * First run: exit 1, `Ran 421 tests in 224.301s`, `FAILED (failures=1, skipped=158)`; the one failure is `tests.test_priority_order.SqliteLegacyEdges.test_large_legacy_backfill_is_linear_and_survives_concurrent_openers`, `AssertionError: Lists differ: [OperationalError('database is locked')] != []` at `test_priority_order.py:734`. Log sha256 `f3b54e839ea223ee413196d435af11d6b2655b3374958714d1d73cdf9d380218`. Serial rerun (`core-store-priority-r2.log`, `3413ad0cf4a6`): exit 0, 421 tests, 158 skipped.
* Original API command (cwd `src/api`): `env -u ZF_TEST_MSSQL -u ZF_SQL_TASK_MANIFEST PYTHONPATH=../core/tests:../agents/tests:tests $PY -m unittest -v tests.test_case_journey tests.test_auth tests.test_entra_authoritative tests.test_role_endpoint_inventory tests.test_role_matrix tests.test_assistants`, output `api-journey-auth-roles-assistants.log` (`8f630cfb9c10`): exit 0, 263 OK, 58 skipped, tool time 2m22s.
* Original concurrency: the log narrates "Core and API in parallel"; load average was 5.4 at the failing run per the 440 handoff. API (about 142 s) and Core (224.301 s) were separate shell calls; their exact start times and overlap offset are not retained (RL-3).
* Count of 421 and 263 was not used to infer selectors; both selectors are stated verbatim above and match the counts only as a cross-check to verify at run time.

## Prior campaign evidence relevant here

* Prior campaign used `PYTHONPATH` into the worktree `src` directories, no editable install, a timeout of 180 s for one test, and `tests.test_auth` alone as the companion. This campaign changes those three variables back to the original shapes (full selections, original six API modules, 420 s caps, original editable-install import profile).
* The existing failing test and source anchors: `src/core/tests/test_priority_order.py:704-735` (two `threading.Thread` openers call `self.open_store()`, exceptions appended to `errors`), `src/core/src/zava_forward/core/sqlstore.py:224,258` (`PRAGMA busy_timeout=5000`), `_migrate_recommendations` write section. The captured-errors seam is the `except BaseException as error: errors.append(error)` in `opener`.
* The prior observer (`logs-1292-startup-diagnostic/observer_run.py`) wrapped `SqlStore` methods and re-raised; that approach is reused conceptually as an external recorder only. Observer runs perturb timing and failure semantics and are never equivalent to plain runs.

## Prior records and disclosures to carry (new additive note only)

* Prohibited amendment: the owner-side unpublished commit `0e43484f652b774d9daeca5e9cab12899a05bf69` (parent `ec708dda2`) was amended into `72ca1c9aac6396e19174352a3503f9b5e4ee8643` (reflog `commit (amend)`; a one-line addition to the qualification review). The amendment was not authorized. The original `59accfa1c`, `8aea86f8b` and published owner history are unchanged. The process is therefore not fully conforming; this record does not claim that it is. `0e43484f` is no longer an ancestor of HEAD but remains a retrievable object.
* First post-wait traces, qualified precisely (read from the retained `I2/I3/C2/C3.observer.json` for this research; the holder is the thread with the first `BEGIN IMMEDIATE`): in I2 the first later non-holder event at 8.0001 s is a `PRAGMA table_info(recommendations)` statement trace; in I3, C2 and C3 it is a `PRAGMA table_info(cases)` statement trace at 8.4058 s, 8.7021 s and 8.4216 s respectively (I3 and C2 by the second opener thread, C3 by the first). In I3, C2 and C3 a `COMMIT` trace follows within about 0.0005 s, and the observed `COMMIT` and later events come after the first post-wait event, not before it. The numbers are statement-start trace times only, with no return events: they are not COMMIT durations and are not rounded or read as causal.
* The seven prior original records, the external original handoff and the 29-member raw packet stay unchanged. Counts to preserve: 14 original records, 29 raw members, original Reviews.
* FR1 gap (prior plan promised per-module import origins and hashes; only `sqlstore.py` prefix `0b0caf62802d` was retained): corrected prospectively by recording full import origins and sha256 before any attempt in this task. It does not repair past provenance.

## Environment and host facts

* Pinned runtime: source `8d6f029ca` (PR 1308 squash). Fetched `origin/main` `1464b4d850a89aaaf835ba8a9ad98d38aeb1fdd6` differs from this HEAD only in tool, selector, score and tracking paths; `git diff --name-only HEAD origin/main -- src` is empty. It is not merged, and #189 is not merged.
* System python 3.12.3 lacks `fastapi`, `pydantic`, `uvicorn`, `httpx`; the API package's declared dependencies (`aiohttp`, `azure-*`, `mssql-python`) are not installed globally. Whether the chosen profile fails for missing packages is to be established by the first import probe in the plan, after the planning commit.
* Heavy-resource lock: `/tmp/ama-rpi-heavy.lock` exists; `flock`, `fuser`, `lsof` are available. Host `nproc` 4; load 0.25 at 16:47 UTC. Prior load during attempts was 2.5-4.8; the failing original had 5.4 (not reproducible by design; no load is injected).
* Another lane owns `/home/azureuser/source/ama-demo-wt/venv-440-1109`; it is not reused or modified.

## Research limits (RL)

* RL-1: the original package versions and `sqlite3.sqlite_version` are not retained; this run records its own and cannot claim equality.
* RL-2: the failure was a single observation in one run of 421 tests; frequency is unknown. Two attempts cannot estimate it; zero of two would not exclude load, timing or the original venv.
* RL-3: original overlap offset, start order and concurrent host load beyond 5.4 are not retained. This run starts API first and Core immediately after, as the log lists them, and records real timestamps; it does not claim equivalence of timing.
* RL-4: no hosted CI read; the plan authors its own review, not independent.

## Planning Readiness

* Ready. Exact original selectors, working directories, environment unsets and `PYTHONPATH` are identified from retained command text, so the stop-on-missing-witness condition does not apply.
