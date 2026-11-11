---
title: Issue 144 permit SQL boundary plan
description: Prospective plan for real disposable-MSSQL validation of the worker-permit clock and lock boundary and stored-permit result attribution
ms.date: 2026-11-11
task_id: issue-144-permit-sql-1111
---

## Objective

Close only the retained validation gap: observe `Assistants.issue_permit` (E1 clock and lock boundary) and `Assistants.complete_result` (E2 stored root and meter-id attribution) on an actual owned disposable SQL Server, with a real independent task-row lock holder, deterministic database-clock coordination, a positive control and negative controls. No production code change is authorised. A real source defect found stops the work for Root on the existing #144 evidence, with no fix, no new issue and no cycle spent.

## Status

* Phase gate: Research done, Plan done (this document). STOP before Implement. Nothing below has been run.
* Counter: E1/E2 of the Nov 10 five spent, three remain. This launch spends none. No reset, no new five.

## Admission options for Root

* Option U, unchanged-source observation. Author the test module outside the repository under the external ROOT, run it against the unchanged tree, commit nothing. Spends no cycle. Evidence is not durable in the repository.
* Option T, one test-only E3. Commit the same module to the allowed path below. Spends E3 (two remain). Recommended if a durable local regression is wanted; the caveat is that hosted CI and `SQL_SELECTORS` will not select it (see decision D2).
* Both options use the identical module, commands and controls. The plan below assumes T and notes the U differences.

## Allowed paths (Option T)

* New: `src/api/tests/test_permit_sql.py` (one module, test code only).
* New dated RPI records under `.copilot-tracking/` for the later phases (changes, review, state).
* Forbidden: `assistants.py`, `ai_consumption.py`, `mssqlstore.py`, any other `src/**/src` file, `test_ai_consumption_api.py`, `test_assistants.py`, `sqlguard.py`, workflows, `tools/rpi-checks.py`, `pyproject.toml`, requirements, Dockerfiles, `infra/`.

## Test module design

Module `test_permit_sql`, class `MssqlPermitBoundary(unittest.TestCase)`. Decorators: `@unittest.skipUnless(os.environ.get("ZF_TEST_MSSQL") == "1", "needs disposable SQL Server (ZF_TEST_MSSQL=1)")`, the exact existing tolerated skip text. `setUpClass` calls `sqlguard.require_task_owned_loopback(os.environ)` before any connection. `setUp` composes a fixture `class SqlBase(MssqlFixture, Base)` imported from `test_assistants`, an `Ai()` as `ConsumptionApi.setUp` does (no HTTP server is needed because permit paths never send), and reuses the existing helper bodies by assignment from `ConsumptionApi` (`authority`, `records`, `permit_setup`, `permit_request`, `reserved`, `kinds`, `lease`, `used_calls`, `permitted_result`) so no helper is copied and `test_ai_consumption_api.py` is untouched. Importing `ConsumptionApi` as a module attribute (`import test_ai_consumption_api as base`) avoids discovery collecting it twice.

Test database: the existing `zf_test_assistants` in the owned container; `MssqlFixture.setUp` drops the assistant tables per test, so the module must not run concurrently with other `Mssql*` assistant classes (serial, single container).

### Lock-holder and observer helpers (all real SQL)

* Holder: a second `_Conn` from `self.store.assistant_connection()`, `execute("BEGIN TRAN")` then `UPDATE assistant_tasks SET revision=revision+1 WHERE id=?` for the task row; no applock. `SELECT @@SPID` gives the holder SPID. Release is `IF @@TRANCOUNT > 0 ROLLBACK TRAN`.
* Claimant: a thread calling the actual `self.service.issue_permit(...)` (its own connection from `Assistants.transaction`, so it takes the global applock first, then blocks on the task row). The thread stores the result or the exception. `join` uses one bounded deadline (60 s); a live thread fails the test, no retry.
* Observer: a third connection polling, at 100 ms intervals and bounded to 30 s, `sys.dm_exec_requests` joined to `sys.dm_exec_sql_text` for a request whose `blocking_session_id` equals the holder SPID. Assertions on the observed row: `wait_type` starts with `LCK_M_`, the statement text contains `UPDATE assistant_tasks SET revision=revision+1`, `wait_resource` starts with `KEY:` (a row key), and `sys.dm_tran_locks` shows the blocked session already holds a granted `APPLICATION` lock (lock order: applock first, then task row). This proves a real wait, not a timing guess.
* Clock: every number is database time from `service.now(db)` (the production expression). Release of the holder is gated on the holder connection reading a database time at or beyond a threshold computed from stored rows, polled at 100 ms; no host `sleep` decides an outcome. A passthrough wrapper on `service.now` (calls the real query, records `(thread name, db time)`) is allowed because it changes nothing; it is not a patched predicate or fake store.
* Preconditions asserted before the claimant starts, as invalid-setup failures with no retry: the pre-launch database time is below the stale threshold (so the frozen routine would grant), and the planned release time is at or beyond the fresh threshold.

