---
title: Epic 113 first unmet demo criterion, per-criterion recheck (Refs #113)
description: Recheck on 2026-11-19 of the three acceptance criteria of epic 113 for the synthetic desktop demo, with live GitHub and Azure reads and the reason no source change is justified
ms.date: 2026-11-19
---

Refs #113. Scope is the synthetic demo, desktop only, under the owner decisions of 2026-11-18 (live Azure authorised in resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change; billing reconciliation, DPO and Legal approval and person-run assistive technology testing not needed for the demo). This note ticks nothing. No source, test or Azure resource changed, so nothing needed deleting. No browser or credential was used.

## First unmet criterion

Criterion 1: "Complete the scoped stabilization checkpoint defined in #440 before epic closure." It is the first unticked box and it is unmet.

It is not a code criterion. #440 is OPEN (last updated 2026-11-17) with two unticked criteria: triage of confirmed findings into owner-approved RPI issues, and the research, plan, changes and independent review artifacts in a PR. Both are process and approval items. The issue text also says merged children alone do not satisfy it, and that requirement changes, pivots and deliberate deferrals need owner approval. A code change cannot satisfy them, so no source or test was written, and the tier is FOCUSED (documentation only).

## Live observations (2026-11-19, about 08:40Z)

* `gh issue view` states: #113, #114, #116, #117, #119, #120, #121, #122 and #440 OPEN; #118 CLOSED (2026-11-18); #1906 OPEN. One of eight children is closed, up from none on 2026-11-18.
* `az containerapp show -g ama -n ca-cutover-test-demo-api` (read-only, existing login): revision `ca-cutover-test-demo-api--0000033` Running, image digest `sha256:5368f4e4009cc32937377862e6d242c124005ed39081e1d9caa3b6b5dc17e5fb`. The digest is unchanged from the 2026-11-18 audit; the revision moved from 0000031 to 0000033 without an image change.
* Latest #440 comments (2026-11-16 and 2026-11-17) record unresolved owner decisions on a checkpoint evidence retention question and a privacy review of a preflight log, plus a retained map browser-check failure. They block publication of that checkpoint, not demo behaviour.

## Per-criterion table

| # | Criterion | Demo result | Proven or unproven | Why |
| --- | --- | --- | --- | --- |
| 1 | Stabilization checkpoint #440 completed, residuals and owner decisions recorded | Not met | Unproven | #440 open with two unticked criteria; [triage](./stabilization-checkpoint-triage-440-live-2026-11-18.md) verdict for #113 is "Continue", gated on owner decision D1. Needs #440 closed and an owner decision. |
| 2 | All child features closed or deferred | Not met | Unproven | Seven of eight children remain OPEN; #118 is the only closed child. #120 and #121 carry deferrals of DPO and Legal items to #1906, but no owner-approved deferral covers the remaining demo-provable gaps listed in the [2026-11-18 audit](./issue-113-epic-audit-live-2026-11-18.md). |
| 3 | No production claim without measured load, recovery and DPO or Legal approvals | Holds as a negative guard | Unprovable for the demo | The demo makes no production claim (ADR 0002 line 1131; live register `dpo_reviewed` false per the 2026-11-18 probe, not re-read today). Production-scale load, restore timing and DPO or Legal approvals are out of demo scope and sit in #1906. |

## Residual actions

* Owner: decide D1 for #113 and record a deferral or closure for each open child.
* Engineering, needs an owner decision on a deployment change: roll the demo API image to main so the deployed app carries `verify_ledger_before_reliance`, then run per-year ledger verification (#114). Not done here because it is a deployment change.
* Routing: production-only items remain with #1906 and the named children.

## Evidence limits

* GitHub and Azure reads are point-in-time. Raw output was not retained beyond the values quoted above.
* Per-child statuses other than the issue states above are carried from the 2026-11-18 notes, not re-executed.
