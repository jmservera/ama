---
title: Demo sites live correction plan
description: Bounded SQL-first two-site deployment with exact preservation
ms.date: 2026-10-29
---

Task 5a7ca259-9fe8-407c-accf-fc965757c10e; demo-sites-live-correction.
Parent eb7ee1f8-42fd-48a8-9c24-a1cbebb99513.

## Executive Summary

Backups completed read-only. Apply only the current-main resident view through
an execution override of the existing private initializer. Build exact-main
images using the previously approved local-Docker-to-ACR VM-only route and
restore ACR policies exactly before deploying. One resident forward revision,
then one employee revision. January authority is parked if unmerged #521,
owner-held credentials or individually approved rows prevent safe apply.

## User Decisions and Requirements

* Owner explicitly authorizes az, SQL view correction, one additional resident
  forward revision, employee deployment and conditional #521 apply.
* Preserve full configuration, env/secretrefs, identity, registry, ingress,
  min0, retained rollback and all eight Manual jobs exactly.
* No gh, push, secret printing/.env, authenticated smoke tests, broad network/
  RBAC/server changes, image/tag deletion or other app changes.
* Reuse prior local checks. Commit original and new dated evidence locally
  with Conventional Commit, Copilot trailer, Refs-only language.

## Goals

Both named sites healthy on exact current main, with count-only SQL prerequisite
proof and no unintended protected changes.

## Scope and Non-Goals

Only the view, bounded ACR exception and two app images/revision suffixes may
change. No source modifications, unmerged authority cherry-pick or additional
forward revisions. Authority can remain explicitly parked.

## Functional Requirements

SQL-before-resident-before-employee-before-authority dependency is mandatory.
Failure console and system logs must be collected while the failed resident
revision still exists before any recovery to the previous digest.

## Non-Functional Requirements

Full raw backups remain external private files. Journal all subprocess results
with timestamps/hashes; commit sanitized results only. Compare complete app
responses excluding only systemData and service runtime revision pointers/
provisioning/running status. Only image/suffix may differ in template.
Use nonblocking heavy admission for builds, no local test repetition.

## Acceptance Criteria

1. Both new revisions latest=ready, Healthy/Provisioned, min0 and anonymous
   /healthz200. Record /health separately (historically 404/401).
2. Exact protected app/ACR equality and job template/Manual equality; one added
   forward revision per app and no removed revisions.
3. SQL ordered 17-column shape including documents_json, counts only, exact
   resident principal SID/narrow rights, no allowlist or grants change.
4. Old live digests remain present and rollback revision remains available.
5. Authority applied safely or exact unmet owner prerequisites recorded.
6. Original independent critique and Review preserved; local evidence commit,
   no push or publication approval claim.

## Locked Test Ownership

No source or test edits, removals none, maximum additions zero. Reuse preserved
parent core/API/SQL/browser results. Operational checks are fresh, not regression
suite replacements. No full publication gate or receipt claimed; no publication.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: SQL prerequisite

* [x] P01-T01: Capture both apps/auth/all revisions, ACR and eight jobs privately.
* [x] P01-T02: Start existing initializer with execution-only view worker;
  verify 17 columns/counts/narrow principal rights and exact unchanged job GETs.

<!-- rpi:phase id=P02 -->
### P02: Exact-main images and revisions

* [x] P02-T01: Export tracked src at fetched main, build/push both images with
  source labels and immutable digests; preserve old digests, exact ACR restore.
* [x] P02-T02: One raw-template resident forward revision; logs-before-recovery
  on failure. Only once healthy, one employee revision and identical preservation.

<!-- rpi:phase id=P03 -->
### P03: Authority, Review and persistence

* [x] P03-T01: Evaluate #521 after healthy sites; apply safely or precisely park.
* [x] P03-T02: Reconcile evidence, execute one independent Review and commit locally.

## Critique Disposition

One independent critique Complete / Revise, original preserved. PC-001 through
PC-005 accepted and applied directly in details; no user decision or repeat
critique. Init retryLimit is 1, so temporarily set only retryLimit to 0 with
Manual unchanged, then restore exact original configuration in finally.
Execution template override still avoids persisting the worker.
Planning Readiness Ready for the authorized bounded execution.

## Follow-Up Items

January source integration/credential rotation may require owner work; no second
resident revision is inferred. Publication complete local gate and hosted/human
approval remain coordinator-owned.

## Handoff

Research .copilot-tracking/research/2026-10-29/demo-sites-live-correction-research.md.
Details .copilot-tracking/details/2026-10-29/demo-sites-live-correction-phase-details.md.
Changes .copilot-tracking/changes/2026-10-29/demo-sites-live-correction-changes.md.

Final: all declared tasks complete, authority explicitly parked rather than
applied. Original independent Review Complete / Residual work, two Low historical
evidence limitations routed later. Evidence committed locally as
11f58b9064046d5ced32778dfe8e81e3c3f73543, privacy-safe author/committer and exact
trailer verified. No push or full publication gate claimed. Final state
bookkeeping is a separate local commit; no new live work.
