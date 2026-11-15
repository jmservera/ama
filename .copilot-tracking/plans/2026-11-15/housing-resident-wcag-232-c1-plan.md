<!-- markdownlint-disable-file -->
# RPI Plan: Rebase Housing and Resident WCAG (#232) onto Programme Coordinator WCAG (#230)

## Task Metadata

* Task ID: 2026-11-15-housing-resident-wcag-232-c1
* Task slug: housing-resident-wcag-232-c1
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/housing-resident-wcag-232-c1-plan-critique.md

## Executive Summary

This Cycle 1 (`c1`) plan rebases `feat/ux-232-resident-wcag` (`PR #1786`, local commits `184b828e1` and `cffec920a` from merge-base `a1d0be5f6`) onto the latest `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`, which merged `PR #1784` for Issue #230), resolves the three-way route and specialist-screen overlaps cleanly across `app.js` and `role-screens.js`, verifies combined `#230` and `#232` WCAG 2.2 AA conformance without regressing any repository baseline, updates the `.copilot-tracking/` RPI artifacts for the rebased head, and leaves a clean frozen Conventional Commit ready for coordinator review without pushing.

Read-only `git merge-tree` inspection (`C1`–`C10`) established that `#230` (`6510b6fbc`) and `#232` (`184b828e1` + `cffec920a`) intersect at `isRoleScreensDestination(destination)` in `src/api/src/zava_forward/api/web/app.js` and `ROLE_HASH_SCREENS` in `src/api/src/zava_forward/api/web/role-screens.js`, while all other hunks (`#230` `programme-shared-queue`, `programme-funnel` ["Lifecycle and funnel"], `programmeCell`, `programmeQueue`, `programmeFunnel`, `programmeStepCell`, `programmeJumpNav`, `mapPanel`, `coordinatorView`, and `style.css` vs `#232` `screenTable` `aria-live`, `roleScreensView` `#workspace-status` `announce()`, `#screen-queue` / `section#screen-evidence` landmarks and `data-state-cue="scope"`, inline two-line `document.getElementById` jump listener, `panels.js` `actForm` / `residentPanel`, and `case_journey_browser_check.py`) occupy disjoint regions.

### User Decisions and Requirements Highlights

* Run `git fetch origin feat/demo-233-same-home-tensions-0825` and rebase `feat/ux-232-resident-wcag` onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`).
* Resolve conflicts in `role-screens.js` (and `app.js` `isRoleScreensDestination`) preserving 100% of `#230` (`programme-shared-queue`, `programme-funnel` / lifecycle and funnel, `#/role/programme_manager`, `#/role/retrofit_coordinator`) and `#232` (`resident-choice` / housing-resident queue, `resident-service-issues`, `residentPanel` / `#/my-home`, `#/role/contact_centre`, `#workspace-status` announcements, `section#screen-evidence` landmarks/cues).
* Run the three specified Focused validation commands (`unittest` across 5 suites, `ruff check`, `mypy`), update `.copilot-tracking/` RPI artifacts for the rebased head, commit cleanly with Conventional Commit message (`Refs #232`) and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leave `git status --short` completely clean, and do NOT run `git push`.

### What You May Not Know

