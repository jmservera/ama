<!-- markdownlint-disable-file -->
# RPI Plan: Issue #156 PR #1727 Cycle-2 CI Mypy Union-Attr Fix

## Task Metadata

* Task ID: issue-156-pr-1727-mypy-c2
* Task slug: 156-screen-design-traceability-mypy-c2
* Planning status: ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/156-screen-design-traceability-mypy-c2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/156-screen-design-traceability-mypy-c2-plan-critique.md

## Executive Summary

This Cycle-2 plan resolves the sole failing CI job (`src-api` Type check in `src-ci.yml`, GitHub Actions run `43644223724`) on PR #1727 for Issue #156 (`headRefName: feat/ux-156-design-traceability-1840`, `baseRefName: feat/demo-233-same-home-tensions-0825`). Hosted and local `mypy` runs under `strict = true` fail at two `[union-attr]` sites in `src/api/tests/test_screen_design_traceability.py` where `re.search(...)` (`Match[str] | None`) and `next(..., None)` (`ast.ClassDef | None`) are dereferenced without static `None`-narrowing.

Following the established pattern in sibling `src/api/tests/test_ux_design_traceability.py`, Phase `P01` creates and switches to local branch `feat/ux-156-design-traceability-1840` at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840` (preserving `docs/ux-156-design-traceability-1840` untouched), binds `match` and `target_cls`, pairs `self.assertIsNotNone(...)` with `assert match is not None` and `assert target_cls is not None`, verifies repository-local privacy-safe `user.email` (`{id}+{login}@users.noreply.github.com` via `gh api user`), and runs full `src/api` `mypy`, `ruff check`, `ruff format --check`, and targeted `unittest` checks while leaving the verified working tree uncommitted for `rpi-review`. After `rpi-review` writes `.copilot-tracking/reviews/2026-11-14/156-screen-design-traceability-mypy-c2-review.md` and finalizes session state, RPI Agent closeout creates one clean non-amended local Git commit on `feat/ux-156-design-traceability-1840` with the required `Co-authored-by` trailer without pushing.

### User Decisions and Requirements Highlights

* Preserve every existing `.copilot-tracking/` artifact committed on the PR #1727 branch (`2026-11-14-design-traceability-156-*`, `2026-11-14/156-design-trace-c2-2140-*`, and earlier Issue #156 records remain untouched).
* Narrow optional `Match[str] | None` and `ast.ClassDef | None` in `src/api/tests/test_screen_design_traceability.py` using `assert match is not None` and `assert target_cls is not None` alongside descriptive `unittest` assertions.
* Validate `python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .`, and `python3 -m unittest tests/test_screen_design_traceability.py -v` from `src/api`, then commit cleanly on `feat/ux-156-design-traceability-1840` without pushing.

### What You May Not Know

* `unittest.TestCase.assertIsNotNone` checks `None` at runtime (including under `python -O`), whereas Python's `assert x is not None` provides static type narrowing for `mypy` without triggering Ruff (`select = ["E", "F", "I", "B", "UP"]` in `src/api/pyproject.toml` omits `S101`). Pairing both mirrors `src/api/tests/test_ux_design_traceability.py`.
* Worktree `/home/azureuser/source/ama-demo-wt/feat-156-design-traceability-1840` initially had local branch `docs/ux-156-design-traceability-1840` checked out at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840` with no local `feat/ux-156-design-traceability-1840` ref; creating local `feat/ux-156-design-traceability-1840` at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840` aligns the local branch name with PR #1727's `headRefName` and `push.default = simple` without deleting `docs/ux-156-design-traceability-1840`.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) for the Cycle-2 CI fix on Issue #156 / PR #1727.
* Preserve all existing `.copilot-tracking/` artifacts already present on the branch.
* Add dated `2026-11-14` Cycle-2 RPI artifacts under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/` documenting the `mypy` `union-attr` fix (`assert match is not None` / `assert target_cls is not None`).
* Fix the two `[union-attr]` sites in `src/api/tests/test_screen_design_traceability.py` (`test_rows_are_complete_and_cover_every_issue` and `test_tests_exist`) so `cd src/api && python3 -m mypy` succeeds with `0` errors (`Success: no issues found`), `cd src/api && python3 -m ruff check . && python3 -m ruff format --check .` passes, and `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_screen_design_traceability.py -v` passes.
* Configure repository-local privacy-safe GitHub noreply email (`{id}+{login}@users.noreply.github.com` per `.github/copilot-instructions.md`), commit cleanly on local branch `feat/ux-156-design-traceability-1840` tracking `origin/feat/ux-156-design-traceability-1840` with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and do not push.

## Goals

* Eliminate both strict `mypy` `[union-attr]` errors in `src/api/tests/test_screen_design_traceability.py` while preserving runtime assertion clarity and exact traceability semantics.
* Maintain full Ruff lint/format compliance and focused-tier test verification across `src/api` without adding `pyproject.toml` exemptions.
* Record complete, traceable Cycle-2 RPI artifacts while preserving prior Cycle-1 and Cycle-2 tracking records intact.

## Scope and Non-Goals

### In Scope

