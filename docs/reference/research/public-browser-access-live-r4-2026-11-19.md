---
title: Public Browser Access on the Deployed Demo, Fourth Pass (Issue 344)
description: Fourth live pass for issue 344 that finds criterion 1 unmet for browser clients, explains why the fix needs the full validation tier, and gives a per-criterion proven and unproven table
author: AMA programme
ms.date: 2026-11-19
ms.topic: reference
---

Refs #344. This pass repeats the [first](public-browser-access-live-demo-2026-11-18.md), [second](public-browser-access-live-rerun-2026-11-18.md) and [third](public-browser-access-live-r3-2026-11-18.md) notes with fresh read-only evidence.

## Scope and method

Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure authorised in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change). Target `ca-cutover-test-demo-api`. Azure CLI use was read-only, so no resource was created and nothing needs deleting. No credentials were used; this pass needed no sign-in. Browser proofs of sign-in are unchanged from the earlier passes and were not repeated. Evidence: `.copilot-tracking/evidence/2026-11-19/issue-344-live/`.

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Anonymous curl | `/healthz` 200, `/` 200, `/api/me` 401, `/api/cases` 401, `/app` 401 | `anon-curl.txt` |
| Browser-style anonymous API call | Browser User-Agent with `Accept: application/json` to `/api/me` gets 302 to `login.microsoftonline.com` (tenant id replaced with `<tenant-id>`) | `anon-curl.txt` |
| Easy Auth | `RedirectToLoginPage`; excluded paths `/healthz`, `/readyz`, `/`, `/welcome.html`, `/style.css`, `/zava-logo.png`, `/sign-in` | `auth-globalvalidation.json` |
| SQL `sql-cutover-test-rzsrg` | Public network access Disabled, TLS 1.2, 0 firewall rules | `sql.json`, `sql-fw-count.txt` |

## Why criterion 1 is not fixed here

The 401-for-anonymous-API clause holds for non-browser clients and fails for browser-style requests because the platform action is `RedirectToLoginPage`. `infra/modules/containerapps.bicep` line 302 offers `Return401` only through the opt-in `entraBearerOnly` mode, which drops the client secret and browser sign-in. Satisfying both halves needs either a Bicep change (and a redeploy) or an application-level sign-in flow with the platform action set to `Return401`. Both touch infrastructure, deployment and a security control, so the full validation tier applies and the worker brief requires stopping. No source change was made and no live setting was altered.

## Per-criterion status

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Public landing; sign-in starts Entra; protected pages need Entra; anonymous API 401, not a redirect | Unproven (browser clients) | Landing, Entra start and gating proven earlier; fresh run reproduces the 302 for browser-style API calls |
| 2 | Public edge follows #143 | Already ticked | External Container Apps environment |
| 3 | `/healthz` public; protected API 401 to anonymous | Proven for non-browser clients | Same 302 caveat |
| 4 | SQL private, public access Disabled, no policy bypass | Proven for the demo server | Disabled, 0 rules; zero exemptions from the second pass, not re-run |
| 5 | Parity with the matrix, gaps filed | Unproven | Reachability only; `/api/time/status` 500 defect still unfiled (no shared-system writes) |
| 6 | Browser sign-in smoke recorded | Already ticked | Test account, passed in earlier passes |

No checkbox was changed; the owner ticks.

## Evidence limits

* Sign-in and authenticated reachability were not repeated in this pass.
* Policy exemption count and private endpoint state are carried from the second pass.
