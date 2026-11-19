---
title: Deployed demo parity proof, live run 2 (issue 350)
description: Re-measurement of the ten unticked issue 350 acceptance criteria on the synthetic demo, with retained raw outputs, screenshots and scripts
ms.date: 2026-11-18
---

Refs #350. Scope: the synthetic demo only, desktop only (1440x900), resource group `ama`. Owner decisions of 2026-11-18 apply: live Azure is authorised (cap USD 700), with no drills, no Key Vault rotation and no production change; Azure billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. Run 1 is [deployed-parity-live-2026-11-18.md](deployed-parity-live-2026-11-18.md); this run repeats it at 11:37 to 11:50 UTC and keeps the raw outputs that run 1 did not retain.

## Method and evidence boundaries

* Target: `ca-cutover-test-demo-api`, revision `ca-cutover-test-demo-api--0000031` (created 2026-11-17 19:42 UTC), image `zava-forward-api@sha256:5368f4e4...`, `ZF_AUTH=trusted-proxy`, `ZF_DEPLOYMENT_PROFILE=demo`, `ZF_STORE=mssql`. Redacted settings: [raw/00-app-config.txt](deployed-parity-live-r2-2026-11-18/raw/00-app-config.txt). Secret-bearing values are shown as `<set>`.
* Browser: Playwright Chromium. Credentials were read from the owner files at runtime inside [login.py](deployed-parity-live-r2-2026-11-18/scripts/login.py); nothing was printed, and the saved session files in `/tmp` were deleted at the end.
* One staff account exists for the tests: role `Retrofit Programme Manager`, identity source Entra through the trusted proxy. The `/api/me` staff list shows four staff, three Programme Managers and one Building Safety Liaison, but only the one account could sign in. Per-role proof for any other role is therefore impossible here.
* Every request was a GET. No case was edited, no consent, upload, finance, release or time entry was recorded, and no Azure resource was created or changed, so nothing needed deleting. No source file changed.
* Retained evidence is under [deployed-parity-live-r2-2026-11-18/](deployed-parity-live-r2-2026-11-18/): `raw/` (commands and outputs), `screens/` (17 PNG) and `scripts/` (Playwright helpers). One case reference appears in the screenshots and is a fictional synthetic record.

## Result summary

| # | Criterion (short) | Result |
| --- | --- | --- |
| 1 | Anonymous protected API returns 401 for browser requests; page redirect kept | Unproven, failing |
| 2 | Staff prerequisite; every dated feature row and 16 assets through the public app | Partly proven |
| 3 | Representative continuing synthetic baseline | Partly proven |
| 4 | Model deployment, five assistants, workflow-only, durable state, bounded release | Partly proven; release authority human-owned |
| 5 | Approved map provider; map, list, chart, CSV and sensor agreement; accessible alternative | Partly proven |
| 6 | Own-user photo token prerequisites | Unproven; deferred (consent) |
| 7 | Versioned law store configured and seeded | Unproven; deferred (human-owned, data change) |
| 8 | Ledger, document and digest durability; scheduled jobs | Partly proven |
| 9 | Time capture gated with explanation; case work independent | Partly proven; defect confirmed |
| 10 | Per-role workflow, consent, finance, chat, export, law and recovery results | Partly proven; one role only |

No criterion is fully proven, and none is ticked. A row that reads "Partly proven" names below what is proven and what is not.

## Findings since the 2026-10-16 audit

The issue text is partly stale. Observed 2026-11-18:

* The Foundry account `aif-cutover-test-rzsrg` has one deployment, `standard` (gpt-4.1-nano 2025-04-14, capacity 10, `Succeeded`), and the app sets `AI_ENDPOINT`, `AI_DEPLOYMENT` and `AI_DEPLOYMENT_STRONG` ([raw/04](deployed-parity-live-r2-2026-11-18/raw/04-azure-readonly.txt)).
* `ZF_TILE_URL` is explicitly set to the OpenStreetMap standard tile URL with attribution.
* The store holds 443 open and 537 completed cases (980), not one case.

## 1. Browser-mode 401 versus 302 (unproven, failing)

Anonymous requests, 2026-11-18 11:38 UTC ([raw/01-anonymous-matrix.txt](deployed-parity-live-r2-2026-11-18/raw/01-anonymous-matrix.txt)):

| Path | Native curl | Browser UA, Accept JSON | Browser UA, Accept HTML |
| --- | --- | --- | --- |
| `/api/cases`, `/api/me`, `/api/staff`, `/api/assistants`, `/api/stats`, `/api/law`, `/api/time/status` | 401 | 302 to `login.microsoftonline.com` | 302 |
| `/cases.html`, `/app` | 401 | 302 | 302 |
| `/healthz`, `/` | 200 | 200 | 200 |

The page redirect is preserved, but every anonymous protected API request with a browser User-Agent still receives 302, so the criterion fails. Easy Auth is `unauthenticatedClientAction=RedirectToLoginPage` with excluded paths `/healthz`, `/readyz`, `/`, `/welcome.html`, `/style.css`, `/zava-logo.png` and `/sign-in` ([raw/01-easyauth-config.txt](deployed-parity-live-r2-2026-11-18/raw/01-easyauth-config.txt)).