* `#232`'s `isResidentRoleScreen` guard (`screen.id === "resident-choice" || screen.id === "resident-service-issues"`) in `role-screens.js` keeps `span[data-state-cue="scope"]` (`"State: Confirmed - single-home record scope."`) scoped strictly to the two resident screens, preventing a cross-screen collision with `test_programme_coordinator_wcag_230.py`, which explicitly forbids `"confirmed"` `data-state-cue` values on `programme-queue`.
* `cffec920a` restored the inline two-line `document.getElementById(link.getAttribute("data-jump"))?.focus?.();` and `...?.scrollIntoView?.({ block: "start" });` listener in `role-screens.js` because `test_asset_exec_screen_wcag.py` pins that exact source substring; preserving `cffec920a` during rebase keeps all coupled specialist WCAG suites green simultaneously.
* Per AMA Repository Instructions (`Preserve original critique/Review outcomes`) and the RPI one-pass gate contract, Cycle 0 critique and review artifacts remain immutable while this Cycle 1 (`housing-resident-wcag-232-c1-*`) RPI artifact set and an appended rebase addendum in `housing-resident-wcag-232-changes.md` record the rebased head and combined `#230`+`#232` verification.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`), writing or updating dated `.copilot-tracking/` artifacts (`research`, `plans`, `details`, `changes`, `reviews`) for Issue #232 (`PR #1786`) in `/home/azureuser/source/ama-demo-wt/feat-232-resident-wcag` (caller prompt).
* Run `git fetch origin feat/demo-233-same-home-tensions-0825` and rebase `feat/ux-232-resident-wcag` onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`, including merged `PR #1784` for `#230`) (caller Step 1).
* Resolve conflicts in `src/api/src/zava_forward/api/web/role-screens.js` (and `src/api/src/zava_forward/api/web/app.js`) so both `#230` (`programme-shared-queue`, `programme-funnel` ["Lifecycle and funnel"], `#/role/programme_manager`, `#/role/retrofit_coordinator`) and `#232` (`resident-choice`, `resident-service-issues`, `residentPanel` / `#/my-home`, `#/role/contact_centre`, `#workspace-status`, `section#screen-evidence` landmarks/cues) remain intact (caller Step 2; `.copilot-tracking/research/2026-11-15/housing-resident-wcag-232-c1-research.md`).
* Run focused validation from `src/api`:
  * `PYTHONPATH=../core/src:../agents/src:src:../core/tests:../agents/tests /home/azureuser/source/ama/.venv/bin/python -m unittest tests/test_housing_resident_wcag_232.py tests/test_programme_coordinator_wcag_230.py tests/test_accessibility_baseline.py tests/test_content_standard.py tests/test_procurement_contractor_screen_wcag.py -q`
  * `/home/azureuser/source/ama/.venv/bin/ruff check src/zava_forward/api tests/test_housing_resident_wcag_232.py checks/case_journey_browser_check.py`
  * `/home/azureuser/source/ama/.venv/bin/mypy` (caller Step 3).
* Update `.copilot-tracking/` research, plan/details, changes, and review artifacts to record the rebase onto `origin/feat/demo-233-same-home-tensions-0825` (with `#230`) and the combined test verification while preserving immutable Cycle 0 critique/review verdicts (caller Step 4; AMA Repository Instructions).
* Configure repository-local privacy-safe Git email via `gh api user`, commit cleanly with a Conventional Commit message (`Refs #232`) and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leave `git status --short` completely clean, and do NOT run `git push` (caller Step 5; AMA Branch and Pull Request Workflow).

## Goals

* Produce a clean linear branch history for `feat/ux-232-resident-wcag` directly atop `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) with zero lost hunks from either `#230` or `#232`.
* Prove with automated tests that `#230` and `#232` routes, landmarks, jump navigation, row headers, live announcements, non-colour textual state cues, and counted repository baselines pass together without interference.
* Record traceable Cycle 1 RPI evidence and leave a frozen, clean local commit ready for coordinator review and push.

## Scope and Non-Goals

### In Scope

