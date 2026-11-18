<!-- markdownlint-disable-file -->
# RPI Plan: Issue #76 Correction Cycle 1 — PR #1768 `mssql` CI Parity Fix and Rebase onto `#1641`

## Task Metadata

* Task ID: issue-76-c1
* Task slug: ux-76-hazard-clock-owner-c1
* Planning status: Implementation-ready (critique findings resolved)
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan-critique.md

## Executive Summary

This plan resolves the single `mssql` CI failure (`MssqlParity.test_every_view_filter_sort_and_search_matches_the_in_memory_store` in GitHub Actions job `132694355150`, where 325/326 tests passed) on PR #1768 (`feat/ux-76-hazard-clock-owner`) and rebases the branch onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`, PR #1641 after PR #1769 / Issue #83 merged). Making staff lookup in `_match_staff` and role-fallback scanning in `project_safety_clock_and_owner` invariant to `staff` sequence ordering eliminates the divergence between in-memory/SQLite insertion order and SQL Server clustered primary-key (`email`) order, while rebasing cleanly integrates `#83`'s handoff escalation arguments and bumps `MEMBERSHIP_REVISION` so existing revision-4 databases rebuild `#76` safety queue flags.

### User Decisions and Requirements Highlights

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) with dated tracking artifacts under `.copilot-tracking/` for Issue #76 Correction Cycle 1 (`c1` on PR #1768).
* Rebase `feat/ux-76-hazard-clock-owner` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) before editing code, resolving `Store._work_context` in `src/core/src/zava_forward/core/store.py` so both `#83`'s `handoff=handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))` and `#76`'s `staff=staff_list` are preserved.
* Update `_match_staff` and `project_safety_clock_and_owner` in `src/core/src/zava_forward/core/taskqueues.py` so staff resolution and role-based escalation fallback are deterministic and independent of `staff` row order across `Store`, `SqlStore`, and `MssqlStore`.
* Add a focused unit test in `src/core/tests/test_hazard_safeguarding_clock_owner.py` verifying identical `named_owner` and `escalation_owner` across `staff` orderings (including `owner_code="PM-01"` with `owner="Sam Example"` under `[Sam, Pam, Kim]` vs `[Kim, Pam, Sam]`), run focused validation (`test_hazard_safeguarding_clock_owner.py`, `test_sqlreads.py`, `mypy`, and full `src/core` `unittest`), commit locally with the Copilot trailer, and leave a clean working tree without pushing or running `tools/rpi-checks.py`.

### What You May Not Know

* Upstream `#83` (`PR #1769`, now merged in `0c1fa1da4`) also bumped `taskqueues.MEMBERSHIP_REVISION` from `3` to `4` and changed `SqlStore._refresh_queue_membership` to load `data["staff"]` ordered by `email`. Bumping `MEMBERSHIP_REVISION` to `5` in `taskqueues.py` (and syncing `src/core/README.md`) ensures any SQL database already migrated under `#83` (`MEMBERSHIP_REVISION = 4`) also refreshes `queue_blocked` and `queue_overdue` for `#76`'s standalone safeguarding items.
* Cycle 0 placed its core tests in `src/core/tests/test_hazard_safeguarding_clock_owner_76.py`, while `pyproject.toml` runs `mypy` with `strict = true` across `src` and `tests`. Creating `src/core/tests/test_hazard_safeguarding_clock_owner.py` with full strict type annotations satisfies both the exact `-p "test_hazard_safeguarding_clock_owner.py"` selector and `mypy` strict checking without adding overrides to `pyproject.toml`.

### Unresolved Decisions or Blockers

