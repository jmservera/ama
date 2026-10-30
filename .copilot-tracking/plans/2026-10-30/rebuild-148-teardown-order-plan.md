---
title: Rebuild teardown dependency plan
description: Bounded correction for the Front Door managed environment dependency on PR 511
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Task Metadata

* Task ID: pr-511-teardown-order-2026-10-30
* Task slug: rebuild-148-teardown-order
* Planning status: Complete; implementation validated, Review Conformant and local commit persisted.
* Plan date: 2026-10-30
* Phase details: .copilot-tracking/details/2026-10-30/rebuild-148-teardown-order-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-30/rebuild-148-teardown-order-plan-critique.md

## Executive Summary

Move the Front Door profile into teardown priority 1, ahead of the managed
environment at priority 2. This removes its managed Private Link origin before
the target environment, preserving the existing fixed-map sorter and safety
checks. Add a dependency-chain regression and assert the advertised dry-run
order. Document the contract, run the requested component checks, obtain one
independent Review and commit locally.

### User Decisions and Requirements Highlights

* Continue on feat/rebuild-148 for PR #511, Refs #148; no push or Azure access.
* Use /tmp/mv for Ruff, formatting, mypy and orchestrator tests.

### What You May Not Know

* The existing SQLite rehearsal does not include Front Door and therefore
  could not detect this bug. The dedicated regression must include it.
* /tmp/mv lacks the orchestrator distribution and its editable core points to
  another worktree. Install the current local packages after that observed
  import failure; do not rely on foreign source.
* Historical publication blockers and original Review outcomes remain
  unchanged. This local correction is not a full publication-gate receipt
  or Azure/whole-issue acceptance.

### Unresolved Decisions or Blockers

* No unresolved implementation decision. PC-001 asserted a /tmp prohibition
  not present in the parent execution context. Preserve the critique unchanged,
  reject that unsupported restriction here, and run the caller-required checks.

## User Decisions and Requirements

* Fix the supplied Copilot finding: Front Door profile must precede its target
  managed environment in teardown; distinct priorities or an explicit dependency
  are acceptable.
* Add a regression test under src/orchestrator/tests.
* Run the full dated Research, Plan, Implement and Review loop.
* Validate with ruff check, ruff format --check, mypy and orchestrator tests in
  /tmp/mv.
* No Azure access. Commit locally with a Conventional Commit and
  Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>; do not push.

## Goals

* Deterministically remove the Front Door consumer before its environment.
* Prevent regression on both the teardown executor and authoring-only report.

## Scope and Non-Goals

* In scope: rebuild.py priority map, test_rebuild.py regressions, directly related
  orchestrator README wording and dated RPI records.
* Non-goals: new Azure adapter, dependency-graph framework, changing canonical
  safety rules, fixture resource count, infrastructure definitions, unrelated
  historical findings, issue closure, push or live validation.

## Functional Requirements

* FR1: profile priority 1 must precede environment priority 2 regardless of
  inventory sequence, ID name or mixed resource-kind casing.
* FR2: apps/jobs remain priority 0, WAF remains priority 3, budgets remain last;
  canonical admission and deletion confirmation remain unchanged.
* FR3: dry-run must advertise the same profile-before-environment relationship.

## Non-Functional Requirements

* Keep the existing integer-priority implementation and strict typing; no new
  dependency or test framework.
* Every requested check must exit 0 or be reported explicitly failed/blocked.
* Synthetic checks must not access Azure, private datasets or real models.

## Acceptance Criteria

* AC1: a failing-first test reproduces environment-first behavior before the
  priority change and passes afterward.
* AC2: for forward and reversed inventory inputs, teardown deletes
  apps/jobs, then profile, then environment, then WAF; final inventory is empty.
  At least one profile kind uses mixed casing to exercise normalization.
* AC3: the existing CLI dry-run test asserts profile precedes environment.
* AC4: /tmp/mv Ruff lint, format check, strict mypy and complete orchestrator
  test discovery pass with current-worktree installed packages.
* AC5: independent critique and one post-implementation Review are recorded;
  implementation and original dated evidence are committed locally with the
  specified trailer. No push or Azure access.

## Implementation Context Record