* Rebasing `feat/ux-232-resident-wcag` (`184b828e1`, `cffec920a`) onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) and resolving conflicts in `src/api/src/zava_forward/api/web/app.js` and `src/api/src/zava_forward/api/web/role-screens.js`.
* Extending `src/api/tests/test_housing_resident_wcag_232.py` with a focused post-rebase regression assertion proving `#230` (`#/role/programme_manager`, `#/role/retrofit_coordinator`, `programme-shared-queue`, `programme-funnel`) and `#232` (`#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, `resident-choice`, `resident-service-issues`, `residentPanel`, `#workspace-status`, `section#screen-evidence`) coexist cleanly in `isRoleScreensDestination` and `ROLE_HASH_SCREENS`.
* Executing all caller-specified Focused validation commands, coupled specialist WCAG suites, `ruff format --check`, `tools/rename-zava-tests.py`, and refreshed `web-design-guidelines` `file:line` review.
* Writing complete Cycle 1 `.copilot-tracking/` artifacts (`housing-resident-wcag-232-c1-*`) plus a post-rebase addendum in `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`, then committing cleanly on `feat/ux-232-resident-wcag` without pushing.

### Non-Goals

* Running `git push`, force-pushing, or modifying remote refs.
* Altering `#230` coordinator/programme semantics (`mapPanel`, `coordinatorView`, `programmeQueue`, `programmeFunnel`, `style.css`) or `#232` resident/housing boundaries (`panels.js`, `case_journey_browser_check.py`).
* Rewriting historical Cycle 0 critique (`.copilot-tracking/reviews/plans/2026-11-15/housing-resident-wcag-232-plan-critique.md`) or review (`.copilot-tracking/reviews/logs/2026-11-15/housing-resident-wcag-232-review.md`) verdicts.
* Claiming human assistive-technology sign-off (`#151`, `#155`) or using `Closes #232`.

## Functional Requirements

* FR-1: Rebase `feat/ux-232-resident-wcag` onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) and union-merge `isRoleScreensDestination(destination)` in `src/api/src/zava_forward/api/web/app.js` using `const target = String(destination || "").split("?")[0];` across `#/screens` and all nine `#/role/*` routes (`building_safety_lead`, `repairs`, `housing_officer`, `contact_centre`, `resident_engagement`, `procurement`, `contractor`, `programme_manager`, `retrofit_coordinator`), while retaining `#230`'s `mapPanel` and `coordinatorView` hunks intact.
  * Observable acceptance criteria: `git merge-base --is-ancestor origin/feat/demo-233-same-home-tensions-0825 HEAD` exits `0`; Node VM route checks return `true` for bare and query-bearing hashes across `#230` and `#232` routes and `false` for unknown/prototype routes.
* FR-2: Union-merge `ROLE_HASH_SCREENS` and preserve all `#230` and `#232` specialist-screen hunks in `src/api/src/zava_forward/api/web/role-screens.js`.
  * Observable acceptance criteria: `ROLE_HASH_SCREENS` maps all nine `#/role/*` aliases (`contact_centre` -> `resident-service-issues`, `programme_manager` -> `programme-queue`, `retrofit_coordinator` -> `programme-queue`, plus existing six aliases); `#230` (`programme-shared-queue`, `programme-funnel` ["Lifecycle and funnel"], `programmeCell`, `programmeQueue`, `programmeFunnel`, `programmeStepCell`, `programmeJumpNav`) and `#232` (`screenTable` `aria-live`, `roleScreensView` `announce()`, `#screen-queue`, `section#screen-evidence` with `aria-label="Evidence for ${c.id}"`, `data-state-cue="scope"`, `resident-choice`, `resident-service-issues`, inline two-line `document.getElementById` jump listener) all pass their respective DOM assertions.
* FR-3: Verify post-rebase coexistence of `#230` and `#232` in `src/api/tests/test_housing_resident_wcag_232.py` and across the combined Focused validation test run.
  * Observable acceptance criteria: `test_housing_resident_wcag_232.py` asserts `#230` + `#232` coexistence in `isRoleScreensDestination` and `ROLE_HASH_SCREENS`, and the combined 5-module `unittest` command (`test_housing_resident_wcag_232.py`, `test_programme_coordinator_wcag_230.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_procurement_contractor_screen_wcag.py`) plus coupled specialist WCAG suites exit `0`.
