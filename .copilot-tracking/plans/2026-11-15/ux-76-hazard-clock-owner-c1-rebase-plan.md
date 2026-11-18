<!-- markdownlint-disable-file -->
# RPI Plan: Issue #76 C1 Rebase Continuation onto `#1641` (`08c36e4dc`)

## Task Metadata

* Task ID: issue-76-c1-rebase
* Task slug: ux-76-hazard-clock-owner-c1-rebase
* Planning status: Implementation-ready (critique passed)
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-plan-critique.md

## Executive Summary

This plan rebases `feat/ux-76-hazard-clock-owner` (`8bd8a4f4d` and `c98e58bf4`) from `0c1fa1da4` onto the latest `origin/feat/demo-164-chat-grounding-provenance-0900` (`08c36e4dc`, incorporating `#1770` / Issue #133 and `#1771` / Issue #108), resolves the two top-of-file section conflicts in `src/api/README.md` and `src/core/README.md` while preserving all content from both sides in reverse-chronological README order, verifies the three caller-specified focused validation suites across `src/core` and `src/api`, and commits the compact `ux-76-hazard-clock-owner-c1-rebase-*` RPI tracking artifacts locally with `Refs #76` and the Copilot trailer without pushing.

### User Decisions and Requirements Highlights

* Record compact RPI artifacts under `.copilot-tracking/*/` named `ux-76-hazard-clock-owner-c1-rebase-*` across Research, Plan, Implement, and Review.
* Fetch `origin feat/demo-164-chat-grounding-provenance-0900` and rebase `feat/ux-76-hazard-clock-owner` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`08c36e4dc`).
* Resolve the conflicts in `src/api/README.md` and `src/core/README.md` by preserving both sides' dated sections in the READMEs' chronological order (`#76` rebased head section above `#108` merged `08c36e4dc` section, above `2026-11-11 #83` / `#1288, #107`, while keeping `#133`'s `aftercare` update intact).
* Execute focused validation (`#76` unit tests across `src/core` and `src/api`, `ruff check` + `ruff format --check` + `mypy` in `src/core`, and `ruff check` + `ruff format --check` in `src/api`).
* Commit tracking artifacts locally with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leave `git status --short` empty, and do NOT push.

### What You May Not Know

* Both `src/api/README.md` and `src/core/README.md` prepend new feature sections directly after YAML frontmatter in newest-first (reverse-chronological) order (`2026-11-15` -> `2026-11-11` -> `2026-10-31`). Placing `#76` (`2026-11-15`, rebased onto `08c36e4dc`) immediately above `#108` (`2026-11-15`, merged in `08c36e4dc`) matches that reverse-chronological convention AND keeps Commit 2 (`c98e58bf4`, which updates `MEMBERSHIP_REVISION = 5` right below frontmatter in `src/core/README.md`) cleanly replayable without a second conflict.
* Neither `#1770` (`#133`) nor `#1771` (`#108`) touched `taskqueues.py`, `store.py`, `sqlstore.py`, `workflows.py`, or `web/app.js`, so `MEMBERSHIP_REVISION = 5` and all `#76` code/test modules carry forward unchanged.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop (`research`, `plan`, `implement`, `review`) for Issue #76 C1 rebase continuation onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`08c36e4dc`) on branch `feat/ux-76-hazard-clock-owner`, recording compact `.copilot-tracking/*/` artifacts with slug `ux-76-hazard-clock-owner-c1-rebase` (`Caller intake brief`).
* Run `git fetch origin feat/demo-164-chat-grounding-provenance-0900` and `git rebase origin/feat/demo-164-chat-grounding-provenance-0900`, resolving `src/api/README.md` and `src/core/README.md` conflicts by preserving both sides' entries in README chronological order (`Caller intake brief`).
* Run the three caller-specified focused validation commands covering `#76` `core`/`api` unit tests, `src/core` `ruff check` + `ruff format --check` + `mypy`, and `src/api` `ruff check` + `ruff format --check` (`Caller intake brief`).
* Configure privacy-safe GitHub noreply commit author if needed, commit the `ux-76-hazard-clock-owner-c1-rebase-*` tracking artifacts with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leave `git status --short` clean, and do not push (`Caller intake brief`, `.github/copilot-instructions.md`).

## Goals

* Rebase `feat/ux-76-hazard-clock-owner` cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`08c36e4dc`) preserving both `#76` commits (`feat(queues)` and `fix(queues)`) and all upstream `#133` / `#108` documentation and code.
* Confirm zero regressions across `#76` unit tests, `ruff`, and strict `mypy` on the rebased tree.
* Close out with reconciled RPI artifacts committed locally on a clean working tree without pushing.

