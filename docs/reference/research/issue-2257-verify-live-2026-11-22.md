---
title: Issue 2257 verify-fixed, live evidence on revision 0000053
description: Re-verification that main and the deployed demo recover from a dropped first /api/map request, with the per-criterion status
ms.date: 2026-11-22
---

Scope: synthetic demo, desktop only, `ca-cutover-test-demo-api--0000053` (Healthy, 100 percent traffic, created 2026-11-22 19:38 UTC, after the #2261 merge). Scripts and results are in [issue-2257-verify-live-2026-11-22/](./issue-2257-verify-live-2026-11-22/). Credentials were read at runtime and never printed. No Azure resource was created or changed. Earlier evidence for the same issue is in [issue-2257-mapfetch-live-2026-11-22.md](./issue-2257-mapfetch-live-2026-11-22.md).

## Does main already fix it

Yes for the client. Commit 0234e8e79d (#2261) added `fetchReadRetrying` in `src/api/src/zava_forward/api/web/app.js`; every read in `api()` (including the `/api/map` call in the map draw) retries a transport failure twice (400 ms, 1200 ms) with the status "The connection dropped. Trying again.", never on abort and never for changes. The unit test `test_first_load_reads_retry_a_cold_start_gateway_failure` covers the helper with a different path (`/api/law/alerts`); this task adds a test pinned to the map path (see the changes record).

## Live proof

* Injected reset ([recovery-proof-result.json](./issue-2257-verify-live-2026-11-22/recovery-proof-result.json), 23:02 UTC): the first `/api/map` was aborted with `connectionreset`. The deployed revision 0000053 requested the map again, received 200 and showed 443 markers with no "Map unavailable" message. The 2026-11-22 earlier run showed the previous deployed revision (0000050) failing the same test, so the client fix is now deployed. Screenshots: `map-after-reset-deployed.png` and `map-after-reset-patched.png`.
* Eight fresh sign-ins ([probe-result-230459.json](./issue-2257-verify-live-2026-11-22/probe-result-230459.json), 23:03 to 23:05 UTC): each loaded 443 markers in 3.5 to 6.2 s with `/api/map` 200 and no failed request.

## Cause

Not isolated at request level. The earlier note correlates the 14:56 to 15:00 UTC failures with API replica Readiness and Liveness probe timeouts and a "Scale down to 1" event at 14:56:51 (min 0, max 4 replicas, 0.5 CPU). A replica leaving the pool resets open connections, which a browser reports as `Failed to fetch` while the server logs nothing. That is an inference from timing; no request-level trace exists, and none can be recovered retroactively.

## Per-criterion status

| Criterion (issue Expected) | Status | Evidence |
| --- | --- | --- |
| The map retries or recovers without a reload | Proven on the deployed demo (injected reset) and by a unit test on the map path | recovery-proof-result.json, screenshots, regression test |
| The cause is found | Partly proven: platform events coincide with the window; request-level cause unproven | earlier note, system-log correlation |
| Failure on a fresh sign-in is gone | Observed, not proven: 0 of 8 failed now; the original 3 of 8 rate was not reproducible without replica churn | probe-result-230459.json |

## Follow-ups

* Consider min replicas 1 and probe timeouts for the demo window (owner action; not changed here).
