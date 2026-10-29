---
title: Sensor scenarios PR 505 rebase plan
description: Reconcile current main without widening the original synthetic feature
ms.date: 2026-10-29
---

## Task Metadata

* Task ID: 505; slug: sensor-scenarios-190-rebase.
* Parent: 190 / sensor-scenarios-190.
* Planning status: Ready; single critique disposed.
* Details: .copilot-tracking/details/2026-10-29/sensor-scenarios-190-rebase-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/sensor-scenarios-190-rebase-plan-critique.md

## Executive Summary

Rebase the existing two-commit scenario feature onto fetched main, preserve
both documentation narratives and main-owned source/pin changes, then check
the merged behavior in /tmp/mv. Commit the candidate and dated RPI records;
the coordinator alone owns push and hosted CI.

### What You May Not Know

Main changes the underlying indoor model and fixture hashes. A conflict-free
rebase alone is insufficient: scenario outcomes and provenance need actual
regression checks. Original adverse Review and downstream/live limitations
remain unchanged.

### Unresolved Decisions or Blockers

None for implementation. Hosted CI and publication acceptance cannot be
completed without the explicitly prohibited push.

## Sources

* .copilot-tracking/research/2026-10-29/sensor-scenarios-190-rebase-research.md:
  Ready; evidence C1-C7 and W1.
* User request 2026-10-29: exact branch, rebase, ownership, validation and no push.

## User Decisions and Requirements

* Complete Research, Plan, Implement and Review with dated tracking artifacts.
* Fetch/rebase origin/main on feat/sensor-scenarios-190 for draft PR 505.
* Preserve both sides' intent; use main's .github/rubric/* and scenario manifest.
* Recompute only stale pinned-source hashes; run test_scenario_manifest.
* Source remains in src/ and tests outside packages; no legacy application code.
* Run Ruff check/format, applicable core/API mypy and relevant unittest modules
  using /tmp/mv with source/test sibling paths.
* Never run full API discovery unless the specified flock probe succeeds.
* Use Conventional Commit with required Copilot trailer; no push or issue
  closing keywords. Refs #190 #192 #193 #194.

## Goals

* Clean local descendant of fetched origin/main with unchanged intended
  scenario scope and preserved upstream functionality.
* Reproducible, bounded local evidence for the coordinator.

## Scope and Non-Goals

In scope: branch rebase/conflicts, tightly coupled compatibility corrections,
pin integrity, related docs and RPI evidence.

Non-goals: new sensor/live/consumer features, web changes, issue closure,
draft promotion, hosted execution, remote writes and historical regrading.

## Functional Requirements

* Eleven synthetic cases still yield fifteen default per-check results,
  observations/truth separation and fixed-truth threshold sensitivity.
* New upstream generator/model behavior remains intact.
* Main-owned rubric and manifest are retained except necessary hash refresh.

## Non-Functional Requirements

* Project Ruff, format and mypy checks exit zero using existing configuration.
* Relevant unit selectors run using installed local namespace distributions;
  no private dataset, live service or new dependency is required.
* Conflict resolution does not edit original tracking evidence.

## Acceptance Criteria

* Rebase finishes; origin/main is an ancestor; no conflict markers or
  unmerged paths remain. No mvp/ source introduced.
* All selected checks pass or their genuine blocker is explicitly recorded;
  failed checks are not reported as successful.
* Four manifest hashes match exact source bytes and test_scenario_manifest passes.
* One independent critique and one post-implementation Review are recorded.
* Clean committed branch with privacy-safe identity and Copilot trailer; no push.
* Full-gate/publication and hosted/human gaps remain explicit, never fabricated.

## Test Ownership and Change Budget

Canonical source: src/core/src/zava_forward/core/synthetic/sensor_scenarios.py.
Canonical tests: src/core/tests/test_sensor_scenarios.py and existing sibling
sensor/manifest tests; API tests remain under src/api/tests.
Exact removals: none. Maximum new test modules: zero. Maximum additions:
two regression methods only if a rebase-coupled defect is reproduced.
No generated source targets. External temporary logs are validation output.
Semantic checks: exact case/check counts, truth separation and threshold
sensitivity. Regression checks: backfill/model/provenance, manifest and
dependency rule; API sensor/workbench contract.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Reconcile ancestry

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Rebase and resolve conflicts

Rebase onto b0364e4b326936715d69ab1d75040c4528282af7, preserve both docs
and incoming source changes, keep rubric/manifest equal to main initially.
Dependency: final critique dispositions.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate merged behavior

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Restore local installs and run scoped checks

Install current editable core/agents/API after reproduced missing import;
run Ruff/format/mypy from core/API. Run sensor/manifest/model/dependency unit
modules and API sensor/workbench selectors with sibling source/test paths.
Avoid full API discovery. Correct only reproduced rebase-coupled defects.
Dependency: P01.

<!-- rpi:phase id=P03 -->
### [x] P03: Prepare Review and commit handoff

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Record evidence and prepare independent Review

Reconcile checklist/details/changes and prepare a reviewable bounded delta.
The RPI wrapper then runs one fresh independent Review, records its outcome
and routes findings rather than repeating Review. It commits candidate and
dated original evidence with required identity/trailer, and attempts the
complete gate after commit only if a fresh heavy-lock probe succeeds.
Preserve unavailable capacity/prerequisites as publication blockers. Do not push.
Dependency: P02.

## Dependencies

* /tmp/mv Python 3.12 and pip-installed local distributions, with explicit
  source/test paths because its editable mappings are shared with other worktrees.
* Shared heavy lock for full-gate work; targeted tests do not require it.
* Coordinator must push rewritten branch and observe hosted checks separately.

## Critique Disposition

Critique execution Complete; original verdict Revise (one High finding).
Original critique is preserved unchanged.

| Finding | Disposition | Evidence and consequence |
| --- | --- | --- |
| PC-001 | Rejected: conflicts with caller-selected environment and unsupported parent restriction | Critique asserts an unspecified temporary-directory ban. No such restriction applies to the parent execution context; user explicitly selected /tmp/mv and /tmp/ama-rpi-heavy.lock. Existing Bash tools successfully accessed the interpreter and lock. Run actual checks and retain genuine failures instead of inventing a blocker. No historical original-task finding is regraded. |

## Follow-Up Items

* Original RV-001 execution-boundary dispute and RV-002-RV-004 downstream/live
  acceptance remain with their recorded owner/dependency; outside this rebase.
* Coordinator owns required complete publication gate, exact-head assessment,
  push and hosted CI if local prerequisites block this handoff.
* Shared heavy lock is currently held elsewhere (fresh probe exit 1); full
  gate remains unrun unless capacity becomes available before handoff.

## Handoff

Changes path:
.copilot-tracking/changes/2026-10-29/sensor-scenarios-190-rebase-changes.md.
P01-P03 complete; ready for one independent Review. Core/API static and
174 selected unit tests passed (one existing SQL skip), migration 25 passed.
Main remains b0364e4b after fresh fetch. No source compatibility changes.
Full publication gate remains unavailable while the shared heavy lock is held.
