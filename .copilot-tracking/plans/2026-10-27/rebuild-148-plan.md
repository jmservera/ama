<!-- markdownlint-disable-file -->
# RPI Plan: Repeatable rebuild authoring

## Task Metadata

* Task ID: 148
* Task slug: rebuild-148
* Plan date: 2026-10-27
* Planning status: Ready for source-only implementation
* Phase details: .copilot-tracking/details/2026-10-27/rebuild-148-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-27/rebuild-148-plan-critique.md

## Executive Summary

Author a checked rebuild/teardown sequence in the orchestrator package, a
zero-I/O dry-run, and a disposable synthetic SQLite rehearsal. Keep cloud
execution unavailable rather than guessing preservation, retention or tenant
authority. This delivers independently testable automation contracts, not a
completed Azure rebuild or issue closure.

### What You May Not Know

Budgets are not in the generic resource inventory. Locks/immutable audit
retention cannot be bypassed to manufacture an empty inventory. Current #138
and tenant setup helpers have distinct live acceptance gates.

### Unresolved Decisions or Blockers

No blocker to authoring. Live integration requires separately authorized
exact-resource preservation/destruction and tenant/credential operations.

## User Decisions and Requirements

* Run research, plan, implement, review in order; commit dated evidence.
* #148 authoring/local validation only; no deployment or deletion of ama.
* New code under src per ADR 0006; tests outside package.
* No secret/.env/private-data reads, uv, force-push or workflow-name changes.
* One draft PR to main; Refs #148 unless all acceptance is proved.
* Local unit tests; no --all; one scoped locked --changed only if large.

## Goals

* Encode mandatory ordering and fail-closed checkpoints once.
* Prove repeatable local from-empty execution and ordered teardown.
* Make unavailable Azure/tenant evidence explicit.

## Scope and Non-Goals

In scope: orchestrator engine and local adapter, tests, component runbooks.
Out of scope: live Azure adapter, shell hooks, cloud deployment/deletion, tenant
access, preserved private lineage restoration, real model invocation or approvals.
The lack of an Azure adapter is an explicit partial-delivery boundary, not a
claim that a simulation completes #148.

## Functional Requirements

* Rebuild requires empty generic and budget inventories; ordered steps include
  dependency bootstrap, versioned images, credential, SQL grants, generated
  synthetic seed, apps, auth, staff, health and restart persistence.
* Each operation has an independently invoked verification; stop immediately
  on failure. Never auto-rollback or hide partially completed operations.
* Teardown validates exact subscription/ama scope and known types, rejects
  locks/unknown resources, orders children and dependencies, verifies each
  deletion and finally both inventories. Never delete group, purge retained
  data or remove retention/locks.
* Dry-run prints a typed declarative sequence only, no reads/writes/network.
* Local rehearsal owns a fresh temporary directory/SQLite state only; synthetic
  seed/staff are generated, never loaded from ZF_DATA or a caller data file.
* Reports label every backend result synthetic/local and never imply health,
  image, model, tenant or Azure success.

## Non-Functional Requirements

Standard library only; strict types and existing lint/format conventions.
No subprocess, credential handling, arbitrary execution or environment data
access in this first adapter. Resource parsing must fail on malformed or
cross-scope IDs before mutation. Deterministic plan ordering and bounded sizes.

## Acceptance Criteria

Local delivery criteria (not the issue's cloud criteria):

* Checked rebuild trace matches all mandatory stages and halts on bad verification.
* Dependency teardown covers child/parent, apps/environment, PE/network,
  Foundry project/account and AMPLS/component ordering plus separate budgets.
* Temporary SQLite seed/staff survive close/reopen and teardown ends empty.
* CLI dry-run is read-only and local rehearsal reports scope honestly.
* Negative tests prove fail-closed scope, unknown types, changed inventories,
  lingering deletes/budgets, errors and no private/default data access.

Issue mapping: all four criteria remain partial pending real helper integration
and authorized disposable Azure test. Tick none based on rehearsal.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-27/rebuild-148-research.md.
Implementation record: .copilot-tracking/changes/2026-10-27/rebuild-148-changes.md.
Primary planner owns these plan/details; critique writes only its own artifact.

## Sources

* infra/README.md, From-empty rebuild observed on 2026-10-12.
* ADR 0002, exercise delivery; ADR 0006, src layout.
* BRD CON-007/AC-086 and PRD CON-009/AC-057: local checks are not live acceptance.
* Research C1-C7 and W1; #138/#136 dependency acceptance not assumed.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Author and validate bounded automation

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement checked sequencing and local rehearsal

Targets: src/orchestrator/src/zava_forward/orchestrator/rebuild.py and
src/orchestrator/tests/test_rebuild.py. Details: P01-T01.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Document limits and run local validation

Targets: infra/README.md and src/orchestrator/README.md. Details: P01-T02.

## Dependencies

P01-T02 depends on P01-T01. #138 live deployment integration remains deferred.
Install editable core/orchestrator distributions after observed missing-package
failure; API/agents only if API validation needs them.

## Test Ownership and Validation Lock

Canonical owner: src/orchestrator/tests/test_rebuild.py (one new test module,
maximum 30 tests); removals none. Production target one new module; no generated
committed payloads. Semantic sequencing and SQLite persistence tests plus CLI
regressions. Run orchestrator full existing suite, Ruff and mypy; unchanged API
does not need unrelated full discovery. No heavy gate for this local-only tool.

## Critique Disposition

One critique executed, original verdict Revise preserved.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 High | Applied directly | P01-T01 now enumerates all runbook stages and separate identity-bound postchecks; local simulations stay labelled |
| PC-002 Medium | Applied directly | P01-T01 requires exact canonical remaining records in both inventories before/after each delete |
| PC-003 Medium | Rejected, unsupported premise | No supplied parent environment instruction prohibits /tmp; explicit owner request itself specifies /tmp lock and external output directories. Owned TemporaryDirectory is retained, no arbitrary cleanup path |

No human decision needed; no second critique.

## Follow-Up Items

* Authorized Azure adapter integrating #138 and existing SQL/auth/staff helpers,
  exact inventory/preservation/retention approval and a disposable cloud test.
  Outside current no-deployment authoring scope; owner selects later work.

## Handoff

P01/P01-T01/P01-T02 complete for authoring/local scope. Orchestrator suite:
68 tests pass, zero skips; Ruff check/format and mypy pass. Ready for the
single independent Review. Whole-issue live acceptance remains unmet.
