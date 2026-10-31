---
title: Redeploy 8 immutable-cache plan
ms.date: 2026-10-31
---

## Task Metadata

Task 2c99fa13-81cb-4fd2-af53-81ad16cb565a; demo-sites-redeploy-cache.
Planning status: Ready; operational implementation complete, one Review Complete / Residual work.
Details: .copilot-tracking/details/2026-10-31/demo-sites-redeploy-cache-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-31/demo-sites-redeploy-cache-plan-critique.md.

## Executive Summary

Redeploy both images from main d20bc50c4b664521f72446e5d0c85cc576ef0850,
using #596's guarded publisher and pair rollout. Prove #597's exact-year
immutable versioned asset caching and no-store HTML on both anonymous public
shells. Skip SQL because the inspected delta from 4cb5964f contains no SQL
change. Employee widget live200 is still behind authentication, not an anonymous
acceptance claim. Keep AI OFF and all protected baseline settings unchanged.
Local evidence commits only; no publication gate, push or signed-in claim.

## Sources

* .copilot-tracking/research/2026-10-31/demo-sites-redeploy-cache-research.md: Complete / Ready, C1-C3.
* .copilot-tracking/changes/2026-10-31/demo-sites-redeploy-1031-changes.md: exact #596 procedure and known fixes.
* .copilot-tracking/changes/2026-10-30/demo-sites-redeploy-changes.md: original evidence, not fresh authority.
* Retained helper root /home/azureuser/.copilot/session-state/975bbf93-de84-47b4-ad5d-b55583f970c9/files/redeploy.

## User Decisions and Requirements

* Full RPI loop, dated artifacts, current topic/worktree, local Conventional Commit only.
* Standing redeployment authority through 2026-11-15.
* "Always allow a short public-access window on the ACR, but if not possible, use `az acr build` command".
* Shortest /32 restriction if possible; push then exact prior private restoration/readback and old live digest protection.
* SQL init only if source diff since 4cb5964f touches SQL; resident AI stays OFF.
* Min0, all eight jobs Manual, existing backups/auth/policies/history retained; guarded rollback on actual live failure.
* Long-timeout cold-start warming, curl/Playwright anonymous health/assets/header/dock evidence; no sign-in.
* No secrets/.env/private data, no new RBAC/endpoints/public SQL/RG deletion.
* Refs #568, #520, #570 only; required Copilot trailer; no push.

## Goals

* Exact main images healthy on both sites, immutable public asset policy live.
* Evidence reproducible without disclosing secret config or overstating signed-in acceptance.

## Scope and Non-Goals

Operational redeploy and dated tracking only. No application source/test/dependency
changes, SQL init, identity or resident AI change. No new resources or historical
cleanup. Full publication/hosted/human gates remain separate and unclaimed.

## Functional Requirements

Fresh full private app/auth/history/eight-job/ACR backups. Tracked-source archive,
local OCI config binding, local packaged asset proof before cloud writes.
Guarded publisher with defaultDeny/VM32 and close-first exact ACR restore.
Persist pair intent before app writes and per-app intent before single PATCH;
retain all previous revisions and digests. One added revision/app on success.
Final exact protected app/auth/job/ACR readback and actual GET-only HTTP/browser evidence.

## Non-Functional Requirements

Private root0700/raw0600; journal actual argv/exit and stdout/stderr hashes,
tokens withheld. Shared /tmp/ama-rpi-heavy.lock for builds/publish. Distinct
main-20261031-d20bc50c4b66-cache8 tags. No blind repeated PATCH or job start.
180s health attempts/900s read-only convergence; timeout alone not failure.
Local proof and administrative failures never compensate live apps.
Live operational startup/HTTP/config failures invoke retained drift-guarded
pair recovery. Expected auth401/browser302 are diagnostics, not live failure.

## Acceptance Criteria

AC1: both new index/platform/config/source chains published and deployed by digest.
AC2: old live manifests retained; full stable ACR equals exact private baseline.
AC3: no SQL execution; all eight complete Manual definitions equal fresh baseline.
AC4: both exact revisions Healthy/ready/Provisioned/100%, protected config/auth/history equal, min0.
AC5: both warm health200, shell200/source-equal/versioned URLs; each public asset200/source-equal,
Cache-Control exact max-age=31536000 and immutable; HTML no-store.
AC6: resident chat JS/CSS/assistant and dock present/load200; fresh desktop/mobile
Playwright open/dock/undock/Escape state asserted. Employee anonymous denial
retained; packaged employee widget verified, live signed-in200 not claimed.
AC7: actual command/result/hash journal, one independent critique and Review,
Refs-only privacy-safe local Conventional Commit; no push.

## Test Ownership and Change Budget

Application test removals none, additions0. Canonical source d20bc50c archived
src; generated executors/backups/body receipts external current-session files/redeploy.
Real image/registry/ARM/curl/browser evidence, no proxy tests or conformance claim.
Fallback, retry/recovery and signed-in branches unproven unless actually exercised.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve, build and publish

Dependencies: Research / Ready and critique dispositions.
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Adapt/hash helpers; fresh backups; locked build and local image proof
<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Guarded IP-only push and exact ACR restoration

<!-- rpi:phase id=P02 -->
### [x] P02: Pair rollout without SQL

Dependencies: P01, image proof and private ACR restoration.
<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Record SQL skip, roll resident then employee and protected readbacks

<!-- rpi:phase id=P03 -->
### [ ] P03: Live verification and persistence

Dependencies: P02.
<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Warm curl/cache/browser/dock verification and full invariants
<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: Sanitized export, one independent Review and local evidence commit

## Dependencies

Existing Azure/Docker access confirmed; no new permissions. Guarded transitive
executors inspected. Recheck main pin/drift before build/writes.

## Critique Disposition

Original Complete / Revise critique retained unchanged.
PC-001 applied: pre-push image proof consumes current build-proof local IDs,
config/source/archive binding, not nonexistent push-proof or fabricated digests.
Remote digest proof remains exclusively P01-T02.
PC-002 rejected: alleged /tmp filesystem prohibition is not present in this
parent's instructions; actual repository requires shared /tmp/ama-rpi-heavy.lock.
Same unsupported advice was rejected in #596. Preserve shared exclusion, not
a unique or unverifiable substitute. No second critique or unresolved decision.

## Follow-Up Items

* Owner-run signed-in employee/resident identity/widget acceptance remains outside scope.
* Resident AI activation remains separately pending owner decision.
* Optional anonymous console-error diagnosis (RV-003) is a separate bounded
  maintainer task; counts alone are not a demonstrated defect.

## Handoff

Implementation changes path: .copilot-tracking/changes/2026-10-31/demo-sites-redeploy-cache-changes.md.
P01/P02/P03-T01 complete. AC1-6 scoped anonymous evidence passed; AC7 export
complete, original independent Review Complete / Residual work, local commit pending. Both public
versioned asset sets exact-year immutable and HTML no-store. Employee
protected widget live200/cache and signed-in/model acceptance unproven.
No operational blocker. RV-001/RV-003 routed separately; RV-002 local
administrative persistence next. No repeat Review or operational implementation.
