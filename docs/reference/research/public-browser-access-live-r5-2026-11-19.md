---
title: Public Browser Access on the Deployed Demo, Fifth Pass (Issue 344)
description: Fifth live pass for issue 344 with fresh read-only probes; no remaining criterion is buildable at the focused tier, with a per-criterion table
author: AMA programme
ms.date: 2026-11-19
ms.topic: reference
---

Refs #344. This pass follows the [fourth note](public-browser-access-live-r4-2026-11-19.md) and reruns the probes against `ca-cutover-test-demo-api` under the owner decisions of 2026-11-18 (synthetic demo, desktop only, resource group `ama`). Azure use was read-only, no resource was created and no credential was used. Evidence: `.copilot-tracking/evidence/2026-11-19/issue-344-live-r2/`.

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Anonymous curl | `/healthz` 200, `/` 200, `/api/me` 401, `/api/cases` 401, `/app` 401 | `anon-curl.txt` |
| Browser-style anonymous API call | Browser User-Agent with `Accept: application/json` to `/api/me` gets 302 to `login.microsoftonline.com` (tenant id redacted) | `anon-curl.txt` |
| SQL `sql-cutover-test-rzsrg` | Public network access Disabled, TLS 1.2, 0 firewall rules | `sql.json`, `sql-fw-count.txt` |

The Easy Auth action is read from `infra/modules/containerapps.bicep` (`RedirectToLoginPage` unless `entraBearerOnly`); the live `az containerapp auth show` returned no output this pass, so the live value is not independently re-captured here.

## Decision

No criterion can be built or proven further at the focused tier. The one open clause, anonymous API 401 instead of a redirect for browser-style clients, needs a change to the Easy Auth security control and a redeploy (full tier, production-affecting), and an app-level workaround cannot work because Easy Auth answers before the application sees the request. Criterion 5 remains reachability only and the `/api/time/status` 500 is still unfiled.

## Per-criterion status

| # | Criterion | Status for the demo |
| --- | --- | --- |
| 1 | Public landing, Entra sign-in, anonymous API 401 not a redirect | Unproven for browser clients |
| 2 | Public edge follows #143 | Already ticked |
| 3 | `/healthz` public; anonymous protected API 401 | Proven for non-browser clients |
| 4 | SQL private, public access Disabled | Proven for the demo server |
| 5 | Parity with the matrix, gaps filed | Unproven |
| 6 | Browser sign-in smoke recorded | Already ticked |

No checkbox was changed; the owner ticks.
