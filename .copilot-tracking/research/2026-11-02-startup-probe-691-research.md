---
title: Startup and readiness probe research for issue 691
description: Evidence for cold-start 5xx bursts on the employee container app
ms.date: 2026-11-02
---

## Research disposition: executed. Planning Readiness: Ready

## Evidence

* Issue #691 latest comment: Easy Auth middleware logged `Failed to forward request to http://127.0.0.1:8088` within 1-15 ms in bursts at redeploy/cold start (2026-11-01 18:15, 20:35, 20:37, 23:18 UTC). Hypothesis (unproven app-side): requests reach the sidecar before the app listens.
* `infra/modules/containerapps.bicep` api app already had Startup/Liveness/Readiness probes on `/healthz`:8088 but with platform defaults for timeout, delay and readiness period; `minReplicas` is `apiMinReplicas` (default 0, scale from zero).
* `infra/resident-demo.bicep` (the resident container app, port 8089) had no probes. Its `/healthz` runs after a host-allow check, so a probe without a `Host` header would get 403.
* `/healthz` (employee `server.py`) returns 503 when the store is not ready, so it is a real readiness signal; it is excluded from Easy Auth.
* Client: `retryWorkspaceScript` retried vendor scripts only twice (250/500 ms); `api()` GETs and `loadPhoto` did not retry a gateway 5xx.

## Decisions

* Keep `apiMinReplicas` default 0 (cost decision belongs to the owner); mention as follow-up.
* Explicit probe timings in Bicep for both apps; Host header for resident demo.
* Client: bounded read retry (500/1500/3000 ms) for 502/503/504 and non-JSON 500 only; plain-language status; script retry extended to 3 attempts.

## Unproven

* App-side correlation and live re-check; no deploy in this task.
