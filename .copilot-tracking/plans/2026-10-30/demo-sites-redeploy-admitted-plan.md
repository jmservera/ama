---
title: Admitted demo redeployment plan
ms.date: 2026-10-30
---

## Task Metadata

8053a799-0279-4f5c-b23b-adea3537291b; demo-sites-redeploy-admitted.
Parent f09558e0-64f4-4440-856f-8e9a302dbb6f retains original blocked outcome.

## Executive Summary

Publish the retained pinned-main images, initialize sensor schema and resident
view transactionally through the existing private SQL job, then roll resident
and employee with exact protected-state checks. Owner cost decision admits only
this redeploy. Research Complete / Ready; one critique Complete / Pass,
zero actionable findings at the original candidate. Deployment complete after
documented SQL corrections: both immutable target revisions healthy and
serving100%; SQL counts/schema/projection verified and preservation checks pass.
Minimal coupled SQL source correction and one real-SQL regression added.
No application image rebuild, dataset, credential, model call or push.

## Sources

.copilot-tracking/research/2026-10-30/demo-sites-redeploy-admitted-research.md;
original review and successful prior operational details referenced there.
Source ffd8f35e63b24905b9aeb937dbf2a7fe9968747f, freshly fetched unchanged.

## User Decisions and Requirements

* Owner 2026-10-30 08:36Z: "Proceed: RG cost 337.19 of 700 is sufficient headroom for this redeploy".
* No broader cost queries; authorization through 2026-11-15; existing IoT role
  and in-VNet sensor SQL job approved.
* Publish already built images to private ACR, SQL views/sensor tables counts
  only, roll both apps and rollback on actual failure.
* Minima0, eight jobs Manual, ACR policies/backups retained. No .env, secrets
  output, RG deletion, push, merge or closing keywords. Refs only.
* Full dated RPI loop, one critique and Review, local Conventional Commit
  with required Copilot trailer. Owner-run Entra checks reported separately.

## Goals

Both apps serve exact immutable retained images with healthy ready revisions;
SQL sensor schema/view is committed with no data or authorization expansion.

## Scope and Non-Goals

Two images, existing initializer executions, additive six-table sensor schema
and corrected view batch, existing two app image/suffix updates. No seeding, role changes
unless existing approved role is missing (otherwise report), telemetry/device
action, job image update, new infra, model smoke or authenticated bypass.

## Functional Requirements

Fresh full backups/drift checks; actual local config/source proof and remote
manifest binding including old digest preservation. One attempt per explicitly
recorded SQL execution/transaction, retries0 temporarily, same persistent
job/image/identity/env/resources. Failed/rehearsal/diagnostic executions are
retained separately; no ambiguous mutation replay.
Template-only raw app PATCH and one forward revision each, resident first.
All commands/results journaled privately, hashes and sanitized receipts committed.

## Non-Functional Requirements

Private execution root under current session files, modes0700/0600. Token only
memory/stdin; exact owned Docker auth cleanup. ACR exception max600s,
forward420s, private-first recovery reserve180s; per-request remaining deadlines.
SQL timeout600/retry0; no ambiguous start/reapply retry. App/recovery600s each.
Concurrent protected drift stops writes, never overwritten to force equality.

## Acceptance Criteria

Terminal SQL Succeeded plus one bound post-COMMIT marker with worker/input
hashes, one replica attempt per execution, six table shape/count equality, principal/rights
and 17-column view projection verified. All job definitions restored exactly.
Each app target latest=ready Healthy/Provisioned, active100%, ready replica,
exact expected digest, history retained, exactly one forward revision. Full
protected app/auth comparison; minima0; stable ACR exact equality.
Curl health200, resident shared assets200 and pinned-source bytes, employee
protected paths401/redirect. Playwright public shells desktop/narrow receipts.
Authenticated semantics are separately owner-run, not a condition fabricated
as automated success. Actual failure recovered is non-delivery.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve and publish
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Fresh backups, pin/config validation and bounded publication
<!-- rpi:phase id=P02 -->
### [x] P02: Initialize and roll
<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: One transactional in-VNet sensor/view initialization
<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Resident then employee rollout with recovery
<!-- rpi:phase id=P03 -->
### [ ] P03: Verify and persist
<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Curl/Playwright and full final invariant checks
<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: One independent Review and local evidence commit

## Test Ownership and Targets

Original candidate locked removals0/additions0; scoped implementation amendment
adds exactly one actual-SQL test to the existing boundary module, removals0.
Two selected modules44 tests pass on real disposable loopback SQL; targeted
Ruff lint/format pass. Missing core/build/lint prerequisites installed privately
only after actual missing-package/tool failures. Generated private executors
validated with compile and exact cloud/live assertions. Semantic
acceptance distinct from static assets. Publication gate/hosted/human approval
separate; no push and no receipt claimed.

## Critique Disposition

One independent final-candidate critique Complete / Pass, zero findings, at
.copilot-tracking/reviews/plans/2026-10-30/demo-sites-redeploy-admitted-plan-critique.md.
No repeat, planner correction or unresolved owner decision.

## Follow-Up Items

Owner authenticated chat/map/case acceptance, without sharing credentials.
Any future remote publication requires complete applicable local gate and
independent exact-head/hosted/human checks; no publication is requested here.

## Implementation Amendment

Initial SQL execution terminal Failed, worker explicitly rolled back before
emitting committed=false; no apps changed and all jobs restored. Permit one
read-only schema/count diagnostic execution to isolate the failed exact-shape
assertion. A corrected write requires a proven safe root cause, no ambiguous
commit and no schema ALTER/data/permission widening. Retain all original
failure evidence and exact distinct execution IDs; no blind or automatic retry.
Original critique remains Pass at its original candidate, not re-executed.
Null-default hypothesis disproved by a guard-only execution before DDL; local
SQL column predicates pass. Admit one rollback-only in-VNet rehearsal with
metadata/failing-line instrumentation to isolate the actual predicate.
No persistent change or app rollout permitted by rehearsal success alone.

Resident startup exposed a coupled source SQL defect: with both empty sensor
tables present, sensors_json is NULL for all522 admitted view rows. Counts-only
projection probe proves the issue; TOP0/count-only shape had not evaluated it.
Amend scope to the minimal SQL empty-history correction and one actual SQL
regression in the existing boundary-test module (maximum additions1, removals0).
Images remain the already-built source pin; SQL correction gets its own hash.
Stop pending read-only convergence before any recovery PATCH; roll back the
broken view behavior through transactional correction, then assess the SAME
single forward resident revision. No repeated forward rollout or auth bypass.

## Current Reconciliation

P01/P02 and P03-T01 complete. Two committed SQL transactions are distinguished:
initial schema/view commit, then verified empty-history view correction.
Failed, guard-only, rollback-only and read-only job executions remain visible.
One forward revision each; resident restart then one reactivation cycle reset
failed dependency activation, no recovery-image PATCH or extra revision.
Both target latest=ready Healthy/Provisioned active100%, ready replica, min0.
All eight complete job definitions and ACR protected state match baseline.
Curl health200 and resident widget JS/CSS200/source-equal; anonymous denial
preserved. Native traced Playwright public shells at1365x900/390x844 have no
horizontal overflow; resident shared widget script/runtime/launcher/dialog exist.
Console residuals are not a clean-console pass. Entra/owner-held authenticated
acceptance remains separately owner-run. One Review/local persistence pending.

## Handoff

Details: .copilot-tracking/details/2026-10-30/demo-sites-redeploy-admitted-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-30/demo-sites-redeploy-admitted-changes.md.
