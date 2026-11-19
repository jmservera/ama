# Issue 344 live research (2026-11-18)

Scope: unticked criteria of #344 against the synthetic demo (ca-cutover-test-demo-api, resource group ama).
Owner decisions 2026-11-18: demo, desktop only, live Azure read-only authorised, no drills.
Existing evidence cited, not duplicated: docs/reference/research/entra-signin-live-demo-2026-11-18.md (#349); #350 owns per-feature acceptance.

Research disposition: executed. Planning Readiness: Ready.

Findings: see docs/reference/research/public-browser-access-live-demo-2026-11-18.md.
* External Container Apps env, HTTPS only, Easy Auth RedirectToLoginPage with a short excluded-path list.
* Anonymous curl: / 200, /healthz 200, protected paths 401. Browser fetch: redirect (known, #350).
* SQL public access Disabled, 0 firewall rules, private endpoint approved.
* Authenticated: 22 of 25 read routes 200; /api/law 503, /api/account/photo 503 (known), /api/time/status 500 (new).
Evidence: .copilot-tracking/evidence/2026-11-18/issue-344-live/