* None. All root-cause, rebase, test-ownership, and typing boundaries were verified in `.copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c1-research.md`.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Execute the full ordered RPI loop (`research`, `plan`, `implement`, `review`) writing dated `.copilot-tracking/` artifacts for Issue #76 Correction Cycle 1 on PR #1768 (`Caller intake brief`).
* Rebase `feat/ux-76-hazard-clock-owner` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`), resolving the `store.py` conflict in `Store._work_context` by keeping both `handoff=handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))` and `staff=staff_list` (`Caller intake brief`).
* Make `_match_staff` in `src/core/src/zava_forward/core/taskqueues.py` deterministic and independent of `staff` list ordering by checking `code` across all `staff` first, then `email` across all `staff`, then `name` across all `staff`, and sort `roster` by `str(m.get("code") or m.get("email") or m.get("name") or "")` when scanning for `target_role` in `project_safety_clock_and_owner` (`Caller intake brief`).
* Add focused unit test coverage in `src/core/tests/test_hazard_safeguarding_clock_owner.py` verifying identical `named_owner` and `escalation_owner` regardless of `staff` ordering, including when `case` has `owner_code="PM-01"` and `owner="Sam Example"` with `staff` ordered `[Sam, Pam, Kim]` vs `[Kim, Pam, Sam]` (`Caller intake brief`).
* Run focused validation (`test_hazard_safeguarding_clock_owner.py`, `test_sqlreads.py`, `mypy`, and full `src/core` `unittest` suite), configure privacy-safe GitHub noreply commit author if needed, commit with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leave `git status --short` empty, and do not push or run `tools/rpi-checks.py` (`Caller intake brief`, `.github/copilot-instructions.md`).

## Goals

* Rebase `feat/ux-76-hazard-clock-owner` cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) with zero regression to either `#83` handoff escalation or `#76` safety clock/owner projection.
* Guarantee 100% `staff`-order invariance in `_match_staff` and `project_safety_clock_and_owner` so `Store` (JSON order), `SqlStore` (SQLite), and `MssqlStore` (SQL Server clustered `email` PK order) produce byte-identical safety clock and owner projections.
* Verify parity and regression safety under focused validation (`unittest` + `mypy` + `ruff`) and leave a clean committed branch ready for owner push.

## Scope and Non-Goals

### In Scope

* Rebasing `feat/ux-76-hazard-clock-owner` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) and resolving `src/core/src/zava_forward/core/store.py`.
* Deterministic multi-pass staff matching and sorted role fallback plus `MEMBERSHIP_REVISION = 5` in `src/core/src/zava_forward/core/taskqueues.py`, with matching revision note in `src/core/README.md`.
* Strictly typed staff-ordering permutation and SQL parity unit tests in `src/core/tests/test_hazard_safeguarding_clock_owner.py`.
* Focused validation in `src/core`, dated `.copilot-tracking/` `c1` artifacts, and local Git commit with clean worktree.

### Non-Goals

* Modifying `src/api/` web files or running `tools/rpi-checks.py`.
* Pushing to `origin` or mutating remote PR state.

## Functional Requirements

* FR-1: Clean rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) and queue-revision separation.
  * Rebase `feat/ux-76-hazard-clock-owner` onto `0c1fa1da4`, keeping both `handoff=handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))` and `staff=staff_list` in `Store._work_context` (`src/core/src/zava_forward/core/store.py`), and advance `taskqueues.MEMBERSHIP_REVISION` to `5` (updating `src/core/README.md`) so databases created at `#83`'s revision `4` recompute `#76` queue flags.
  * Observable acceptance criteria: `git merge-base --is-ancestor 0c1fa1da4 HEAD` exits `0`; both `#83` (`test_handoff_escalation_83.py`) and `#76` (`test_hazard_safeguarding_clock_owner_76.py`) pass on the rebased tree.