* FR-4: Record the rebase onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) and combined validation evidence in `.copilot-tracking/` Cycle 1 (`housing-resident-wcag-232-c1-*`) artifacts and a concise rebase addendum in `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`, then leave a clean Conventional Commit without pushing.
  * Observable acceptance criteria: All Cycle 1 tracking artifacts (`research`, `plan`, `details`, `critique`, `changes`, `review`, `state.json`) and the Cycle 0 `changes` addendum are committed cleanly with `Refs #232` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`; `git status --short` is empty; `origin/feat/ux-232-resident-wcag` is untouched (no `git push`).

## Non-Functional Requirements

* NFR-1: Counted accessibility, design-system, and plain-language baseline preservation.
  * Objective threshold or evaluation condition: `h("table", {}, ...)` count remains `14`, `aria-invalid` count remains `9`, bare `h("th", {}` count remains `0`, `position:fixed` count remains `2`, standalone `[tabindex="-1"]:focus` rule remains intact in `style.css`, inline two-line `document.getElementById` jump listener remains intact in `role-screens.js`, and `test_content_standard.py` reports `0` violations.
  * Operating condition or verification approach, if needed: Verified via `test_accessibility_baseline.py`, `test_content_standard.py`, `test_asset_exec_screen_wcag.py`, and `test_technical_quality_screens_wcag.py`.
  * Observable acceptance criteria: All baseline and peer WCAG suites exit `0`.
* NFR-2: Lint, formatting, strict `mypy`, and migration-test cleanliness.
  * Objective threshold or evaluation condition: `0` `ruff check` findings, `0` `ruff format --check` diffs, `0` strict `mypy` errors across `src/api`, `0` `sys.modules` mutations, and `0` failures in `python3 tools/rename-zava-tests.py`.
  * Operating condition or verification approach, if needed: Verified via caller Step 3 commands plus `ruff format --check` and `rename-zava-tests.py`.
  * Observable acceptance criteria: Every static/type/migration command exits `0`.

## Acceptance Criteria

* AC-1: `feat/ux-232-resident-wcag` has `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) as its direct ancestor (`git merge-base --is-ancestor 6510b6fbc HEAD`), with both `#230` and `#232` route aliases and specialist screen hunks preserved in `app.js`, `role-screens.js`, `panels.js`, `style.css`, and `case_journey_browser_check.py`.
* AC-2: All three caller-specified validation commands (`5`-module `unittest`, `ruff check`, `mypy`), coupled specialist WCAG tests (`test_asset_exec_screen_wcag.py`, `test_technical_quality_screens_wcag.py`, `test_programme_screen_wcag.py`, `test_housing_resident_screen_wcag.py`), `python3 tools/rename-zava-tests.py`, and refreshed `web-design-guidelines` `file:line` review pass with zero open defects.
* AC-3: `.copilot-tracking/` Cycle 1 (`housing-resident-wcag-232-c1-*`) `research`, `plan`, `details`, `critique`, `changes`, `review`, and `state.json` artifacts plus the Cycle 0 `housing-resident-wcag-232-changes.md` rebase addendum accurately document the `6510b6fbc` rebase and combined verification while leaving Cycle 0 critique and review verdicts untouched.
* AC-4: All changes are committed cleanly on `feat/ux-232-resident-wcag` using repository-local privacy-safe noreply email, Conventional Commit formatting (`Refs #232`), and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, with `git status --short` empty and zero `git push` execution.

## Test Ownership and Boundaries

* Canonical production and test targets modified or reconciled during rebase:
  * `src/api/src/zava_forward/api/web/app.js` (conflict resolution in `isRoleScreensDestination`)
  * `src/api/src/zava_forward/api/web/role-screens.js` (union of `ROLE_HASH_SCREENS` and preservation of all `#230` + `#232` hunks)
  * `src/api/tests/test_housing_resident_wcag_232.py` (add post-rebase `#230`+`#232` coexistence assertions)
