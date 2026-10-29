---
title: PR 508 IoT review corrections plan
description: Surgical cancellation, pacing validation and high-rate replay corrections
ms.date: 2026-10-29
---

Task ID: pr-508-review-fixes-2026-10-29. Slug: iot-review-508.
Status: complete; independent Review Complete / Conformant; locally committed, no push.

## Executive Summary

Repair the shared cleanup ownership boundary, reject invalid supplied controls
before SDK creation, and sleep until the nearer active pacing target. Add
focused regressions to the two existing test files, update their owning guides,
run the requested checks, independently review once, and commit without pushing.
No new transport architecture, Azure action, full API suite or dependency change.

## Sources

`.copilot-tracking/research/2026-10-29/iot-review-508-research.md` C1-C5;
caller-supplied PR #508 findings; `src/api/README.md`, `src/core/README.md`.
Research disposition executed / Planning Readiness Ready. No evidence gap.

## User Decisions and Requirements

* Complete Research, Plan, Implement and Review with dated tracking artifacts.
* Continue `feat/iot-consumer-110` in this worktree; pull --rebase first, taking
  origin/main's rubric JSON copy.
* Source in src; tests outside packages in existing test files; no mvp or Azure.
* Put cleanup cancellation and observation in finally for both runners.
* Reject nonpositive/out-of-budget supplied rates and NaN deadlines before clients.
* Include active target remainder in pacing sleeps; preserve bounded paused polls.
* Use /tmp/mv; run Ruff check/format, mypy for core/API, relevant unittests only.
* Conventional Commit with required Copilot trailer; no push, coordinator owns it.

## Goals

G1: deterministic bounded task ownership during cancellation in cleanup.
G2: externally supplied pacing cannot weaken validated entry limits.
G3: supported 100/s cadence is not artificially restricted to 20/s.

## Scope and Non-Goals

Two production modules, their two existing test files, two owning READMEs,
origin/main rubric JSON restoration, dated RPI artifacts. No generated targets,
new test files, SDK redesign, Pacer-wide validation, frontend or remote writes.

## Functional Requirements

FR1: `_cleanup` cancels unfinished operations and attaches observation to all tasks
in a non-awaiting finally, on timeout and cancellation as well as success.
FR2: preserve `IOT_CLEANUP_FAILED` for ordinary timeout/failure and propagate caller
CancelledError when interrupted. Do not await cancellation-resistant SDK shutdown.
FR3: supplied deadline must be finite and not exceed the validated budget horizon.
Rate must be numeric, finite, positive and <= validated budget.max_per_second.
FR4: active sleeps bound by 50 ms, deadline remainder and target remainder; paused
sleeps remain bounded by 50 ms/deadline without spinning on elapsed targets.

## Non-Functional Requirements

Retain typing, fixed public error codes, original delivery/SQL/consent behavior and
global admission immediately before sends. No additional dependencies or cloud use.

## Acceptance Criteria

AC1: real receiver and publisher cancelled after entering shutdown promptly return
CancelledError; all close operations are cancelled and late errors observed.
AC2: invalid rates (-1, 0, NaN, infinities, bool, over-budget) and invalid deadlines
(NaN, infinities, over-budget) refuse with fixed error before any SDK factory call.
Valid stricter finite supplied controls remain usable.
AC3: fake-clock 25/50/100 per-second admissions advance exactly by 1/rate; short
nominal targets, pause past target, deadline and stop behavior remain covered.
AC4: requested project lint/format/mypy and relevant unittest modules pass.
AC5: one critique and one independent post-implementation Review are recorded.
Any blocking in-scope Review finding makes the handoff Not accepted and routes to
later work; do not claim successful completion while such findings remain open.
local commit contains original dated evidence and required trailer. No push.

## Test Ownership and Validation Lock

Core owns Pacer timing in `src/core/tests/test_sensor_stream.py`. API owns runner
cleanup and supplied control checks in `src/api/tests/test_iot_stream.py`.
Removals: none. Maximum additions: six test methods across those two files.
Canonical targets: the two source modules; generated targets: none.
Semantic coverage: runner propagation, task cancellation/observation, pre-client
validation and numerical timing. Regression coverage: existing modules preserved.
Commands in each project:
`/tmp/mv/bin/ruff check .`, `/tmp/mv/bin/ruff format --check .`,
`/tmp/mv/bin/mypy`.
Unittest environment from each project:
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`.
Core selector: `test_sensor_stream`; API selectors:
`test_iot_stream test_sensor_ingestion`. Never full API discovery.
Full publication receipt is not produced: this is a local, explicitly unpushed
handoff with focused validation. Coordinator must satisfy publication gates.

## Phase Checklist

<!-- phase: P01 -->
### P01: Regression-first corrections

* [x] P01-T01 Add focused regressions and record their failure before fixing source.
* [x] P01-T02 Apply shared cleanup finally, supplied limits and nearer-target sleep.

<!-- phase: P02 -->
### P02: Documentation and validation

* [x] P02-T01 Update the two owning README contracts and restore main rubric copy.
* [x] P02-T02 Run requested core/API static checks and relevant unittest modules.

<!-- phase: P03 -->
### P03: Independent Review and local handoff

* [x] P03-T01 Reconcile implementation evidence and execute one independent Review.
* [x] P03-T02 Record Review disposition and commit with privacy-safe identity/trailer.

Dependencies: P01-T02 after P01-T01; P02-T02 after P01-T02 and P02-T01;
P03-T01 after P02-T02; P03-T02 after P03-T01.

## Critique Disposition

Execution: complete. Original verdict: Revise (two Medium findings).
Artifact: `.copilot-tracking/reviews/plans/2026-10-29/iot-review-508-plan-critique.md`.

* PC-001 rejected as inapplicable: the worker cited a worker-local prohibition on
  /tmp writes absent from this parent execution's rules. Existing tempfile-based
  SQLite fixtures and caller-required /tmp/mv remain unchanged. No scratch
  environment redesign is needed or authorized.
* PC-002 applied in compatible form: blocking in-scope Review findings prevent
  an accepted handoff. Preserve original Review and route later work without
  another implementation/review loop, consistent with the one-pass RPI contract.
  No new user decision required.

Final readiness: Ready. Critique not repeated.

## Follow-Up Items

Coordinator publication/full exact-head gate and hosted/human approval remain
outside this no-push task; no live acceptance is inferred.

## Handoff

Details: `.copilot-tracking/details/2026-10-29/iot-review-508-phase-details.md`.
Critique target:
`.copilot-tracking/reviews/plans/2026-10-29/iot-review-508-plan-critique.md`.
Implementation changes target:
`.copilot-tracking/changes/2026-10-29/iot-review-508-changes.md`.
Do not implement until the one critique's compatible findings are disposed.
