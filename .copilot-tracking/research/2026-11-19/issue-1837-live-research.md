# Issue 1837 live research, 2026-11-19

Base `399e2c011`. Prior record: `docs/reference/research/issue-1837-live-demo-evidence-2026-11-18.md`.

## Findings so far

* Transport defect repaired on main by #1878 (JSON post plus `X-ZF-CSRF`). Regression tests exist in `src/api/tests/test_nomination_api_routes.py`.
* Criterion 4 (browser journeys with axe, no unexpected result) is the first unmet one: the standalone page has no stylesheet, so axe `target-size` (WCAG 2.5.8) fails on summaries, inputs and buttons. The checker `src/api/checks/nomination_route_forms_browser_check.py` records but does not assert it.
* Planned fix: link the existing `/style.css` (allowed by CSP `default-src 'self'`; served unauthenticated by the trusted-proxy allowlist) from the standalone page and make the checker assert zero target-size violations.
* Live: `/nomination-routes.js` on `ca-cutover-test-demo-api` returned HTTP 401 for an unauthenticated probe on 2026-11-19; the deployed image predates the script per the 2026-11-18 record. Redeploy is a production change and out of scope.
