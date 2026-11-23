# Research 2244 live r3 (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

Scope: r2 follow-up 2, the API StartUp probe window against the start-up lock retry budget (criterion C4). Demo owner decisions of 2026-11-18 apply: no drills, no production change, read-only Azure. The issue has no tick-box list; C1 to C5 come from the first 2026-11-23 note. Prior notes already prove C1 and C2 and leave C3 to C5 open.

## Evidence

* Live (read-only `az containerapp show`): revision `ca-cutover-test-demo-api--0000055` Healthy; StartUp probe initialDelay 1 s, period 3 s, failureThreshold 40, so the window is 121 s.
* Code: `MssqlStore` and, since r2, the law store retry a `BEGIN` lock timeout 8 times. Each attempt waits at most `@LockTimeout = 15000` ms (`mssqlstore.py` line 87) and sleeps 1, 2, 4, 8, 16, 30, 30 s between attempts: 8 x 15 + 91 = 211 s worst case per start-up transaction.
* Bicep `infra/modules/containerapps.bicep` line 263 is the only API StartUp probe; tests `test_container_hosting_completeness` (budget 60 to 300 s) and `test_bicep_policy` (exact probe equality for the API) pin it.
* Consequence: with a writer holding the lock for more than 121 s, the platform kills the replica before the retry budget is spent, so retry cannot prevent the restart loop that issue #2244 describes.

## Selected work

Raise the API StartUp failureThreshold to 80 (1 + 3 x 80 = 241 s, above 211 s, inside the existing 300 s test ceiling) and pin the relationship in a test that derives the retry budget from `mssqlstore` constants. Not deployed; deployment is a production change reserved to the owner.
