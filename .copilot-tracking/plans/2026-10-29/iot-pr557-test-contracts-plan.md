---
title: PR 557 IoT test contracts plan
description: Test-only correction of live profile parameter and resource-name coverage
ms.date: 2026-10-29
---
<!-- markdownlint-disable-file -->

## Task Metadata

* Task ID: pr557-test-contracts-2026-10-29
* Task slug: iot-pr557-test-contracts
* Planning status: Ready; original Revise critique resolved directly
* Phase details: .copilot-tracking/details/2026-10-29/iot-pr557-test-contracts-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/iot-pr557-test-contracts-plan-critique.md

## Executive Summary

Add a compiled live-parameter contract and replace the live consumer-group
suffix assertion with an evaluated complete resource-name assertion. Reject
wrong-hub and wrong-group mutations without changing infrastructure behavior.
Keep all source edits in infra/tests/test_iothub_module.py, then run requested
local validation, independently review once and commit locally.

### What You May Not Know

The local build-params command emits both templateJson and parametersJson,
allowing comparison to the independently compiled live template. The live
profile is not a main deployment environment. Azure CLI is used only as a
local Bicep compiler; no Azure account or service operation is required.
Ruff is absent from system Python; restore it only after that observed failure.
Full publication gates are not implied by this local-only task.

## User Decisions and Requirements

* Run git pull --rebase first, completed with no changes on the requested branch.
* Complete Research, Plan, Implement and Review with dated tracking artifacts.
* Fix only the two named Copilot test findings on PR #557.
* Validate from infra with unittest discover -s tests -p 'test_iothub*',
  parameter tests, and Ruff on touched Python.
* Commit locally; do not push, use Azure or hand-edit rubric scores.

## Goals

Detect changes to approved live parameters, referenced template and complete
consumer-group parentage.

## Scope and Non-Goals

One test file plus original dated RPI evidence. No Bicep, bicepparam, production,
documentation, scorecard, deployment or remote-write changes.

## Functional Requirements

* Invoke local az bicep build-params against iot-hub-live.bicepparam; assert
  success before parsing JSON.
* Assert parsed templateJson equals self.live and parametersJson contains
  exactly name iot-cutover-test-rzsrg, location uksouth, skuName B1, unitCount 1.
* Evaluate consumer-group name with self.values(self.live) and compare exactly
  to fixture/events/api-consumer. Use this same assertion for negative mutations.

## Non-Functional Requirements

Reuse compiler, fixture and evaluator conventions. No new dependency manifests,
general-purpose abstractions or cloud validation. Tests must run with zero skips.

## Acceptance Criteria

* A different using template or changed approved parameter value fails coverage.
* A different hub with the same suffix and a different group both fail.
* Requested IoT suite, main parameter contracts and touched-file Ruff pass.
* Exactly one final-candidate critique and one post-implementation Review are
  preserved. All implementation and evidence is committed locally.

## Sources

.copilot-tracking/research/2026-10-29/iot-pr557-test-contracts-research.md,
evidence C1-C6 and W1; current user request.

## Implementation Context Record

Research executed / Ready. Critique executed once, original Revise verdict,
PC-001 resolved directly. Implementation evidence is recorded at
.copilot-tracking/changes/2026-10-29/iot-pr557-test-contracts-changes.md.
Independent Review executed once, Complete / Conformant, no findings.
Local commit a272edfc6c2cbbdcd18da3c4bb92564603c417d8 verified. All tasks complete.
User explicitly requested each phase;
no continuing automatic session.

## Test Ownership and Change Budget

Canonical owner: infra/tests/test_iothub_module.py. Generated targets: none.
Removals: none. Maximum additions: three test methods and one narrow assertion
helper. Semantic coverage: compiled template/parameters and full evaluated name.
Regression coverage: wrong hub and wrong group. Existing main parameter loops
remain unchanged. Required parameter selectors:
test_bicep_policy.BicepPolicyTests.test_parameter_examples_keep_api_scaled_to_zero
and test_bicep_policy.BicepPolicyTests.test_committed_environment_parameters_compile_and_match_the_contract
(confirm class name before execution).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Strengthen live test contracts

Dependency: research C1-C6 and critique disposition.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Assert live compiled parameters and referenced template

Compile and parse the profile using existing subprocess conventions. Compare
the whole emitted template and exact four parameter entries.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Assert full evaluated consumer-group name

Replace suffix-only coverage, extract only the shared assertion needed for
negative tests, and reject wrong hub and wrong group.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate, independently review and commit

Dependency: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run requested selectors and Ruff

Capture commands, counts and zero-skip results. Review diff for test-only scope.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Preserve independent Review and commit locally

Independent Review runs once after implementation. Classify every finding against
the requested contracts: unresolved in-scope acceptance failures mean blocked or
incomplete delivery, never success. Route out-of-scope work separately and do not
repeat Review. A checkpoint commit alone does not establish acceptance.
Configure privacy-safe repository-local email from
authenticated account, preserve all original evidence and commit with trailer.
Do not run publication gate or push; publication is explicitly excluded.

## Dependencies

Existing local Azure CLI/Bicep compiler and Python unittest evaluator.
Ruff must be available before validation is complete.

## Critique Disposition

Critique executed once, original verdict Revise, one Medium finding PC-001.
Resolved directly: P02-T02 in this plan and phase details now requires explicit
acceptance-linked Review disposition and prohibits successful completion with
unresolved in-scope blockers. Original critique remains unchanged.

## Follow-Up Items

* None.

## Handoff

P01 and P02-T01 complete; requested validation passes without skips.
Independent Review Complete / Conformant, no findings; local implementation and
original evidence commit a272edfc6c2cbbdcd18da3c4bb92564603c417d8 verified.
All P01/P02 markers complete. Final tracking reconciliation is a separate
local evidence-only commit, not a new source candidate or repeated Review.
No unresolved design decision. Changes record path is specified above;
phase details use the same P01/P02 task IDs.
