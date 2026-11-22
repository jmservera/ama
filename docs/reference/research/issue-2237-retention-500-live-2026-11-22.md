---
title: Issue 2237 GET /api/retention 500 on the live demo API (2026-11-22)
description: Live investigation of the one-off 500 from GET /api/retention for ProgrammeManager on ca-cutover-test-demo-api, with the evidence that the cause cannot be recovered and a per-criterion proven and unproven table
ms.date: 2026-11-22
---

Synthetic demo, desktop only. Refs #2237 (found by the #2204 live role proof, run 2026-11-22 from 10:48 UTC; its probe list is `live-all-roles.json` on branch `docs/issue-2204-roles-live`).

## What was found

* The 500 was a single probe result for ProgrammeManager (`/api/retention`: 500; the same run returned 403 for the other eight roles and 200 for `/api/cases`, `/api/stats`, `/api/finance`, `/api/packages`, `/api/funding` and `/api/audit-check`). The 2204 run recorded status codes only, no response body or time.
* The handler (`src/api/src/zava_forward/api/server.py`, `/api/retention`) catches only `PermissionError`. Any other exception reaches `_unhandled`, which logs `http-error GET /api/retention status=500 exc=<class> at=<file:line:function>` and answers 500. `retention_due` in `src/core/src/zava_forward/core/doc_controls.py` is the only GET handler there that also writes an audit entry (`retention_job_listed`), so a transient audit commit failure is one candidate. A malformed stored date or contact record is another. Neither is proven.
* The app is `ca-cutover-test-demo-api` revision `0000047` (created 10:34 UTC), scale 0 to 4 replicas with `cooldownPeriod` 300 s. The replica now running started at 11:20:59 UTC, after the 500, so the replica that served the failing call no longer exists.

## Evidence of why the cause cannot be recovered

| Source | Result |
| --- | --- |
| `az containerapp logs show -n ca-cutover-test-demo-api -g ama --tail 300 --format text` (11:28 and 11:29 UTC) | Only the current replica: four start-up and auth lines from 11:20:59 to 11:21:14 UTC. No `http-error` line. |
| `az monitor log-analytics query` on `log-cutover-test` | Refused: `InsufficientAccessError`, `NspValidationFailedError`, workspace public query access disabled. |
| `az monitor app-insights query` on `appi-cutover-test` | Refused: `InsufficientAccessError`. |

Changing the workspace network settings or perimeter would be an Azure estate change that the owner decisions of 2026-11-18 do not authorise for this task, so it was not attempted.

## Live re-proof (2026-11-22, about 11:29 UTC, revision 0000047)

[live_probe.py](./issue-2237-retention-500-live-2026-11-22/live_probe.py) signs in with the demo employee account (read at runtime, not printed) and calls the API from the browser session. Results are in [before.json](./issue-2237-retention-500-live-2026-11-22/before.json) and [after-burst.json](./issue-2237-retention-500-live-2026-11-22/after-burst.json).

* `GET /api/retention` returned 200 with keys `as_of`, `label`, `records` and 0 records.
* A burst of 15 sequential, 20 parallel and 20 mixed (half `/api/cases`) requests all returned 200 (55 of 55).
* The container log after the burst showed no `http-error` line.

## Decision

No source change. A code change would be a guess at an unobserved failure, and the candidates differ in the right behaviour: a malformed record that is skipped silently could hide a due retention item. The class and frame that `_unhandled` logs would settle it, so the next occurrence should be captured at once with `az containerapp logs show` (before scale to zero) and the response time recorded.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Reproduce | Unproven | 55 of 55 calls returned 200 on revision 0000047; the original failure is not reproducible now |
| Find the cause in the demo container logs | Unproven | Failing replica gone; Log Analytics and Application Insights refuse queries from this host |
| Fix with a regression test | Not applicable | No cause established; a speculative fix was rejected for the reason above |
| Re-prove 200 live | Proven for the demo account on revision 0000047, 2026-11-22 | `before.json`, `after-burst.json`. The account's assigned role at probe time was not re-read; the original failure was for ProgrammeManager |