## Scope and Non-Goals

### In Scope

* Fetching `origin/feat/demo-164-chat-grounding-provenance-0900` and rebasing `feat/ux-76-hazard-clock-owner` onto it (`08c36e4dc`).
* Resolving `src/api/README.md` and `src/core/README.md` during rebase.
* Executing focused validation in `src/core` and `src/api`.
* Recording and committing `ux-76-hazard-clock-owner-c1-rebase-*` tracking artifacts locally.

### Non-Goals

* Modifying `#76`, `#133`, or `#108` production or test source files.
* Running `tools/rpi-checks.py` or pushing to `origin`.

## Functional Requirements

* FR-1: Clean rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`08c36e4dc`).
  * Fetch `origin feat/demo-164-chat-grounding-provenance-0900` and replay both `#76` commits (`8bd8a4f4d` and `c98e58bf4`) onto `08c36e4dc`.
  * Observable acceptance criteria: `git merge-base --is-ancestor 08c36e4dc HEAD` exits `0`, and both rebased `#76` commits remain intact above `08c36e4dc`.
* FR-2: Lossless chronological resolution of `src/api/README.md` and `src/core/README.md`.
  * Keep `ms.date: 2026-11-15` in YAML frontmatter, place the `#76` (`2026-11-15, Refs #76`) section immediately above the `#108` (`2026-11-15, Refs #108`) section (matching the READMEs' newest-first reverse-chronological section order above `2026-11-11 #83` / `#1288, #107`), preserve `c98e58bf4`'s `MEMBERSHIP_REVISION = 5` + staff-order-invariant wording in `src/core/README.md`, and preserve `#133`'s `neutral_text` documentation update in `src/core/README.md`.
  * Observable acceptance criteria: Zero conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) exist anywhere in the repository, and both `#76` and `#108` sections (plus `#133` in `src/core/README.md`) appear in full.

## Non-Functional Requirements

* NFR-1: Focused validation pass across `src/core` and `src/api` with locked zero-delta test budget.
  * Objective threshold or evaluation condition: Exact test removals = `none`; maximum new test files = `0` (existing `test_hazard_safeguarding_clock_owner.py`, `test_hazard_safeguarding_clock_owner_76.py`, and `test_hazard_safeguarding_clock_owner_api_76.py` retained unchanged); all 3 caller validation commands exit `0`.
  * Operating condition or verification approach, if needed: Run caller `unittest`, `ruff check`, `ruff format --check`, and `mypy` commands.
  * Observable acceptance criteria: 9/9 targeted `#76` unit tests pass (`4` + `3` + `2`), and `ruff` + `mypy` exit `0`.
* NFR-2: Clean local commit closeout with privacy-safe author identity and zero remote push.
  * Objective threshold or evaluation condition: Repository-local `user.email` matches `{id}+{login}@users.noreply.github.com` from `gh api user`; tracking artifacts commit locally with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`; `git status --short` is empty; no `git push` runs.
  * Operating condition or verification approach, if needed: Check `git config --local user.email`, `git log -n 4 --oneline`, and `git status --short`.
  * Observable acceptance criteria: Clean working tree with local tracking commit atop the two rebased `#76` commits above `08c36e4dc`.

## Acceptance Criteria

* AC-1: `git merge-base --is-ancestor 08c36e4dc HEAD` exits `0` on `feat/ux-76-hazard-clock-owner` with zero conflict markers in `src/api/README.md` or `src/core/README.md` and all `#76`, `#108`, and `#133` README sections preserved.
* AC-2: `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api/src:src/api/tests python3 -m unittest src/core/tests/test_hazard_safeguarding_clock_owner.py src/core/tests/test_hazard_safeguarding_clock_owner_76.py src/api/tests/test_hazard_safeguarding_clock_owner_api_76.py -q` exits `0`.
* AC-3: `(cd src/core && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy)` and `(cd src/api && python3 -m ruff check src tests && python3 -m ruff format --check src tests)` both exit `0`.
* AC-4: All `ux-76-hazard-clock-owner-c1-rebase-*` `.copilot-tracking/` artifacts (`research`, `plans`, `details`, `critique`, `changes`, `reviews`, and `state.json`) are current and committed locally with `Refs #76` and the Copilot trailer, `git status --short` is empty, and no remote push occurred.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                         |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-plan.md                                                      |
| Phase details                    | .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-phase-details.md                                           |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-plan-critique.md (`Verdict: Pass`, 0 findings) |
| Relevant research                | .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-research.md                                               |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-changes.md is created by `rpi-implement`                   |
| Planning execution and readiness | Complete; implementation-ready                                                                                                     |
| Continuation context             | Confirmed automatic RPI Agent parent continues to `rpi-implement` once critique gate completes                                     |

