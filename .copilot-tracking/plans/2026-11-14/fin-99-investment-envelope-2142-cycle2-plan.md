<!-- markdownlint-disable-file -->
# RPI Plan: Cycle-2 Fix for Issue #99 / PR #1739 `sys.modules` Test Bootstrap

## Task Metadata

* Task ID: fin-99-investment-envelope-2142-cycle2
* Task slug: fin-99-investment-envelope-2142-cycle2
* Planning status: ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-cycle2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/fin-99-investment-envelope-2142-cycle2-plan-critique.md

## Executive Summary

This Cycle-2 plan resolves the 40 downstream `src-core` CI `unittest discover` errors/failures on PR #1739 (Issue #99). In Cycle-1, both `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py` executed a module-level bootstrap that deleted every `zava_forward` and `zava_forward.*` module from `sys.modules` whenever `zava_forward.core.exposure_limits` had not yet been imported (`_loaded is None`). During alphabetical `unittest discover`, earlier test modules (`test_bulk_edits.py`, etc.) had already imported `zava_forward.core.store` and its exception classes (`ConflictError`, etc.) without eagerly importing `exposure_limits`; deleting `zava_forward.*` mid-discovery split module and class identities across earlier and later test modules (`test_taskqueues.py`, etc.). This plan replaces that bulk eviction in **both** test files with a targeted, namespace-safe bootstrap that never touches `zava_forward.core.store` or any sibling `zava_forward.*` module, evicts `zava_forward.core.exposure_limits` (and its cached attribute on `zava_forward.core`) **only** when `_loaded is not None` and its resolved file path lies outside `_CORE_SRC`, and adds a focused regression test verifying `store` / `ConflictError` identity preservation across both unloaded and external-path bootstrap states.

### User Decisions and Requirements Highlights

* Do NOT delete all `zava_forward.*` modules when `_loaded is None` in `src/core/tests/test_issue_99_acceptance.py`, and inspect/fix `src/core/tests/test_exposure_limits.py` so neither file performs bulk `sys.modules` eviction.
* Record the Cycle-2 fix in `.copilot-tracking/` (including `.copilot-tracking/{changes,reviews}/`).
* Validate in `src/core` with `python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .`, and `PYTHONPATH=src:tests python3 -m unittest tests/test_bulk_edits.py tests/test_issue_99_acceptance.py tests/test_exposure_limits.py tests/test_taskqueues.py -q`, plus commit cleanly on `feat/fin-99-investment-envelope-2142` with the required `Co-authored-by` trailer without pushing.

### What You May Not Know

* `src/core/tests/test_exposure_limits.py` contained the exact same `if _loaded is None or ...: del sys.modules[_mod]` loop as `test_issue_99_acceptance.py`; fixing only `test_issue_99_acceptance.py` would leave the identical CI regression active one file later.
* In Python 3.12, `from zava_forward.core import exposure_limits` checks the bound `exposure_limits` attribute on `sys.modules["zava_forward.core"]` before consulting `sys.modules`, and PEP 420 `_NamespacePath` objects have no `.insert()` method (`AttributeError`), so targeted eviction when `_loaded` is outside `_CORE_SRC` must also call `delattr(core_pkg, "exposure_limits")`, assign `__path__` as a list slice only if `_core_dir` is not already first, and call `importlib.invalidate_caches()`.

### Unresolved Decisions or Blockers