### Deterministic cases (7)

1. `test_lock_wait_crossing_the_lease_margin_refuses_without_a_reservation`. Set `lease_until = L0 + 42` (L0 database time). Stale threshold: grant if the pre-lock read plus 38 is below the lease, so a pre-lock read near L0 grants. Fresh threshold: deny when `now >= lease_until - 38 = L0 + 4`. Holder releases when its database time reaches `L0 + 4.5`. Expect `{permit: False, reason: lease-expiring}`; the first `service.now` read in the claimant thread is at or after the recorded release time; zero `reserved` records; no `permitted` marker; allowance `used_calls` unchanged from before the call; observed block recorded. Discriminating against the original defect.
2. `test_lock_wait_crossing_authority_expiry_refuses_and_refunds`. `permit_setup(authority_seconds=8)` and `lease(…, 120)`. Deny when `now >= end - 2.0`. Release at `end - 1.5`. Expect `authority-expiring`, zero reservations, no marker, `used_calls == before - 1`, one `permit-denied` event. Guards the E1 expiry-at-reservation path; expected not to discriminate the stale-clock mutant because `reserve_in` reads its own clock (to be observed in control N1).
3. `test_valid_window_after_a_real_lock_wait_grants_with_post_lock_time`. Positive control. Lease 120, far authority. Holder is released once the block is observed and its database time is at least 1.0 s beyond the observation. Expect `permit True`; one `reserved` record equal to `meter_id`; `issued_at >=` the recorded release time; `lease_remaining == lease_until - issued_at` (stored `lease_until` read back); `dispatch_within_ms >= 1`; `permitted` marker present; attempt outcome `sending`; a second call returns `duplicate-permit` with still one reservation (idempotence). Its `issued_at` assertion also fails on the stale mutant.
4. `test_unavailable_send_fence_refuses_without_a_reservation_or_a_marker` (SQL round trip of the existing `attempt-ended` branch: set `assistant_attempts.active_until=0`, expect `send-fence-refused`, zero reservations, `send-refused` event, no `permitted`, `used_calls == before - 1`). Operator-disable and consent/readings paths remain SQLite-only predicate-patched evidence and are not mirrored.
5. `test_permitted_result_binds_attribution_to_the_stored_reservation_root`. Real permit, then `complete_result` with the root omitted: the `output` record carries `reserved[0]["root"]` and the meter completes once, mirroring the existing SQLite assertions on the same values.
6. `test_permitted_result_rejects_conflicting_attribution_without_settling`. Conflicting `meter_root` and conflicting `meter_id` each return False, write `result-rejected`, leave zero `completed` records and unchanged allowance, then the matching result still settles once.
7. `test_permitted_failure_without_root_settles_the_meter_and_publishes_no_output`. Failure outcome with no output: meter settles as unavailable, no `output` record, no review attribution.

Distinction retained: cases 1-3 prove E1 expiry-at-reservation and the post-lock clock use; case 4 proves the send-fence refund on SQL; cases 5-7 prove E2 stored root and meter-id attribution and review accounting inputs. Case 3 also records `dispatch_within_ms`, the E1 dispatch window computed after reservation; the dispatch-time recheck itself is the worker (B scope) and is not covered.

## Negative controls (external mutants, never in the repository)

* N1, stale-clock mutant. Copy `src/core` to an external directory and move the single statement `now = self.now(db)` in `issue_permit` to before the `UPDATE assistant_tasks ... revision+1`, which is the shape in frozen `a482d787` `assistants.py` 1047. Record `diff -u` and sha256 of both files. Expected observation: case 1 fails (permit granted after the margin), case 3 fails on the `issued_at` assertion, case 2 passes, 4-7 pass.
* N2, attribution mutant. Copy `src/core` and restore the pre-E2 `complete_result` shape (forward the caller envelope, no `_permitted_root` check). Expected: cases 5 and 6 fail, others pass.
* Each mutant runs in its own venv with editable installs of the mutant core and the real agents and api of this worktree, import origins asserted, the same container and the same test file. Results are reported as observed. A control that does not fail where predicted is reported as a non-discriminating assertion, not repaired.

## Environment and bindings

* Own external ROOT directory `ROOT/144-permit-sql-1111/` for venvs, scripts, logs, manifests and cache; `PYTHONDONTWRITEBYTECODE=1`; external `--cache-dir`/mypy cache; nothing written into the worktree except Option T files.
* Venv V: `python3.12 -m venv`; `pip install --require-hashes -r src/api/requirements.txt`, then `pip install --no-deps -e src/core -e src/agents -e src/api` (the CI command). Needs network access to the package index (Root admission item A5). Asserted bindings: `zava_forward.core`, `zava_forward.agents`, `zava_forward.api` resolve under this worktree; `mssql_python` 1.15.0 and `mssql_python_odbc` 18.6.2.1 (or the versions in the hashed requirements, recorded); ruff and mypy versions from `pip freeze` recorded. Test-only `PYTHONPATH=tests:../core/tests:../agents/tests` is the repository convention for test helper modules, not a source workaround.
* Image: `mcr.microsoft.com/mssql/server:2022-latest` by image id `cf8f0ab2ebe6...` (full id and digest read again at run time and compared with `sha256:cf8f0ab2ebe61feec2eed2629061a07d247f791c2a8ddda74a4ac9f06a291718`); no pull.

