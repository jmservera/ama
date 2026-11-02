---
title: Research for issue 691 API 4xx/5xx follow-up
ms.date: 2026-11-02
---

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Live proof (issue 691 latest comment, 2026-11-02): 30 parallel `/vendor/leaflet.js` all 200; mixed API burst 6x200, 12x403, 11x503, 1x500; second run 500 on `/panels.js` and `/api/law/alerts`. Console logs had rolled over.
* 403 sources (`src/api/src/zava_forward/api/server.py`): role denial via `projection.allowed` (for example `/api/assistants`, `/api/chat/regulatory/status`, `/api/law/*`). Expected for the test user's role.
* 503 sources: `/api/account/photo` returns 503 when no `X-MS-TOKEN-AAD-ACCESS-TOKEN` (`core/profile.py own_photo`); `/api/law/alerts` returns 503 `{"status":"unknown","safe_route":...}` when the law store is not loaded. Both carry a plain-language body. `web/app.js loadPhoto` already shows the body and the rest of the workspace works. The law 503 is deliberately fail-closed ("unknown" must not read as an all-clear), so it is kept.
* 500: no code path in `src/api` emits a 500. A 500 can only come from (a) an exception escaping `do_GET`/`do_POST`, where the stdlib drops the connection with no body and the ingress reports an error, or (b) the Container Apps ingress or Easy Auth sidecar. `/panels.js` is served from an in-memory snapshot (`StaticAssets`) after only `provider.authenticate`, so an app-level cause for that URL is unlikely; this points toward ingress or sidecar, but is unproven.
* Local reproduction: an ad hoc burst of 1000 concurrent mixed requests (distinct principals, JSON store and SqlStore; script not retained, so not reproducible from the repository) produced only 200/403/503 as classified above, no 500 and no dropped connection. Concurrency race not reproduced.
* Existing logging: `send_response` logged 5xx method, path and status only; escaped exceptions logged nothing structured.

## Decisions

* Keep 403 and 503 statuses unchanged (behavior-preserving, safety fail-closed).
* Add an escaped-exception guard that answers a plain 500 and logs class, status, path and raising frame (no message, query, headers or tokens).
* Pin classification and a bounded (16 workers, 140 requests) burst check in a focused test.
* Logging trade-off: the stdlib prints the full traceback to stderr for an escaped exception; this is replaced by one `http-error` line with the innermost frame only (no message, no query). No DEBUG traceback is added because exception messages and frame locals can carry tokens or personal data.
