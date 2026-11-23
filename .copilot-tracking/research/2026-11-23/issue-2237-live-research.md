# Issue 2237 live research (2026-11-23)

Research disposition: executed. Planning Readiness: Ready.
Scope: synthetic demo, desktop only. Live revisions `ca-cutover-test-demo-api--0000054` and `ca-resident-demo--0000026`. Refs #2237.

## Acceptance criteria (issue body)

1. Reproduce the 500.
2. Find the cause in the demo container logs.
3. Fix with a regression test.
4. Re-prove 200 live.

## Key new finding

Earlier passes (2026-11-22) could not query Log Analytics. From this host, with the existing login, `az monitor log-analytics query -w 3f6f76f1-9d76-413d-bc86-bcbc92fce2be` (workspace `log-cutover-test`) now works. Tables used: `ContainerAppConsoleLogs`, `ContainerAppHTTPLogs`, `AzureDiagnostics` (category `Errors`). Evidence files are in `docs/reference/research/issue-2237-retention-500-live-2026-11-23/`.

* `law-retention-http-5xx.json`: 11 HTTP 500 responses for `/api/retention` between 2026-11-21 06:12 and 2026-11-22 10:34 UTC (revisions 0000038, 0000040, 0000042, 0000043, 0000046). Every one took 15.04 to 15.39 s.
* `law-retention-500s.json`: the matching console line for each: `http-error GET /api/retention status=500 exc=ProgrammingError at=exceptions.py:583:raise_exception`.
* `law-startup-lock-traceback-2026-11-22T10-34.json` and the console log of revision 0000047 at 10:34:48: `mssql_python.exceptions.ProgrammingError: ... [Microsoft][SQL Server]could not take the write lock`. A SQL `Errors` event with number 50002 and the same message lands within about a second of the retention 500 at 2026-11-21 06:12:36, 2026-11-21 22:56:11 and 2026-11-22 10:34:49.
* `law-sql-errors-summary.json`: 1059 SQL error events with number 50002 in 4 days; the other SQL errors (208, 207, 8116, 297, 37387) are different failures.
* `law-lock-timeouts-per-hour.json`: lock timeouts cluster in bursts (peak 182 in the hour from 12:00 UTC on 2026-11-22).
* `law-programmingerror-by-endpoint.json`: the same `ProgrammingError` 500 also hit `/api/briefing`, `/api/map`, `/api/exceptions`, `/api/ai/report`, `/api/continuity/export`, `/api/time/*`, upload and chat endpoints, so retention is one victim of a shared condition.

## Root cause

`src/core/src/zava_forward/core/mssqlstore.py` serialises every write on one SQL application lock: `BEGIN` runs `sp_getapplock @Resource='zavaforward_write', @LockMode='Exclusive', @LockTimeout=15000` and then `THROW 50002, 'could not take the write lock'`. Only start-up retries it (issue #2244, `startup_retries`). At run time the error propagates as the driver's `ProgrammingError` (SQLSTATE 42000).

`Store.retention_due` (`src/core/src/zava_forward/core/doc_controls.py`) looks like a read, but it calls `self.audit(..., "retention_job_listed", ...)`. `SqlStore.audit` queues the entry and `_SyncLock.__exit__` -> `_finish` writes it with `BEGIN IMMEDIATE`, which needs the global write lock. When another writer holds the lock for more than 15 s (bursts of concurrent writers during live proofs and replica start-up migrations), the audit write times out and the request answers 500 after 15 s. The handler catches only `PermissionError`, so `_unhandled` answers a generic 500 and logs only `exc=ProgrammingError`, which hid the lock cause. Nothing in the logs points at stored case data, so the malformed-record candidates in the 2026-11-22 note are not supported for these 11 failures.

Not established: which writer held the lock each time. The logs show contention, not the holder. The issue text dates the 2204 failure from 10:48 UTC; the nearest logged retention 500 is 10:34:34 UTC (HTTP log), so the issue time is probably approximate.

## Criterion status

| Criterion | Status | Evidence |
| --- | --- | --- |
| Reproduce | Proven historically, not re-triggerable on demand | 11 logged 500s of about 15 s each; later probes returned 200 on 0000047 to 0000054 because no writer held the lock. A deterministic local reproduction is added as a unit test (lock timeout during the audit write) |
| Find the cause in the container logs | Proven | Console, HTTP and SQL `Errors` records above; lock holder not identified |
| Fix with a regression test | Implemented locally, not deployed | See plan and changes; deployment needs a push, which this task forbids |
| Re-prove 200 live | Proven on 0000054 for the Retrofit Programme Manager demo account (2026-11-23 about 01:28 UTC) | `r54-role-2026-11-23T01.json`: `/api/me` role `Retrofit Programme Manager`, `/api/retention` 200, 15 sequential, 20 parallel and 20 mixed all 200 |

## Options considered

* Retry the write lock at run time. Each attempt waits 15 s; two attempts exceed typical client timeouts and still fail under sustained contention.
* Skip the audit when the lock is busy. Rejected: the audit ledger is a control and must not be bypassed.
* Report a busy lock as 503 with `Retry-After` and a log line that names the cause. Chosen: it is the honest, retryable status, fails closed, and makes the next occurrence diagnosable. It applies to every handler, since `_unhandled` is the shared path.

## Follow-ups (candidates, not committed)

* Find the lock holders (needs the live SQL session view; owner-gated if it needs estate change).
* Shorten write transactions or split the global lock; larger design change.
