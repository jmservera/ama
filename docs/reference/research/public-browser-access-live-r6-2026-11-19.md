---
title: Public Browser Access on the Deployed Demo, Sixth Pass (Issue 344)
description: Live re-check of issue 344 with a diagnosed cause for the time-status 500 and a per-criterion table
author: AMA programme
ms.date: 2026-11-19
ms.topic: reference
---

Refs #344. Extends the [rerun note](public-browser-access-live-rerun-2026-11-18.md). Synthetic demo, desktop only; Azure use was read-only against `ca-cutover-test-demo-api` in resource group `ama`; no resource was created. Credentials were read at run time and never printed (a literal assertion in the probe script checks the output). Evidence: `.copilot-tracking/evidence/2026-11-19/issue-344-live-r6/`.

## Observations

| Observation | Result | Evidence |
| --- | --- | --- |
| Landing page and sign-in | Landing 200; sign-in click reaches `login.microsoftonline.com`; test account returns to `/app` | `time_status_probe.json`, `1-workbench-after-signin.png` |
| Browser-style anonymous `/api/me` | In-page `fetch` with default, JSON and HTML Accept headers all end in a redirect; `/healthz` 200 | `time_status_probe.json` |
| Easy Auth action | `RedirectToLoginPage`; `/healthz`, `/readyz`, `/`, `/welcome.html` and assets excluded | `az containerapp auth show` (read-only) |
| `/api/time/status` | 500 on 3 of 3 calls at 15:53:02Z while `/api/me` is 200 | `time_status_probe.json` |
| Cause of the 500 | App log `exc=ProgrammingError at=exceptions.py:583:raise_exception`, a database driver error on the SQL path, not an Easy Auth or ingress fault | `http-error-logs.txt` |

## Per-criterion status

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Landing, Entra sign-in, anonymous API 401 not redirect | Unproven for browser clients | Redirect reproduced; Return401 is the `entraBearerOnly` setting at `infra/modules/containerapps.bicep` line 302 and would remove the browser redirect to sign-in, so it needs an owner decision, an infra change and a redeploy (FULL tier) |
| 2 | Edge follows #143 | Already ticked | External Container Apps environment |
| 3 | `/healthz` public; anonymous API 401 | Proven for non-browser clients | Earlier curl evidence; same redirect caveat |
| 4 | SQL private, public access Disabled | Proven earlier (rerun note); not re-read in this pass | No change made |
| 5 | Parity, gaps filed | Unproven | Reachability only; the `/api/time/status` 500 is now diagnosed as a SQL-path `ProgrammingError`, and the underlying table or permission fault needs SQL-scope work (FULL tier) before parity can be claimed |
| 6 | Browser sign-in smoke | Already ticked | Passed again with the test account |

No checkbox was changed. Raw driver message is not in the retained log, so the exact SQL fault (missing table versus DDL permission for the time-capture tables) is unconfirmed.
