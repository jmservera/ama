---
title: Deployed demo parity proof, live run 2026-11-18 (issue 350)
description: Per-criterion proven and unproven results for the unticked issue 350 acceptance criteria, measured on the synthetic demo with Playwright and Azure CLI
ms.date: 2026-11-18
---

Refs #350. Scope: the synthetic demo only, desktop only, resource group `ama`. Owner decisions of 2026-11-18 apply: live Azure is authorised, with no drills, no Key Vault rotation and no production change; Azure billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. Sign-in is covered by #349 and is used here only as a means.

## Method and evidence boundaries

* Target: `ca-cutover-test-demo-api` (revision image `zava-forward-api@sha256:5368f4e4...`, `ZF_AUTH=trusted-proxy`, `ZF_DEPLOYMENT_PROFILE=demo`) and `ca-resident-demo`.
* Browser: Playwright Chromium, desktop viewport 1440x900. Session state is written by the scripts to `/tmp/state-*.json` and was not committed. Credentials were read from the owner's files at runtime inside the scripts in [scripts/](deployed-parity-live-2026-11-18/scripts/); no credential, cookie or token is printed or stored in the repository. Session state files were kept outside the repository and deleted.
* Only one staff account was available: a Retrofit Programme Manager (`ZavaForward.ProgrammeManager`). Per-role proof for other roles is therefore not possible here.
* Requests were reads only (GET). No case was edited, no consent recorded, no money or release action taken, nothing created in Azure, so nothing needed deleting.
* Screenshots: [overview](deployed-parity-live-2026-11-18/screens/staff-overview.png), [all cases](deployed-parity-live-2026-11-18/screens/staff-all.png), [time capture](deployed-parity-live-2026-11-18/screens/staff-time.png), [law viewer](deployed-parity-live-2026-11-18/screens/staff-law.png), [resident home](deployed-parity-live-2026-11-18/screens/resident-home.png).

## Findings since the 2026-10-16 audit

The issue text is partly stale. Observed on 2026-11-18:

* The Foundry account `aif-cutover-test-rzsrg` now has one deployment: `standard`, gpt-4.1-nano 2025-04-14, GlobalStandard, capacity 10, provisioning `Succeeded`. The app sets `AI_ENDPOINT`, `AI_DEPLOYMENT` and `AI_DEPLOYMENT_STRONG` to it.
* `ZF_TILE_URL` is explicitly set to the OpenStreetMap standard tile URL with attribution.
* The store is `mssql` with 443 open and 537 completed cases (980 total), not one fictional case.

## Per-criterion result

| # | Criterion (short) | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Anonymous protected API returns 401 for browser-style requests; page redirect kept | Unproven, failing | See below |
| 2 | Tenant/staff prerequisite, all dated rows and 16 assets executed through public app | Partly proven; not complete | See below |
| 3 | Representative continuing synthetic baseline | Partly proven | See below |
| 4 | Model deployment, five assistants, workflow-only and durable state | Partly proven; release authority is human-owned | See below |
| 5 | Approved map provider; map/list/chart/CSV/sensor agreement; accessible alternative | Partly proven | See below |
| 6 | Own-user photo token prerequisites | Not proven; deferred | See below |
| 7 | Versioned law store configured and seeded | Not proven; deferred | See below |
| 8 | Ledger, document, digest durability and scheduled jobs | Partly proven; scheduled jobs failing | See below |
| 9 | Time capture gated with unavailable explanation; case work independent | Partly proven; defect found | See below |
| 10 | Per-role workflow, consent, finance, chat, export, law and recovery results | Partly proven; one role only | See below |

### 1. Browser-mode 401 versus 302 (unproven, failing)

Raw curl, API and container-log output below was not retained in the repository; only the screenshots and scripts are. Anonymous requests to the demo API, 2026-11-18 08:16 UTC (`curl -A ... -H Accept`):

| Path | Native curl | Browser UA, Accept: application/json | Browser UA, Accept: text/html |
| --- | --- | --- | --- |
| `/api/cases`, `/api/me`, `/api/staff`, `/api/assistants` | 401 | 302 to `login.microsoftonline.com` | 302 |
| `/cases.html` | 401 | 302 | 302 |
| `/healthz`, `/` | 200 | 200 | 200 |

The page redirect is preserved, but every anonymous protected API request with a browser User-Agent still receives 302, so the criterion fails. Easy Auth is `unauthenticatedClientAction=RedirectToLoginPage` with excluded paths `/healthz`, `/readyz`, `/`, `/welcome.html`, `/style.css`, `/zava-logo.png`, `/sign-in`. Changing `unauthenticatedClientAction` to `Return401` for `/api/*` is an edge auth configuration change on a shared app; it is not made here (no production changes) and any API exemption requires trusted platform-principal proof. Needs a follow-up decision with #349.

### 2. Tenant/staff prerequisite and rows/assets (partly proven)

Screenshots are retained only for Overview, All cases, Time capture and law; the other screens were observed but not captured. Proven: the staff Entra sign-in lands on `/app` (title "Zava Forward | Zava North Homes"); `/api/me` returns role `Retrofit Programme Manager`, `identity_source=entra`, `auth_provider=trusted-proxy`. Rendered through the browser: My cases, All cases, Overview (heatmap, funnel, map), Progress dashboard, Visits, Funding, Finance, Time capture and the law viewer; each loaded, only Time capture and law showed errors (items 7 and 9).
Unproven: the remaining dated feature rows and the other historical assets (for example `panels.js`, `timecapture.js` rendered in every state) were not individually executed, and no other role account exists. The parity matrix rows stay Blocked for them.

