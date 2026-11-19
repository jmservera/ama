---
title: Deployed demo parity proof, live run 3 (issue 350)
description: Third live re-measurement of the ten unticked issue 350 acceptance criteria on the synthetic demo, with per-criterion proven and unproven results, retained raw outputs and four screenshots
ms.date: 2026-11-18
---

Refs #350. Scope: the synthetic demo only, desktop only (1440x900), resource group `ama`. Owner decisions of 2026-11-18 apply: live Azure is authorised (cap USD 700), with no drills, no Key Vault rotation and no production change; Azure billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. Earlier runs: [run 1](deployed-parity-live-2026-11-18.md) and [run 2](deployed-parity-live-r2-2026-11-18.md). This run was taken at 14:04 to 14:10 UTC and keeps its own raw outputs.

## Method and boundaries

* Target: `ca-cutover-test-demo-api`, revision `--0000031` (created 2026-11-17 19:42 UTC), image digest `sha256:5368f4e4...`; resident app `ca-resident-demo`, revision `--0000012`. Both revisions are the same as in run 2, so the deployed code did not change between runs ([raw/04](deployed-parity-live-r3-2026-11-18/raw/04-azure-readonly.txt)).
* Browser: Playwright Chromium. Credentials were read from the owner files at runtime in the scripts; nothing was printed, and the saved sessions in a local session directory were deleted afterwards.
* One staff account (role `Retrofit Programme Manager`) and one resident account exist for the tests. Per-role proof for any other staff role is impossible here.
* Every request was a GET (the sign-in form posts go to Microsoft). No case, consent, upload, finance, release or time entry was written, and no Azure resource was created, so nothing needed deleting. No source file changed.
* Evidence: [deployed-parity-live-r3-2026-11-18/](deployed-parity-live-r3-2026-11-18/) with `raw/`, `screens/` (4 PNG; the 12 other staff screenshots showed personal names, addresses or phone numbers and are not retained) and `scripts/`.

## Result summary

| # | Criterion (short) | Result |
| --- | --- | --- |
| 1 | Anonymous protected API returns 401 for browser requests; page redirect kept | Unproven, failing |
| 2 | Staff prerequisite; every dated feature row and 16 assets through the public app | Partly proven |
| 3 | Representative continuing synthetic baseline | Partly proven |
| 4 | Model deployment, five assistants, workflow-only, durable state, bounded release | Partly proven; release authority human-owned; new suspension blocks release |
| 5 | Approved map provider; map, list, chart, CSV, sensor agreement; accessible alternative | Partly proven |
| 6 | Own-user photo token prerequisites | Unproven; deferred (consent, sign-in edge) |
| 7 | Versioned law store configured and seeded | Unproven; deferred (human-owned data change) |
| 8 | Ledger, document and digest durability; scheduled jobs | Partly proven |
| 9 | Time capture gated with explanation; case work independent | Partly proven; defect reproduced |
| 10 | Per-role workflow, consent, finance, chat, export, law and recovery results | Partly proven; one staff role and one resident |

No criterion is fully proven and none is ticked.

## Changes since run 2

* `/api/continuity` now reports epoch 1 and an active suspension `SUS-1`, scope `all`, kind `release`, reason "Demo probe: negative test", recorded 2026-11-18 11:51 by the staff identity ([raw/14](deployed-parity-live-r3-2026-11-18/raw/14-continuity.txt)). It is not a drill of this run; it came from other work on the same demo after run 2.
* Audit ledger: 1,943 entries, intact (run 2: 1,722). Assistant proposals: 6 (run 2: 5). RAI metrics persisted records: 87 (run 2: 86).
* Closed-case export: `/api/cases.csv?view=closed` returns 537 rows, equal to the completed KPI ([raw/08](deployed-parity-live-r3-2026-11-18/raw/08-agreement.txt)). Run 2 reported 20 rows; that figure is not reproduced and the closed export agrees with the list on this run.
* Unchanged from run 2: anonymous API 302, time status 500, law 503, photo 503, own-queue CSV 133 against list 16.

## 1. Browser-mode 401 versus 302 (unproven, failing)

