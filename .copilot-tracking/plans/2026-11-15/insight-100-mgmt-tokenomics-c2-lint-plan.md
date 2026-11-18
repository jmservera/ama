---
title: "RPI Plan: PR #1792 c2 Ruff Format Remediation (Issue #100)"
description: "Implementation plan for Issue #100 PR #1792 c2 Ruff line-length=100 formatting fix across src/core and src/api"
ms.date: 2026-11-15
---
<!-- markdownlint-disable-file -->

## Task Metadata

* Task ID: issue-100-mgmt-tokenomics-c2-lint
* Task slug: insight-100-mgmt-tokenomics-c2-lint
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-plan-critique.md

## Executive Summary

This `c2` child plan resolves the sole hosted CI failure on `PR #1792` (`feat/insight-100-mgmt-tokenomics` at `d3a2c5405`, targeting `feat/demo-164-chat-grounding-provenance-0900` / `PR #1641`) for Issue `#100`. Commit `d3a2c5405` passed `8/10` CI jobs and passed `Unit tests and dependency-rule test` in both `src-core` and `src-api`, failing only Step 6 (`Lint`: `ruff check . && ruff format --check .`) because `tokenomics.py` and `progress.py` had been formatted at Ruff's repo-root default `line-length = 88` instead of the package-configured `line-length = 100` in `src/core/pyproject.toml` and `src/api/pyproject.toml`. Running package-scoped `python3 -m ruff format` on `src/core/src/zava_forward/core/tokenomics.py` (5 line-wrap hunks) and `src/api/src/zava_forward/api/progress.py` (1 call-wrap hunk) restores `10/10` `src-ci.yml` parity with zero AST or runtime behavioral changes, validated under the Focused tier (`ruff check .`, `ruff format --check .`, bare `mypy`, and Focused `unittest` suites) and committed locally on `feat/insight-100-mgmt-tokenomics` without pushing.

### User Decisions and Requirements Highlights

