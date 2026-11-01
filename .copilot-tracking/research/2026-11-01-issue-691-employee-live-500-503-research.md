# Issue 691 research: employee live 500 on leaflet.js and 503/403 API responses

Date: 2026-11-01. Task slug: `issue-691-employee-live-500-503`. Disposition: executed. Planning Readiness: Ready.

## Evidence gathered

| Check | Result |
| --- | --- |
| Employee app | `ca-cutover-test-demo-api` (rg `ama`), image `zava-forward-api@sha256:7d179115...`, min 0 / max 4 replicas |
| Local repro, `GET`/`HEAD`/`?v=`/css/png under `/vendor/` | All 200, `leaflet.js` 147,552 bytes, no 500 (password provider, in-process server) |
| Static route code (`server.py` do_GET, `static_assets.py`) | Unknown asset gives 404, unauthenticated trusted-proxy gives 302, unprovisioned gives 403. No code path returns 500; `identity.bind`/`link` fail soft |
| Live, unauthenticated `curl` | `/vendor/leaflet.js`, `/app.js`, css, png return 401 with 0 bytes; `/style.css` 200. 401 comes from Container Apps built-in auth (`globalValidation.excludedPaths` lists only healthz, readyz, /, welcome, style.css, logo, sign-in), not from the app |
| `az containerapp logs show --type console` (last 300 lines) | Only start-up and `auth flow: workbench-entered`; no traceback and no stderr. The app writes no request log, so a 5xx from the edge or auth sidecar leaves no app-side trace |
| Log Analytics `log-cutover-test` | Blocked: `NspValidationFailedError` (network perimeter denies this host). Not changed (no config changes authorised) |

## Findings

1. `/vendor/leaflet.js` 500: not reproducible in the app; no application code path produces 500 and no traceback exists. The producing component is unproven while ingress and auth logs are unavailable; Container Apps ingress or the built-in auth layer during a scale-from-zero revision swap is a hypothesis only, and an application failure is not excluded. Cause remains unresolved with evidence above. The app-side gap is that responses are invisible: there is no request or error log line. Fix scoped here: log every >=500 response and every non-200/304 static asset response with method, path and status, plus a regression test that full-length `leaflet.js` is served for GET, HEAD, `?v=`, conditional and concurrent requests.
2. 503 `/api/account/photo`: expected. `profile.own_photo` raises `PhotoError(503)` when `X-MS-TOKEN-AAD-ACCESS-TOKEN` is absent (token store not set up). `loadPhoto` already shows the message; the error was visible only as a browser network line.
3. 503 `/api/law/alerts`: expected when the law store is not loaded (`server.py` "The law store is not loaded.") or rule alerts are unavailable. `chat.js` shows raw server text prefixed "Alert coverage unknown".
4. 403 `/api/assistants` and `/api/chat/regulatory/status`: expected denial for the Application Administrator role (shows every option, acts on none; `assistants.registry` raises "Staff assistance only", `_regulatory_access` denies). `chat.js` still calls both and shows raw text prefixed "unavailable".

## Scope decision

* Add `unavailableNote` plain-language handling in `chat.js` for status 403 and 503.
* Skip the two staff-only calls (`/api/assistants`, `/api/chat/regulatory/status`) for the Application Administrator role so no denial is requested.
* Add >=500 and asset non-success logging in `server.py`.
* Tests outside the package in `src/api/tests/`. No `mvp/` or `prototype/` changes.

## Acceptance criteria mapping

* Criterion 1 (cause identified and fixed with regression test): partially met. Producing component unproven (ingress or auth is a hypothesis, application not excluded); observability fix and regression test added. Not proven fixed.
* Criterion 2: met by classification above plus UI change and tests.
* Criterion 3: live re-check marked pending the next deploy.

## Follow-ups

1. Grant read access to Log Analytics or an approved path, then query ingress and auth sidecar 5xx for `/vendor/leaflet.js` (blocks criterion 1).
2. Consider adding `/vendor/*` ordering check against Easy Auth token refresh during revision swaps.

## Correction cycle 2026-11-01 (PR #694 review threads)

Three Copilot threads read and validated: (1) inherited handler responses (e.g. `OPTIONS /vendor/leaflet.js` 501) bypass `_send`; (2) 403/503 can also mean missing configuration or unexpected failure, so role/disabled wording over-claims; (3) source-order test passes without the administrator guards. All valid.

## Correction cycle 2 2026-11-01 (PR #694, thread on send_response)

Thread valid: malformed or oversized request lines reach `send_response` before `self.path` exists (AttributeError) and a malformed target (`OPTIONS http://[`) makes `urlparse` raise ValueError. Fix must keep error responses working.
