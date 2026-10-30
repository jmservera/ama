---
title: Capacity browser import correction changes
description: Correction cycle 1 implementation evidence, Refs 523
ms.date: 2026-10-30
---

## Scope and Current State

Task 523-correction-1; full approved correction plan complete, including local
commit after one critique, parent disposition and one independent Review.
Prior RPI outcomes and publication/live blockers remain unchanged.

## P01: Dependency Boundary

Baseline import-blocked discovery reproduced: one loader error caused by the
capacity harness's module-level Playwright import. The new
`test_scanner_suite_runs_without_playwright` was then run before the harness fix:
one test, one failure, with the expected ModuleNotFoundError at the same import.
This proves the added regression detects the actual defect.

The harness now postpones annotations and keeps Page/Request/Response/Route
imports type-only. Real expect/sync_playwright imports occur first in `check`,
before store access or server startup. Both scanner mocks use evaluate-only
list specs. One new subprocess regression executes the four existing tests,
asserts count/no skips/success/no loaded Playwright, then asserts browser
execution fails explicitly with Playwright denied. Existing scanner assertions
and browser flows are unchanged. The related README now names both harnesses.

## Plan Maintenance and Critique Disposition

PC-001's claimed `/tmp` prohibition is not active in the parent environment.
Preserve the exact caller lock protocol and original critique verdict; no new
critique or lock substitution. This is a direct evidence-bound disposition,
not a change to scope, architecture or required validation.

## Validation

Targeted green: five capacity tests passed in 0.167s, including the fresh-process
four-test scanner suite with Playwright denied and explicit execution refusal.
The exact shared heavy lock was acquired successfully, disproving PC-001's
environment premise.
Existing `/tmp/ama-capacity-523-venv` has the pinned tools. Caller PYTHONPATH
selects current-worktree source ahead of older editable installations.
An explicit pre-check confirmed API server and core SQL modules resolve inside
this worktree.

### First Full Attempt: Incomplete Existing Environment

The existing environment was insufficient for the current full suite:
1350 tests in 479.664s, one failure (current source-tree distribution metadata
reported no version), one loader error (missing azure.eventhub), 318 opt-in skips.
Ruff passed; all 61 formatter-covered files were already formatted. Mypy
reported seven missing/untyped Azure SDK imports in existing IoT files.
The capacity tests passed. No source defect was identified in this correction.
These results are retained, not reclassified as a pass.

An actual missing-dependency failure now justifies dependency restoration.
Create a dedicated correction venv rather than mutate the older shared venv,
and install the current core, agents and API dev distributions with pip. This
also restores generated current-source metadata. Preserve all manifest pins;
do not add overrides, skips, runtime dependencies or uv. Rerun the exact requested
full checks under the same mandated shared lock.

### Dedicated Environment Restoration

The shared lock was acquired again with the exact 600-second wait protocol.
Created `/tmp/ama-577-correction1-04d75329-venv` and installed current
`src/core`, `src/agents` and `src/api[dev]` with pip under that lock.
Azure Event Hub/IoT SDK imports and API version metadata now pass an explicit
pre-check. Capacity plus version targeted tests: eight passed in 0.156s.
Full discovery and the three static checks were then started in the restored
environment. No shared venv, dependency manifest or application source was
changed by environment repair.

### Final Requested Validation: Passed

The restored-environment command exited 0, under
`flock -w 600 /tmp/ama-rpi-heavy.lock`. All commands ran from `src/api` with
`PATH=/tmp/ama-577-correction1-04d75329-venv/bin:$PATH` and the exact caller
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`:

| Command | Result |
| --- | --- |
| `python3 -m unittest test_capacity_browser_check test_version -q` | Eight passed, 0.156s. |
| `python3 -m unittest discover -s tests -q` | 1377 tests, 487.774s, OK, 318 opt-in skips. |
| `ruff check .` | All checks passed. |
| `ruff format --check .` | 61 files already formatted. |
| `mypy` | No issues in 117 source files. |
| `git diff --check` | Passed. |

The 318 existing opt-in skips are recorded, not browser/SQL/live acceptance.
The new capacity regression runs without skips and fails on the original code.
No live Azure, sign-in, secret, uv or remote-write action was used.

## Remaining Work and Follow-ups

Implementation, required checks, independent Review and local commit are complete.
Source remains frozen as reviewed. Only tracking closeout is recorded afterward.
No push. Full exact-head publication gates and owner live verification stay
outside this correction and are not claimed satisfied.

## P02-T02: Independent Review

The single independent Review executed Complete / Conformant at
`.copilot-tracking/reviews/logs/2026-10-30/capacity-browser-import-correction-523-review.md`.
No source defects were found. Low RV-001 routes inherited publication/live
acceptance to separate follow-up work. No implementation or repeat Review was
started. Only parent marker/state and local commit administration follow.

## P02-T03: Local Commit and Final Administration

Committed implementation and original dated RPI evidence locally as
`7cc45330c7e768c0a5c955644ae4dac577e35a03`
(`fix(api): keep capacity unit discovery browser-free (Refs #523)`).
Before committing, `gh api user` returned the authenticated account ID/login.
Repository-local identity was configured and the actual commit verified with
author and committer `8036360+jmservera@users.noreply.github.com`, plus:

```text
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

The implementation commit left a clean worktree. This tracking-only follow-up
records completed markers/state without amending the implementation commit or
changing source after Review. No push or remote update was performed. Original
critique and Review remain unchanged; full publication/live gates are still open.
