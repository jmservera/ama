# Changes: issue 2310 (docs and evidence only, no src edits)

Tier: focused. No source or test change, because the requested tests already exist in src/api/tests/test_auth.py and pass.

Files: docs/reference/research/2026-11-25-issue-2310-anonymous-api-401-proof.md, docs/reference/README.md, docs/reference/log.md, dated RPI artifacts.

Validation: `python3 -m unittest test_auth` in src/api, 45 tests OK. Live curl probe of ca-cutover-test-demo-api, no Azure change.

| Criterion | Status | Evidence |
| --- | --- | --- |
| Test: anonymous API GET, browser UA, Accept JSON returns 401 | Proven (local test, already existing) | test_anonymous_api_is_401_for_browser_style_requests_and_pages_still_redirect; passes |
| Same behaviour on the live demo | Unproven, contradicted | Live GET /api/me and /api/cases return 302 to Entra: platform RedirectToLoginPage; not changed (no production changes) |
| Test: anonymous protected page redirects to Entra | Proven locally (302 to /sign-in, then /.auth/login/aad) and live (/app 302 to login.microsoftonline.com) | same test; curl |
| Existing auth tests pass, no weakened protection | Proven | 45 tests OK; no route code changed |