Why it was not fixed: the platform has one global action; `Return401` would also break the browser page redirect that the same criterion requires, and a per-path split needs a trusted platform-principal design (see the 2026-11-04 plan). Changing the sign-in edge of the demo is also not in the owner's authorisation and is coupled to #349.

## 2. Tenant/staff prerequisite, dated rows, 16 assets (partly proven)

Proven:

* The staff session shows the cases page at `/app` ([staff-landing.png](deployed-parity-live-r2-2026-11-18/screens/staff-landing.png)); `/api/me` returns role `Retrofit Programme Manager`, `auth_provider=trusted-proxy`, 13 navigation items and 4 service flags ([raw/02](deployed-parity-live-r2-2026-11-18/raw/02-staff-api-probe.txt)).
* All 13 navigation routes plus the law viewer rendered at 1440x900 with no failed response except three expected ones (time status 500, aftercare form 403, law sources 503) ([raw/03-staff-render.txt](deployed-parity-live-r2-2026-11-18/raw/03-staff-render.txt); screenshots `staff-*.png`).
* The 16 historical assets all return 200 from the deployed app ([raw/06-assets.txt](deployed-parity-live-r2-2026-11-18/raw/06-assets.txt)). Eight hashes match the repository copy (`law.js`, `timecapture.js`, `zava-logo.png` and the five `vendor/` files). Eight differ (`app.js`, `assistants.js`, `index.html`, `law.html`, `ops.js`, `panels.js`, `style.css`, `welcome.html`) because web files changed in `main` after the image was built: commits 843c007d3 (2026-11-17 22:36 +01:00) and 5cb2c6027 (2026-11-18 07:23 +01:00) post-date the revision. The deployed files are older, not corrupt; rendering them is the proof, and a hash match to head is not claimed.

Unproven: no write or role-specific action in any dated feature row was executed (case actions, sign-offs, handoffs, consent, upload), the other roles (contractor, assessor, quality, finance approver) have no test account, and the aftercare form returns 403 for this role. The parity matrix rows stay Blocked for those.

## 3. Synthetic baseline (partly proven)

Authenticated reads ([raw/02](deployed-parity-live-r2-2026-11-18/raw/02-staff-api-probe.txt), [raw/07](deployed-parity-live-r2-2026-11-18/raw/07-staff-api-probe-2.txt)): `/api/stats` open 443 and completed 537; 30 visits; 1 package; 601 work orders; 13 finance rows; 167 funding rows; 4 handoffs; five checklist families; a case card with 5 documents; ranking snapshot of 443 entries under policy 1.0.0. This agrees with the historical 980-case figure.

Unproven: who restored the baseline and under what authorisation is not recorded in this run; sensor and contractor cases are not visible to this role (`/api/sensors` and the case sensors route return 403); the ranking policy is an unsigned draft (`policy_signed=False`), so no priority is ratified. No restoration was performed.

## 4. Models, assistants, workflow-only, release (partly proven)

Proven: the deployment exists and is configured (above). `/api/assistants` lists five assistants and nine registered tasks, `proactive=False`, with limits and a manual route; `/api/assistants/proposals` returns five proposals with the notice "Operator authority, finite allowance and expiry are required"; `/api/assistants/rai-metrics` shows 86 persisted records, which indicates durable state. `/api/governance` reports `releases=[0]` and three `release_gaps`; `/api/ai/priority` returns no recommendation. The Assistant proposals screen renders ([staff-assistants.png](deployed-parity-live-r2-2026-11-18/screens/staff-assistants.png)).

Unproven, and human-owned: a bounded release (an approved, unexpired record and an appointed task owner, OQ-017) does not exist and was not created. No live model draft was produced, so live output, the failure path against the real model and an AI task surviving restart are unproven. Calling the model needs release authority that only a named human can grant.

## 5. Map provider and agreement (partly proven)

Proven ([raw/08](deployed-parity-live-r2-2026-11-18/raw/08-agreement.txt), [raw/12](deployed-parity-live-r2-2026-11-18/raw/12-map-list-alternative.txt), [staff-overview-map-list.png](deployed-parity-live-r2-2026-11-18/screens/staff-overview-map-list.png)):

* Overview renders a Leaflet map; 18 OSM tile requests were all 200; attribution "Leaflet | OpenStreetMap contributors" is shown.
* The "Show the map areas as a list (keyboard and screen reader friendly)" control opens a list of 443 rows, matching 443 markers.
* Agreement at 443: `stats.kpis.open`, the sum of the stage chart (443), `/api/map` total, shown and unique items (cap 500), `/api/cases?view=all` total, and `/api/cases.csv?view=all` rows (443 unique, same reference set as the map).

Unproven: an approved or licensed provider (the demo uses the public OSM standard tile server, whose usage policy does not suit production reliance; choosing a licensed provider is an owner decision); sensor agreement (403 for this role); the closed-cases export holds 20 rows against 537 completed, which this run did not explain.