* FR-2: Order-invariant staff lookup in `_match_staff`.
  * `_match_staff` checks `code` across all `staff` first, then `email` (case-insensitive) across all `staff`, then `name` (case-insensitive) across all `staff`, iterating over a canonically sorted view of `staff` (`(code/oid, email, name)`) so neither cross-field conflicts (`owner_code="PM-01"` with `owner="Sam Example"`) nor duplicate-attribute ties depend on input row order.
  * Observable acceptance criteria: Calling `_match_staff` or `project_safety_clock_and_owner` with `owner_code="PM-01"` and `owner="Sam Example"` resolves `Pam Lead` (`PM-01`) identically across `[Sam, Pam, Kim]`, `[Kim, Pam, Sam]`, and every permutation of `STAFF`.
* FR-3: Order-invariant role-based escalation fallback in `project_safety_clock_and_owner`.
  * When `destination` and `case["owner"]` are absent or unrecorded, `project_safety_clock_and_owner` scans `sorted(roster, key=lambda m: str(m.get("code") or m.get("email") or m.get("name") or ""))` for each priority `target_role`.
  * Observable acceptance criteria: When multiple staff members share `target_role`, `project_safety_clock_and_owner` selects the exact same `named_owner`, `escalation_owner`, `owner_role`, and `owner_id` across every permutation of `staff`.
* FR-4: Regression test coverage for staff-ordering invariance and store parity.
  * `src/core/tests/test_hazard_safeguarding_clock_owner.py` verifies `project_safety_clock_and_owner` across all permutations of `[Sam, Pam, Kim]` (both direct and `escalation_owner` resolution with `owner_code="PM-01"` + `owner="Sam Example"`, unallocated fallback across duplicate-role rosters, and `Store` vs `SqlStore` `page_cases` parity when `store.data["staff"]` is ordered in SQL Server `email` PK order `[Kim, Pam, Sam]` while `Store` uses `[Sam, Pam, Kim]`).
  * Observable acceptance criteria: `python3 -m unittest discover -s tests -p "test_hazard_safeguarding_clock_owner.py" -v` runs and passes, and would fail against the pre-fix single-pass `_match_staff`.

## Non-Functional Requirements

* NFR-1: Strict static typing and lint hygiene in `src/core`.
  * Objective threshold or evaluation condition: `0` errors from `mypy` (strict mode across `src` and `tests`), `ruff check`, and `ruff format --check` on touched files in `src/core`.
  * Operating condition or verification approach, if needed: Run `mypy` and `ruff check` in `src/core`.
  * Observable acceptance criteria: Commands exit `0` without adding `ignore_errors` or `type: ignore` suppressions.
* NFR-2: Locked test budget and ownership.
  * Objective threshold or evaluation condition: Exact test removals = `none`; maximum new test files = `1` (`src/core/tests/test_hazard_safeguarding_clock_owner.py`, owned by `src/core/tests`; existing `test_hazard_safeguarding_clock_owner_76.py` and `test_sqlreads.py` retained).
  * Operating condition or verification approach, if needed: Check `git status` / `git diff --name-status` and run `unittest` selectors.
  * Observable acceptance criteria: Exactly one new test file added, zero test removals, and 100% of `src/core` unit tests pass.
* NFR-3: Clean local repository closeout without unauthorized remote side effects.
  * Objective threshold or evaluation condition: Local commit uses repository-local `gh api user` noreply email and includes `Refs #76` plus the Copilot `Co-authored-by` trailer; `git status --short` outputs empty after final commit; remote ref `origin/feat/ux-76-hazard-clock-owner` is untouched.
  * Operating condition or verification approach, if needed: Verify `git log -1` and `git status --short`.
  * Observable acceptance criteria: Working tree is completely clean and no `git push` or `rpi-checks.py` invocation occurs.

## Acceptance Criteria