## Sources

* .copilot-tracking/research/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-research.md: Rebase merge-tree inspection and semantic audit (`C1`–`C6`).
* .copilot-tracking/plans/2026-11-15/ux-76-hazard-clock-owner-c1-plan.md: Parent Issue #76 C1 plan and invariants.
* src/api/README.md and src/core/README.md: Conflict target files on `08c36e4dc` and `feat/ux-76-hazard-clock-owner`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Rebase `feat/ux-76-hazard-clock-owner` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`08c36e4dc`)

* Intent: Fetch latest target ref (`08c36e4dc`), replay `8bd8a4f4d` and `c98e58bf4`, and resolve `src/api/README.md` and `src/core/README.md` preserving both `#76` and `#108` (`#1771`) sections (plus `#133` / `#1770`) cleanly.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Fetch target branch, rebase `feat/ux-76-hazard-clock-owner`, and resolve `src/api/README.md` and `src/core/README.md`

* Requirement and evidence: FR-1, FR-2, AC-1; research `C1`–`C5`
* Expected result: `feat/ux-76-hazard-clock-owner` sits cleanly atop `origin/feat/demo-164-chat-grounding-provenance-0900` (`08c36e4dc`) with both rebased `#76` commits intact, zero conflict markers, `#76` (`MEMBERSHIP_REVISION = 5`) above `#108` in both READMEs' reverse-chronological top sections, and `#133`'s `aftercare` section preserved in `src/core/README.md`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Focused Validation and Local Tracking Commit Closeout

* Intent: Execute the three caller-specified validation commands across `src/core` and `src/api`, verify diff boundaries and privacy-safe Git author config, reconcile tracking artifacts for `rpi-review`, and commit tracking artifacts cleanly without pushing.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run focused `#76` unit tests, `ruff`, and `mypy` across `src/core` and `src/api`

* Requirement and evidence: NFR-1, AC-2, AC-3; research `C5`, `C6`
* Expected result: All 3 caller validation commands exit `0` with 0 test removals and 0 new test or source files modified beyond README conflict resolution.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile changes, run `rpi-review` closeout commit with `Refs #76` and Copilot trailer, and verify clean `git status --short`

* Requirement and evidence: NFR-2, AC-4; `.github/copilot-instructions.md`
* Expected result: Privacy-safe `user.email` (`{id}+{login}@users.noreply.github.com`) verified, `changes.md` and checklist markers reconciled prior to `rpi-review`, and after `rpi-review` completes `review.md` + `state.json`, all `ux-76-hazard-clock-owner-c1-rebase-*` tracking artifacts are committed locally with `Refs #76` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leaving `git status --short` empty with no `git push`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-phase-details.md

## Dependencies

* `origin/feat/demo-164-chat-grounding-provenance-0900` (`08c36e4dc`).
* Local Python 3.12 toolchain with `ruff`, `mypy`, and `unittest` across `src/core` and `src/api`.

## Critique Disposition

Single final-candidate critique completed in `.copilot-tracking/reviews/plans/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-plan-critique.md` (`Verdict: Pass`, `0` findings across `P01` and `P02`; verified clean Commit 2 replay when `#76` sits above `#108` in both READMEs, unchanged `ranking.policy_hash(ranking.CURRENT)` for `#108` `heldout_eval`, and Python 3.12 `unittest` CLI support). Zero plan revisions or user decisions required; accepted residual risk remains post-push hosted `mssql` CI execution once push is authorized.

## Follow-Up Items

* Push rebased `feat/ux-76-hazard-clock-owner` to `origin` (`PR #1768`) once authorized by the owner/coordinator and verify the hosted GitHub Actions `mssql` job (`MssqlParity`) passes on the new head SHA.
* Optional hardening (`RV-001` from C1 review): sort `staff` before role-based fallback in `workflows._resolve_escalation_target` (`#83`).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/ux-76-hazard-clock-owner-c1-rebase-changes.md
* Ready phase or task: Review (`P01` and `P02` complete)
* Remaining provisional question or blocker: None