* None for Cycle-2 `src/core` delivery. External Board ratification of Zava North Homes `OD-12` and `OD-15` thresholds remains an organizational prerequisite (`Refs #99`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run a Cycle-2 RPI fix (research, plan, implement, review) for Issue #99 / PR #1739 in `/home/azureuser/source/ama-demo-wt/feat-99-investment-envelope-2142` on branch `feat/fin-99-investment-envelope-2142` targeting `feat/demo-233-same-home-tensions-0825` (source: user prompt).
* In `src/core/tests/test_issue_99_acceptance.py`, do NOT delete all `zava_forward.*` modules when `_loaded is None`; only evict `zava_forward.core.exposure_limits` when `_loaded is not None` and not relative to `_CORE_SRC` (refreshing `zava_forward.core` namespace state as needed), never wiping `zava_forward.core.store` or unrelated `zava_forward.*` modules (source: user prompt).
* Check `src/core/tests/test_exposure_limits.py` as well and remove bulk `sys.modules` eviction there too (source: user prompt, Research `C2`).
* Record the Cycle-2 fix in `.copilot-tracking/{changes,reviews}/` alongside the Cycle-2 research, plan, details, critique, and session state artifacts while preserving historical Cycle-1 RPI artifacts (source: user prompt, repo RPI retention instructions).
* Validate in `src/core` using `python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .`, and `PYTHONPATH=src:tests python3 -m unittest tests/test_bulk_edits.py tests/test_issue_99_acceptance.py tests/test_exposure_limits.py tests/test_taskqueues.py -q`, plus verify bare worktree `unittest` discovery still resolves `exposure_limits` to `_CORE_SRC` (source: user prompt, Cycle-1 `C8`).
* Commit cleanly on `feat/fin-99-investment-envelope-2142` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` and do NOT push (source: user prompt).

## Goals

* Preserve module and class identity (`zava_forward.core.store`, `ConflictError`, `FinanceMixin`, etc.) across all test modules in `unittest discover`.
* Retain worktree-local `zava_forward.core.exposure_limits` resolution under both `PYTHONPATH=src:tests` (CI) and bare `python3 -m unittest` in multi-worktree environments.
* Lock regression coverage proving `zava_forward.core.store` and `ConflictError` identity survive the bootstrap under both unloaded (`_loaded is None`) and external-module (`_loaded` outside `_CORE_SRC`) states.

## Scope and Non-Goals

### In Scope

* `src/core/tests/test_issue_99_acceptance.py`: Replace bulk `sys.modules` deletion with targeted single-module `exposure_limits` bootstrap and add focused regression test for `zava_forward.core.store` / `ConflictError` identity preservation and stale-origin eviction.
* `src/core/tests/test_exposure_limits.py`: Replace bulk `sys.modules` deletion with the matching targeted single-module `exposure_limits` bootstrap.
* `.copilot-tracking/`: Cycle-2 research, plan, phase details, plan critique, changes, review, and session state artifacts.

### Non-Goals

* Changing `src/core/src/zava_forward/core/exposure_limits.py` or `src/core/README.md` (already conformant from Cycle-1).
* Mutating shared `~/.local` editable installs or modifying `src/api`.
* Pushing to remote or rewriting existing commits.

## Functional Requirements

* Module-import bootstrap in `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py` shall prepend `_CORE_SRC` to `sys.path` (calling `importlib.invalidate_caches()` when `sys.path` changes) and leave `sys.modules` completely untouched whenever `zava_forward.core.exposure_limits` is not yet loaded (`_loaded is None`) or already resolves inside `_CORE_SRC`.
  * Observable acceptance criteria: Importing `test_bulk_edits`, `test_issue_99_acceptance`, `test_exposure_limits`, and `test_taskqueues` in one `unittest` process keeps `sys.modules["zava_forward.core.store"]` and `store.ConflictError` identical before and after both Issue #99 test modules load, with 0 test errors or failures.
* When `zava_forward.core.exposure_limits` is already present in `sys.modules` (`_loaded is not None`) with `__file__` missing or resolving outside `_CORE_SRC`, the bootstrap shall evict only `zava_forward.core.exposure_limits` from `sys.modules`, remove any bound `exposure_limits` attribute on `sys.modules.get("zava_forward.core")`, safely ensure `zava_forward` and `zava_forward.core` `__path__` entries begin with `_CORE_SRC` without calling `.insert()` on PEP 420 `_NamespacePath`, and call `importlib.invalidate_caches()`, without removing any other `zava_forward.*` module.
  * Observable acceptance criteria: Injecting a synthetic external `zava_forward.core.exposure_limits` module while `zava_forward.core.store` is loaded causes the bootstrap to reload `zava_forward.core.exposure_limits` from `_CORE_SRC` while `sys.modules["zava_forward.core.store"]` and `store.ConflictError` remain the exact same objects (`is`).

## Non-Functional Requirements

* Strict typing, lint/format cleanliness, ordered multi-module `unittest` compatibility (`PYTHONPATH=src:tests`), and bare worktree `unittest` isolation for the Issue #99 test modules in `src/core`.
  * Objective threshold or evaluation condition: Zero errors from `python3 -m mypy`, zero diagnostics from `python3 -m ruff check .`, zero formatting diffs from `python3 -m ruff format --check .`, and 100% pass rate on `PYTHONPATH=src:tests python3 -m unittest tests/test_bulk_edits.py tests/test_issue_99_acceptance.py tests/test_exposure_limits.py tests/test_taskqueues.py -q`, `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q`, and bare `python3 -m unittest tests/test_issue_99_acceptance.py tests/test_exposure_limits.py -q` in `src/core`.
  * Observable acceptance criteria: Every validation command exits `0` with zero errors or failures.

## Acceptance Criteria

* Neither `src/core/tests/test_issue_99_acceptance.py` nor `src/core/tests/test_exposure_limits.py` iterates over `sys.modules` to delete `zava_forward` or sibling `zava_forward.*` modules.
* Test ownership and scope lock: canonical test targets are `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py` (generated targets: `none`; test removals: `none`; maximum new test methods added: `<= 2` focused regression tests in `test_issue_99_acceptance.py` verifying `store`/`ConflictError` identity preservation across unloaded and external-origin bootstrap states).
* `python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .`, `PYTHONPATH=src:tests python3 -m unittest tests/test_bulk_edits.py tests/test_issue_99_acceptance.py tests/test_exposure_limits.py tests/test_taskqueues.py -q`, `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q`, and bare `python3 -m unittest tests/test_issue_99_acceptance.py tests/test_exposure_limits.py -q` all pass 100% in `src/core`.
* Stage-sequenced closeout: `rpi-implement` writes `.copilot-tracking/changes/2026-11-14/fin-99-investment-envelope-2142-cycle2-changes.md`, `rpi-review` writes `.copilot-tracking/reviews/logs/2026-11-14/fin-99-investment-envelope-2142-cycle2-review.md`, and post-review orchestration configures privacy-safe `git config --local user.email "{id}+{login}@users.noreply.github.com"` via `gh api user` and creates one clean commit on `feat/fin-99-investment-envelope-2142` (`Refs #99` + `Co-authored-by` trailer, no push, leaving `git status --short` empty).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                                 |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-cycle2-plan.md                                                          |
| Phase details                    | .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-cycle2-phase-details.md                                               |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-14/fin-99-investment-envelope-2142-cycle2-plan-critique.md (`Revise`; `PC-001`..`PC-003` applied directly) |
| Relevant research                | .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-cycle2-research.md                                                   |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/fin-99-investment-envelope-2142-cycle2-changes.md is created by `rpi-implement`; `.copilot-tracking/reviews/logs/2026-11-14/fin-99-investment-envelope-2142-cycle2-review.md` is created by read-only `rpi-review`; final local commit runs post-review after privacy-safe `gh api user` email setup |
| Planning execution and readiness | Complete and implementation-ready (`ready`); all single-pass critique findings resolved                                                    |
| Continuation context             | Confirmed automatic RPI Agent continuation to `rpi-implement`                                                                              |

## Sources

* .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-cycle2-research.md: Evidence `C1`-`C6` reproducing the CI failure and proving Python 3.12 PEP 420 parent-attribute and `_NamespacePath` behavior.
* src/core/tests/test_issue_99_acceptance.py: First bulk `sys.modules` eviction site (`C1`).
* src/core/tests/test_exposure_limits.py: Second bulk `sys.modules` eviction site (`C2`).
* .github/workflows/src-ci.yml: Hosted `src-core` `python -m unittest discover -s tests -v` runner (`C4`).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Replace bulk `sys.modules` eviction with targeted `exposure_limits` bootstrap and validate multi-module `unittest` discovery

* Intent: Eliminate `zava_forward.*` class-identity splits across `unittest discover` while preserving worktree-local `exposure_limits` import resolution and adding focused regression coverage.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update module-import bootstrap in `test_issue_99_acceptance.py` and `test_exposure_limits.py` and add identity-preservation regression test

* Requirement and evidence: User prompt Requirement 1; Research `C1`, `C2`, `C3`, `C5`, `C6`.
* Expected result: Both test files evict only `zava_forward.core.exposure_limits` (plus `delattr` on `zava_forward.core` and safe `__path__` slice refresh) when `_loaded is not None` and outside `_CORE_SRC`, never touch `zava_forward.core.store` or sibling modules, and `test_issue_99_acceptance.py` includes a focused regression test verifying `store` / `ConflictError` identity preservation across unloaded and external-origin states while restoring module state cleanly in `finally`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-cycle2-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Run `src/core` static analysis, ordered multi-module `unittest`, and full `src/core` test discovery verification

* Requirement and evidence: User prompt Requirement 3; Research `C4`, `C5`, `C6`.
* Expected result: `python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .`, `PYTHONPATH=src:tests python3 -m unittest tests/test_bulk_edits.py tests/test_issue_99_acceptance.py tests/test_exposure_limits.py tests/test_taskqueues.py -q`, and full `src/core` `unittest discover -s tests -q` exit `0` with 0 errors/failures.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-cycle2-phase-details.md

## Dependencies

* Python 3.12 toolchain (`mypy`, `ruff`, `unittest`) in `src/core`: required to verify static types, formatting, and multi-module discovery.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass critique `PC-001` [High] | Applied directly | Aligned Plan NFR and Acceptance Criteria with `P01-T02`: multi-module and full-suite `unittest` commands use `PYTHONPATH=src:tests` (matching CI / user prompt), while bare worktree isolation is verified via `python3 -m unittest tests/test_issue_99_acceptance.py tests/test_exposure_limits.py -q`. |
| Single-pass critique `PC-002` [Medium] | Applied directly | Updated `P01-T01` regression test spec to use `getattr(store_before, "ConflictError")`, `setattr`/`delattr` on `core_pkg`, and a non-`/tmp` fixture path (`str(_CORE_SRC.parent / "foreign_fixture" / "exposure_limits.py")`) so strict `mypy` and Ruff `S108`/lint checks pass cleanly. |
| Single-pass critique `PC-003` [Medium] | Applied directly | Clarified stage-sequenced artifact ownership (`changes/` in `rpi-implement`, `reviews/` in read-only `rpi-review`) and post-review single commit with privacy-safe `gh api user` noreply `git config --local user.email`, `Refs #99`, and `Co-authored-by` trailer (no push). |

## Follow-Up Items

* Surface `liquidity` / `covenant` minimum floor findings (`f.minimum ?? f.maximum` in `panels.js` `exposureNotice`) and `pause_signal.decision_owner` in the web Finance workbench UI (`src/api`): carried forward from Cycle-1 (`src/core`-only scope).
* Record actual Zava North Homes Board-ratified capital envelope, liquidity/covenant thresholds, and downside tolerances (`OD-12`, `OD-15`): external human governance input outside repository code (`Refs #99`).
