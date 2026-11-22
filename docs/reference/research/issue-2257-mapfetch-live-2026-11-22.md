---
title: Issue 2257 employee map fetch failure, live evidence
description: Live demo reproduction attempt, platform log correlation and client recovery proof for the intermittent "Map unavailable: Failed to fetch" message
ms.date: 2026-11-22
---

Scope: synthetic demo, desktop only, revision `ca-cutover-test-demo-api--0000050`. Probes and result files are in [issue-2257-mapfetch-live-2026-11-22/](./issue-2257-mapfetch-live-2026-11-22/). Credentials were read at runtime and never printed.

## Findings

* Eight fresh sign-ins at 15:51 to 15:54 UTC loaded 443 markers each with `/api/map` 200 and no failed request ([result](./issue-2257-mapfetch-live-2026-11-22/probe-result-155403.json)). The original failure is not reproduced now that SQL is S3.
* Log Analytics system logs for 14:40 to 15:10 UTC show Readiness and Liveness probe timeouts on the API replicas, a scale to 2 at 14:49:47 and a "Scale down to 1" at 14:56:51, inside the 14:56 to 15:00 failure window. The app runs min 0 to max 4 replicas at 0.5 CPU. A replica leaving the pool resets open connections, which a browser reports as `Failed to fetch` while the server logs nothing. This link is inferred from timing; no request-level trace exists.
* The client treated a transport failure on a read as final. `fetchReadRetrying` now retries a reset read twice (400 ms, 1200 ms) with a plain-language status, never on abort and never for changes.
* Live proof ([result](./issue-2257-mapfetch-live-2026-11-22/recovery-proof-result.json)): with the first `/api/map` aborted by `connectionreset`, the deployed client shows "Map unavailable" with 0 markers; the patched `app.js`, served through Playwright route interception, retries and loads 443 markers without a reload. Screenshots: `map-after-reset-deployed.png`, `map-after-reset-patched.png`.

## Per-criterion status

| Criterion (issue Expected) | Status | Evidence |
| --- | --- | --- |
| The map retries or recovers without a reload | Proven for the patched client (unit test and live interception); not yet deployed | recovery-proof-result.json, `test_workspace_scripts.py` |
| The cause is found | Partly proven: probe timeouts and scale-in coincide with the window; request-level cause unproven | system log query above |
| Failure reproduced on the live demo | Unproven: 0 of 8 failed now; the injected reset reproduces the exact message | probe-result-155403.json |

## Follow-ups

* Deploy the client fix (owner action, no production change made here).
* Consider min replicas 1 and probe timeouts for the demo window; not changed here.