### 3. Synthetic baseline (partly proven)

Authenticated reads of the public deployed app: `/api/stats` gives open 443 and completed 537 (980 total, matching the historical 980-case figure), 22 hazards, 140 support, 26 funding; `/api/visits`, `/api/packages` (`PKG-SYN-001`), `/api/workorders` (`WO-SYN-*`), `/api/finance` (`INV-SYN-001`), `/api/funding`, `/api/handoffs`, `/api/checklists` (QC-LOFT, QC-WALL and others) and `/api/ranking/snapshot` (443 entries, policy hash `b66fdacc...`) return 200 with synthetic data. `/api/retention` returns no records.
Unproven: who restored the baseline and under which authorisation is not recorded; documents, sensors (403 for this role) and contractor cases were not checked; no restoration was performed in this run.

### 4. Model deployment, assistants, workflow-only (partly proven)

Proven: the deployment exists (see above). `/api/assistants` lists five assistants (stock-prioritisation, assessment-preparation, funding-evidence, works-resident-coordination, quality-evidence), each with `release` reason "Release admission denied: no approved release matches ... Owner: RAI task owner not appointed (OQ-017)", `proactive=false`, limits (12000 input chars, 600 output tokens, 20 s timeout, 2 attempts) and a manual route. `/api/ai/report`: evaluation 11 scenarios passed; live tasks briefing 118 total, 0 AI, 118 workflow; message 6/0/6; summary 5/0/5; funding_draft 1/0/1; fallback reasons "AI is not configured" 14, "workflow-only mode selected" 5, release denied 111; `/api/briefing` returns `source=template`, `validated=true`. This proves the workflow-only and failure path with retained tasks. `/api/audit-check` shows an intact ledger of 999 entries.
Unproven, and human-owned: bounded release authority (an approved, unexpired release record and an appointed RAI task owner). No AI call has produced a draft in the demo, so live model output and an AI task surviving restart are not proven. No release was created in this run because release authority is a named human decision.

### 5. Map provider and agreement (partly proven)

Proven: the Overview screen renders a Leaflet map with 33 OSM tile requests, all 200, with attribution, and a keyboard/screen-reader list alternative ("Show the map areas as a list"). Counts agree: `/api/stats` open 443, `/api/map` total 443 (cap 500, all shown), `/api/cases?view=all` total 443, `/api/cases.csv?view=all` 443 unique references.
Unproven: an approved/licensed provider (the demo uses the public OpenStreetMap standard tiles, whose usage policy does not suit production reliance; selecting a licensed provider is an owner decision and is deferred); sensor agreement (`/api/sensors` is 403 for the Programme Manager role); chart agreement beyond the totals. One open observation: `/api/cases.csv` with the default `view=mine` returns 133 rows while the My cases list total is 16; the cause (CSV mine scope versus open-only list) was not determined.

### 6. Own-user photo (not proven; deferred)

`/api/account/photo` returns 503 "Microsoft photo access is not available. Sign in again after token-store setup." and `/api/me` reports `services.photo=false`. Enabling the delegated token store needs authorised consent (#116); deferred as a consent item, not a demo defect.

### 7. Law store (not proven; deferred)

`/api/law` returns 503 "The law store is not loaded." and the law viewer's `/api/law/sources` is 503 (screenshot). Seeding the store through the approved SQL/Blob path is a production data change, and viewer, source and approval controls are human-owned (#210, #211, #213). Deferred.

### 8. Durability and scheduled jobs (partly proven)

Proven: the ledger is intact (999 entries, no problem); `/api/continuity` is healthy (epoch 0, history valid, no suspensions); data persists in SQL (`ZF_STORE=mssql`) and documents use `azure-blob`. The Event Hub namespace `evhns-cutover-test-demo` is `Succeeded`.
Unproven: `digests_checked` is 0, so digest durability is not shown; document upload/download durability was not exercised (a write); all nine Container App Jobs in `ama` have trigger type `Manual` with no cron schedule, so no scheduled job exists to verify. `job-cutover-test-ledger-verify` shows Failed runs at 08:00 and 08:02 UTC and a success at 08:05 UTC on 2026-11-18; these belong to other concurrent work and were not triggered or diagnosed here.

### 9. Time capture (partly proven; defect found)

`/api/time/status` returns 500 for the staff user; container log: `http-error GET /api/time/status status=500 exc=ProgrammingError` (a SQL error, likely a missing time table or column in the demo database). The screen shows "Staff time capture could not load. Owner: application support. Next action: refresh to try again" instead of the gated "not enabled until approvals" explanation the criterion expects. Case work is independent: all other screens loaded at the same time. The gated explanation is therefore not proven; the defect needs a source or schema follow-up (SQL, so it takes the FULL tier) and was not fixed here.

### 10. Per-role results (partly proven)

Recorded for the Programme Manager only: workflow lists (handoffs, packages, work orders, finance, funding), export (CSV above), chat (`/api/chat/threads` returns one owned thread, 2 messages), recovery/continuity, ledger. Not recorded: other roles, consent flows, resident-side results (the resident demo app answers `/` with the synthetic-showcase sign-in page and has no staff API), privacy and law. No route redirect or file existence is counted as a pass.

## Open follow-ups

* Decide the edge behaviour for anonymous browser API requests (item 1) with #349.
* Fix `/api/time/status` ProgrammingError and the unavailable explanation (item 9), FULL tier.
* Explain the CSV `view=mine` 133 versus list 16 difference (item 5).
* Human-owned and deferred: release authority (OQ-017), licensed map provider, photo consent, law-store seeding, scheduled jobs design.