* Rebased unchanged from `#232` (`184b828e1` / `cffec920a`):
  * `src/api/src/zava_forward/api/web/panels.js`
  * `src/api/checks/case_journey_browser_check.py`
  * `src/api/tests/test_procurement_contractor_screen_wcag.py`
* Inherited unchanged from `#230` (`6510b6fbc`):
  * `src/api/src/zava_forward/api/web/style.css`
  * `src/api/tests/test_programme_coordinator_wcag_230.py`
  * `src/api/tests/test_programme_screen_wcag.py`
* Test ownership:
  * Exact test removals: `none`
  * Maximum new test files: `0` (update existing `src/api/tests/test_housing_resident_wcag_232.py` only)
  * Semantic vs regression coverage: Node VM behavioral execution across combined `#230` and `#232` routes/screens (`test_housing_resident_wcag_232.py`, `test_programme_coordinator_wcag_230.py`, `test_procurement_contractor_screen_wcag.py`) paired with counted static/copy regression guards (`test_accessibility_baseline.py`, `test_content_standard.py`).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-c1-plan.md                                            |
| Phase details                    | .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-c1-phase-details.md                                 |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/housing-resident-wcag-232-c1-plan-critique.md (`Revise` -> `PC-001` applied directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/housing-resident-wcag-232-c1-research.md                                     |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-c1-changes.md is created by implementation          |
| Planning execution and readiness | Complete and implementation-ready (`Ready`)                                                                        |
| Continuation context             | Confirmed automatic RPI Agent session; parent continues directly to `rpi-implement` (`P01-T01`)                    |

## Sources

* `.copilot-tracking/research/2026-11-15/housing-resident-wcag-232-c1-research.md`: Cycle 1 three-way merge-tree findings (`C1`–`C10`, `W1`) and Option B convergence selection.
* `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md` & `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`: Cycle 0 `#232` implementation baseline.
* `src/api/tests/test_programme_coordinator_wcag_230.py` (`6510b6fbc`) & `src/api/tests/test_housing_resident_wcag_232.py` (`cffec920a`): `#230` and `#232` behavioral WCAG 2.2 AA contracts.
* `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/design-system.md`, and `docs/reference/research/ux/content-standard.md`: UX, WCAG 2.2 AA, and plain-language baselines.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Rebase onto `origin/feat/demo-233-same-home-tensions-0825` and Resolve `#230` + `#232` Overlaps

* Intent: Configure repository-local privacy-safe Git identity, rebase `feat/ux-232-resident-wcag` (`184b828e1`, `cffec920a`) onto `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`), and union-merge `app.js` and `role-screens.js` so every `#230` and `#232` change survives intact.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Configure local noreply Git identity and rebase `feat/ux-232-resident-wcag` onto `origin/feat/demo-233-same-home-tensions-0825`

* Requirement and evidence: FR-1, FR-2, AC-1; research `C1`–`C7`.
* Expected result: Local `user.email` is set to `{id}+{login}@users.noreply.github.com` from `gh api user`; `git rebase origin/feat/demo-233-same-home-tensions-0825` replays `184b828e1` and `cffec920a` cleanly onto `6510b6fbc` with `isRoleScreensDestination` in `app.js` normalizing `split("?")[0]` across all 10 routes (`#/screens` + 9 `#/role/*` aliases) and `ROLE_HASH_SCREENS` + specialist screen hunks in `role-screens.js` preserving 100% of `#230` and `#232` logic.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-c1-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Cross-Branch WCAG Verification, Web Guidelines Audit, and Tracking Reconciliation

* Intent: Lock `#230` + `#232` route/screen coexistence in `test_housing_resident_wcag_232.py`, execute all required Focused-tier and coupled WCAG checks plus refreshed Web Interface Guidelines review, and record post-rebase evidence in `.copilot-tracking/` before final single-pass `rpi-review` and local commit.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add `#230` + `#232` post-rebase coexistence assertion to `test_housing_resident_wcag_232.py` and run Focused + coupled validation

