---
title: Employee single redeploy plan
description: Finite operations and publication boundary for employee-redeploy-20261028
ms.date: 2026-10-28
---

## Task Metadata

* Task ID: employee-redeploy-20261028
* Task slug: employee-redeploy
* Planning status: Complete / Blocked for build, cloud mutation and publication
* Details: .copilot-tracking/details/2026-10-28/employee-redeploy-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-28/employee-redeploy-plan-critique.md

## Executive Summary

Intended outcome remains one merged-main image and one employee revision.
Execution is blocked before mutation: the shared heavy lock has a foreign
holder, current cost evidence is inaccessible, and a fully supported
Single-mode/no-second-revision rollback is not established. Complete only safe
read-only backup/evidence and independently review this blocked outcome.
No source changes, cloud mutations, inference or resource creation.

### What You May Not Know

The registry currently denies public access despite default action Allow; its
original policy must be restored literally, not replaced with a preferred
policy. Anonymous sign-in challenges are expected and do not prove a broken
rollout. An authenticated asset/UX check and task-release/model acceptance
cannot be claimed from anonymous probes. Publication requires the complete
local gate; historical exceptions on other PRs do not apply here. Its own
nonblocking admission is also subject to the foreign heavy-lock holder.

### Current Blockers

* Actual lock holder observed: PID3869238, `python3`, `/tmp/ama-rpi-heavy.lock`.
  No queued build, foreign-process interruption or release polling.
* Cost query failed HTTP429; one alternative stable-API explicit-period query
  failed `RBACAccessDenied`/Unauthorized. No role/auth/session change attempted.
* Supported Single-mode/no-new-revision recovery cannot be established from
  official revision documentation; do not improvise mode/traffic exceptions.

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
* Cloud writes require current sanitized all-in headroom/reserve/remaining
  liabilities and bounded exposure. Fresh operation authority is not evidence
  of an amount; unknown cost blocks cloud actions.

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
* On actual rollout/config/startup/asset failure: activate previous revision and
  verify old digest/readiness/traffic; no second image revision.
* Original critique and independent Review retained; complete exact-head local
  gate/receipt verified immediately before push or publication remains blocked.

## Sources

* .copilot-tracking/research/2026-10-28/employee-redeploy-research.md: C1-C4/W1-W4.
* infra/README.md: small employee prerequisite and historical API contract.
* src/README.md: full local deployment/publication gate.
* Caller request: finite operational approval and exclusions.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [ ] P01: Preserve and publish image

<!-- rpi:task id=P01-T01 -->
#### [ ] P01-T01: Capture baseline and build once

Use safe projections, external mode0700 directory, verify context has no local
untracked/ignored files, build with nonblocking heavy lock and immutable source SHA.
Current result: backup and unchanged-state verification complete under
`/tmp/ama-employee-redeploy-20261028.nbVE6l`; build blocked, task remains partial.

<!-- rpi:task id=P01-T02 -->
#### [ ] P01-T02: Push digest and restore ACR

Depends on P01-T01. Temporary one-IP deny-by-default route, expose token,
docker login/push, digest readback, finally restore exact original policy.

<!-- rpi:phase id=P02 -->
### [ ] P02: Update and verify once

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: One additive revision update and bounded checks

Depends on P01-T02. Verify no baseline drift immediately before write. Update
image/three env entries/min zero once; verify health, config, logs and assets.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Failure rollback or success readback

Depends on P02-T01. No failure retries that create revisions. On failure,
use a supported original-mode/traffic recovery route proven before mutation.
That prerequisite is currently unmet: cloud mutation is blocked. Do not leave
multiple mode or create another revision as an improvised workaround.

<!-- rpi:phase id=P03 -->
### [ ] P03: Review and publication

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Record evidence and independent Review

Reconcile plan/details/changes and run one fresh independent Review.
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

Original critique execution Complete, verdict Revise; no repeat.

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
* Coordinator must establish cost/recovery prerequisites and explicitly
  re-admit build after foreign lock ownership is free; no automatic polling.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-28/employee-redeploy-changes.md.
Permitted independent work: reference-only backup and blocked-execution evidence.
P01-T01 build, P01-T02 and P02 remain blocked; never mark runtime work complete.
Changes evidence and details reconciled for a Review of the blocked execution,
not successful implementation. Full gate not admitted because of foreign lock;
local evidence commit only, no push/PR without cleared publication gate.
