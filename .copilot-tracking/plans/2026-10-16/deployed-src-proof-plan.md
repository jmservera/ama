---
title: Deployed src proof plan
ms.date: 2026-10-16
---

Task: issues-200-201-deployed-src-proof. Readiness: Ready after critique dispositions.

## Executive Summary

Honor private SQL policy, bootstrap the retained ama stack using the repository
wrapper, and execute initialization and smoke exclusively in its VNet. Capture
partial results honestly; tenant staff and owner cut-over approval stay separate.

## User Decisions and Requirements

* Refs #200 and #201; no closing keywords in PR body.
* AMA only; preserve resource group, pre-existing budget and private data.
* No public SQL, firewall requests, policy/tag bypass, peering or VM data-plane.
* ACR Tasks only; src image contexts; no legacy edits or local Docker.
* RPI evidence, tests for scripts, sanitized docs/JSON, log, push and PR.

## Goals

Prove src image deployment, private SQL initialization and restart persistence;
exercise health and API denial, authorized HTTP only where safely feasible.

## Scope and Non-Goals

Infrastructure/runtime proof only. No tenant changes, human roster invention,
live inference, product acceptance, private-data migration or owner approval.

## Functional Requirements

Explicit false public-access input must be honored in development. Run all SQL
commands and HTTP private smoke inside Container Apps. Use a dedicated SQL
initializer MI; grant API/import contained users without Graph lookup.
If existing tenant app credentials are unavailable, permit explicitly selected
bearer-only EasyAuth without a client secret, retaining issuer/audience checks,
trusted proxy and 401 denial. Do not claim a human sign-in or authorized HTTP pass.

## Non-Functional Requirements

Preserve existing dev defaults and browser login. All evidence excludes tokens,
subscription/tenant IDs and Entra object/client IDs. Deploy incrementally only.
No resource cleanup unless a broken resource was created in this execution.

## Acceptance Criteria

Each requested probe has Passed, Failed, Blocked or Not run plus evidence.
SQL remains Disabled, no firewall resource write occurs, private DNS resolves.
Capture image digests, job executions, revision status and persistence marker.
All owner checklist boxes stay unchecked. No unrelated files or resource writes.

## Phase Checklist

<!-- P01 -->
### P01: Private deployment and execution tooling

* [x] P01-T01: Correct development explicit-false switch; cover with compiled matrix.
* [x] P01-T02: Add bounded in-VNet proof runner and offline unit tests, with no secrets logged.
* [x] P01-T03: Add explicit bearer-only ingress option if needed; preserve browser default.

<!-- P02 -->
### P02: Azure execution

* [x] P02-T01: Build src images remotely, bootstrap using deploy.py and reviewed what-if.
* [x] P02-T02: Create dedicated initialization identity/job within ama; initialize SQL privately.
* [x] P02-T03: Deploy all images and run private health/denial/MI/restart probes or record blockers.

<!-- P03 -->
### P03: Evidence and delivery

* [x] P03-T01: Update pack, JSON, infra guide, index and append-only reference log.
* [x] P03-T02: Run scoped suites and prepare the single Review handoff; publish after Review.

## Test Ownership and Bounds

Existing infra suite owns deployment semantics. Remove no tests. Add at most
one runner test module and eight compiled/profile/auth tests. Runner unit tests
cover wrong network/URL, HTTP codes, idempotence and sanitized output using
fakes; Azure execution is semantic evidence, never replaced by mocks.
Canonical targets are src/infra source and the two existing evidence files.
Generated temporary job specifications and raw logs stay in session storage.

## Critique Disposition

Executed once; verdict Revise, all six compatible findings applied directly.

* PC-001: add `deployEnvironmentOnly` stage, no placeholder application.
* PC-002: inspect only sys.tables and dedicated sentinel before Store creation;
  reject unknown tables without application-data reads or writes.
* PC-003: initializer MI is admin by principal ID; API/import users use client
  SID (UUID little-endian), API reader/writer/ddladmin, import reader/writer.
  API-MI Store startup proves runtime grants separately from admin connection.
* PC-004: valid nonempty fictional case and application meta marker, post-restart
  API-MI Store read without seed file. No human staff bindings.
* PC-005: bearer-only uses current authenticated application client ID as
  identified audience; omit secret and token store, Return401, issuer validation.
  Test malformed token/forged principal denial; authorized HTTP remains separate.
* PC-006: build all four images and runner, capture digests and contracts before
  isolation. Every wrapper uses explicit orchestrator digest. No post-isolation
  repair build without demonstrated authorized path; report Blocked instead.

## Follow-Up Items

Human staff initialization requires privately supplied roster and tenant Graph
permissions. Managed identities are not human staff; never relax this boundary.
Other cut-over owner gates remain separate.
Authorized HTTP token acquisition returned 400. Do not weaken ingress or grant
MI a human staff role. Resolve approved tenant API/role prerequisites separately.
Skeleton worker acceptance, private-data attestation and owner sign-off remain
outside this bounded infrastructure proof. Delivery (commit/push/PR) follows
the single Review as an administrative action, not another implementation loop.

## Handoff

Research: `.copilot-tracking/research/2026-10-16/deployed-src-proof-research.md`.
Details: `.copilot-tracking/details/2026-10-16/deployed-src-proof-phase-details.md`.
Changes target: `.copilot-tracking/changes/2026-10-16/deployed-src-proof-changes.md`.
