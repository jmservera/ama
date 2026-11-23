# Issue 2310 research, live run 3 (2026-11-23)

Disposition: executed. Planning Readiness: Ready. Earlier runs covered GET, HEAD and POST (r2), the live edge 302 (docs/reference/research/issue-2310-anon-401-live-2026-11-23.md) and, on another branch, the unreadable-body POST. New angle: other HTTP verbs.

## Evidence

* `make_handler` in src/api/src/zava_forward/api/server.py defines only `do_GET`, `do_HEAD` and `do_POST`.
* Probe (in-process server, trusted-proxy provider, no credentials): anonymous PUT, PATCH, DELETE and OPTIONS on `/api/cases` with `Accept: application/json` return 501 (stdlib default), not 401. Criterion 1 says every anonymous protected API request returns 401, so these verbs are a gap (no redirect, but an unauthenticated caller learns nothing about auth state and the Entra-expiry handling in the client expects 401).
* Live deployment: Easy Auth edge answers 302 before the app for all verbs (earlier run); not re-probed, owner decision outstanding. Resident site returns 404 for workbench routes.

## Candidate

Add `do_PUT`, `do_PATCH`, `do_DELETE` that return 401 JSON for anonymous `/api/` requests and otherwise keep the existing 501 behaviour. OPTIONS is left alone (no CORS surface; not a mutation verb).

## Unticked criteria

All three: see the changes record table. Live proof of criterion 1 is not possible without an owner-approved edge change.