New defect observation: `/api/cases.csv` with the default or explicit `view=mine` returns 133 rows, all with the signed-in user as owner, while `/api/cases?view=mine` and `/api/me` report 16. The 16 are a subset of the 133. List and export therefore disagree for the own queue.

## 6. Own-user photo (unproven; deferred)

`/api/account/photo` returns 503 "Microsoft photo access is not available. Sign in again after token-store setup." and `/api/me` reports `services.photo=false`; Easy Auth `login.tokenStore.enabled=false` ([raw/01-easyauth-config.txt](deployed-parity-live-r2-2026-11-18/raw/01-easyauth-config.txt)). Enabling the delegated token store needs authorised consent (#116) and changes the sign-in edge, so it was not done. Binary photo, fallback and account switching are unproven.

## 7. Law store (unproven; deferred)

No `ZF_LAW_STORE`, `ZF_LAW_DB` or `ZF_LAW_BLOB_*` setting exists ([raw/00](deployed-parity-live-r2-2026-11-18/raw/00-app-config.txt)); `/api/law`, `/api/law/sources`, `/api/law/cards` and `/api/law/alerts` all return 503 "The law store is not loaded", and the viewer shows that state ([staff-law.png](deployed-parity-live-r2-2026-11-18/screens/staff-law.png)). The alerts route fails safe (`status=unknown`, human hazard route named). Seeding the store is a data change through the SQL/Blob path, and source, viewer and approval controls are human-owned (#210, #211, #213), so it was not done.

## 8. Ledger, document, digest durability and jobs (partly proven)

Proven: the audit ledger is intact with 1,722 entries and no problem (`/api/audit-check`); `/api/continuity` is healthy (epoch 0, history valid, no suspensions); the Event Hub namespace `evhns-cutover-test-demo` is `Succeeded` and Active with hub `sensor-readings` (2 partitions) ([raw/04](deployed-parity-live-r2-2026-11-18/raw/04-azure-readonly.txt)). Five case documents download with 200 ([raw/09](deployed-parity-live-r2-2026-11-18/raw/09-documents.txt)), but all five are `generated=True` text placeholders (110 to 129 bytes), not Blob-stored uploads.

Unproven: `digests_checked=0`, so digest durability is not shown (`/api/ledger/digest` is 403 for this role); uploaded-document durability needs a write; the storage account rejects data-plane listing from this host (network rules), so Blob contents could not be inspected; all eight Container App Jobs are `Manual` with no cron. `job-cutover-test-ledger-verify` shows scheduled-style executions on 2026-10-24 to 26 (all Succeeded) and manual ones on 2026-11-18 (Failed 08:00 and 08:02, Succeeded 08:05) ([raw/13](deployed-parity-live-r2-2026-11-18/raw/13-ledger-verify-job.txt)); no schedule is configured now, so no scheduled run can be verified. The document scanner logs "no malware assurance" (#117).

## 9. Time capture (partly proven; defect confirmed)

`/api/time/status` returns 500 on repeated calls, including after a fresh replica start; the container log shows `http-error GET /api/time/status status=500 exc=ProgrammingError` ([raw/05](deployed-parity-live-r2-2026-11-18/raw/05-time-status-log.txt)). The screen shows "Staff time capture could not load. Owner: application support" instead of the gated explanation ([staff-time.png](deployed-parity-live-r2-2026-11-18/screens/staff-time.png)).

Likely cause (hypothesis from reading `timecapture.py`, not tested): `_exists()` returns true whenever a SQL store is set, so `status()` queries `time_request` and `time_enabled`, which exist only after `_ensure` runs on a first write; on Azure SQL the read fails. `/api/time` is 403 for this role. Case work is independent: all case, list and overview routes loaded while time status failed. Fixing this is a source and SQL change, so it needs the FULL tier and is a follow-up, not part of this proof.

## 10. Per-role results (partly proven)

Recorded for the Programme Manager only: lists (cases, visits, packages, work orders, finance, funding, handoffs), exports (CSV), continuity, ledger check, retention (0 records), data-protection register (owners not yet named, `dpo_reviewed=False`), exceptions (`roles_not_named`), finance exposure (held, human decision), ranking publication (`overdue=True`, unsigned). `/api/chat/threads` returns no threads for this user now.

Not recorded: any other role, resident consent and pause flows, privacy and recovery actions, chat dialogue (a POST), finance and grant actions, law. The resident demo app (`ca-resident-demo`, revision 0000012) shows a sign-in form ([login-resident.png](deployed-parity-live-r2-2026-11-18/screens/login-resident.png)); a signed-in synthetic showcase page, "Your home improvement progress - synthetic showcase, not live", was observed (raw output not retained); it has no staff API and is not evidence for staff workflows.

## Open follow-ups

* Decide the edge behaviour for anonymous browser API requests with #349 (criterion 1).
* Fix `/api/time/status` on Azure SQL and show the gated explanation (criterion 9), FULL tier.
* Explain the `view=mine` CSV (133) against list (16) difference and the 20-row closed export (criterion 5).
* Human-owned and deferred: release authority (OQ-017), licensed map provider, photo consent, law-store seeding, scheduled-job design, further role accounts.
