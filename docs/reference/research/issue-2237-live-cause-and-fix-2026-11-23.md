---
title: Issue 2237 retention 500 cause and fix (2026-11-23)
description: Log Analytics evidence that the live GET /api/retention 500 was the 15 s SQL write-lock timeout, the 503 mapping that fixes it, the live re-proof on revision 0000054 and a per-criterion table
ms.date: 2026-11-23
---

Synthetic demo, desktop only. Refs #2237. Live revisions: `ca-cutover-test-demo-api--0000054` and `ca-resident-demo--0000026` (both active when checked, 2026-11-23 about 01:28 UTC). Evidence files: [issue-2237-retention-500-live-2026-11-23/](./issue-2237-retention-500-live-2026-11-23/). No credentials, tokens or staff e-mail addresses are recorded in them.

## Cause

Earlier notes could not read the container logs. From this host, `az monitor log-analytics query -w 3f6f76f1-9d76-413d-bc86-bcbc92fce2be` (workspace `log-cutover-test`, tables `ContainerAppConsoleLogs`, `ContainerAppHTTPLogs`, `AzureDiagnostics`) now succeeds.

| Observation | Evidence file |
| --- | --- |
| 11 HTTP 500s on `/api/retention` between 2026-11-21 06:12 and 2026-11-22 10:34 UTC, revisions 0000038, 0000040, 0000042, 0000043, 0000046; every request lasted 15.04 to 15.39 s | [law-retention-http-5xx.json](./issue-2237-retention-500-live-2026-11-23/law-retention-http-5xx.json) |
| Each has the console line `http-error GET /api/retention status=500 exc=ProgrammingError` | [law-retention-500s.json](./issue-2237-retention-500-live-2026-11-23/law-retention-500s.json) |
| The driver message is `[SQL Server]could not take the write lock`; a SQL `Errors` event (error 50002) with the same message falls within about a second of the 500 at 2026-11-21 06:12:36, 2026-11-21 22:56:11 and 2026-11-22 10:34:49 | [law-startup-lock-traceback-2026-11-22T10-34.json](./issue-2237-retention-500-live-2026-11-23/law-startup-lock-traceback-2026-11-22T10-34.json), [law-sql-errors-summary.json](./issue-2237-retention-500-live-2026-11-23/law-sql-errors-summary.json) |
| 1059 such lock timeouts in 4 days, in bursts (peak 182 in one hour) | [law-lock-timeouts-per-hour.json](./issue-2237-retention-500-live-2026-11-23/law-lock-timeouts-per-hour.json) |
| The same `ProgrammingError` 500 hit briefing, map, exceptions, AI report, uploads, time capture and chat endpoints | [law-programmingerror-by-endpoint.json](./issue-2237-retention-500-live-2026-11-23/law-programmingerror-by-endpoint.json) |

Mechanism: `mssqlstore.BEGIN` takes `sp_getapplock 'zavaforward_write'` with a 15 000 ms timeout and throws 50002 on failure; only start-up retries it (issue #2244). `Store.retention_due` is a GET that writes the `retention_job_listed` audit entry, and `SqlStore._finish` writes pending audit entries under that lock. A writer holding the lock for more than 15 s therefore turns the listing into a 500. The role does not matter: the 2204 failure was ProgrammeManager only because that role can reach the endpoint.

Not established: which writer held the lock each time (the logs show contention, not the holder). The issue text dates the 2204 failure from 10:48 UTC; the nearest logged 500 is 10:34:34 UTC, so the issue time is probably approximate.

## Fix (local commit, not deployed)

* `core/mssqlstore.py`: `is_write_lock_busy(exc)` recognises the driver `ProgrammingError` or `DatabaseError` carrying the lock text, through the exception chain, without importing the optional driver.
* `api/server.py` `_unhandled`: a busy lock before the response starts answers a GET or HEAD request with 503 and `Retry-After: 5` and a plain-language message, and logs `http-error GET <path> status=503 exc=ProgrammingError cause=sql-write-lock-busy at=<frame>` (no message text). Every other failure, including a POST that hits the same timeout (it may follow a committed step), keeps the 500 path. The audit write still fails closed; it is never skipped.
* Tests: three helper cases in `src/core/tests/test_mssql_startup_lock.py`; two API cases in `src/api/tests/test_error_logging.py` (503 with `Retry-After`, secret-free log; an unrelated driver error still answers 500). The 503 test fails without the server change (500, no header).

## Live re-proof (revision 0000054)

[live_probe.py](./issue-2237-retention-500-live-2026-11-23/live_probe.py) signs in with the demo employee account (read at runtime, not printed). [r54-role-2026-11-23T01.json](./issue-2237-retention-500-live-2026-11-23/r54-role-2026-11-23T01.json): `/api/me` role `Retrofit Programme Manager`; `/api/retention` 200 with keys `as_of`, `label`, `records` and 0 records; 15 sequential, 20 parallel and 20 mixed requests all 200. [r54-2026-11-23T01.json](./issue-2237-retention-500-live-2026-11-23/r54-2026-11-23T01.json) is the same probe a minute earlier. The fix is not on the live revision, and a lock timeout cannot be provoked on demand without a production-affecting load, so the 503 path is proven by unit test only.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Reproduce | Proven in history, not on demand | 11 logged 500s of about 15 s; a deterministic local reproduction (audit write raising the lock error) is the new test; live reproduction needs a lock held for over 15 s, not attempted (no drills) |
| Find the cause in the demo container logs | Proven | Console, HTTP and SQL `Errors` records above; lock holder unidentified |
| Fix with a regression test | Proven locally | Code and tests in this commit; not deployed because publishing is out of scope for this task |
| Re-prove 200 live | Proven on 0000054 | Programme Manager account, 55 of 55 requests 200 |

Owner-gated or out of scope: deployment of the fix; finding the lock holders and reducing lock hold time (a design change).
