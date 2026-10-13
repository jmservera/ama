<!-- markdownlint-disable-file -->
---
title: Five Retrofit Assistants Implementation Plan
ms.date: 2026-10-13
---

Task: five-retrofit-assistants-2026-10-13

## Executive Summary

Extend the existing MVP with five registered assistants, on request and through
bounded proactive checks. SQL owns tasks and claims; the existing API remains
the write boundary. Outputs enter version-bound, role-owned human review,
never controlled workflow transitions. Update the PRD/ADR and build a new
image on the retained data and existing Azure services. Continue #68.

## User Decisions and Requirements

* Add the five reactive/proactive assistants to PRD and ADR and build a version.
* Complete autonomously, resolve ordinary choices and implement.
* Preserve the existing MVP/data lineage, actual AI/SQL/Azure exercise baseline
  and the earlier consolidated-PR direction.
* On 2026-10-13 the owner explicitly authorized the offered existing-app
  retained-data rollout and bounded QA: 10 calls, 126000 reserved tokens,
  one-hour expiry, proactive off, up to USD 5 incremental target. Token
  reservations do not guarantee exact billing. No merge, tenant changes or
  separate worker estate.
* The owner subsequently stops retained-data migration and explicitly permits
  wiping/recreating the exercise database from the existing synthetic generator.
  Enrich missing operational sections, including visits, using the requested
  hve-core-all:eval-dataset-creator. Preserve tenant role/identity bindings and
  app authentication; replaced synthetic domain is a new dated baseline.

## Evidence and Readiness

Research: .copilot-tracking/research/2026-10-13/five-retrofit-assistants-research.md.
Latest owner direction resolves the unanswered procedural intake. Target is
the existing application, not another deck or product. Existing requester-only
review and mutating funding drafts are not reusable unchanged.

The bounded planner could read but could not write; the parent authors its
resolved candidate directly. No planner contribution or critique is fabricated.

## Goals

Deliver usable stock, assessment, funding, works/resident coordination and
quality evidence assistants without weakening current controls.

## Scope and Non-Goals

Existing MVP backend/UI/tests, PRD, ADR 0002 and necessary ADR 0001 linkage,
MVP/operator documentation, knowledge index/log and delivery evidence.
No new worker estate, production approval, original/BRD/memory/regulatory
changes, presentation redesign or PR merge. Exercise database replacement
and synthetic-data enrichment are explicitly authorized exceptions to the
earlier no-reset/no-new-database boundary.

## Functional Requirements

* Five versioned registry contracts with roles, permitted sources, triggers,
  human reviewers and failure/manual paths.
* Reactive requests and proactive eligibility produce the same bounded,
  source/version-bound proposal; record invocation provenance separately.
* Durable deduplication, SQL-owned claim/lease lifecycle, bounded scans,
  retry/backoff and model-call limits; no process-local lock-only durability.
* API/service projections enforce roles. Review queues are role/owner scoped;
  review rechecks current source hash and permissions. Stale cannot be accepted.
* Every output has explicit AI/template/failure/unverified status and citations.
  Accept/edit/reject concerns the proposal only, not a domain approval.
* Existing case-card controls expose appropriate assistance and proactive work.

## Non-Functional Requirements

No model write credentials or external actions. Preserve safety routing,
ranking, consent, work release, grant state and QA independence. Use existing
SQL/AI adapters and generated data. No new dependency/tooling unless necessary.
Bound output, input, scan and invocation costs; fail explicitly and retain manual
case access. Preserve rollback and private configuration.

## Acceptance Criteria

* All five have real callable paths and demonstrated reactive/proactive rules.
* Unauthorized sources/tasks/reviews, stale/failed outputs, duplicate triggers,
  competing claims and restart recovery are tested.
* Every assist leaves controlled case/ranking/approval state unchanged.
* Current tests plus targeted tests pass; image builds and runs non-root.
* Real-platform evidence is revision/source/image linked: SQL persistence and
  actual model invocation, with failure/manual paths distinct. Human/business
  acceptance and measured value are not claimed.
* Documents describe delivered versus deferred capabilities truthfully.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Specify the five bounded assistants

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update PRD and ADR contracts

