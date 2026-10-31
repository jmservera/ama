---
title: Exact-main two-site redeployment plan
ms.date: 2026-10-31
---

Task 975bbf93-de84-47b4-ad5d-b55583f970c9; demo-sites-redeploy-1031.
Status: operational implementation complete; one independent Review Complete /
Not accepted against whole requested acceptance. Local persistence pending.

## Executive Summary

Build both images from main 4cb5964f7acce89668a37b5a56c3e125e26f6d21,
reuse the latest successful guarded ACR/SQL/pair-rollout executors and restore
all protected configuration. Verify exact deployed image provenance and fresh
anonymous HTTP/browser behavior. Current main versions URLs but does not give
assets long-lived cache headers; employee widget routes require sign-in.
Those checks will be recorded unmet, not hidden or repaired by changing source
or weakening authentication. Local commit only, no publication or push.

## Sources

Research: .copilot-tracking/research/2026-10-31/demo-sites-redeploy-1031-research.md.
Original and latest changes records dated 2026-10-30 read and preserved.
Exact latest private root:
/home/azureuser/.copilot/session-state/fc881d21-3ba8-4071-a186-c2dba4fa081e/files/redeploy.
Guarded original root:
/home/azureuser/.copilot/session-state/f07c3f9e-9452-44e9-95f3-7dff928ba9eb/files/redeploy.

## User Decisions and Requirements

* Full RPI loop, dated artifacts in this worktree and local Conventional Commit.
* Always authorized to redeploy both demo sites through 2026-11-15.
* "Always allow a short public-access window on the ACR, but if not possible,
  use `az acr build` command".
* Protect live digests, config backups, exact private ACR restore/readback.
* In-VNet initializer counts only; pair roll, min0, eight Manual jobs unchanged.
* Cold-start-aware curl/Playwright without sign-in; record every command/result.
* Resident AI OFF; no .env/secrets/private data, RBAC/endpoints/public SQL/RG deletion.
* Refs #568, #520, #570 only, Copilot trailer; no push, no signed-in acceptance.

## Goals

Deliver exact-current-main images to both live sites without protected drift.
Persist honest, independently reviewed operational evidence.

## Scope and Non-Goals

Only redeployment and tracking evidence. No source/dependency/test/auth/cache
policy repairs, AI or new infrastructure. Full publication gate is separate:
no push/PR/final-candidate publication requested or claimed.

## Functional Requirements

Fresh complete private backups; source archive, OCI config/index/platform chain;
short defaultDeny/VM32 ACR exception with exact restore; original and new digests
preserved; one bound SQL init execution; resident then employee rollout with
persisted intent and pair compensation on failure; final full config readback.

## Non-Functional Requirements

External private root0700/raw files0600. No token outputs or secret argv.
Shared heavy lock for build/push. No blind retry of SQL/start/forward PATCH.
900s convergence and 180s health attempts; curl28/124 retry same target.
Known auth/cache nonconformance is diagnostic, not a startup-failure trigger.

## Acceptance Criteria

AC1 Both fresh tracked-main image chains published and immutable digests deployed.
AC2 ACR exact stable baseline restored/read back; old remote digests retained.
AC3 SQL terminal Succeeded, one replica/retry0, input/worker-bound post-COMMIT
counts receipt; unchanged counts/principal/allowlist and eight restored jobs.
AC4 Both exact target revisions ready/Healthy/100% with original auth/config,
history retained, min0; all four ama minima0 and all eight Manual.
AC5 Warm health200/public200; rendered versioned HTML, resident widget/dock200,
source-equal bytes, anonymous denial intact.
AC6 Measure long-lived versioned-asset headers and no-cache HTML and employee
widget200 expectations explicitly; report actual deviations, not whole acceptance.
AC7 Fresh anonymous Playwright contexts, public shells/widget open/Escape and
network/versioned URLs; no password, model or private/session import.
AC8 One independent critique/Review, sanitized actual command journal and local
Refs-only Conventional Commit with required trailer; no push.

## Test Ownership and Change Budget

Application tests/removals/additions: none; exact-main operational task.
Canonical targets are current-main archived src and dated tracking evidence.
Generated workers/backups/images/HTTP bodies stay external. Validation is real
build/registry/SQL/ARM/curl/Playwright, not unit-test proxies. Record unexercised
rollback/fallback branches as unproven. No complete local publication gate claim.

## Phase Checklist

<!-- P01 -->
### P01 Preservation, build and publish

* [x] P01-T01 Fresh backups, guarded execution adapters and locked tracked builds.
* [x] P01-T02 IP-only bounded push, verify old/new chains, exact ACR restore.

<!-- P02 -->
### P02 Private initialization and pair rollout

* [x] P02-T01 One counts-only SQL execution, restore eight full job definitions.
* [x] P02-T02 Roll resident then employee; verify intent/ready targets and rollback.

<!-- P03 -->
### P03 Anonymous verification and persistence

* [x] P03-T01 Warm curl/browser, cache/version/dock checks and final invariants.
* [ ] P03-T02 Export, one independent Review, dispositions and local commit.

## Critique Disposition

Original critique preserved at
.copilot-tracking/plans/2026-10-31/demo-sites-redeploy-1031-critique.md.
PC-001 rejected: asserted temporary-directory prohibition is absent from this
parent's actual instructions; explicit repository shared /tmp lock applies.
No unshared substitute or permission weakening.
PC-002 applied: named late operational failure handler performs guarded pair
compensation; known cache/401 and administrative failures do not trigger rollback.
PC-003 applied: pre-mutation complete dependency/hash/adaptation manifest,
current-task exporter, compile-only checks and actual per-criterion outcomes.
PC-004 resolved by correcting unsupported planning prose to actual original
procedure: pair app/image intent before first PATCH; exact per-app target intent
immediately before that app's single PATCH. This meets owner procedure reuse,
without unnecessary new suffix choreography; refuse blind resumed invocation.
PC-005 applied: current anonymous checks GET only; no assistant POST/submission.
PC-006 applied: cleanup classifies baseline, owned retry0 or drift; only owned
delta restored, both failures retained. No new SQL retry or fault injection.
No second critique. No unresolved deployment authority or planning blocker.

## Follow-Up Items

1. Current-main long-lived versioned caching is absent: source repair in a later
   independently reviewed workstream, no cache success claim here.
2. Signed-in employee/resident acceptance remains owner-run.
3. Resident generated-prose authority/prerequisites remain pending; preserve OFF.

## Handoff

One Review executed Complete / Not accepted. AC1-5/7 operational anonymous scope proven.
AC6 requested long-lived caching and anonymous employee-widget200 remain unmet;
HTML no-store is stronger freshness but not literal no-cache. AC8 local commit
pending after Review. Initial local proof helper defect triggered actual paired
recovery; evidence preserved and distinct corrected redeployment completed with
fresh backups. No unresolved operational blocker or source changes. Final intake
history adds3 revisions/app (initial forward, recovery, corrected forward);
final corrected attempt adds1/app relative to recovered baseline.
Changes: .copilot-tracking/changes/2026-10-31/demo-sites-redeploy-1031-changes.md.
RV001 cache and RV002 signed-in employee widget routed to distinct follow-ups;
RV003 undock action lacks state assertion, later evidence reconciliation.
Archive corrected-helper and registry raw-body limitations retained. No repeat
Review or current-task implementation; P03-T02 local administrative commit next.
