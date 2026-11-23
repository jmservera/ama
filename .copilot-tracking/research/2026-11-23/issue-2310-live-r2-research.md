# Issue 2310 research, live run 2 (2026-11-23)

Research disposition: reused plus gap analysis. Planning Readiness: Ready.

* Existing evidence: docs/reference/research/issue-2310-anon-401-live-2026-11-23.md and the #1005 test cover GET on three routes.
* Gap: no test pins HEAD, POST, unknown /api paths, text/html-first Accept or a cookie-only browser request; criterion 2 is pinned only to /app to /sign-in, not the chained redirect to Entra.
* Live edge 302 (Easy Auth RedirectToLoginPage) is outside demo authority; recorded as unproven live.