[raw/01](deployed-parity-live-r3-2026-11-18/raw/01-anonymous-matrix.txt): every protected API path (`/api/cases`, `me`, `staff`, `assistants`, `stats`, `law`, `time/status`, `account/photo`) returns 401 to native curl and 302 to a browser User-Agent with either `Accept: application/json` or `text/html`; `/cases.html` and `/app` return 302 in browser mode (page redirect preserved); `/healthz` and `/` return 200. The Easy Auth action is `RedirectToLoginPage` with seven excluded paths and `tokenStore=false`. Browser sign-in lands on the staff app (screenshot not retained: it showed personal names). The criterion fails: a single platform-wide action cannot give 401 for API paths and a redirect for pages without a trusted platform-principal design (coupled to #349); changing the sign-in edge is outside the owner's demo authorisation.

## 2. Staff prerequisite, dated rows, 16 assets (partly proven)

Proven: signed-in staff session reaches `/app`; 13 navigation routes plus the law viewer rendered ([raw/03](deployed-parity-live-r3-2026-11-18/raw/03-staff-render.txt)) with only three expected failures (time status 500, aftercare form 403, law sources 503); the 16 historical assets all return 200 ([raw/06](deployed-parity-live-r3-2026-11-18/raw/06-assets.txt)). Eight hashes match the repository copy; eight differ because web files changed in `main` after the image was built. No hash match to head is claimed. Unproven: no write or role-specific action was executed; no contractor, assessor, quality or finance-approver account exists; `/api/staff` and the aftercare form return 403 for this role.

## 3. Synthetic baseline (partly proven)

Reads ([raw/02](deployed-parity-live-r3-2026-11-18/raw/02-staff-api-probe.txt), [raw/08](deployed-parity-live-r3-2026-11-18/raw/08-agreement.txt)): 443 open and 537 completed cases (980), 30 visits, 13 finance rows, 167 funding rows, 4 handoffs, ranking snapshot of 443 entries under policy 1.0.0. Unproven: who restored the baseline and under what authorisation is not recorded here; sensor and contractor cases are invisible to this role (`/api/sensors` 403); the ranking policy is not signed off, so no priority is ratified.

## 4. Models, assistants, workflow-only, release (partly proven)

Proven: Foundry account `aif-cutover-test-rzsrg` holds one `Succeeded` deployment `standard` (gpt-4.1-nano 2025-04-14); the app has the AI endpoint and deployment settings; `/api/assistants` lists five assistants and nine registered tasks with `proactive=False`; proposals carry "Operator authority, finite allowance and expiry are required"; `/api/governance` shows `releases=[0]` and three `release_gaps`; RAI metrics show 87 persisted records. Screenshot not retained: it showed personal names. Unproven: a bounded release does not exist and an active `release`-scope suspension now stands, so no live model draft, real-model failure path or task-survives-restart proof was attempted. Release authority is a named human decision; lifting the suspension is a drill-adjacent action and was not done.

## 5. Map provider and agreement (partly proven)

Proven: Overview renders the Leaflet map with 33 OSM tile responses, all 200 ([staff-overview.png](deployed-parity-live-r3-2026-11-18/screens/staff-overview.png)); agreement at 443 across `stats.kpis.open`, stage chart sum, `/api/map` total, shown and items, list `view=all` and CSV `view=all`; closed CSV equals the 537 completed. Unproven: an approved or licensed provider (the demo uses the public OSM standard tile URL, an owner decision); sensor agreement (403); the keyboard list alternative was proven in run 2 and not re-run here. Defect: default own-queue CSV returns 133 rows, the own-queue list and `/api/me` report 16.

## 6. Own-user photo (unproven; deferred)

`/api/account/photo` returns 503 "Microsoft photo access is not available. Sign in again after token-store setup."; `services.photo` is false and `tokenStore=false`. Enabling it needs authorised consent (#116) and changes the sign-in edge, so it was not done.

## 7. Law store (unproven; deferred)

No `ZF_LAW_*` setting exists in the app configuration; `/api/law`, `/api/law/sources` and `/api/law/alerts` return 503, and alerts fail safe with status `unknown` and the human hazard route. The viewer shows the not-loaded state ([staff-law.png](deployed-parity-live-r3-2026-11-18/screens/staff-law.png)). Seeding is a data change with human-owned source, viewer and approval controls (#210, #211, #213).

## 8. Ledger, document, digest durability and jobs (partly proven)

Proven: audit ledger intact at 1,943 entries; continuity history valid; Event Hub namespace `evhns-cutover-test-demo` Active with hub `sensor-readings` (2 partitions); `ca-cutover-test-demo-api` ledger entries grew between runs, which shows durable writes on the SQL store. Unproven: `digests_checked=0` and `/api/ledger/digest` is 403 for this role; uploaded-document durability needs a write; all eight Container App Jobs are `Manual` with no cron, and `job-cutover-test-ledger-verify` last ran on schedule 2026-10-26, then manually on 2026-11-18 (Failed 08:00 and 08:02, Succeeded 08:05), so no scheduled run can be verified now.

## 9. Time capture (partly proven; defect reproduced)

`/api/time/status` returns 500 and the container log shows `http-error GET /api/time/status status=500 exc=ProgrammingError` at 14:06 UTC ([raw/05](deployed-parity-live-r3-2026-11-18/raw/05-time-status-log.txt)); the screen shows "Staff time capture could not load. Owner: application support" instead of the gated explanation (screenshot not retained: it showed a personal name). Case work stays independent: all case, list and overview routes loaded while it failed. Fixing it is a source and SQL change (FULL tier), so it is a follow-up.

## 10. Per-role results (partly proven)

Recorded for the Programme Manager: lists, CSV exports, continuity, ledger check, retention (0 records), data-protection register (owners not recorded, `dpo_reviewed=False`), governance and finance exposure (held, human decision). Resident app: anonymous and signed-in access show the synthetic showcase "Your home improvement progress - synthetic showcase, not live" and `/api/cases` returns 404 there, so the resident surface exposes no staff API ([raw/15](deployed-parity-live-r3-2026-11-18/raw/15-resident.txt), [resident-after-login.png](deployed-parity-live-r3-2026-11-18/screens/resident-after-login.png)). Not recorded: other staff roles, consent and pause flows, privacy and recovery actions, chat dialogue, finance and grant actions, law.

## Follow-ups

* Edge behaviour for anonymous browser API requests, with #349 (criterion 1).
* Fix `/api/time/status` on Azure SQL (criterion 9), FULL tier.
* Explain the own-queue CSV (133) against list (16) difference (criterion 5).
* Human-owned: release authority and the active release suspension, licensed map provider, photo consent, law-store seeding, scheduled-job design, further role accounts.
