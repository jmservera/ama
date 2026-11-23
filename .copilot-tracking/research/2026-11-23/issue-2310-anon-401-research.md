# Issue 2310 research (2026-11-23)

Research disposition: executed. Planning Readiness: Ready.

* Code: `do_GET` in `src/api/src/zava_forward/api/server.py` returns 401 for any `/api/` path without a user; pages redirect to `/sign-in`.
* Tests: `ProxyHttpTests.test_anonymous_api_is_401_for_browser_style_requests_and_pages_still_redirect` (from #1005) covers criteria 1 and 2; 90 auth tests pass.
* Live: edge Easy Auth `RedirectToLoginPage` returns 302 for anonymous API fetches before app code runs.
* Canonical evidence: docs/reference/research/issue-2310-anon-401-live-2026-11-23.md
