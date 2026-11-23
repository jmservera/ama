---
title: Issue 344 live research, ninth pass (2026-11-22)
description: Research record for reconciling the remaining acceptance criteria of issue 344 against the deployed demo
ms.date: 2026-11-22
---

Refs #344. Research disposition: executed. Planning Readiness: Ready.

## Scope

* Unticked criteria: 1 (landing, sign-in, 401 not redirect), 3 (`/healthz` and anonymous 401), 4 (SQL private), 5 (parity with the MVP matrix).
* Prior pass: `docs/reference/research/public-browser-access-live-r8-2026-11-21.md`. Open there: browser redirect (criterion 1), no feature-by-feature walk (criterion 5), handoff ageing defect fixed locally but undeployed.
* Constraints: synthetic demo, desktop only, resource group `ama`, read-only Azure use, credentials read at run time only and asserted absent from output, no resource created.

## Evidence (recorded about 23:18Z on 2026-11-22; files in `.copilot-tracking/evidence/2026-11-22/issue-344-live/`)

| Probe | Result |
| --- | --- |
| Azure read-only | Latest revision `ca-cutover-test-demo-api--0000054`; environment `cae-cutover-test-demo` external (`internal` false); Easy Auth `unauthenticatedClientAction` is `RedirectToLoginPage`; excluded paths are `/healthz`, `/readyz`, `/`, `/welcome.html`, `/style.css`, `/zava-logo.png`, `/sign-in` |
| SQL | `sql-cutover-test-rzsrg` `publicNetworkAccess` Disabled, 0 firewall rules; 0 policy assignments in the resource group |
| Anonymous, non-browser client | `/healthz`, `/` and `/welcome.html` 200; `/sign-in` 302 to `/.auth/login/aad`; `/api/me`, `/api/cases`, `/api/time/status`, `/app`, `/index.html`, `/law.html` all 401 (also with `Accept: application/json`) |
| Anonymous, with `X-Requested-With: XMLHttpRequest` | 403 on `/api/me` and `/api/cases` (a denial, no redirect) |
| Anonymous, browser User-Agent | 302 to `login.microsoftonline.com` for `/api/me` even with `Accept: application/json`; `Sec-Fetch-*` and `Origin` headers alone do not change the 401, so the platform keys on the browser User-Agent |
| Playwright anonymous in-page `fetch('/api/me')` | Opaque redirect for default and JSON headers; 403 with `X-Requested-With` |
| Playwright landing page | 200, title "Welcome to Zava Forward", sign-in link `/sign-in` |
| Playwright sign-in | Click reaches `login.microsoftonline.com`; test employee returns to `/app` ("My cases today") |
| Workbench walk, 13 navigation destinations | All render a heading and content (My cases, All cases, Overview, Progress dashboard, Visits, Funding, Finance, Capacity and work orders, Closed cases, Assistant proposals, Time capture, Aftercare concerns, Specialist screens); the only 4xx is `/api/aftercare/form` 403, which `aftercare.js` treats as a role gate |
| Assistant proposals | Renders "Role-owned assistant proposals" 13.4 s after the click; the first-walk screenshot `walk-10.png` shows the previous view still loading, `walk-10-assistants-recheck.png` shows the settled state |
| Deployed web assets vs repository | 27 of 30 top-level web files byte-identical when fetched signed in (the `vendor/` folder was not compared); `welcome.html`, `index.html` and `law.html` differ because the server injects the asset version query and the icon sprite (`__WELCOME_ICONS__` placeholder in the source; the welcome diff was inspected, the other two were not) |
| Previously failing endpoints, signed in | `/api/handoffs/unaccepted` and `.csv` now 200 (the r8 500 is gone, consistent with the ageing fix being deployed; the image digest was not compared to a commit); `/api/time/status` 200; `/api/ai/report` 500; `/api/account/photo` 503; `/api/law` 404 (bare path; r8 saw 503) |

## Findings

* Criterion 1: the 401 reaches clients that are not browsers; a browser User-Agent gets a redirect, which is the Easy Auth `RedirectToLoginPage` setting. "401, not a redirect" for a browser `fetch` needs `Return401` (the `entraBearerOnly` Bicep parameter), which also removes the interactive redirect to sign-in and needs an application-side sign-in hand-off. That is an infrastructure change and an owner decision; no Azure change is authorised.
* Criteria 3 and 4: reproduced and unchanged.
* Criterion 5: the 13-destination walk plus byte-identical assets is stronger than r8, but the MVP is retired, so a complete feature-by-feature comparison is not possible; remaining gaps map to matrix rows already Blocked (#349, #350, #210).

## Planning readiness

Ready. No further probing is needed. The only repository change is the evidence note, index and log entry. No source change is justified (the handoff defect is already deployed; the remaining gaps are infrastructure or Blocked rows), so the tier is the focused tier.
