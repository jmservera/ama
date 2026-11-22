---
title: Issue 2257 research, employee map fetch failure
ms.date: 2026-11-22
---

Research disposition: executed. Planning Readiness: Ready.

## Question

Why did 3 of 8 fresh employee sessions show "Map unavailable: Failed to fetch" on the first `/api/map` request (14:56 to 15:00 UTC, revision 0000050), and should the client recover without a reload?

## Evidence

* Client: `fetchReadRetrying` in `src/api/src/zava_forward/api/web/app.js` retries only 500/502/503/504 non-JSON gateway answers. A network-level rejection (`TypeError: Failed to fetch`) is thrown on the first attempt by design (comment and test `test_first_load_reads_retry_a_cold_start_gateway_failure`). The map handler then renders `Map unavailable: <message>`.
* Server: `server.py` serves with `BaseHTTPRequestHandler`, HTTP/1.1, 300 s keep-alive timeout. No per-request timeout shorter than the client's; a client abort is not logged.
* Platform (Log Analytics `ContainerAppSystemLogs`, workspace log-cutover-test, 14:40 to 15:10 UTC): scale-to-zero ended 14:41:16; replica scheduled 14:47:50; scaled to 2 by `http-scaler` 14:49:47; Readiness and Liveness probe timeouts (3 s, 5 s) at 14:49:54, 14:50:01, 14:52:29 to 14:53:59; "Scale down to 1" at 14:56:51 (inside the failure window); further Readiness timeouts 15:01 and 15:02; scale to 2 again at 15:03:10. App has min 0, max 4 replicas, 0.5 CPU, 1 GiB, `http` scaler at 50 concurrent requests, cooldown 300 s.
* Fresh reproduction 2026-11-22 15:51 to 15:54 UTC with Playwright, 8 fresh sign-ins to `/app#/overview`: 8 of 8 loaded 443 markers, no `requestfailed`, `/api/map` 200 each time (4 s then 10 s once a second replica appeared at 15:53:02). Script and result: `docs/reference/research/issue-2257-mapfetch-live-2026-11-22/`. The SQL tier is now S3, so the original slowness is not reproduced.

## Findings

* Cause, supported but not directly proven: replica churn. Probe timeouts and a scale-in at 14:56:51 coincide with the window; a connection reset by a replica leaving the ingress pool surfaces in the browser as `Failed to fetch`, and server logs show nothing because no handler ran. A request-level link (which connection was reset) is not observable from the available logs.
* Defect: an idempotent GET read has no recovery path for a transient transport failure, so one reset needs a manual reload. This is a client defect independent of the exact platform trigger.
* Infra and server timeouts are not changed: no evidence of a server-side timeout shorter than the client, and the owner forbids production changes.

## Planning Readiness

Ready: add a bounded retry of read requests on transport failure to `fetchReadRetrying`, keep aborts and mutations untouched, amend the test that asserted no retry.
