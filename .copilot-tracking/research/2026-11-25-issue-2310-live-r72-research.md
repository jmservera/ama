---
title: Issue 2310 research, anonymous API 401 on revision 0000072
date: 2026-11-25
---

## Research disposition

Disposition: executed. Planning Readiness: Ready.

## Findings

* Code already returns 401 for anonymous `/api/` requests (`server.py` `do_GET`, `_unsupported_method`, `do_POST`), and redirects pages to `/sign-in`.
* Existing tests in `src/api/tests/test_auth.py` cover browser User-Agent with `Accept: application/json` (three tests, all methods). The 45 tests of `tests.test_auth` pass locally.
* Live revision `ca-cutover-test-demo-api--0000072` (100 percent traffic): anonymous `/api/me` and `/api/cases` with a browser User-Agent and `Accept: application/json` return 302 to login.microsoftonline.com. The same call without a browser User-Agent returns 401 with `WWW-Authenticate`.
* Cause: Container Apps built-in authentication runs before the app with `unauthenticatedClientAction: RedirectToLoginPage`; `excludedPaths` has no `/api/` entries. This is platform configuration, not an application code gap, so no source change is possible.
