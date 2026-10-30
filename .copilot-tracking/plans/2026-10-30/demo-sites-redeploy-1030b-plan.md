---
title: Current-main demo redeployment plan
ms.date: 2026-10-30
---

## Task Metadata

Task870037be-e9ad-4240-8734-fa056bea01df; demo-sites-redeploy-1030b.
Branch chore/ops-redeploy-1030b, source a72cb268e11f2fc744d299b2b72bdcb1e05b5d6f.
Manual full sequence explicitly requested; no ongoing automatic follow-up session.

## Executive Summary

Build both images from tracked current main, preserve configuration and live
digests, and perform cold-start-aware live anonymous/browser checks. Full
deployment is blocked: the exact previous publisher needs a temporary public
ACR exception, now explicitly forbidden. Keep SQL/apps unchanged until an
authorized publishing path exists. Leave resident AI disabled.

### What You May Not Know

The prior admitted publisher was not a private transport: it opened a VM/32
public exception then restored ACR. Both public-denied and confirmed existing
private-login TCP timeout are freshly observed. Model provisioning/pilot
budget does not prove accounting migration or approval of generated prose.
Successful current-site health must not be reported as current-main delivery.

## Sources

Current research; earlier demo-sites-redeploy and demo-sites-redeploy-admitted
changes/details and actual retained private executors; API/infra READMEs.

## User Decisions and Requirements

* Full Research, Plan, Implement, Review; dated artifacts; same worktree.
* Build current main, protect live ACR digests, in-VNet counts-only init,
  roll employee and resident, rollback actual failure.
* Existing redeploy authority through2026-11-15; earlier USD337.19/700 accepted.
* No .env/secrets/private rows, RG deletion, new RBAC/endpoints/public network.
* Preserve min0, eight Manual jobs, ACR policies and configuration backups.
* Enable resident AI only if existing pilot approval and prerequisites suffice;
  otherwise keep off, report setting names only and exact unresolved decisions.
* Warm both health endpoints; long deadlines/retries; cold timeout alone is not
  failure. Curl/Playwright anonymous/public checks, every command/result.
* Local Conventional Commit, Refs only, exact Copilot trailer; no push.

## Goals

Safely deliver every independently eligible operation and a truthful persistent
record of unmet deployment criteria; no unauthorized substitute transport.

## Scope and Non-Goals

Two images, existing two demo apps/ACR/eight jobs; external private backups.
No feature edits, new infrastructure, SQL grants, model invocation, credentials,
authenticated journeys, issue closure, publication gate or remote Git write.

## Functional Requirements

Use the previous exact git-archive/docker build and preservation/check commands.
Fresh full app/auth/history/job/ACR snapshots before any eligible operation.
Publish/init/rollout remain gated, not silently skipped as success. No ACR
policy/network operation. Record existing digest references, full stable resource
equality and current public results. Four optional AI prerequisite names only.

## Non-Functional Requirements

Private evidence0700/0600; journal argv/exits/timing/output hashes, no secret
values. Heavy builds under nonblocking /tmp/ama-rpi-heavy.lock. Main pin must
match expected source. Curl health retries with per-attempt180s, total bounded
900s; HTTP timeout recorded, not alone a rollback condition. Fresh anonymous
Playwright context; no password/session import or OAuth query logging.

## Acceptance Criteria

* AC1: both tracked-source images built, source/config hashes recorded.
* AC2: two images published and previous live manifests protected: BLOCKED.
* AC3: in-VNet init success/count-only receipt and eight jobs restored: BLOCKED
  behindAC2; do not mutate SQL gratuitously when no rollout is admitted.
* AC4: both new digest targets ready/healthy/traffic100 and history retained:
  BLOCKED behindAC2/AC3. Failure rollback only after actual owned rollout.
* AC5: warm both health200, resident widget assets and anonymous boundaries
  checked with curl/browser; distinguish current old targets.
* AC6: full config/auth/history/jobs/ACR preserved; min0/all eightManual.
* AC7: AI off, optional setting names and explicit decision/prerequisite gaps.
* AC8: one critique, one independent Review, local commit/no push.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve and build
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Capture private backups and journal baseline
<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Build both exact tracked-source images under shared lock

<!-- rpi:phase id=P02 -->
### [ ] P02: Gated deployment
<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Publish with previous-digest protection (blocked)
<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: In-VNet initialization then resident/employee roll (blocked)

<!-- rpi:phase id=P03 -->
### [x] P03: Verification and local handoff
<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Warm public checks, Playwright and final preservation
<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Reconcile, independent Review and local evidence commit

## Test Ownership

No source or test changes. Exact removals:none; maximum test additions:0.
Canonical targets: dated task evidence and actual private executor copies.
Generated targets: external owned session files only. Actual two Docker builds,
curl/source-byte/public browser and full cloud-state comparisons validate this
partial operational outcome; no mock or unit proxy for deployment.
No repository-wide gate claimed; no publication requested.

## Critique Disposition

Exactly one independent critique: Complete / Revise, PC-001 High. Original
preserved unchanged. Parent disposition: rejected. PC-001 asserts an execution
prohibition on all /tmp file operations, but no such prohibition exists in the
current parent instructions or caller request. Repository API instructions and
the caller-required exact historical procedure expressly use the shared
/tmp/ama-rpi-heavy.lock. Replacing it would defeat inter-session exclusion.
Keep the existing nonblocking lock; no additional critique. This does not relax
the real no-public-network restriction or any cloud gate. Plan ready for
independently eligible work, full deployment still blocked.

## Follow-Up Items

* Owner-held authenticated resident/employee acceptance and actual-model quality
  remain separate from this anonymous deployment verification.

## Handoff

Implement only P01/P03 while B1 unresolved; P02 stays unchecked. Changes path:
.copilot-tracking/changes/2026-10-30/demo-sites-redeploy-1030b-changes.md.
P01/P03 complete. Original evidence committed locally as
baef7d8f33970cddd8af7250736ec9bd7caf00f2 after one independent Review,
Complete / Not accepted. P02 and AC2..4 remain blocked/unmet. Overall
implementation Partial/Blocked, not deployment success. Final parent-status
persistence is administrative only; no second Review or implementation.
