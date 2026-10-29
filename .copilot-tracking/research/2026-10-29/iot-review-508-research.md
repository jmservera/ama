<!-- markdownlint-disable-file -->
---
title: PR 508 IoT review corrections research
description: Focused cancellation, supplied pacing limits and high-rate pacing investigation
ms.date: 2026-10-29
---

## Research Brief

Fix the three caller-supplied Copilot findings on open PR #508 for the coordinator.
Scope: `src/api/src/zava_forward/api/iot_stream.py`,
`src/core/src/zava_forward/core/synthetic/sensor_stream.py`, their existing
outside-package tests, and directly related documentation. No `mvp/`, Azure,
push, full API suite, dependency changes or unrelated refactoring.
Output mode: convergence, preparing a surgical implementation plan.
Criteria: cancel and observe cleanup tasks even when shutdown is interrupted;
reject invalid supplied pacing limits before SDK creation; permit 100/s pacing
without weakening pause/deadline polling. Run requested Ruff, format, mypy and
focused unittest modules with `/tmp/mv`.

## Research Parameters and Direction Controls

Focused posture selected from named source targets and supplied failure evidence.
Trusted evidence root: `.copilot-tracking/research/2026-10-29/`.
No external research required: these are Python/asyncio contracts present in source.
Starting internal areas: both modules, `test_iot_stream.py`, `test_sensor_stream.py`,
project manifests/READMEs and earlier IoT evidence.
Prior-knowledge gate: caller findings are claims to verify against current branch.
Rebase completed first at clean intake: `883ed609`. PR remains OPEN against main.
User expressly authorized every phase and local commit, but no push.

## Extension Registry and Provenance

* Repository instructions: selected; src layout, fixture privacy, local identity,
  dated RPI evidence and publication gate apply.
* RPI research/plan/implement/review: selected for the requested lifecycle.
* Python foundational skill: not separately selected; existing project patterns,
  type/lint tooling and bounded changes suffice.
* Frontend/design/accessibility skills: skipped; no web surface changes.
* Research specialists: skipped; this is one tightly coupled low-volume code trace.

## User Participation and Research Decisions

Interaction unavailable and unnecessary: source targets, fixes, validation and
side-effect limits are explicit. Preserve original adverse evidence. Full
publication gate is outside this unpushed focused handoff and remains unmet.

## Research Cycle Log

Cycle 1 completed inline in Wider, Deeper, Contrarian order. No worker needed.

### Wider

The shared `_cleanup` is used by both receiver and publisher. `Pacer` accepts a
budget without calling budget validation, and its fields remain mutable.
Existing tests cover ordinary cancellation, blocked cleanup, actual send spacing,
pause/stop/deadline, but not cancellation after cleanup begins or exact high rates.
Reflection: shared-finally repair addresses both runners without duplicated logic;
test the real runner paths rather than only the helper.

### Deeper

Local `/tmp/mv/bin/python` probes confirmed a 100/s pacer's second admission at
0.05 seconds, not 0.01; negative/zero/NaN rates all pass the current upper-only
publisher check. An interrupted `_cleanup` left its shutdown coroutine pending.
Both probes completed with exit 0 and released their own tasks.
Reflection: regression tests need exact fake-clock thresholds and cancellation
after a shutdown-entry event, not arbitrary pre-shutdown cancellation sleeps.

### Contrarian

Considered waiting for cancelled shutdowns with `gather`: rejected because an SDK
may suppress cancellation, defeating the time allowance. Considered shielding
cleanup: rejected because caller cancellation must not leave the original waiter
and close tasks unowned. Instead, use a synchronous `finally` that cancels any
unfinished task and registers observation on every task. Keep the existing
normal timeout/failure error. Preserve actual CancelledError on interrupted cleanup.
Rate comparison must be positive and upper-bounded, which also rejects NaN.
Deadline finite checking rejects NaN/infinities; expired finite deadlines remain
ordinary runtime stops. When paused, ignore an already elapsed target and poll at
min(50 ms, deadline remainder), avoiding a zero/negative sleep loop.
Reflection: these alternatives cover material failure modes within caller scope.

### Parent Synthesis and Re-entry Decision

Accepted C1-C3 and the caller's surgical fixes; C4-C5 define appropriate existing
test surfaces. No unresolved design decision. Further cycles would repeat the same
source contracts. Re-enter only for a failing regression or material critique.

## Evidence Log

* C1: `src/api/src/zava_forward/api/iot_stream.py:173`:
  cleanup awaits `asyncio.wait` before any cancellation/observation.
* C2: `src/api/src/zava_forward/api/iot_stream.py:357`:
  supplied control is checked only with upper bounds after validating a different budget.
* C3: `src/core/src/zava_forward/core/synthetic/sensor_stream.py:256`:
  unconditional 50 ms poll ignores a nearer send target.
* C4: `src/api/tests/test_iot_stream.py:685`:
  existing shutdown timeout case is not interrupted during cleanup.
* C5: `src/core/tests/test_sensor_stream.py:227`:
  fake-clock tests provide deterministic pacing prior art.

## Findings Mapped to Questions and Evidence

* Q1 answered by C1/C4: both runners share the vulnerable await; test cancellation
  inside client shutdown (and credential close for receiver), with late exception
  observation and bounded return.
* Q2 answered by C2: check finite deadline and numeric, finite positive rate within
  the validated budget before factory invocation. Different valid stricter limits
  remain allowed.
* Q3 answered by C3/C5: include target remainder in active sleeps; deterministic
  25/50/100 per-second cases must produce exactly 1/rate spacing, with nominal wait,
  pause, stop and deadline behavior preserved.

## Alternatives and Decision State

Selected shared-finally cancellation/observation, entry validation and nearer-target
sleep. Reject shielded/unbounded cleanup, scheduler replacement and Pacer-wide
budget validation: they broaden or undermine the requested contract. Do not select
a new SDK lifecycle or architecture.

## Open Questions, Risks, and Residual Uncertainty

Cancellation cannot forcibly terminate an SDK coroutine that suppresses cancellation;
the local guarantee is bounded runner return plus cancellation and eventual observation.
No live SDK/Azure evidence is requested or inferred.

## Planning Readiness

Ready. Research disposition: executed, complete. All three questions answered;
evidence paths and local probe outputs checked. No implementation in Research.
Publication and live acceptance remain separate, not blockers to local fixes.