| Context item | Current artifact or record |
| --- | --- |
| Plan | .copilot-tracking/plans/2026-10-30/rebuild-148-teardown-order-plan.md |
| Phase details | .copilot-tracking/details/2026-10-30/rebuild-148-teardown-order-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-10-30/rebuild-148-teardown-order-plan-critique.md; Complete / Revise, PC-001 rejected with rationale below |
| Relevant research | .copilot-tracking/research/2026-10-30/rebuild-148-teardown-order-research.md; C1-C6 |
| Changes-record role | .copilot-tracking/changes/2026-10-30/rebuild-148-teardown-order-changes.md, implementation-owned |
| Planning execution and readiness | Complete; all planned work now evidenced and locally committed |
| Continuation context | Full loop complete; automatic parent at Follow-up with no child selected |

## Sources

* Dated research C1-C6: reproduced ordering, Bicep origin target, existing
  MemoryBackend, fixture gap and component validation contracts.
* User's quoted PR #511 finding and local-only full-loop request.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and regress the teardown dependency

* Intent: observable deterministic consumer-before-target ordering.
* Dependencies: completed Research and independent critique disposition.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add failing-first ordering coverage

* Add one dedicated test using resource(), Inventory and MemoryBackend, plus
  a profile/environment assertion in the existing dry-run test.
* Run test_rebuild.py on the original priority map and retain the failure.
* Details: P01-T01 in the phase-details artifact.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Correct the profile tier and document the contract

* Change only profile priority 2 to 1; keep environment 2, apps/jobs 0 and WAF 3.
* Update the existing source-only rebuild README section, maintaining its local
  simulation and no-Azure-adapter limitations.
* Rerun focused tests. Depends on P01-T01.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate, independently review and commit locally

* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute component validation and reconcile evidence

* Install this worktree's core/orchestrator into /tmp/mv after the observed
  missing-package failure.
* From src/orchestrator run /tmp/mv/bin/ruff check .,
  /tmp/mv/bin/ruff format --check ., /tmp/mv/bin/mypy and
  PYTHONPATH=../core/tests /tmp/mv/bin/python -m unittest discover -s tests -q.
* Record commands, exits, counts/skips, environment identities and diff review.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Execute one independent Review and persist a local commit

* Fresh independent reviewer assesses the bounded diff against this plan and
  test evidence; writes the original Review artifact.
* Route any findings as later work without repeating Review in this task.
* Resolve authenticated GitHub privacy-safe local email for author/committer.
  Commit only task files, no amendments, pushes or branch rewrites.
* Record local closeout; full external publication gate remains a later
  publication prerequisite, not claimed by this local-only task.

## Test Ownership and Change Budget

* Canonical source: src/orchestrator/src/zava_forward/orchestrator/rebuild.py.
* Canonical tests: src/orchestrator/tests/test_rebuild.py. Exact removals: none.
* Maximum additions: one new test method and assertions in one existing method.
* Generated targets: none. Local fixture resource count remains ten.
* Semantic coverage: consumer-target and profile-WAF/app-job dependencies,
  mixed-case normalization, forward/reversed inventory order, actual executor.
* Regression coverage: both new pair and dry-run assertion fail on original
  priorities; requested complete component checks preserve existing behavior.

## Dependencies

* Current-worktree editable packages and existing pinned Ruff/mypy in /tmp/mv.
* No Azure credentials, cloud tools, browser or real SQL needed for the bounded
  in-memory sorting regression and existing local component checks.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
| --- | --- | --- |
| One independent critique: Complete / Revise; PC-001 High, claimed /tmp operations prohibited | Rejected as unsupported in the parent context and conflicting with the explicit caller environment | No parent execution restriction prohibits /tmp; existing Python and pip probes there succeeded. Keep the requested /tmp/mv checks and run them, recording actual failures if any. The critique explicitly performed no validation; its original wording remains unchanged. |

* No second critique. The code/test plan received no design findings.
* This disposition grants no new permission: it follows the actual parent
  execution boundary and explicit caller requirement rather than importing a
  worker assertion as authority. Validation remains unproven until executed.

## Follow-Up Items

* None newly discovered. Preserve earlier refresh/full-gate and original CLI
  failure-evidence findings outside this local correction.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-30/rebuild-148-teardown-order-changes.md.
* Ready next task: none in this bounded task; parent at Follow-up.
* Boundaries: local-only commit, no push/Azure, no publication acceptance claim.
* Final reconciliation: all P01/P02 tasks complete; requested lint, format, mypy
  and 69 orchestrator tests pass. Independent Review Complete / Conformant,
  no findings. Local implementation/evidence commit: 574954e0.
* AC1-AC5 proven for the bounded local task. No remaining source work, amendment
  or unresolved design decision. Publication and Azure acceptance remain outside
  this outcome; no push occurred.