* Aligning local branch `feat/ux-156-design-traceability-1840` at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840` without deleting `docs/ux-156-design-traceability-1840`.
* Narrowing `re.search(r"#(\d+)\]", row[0])` (`match`) and `next(..., None)` (`target_cls`) in `src/api/tests/test_screen_design_traceability.py`.
* Focused-tier local verification (`mypy`, `ruff check`, `ruff format --check`, and `unittest` on `tests/test_screen_design_traceability.py`, plus `tests/test_ux_design_traceability.py` sibling regression confirmation).
* Creating Cycle-2 RPI artifacts under `.copilot-tracking/{rpi-sessions,research,plans,details,reviews/plans,changes,reviews}/2026-11-14/` and creating one clean post-`rpi-review` local Git commit on `feat/ux-156-design-traceability-1840`.

### Non-Goals

* Editing `docs/reference/research/ux/screen-design-traceability.md`, `src/api/pyproject.toml`, workflows, or production application modules.
* Claiming human design, content, or WCAG acceptance for Issue #156 (criterion 1 remains unticked).
* Pushing commits to `origin` or mutating GitHub PR state.

## Functional Requirements

* FR-01: In `ScreenDesignTraceability.test_rows_are_complete_and_cover_every_issue`, bind `match = re.search(r"#(\d+)\]", row[0])`, verify `self.assertIsNotNone(match, row[0])`, narrow with `assert match is not None`, and extract `int(match.group(1))`.
  * Observable acceptance criteria: `test_rows_are_complete_and_cover_every_issue` passes in `unittest` and reports zero `mypy` `[union-attr]` errors.
* FR-02: In `ScreenDesignTraceability.test_tests_exist`, bind `target_cls = next((n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == klass), None)`, verify `self.assertIsNotNone(target_cls, f"{klass} not found in {path}")`, narrow with `assert target_cls is not None`, and inspect `target_cls.body`.
  * Observable acceptance criteria: `test_tests_exist` passes in `unittest` and reports zero `mypy` `[union-attr]` errors.
* FR-03: Preserve all pre-existing `.copilot-tracking/` files and record complete Cycle-2 RPI artifacts for the `mypy` fix before committing locally without pushing.
  * Observable acceptance criteria: `git status` is clean after commit, `git diff --diff-filter=D HEAD~1..HEAD` is empty, and `origin/feat/ux-156-design-traceability-1840` is untouched (`ahead 1`).

## Non-Functional Requirements

* NFR-01: Strict static type safety across `src/api` without configuration overrides.
  * Objective threshold or evaluation condition: `cd src/api && python3 -m mypy` exits `0` with `Success: no issues found` across all checked files (`src`, `tests`, `checks`), and `src/api/pyproject.toml` has zero diff.
  * Operating condition or verification approach, if needed: Run `python3 -m mypy` directly from `src/api`.
  * Observable acceptance criteria: `0` errors across all `src/api` checked files.
* NFR-02: Code style, formatting, and test suite determinism.
  * Objective threshold or evaluation condition: `cd src/api && python3 -m ruff check . && python3 -m ruff format --check .` exits `0`, and `unittest` runs all 5 test methods in `tests/test_screen_design_traceability.py` with `OK` and zero `.pyc` artifacts tracked in Git.
  * Operating condition or verification approach, if needed: Execute `ruff` and `unittest` from `src/api` and inspect `git status --short`.
  * Observable acceptance criteria: Clean exit code `0` for all three verification commands and clean working tree post-commit.

## Acceptance Criteria

* AC-01: `src/api/tests/test_screen_design_traceability.py` contains `assert match is not None` and `assert target_cls is not None` paired with `self.assertIsNotNone(...)`, with zero test removals (`none`) and zero new test methods added (`max additions: 0` methods; semantic coverage of all 5 existing traceability tests preserved unchanged).
* AC-02: `cd src/api && python3 -m mypy` exits `0` (`Success: no issues found`).
* AC-03: `cd src/api && python3 -m ruff check . && python3 -m ruff format --check .` exits `0`.
* AC-04: `cd src/api && PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src python3 -m unittest tests/test_screen_design_traceability.py -v` exits `0` (5/5 tests pass).
* AC-05: All pre-existing `.copilot-tracking/` artifacts remain intact, new Cycle-2 artifacts exist under `.copilot-tracking/{research,plans,changes,reviews}/2026-11-14/`, and all changes are committed locally on `feat/ux-156-design-traceability-1840` (tracking `origin/feat/ux-156-design-traceability-1840` for PR #1727, `ahead 1`) with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` and not pushed.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/156-screen-design-traceability-mypy-c2-plan.md                                                        |
| Phase details                    | .copilot-tracking/details/2026-11-14/156-screen-design-traceability-mypy-c2-phase-details.md                                             |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-14/156-screen-design-traceability-mypy-c2-plan-critique.md with Pass verdict (0 open findings) |
| Relevant research                | .copilot-tracking/research/2026-11-14/156-screen-design-traceability-mypy-c2-research.md                                                 |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/156-screen-design-traceability-mypy-c2-changes.md is created by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready; single-pass `rpi-plan-critique` completed with Pass verdict                                                          |
| Continuation context             | Confirmed automatic RPI Agent parent return for automatic transition to `rpi-implement`                                                   |

