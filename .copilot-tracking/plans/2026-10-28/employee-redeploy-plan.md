---
title: Employee single redeploy plan
description: Finite operations and publication boundary for employee-redeploy-20261028
ms.date: 2026-10-28
---

## Task Metadata

* Task ID: employee-redeploy-20261028
* Task slug: employee-redeploy
* Planning status: Complete / implementation attempted and rolled back
* Details: .copilot-tracking/details/2026-10-28/employee-redeploy-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-28/employee-redeploy-plan-critique.md

## Executive Summary

Intended outcome remains one merged-main image and one employee revision.
Owner update re-admits the existing implementation: take the heavy lock
nonblocking, do not retry denied cost queries, and permit failure-only
Single-mode rollback by updating to the exact previous digest and env.
One forward rollout was attempted. Verification command failed, triggering the
authorized rollback. Exact old image/env are now restored and Healthy.
Desired AI-enabled deployment is NOT accepted; no further forward retry.
No source changes, inference or resource creation.

### What You May Not Know

The registry currently denies public access despite default action Allow; its
original policy must be restored literally, not replaced with a preferred
policy. Anonymous sign-in challenges are expected and do not prove a broken
rollout. An authenticated asset/UX check and task-release/model acceptance
cannot be claimed from anonymous probes. Publication requires the complete
local gate; historical exceptions on other PRs do not apply here. Its own
nonblocking admission must succeed without queueing.

### Current Blockers

* Forward update consumed. Failed system-log verification required rollback;
  another rollout requires separate owner authorization.
* Publication remains conditional on the complete exact-head local gate.

## User Decisions and Requirements

* Full brief RPI loop; #514/#515/#516 already merged; exactly one employee redeploy.
* Use `docker build -f src/api/Dockerfile src`, existing ACR expose-token/docker
  route and temporary VM `/32`; restore exact original policy afterwards.
* Set only AI_ENDPOINT, AI_DEPLOYMENT and AI_DEPLOYMENT_STRONG from #515/Bicep.
* Keep min replicas zero, identities, registry, secrets/references and other env.
* No other apps/jobs/RG/roles/network changes beyond authorized ACR exception;
  never read/print secrets or `.env`; no extra resources.
* Roll back to previous revision on rollout/verification failure.
* Commit tracking with requested coauthor, push `ops/employee-redeploy-20261028`
  and open Refs-only PR if required publication gates permit.
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
* On actual rollout/config/startup/asset failure: update exact backed-up image
  and env, verify old digest/readiness/traffic in Single mode.
* Original critique and independent Review retained; complete exact-head local
  gate/receipt verified immediately before push or publication remains blocked.

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
Complete: pushed digest equals exact local image ID; old manifest retained.
ACR baseline equality verified after correcting removal to Azure's canonical
bare IPv4 rule representation. Public access was already disabled throughout
that cleanup correction; employee baseline stayed unchanged.

<!-- rpi:phase id=P02 -->
### [x] P02: Update and verify once

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: One additive revision update and bounded checks

Depends on P01-T02. Verify no baseline drift immediately before write. Update
image/three env entries/min zero once; verify health, config, logs and assets.
Executed once, forward revision Healthy/Provisioned and exact config passed;
HTTP health200, protected assets401. System log command rejected --revision;
verification failed, not an accepted deployment. No forward retry.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Failure rollback or success readback

Depends on P02-T01. No forward-update retry. On failure only, update the exact
backed-up image and complete original env; verify original configuration and
health. Owner explicitly permits this recovery revision in Single mode.
Complete: rollback revision `ca-cutover-test-demo-api--rollback-20261028-103137`,
Healthy/Provisioned/Running, exact old digest/env/config except revision suffix.
Console startup positive, no startup error matches; health200/assets401.

<!-- rpi:phase id=P03 -->
### [ ] P03: Review and publication

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Record evidence and independent Review

Reconcile plan/details/changes and retain the one original independent Review.
Complete: original independent Review execution Complete, outcome Not accepted.
RV-001..005 routed; no deployment acceptance or repeated Review.

<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: Commit, complete gate and conditional publication

Resolve privacy-safe authenticated git identity. Commit evidence with trailer.
Fetch main, run full gate externally with `--lock-timeout 0`, verify receipt
at current main immediately before independent exact-head assessment and push.
If gate fails, retain original failure externally, record blocker, commit
historical outcome if needed and do not push/open PR.

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
* Publication is blocked if the full exact-head gate fails.
* Separate later owner authorization is required for another forward rollout.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-28/employee-redeploy-changes.md.
Owner selected later implementation of routed findings; original critique and
Not accepted Review remain immutable evidence, with no repeated critique/Review.
P01/P02 execution complete with failed verification and successful rollback,
not the desired AI-enabled outcome. P03 publication still conditional.
No push/PR without cleared publication gate.
