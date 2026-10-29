<!-- markdownlint-disable-file -->
# RPI Plan: IoT PR 557 main refresh

## Task Metadata

* Task ID: pr-557-main-refresh-2026-10-29
* Task slug: iot-pr557-main-refresh
* Date: 2026-10-29
* Planning status: Complete / Ready
* Details: .copilot-tracking/details/2026-10-29/iot-pr557-main-refresh-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/iot-pr557-main-refresh-plan-critique.md

## Executive Summary

Rebase the existing PR onto fetched main and resolve additive documentation
without losing either workstream. Preserve main's rubric and scenario manifest
exactly, retain IoT runtime and compiled-template safeguards, run affected
local checks and commit the complete dated evidence. No push or Azure change.

### What You May Not Know

PR #557 is already marked ready. Its ten unmerged commits include generated
scores that must not overwrite main. Existing local/live acceptance blockers
remain historical, and hosted CI cannot run on the new candidate until the
coordinator publishes it. A full publication gate is separate from this
local-only refresh.

## User Decisions and Requirements

* Execute Research, Plan, Implement and Review with dated tracking artifacts.
* Fetch and rebase `feat/iot-hub-live-140` onto main, retaining both sides' intent.
* Use main's `.github/rubric/*` and scenario manifest; revalidate pinned inputs.
* Source remains under `src/`, with project tests outside package directories.
* Use `/tmp/mv`, project Ruff/format/mypy and relevant unittest modules; full
  API discovery is prohibited unless a nonblocking heavy-lock probe succeeds.
* Do not create/modify Azure resources or push. Use a Conventional Commit,
  privacy-safe identity and the required Copilot coauthor trailer. Refs #140 #184.

## Goals

Produce a clean local candidate descended from reviewed main with preserved
IoT contracts, explicit validation results and an independent Review.

## Scope and Non-Goals

In scope: per-commit rebase conflicts, main-authoritative generated files,
directly coupled CI fixes, additive documentation and dated evidence.
Out of scope: live transport, deployment, full issue acceptance, hosted CI
claims, unrelated cleanup, follow-up implementation and remote operations.

## Functional Requirements

* Preserve publisher-only activation, routed receiver restriction, finite
  budgets and live compiled-template scope/SKU/unit/name/parameter assertions.
* Keep both index/log/infra documentation additions and main's canonical metadata.

## Non-Functional Requirements

No Azure state change, no private dataset, no new dependencies absent a missing
dependency error, no protection changes and no unowned cleanup.

## Acceptance Criteria

* Main SHA `8ee1b77f8983ddf39216da07ae60c63ef66431d6` is an ancestor; rebase
  finished with no conflicts or unexpected source differences.
* Main rubric directory and scenario manifest have no diff; branch IoT
  implementation/tests survive, and both documentation histories remain.
* Core/API Ruff check, format check and mypy pass; compiled IoT infrastructure
  tests, relevant sensor unittest modules and scenario manifest test pass.
  Failures must be resolved when task-coupled or reported as blockers.
* Changes artifact records actual commands, exits, skips and identities.
* One independent critique and one post-implementation Review are preserved.
* Local commit has requested message/trailer; no push is performed. Remote
  mergeability, hosted CI and publication are explicitly unverified.

## Sources

* .copilot-tracking/research/2026-10-29/iot-pr557-main-refresh-research.md C1-C8.
* src/README.md and .github/workflows/src-ci.yml: validation contracts.

## Implementation Context Record

Research Complete / Ready. Critique pending; no decision-critical gaps.
Changes record will be created during implementation:
.copilot-tracking/changes/2026-10-29/iot-pr557-main-refresh-changes.md.
Explicit full-loop parent continuation; no routine phase question needed.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Rebase and reconcile

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Replay the existing topic on main

Run requested rebase. Resolve each conflict using the complete three-way context.
Keep both additive sections; main's generated files win. Remove only duplicated
metadata introduced by reconciliation. No test removal or new test expected.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate the reconciled contracts

Depends on P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute targeted static, types and unittest checks

Core/API Ruff+format+mypy; offline infra IoT/Bicep parameter policy selectors;
API IoT/ingestion/stream/resident-sensors; core sensor-stream/consumer/manifest
and dependency boundaries. Do not run full API discovery in this bounded pass.
Record commands/results and repair only directly coupled failures.

<!-- rpi:phase id=P03 -->
### [ ] P03: Review and commit locally

Depends on P02.

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Independent Review and durable local handoff

Reconcile markers and changes evidence, run one independent Review against
original and rebased source identities, record its unmodified outcome, commit
the candidate/evidence and verify clean status and trailer. No second Review;
unresolved material findings block successful outcome and route to later work.

## Dependencies

Existing `/tmp/mv`, local offline Bicep, current branch and main ancestry.
No new cloud or package resources. Future publication requires its own current
exact-head full gate; this task neither publishes nor substitutes for that gate.

## Test Ownership and Change Budget

Tests belong to `infra/tests`, `src/core/tests` and `src/api/tests`.
Exact removals: none. Maximum new tests: zero for pure conflict reconciliation;
if a real coupled defect requires a regression, explicitly amend this plan
before adding it. Canonical runtime targets are current `src/` packages and
infra Bicep, never legacy source. Generated rubric/manifest targets equal main.
Semantic coverage is the existing compiled-template and synthetic transport
tests; no new live verification claim is allowed.

## Critique Disposition

Exactly one independent critique executed Complete / Pass, no findings.
Original artifact:
.copilot-tracking/reviews/plans/2026-10-29/iot-pr557-main-refresh-plan-critique.md.
No plan corrections or repeat critique required.

## Follow-Up Items

* Coordinator owns publication, fresh complete gate/exact-head assessment,
  hosted CI and human approval; they are outside the no-push task.
* Historical registry/adapter/live-to-SQL/resident-gauge approval remains open.

## Handoff

P01/P02 complete. One independent post-implementation Review executed
Complete / Conformant, no findings; P03-T01 local evidence commit remains.
All targeted checks passed without skips;
no source changes were necessary beyond additive conflict reconciliation.
No unresolved local source or validation blockers.
