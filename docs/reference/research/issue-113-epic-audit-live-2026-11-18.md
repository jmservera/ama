---
title: Epic 113 Azure platform, security and data protection audit with live demo read (Refs #113)
description: Per-criterion evidence table for epic 113, a per-child roll-up of the unticked child criteria split into demo-provable and production-only, and a fresh read-only probe of the synthetic demo on 2026-11-18
ms.date: 2026-11-18
---

Refs #113. Scope is the synthetic demo, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change) and waive Azure billing reconciliation, DPO and Legal approval and person-run assistive technology testing for the demo. This note ticks nothing in any issue. No source code changed and no Azure resource was created, so nothing needed deleting.

## Method and retained evidence

* Issue state read with `gh issue view` and the sub-issue list of #113 on 2026-11-18. All eight children (#114, #116, #117, #118, #119, #120, #121, #122) are OPEN; #440 is OPEN; #1906 (production DPO and privacy sign-off, deferred from the demo) is OPEN. Observed; raw output not retained.
* Azure CLI with the existing login, read-only: `az containerapp show -g ama -n ca-cutover-test-demo-api`. Result: revision `ca-cutover-test-demo-api--0000031`, image digest `sha256:5368f4e4...c17e5fb` (unchanged from the same-day notes), scale 0 to 4 replicas.
* Playwright Chromium, 1366 by 900, signed in as the employee demo account (Entra, role `ZavaForward.ProgrammeManager`). The driver read credentials at run time, never printed or saved them, and scrubbed e-mail addresses and GUIDs; a scan of the output found no `@`. It made eight GET calls only. Six returned 200 (`/api/me`, `/api/audit-check`, `/api/data-protection`, `/api/retention`, `/api/continuity`, `/api/chat/status`). `/api/health` and `/api/documents` returned 403 for this role (a path or role refusal, not examined further). No write was made. The orientation screenshot was deleted because the workbench shows resident names.
* Files are in `.copilot-tracking/evidence/2026-11-18/issue-113-live/`: `live_epic113_probe.py`, `live_epic113_probe.json`, `az_containerapp.json`. Staff names and the registry host name were redacted afterwards; the driver takes the demo URL from an environment variable.
* Reused from merged or same-day notes, not repeated: [#114 ledger rerun](./sql-ledger-live-r2-2026-11-18.md), [#116 round 2](./issue-116-live-r2-evidence-2026-11-18.md), [#117 audit](./issue-117-live-r2-audit-2026-11-18.md), [#118 audit](./issue-118-live-20261118T1512Z-2026-11-18.md), [#119 round 2](./issue-119-live-r2-map-evidence-2026-11-18.md), [#121 evidence](./issue-121-live-data-protection-evidence-2026-11-18.md), [#122 audit](./issue-122-continuity-live-audit-2026-11-18.md), [digest alert](./digest-verification-alert-live-2026-11-18.md) and the [#440 triage](./stabilization-checkpoint-triage-440-live-2026-11-18.md). There is no research note for #120; its position is taken from the issue comments of 2026-10-31, 2026-11-05 and 2026-11-18.

## Fresh live observations (2026-11-18, about 16:25Z)

* `/api/me`: Entra identity source, role Programme Manager, `view_only` false, `auth_provider` `trusted-proxy`, 443 open cases.
* `/api/audit-check`: `intact` true, 2,076 entries (1,610 at the earlier #114 rerun, so the demo keeps writing), `digests_checked` 0, no mismatches. No yearly digest has been sealed against live data.
* `/api/data-protection`: label `synthetic-demo`, `dpo_reviewed` false, 8 classes; the statement reads "Recorded references are not verified DPO or Legal approval. Local deletion is not provider erasure."
* `/api/retention`: zero records, label "synthetic-demo placeholder period from the trigger; not an approved retention schedule. The DPO and Legal set the real periods."
* `/api/continuity`: epoch 1, `history_valid` true, one suspension `SUS-1` with scope `all` and status `Suspended`; the note states manual case work, resident challenge and hazard response continue outside any suspension.
* `/api/chat/status`: 200, demo-only activation as in earlier notes.

These agree with the same-day child notes: the demo store is durable and tamper-evident, nothing in the demo carries an approved retention period or DPO sign-off, and the live suspension has no restart authority.

## Epic 113 acceptance criteria

| # | Criterion (state on the issue) | Demo result | Evidence | Tickable now |
| --- | --- | --- | --- | --- |
| 1 | Stabilization checkpoint #440 completed, with Azure-only residuals and owner pivot or defer decisions recorded (unticked) | Not met | #440 is OPEN with two unticked criteria (triage into owner-approved RPI issues, and the research, plan, changes and review artifacts). The [triage](./stabilization-checkpoint-triage-440-live-2026-11-18.md) gives #113 the verdict "Continue", gated by D1 (the time status 500 against the #350 parity explanation) only if the owner or #120 criteria adopt it. The issue text also states merged children alone do not satisfy it. | No. Needs #440 closed and the owner's recorded decision on D1 for #113. |
| 2 | All child features closed or deferred (unticked) | Not met | Live `gh` read: #114, #116, #117, #118, #119, #120, #121 and #122 are all OPEN. #120 carries a comment moving DPIA and staff notice approval to Deferred (owner rule 2026-11-18, tracked with #1906) and #121 defers its DPO and Legal criteria to production, but the children stay open and no owner-approved deferral covers the remaining demo-provable gaps below. | No. Needs each child closed, or an explicit owner deferral per child. |
| 3 | No production claim without measured load, recovery and DPO or Legal approvals (unticked) | Consistent as a negative guard; not satisfiable for the demo | ADR 0002 line 1131 states "no production resilience or blanket assurance claim"; the live register says `dpo_reviewed` false and that references are not DPO or Legal approval; retention is a labelled placeholder; the live suspension `SUS-1` has restart authority unavailable. Measured demo-scale load and point-in-time restore are recorded in the #114 notes (30-minute run, restore of `retrofit` with hash-chain match); they are demo-scale only. DPO and Legal approvals are waived for the demo and sit in #1906. | No. The guard holds because the demo makes no production claim. Ticking needs production-scale load, restore timing and real approvals (#1906), all out of demo scope. |

## Per-child roll-up of unticked criteria

Class "Demo-provable gap" means something the demo could still show with owner-allowed actions. Class "Production-only" means it needs a named human approval, an appointed role, real scale or a drill the owner excluded.

| Child | Unticked criterion | Status | Class | Reason |
| --- | --- | --- | --- | --- |
| #114 | Per-year audit and ledger digest verification proven by test before reliance | Proven by 62 local tests and on live-shaped data; unproven on the deployed image | Demo-provable gap | The deployed image lacks `verify_ledger_before_reliance`, live data holds one year and `digests_checked` is 0 here. Needs an image roll (a deployment change, not done) and `VIEW LEDGER CONTENT` for native verification |
| #116 | Roles allowed to see a vulnerability reason confirmed (OD-14, OD-19) | Unproven | Production-only | Enforcement shown for one reason role with no leak across exports and AI surfaces; "confirmed" means a named human approval of the matrix, and no second role can be signed in (no directory privilege) |
| #116 | Allowlists at every provider boundary; permission recheck on outputs and exports; document AI derivative rule (RAI section) | Unproven live | Demo-provable gap (offline) and production-only (approved manifests) | Offline provider-spy tests are the evidence; payload content is not exposed by the deployed app |
| #117 | Uploads scanned before availability | Proven for the synthetic local scanner live and for the Defender tag path offline; unproven for a real engine guarding the app | Demo-provable gap | Defender for Storage is enabled on the account but the app default scanner is `local`; switching scanner config is a production-shaped change |
| #118 | Azure Policy and Defender plans decided | Decision recorded; live enforcement unproven | Production-only (enforcement) | Subscription-level policy and plans are outside resource group `ama` authority |
| #119 | Provider licence, cost, coverage and processor terms recorded | Unproven | Production-only | Demo uses OpenStreetMap tiles; selection needs owner, procurement and DPO |
| #119 | Screen reader test of the list alternative | Structural proof only | Production-only | Person-run assistive technology testing waived for the demo; the accessibility tree and keyboard path are proven |
| #120 | Staff notice approved and enabling action audited | Audit mechanics tested; notice approval unmet | Production-only | Moved to Deferred by owner rule 2026-11-18 (#1906) |
| #121 | Eight RAI-section criteria (identity population mapping, whole-system coverage, per-task declarations, owned retention, DPO/Legal approvals, others) | Partly observed live | Mostly production-only | The deployed image predates part of the register; approvals and retention periods are DPO and Legal decisions (#1906) |
| #122 | Witnessed authorised drill of suspension, communication and restart | Unproven | Production-only | Owner forbids drills; no appointed duty staff, restart authority (OD-35) or witness. Constructed drills (26 tests) prove the mechanism only |

## Residual actions and blockers

* Owner: record a decision on D1 for #113, and an explicit deferral or closure per child (criterion 2).
* Engineering (needs an owner decision on a deployment change): roll the demo API image to main, grant `VIEW LEDGER CONTENT` to a verifying identity, then run per-year ledger verification with sealing (#114).
* Engineering: choose the app scanner configuration for the demo (#117).
* Production-only items route to #1906 and the named children; none can be proven for the demo.

## Evidence limits

* The probe is a point-in-time read of a demo that keeps writing; counts will drift.
* Child-level statuses are taken from the cited same-day notes, not re-executed here, except the live reads listed above.
* The 403 on `/api/health` and `/api/documents` was not investigated.
* Tier: FOCUSED, documentation only. No source, test or workflow file changed.
