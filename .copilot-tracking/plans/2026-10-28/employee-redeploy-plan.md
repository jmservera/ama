---
title: Employee single redeploy plan
description: Finite operations and publication boundary for employee-redeploy-20261028
ms.date: 2026-10-28
---

## Task Metadata

* Task ID: employee-redeploy-20261028
* Task slug: employee-redeploy
* Planning status: Complete / re-apply verified, evidence published in #518
* Details: .copilot-tracking/details/2026-10-28/employee-redeploy-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-28/employee-redeploy-plan-critique.md

## Executive Summary

Reuse completed P01 image proof and the existing pushed digest. Owner approved
one additional forward revision on2026-10-28, with the same three AI settings
and min0, preserving everything else. Verify manifest read-only; use the approved
temporary ACR route only if needed and restore exact policy before rollout.
Roll back only for unhealthy revision or app startup errors, not tooling failure.
Publish evidence under the explicit owner exception without waiting for the full
gate; disclose original matrix drift and pending #517 fix. No rebuild, source
change, inference, cost query or resource creation.

### What You May Not Know

The registry currently denies public access despite default action Allow; its
original policy must be restored literally, not replaced with a preferred
policy. Anonymous sign-in challenges are expected and do not prove a broken
rollout. An authenticated asset/UX check and task-release/model acceptance
cannot be claimed from anonymous probes. Publication requires the complete
local gate normally; this evidence PR has an explicit dated owner exception.
No gate success or independent approval may be inferred from that exception.

### Current Blockers

* No active operational blocker: exactly one approved re-apply is verified.
* Historical complete gate failed `Workflow matrix drift: src-deploy.yml`;
  #517 proposes its correction. Publication authorized with explicit disclosure.

## User Decisions and Requirements

* Full brief RPI loop; #514/#515/#516 already merged; exactly one employee redeploy.
* Use `docker build -f src/api/Dockerfile src`, existing ACR expose-token/docker
  route and temporary VM `/32`; restore exact original policy afterwards.
* Set only AI_ENDPOINT, AI_DEPLOYMENT and AI_DEPLOYMENT_STRONG from #515/Bicep.
* Keep min replicas zero, identities, registry, secrets/references and other env.
* No other apps/jobs/RG/roles/network changes beyond authorized ACR exception;
  never read/print secrets or `.env`; no extra resources.
* Latest owner decision: roll back only on unhealthy revision or app startup
  errors; verification-tool failure alone must not trigger rollback.
* Commit tracking with requested coauthor, push `ops/employee-redeploy-20261028`
  and open Refs-only PR without waiting for full gate, disclosing #517 and
  validation actually performed under the explicit2026-10-28 exception.
* Nonblocking `/tmp/ama-rpi-heavy.lock` while Docker builds.
* Owner update: proceed without cost query; one build and revision accepted
  within budget. No cost retries or claim of known all-in headroom.
* Failure-only rollback uses exact backed-up image and env in Single mode;
  retain old manifest/tags, do not purge or alter revision mode.

## Goals

* One healthy digest-pinned employee revision with exact approved AI settings.
* Auditable preservation, ACR restoration and honest acceptance boundaries.

## Scope and Non-Goals

* Included: named employee app, existing ACR image/policy exception and tracking.
* Excluded: source edits, all resident workloads, jobs, roles, new resources,
  private datasets, secret APIs, `.env`, inference and authentication bypass.

## Functional Requirements

* Store exact app configuration metadata/env and current digest, revisions,
  auth configuration metadata if needed, identity, registry and scale outside
  git under `/tmp`; project secret definitions to references only.
* Build one unique image tag; token only in process memory/stdin and isolated
  temporary Docker config; never output or commit it.
* Digest-pin one additive app update, container `api`, min zero, unique suffix.
* Verify entire unrelated template/config/identity baseline, not just three keys.
* Restore ACR before rollout; private access first, remove only owned IP rule,
  restore original export/default/public/bypass/IP/VNet fields and compare.

## Non-Functional Requirements

* No queueing for shared heavy lock; busy ownership blocks affected build/gate.
* Bound command timeouts, revision convergence and log/error checks.
* Only ephemeral local image checks with no real database/cloud credentials.
* Keep external backup and sanitized operation results; do not commit config
  values, credentials, Docker config or raw logs.
* Explicit owner financial exception permits only this bounded build/revision;
  all-in headroom remains unknown, no new resources or paid inference.

## Acceptance Criteria

* A single new revision exists and is Healthy; ready/latest matches new suffix,
  pinned image matches pushed manifest digest and traffic routes to it.
* Existing configuration equals baseline except image, suffix, three AI entries;
  min zero stays zero. All registry/identity/secret-reference/auth state preserved.
* Public `/healthz` is 200 if reachable or expected 401 sign-in challenge;
  no startup error in bounded new-revision system/console observations.
* Built image's actually served synthetic HTTP index orders ops.js before app.js;
  live assets checked if anonymously accessible, otherwise disclose protected
  route boundary without changing auth or inventing a staff session.
* ACR policy matches exact baseline after push and at final readback.
* On unhealthy revision or app startup errors only: update exact backed-up image
  and env, verify old digest/readiness/traffic in Single mode. Verification-tool
  failure alone is disclosed, never a rollback trigger.
* Original critique, failed gate and independent Review retained unchanged.
  Owner-authorized evidence PR discloses missing successful full gate and
  independent exact-head assessment; no acceptance or gate pass claimed.

## Sources