Define each assistant and invocation modes, map existing FR/AC obligations,
extend explicit acceptance criteria if needed, preserve approval state and
update index/log.

<!-- rpi:phase id=P02 -->
### [x] P02: Implement the specified assistants

Depends on P01. Whole phase owns only MVP runtime, UI, tests and MVP README;
it can run independently of the parent's live-platform inspection.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Implement shared runtime and UI

Registry, bounded evidence, durable task/claim storage, proactive checks,
reactive generation, role-owned proposal review and existing UI integration.

<!-- rpi:phase id=P03 -->
### [ ] P03: Validate and deliver the existing-platform version

Depends on P02. Parent owns platform rollout, Review and publication.

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Validate, build and publish

Targeted then existing suites; real image build and approved existing exercise
services; record version-linked evidence. Commit/push #68 with privacy-safe
identity. Preserve all unrelated and private files.

Owner-approved replacement: stop old-database assistant migration, enrich the
existing deterministic MVP generator without inventing approvals, and seed a
new exercise baseline. Correct Azure SQL ledger event-table DDL before fresh
startup. Verify populated operational sections (especially visits), retain
tenant staff bindings/auth, and compare assistant-only changes against the new
baseline rather than pretending the old domain remained unchanged.

## Test Ownership and Locked Boundary

Add mvp/tests/test_assistants.py and at most one new browser test file. Modify
only tightly coupled existing store/API/projection tests as necessary. No
test removals. Semantic coverage: five contracts, sources/roles/staleness and
proposal-only behavior. Regression coverage: existing draft/domain flows,
authentication, store backends and UI. No generated requirements lock change
unless a dependency is actually required.

## Critique Disposition

One independent critique executed; verdict Revise. PC-001 to PC-008 accepted
and applied as the following locked implementation obligations. No repeat.

* PC-001: durable unique proposal key (assistant/version, case, canonical
  intended proposal identity, permitted dependency signature), provenance
  distinct from key; changed intent cannot replay an earlier proposal when
  dependencies are unchanged. Test changed intent and reactive/proactive
  collisions. Pending/leased/ready/failed states, owner plus monotonic fencing
  token, database-time lease CAS, bounded attempts/backoff and lookup recovery.
  Late completion cannot win. Inference is bounded at-least-once, not
  exactly-once billing.
* PC-002: valid scoped operator authority/config before real automatic calls;
  bounded input/output, scan interval/size, active calls/attempts and durable
  shared allowance reservations. Timeout/missing usage retains liability.
  Preserve provider/model/usage envelope, never count missing usage as zero.
* PC-003: per-assistant source allowlist compatible with the recipient audience;
  independent service purpose, no requester impersonation. Recheck roles,
  ownership and source access on request, list/detail and review.
* PC-004: material dependency signatures include source IDs/content/document
  hashes and registry version. Review validates them and proposal version in
  its transaction/CAS. Stale, failed or unverified accept/edit is denied.
* PC-005: provider calls outside domain/database locks, bounded worker
  concurrency, independent connection ownership and interruptible lifecycle.
  Slow inference must not prevent ordinary case work.
* PC-006: additive idempotent SQLite/MSSQL migrations on retained data, startup
  concurrency serialization; old image can ignore new state. Disable worker/
  restore previous digest without deleting evidence or reseeding.
* PC-007: capture existing private config/identity/data/rollback fingerprints;
  build exact source, verify non-root/health, preserve existing SQL/AI/auth
  references and serving digest/revision. Record deployed assistant/usage,
  independent SQL before/after/restart and unchanged domain evidence.
* PC-008: distinct five-contract source/role/trigger/typed-output matrix; for
  each, reactive and eligible/ineligible proactive, failure/disabled/malformed
  and unchanged-state tests. Citations prove provenance, not semantic truth.

## Follow-Up Items

Human role/accessibility acceptance, calibrated task quality and paired benefit
measurement remain separate. Separate queue/worker infrastructure is deferred
unless this exercise demonstrates a material need.

## Handoff

Details: .copilot-tracking/details/2026-10-13/five-retrofit-assistants-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-13/five-retrofit-assistants-changes.md.
One post-implementation Review, then route residual work outside this task.
