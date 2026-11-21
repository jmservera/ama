---
title: Public Browser Access on the Deployed Demo, Eighth Pass (Issue 344)
description: Live browser sign-in and endpoint sweep for issue 344, one real defect fixed locally, with a per-criterion table
author: AMA programme
ms.date: 2026-11-21
ms.topic: reference
---

Refs #344. Extends the [seventh pass](public-browser-access-live-r7-2026-11-19.md). Synthetic demo, desktop only; owner decisions of 2026-11-18 apply. Azure use was read-only in resource group `ama`; no resource was created and nothing needs deleting. Credentials were read at run time and never printed (the probe asserts they are absent from its output). Evidence is in `.copilot-tracking/evidence/2026-11-21/issue-344-live/` (`probe.py`, `time_status_probe.json`, `handoff_probe.json`), recorded about 15:25Z.

## Observations

| Probe | Result |
| --- | --- |
| Anonymous curl: `/healthz`, `/welcome.html` | 200 |
| Anonymous curl: `/api/me`, `/api/time/status`, `/app` (default and JSON Accept) | 401, no redirect |
| Anonymous curl `/sign-in` | 302 to `/.auth/login/aad` |
| Playwright landing page | 200, title "Welcome to Zava Forward" |
| Playwright sign-in click | Reaches `login.microsoftonline.com`; test account returns to `/app` ("My cases today") |
| In-page anonymous `fetch('/api/me')` (default, JSON, HTML Accept) | Redirect (Easy Auth `RedirectToLoginPage`), unchanged since r6 |
| SQL server | `publicNetworkAccess` Disabled, 0 firewall rules, 0 policy assignments |
| `/api/time/status` signed in | 200 (the r6 500 is gone) |
| Signed-in sweep, 11 web assets and 25 API paths | All 200 except `/api/ai/report` 500, `/api/law` 503, `/api/account/photo` 503 |
| `/api/handoffs/unaccepted` and `.csv` | 500 (defect below) |

The 503 and `/api/ai/report` results match rows the [parity matrix](../../architecture/mvp-to-src-parity-matrix.md) already lists as Blocked (law-store settings, delegated token store, release authority; #349, #350, #210), so they are filed gaps, not new ones.

## Defect found and fixed locally

Deployed handoffs carry a naive `offered_at` (for example `2026-10-13T09:00`). `handoff_ageing` rejects it with `ValueError`, which escaped `Store.unaccepted_handoffs` and returned 500 for every staff caller (log: `ValueError at=workflows.py:393:handoff_ageing`). The fix skips a handoff that cannot be aged; it stays listed in `/api/handoffs` and `/api/handoffs/unowned`. Treating the naive time as UTC was rejected because it would invent an instant. A regression test runs on the JSON and SQL stores; it fails without the fix (2 errors) and passes with it. The fix is a local commit and is not deployed, so the live endpoint stays 500 until a rollout.

## Per-criterion status

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Landing, Entra sign-in, anonymous protected API 401 not redirect | Partly proven | Landing, sign-in and curl 401 proven. A browser `fetch` is still redirected; `Return401` is `entraBearerOnly` in `infra/modules/containerapps.bicep` and removes the browser redirect to sign-in, so it needs an owner decision and an infra redeploy |
| 2 | Edge follows #143 | Ticked | External Container Apps environment |
| 3 | `/healthz` public; anonymous API 401 | Proven | 200 and 401 above |
| 4 | SQL private, public Disabled, no policy bypass | Proven | Disabled, 0 firewall rules, 0 policy assignments |
| 5 | Parity with the MVP matrix | Unproven | 33 of 36 swept paths return 200 signed in; the other three are Blocked matrix rows (#349, #350, #210), and one further defect is fixed locally but not deployed; a feature-by-feature walk-through was not performed |
| 6 | Browser sign-in smoke | Ticked | Passed again |

No issue checkbox was edited.