* .copilot-tracking/research/2026-10-28/employee-redeploy-research.md: C1-C4/W1-W4.
* infra/README.md: small employee prerequisite and historical API contract.
* src/README.md: full local deployment/publication gate.
* Caller request: finite operational approval and exclusions.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve and publish image

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Capture baseline and build once

Use safe projections, external mode0700 directory, verify context has no local
untracked/ignored files, build with nonblocking heavy lock and immutable source SHA.
Fresh reference-only backup: `/tmp/ama-employee-redeploy-20261028-resumed.kbxpikmg`.
One build completed with nonblocking heavy-lock admission. Exact built image
served health/app/ops.js/app.js HTTP200; script indices2<7. Old backup retained.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Push digest and restore ACR

Depends on P01-T01. Temporary one-IP deny-by-default route, expose token,
docker login/push, digest readback, finally restore exact original policy.
Complete: pushed digest equals the local RepoDigest (not the image ID); old manifest retained.
ACR baseline equality verified after correcting removal to Azure's canonical
bare IPv4 rule representation. Public access was already disabled throughout
that cleanup correction; employee baseline stayed unchanged.

<!-- rpi:phase id=P02 -->
### [x] P02: Owner-approved one-time re-apply and verification

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: One additive re-apply and bounded checks

Depends on P01-T02. Verify no baseline drift immediately before write. Update
image/three env entries/min zero once; verify health, config, logs and assets.
Complete: one additional revision using existing digest, update exit0, exactly
one added revision. Full unrelated config/template/identity preserved.
Supported system/console logs checked, positive console startup, no matched
startup errors; health200/protected assets401. Historical attempt retained.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Failure rollback or success readback

Depends on P02-T01. No forward-update retry. On unhealthy/startup failure only, update the exact
backed-up image and complete original env; verify original configuration and
health. Owner explicitly permits this recovery revision in Single mode.
Complete: final active revision
`ca-cutover-test-demo-api--emp-reapply-20261028-110058`, Healthy/Provisioned/Running,
latest=ready,100% traffic, min0/max4 and exact ACR policy equality. No rollback.

<!-- rpi:phase id=P03 -->
### [x] P03: Review and owner-authorized evidence publication

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Record evidence and independent Review

Reconcile plan/details/changes and retain the one original independent Review.
Complete: original independent Review execution Complete, outcome Not accepted.
RV-001..005 routed; no deployment acceptance or repeated Review.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Commit and owner-authorized evidence publication

Resolve privacy-safe authenticated git identity. Commit evidence with trailer,
push only the requested topic and open Refs-only PR. Do not wait for full gate:
owner explicitly directs publication with drift/#517 disclosure. Retain original
failed receipt and original Review; list only validation actually performed.
No force-push, main write, rewrite or merge. Hosted/human approval stays separate.
Complete: evidence commit87bd00bd pushed to the requested topic; Refs-only
PR #518 opened against main. Full gate not rerun under explicit exception.
Original failed receipt and original Not accepted Review remain unchanged;
completion means evidence publication, not gate/release/human acceptance.

## Dependencies and Test Ownership

* No test removals or additions; maximum additions zero, no canonical source or
  generated runtime targets. Operations/tracking only.
* Semantic evidence: exact config diff and ACR policy equality; regression
  evidence: local image HTTP/assets, Azure revision/log/probe results.
* Original final RPI Review precedes candidate gate; later exact-head publication
  assessment is a distinct publication gate, not a second RPI Review.

## Critique Disposition

Original critique execution Complete, verdict Revise; no repeat. The following
records the original conservative dispositions, not current runtime state.
Owner continuation supersedes PC-001/003 prerequisites with explicit recovery/
cost decisions; PC-004 proof executed and PC-005 exception restored exactly.

| Finding | Disposition | Resolving evidence/action |
|---|---|---|
| PC-001 High | Applied conservatively, runtime dependency blocked | Remove multiple-mode fallback; official revisions/manage docs do not establish compliant Single-mode rollback. No app mutation. |
| PC-002 High | Applied | Require positive timestamped new-revision provisioning/readiness/replica evidence. Empty logs plus401 are not a pass; unobserved startup blocks acceptance. |
| PC-003 High | Applied conservatively, cost dependency blocked | ActualCost query429; alternative stable API/query Unauthorized/RBACAccessDenied. Headroom unknown, no new roles/login changes. |
| PC-004 Medium | Applied, execution blocked by lock | Existing Store accepts constructed `{cases:[],staff:[]}` fixture. Specify isolated UID-compatible data/state, loopback HTTP statuses/script parser and built-image ID binding in details; no weaker static-only pass. |
| PC-005 Medium | Applied | Ten-minute total ACR exception, bounded individual commands, private-first restoration in finally; no exception opened in this run. |

## Follow-Up Items

* Authenticated employee acceptance and task-release/model binding verification
  remain owner-operated work outside this no-inference redeploy.
* Existing src-deploy.yml workflow matrix drift is addressed by pending #517;
  no unrelated workflow edit or successful gate claim in this operation.
* No further forward rollout after the one newly approved re-apply.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-28/employee-redeploy-changes.md.
Owner selected later implementation of routed findings; original critique and
Not accepted Review remain immutable evidence, with no repeated critique/Review.
P01 reused. P02 one-time re-apply verified successfully. P03 publishes
evidence under the dated owner exception; historical failed gate/Review remain
unchanged. Current execution evidence belongs in the existing changes record.
PR #518 is open; automatic session remains running at Follow-up. No further
implementation begins without a selected follow-up and required authority.