* Complete the full `c2` RPI loop (`research`, `plan`, `implement`, `review`) with dated `2026-11-15` `c2` artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews/logs`, `rpi-sessions`).
* Reformat `src/core/src/zava_forward/core/tokenomics.py` inside `src/core` and `src/api/src/zava_forward/api/progress.py` inside `src/api`, verifying `ruff check .` and `ruff format --check .` in both package directories.
* Run Focused unit tests and strict `mypy` type checks across `src/core` and `src/api`, then commit the 2 formatted Python files and all `.copilot-tracking/*-c2-*` artifacts locally with `Refs #100` and the Copilot `Co-authored-by` trailer without pushing.

### What You May Not Know

* In `d3a2c5405`, the new Issue `#100` test modules are named `src/core/tests/test_management_tokenomics_invariant_100.py` (6 tests, alongside `test_tokenomics_comparison.py`) and `src/api/tests/test_management_tokenomics_api_100.py` (2 multi-endpoint HTTP tests). Running `-p "test_tokenomics*.py"` alone in `src/core` skips `test_management_tokenomics_invariant_100.py`, and running `-p "test_management_tokenomics_100.py"` alone in `src/api` matches `0` tests. Validation therefore executes both the exact caller-listed commands and explicit `-p "test_*tokenomics*.py"` discovery (with `tests` on `src/api` `PYTHONPATH`) so every Issue `#100` test suite actually runs.
* `gh pr view 1792` confirms the checked-out PR branch in this worktree is `feat/insight-100-mgmt-tokenomics` (`d3a2c5405`), matching the existing worktree HEAD; commits stay on `feat/insight-100-mgmt-tokenomics` without branch creation or remote push.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`), writing dated `c2` artifacts under `.copilot-tracking/` (`research`, `plans` and `phase-details`, `reviews/plans`, `changes`, `reviews/logs`, `rpi-sessions`) for Issue `#100` (`PR #1792` `c2` lint/format fix) (user prompt).
* Format `src/core/src/zava_forward/core/tokenomics.py` and `src/api/src/zava_forward/api/progress.py` from within `src/core` and `src/api` respectively and verify `python3 -m ruff check .` and `python3 -m ruff format --check .` in each package directory (user prompt).
* Run Focused unit tests and `mypy` type-checks in `src/core` and `src/api` under the Focused validation tier (user prompt; `.copilot-tracking/research/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-research.md` `C7`, `C8`).
* Commit `src/core/src/zava_forward/core/tokenomics.py`, `src/api/src/zava_forward/api/progress.py`, and `.copilot-tracking/*-c2-*` locally on the checked-out PR `#1792` branch (`feat/insight-100-mgmt-tokenomics`) with `Refs #100`, privacy-safe GitHub noreply author/committer identity, and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`; do NOT push (user prompt; `.github/copilot-instructions.md`).

## Goals

* Restore `100%` package-local Ruff lint and format conformance (`line-length = 100`) in `src/core` and `src/api` matching `.github/workflows/src-ci.yml`.
* Preserve exact Python AST and runtime behavior across `zava_forward.core.tokenomics` and `zava_forward.api.progress`.
* Verify Focused-tier unit tests and strict `mypy` checks across `src/core` and `src/api` with non-zero executed test counts covering all Issue `#100` suites.
* Deliver a complete, auditable dated `c2` RPI tracking trail and leave a single clean local commit at frozen `HEAD` for coordinator review.

## Scope and Non-Goals

### In Scope

* Canonical Python targets: `src/core/src/zava_forward/core/tokenomics.py` and `src/api/src/zava_forward/api/progress.py` (generated targets: `none`).
* Test ownership lock: existing suites `src/core/tests/test_tokenomics_comparison.py`, `src/core/tests/test_management_tokenomics_invariant_100.py`, and `src/api/tests/test_management_tokenomics_api_100.py`; exact test removals: `none`; maximum test additions: `0` (pure AST-identical formatting change).
* Focused validation: package-scoped `ruff check .`, `ruff format --check .`, bare `mypy`, AST parse-equivalence check, and Focused `unittest` discovery in `src/core` and `src/api`.
* Complete `2026-11-15` `c2` RPI tracking artifacts under `.copilot-tracking/` and a single post-Review local git commit on `feat/insight-100-mgmt-tokenomics`.

### Non-Goals

* Semantic, algorithmic, or schema edits to `tokenomics.py`, `progress.py`, or any other module.
* Creating or modifying `pyproject.toml`, `.github/workflows/src-ci.yml`, Dockerfiles, SQL migrations, `src/api/checks/` browser scripts, or `src/api/src/zava_forward/api/web/` UI assets.
* Implementing deferred `c1` follow-up items (`RV-001`, `RV-002`, or `OD-51` governance closure).
* Rebasing, amending `d3a2c5405`, or pushing commits to `origin`.

## Functional Requirements

* FR-1: Package-scoped Ruff formatting in `src/core` and `src/api`.
  * Observable acceptance criteria: `(cd src/core && python3 -m ruff check . && python3 -m ruff format --check .)` exits `0` (`302 files already formatted`) and `(cd src/api && python3 -m ruff check . && python3 -m ruff format --check .)` exits `0` (`214 files already formatted`), touching only `src/core/src/zava_forward/core/tokenomics.py` and `src/api/src/zava_forward/api/progress.py`.
* FR-2: Complete dated `c2` RPI evidence trail and clean frozen local commit.
  * Observable acceptance criteria: All seven dated `c2` artifacts exist (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews/logs`, `rpi-sessions`) and are committed together with the two formatted Python files in one new commit atop `d3a2c5405` on `feat/insight-100-mgmt-tokenomics` containing `Refs #100` and the `Co-authored-by` trailer, with `git status --short` empty and zero remote pushes.

## Non-Functional Requirements

* NFR-1: Exact AST and behavioral invariance (semantic coverage).
  * Objective threshold or evaluation condition: `ast.dump(ast.parse(before), include_attributes=False) == ast.dump(ast.parse(after), include_attributes=False)` holds for both `tokenomics.py` and `progress.py`.
  * Operating condition or verification approach, if needed: Verified against `d3a2c5405:<path>` via `python3 -c` AST comparison after `ruff format`.
  * Observable acceptance criteria: Zero AST divergence between `d3a2c5405` and the formatted files.
* NFR-2: Focused static-typing and unit-test regression parity (regression coverage).
  * Objective threshold or evaluation condition: `mypy` reports `0` issues across all `src/core` and `src/api` files, and Focused `unittest` runs execute `test_tokenomics_comparison.py`, `test_management_tokenomics_invariant_100.py` (`6` tests), and `test_management_tokenomics_api_100.py` (`2` multi-endpoint HTTP tests) with `0` failures.
  * Operating condition or verification approach, if needed: Execute both the caller-specified commands and `-p "test_*tokenomics*.py"` selectors (with `tests` included in `src/api` `PYTHONPATH` and `-W error::ResourceWarning` on the HTTP suite).
  * Observable acceptance criteria: All `mypy` and `unittest` commands exit `0` with verified non-zero test counts covering all three tokenomics test modules.

## Acceptance Criteria

* `src/core/src/zava_forward/core/tokenomics.py` and `src/api/src/zava_forward/api/progress.py` are formatted with package-local Ruff (`line-length = 100`) and remain AST-identical to `d3a2c5405`.
* `(cd src/core && python3 -m ruff check . && python3 -m ruff format --check .)` and `(cd src/api && python3 -m ruff check . && python3 -m ruff format --check .)` both exit `0`.
* `(cd src/core && PYTHONPATH=src python3 -m mypy)` and `(cd src/api && PYTHONPATH=../core/src:../agents/src:src python3 -m mypy)` both exit `0`.
* Focused `unittest` discovery in `src/core` and `src/api` executes `test_tokenomics_comparison.py`, `test_management_tokenomics_invariant_100.py`, and `test_management_tokenomics_api_100.py` with `0` failures.
* All seven dated `c2` `.copilot-tracking/` artifacts (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews/logs`, `rpi-sessions`) are reconciled and committed with the 2 Python files on `feat/insight-100-mgmt-tokenomics` (`Refs #100`, privacy-safe noreply email, `Co-authored-by` trailer) with `git status --short` clean and `origin/feat/insight-100-mgmt-tokenomics` untouched at `d3a2c5405`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-plan.md                                                           |
| Phase details                    | .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-phase-details.md                                                |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-plan-critique.md with Pass disposition (`0` findings) |
| Relevant research                | .copilot-tracking/research/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-research.md                                                    |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-changes.md is created by implementation as its evidence record  |
| Planning execution and readiness | Complete; Ready for implementation                                                                                                       |
| Continuation context             | Active confirmed automatic RPI Agent parent continues to `Implement` after all planning gates pass                                       |

## Sources

* `.copilot-tracking/research/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-research.md`: Cycle 1 evidence (`C1`-`C8`) reproducing PR `#1792` Step 6 (`Lint`) failures, line-level Ruff diffs, and test-glob discovery checks.
* `.github/workflows/src-ci.yml`: Normative CI `Lint` (`ruff check . && ruff format --check .`) and `Type check` (`mypy`) steps executed with `working-directory: src/${{ matrix.project }}`.
* `src/core/pyproject.toml` and `src/api/pyproject.toml`: Package-level `[tool.ruff] line-length = 100` and `[tool.mypy]` configurations.
* `.copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-changes.md`: `c1` implementation and test baseline (`d3a2c5405`).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Package-Scoped Ruff Formatting and AST Invariance

* Intent: Reformat `tokenomics.py` and `progress.py` using their package-local `pyproject.toml` (`line-length = 100`) and verify full package lint/format conformance and AST equivalence against `d3a2c5405`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Format `src/core/src/zava_forward/core/tokenomics.py` and verify `src/core` Ruff + AST invariance

* Requirement and evidence: FR-1, NFR-1 (`C1`, `C2`, `C3`, `C5`)
* Expected result: `(cd src/core && python3 -m ruff format src/zava_forward/core/tokenomics.py && python3 -m ruff check . && python3 -m ruff format --check .)` exits `0`, and `tokenomics.py`'s parsed AST equals `d3a2c5405:src/core/src/zava_forward/core/tokenomics.py`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Format `src/api/src/zava_forward/api/progress.py` and verify `src/api` Ruff + AST invariance

* Requirement and evidence: FR-1, NFR-1 (`C1`, `C2`, `C4`, `C6`)
* Expected result: `(cd src/api && python3 -m ruff format src/zava_forward/api/progress.py && python3 -m ruff check . && python3 -m ruff format --check .)` exits `0`, and `progress.py`'s parsed AST equals `d3a2c5405:src/api/src/zava_forward/api/progress.py`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Focused Type-Check, Unit-Test Validation, and Git Identity Preparation

* Intent: Prove zero type or runtime regressions across `src/core` and `src/api` under Focused validation and verify repository-local privacy-safe git author/committer identity ahead of post-Review local commit closeout.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run Focused `mypy` and `unittest` suites across `src/core` and `src/api` and verify local git identity

* Requirement and evidence: FR-2, NFR-2 (`C7`, `C8`; `.github/copilot-instructions.md` Focused tier and noreply git identity rule)
* Expected result: `mypy` exits `0` in `src/core` and `src/api`; both caller-specified `unittest` commands and `-p "test_*tokenomics*.py"` suites execute `test_tokenomics_comparison.py`, `test_management_tokenomics_invariant_100.py`, and `test_management_tokenomics_api_100.py` (`-W error::ResourceWarning`) with `0` failures; local `user.email` is confirmed as `{id}+{login}@users.noreply.github.com` so the final frozen-HEAD commit after `rpi-review` includes all 2 Python files and all 7 `.copilot-tracking/*-c2-*` artifacts without pushing.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-phase-details.md

## Dependencies

* `ruff==0.17.1` and `mypy==2.4.0` installed in the active Python 3.12 environment matching `src/core/pyproject.toml` and `src/api/pyproject.toml`.
* `gh api user` availability to confirm repository-local `{id}+{login}@users.noreply.github.com` email before committing.

## Critique Disposition

Single-pass `rpi-plan-critique` completed with verdict `Pass` (`0` Critical, `0` High, `0` Medium, `0` Low).

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass critique (`Pass`, `0` findings) | resolved | No plan or phase-detail edits required; candidate finalized as `Ready`. |
| Residual risk: remote PR `#1792` stays at `d3a2c5405` until coordinator push | accepted with risk | Explicit caller `exclude` control forbids pushing from this worktree; frozen local HEAD commit leaves exact `10/10`-ready code and `c2` tracking trail for coordinator push. |

## Follow-Up Items

* Carry-forward `c1` follow-up (`RV-002`): Gate unlinked JSON recommendation historical acceptance on `resolved_at <= as_of` and clarify the 5-external + 3-metered TCA component mapping in `src/core/README.md` (outside `c2` lint/format scope; owned by follow-up backlog selection).
* Carry-forward `c1` follow-up (`RV-001`): Filter SQL `ai_meter` ledger rows to synthetic-admitted roots in `zava_forward.api.progress._ai_economics` for hybrid databases (outside `c2` lint/format scope; owned by follow-up backlog selection).
* Carry-forward governance item (`OD-51`): Obtain owner commercial tariff and spend-ceiling approval and wire live Azure Cost Management billing export reconciliation (`Refs #100`, `#432`; owned by project owner).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-c2-lint-changes.md
* Ready phase or task: P01 (`P01-T01`, `P01-T02`), P02 (`P02-T01`)
* Remaining provisional question or blocker: None
