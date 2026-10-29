<!-- markdownlint-disable-file -->
# RPI Plan: Nominal replay pacing

## Task Metadata

* Task ID: pr-508-nominal-pacing
* Task slug: iot-nominal-pacing-508
* Planning status: Ready; original Revise critique resolved directly
* Plan date: 2026-10-29
* Phase details: .copilot-tracking/details/2026-10-29/iot-nominal-pacing-508-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/iot-nominal-pacing-508-plan-critique.md

## Executive Summary

Separate replay scheduling time from fault-injected observation time. Carry a
required nominal_at datetime on each Frame, retain it through duplicate creation
and publisher snapshotting, then compute scheduling intervals from it.
Payload schema, bytes, references and intentionally reordered observations stay unchanged.

### User Decisions and Requirements Highlights

* Fix one finding on existing PR #508, with targeted local checks and a commit, never a push.

### What You May Not Know

* Slots 3/4 currently select payload rows 2/5, causing 86.4 seconds instead of
  28.8 seconds at speed 1000. The regression will exercise the actual Pacer
  with virtual time, so it checks deadline/scaling without real-time delays.
* No full publication gate is claimed: its full API suite conflicts with the
  explicit validation limit. Coordinator retains publication responsibility.

### Unresolved Decisions or Blockers

* No implementation blocker; independent critique executed once, PC-001 resolved.

## User Decisions and Requirements

* Run research, plan, implement and review with dated tracking artifacts.
* Work on feat/iot-consumer-110 in this worktree for PR #508.
* Carry nominal time separately, preserve reordered observation timestamps,
  add the suffix publisher regression in the existing test file.
* Source in src/, tests outside packages; no mvp edits or Azure.
* Pull/rebase first; use origin/main for rubric latest.json.
* Use /tmp/mv; Ruff check/format and mypy in core/API; relevant unittest
  modules with requested PYTHONPATH, not full API discovery.
* Commit with Conventional Commit and Copilot trailer; do not push.

## Goals

* Restore nominal 8-hour pacing for consecutive suffix slots independently of faults.
* Preserve existing fault simulation and run safety controls.

## Scope and Non-Goals

* In scope: Frame, replay constructors, publisher frame copy and schedule, existing
  core/API tests, core/API replay README paragraphs, dated RPI records, rubric replacement.
* Non-goals: new CLI/config, payload fields/schema versions, SDK/Pacer redesign,
  unrelated findings, whole API suite, cloud use or publication.

## Functional Requirements

* Each generated Frame carries its nominal UTC datetime from origin plus slot cadence.
* Duplicate frames retain identical nominal time; equal slots across devices have no model delay.
* Publisher snapshots nominal time and uses it for positive inter-frame model spacing.
* Payload timestamps remain fault-injected and wire bodies/reference hashing unchanged.
* Burst skips model-time spacing while actual send rate admission remains enforced.

## Non-Functional Requirements

* No optional nominal-time fallback to observation time.
* Maintain strict typing and current formatting conventions.
* Regression uses virtual time and fake SDK clients; no credentials, private data or network.

## Acceptance Criteria

* Replay(out_of_order, first_slot=3, end_slot=5) sends both messages within a
  simulated 60-second budget at speed 1000; send instants differ by 28.8 seconds.
* Sent bodies exactly match the intentionally swapped rows 2/5 from clean replay,
  whose observed_at values remain 24 hours apart.
* Core tests establish nominal timestamps for default/custom origin and cadence,
  suffix equality and all existing fault modes including duplicate metadata.
* Requested static checks and relevant core/API unittest modules pass.
* One independent critique and one independent post-implementation Review are recorded.
* All requested changes and original dated evidence are committed, no push.

## Implementation Context Record

| Context item | Current artifact or record |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-29/iot-nominal-pacing-508-research.md, executed / Ready |
| Plan | .copilot-tracking/plans/2026-10-29/iot-nominal-pacing-508-plan.md |
| Phase details | .copilot-tracking/details/2026-10-29/iot-nominal-pacing-508-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-29/iot-nominal-pacing-508-plan-critique.md, executed / Revise, PC-001 resolved |
| Changes record | .copilot-tracking/changes/2026-10-29/iot-nominal-pacing-508-changes.md, implementation-owned |
| Continuation | Automatic full loop requested; no routine phase prompts |

## Sources

* Research C1-C5: frame generation, constructors, publisher and actual Pacer behavior.
* src/core/tests/test_sensor_stream.py and src/api/tests/test_iot_stream.py: owned regression fixtures.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve nominal scheduling through replay and publication

* Intent: separate scheduling metadata from observation faults.
* Dependencies: completed research and critique disposition.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add nominal metadata and publisher suffix regression

* Update all three Frame construction sites; derive nominal time from spec origin/cadence.
* Use nominal_at in HubPublisher interval calculation; preserve burst/rate/deadline logic.
* Add at most two new unittest methods in existing core/API test files, extend
  current fault/suffix assertions as needed. Exact removals: none.
* Test ownership: core tests own generation semantics; API tests own actual publication/pacing.
* Canonical targets: sensor_stream.py, iot_stream.py, their existing tests.
  Generated targets: none. Semantic coverage: nominal slot metadata; regression
  coverage: suffix scheduling plus unchanged faulted payload.

<!-- rpi:phase id=P02 -->
### [x] P02: Document, validate and hand off

* Intent: establish bounded engineering evidence and retain publication controls.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update guides and execute exact scoped checks

* Explain nominal_at and fault-independent spacing in existing component READMEs.
* Restore latest.json from origin/main as requested.
* From each project run /tmp/mv/bin/ruff check ., ruff format --check ., and mypy.
* From src/core run test_sensor_stream, test_sensor_consumer and test_dependency_rule.
* From src/api run test_iot_stream, test_sensor_ingestion and test_dependency_rule.
* Set PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
* Preserve failures and corrections in changes evidence; no full API suite.
* Reconcile implementation evidence for one subsequent independent Review and
  commit with required identity/trailer. Review/commit are lifecycle handoff
  obligations, not prerequisites of this implementation task's completion.
* Any material in-scope Review finding blocks a successful fix handoff; preserve
  the adverse outcome and route correction to later work without repeating Review
  or returning to implementation in this task. Unrelated findings may be deferred.

## Dependencies

* /tmp/mv existing tooling and installed distributions; install only upon a real missing dependency failure.
* Existing constructed sensor stock and SDK mocks, no network/cloud dependencies.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
| --- | --- | --- |
| One executed critique, original verdict Revise, PC-001 | Resolved directly | P02-T01 now explicitly blocks successful completion for material in-scope Review findings. The compatible blocked-handoff option is accepted; post-Review correction within this task is rejected under the one-pass RPI contract. No user decision or repeat critique. |

## Follow-Up Items

* Coordinator must satisfy publication/hosted/human gates before push or merge;
  broader validation is excluded from this bounded local run.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-29/iot-nominal-pacing-508-changes.md
* Implementation: P01/P02 complete with requested checks passed; ready for
  one independent Review followed by commit-only handoff.
* Remaining implementation question: none.