## Sources

* .copilot-tracking/research/2026-11-14/156-screen-design-traceability-mypy-c2-research.md: Primary Cycle-2 research evidence (`C1`–`C8`) establishing root cause, PR #1727 branch mapping, and selected narrowing pattern.
* src/api/tests/test_screen_design_traceability.py: Target test module failing strict `mypy` at the optional regex match and AST class lookup sites.
* src/api/tests/test_ux_design_traceability.py: Sibling traceability test establishing `self.assertIsNotNone(...)` + `assert ... is not None` convention.
* src/api/pyproject.toml: Strict `mypy` (`strict = true`) and Ruff (`line-length = 100`, `select = ["E", "F", "I", "B", "UP"]`) rules.
* .github/copilot-instructions.md: Focused-tier validation policy, branch-reuse guidance, and privacy-safe noreply Git commit email configuration.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Type-Narrow Optional Lookups and Verify Focused-Tier Checks

* Intent: Align local branch `feat/ux-156-design-traceability-1840`, narrow optional regex match and AST class lookup in `src/api/tests/test_screen_design_traceability.py`, and verify `mypy`, `ruff`, and `unittest` checks without altering existing test semantics or tracking history.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Narrow `match` and `target_cls` in `test_screen_design_traceability.py`

* Requirement and evidence: FR-01, FR-02, AC-01; `.copilot-tracking/research/2026-11-14/156-screen-design-traceability-mypy-c2-research.md` (`C3`, `C4`, `C7`).
* Expected result: `src/api/tests/test_screen_design_traceability.py` binds `match` and `target_cls`, calls `self.assertIsNotNone(...)`, narrows with `assert match is not None` and `assert target_cls is not None`, removes `none` existing tests, and adds `0` extra test methods.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/156-screen-design-traceability-mypy-c2-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Align Branch `feat/ux-156-design-traceability-1840`, Execute Focused-Tier Validation, Configure Noreply Git Identity, and Record Implementation Evidence

* Requirement and evidence: FR-03, NFR-01, NFR-02, AC-02, AC-03, AC-04, AC-05; `.github/copilot-instructions.md` and `.github/workflows/src-ci.yml` (`C1`, `C2`, `C5`, `C7`, `C8`).
* Expected result: Local branch `feat/ux-156-design-traceability-1840` is checked out at `deadb7144` tracking `origin/feat/ux-156-design-traceability-1840` (`docs/ux-156-design-traceability-1840` preserved untouched); `mypy`, `ruff check .`, `ruff format --check .`, and `unittest` on `tests/test_screen_design_traceability.py` (plus verified sibling `tests/test_ux_design_traceability.py`) pass with exit code `0`; repository-local `git config --local user.email "{id}+{login}@users.noreply.github.com"` is verified from `gh api user`; `git diff --diff-filter=D` is empty and no `.pyc` files are tracked; `.copilot-tracking/changes/2026-11-14/156-screen-design-traceability-mypy-c2-changes.md` records verified outcomes and leaves the working tree uncommitted for `rpi-review` so post-review closeout commits all Cycle-2 artifacts (including `.copilot-tracking/reviews/2026-11-14/156-screen-design-traceability-mypy-c2-review.md`) on `feat/ux-156-design-traceability-1840` in one clean `ahead 1` commit without pushing.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/156-screen-design-traceability-mypy-c2-phase-details.md

## Dependencies

* Local `src/api` Python 3.12 editable environment with `mypy`, `ruff`, `zava-forward-core`, and `zava-forward-agents`: already installed and verified during research (`C2`).
* Existing PR #1727 worktree `/home/azureuser/source/ama-demo-wt/feat-156-design-traceability-1840` at `deadb7144` matching `origin/feat/ux-156-design-traceability-1840` (`C8`).

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass `rpi-plan-critique`: Pass (`0` open findings; prior `PC-001` and `PC-002` verified resolved) | resolved | Plan and phase details verified implementation-ready with explicit `feat/ux-156-design-traceability-1840` alignment, noreply `user.email` check, and post-`rpi-review` single-commit sequencing |
| Single-pass `rpi-plan-critique`: Residual risk (hosted CI unobserved due to caller no-push constraint) | accepted_with_risk | Caller explicitly prohibited `git push`; local `mypy`, `ruff`, and `unittest` checks verify the `src-api` failure path locally and implementation/review artifacts record that hosted CI on the new head remains pending owner push |

## Follow-Up Items

* Role-owner screen wireframes, written screen task flows, and human design/accessibility acceptance reviews for Issue #156 (`docs/reference/research/ux/screen-design-traceability.md`): out of scope for this CI typing fix; owned by domain role design reviewers under Issues #155 and #156.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/156-screen-design-traceability-mypy-c2-changes.md
* Ready phase or task: P01 (P01-T01, P01-T02), followed by `rpi-review` and single post-review local commit on `feat/ux-156-design-traceability-1840` (`Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, no push)
* Remaining provisional question or blocker: none
