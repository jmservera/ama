---
title: Public Browser Access on the Deployed Demo (Issue 344)
description: Live curl, Playwright and read-only Azure evidence for public HTTPS access, Entra sign-in, anonymous 401, SQL privacy and src feature reachability on the synthetic demo
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: synthetic demo, desktop only. Live Azure is
authorised in resource group `ama` (cap USD 700, no drills, no Key Vault
rotation, no production change). All Azure calls were read-only and no
resource was created. Credentials were read at run time and never printed; a
literal scan of every evidence file for each credential value found no match.

Target: `ca-cutover-test-demo-api` (revision `ca-cutover-test-demo-api--0000031`)
in environment `cae-cutover-test-demo`, reached directly through its Container
Apps ingress FQDN. Browser: Playwright Chromium, 1366 by 900 desktop, run at
08:29 to 08:31 UTC on 2026-11-18. Evidence files are under
`.copilot-tracking/evidence/2026-11-18/issue-344-live/`.

Cited, not repeated: the Entra callback, `/api/me` role claim, logout and
resident-app results are in
[entra-signin-live-demo-2026-11-18.md](./entra-signin-live-demo-2026-11-18.md)
(#349). Per-feature acceptance is owned by #350. Earlier 2026-10-16 results
for `ca-cutover-test-api` behind Front Door are in the
[evidence pack](../../architecture/cutover-evidence-pack.md#public-browser-restoration-2026-10-16)
and are not re-tested here.

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Public edge choice | External Container Apps environment (`internal` false, public network access Enabled), ingress external, `allowInsecure` false, HTTP returns 301 to HTTPS; no Front Door on the demo | `azure-sql-env.txt`, `azure-config.json`, `anon-curl.txt` |
| Anonymous `/`, `/welcome.html`, `/style.css`, `/zava-logo.png` | 200 over HTTPS; page title "Welcome to Zava Forward / Zava North Homes", with a `/sign-in` action | `anon-curl.txt`, `1-landing-anonymous.png` |
| Anonymous `/healthz` | 200, body `ok`, also 200 from a browser `fetch` | `anon-curl.txt`, `access_proof.json` |
| Security headers on `/` | HSTS, `nosniff`, CSP with `frame-ancestors 'none'` | `anon-curl.txt` |
| Easy Auth | Enabled, `RedirectToLoginPage`; only `/healthz`, `/readyz`, `/`, `/welcome.html`, `/style.css`, `/zava-logo.png` and `/sign-in` are excluded | `azure-config.json` |
| Sign-in action in a real browser | Clicking `/sign-in` ends on `login.microsoftonline.com`; the page was captured while loading | `access_proof.json`, `2-entra-signin-page.png` |
| Completing sign-in with the employee test account | Callback returns to `/app`, title "Zava Forward / Zava North Homes", briefing and filters render (443 permitted open cases in the synthetic summary) | `access_proof.json`, `3-workbench-after-signin.png`; container log shows `sign-in-started` then `workbench-entered` |
| Anonymous protected requests by `curl` (no browser Accept) | `/app`, `/api/me`, `/api/cases`, `/workspace-shell.js`, JSON-Accept `/api/me` each return 401 | `anon-curl.txt` |
| Anonymous protected requests from a browser page | `fetch('/api/me')` returns a redirect (to Entra) for default, JSON and HTML Accept headers | `access_proof.json` |
| `/sign-in` anonymous | 302 to `/.auth/login/aad`, which 302s to the tenant authorize endpoint | `anon-curl.txt` |
| SQL server `sql-cutover-test-rzsrg` | `publicNetworkAccess` Disabled, 0 firewall rules, minimal TLS 1.2, private endpoint `pe-sql-cutover-test-rzsrg` Approved; the app reads it by name with `ZF_SQL_AUTH=msi` | `azure-sql-env.txt` |
| Authenticated web assets | All 11 probed assets (`app.js`, `assistants.js`, `index.html`, `law.html`, `law.js`, `ops.js`, `panels.js`, `timecapture.js`, `chat.js`, Leaflet files) return 200 | `access_proof.json` |
| Authenticated read APIs | 22 of 25 GET routes return 200 (cases, CSV, facets, ranking, stats, map, visits, handoffs, packages, work orders, checklists, finance, funding, retention, briefing, assistants, governance, AI report, audit check, continuity) | `access_proof.json` |
| Authenticated read APIs that did not pass | `/api/law` 503 (law store not configured, known), `/api/account/photo` 503 (token store disabled, known), `/api/time/status` 500 (new, see below) | `access_proof.json` |

## Adverse and unexpected results

* In a browser, anonymous API requests are redirected, not answered with 401.
  Easy Auth chooses the response by client type, so only non-browser clients
  see 401. This is the gap already filed as #350 and it is not a regression of
  this run. Changing it is an infrastructure auth setting and was not
  attempted.
* `/api/time/status` returned 500 for the authenticated employee account. The
  handler calls `app.time.status(u)`; the console log showed no traceback and
  the cause is unproven. Time capture is deliberately gated off on the demo,
  so a status 200 with "switched off" was expected. This is a candidate defect
  for a follow-up issue; no source was changed.
* The Entra screenshot captured the account page while it was still loading,
  so it shows the Zava branded shell without the form. The URL host, not the
  image, is the proof.

## Acceptance criteria

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Public HTTPS landing page; sign-in action starts Entra; protected pages need Entra; anonymous protected API returns 401, not a redirect | Partly proven | Landing 200, sign-in click reaches Entra, `/app` anonymous 401, sign-in completes to the workbench. Browser-originated anonymous API calls are redirected, so the "not a redirect" wording holds only for non-browser clients (#350) |
| 2 | Public edge follows #143, choice and trade-off recorded | Already ticked | Demo uses an external Container Apps environment; Front Door is optional and absent (see the `ca-cutover-test-api` record for the Front Door path) |
| 3 | `/healthz` public; protected API 401 to anonymous API calls | Proven for non-browser clients | `/healthz` 200 anonymous; `/api/me`, `/api/cases` 401 by curl. Same browser caveat as criterion 1 |
| 4 | SQL stays private, public access Disabled, no policy bypass | Proven for the demo server | Public access Disabled, zero firewall rules, approved private endpoint, managed-identity auth. Azure Policy assignments and the `drill114src` database were not inspected, so "no policy bypass" is only shown by the absence of a firewall opening |
| 5 | Parity with the matrix: every MVP user-visible feature reachable, gaps listed and filed | Partly proven | Static assets and 22 read routes return 200 for an authenticated session, which proves reachability and not correct behaviour or data. Write workflows, role-specific views, AI, documents and chat dialogue were not exercised; they stay under #350. New gap: `/api/time/status` 500 (needs filing); `/api/law` and `/api/account/photo` 503 are known |
| 6 | Browser sign-in smoke recorded honestly | Already ticked; refreshed | Passed with the test account on 2026-11-18 (this note and #349) |

## What remains for a real-user deployment

* Real-user tenant registration items are listed in the #349 note and are not
  needed for the demo.
* Decide whether to change Easy Auth so browser-originated API calls return
  401, which needs an owner-approved infrastructure change.
* Investigate and file the `/api/time/status` 500.
* Optional: add Front Door and WAF in front of the demo if the owner wants the
  #143 premium edge rather than direct ingress.
