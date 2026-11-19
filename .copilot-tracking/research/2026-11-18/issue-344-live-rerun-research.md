# Issue 344 live rerun: research (2026-11-18, opened 11:30 UTC)

Refs #344. Task slug `issue-344-live` (second pass, artifacts suffixed `-rerun`; the first pass, merged as #1919, is preserved unchanged).

Research disposition: executed (fresh live checks) plus reused (first-pass note `docs/reference/research/public-browser-access-live-demo-2026-11-18.md`, #349, #350, #360 notes).

Planned probes (all read-only against `ama`, desktop, demo):
* anonymous curl and browser-context fetch against `ca-cutover-test-demo-api`
* Playwright landing, sign-in click, Entra sign-in with the test account, protected page entry, authenticated GET probes
* SQL server public access, firewall, private endpoint, Azure Policy assignments and compliance for the server (the first-pass gap)
* `/api/time/status` 500 recheck and cause from container logs
* Planning readiness: Ready.

## Findings (evidence in `.copilot-tracking/evidence/2026-11-18/issue-344-live-rerun/`)

* Anonymous curl: `/healthz`, `/`, `/welcome.html` 200; `/api/me`, `/api/cases`, `/app`, `/workspace-shell.js` 401; HTTP 301 to HTTPS. A request with a browser User-Agent and `Accept: application/json` gets 302 to Entra (platform Easy Auth behaviour, unchanged from #350).
* Playwright: landing 200 titled "Welcome to Zava Forward"; sign-in click reaches `login.microsoftonline.com`; test-account sign-in returns to `/app` titled "Zava Forward"; anonymous in-page fetches of `/api/me` redirect, `/healthz` 200.
* Authenticated GET probes: 11 of 11 static assets 200; 22 of 25 API routes 200; `/api/law` and `/api/account/photo` 503 (known), `/api/time/status` 500 (same unexpected-error body, reproduced; container console log shows no matching lines).
* SQL `sql-cutover-test-rzsrg`: public network access Disabled, 0 firewall rules, one private endpoint connection `Approved`, minimum TLS 1.2.
* Policy (new versus first pass): no policy exemptions at subscription or resource-group scope (0 and 0), none can bypass; no resource-group assignments; subscription assignments are audit-only (`MCAPSGovAuditPolicies` SQL auditing and threat detection `NonCompliant`, audit effect, not a deny bypass).
* Planning readiness: Ready.