* Requirement and evidence: FR-3, NFR-1, NFR-2, AC-2; research `C8`–`C10`, `W1`; critique `PC-001`.
* Expected result: `test_contact_centre_housing_and_resident_routes_and_script_isolation` in `test_housing_resident_wcag_232.py` verifies that `#/role/programme_manager` and `#/role/retrofit_coordinator` (bare and with query strings) return `true` in `isRoleScreensDestination` alongside `#/role/housing_officer`, `#/role/contact_centre`, and `#/role/resident_engagement`, exports lexical `ROLE_HASH_SCREENS` and `programmeOverviewSections` in the Node VM context to verify `"programme-queue"` coexists in `roleScreens` and `ROLE_HASH_SCREENS` with `"resident-choice"` and `"resident-service-issues"`, and verifies `"programme-shared-queue"` and `"programme-funnel"` remain `#230` overview jump-target section IDs; all 3 caller validation commands (`5`-module `unittest`, `ruff check`, `mypy`), coupled WCAG suites, `ruff format --check`, `rename-zava-tests.py`, and refreshed `web-design-guidelines` review exit `0`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-c1-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Record Cycle 1 changes artifact and Cycle 0 rebase addendum for `rpi-review` and post-review frozen commit

* Requirement and evidence: FR-4, AC-3, AC-4; caller Steps 4–5 and AMA Repository Instructions.
* Expected result: `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-c1-changes.md` and an appended rebase-verification addendum in `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md` record the `6510b6fbc` rebase and combined test verification (preserving immutable Cycle 0 critique and review files), reconciled and ready for single-pass `rpi-review` followed by atomic parent-owned Conventional Commit (`Refs #232` + Copilot trailer, clean `git status --short`, no `git push`).
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/housing-resident-wcag-232-c1-phase-details.md

## Dependencies

* Remote-tracking ref `origin/feat/demo-233-same-home-tensions-0825` (`6510b6fbc`) fetched in worktree.
* Active host Python/lint/type toolchain on `PATH` (`/usr/bin/python3`, `/home/azureuser/.local/bin/ruff`, `/home/azureuser/.local/bin/mypy`; `/home/azureuser/source/ama/.venv` is an empty directory in this workspace) and Node.js (`node`) for VM DOM harnesses.

## Follow-Up Items

* Align `NO_REGION_GAPS` for `resident-service-issues` (`Routes to ask` region from `#86`) in `src/api/checks/specialist_keyboard_browser_check.py` in a dedicated full-tier gate-tool PR (`#1294`) — outside Focused-tier non-gate scope; owned by harness maintainer.
* Complete human assistive-technology (`NVDA`, `JAWS`, `VoiceOver`) and `360px` mobile walkthroughs across `#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, and `#/case/<id>?tab=resident` before closing Issue #232 (`#151`, `#155`) — owned by human accessibility reviewer.

## Critique Disposition

* Critique artifact: `.copilot-tracking/reviews/plans/2026-11-15/housing-resident-wcag-232-c1-plan-critique.md` (`Complete`, verdict `Revise`, `0` Critical, `0` High, `0` Medium, `1` Low).
* `PC-001` (`[Low]`): Applied directly by planning parent in `P02` / `P02-T01` across `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-c1-plan.md` and `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-c1-phase-details.md` — corrected the existing test method reference to `test_contact_centre_housing_and_resident_routes_and_script_isolation`, distinguished registered screen ID `"programme-queue"` (`roleScreens` / `ROLE_HASH_SCREENS`) from `#230` jump-target section IDs `"programme-shared-queue"` and `"programme-funnel"`, and specified explicit Node VM export (`globalThis.__roleHashScreens = ROLE_HASH_SCREENS; globalThis.__programmeOverviewSections = programmeOverviewSections;`) for lexical `const` bindings in `role-screens.js`. Finalized as `Ready` without repeating critique.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-c1-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None