* AC-1: `feat/ux-76-hazard-clock-owner` is rebased onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) with `Store._work_context` preserving both `#83` and `#76` arguments and `taskqueues.MEMBERSHIP_REVISION == 5`.
* AC-2: `_match_staff` and `project_safety_clock_and_owner` return identical `named_owner`, `accountable_owner`, `owner_role`, `owner_id`, `escalation_owner`, `escalation_owner_role`, and `escalation_owner_id` across every permutation of `staff`, including `owner_code="PM-01"` with `owner="Sam Example"` (`[Sam, Pam, Kim]` vs `[Kim, Pam, Sam]`) and duplicate-role rosters.
* AC-3: `src/core/tests/test_hazard_safeguarding_clock_owner.py` exists, is strictly typed, and passes via `python3 -m unittest discover -s tests -p "test_hazard_safeguarding_clock_owner.py" -v`.
* AC-4: `python3 -m unittest discover -s tests -p "test_sqlreads.py" -v`, `mypy`, `ruff check`, and `python3 -m unittest discover -s tests -q` in `src/core` all exit `0`.
* AC-5: All Correction Cycle 1 `.copilot-tracking/` artifacts (`research`, `plans`, `details`, `critique`, `changes`, `reviews`, and session `state.json`) are current, committed with `Refs #76` and the Copilot trailer, and `git status --short` is empty.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                         |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md                                                             |
| Phase details                    | .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md                                                  |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan-critique.md (`Verdict: Revise`; `PC-001`–`PC-003` resolved) |
| Relevant research                | .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c1-research.md                                                      |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-changes.md is created by `rpi-implement` as its evidence record   |
| Planning execution and readiness | Complete; implementation-ready                                                                                                     |
| Continuation context             | Confirmed automatic RPI Agent parent continues to `rpi-implement`                                                                  |

## Sources

* .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c1-research.md: Root-cause trace (`C1`–`C12`), rebase conflict & `MEMBERSHIP_REVISION` audit, and convergence selection (Option A).
* .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-plan.md: Parent Cycle 0 plan and invariants for Issue #76.
* src/core/src/zava_forward/core/taskqueues.py, store.py, sqlstore.py, mssqlstore.py: Canonical queue projection and store modules.
* src/core/tests/test_sqlreads.py and test_hazard_safeguarding_clock_owner_76.py: Existing SQL read parity and `#76` safety clock/owner regression suites.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Rebase onto `#1641` (`0c1fa1da4`) and Order-Invariant Staff Resolution

* Intent: Rebase `feat/ux-76-hazard-clock-owner` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`), resolve `store.py` preserving `#83` and `#76`, make `_match_staff` and `project_safety_clock_and_owner` order-invariant, and bump `MEMBERSHIP_REVISION` to `5`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Rebase branch onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) and resolve `store.py`

* Requirement and evidence: FR-1, AC-1; research `C5`, `C6`
* Expected result: `feat/ux-76-hazard-clock-owner` is rebased cleanly onto `0c1fa1da4` with `Store._work_context` passing both `handoff=handoff_view(c, as_of=self.as_of, policy=data.get("handoff_policy"), staff=data.get("staff"))` and `staff=staff_list`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Make `_match_staff` and `project_safety_clock_and_owner` order-invariant and bump `MEMBERSHIP_REVISION`

* Requirement and evidence: FR-1, FR-2, FR-3, AC-1, AC-2; research `C6`–`C10`; critique `PC-003`
* Expected result: `_match_staff` normalizes `code.strip()` and checks `code` across all `staff`, then `email`, then `name` over canonically sorted `staff`; `project_safety_clock_and_owner` sorts `roster` before role-based fallback scanning; `MEMBERSHIP_REVISION` is `5` in `taskqueues.py` and `src/core/README.md`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Permutation Parity Unit Tests, Focused Validation, and Local Commit Preparation

* Intent: Add strictly typed permutation and email-ordered `SqlStore` parity tests in `src/core/tests/test_hazard_safeguarding_clock_owner.py`, run all focused validation checks in `src/core`, verify diff boundaries and commit-author setup, and sequence clean post-review local commit closeout.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add `src/core/tests/test_hazard_safeguarding_clock_owner.py` and execute focused validation

