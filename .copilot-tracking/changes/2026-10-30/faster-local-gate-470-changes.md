---
title: Faster local gate 470 changes
ms.date: 2026-10-30
---

## Metadata

Task ID: 470. Slug: faster-local-gate-470. Declared scope: full plan.
Plan: `.copilot-tracking/plans/2026-10-30/faster-local-gate-470-plan.md`.
Details: `.copilot-tracking/details/2026-10-30/faster-local-gate-470-phase-details.md`.

## Execution Status

In progress. First task P01-T01: document the existing runner benchmark.
Write boundary: `src/README.md` and this task's dated tracking evidence only.
No application, runner or test changes. P01/P01-T01 completed; P02/P03 pending.

## Execution Summary

Research verified that #475 already implements the requested functionality.
This continuation targets the remaining full timing evidence. Critique PC-001
requires explicit comparability, actual parallel admission and equal timing
boundaries; the planning parent applied it without a second critique.

## Validation Record

External evidence root: `/mnt/ama-rpi-gates/issue470-20261030-validation`.
Actual missing Ruff, mypy and distributions justified creating an external
venv and pip-installing existing core/agents/API dev dependencies. Installation
passed; pinned Ruff 0.17.1 and mypy 2.4.0 are available. Generated local build
outputs will be removed only at their exact task-created paths.

| Check | Result | Evidence |
| --- | --- | --- |
| Gate regressions | Passed, 35 tests in 11.897 s | External `gate-tests.log` |
| Gate Ruff lint/format | Passed, two files already formatted | Ruff 0.17.1, isolated existing runner configuration |
| Gate strict mypy | Passed, two files | mypy 2.4.0 |
| Diff whitespace | Passed | `git diff --check` |
| Required API bundle | Running under shared flock | External `api.log` |

Task-created build directories, egg-info and Ruff cache were moved to exact
external `generated/core`, `generated/agents`, `generated/api` and
`generated/ruff-cache` archives, not deleted or committed.
Pre-admission resource observation caps requested jobs 3 at 1; actual full
admission must still be recorded. This observation is not a parallel benchmark.

## Completed Work

P01-T01: `src/README.md` now documents serial/parallel full commands, internal
lock ownership, requested versus admitted jobs, identical acquired-to-sealed
timing, independent default-full verification, cache/order qualifications and
coordinator-owned PR recording. Existing partial/full rules remain unchanged.

## Implementation-Time Plan and Detail Updates

PC-001 was applied directly before implementation. No divergence, new
requirement, new test ownership or repeated critique was introduced.

## Blockers

Foreign heavy-lock ownership observed. Authorized 600-second admission wait
is pending; no foreign process/resource is interrupted or reused.

## Remaining Work

P02-T01, P02-T02, P03-T01. Full measurements are not yet available.

## Follow-Up Items

Coordinator-owned PR recording and final exact-head publication gates remain
outside the locally committed handoff.