## Exact bounded command set (Option T)

All producers write unique immutable files under `ROOT/144-permit-sql-1111/logs/NN-name.{out,err}` and record `$?` into `NN-name.exit` on the very next statement; no `tail`, `tee` or pipes mask a producer; the first failure's full trace is kept; reruns get new names.

* C0 identity: `git rev-parse HEAD`, `git rev-parse HEAD^{tree}`, `git status --short --ignored`.
* C1 venv and pip install (A5), `pip freeze`, and import-origin assertion.
* C2 static, from `src/api`: `ruff check --no-cache tests/test_permit_sql.py`, `ruff format --check --no-cache tests/test_permit_sql.py`, `mypy --cache-dir <external> tests/test_permit_sql.py tests/test_ai_consumption_api.py` using the api `pyproject.toml` (strict). If the module needs `# type: ignore[import-untyped]` as `test_ai_consumption_api.py` does, the same existing convention applies.
* C3 SQLite carry-forward (no heavy lock): `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest -v test_ai_consumption_api.ConsumptionApi` the 15 existing permit, E1 and E2 methods by exact id (listed in the phase details; lines 1717-2006 of the file), plus `python -m unittest -v test_permit_sql` with the flag unset to record the exact tolerated skip count and reason.
* C4 heavy admission: `flock -n /tmp/ama-rpi-heavy.lock <driver>`; busy means stop and report UNADMITTED, no queue, spin or kill. The driver records the actual holder before and after.
* C5 inside the lock: `docker image inspect` (id, digest), `docker run -d --name zf-144-permit-sql-1111 --label zf.task=1292-sql-disposable --label ama.rpi.owner=<token> --memory=3g --cpus=2 --publish=127.0.0.1::1433 --env=ACCEPT_EULA=Y --env=MSSQL_PID=Developer --env=MSSQL_MEMORY_LIMIT_MB=2048 --env=MSSQL_SA_PASSWORD` with a random password that is never logged; `docker inspect` receipt; `sqlguard.write_manifest` with a private `0600` file; bounded readiness (at most 40 probes of `SELECT 1`, not a test retry); SQL Server version query.
* C6 real SQL, same container: `ZF_TEST_MSSQL=1 ZF_SQL_SERVER=127.0.0.1 ZF_SQL_PORT=<port> ZF_SQL_DATABASE=master ZF_SQL_AUTH=password ZF_SQL_USER=sa ZF_SQL_PASSWORD=<redacted> ZF_SQL_TRUST_CERT=1 ZF_SQL_TASK_MANIFEST=<file> python -m unittest -v test_permit_sql.MssqlPermitBoundary` in venv V. A DMV permission failure is reported as such, never skipped.
* C7 negative controls N1 and N2 in their venvs, same container, same file, separate logs and exits.
* C8 cleanup and readback: remove only the exact captured container id after label and name check; `docker inspect` of the id must fail; leftover query for databases and manifests created by the task; remove only the resolved owned manifest and directories after hashing the logs; verify the lock is released.
* C9 final: `git status --short --ignored` empty for Option U or showing only the one new test file before commit for Option T.

## Pass criteria (not a blanket gate, and no skip counted as a pass)

* C6 exit 0, the framework line `Ran 7 tests` and `OK` with no `skipped=` and no `(skipped` lines, each of the 7 ids reported `ok`, and the DMV observation recorded for cases 1-3 (blocking SPID, wait type, wait resource, applock held).
* C3 SQLite selectors OK with the existing skip count unchanged; the flag-unset run of the new module shows only the tolerated skip text.
* C2 exit 0 for all three producers.
* N1 and N2 observed as predicted or reported as non-discriminating.
* Cleanup receipts: container id gone, lock free, no leftover owned files.

## Not covered and explicit limits

Local SQL Server 2022 Developer only; not Azure SQL; no provider, model, credential, consent grant, spend, deployment, worker, queue, server route, publisher, date or backoff scope; no full or `--changed` gate; hosted CI will not select the new module unless a workflow or gate-tool edit is separately admitted at the full tier (D2).

## Decisions and authority for Root

* D1: choose U or T (cost: none or one of three remaining cycles).
* D2: whether to wire the module into `src-ci.yml` or `SQL_SELECTORS`. Not in this plan; full-tier by repository policy.
* D3: admit the network `pip install` for new pinned venvs (V, M1, M2), or supply a wheelhouse.
* D4: if the real-SQL run shows the fixed source failing a case, treat it as a source defect: evidence on #144 and stop; no fix and no cycle.