* Requirement and evidence: FR-4, NFR-1, NFR-2, AC-2, AC-3, AC-4; research `C1`–`C4`, `C11`, `C12`; critique `PC-001`
* Expected result: `test_hazard_safeguarding_clock_owner.py` uses `Any`-typed bindings for untyped `Store`/`SqlStore`/`test_sqlreads` collaborators and verifies staff-order invariance across permutations (`[Sam, Pam, Kim]` vs `[Kim, Pam, Sam]`, duplicate-role rosters, and `Store` vs email-seeded `SqlStore` `page_cases`/`detail` parity); `test_hazard_safeguarding_clock_owner.py`, `test_sqlreads.py`, `mypy`, `ruff check`, and full `src/core` `unittest` discovery pass with 0 errors.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Verify diff boundaries, configure privacy-safe Git author, and reconcile changes for Review and local commit

* Requirement and evidence: NFR-2, NFR-3, AC-5; `.github/copilot-instructions.md`; critique `PC-002`
* Expected result: `git diff --name-status` confirms 0 test removals, 1 new test file (`src/core/tests/test_hazard_safeguarding_clock_owner.py`), and 0 `src/api/` edits; repository-local `user.email` is configured from `gh api user` (`{id}+{login}@users.noreply.github.com`); `.copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-changes.md` and checklist markers are reconciled so post-`rpi-review` artifacts and code commit cleanly in one local `Refs #76` commit with the Copilot trailer and empty `git status --short` (no `git push` or `tools/rpi-checks.py`).
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-phase-details.md

## Dependencies

* `origin/feat/demo-164-chat-grounding-provenance-0900` fetched locally at `0c1fa1da4`.
* Editable/installed `zava-forward-core` package in the active Python 3.12 environment (`mypy`, `ruff`, `unittest`).

## Critique Disposition

Single final-candidate critique completed in `.copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan-critique.md` (`Verdict: Revise`). All three findings were resolved directly in this plan and phase details without requiring user decisions or a second critique pass.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 / `PC-001` (Medium)| Resolved    | Updated `P02-T01` in the plan and phase details to invoke untyped `Store`, `SqlStore`, and `test_sqlreads` (`make_cases`, `dataset`) through `Any`-typed bindings (`store_cls: Any = Store`, `sql_store_cls: Any = SqlStore`, `reads_mod: Any = test_sqlreads`) so strict `mypy` passes with zero `type: ignore` or `pyproject.toml` edits, and to seed `SqlStore` with `staff` sorted by `email` (`[Kim, Pam, Sam]`) so `_seed`, `_refresh_queue_membership`, `_sync`, `page_cases`, and `detail` all execute in SQL Server clustered-PK row order. |
| Run 1 / `PC-002` (Medium)| Resolved    | Mapped `AC-1` to `P01-T01`/`P01-T02` and added `P02-T02` mapping `NFR-3` and `AC-5` for diff-boundary verification, `gh api user` noreply email configuration, `changes.md` reconciliation, and post-`rpi-review` clean local commit with `Refs #76` and the Copilot trailer without pushing or running `tools/rpi-checks.py`. |
| Run 1 / `PC-003` (Low)   | Resolved    | Updated `P01-T02` so `_match_staff` Pass 1 strips `code` (`code_clean = code.strip()`) consistently with `email` and `name` normalization. |
| Residual risk            | Accepted with risk | Live SQL Server container execution (`MssqlParity` with `ZF_TEST_MSSQL=1`) runs in GitHub Actions after owner-authorized push; local focused validation exercises all `STAFF` permutations and email-seeded `SqlStore` vs seed-ordered `Store` on `make_cases`. |

## Follow-Up Items

* Push rebased `feat/ux-76-hazard-clock-owner` to `origin` (`PR #1768`) once authorized by the owner and verify the hosted GitHub Actions `mssql` job (`MssqlParity`) passes on the new head SHA.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-changes.md
* Ready phase or task: Review (`P01` and `P02` complete)
* Remaining provisional question or blocker: None
