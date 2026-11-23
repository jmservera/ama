---
title: Public Browser Access on the Deployed Demo, Ninth Pass (Issue 344)
description: Live browser walk, anonymous-access cause analysis and read-only Azure checks for issue 344, with a per-criterion table
author: AMA programme
ms.date: 2026-11-22
ms.topic: reference
---

Refs #344. Extends the [eighth pass](public-browser-access-live-r8-2026-11-21.md). Synthetic demo, desktop only; owner decisions of 2026-11-18 apply. Azure use was read-only in resource group `ama`; no resource was created, so nothing needs deleting, and no source or infrastructure file changed. Credentials were read at run time and never printed (each probe asserts they are absent from its output). Evidence is in `.copilot-tracking/evidence/2026-11-22/issue-344-live/` (`probe.py`, `probe_assistants.py`, `probe_gaps.py`, their JSON results and screenshots), recorded about 23:18Z.

## Observations

| Probe | Result |
| --- | --- |
| Azure | Revision `ca-cutover-test-demo-api--0000054`; environment `cae-cutover-test-demo` is external; Easy Auth `unauthenticatedClientAction` is `RedirectToLoginPage`; `/healthz`, `/readyz`, `/`, `/welcome.html`, `/style.css`, `/zava-logo.png` and `/sign-in` are excluded from authentication |
| SQL | `sql-cutover-test-rzsrg` `publicNetworkAccess` Disabled, 0 firewall rules; 0 policy assignments in the resource group |
| Anonymous, non-browser client | `/healthz`, `/`, `/welcome.html` 200; `/sign-in` 302 to `/.auth/login/aad`; `/api/me`, `/api/cases`, `/api/time/status`, `/app`, `/index.html`, `/law.html` 401, also with `Accept: application/json` |
| Anonymous with `X-Requested-With: XMLHttpRequest` | 403 (denied, no redirect) |
| Anonymous with a browser User-Agent | 302 to `login.microsoftonline.com` for `/api/me`, even with `Accept: application/json`; `Sec-Fetch-*` and `Origin` headers alone leave the 401 unchanged, so the platform separates browsers by User-Agent |
| Playwright landing page | 200, "Welcome to Zava Forward", sign-in link `/sign-in` |
| Playwright anonymous `fetch('/api/me')` | Opaque redirect with default or JSON headers; 403 with `X-Requested-With` |
| Playwright sign-in | Reaches `login.microsoftonline.com`; test employee returns to `/app` ("My cases today") |
| Workbench walk | 13 of 13 navigation destinations render a heading and content; the only 4xx is `/api/aftercare/form` 403, a role gate the client handles |
| Assistant proposals | Renders 13.4 s after the click; an earlier 1.2 s wait captured the previous view still loading (`walk-10.png`), and `walk-10-assistants-recheck.png` shows the settled page |
| Web assets | 27 of 30 top-level files byte-identical to the repository when fetched signed in; `welcome.html`, `index.html`, `law.html` differ by server-side injection (the welcome diff was inspected: asset version query and icon sprite); `vendor/` was not compared |
| Eighth-pass failures, signed in | `/api/handoffs/unaccepted` and `.csv` 200 (consistent with the ageing fix being deployed; the digest was not compared with a commit); `/api/ai/report` 500; `/api/account/photo` 503; `/api/law` 404 on the bare path |

The remaining failing paths match rows the [parity matrix](../../architecture/mvp-to-src-parity-matrix.md) already lists as Blocked (#349, #350, #210), so they are filed gaps, not new ones.

## Per-criterion status

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Landing, Entra sign-in, anonymous protected API 401 not redirect | Partly proven | Landing, sign-in and the 401 for non-browser clients are proven. A browser User-Agent still receives a 302, because `RedirectToLoginPage` is set; `Return401` (`entraBearerOnly` in `infra/modules/containerapps.bicep`) would change that but also removes the interactive sign-in redirect, so it needs an owner decision and an infrastructure redeploy that is not authorised here |
| 2 | Edge follows #143 | Ticked | External Container Apps environment (unchanged) |
| 3 | `/healthz` public; anonymous API 401 | Proven | 200 and 401 above, for non-browser clients |
| 4 | SQL private, public Disabled, no policy bypass | Proven | Disabled, 0 firewall rules, 0 policy assignments |
| 5 | Parity with the MVP matrix | Unproven | 13 of 13 workbench destinations render as a single test role (Retrofit Programme Manager) and 27 of 30 web files are byte-identical; the MVP is retired so a full feature-by-feature comparison is not possible, other roles were not walked, and three gaps remain Blocked (#349, #350, #210) |
| 6 | Browser sign-in smoke | Ticked | Passed again (unchanged) |

No issue checkbox was edited.
