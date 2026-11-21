---
title: Role Sign-in and Wrong-role Denial on the Demo (Issue 2204)
description: Live Playwright proof of the Programme Manager sign-in, its permitted views and two wrong-role denials on the demo workbench, a local per-role matrix for every other role and the administrator, and a per-criterion proven and unproven table
author: AMA programme
ms.date: 2026-11-21
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: this is the synthetic demo, desktop only. Live Azure is
authorised (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no
production change). Billing reconciliation, DPO and Legal approval and person-run
assistive-technology testing are not needed for the demo. The live checks were read-only
against `ca-cutover-test-demo-api`; nothing was created or changed in Azure, so nothing needed
deleting. Credentials were read from the owner's files at run time and never printed. A
literal scan of every retained evidence file for each credential value found no match
(observed; the raw scan output is not retained).

Browser: Playwright Chromium, 1366 by 900, 2026-11-21 between 21:25 and 21:30 UTC.
Evidence: `.copilot-tracking/evidence/2026-11-21/issue-2204-live/` (scripts, JSON, two
screenshots with the account chip hidden and no case data).

## Live results: Retrofit Programme Manager

The one available Entra employee account carries the app role `ZavaForward.ProgrammeManager`
(`live-role-probe.json`).

| Check | Result |
| --- | --- |
| Anonymous `/api/me` in the browser | Redirect to `login.microsoftonline.com` |
| Entra sign-in | Callback to the app origin; `/api/me` 200, role `Retrofit Programme Manager`, `app_admin` false, `view_only` false, `identity_source` `entra` |
| Navigation offered | 13 entries (My cases to Specialist screens); no Simulator control entry and no per-entry "needs a role" flags, which only an administrator sees |
| Permitted data routes | `/api/cases`, `/api/stats`, `/api/finance`, `/api/packages`, `/api/funding`, `/api/audit-check`, `/api/retention` each 200 |
| Wrong-role denial 1 (API) | `GET /api/admin/simulator-control` 403, body code `ADMIN_REQUIRED`, "Only an application administrator can use simulator run control." |
| Wrong-role denial 2 (browser) | `/app#/simulator` renders the plain denial with "Nothing was changed" and the manual route; `live-02-denied-simulator.png` |
| Wrong-role denial 3 (browser) | `/app#/role/repairs` renders "Screen unavailable: This screen is not installed for your signed-in role"; `live-03-denied-repairs-role-screen.png` |
| Unknown route | `/api/no-such-route` 403 (default deny) |

An earlier probe used the wrong path `/api/finance/queue`, which is not a route and
returned the default-deny 403; it is kept as `attempt2-wrong-routes.json` and is not a
finding. Two live attempts failed before the retained run (`ERR_NETWORK_CHANGED` and a
sign-in redirect timeout; `attempt1-*.err`, `attempt4-*.err`); the next attempt passed with
no change to the script's logic.

## Local per-role matrix (not a live sign-in)

`local_role_matrix.py` starts the real HTTP server with the real `TrustedProxyProvider` on
synthetic fictional data and sends a synthetic `X-MS-CLIENT-PRINCIPAL` header for each
role (`local-role-matrix.json`). No credential or Entra account is involved, so this proves
the application's role logic, not Entra sign-in or role assignment.

| Principal | `/api/me` | Navigation entries | Data routes |
| --- | --- | --- | --- |
| Retrofit Coordinator, Resident Liaison Officer | 200 | 10 | finance 403; cases, stats, packages, funding, work orders, audit check 200 |
| Building Safety Liaison, Quality Inspector | 200 | 9 | finance 403; the rest 200 |
| Grants and Evidence Officer | 200 | 10 | all 200 |
| Retrofit Programme Manager, Programme Support Officer | 200 | 13 | all 200 |
| Contractor (roster company bound) | 200 | 2 (My jobs, Specialist screens) | cases and work orders 200; stats, finance, packages, funding, audit check 403 |
| Application Administrator alone | 200 | 14, every one flagged "needs a role with this authority" | every business route 403; simulator control 200 |
| Administrator plus Coordinator | 200, role Coordinator | 14, 3 flagged | data follows the Coordinator; finance 403; simulator control 200 |
| Contractor claim without a roster company binding | 401 | none | none |
| Contractor plus administrator, two staff roles, unmapped role, no role claim, no header | 401 each | none | none |
| Every non-administrator role | | | simulator control 403 |

"Admin sees all" therefore means the administrator sees every navigation option, each
marked as unavailable without a role that carries the authority, while the server returns no
case, resident, finance or export data and permits no action. That is the designed
boundary in `src/api/src/zava_forward/api/workbench.py` (docstring) and
`projection.allowed`, and it matches the existing test
`test_entra_authoritative.py::test_admin_alone_enters_and_sees_every_option_but_reads_no_business_data`.
The targeted suites `test_entra_authoritative`, `test_auth`, `test_role_matrix`,
`test_role_screens` and `test_employee_identity_check` pass on this branch (108 tests).

No defect was found, so no source change was made and the focused validation tier applies.

## Why the other live roles cannot be shown

`az ad app list` returns "Insufficient privileges to complete the operation" with the existing
login, as in [issue 349](./entra-signin-live-demo-2026-11-18.md) and
[issue 116 round 2](./issue-116-live-r2-evidence-2026-11-18.md). Without directory rights no second staff
user, group or app-role assignment can be created, and the resident test account is
federated to a host that does not resolve, so it cannot sign in to Entra. The seven other
staff roles, the contractor and the administrator therefore have no live Entra sign-in for
the demo.

## Acceptance criteria

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Each role signs in and sees only its permitted views; admin sees all | Partly proven; stays unticked | Live: the Programme Manager signs in and sees 13 permitted views with data routes 200 and admin-only routes 403. Local, application layer only: all eight staff roles, the contractor, the administrator alone and the administrator with a staff role, with the matrix above. Unproven live: the other seven staff roles and the administrator, because no accounts or directory rights exist |
| 2 | One wrong-role denial shown; no credentials printed or stored | Proven | Programme Manager refused the administrator-only simulator control through the API (403 `ADMIN_REQUIRED`) and the browser, plus the repairs role screen. Credential literal scan of the evidence folder: no match. Screenshots hide the account chip |
| 3 | Evidence recorded | Proven | This note and the evidence folder |

Criterion 1 can be ticked for the demo only if the owner accepts the live Programme Manager
proof plus the local matrix. A live administrator and a second live role need a tenant
owner to assign app roles to demo accounts, which the owner has not authorised.

## Recommended follow-ups

* Assign `ZavaForward.ApplicationAdmin` and one non-Programme-Manager role to demo accounts (tenant owner action), then rerun `live_role_probe.py` per account.
* Give hash routes distinct document titles (WCAG 2.4.2, from issue 151 round 3).
