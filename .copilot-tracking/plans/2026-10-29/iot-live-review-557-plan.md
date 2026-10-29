---
title: PR 557 live IoT review correction plan
description: Surgical compiled-target regression tests and single-call exercise guidance
ms.date: 2026-10-29
---

## Task Metadata

* Task ID: pr-557-review-corrections
* Task slug: iot-live-review-557
* Planning status: Ready; independent critique Complete / Pass
* Research: .copilot-tracking/research/2026-10-29/iot-live-review-557-research.md
* Details: .copilot-tracking/details/2026-10-29/iot-live-review-557-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/iot-live-review-557-plan-critique.md

## Executive Summary

Add a compiled live-diagnostics assertion helper and mutation tests that reject
wrong hub scope and workspace. Correct the bounded exercise guide to authorize
one publisher call only and remove advice to retry uncertain deliveries.
No runtime or Bicep change is necessary: current wiring is already correct.

### What You May Not Know

Publisher pacing is per call, not exercise-wide accounting. One-run guidance
must exclude concurrent calls and other instances/processes. The prior cycle's
publication gate failed; local tests do not establish publication or live
acceptance. Ruff is absent; install it in an external task-owned environment
after the confirmed missing-module failure, without changing project manifests.

## User Decisions and Requirements

* Run all four RPI phases and preserve dated evidence.
* First run git pull --rebase; completed on the clean active PR #557 branch.
* Fix compiled diagnostic target coverage and prove changed targets are rejected.
* Restrict the exercise to one call with no retry without separate owner approval.
* Validate IoT discovery from infra and Ruff check/format on touched Python.
* Commit locally; no push, no Azure, no hand edits to rubric scores.

## Goals

Prevent silent diagnostic retargeting and remove unsafe exercise retry advice.

## Scope and Non-Goals

Canonical source targets: infra/tests/test_iothub_module.py and src/api/README.md.
Generated targets: none. Evidence only under dated .copilot-tracking paths.
Do not modify Bicep, runtime quota behavior, receiver replay semantics, rubric
scores, existing historical evidence or unrelated knowledge-base content.

## Functional Requirements

* Assert exactly one live diagnostic setting, its complete intended hub scope,
  exact log-cutover-test workspace expression, and existing metrics/log settings.
* Positive assertions must pass on compiled Bicep. Independent deepcopy
  mutations must reject a different hub and a different workspace.
* Document ONE publisher.run call for the entire approved bounded exercise,
  excluding repeated/concurrent calls across instances/processes. On uncertainty,
  stop and retain evidence; any retry needs separate owner approval/accounting.

## Non-Functional Requirements

Keep test style consistent with existing assertion helpers and subTest mutations.
Preserve all existing tests and categories. No dependency or runtime changes.

## Acceptance Criteria

* AC1: live compiled diagnostic helper checks full scope and destination.
* AC2: scope-only and workspace-only mutations fail that same helper.
* AC3: guide retains the two-message, 1/s, 60s and calendar cutoff limits while
  explicitly limiting the entire exercise to one call; no unsafe retry advice.
* AC4: requested IoT discovery passes without skips; touched Python passes Ruff
  check and format --check. Record actual commands/results.
* AC5: independent critique and post-implementation Review are preserved;
  implementation/evidence are committed locally with no push/Azure/score edits.

## Sources

Research C1-C5 and the owner-supplied findings. Existing production diagnostic
helper/mutations establish the local testing pattern.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct test coverage and exercise guidance

Dependency: completed research and independent candidate critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add compiled live diagnostic assertions and target mutations

Test ownership: IotHubModuleTests in infra/tests/test_iothub_module.py.
Removals: none. Maximum additions: one assertion helper and two test methods
(positive and mutation, with scope/workspace subtests); move existing live
category checks into that helper to avoid duplicate ownership.
Semantic coverage: full compiled scope/workspace; regression coverage: original
categories and changed-target rejection. No generated files.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Restrict bounded exercise and uncertain-delivery guidance

Edit both relevant README paragraphs; preserve wider receiver recovery semantics.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate, independently review and commit locally

Dependency: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute requested checks and reconcile evidence

From infra: python3 -m unittest discover -s tests -p 'test_iothub*'.
Run Ruff check and Ruff format --check against the touched Python only.
Review Markdown/diff; preserve truthful failures, amendments and divergences.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Run one independent Review and commit locally

Record original Review execution and outcome without re-review loops.
Resolve GitHub privacy-safe local commit identity before committing.
After committing, attempt the repository-required complete local gate with
nonqueued shared-lock admission and fresh external evidence. Missing prerequisites
or a foreign lock block the gate, not the independent local fix. Do not repair
unrelated gate/tooling failures or delete existing ignored inputs. No publication.

## Dependencies

Existing local az bicep compiler (baseline 18 tests passed), Python, missing Ruff
to restore externally, GitHub account read access for privacy-safe commit identity.

## Critique Disposition

Exactly one independent critique executed, Complete / Pass, zero findings.
Artifact: .copilot-tracking/reviews/plans/2026-10-29/iot-live-review-557-plan-critique.md.
No finding dispositions or user decisions are required. Candidate is Ready.

## Follow-Up Items

* Prior full publication gate admission failure remains outside this two-finding
  correction. Any future publication needs fresh exact-head eligibility.
* Parent live identity/transport/SQL acceptance remains separately blocked and
  requires owner authority; this task performs no Azure operations.

## Handoff

Implementation record: .copilot-tracking/changes/2026-10-29/iot-live-review-557-changes.md.
P01 and P02-T01 are complete; source implementation is ready for one independent
Review. P02-T02 remains pending Review, local commit and gate attempt. Proceed
through the four requested phases; no push or ongoing follow-up session.
