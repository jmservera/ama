---
title: Public Browser Access on the Deployed Demo, Seventh Pass (Issue 344)
description: Read-only live proof of the SQL-private and anonymous-API criteria for issue 344, with the remaining unproven items stated
author: AMA programme
ms.date: 2026-11-19
ms.topic: reference
---

Refs #344. Extends the [sixth pass](public-browser-access-live-r6-2026-11-19.md). Synthetic demo, desktop only; owner decisions of 2026-11-18 apply. Azure use was read-only in resource group `ama`; no resource was created and nothing needs deleting. No credentials were used. No source change was made, so the focused tier applies.

## Live observations (2026-11-19, about 16:12Z)

| Probe | Result |
| --- | --- |
| `GET /healthz` on `ca-cutover-test-demo-api` | 200, no sign-in |
| `GET /welcome.html` | 200, no sign-in |
| Anonymous `GET /api/me` and `/api/time/status` (curl, default and `Accept: application/json`) | 401, no redirect |
| `az sql server show` on `sql-cutover-test-rzsrg` | `publicNetworkAccess` = `Disabled` |
| `az sql server firewall-rule list` | 0 rules |
| `az network private-endpoint list` | `pe-sql-cutover-test-rzsrg` (group `sqlServer`) present |
| `az policy assignment list` (resource group and subscription) | 0 assignments, so no policy exemption or bypass exists to be used |
| `az containerapp auth show` | action `RedirectToLoginPage`; excluded paths `/healthz`, `/readyz`, `/`, `/welcome.html`, `/style.css`, `/zava-logo.png`, `/sign-in` |
| App settings | `ZF_AUTH=trusted-proxy`, `ZF_SQL_AUTH=msi` |

`/readyz` returns 404 on the public host; it is excluded from sign-in but is not served, which does not affect any criterion.

## Per-criterion status

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Landing, Entra sign-in, anonymous protected API 401 | Proven for non-browser clients; browser `fetch` still redirects (r6) | Landing 200 and sign-in proven in r6; curl 401 today. Making browsers get 401 means `Return401` in `infra/modules/containerapps.bicep`, an owner decision, infra change and redeploy (FULL tier) |
| 2 | Edge follows #143 | Ticked | No change |
| 3 | `/healthz` public; anonymous API 401 | Proven | 200 and 401 above |
| 4 | SQL private, public access Disabled, no policy bypass | Proven | `Disabled`, 0 firewall rules, private endpoint, 0 policy assignments |
| 5 | Parity with the MVP matrix | Unproven | `/api/time/status` 500 in r6 is a SQL-path `ProgrammingError`; diagnosing it needs SQL-scope work (FULL tier) and a full parity walk-through is not a code change |
| 6 | Browser sign-in smoke | Ticked | Passed in r6 |

Criteria 3 and 4 can be ticked by the owner or coordinator on this evidence; this pass did not edit the issue. Criterion 1 and 5 remain open and need FULL tier work, so no code was built.
