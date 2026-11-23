---
title: Public Browser Access on the Deployed Demo, Tenth Pass (Issue 344)
description: Rerun of the live browser and read-only Azure checks for issue 344 against API revision 0000054 and resident revision 0000026, with a per-criterion table
author: AMA programme
ms.date: 2026-11-23
ms.topic: reference
---

Refs #344. Extends the [ninth pass](public-browser-access-live-r9-2026-11-22.md). Synthetic demo, desktop only; owner decisions of 2026-11-18 apply. Azure use was read-only in resource group `ama`; no resource was created, so nothing needs deleting, and no source or infrastructure file changed (`src/` and `infra/` are identical between the ninth-pass base and `main` at `ed9500a188`). Credentials were read at run time and never printed. Evidence is in `.copilot-tracking/evidence/2026-11-23/issue-344-live/` (`probe.py`, `probe_assistants.py`, `probe_gaps.py`, JSON results and screenshots), recorded about 00:56Z.

## Observations

| Probe | Result |
| --- | --- |
| Revisions | `ca-cutover-test-demo-api--0000054` and `ca-resident-demo--0000026` are active with 100 percent traffic |
| Edge | Environment `cae-cutover-test-demo` has `vnetConfiguration.internal` false (external); Easy Auth `unauthenticatedClientAction` is `RedirectToLoginPage`; `/healthz`, `/readyz`, `/`, `/welcome.html`, `/style.css`, `/zava-logo.png` and `/sign-in` are excluded from authentication |
| SQL | `sql-cutover-test-rzsrg` `publicNetworkAccess` Disabled, 0 firewall rules; 0 policy assignments in the resource group |
| Anonymous, non-browser client | `/healthz`, `/`, `/welcome.html` 200; `/readyz` 404; `/sign-in` 302 to `/.auth/login/aad`; `/api/me`, `/api/cases`, `/api/time/status`, `/app`, `/index.html`, `/law.html` 401, also with `Accept: application/json` |
| Anonymous with `X-Requested-With: XMLHttpRequest` | 403, no redirect |
| Playwright landing page | 200, "Welcome to Zava Forward | Zava North Homes", sign-in link `/sign-in` |
| Playwright anonymous `fetch('/api/me')` | Opaque redirect with default or JSON headers; 403 with `X-Requested-With` |
| Playwright sign-in | Reaches `login.microsoftonline.com`; the test employee returns to `/app` ("My cases today"). The first attempt of this pass timed out waiting for the return redirect and the immediate rerun passed, so the sign-in is not fully deterministic under automation |
| Workbench walk | 13 of 13 navigation destinations render a heading and content; the only 4xx are `/api/aftercare/form` 403 (role gate) and one `/api/me` 403 on the signed-out XHR probe |
| Web assets | Same set matches the repository byte for byte when signed in; `index.html` and `law.html` differ by server-side injection, as in the ninth pass |
| Signed-in gaps | `/api/handoffs/unaccepted` and `.csv`, `/api/time/status`, `/api/handoffs`, `/api/handoffs/unowned`, `/api/assistants/proposals` 200; `/api/ai/report` 500; `/api/account/photo` 503; `/api/law` 404 (bare path) |
| Assistant proposals | Rendered after 8.0 s with the heading "Role-owned assistant proposals" and no HTTP error |

The 500 on `/api/ai/report` has no recoverable server cause for this pass: the environment has no Log Analytics workspace configured, and the console log stream held only connection lines. The route code (`src/api/src/zava_forward/api/server.py`) raises only `ValueError` to a 400, so the cause is outside the handled path and could not be isolated without server logs. The parity matrix already lists AI review rows as Blocked, so this is a filed gap, not a new one.

## Per-criterion status

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Landing, Entra sign-in, anonymous protected API 401 not redirect | Partly proven | Landing, sign-in and the 401 for non-browser clients are reproduced. A browser User-Agent still gets a 302 because `RedirectToLoginPage` is set; changing it to `Return401` also removes the interactive sign-in redirect, so it needs an owner decision and an infrastructure redeploy that is not authorised here |
| 2 | Edge follows #143 | Ticked | External Container Apps environment, unchanged |
| 3 | `/healthz` public; anonymous API 401 | Proven | 200 and 401 above, for non-browser clients |
| 4 | SQL private, public Disabled, no policy bypass | Proven | Disabled, 0 firewall rules, 0 policy assignments |
| 5 | Parity with the MVP matrix | Unproven | 13 of 13 destinations render for one role (Retrofit Programme Manager); the MVP is retired, so a feature-by-feature comparison is not possible; other roles were not walked; Blocked rows remain (#349, #350, #210) |
| 6 | Browser sign-in smoke | Ticked | Passed again, with one automation timeout recorded above |

No issue checkbox was edited.
