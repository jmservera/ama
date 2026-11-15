<!-- markdownlint-disable-file -->
# RPI Phase Details: Rebase Housing and Resident WCAG (#232) onto Programme Coordinator WCAG (#230)

## Metadata

* Task ID: 2026-11-15-housing-resident-wcag-232-c1
* Task slug: housing-resident-wcag-232-c1
* Related plan: .copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-c1-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/housing-resident-wcag-232-c1-research.md, .copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md, docs/reference/research/ux/wcag-conformance-baseline.md, docs/reference/research/ux/design-system.md, docs/reference/research/ux/content-standard.md

## Phase Index

| Phase ID | Name                                                                                       | Status  | Detail sections       |
|----------|--------------------------------------------------------------------------------------------|---------|-----------------------|
| P01      | Rebase onto `origin/feat/demo-233-same-home-tensions-0825` and Resolve `#230` + `#232` Overlaps | Complete    | P01, P01-T01          |
| P02      | Cross-Branch WCAG Verification, Web Guidelines Audit, and Tracking Reconciliation          | Complete    | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Rebase onto `origin/feat/demo-233-same-home-tensions-0825` and Resolve `#230` + `#232` Overlaps

### Context

Research (`C1`–`C7`) confirmed that `origin/feat/demo-233-same-home-tensions-0825` moved from `a1d0be5f6` to `6510b6fbc` (`PR #1784` for `#230`), while local `feat/ux-232-resident-wcag` holds `184b828e1` and `cffec920a`. Only `isRoleScreensDestination` in `app.js` conflicts directly, and `ROLE_HASH_SCREENS` in `role-screens.js` has adjacent insertions that must both be retained. Because all Cycle 1 tracking files (`housing-resident-wcag-232-c1-*`) are untracked and do not collide with any tracked path in `6510b6fbc`, `git rebase origin/feat/demo-233-same-home-tensions-0825` can run directly without stashing or mutating Cycle 0 tracked artifacts beforehand.

### Intent

Replay `184b828e1` and `cffec920a` cleanly onto `6510b6fbc` while preserving every `#230` and `#232` route, landmark, jump target, row header, live announcement, and textual state cue.

### Boundaries

* Included: Repository-local `git config --local user.email` / `user.name` setup from `gh api user`; `git fetch origin feat/demo-233-same-home-tensions-0825`; `git rebase origin/feat/demo-233-same-home-tensions-0825`; conflict resolution in `src/api/src/zava_forward/api/web/app.js` and `src/api/src/zava_forward/api/web/role-screens.js`.
* Excluded: Running `git push`; altering `style.css`, `panels.js`, `case_journey_browser_check.py`, or `#230` test files; rewriting Cycle 0 critique/review artifacts.

### Likely Targets

* `src/api/src/zava_forward/api/web/app.js`: Resolve `isRoleScreensDestination(destination)` with `const target = String(destination || "").split("?")[0];` and all 10 routes (`#/screens`, `#/role/building_safety_lead`, `#/role/repairs`, `#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, `#/role/procurement`, `#/role/contractor`, `#/role/programme_manager`, `#/role/retrofit_coordinator`), keeping `#230`'s `mapPanel` and `coordinatorView` updates untouched.
* `src/api/src/zava_forward/api/web/role-screens.js`: Ensure `ROLE_HASH_SCREENS` contains all 9 `#/role/*` entries (`contact_centre`, `programme_manager`, `retrofit_coordinator`, plus the existing 6), and verify that both `#230` (`programme-shared-queue`, `programme-funnel` ["Lifecycle and funnel"], `programmeCell`, `programmeQueue`, `programmeFunnel`, `programmeStepCell`, `programmeJumpNav`) and `#232` (`screenTable` `aria-live="polite"`, `roleScreensView` `announce()`, `#screen-queue`, `section#screen-evidence` with `aria-label="Evidence for ${c.id}"`, `data-state-cue="scope"`, `resident-choice`, `resident-service-issues`, inline two-line `document.getElementById` jump listener from `cffec920a`) remain intact.

### Dependencies

* None.

### Validation Expectations

* `git merge-base --is-ancestor origin/feat/demo-233-same-home-tensions-0825 HEAD` exits `0`.
* `git diff origin/feat/demo-233-same-home-tensions-0825...HEAD -- src/api/` contains exclusively `#232`'s additions cleanly integrated with `#230` (zero regressions or dropped lines from `6510b6fbc`).

### Completion Evidence

* Clean rebase completion onto `6510b6fbc` verified by `git log --oneline -n 4` and `git diff origin/feat/demo-233-same-home-tensions-0825 -- src/api/src/zava_forward/api/web/{app.js,role-screens.js}`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Configure local noreply Git identity and rebase `feat/ux-232-resident-wcag` onto `origin/feat/demo-233-same-home-tensions-0825`

#### Context

AMA Branch and Pull Request Workflow requires resolving `{id}+{login}@users.noreply.github.com` via `gh api user` and setting repository-local `git config --local user.email` before committing or rebasing commits so rebased committer metadata uses the privacy-safe noreply address. Replaying `184b828e1` onto `6510b6fbc` pauses at `app.js` (and potentially `role-screens.js` around `ROLE_HASH_SCREENS`), after which `cffec920a` applies cleanly on top.

#### Intent

Complete the rebase onto `6510b6fbc` cleanly with privacy-safe git metadata and 100% preservation of `#230` and `#232`.

#### Boundaries

* Included: `gh api user` lookup, `git config --local`, `git fetch origin feat/demo-233-same-home-tensions-0825`, `git rebase origin/feat/demo-233-same-home-tensions-0825`, `edit` conflict resolution in `app.js` / `role-screens.js`, `git add` + `GIT_EDITOR=true git rebase --continue`.
* Excluded: Modifying global git config or pushing to `origin`.

#### Likely Targets

* `src/api/src/zava_forward/api/web/app.js`
* `src/api/src/zava_forward/api/web/role-screens.js`

#### Dependencies

* None.

#### Validation Expectations

* Rebase completes with exit code `0`, `6510b6fbc` is an ancestor of `HEAD`, and no conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) exist anywhere in the repository.

#### Completion Evidence

* Clean `git rebase` output, conflict-free `app.js` and `role-screens.js`, and verified commit ancestry.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Cross-Branch WCAG Verification, Web Guidelines Audit, and Tracking Reconciliation

### Context

Research (`C8`–`C10`) showed that `#230` and `#232` are structurally compatible (`isResidentRoleScreen` prevents `data-state-cue="scope"` from leaking into `programme-queue`, and counted baselines stay at `14` tables / `9` `aria-invalid` / `0` bare `th` / `2` `position:fixed`), and adding an explicit coexistence check in `src/api/tests/test_housing_resident_wcag_232.py` locks the merged route table and anchor coexistence against future rebase drift.

### Intent

Verify the rebased tree across all required unit, lint, format, strict type-checking, migration, and Web Interface Guidelines gates, and reconcile `.copilot-tracking/` artifacts for single-pass `rpi-review` and final parent-owned commit closeout.

### Boundaries

* Included: `src/api/tests/test_housing_resident_wcag_232.py`, `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-c1-changes.md`, `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md` (append-only Cycle 1 rebase addendum), and plan/details marker reconciliation.
* Excluded: Modifying Cycle 0 critique (`housing-resident-wcag-232-plan-critique.md`) or review (`housing-resident-wcag-232-review.md`) artifacts; running `git push`.

### Likely Targets

* `src/api/tests/test_housing_resident_wcag_232.py`: Update `verifyRouter()`, the `roleSource` Node VM export (`globalThis.__roleHashScreens = ROLE_HASH_SCREENS; globalThis.__programmeOverviewSections = programmeOverviewSections;`), and `test_contact_centre_housing_and_resident_routes_and_script_isolation` to assert post-rebase coexistence: `#/role/programme_manager` and `#/role/retrofit_coordinator` (bare and query-suffixed) resolve `isRoleScreensDestination(...) === true` alongside `#/role/housing_officer`, `#/role/contact_centre`, and `#/role/resident_engagement`; `"programme-queue"` remains registered in `roleScreens` and mapped in `ROLE_HASH_SCREENS` alongside `"resident-choice"` and `"resident-service-issues"`; and `"programme-shared-queue"` and `"programme-funnel"` remain present as `#230` overview jump-target section IDs in `programmeOverviewSections` / rendered `programme-queue` DOM.
* `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-c1-changes.md` and `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`.

### Dependencies

* P01.

### Validation Expectations

* All three caller-specified Focused validation commands from `src/api` pass:
  1. `PYTHONPATH=../core/src:../agents/src:src:../core/tests:../agents/tests /home/azureuser/source/ama/.venv/bin/python -m unittest tests/test_housing_resident_wcag_232.py tests/test_programme_coordinator_wcag_230.py tests/test_accessibility_baseline.py tests/test_content_standard.py tests/test_procurement_contractor_screen_wcag.py -q`
  2. `/home/azureuser/source/ama/.venv/bin/ruff check src/zava_forward/api tests/test_housing_resident_wcag_232.py checks/case_journey_browser_check.py`
  3. `/home/azureuser/source/ama/.venv/bin/mypy`
* Coupled WCAG and migration checks also pass: `test_asset_exec_screen_wcag.py`, `test_technical_quality_screens_wcag.py`, `test_programme_screen_wcag.py`, `test_housing_resident_screen_wcag.py`, `ruff format --check`, and `python3 tools/rename-zava-tests.py`.
* Refreshed `web-design-guidelines` review (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`) reports `✓ pass` in `file:line` format across `app.js`, `role-screens.js`, and `panels.js`.

### Completion Evidence

* Passing command outputs recorded in `housing-resident-wcag-232-c1-changes.md` and `housing-resident-wcag-232-changes.md`, reconciled `[x]` markers in Cycle 1 plan and `Complete` status in Cycle 1 phase details.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add `#230` + `#232` post-rebase coexistence assertion to `test_housing_resident_wcag_232.py` and run Focused + coupled validation

#### Context

Adding explicit assertions in `test_contact_centre_housing_and_resident_routes_and_script_isolation` (`src/api/tests/test_housing_resident_wcag_232.py`) — explicitly exporting lexical `const ROLE_HASH_SCREENS` and `programmeOverviewSections` inside the `roleSource` VM context (`globalThis.__roleHashScreens = ROLE_HASH_SCREENS; globalThis.__programmeOverviewSections = programmeOverviewSections;`) — ensures any future edit to `isRoleScreensDestination`, `ROLE_HASH_SCREENS`, `roleScreens`, or `programmeOverviewSections` cannot accidentally drop `#230` (`programme_manager` / `retrofit_coordinator` -> `"programme-queue"`, plus jump-target section IDs `"programme-shared-queue"` and `"programme-funnel"`) or `#232` (`housing_officer` / `contact_centre` -> `"resident-service-issues"`, `resident_engagement` -> `"resident-choice"`).

#### Intent

Lock post-rebase `#230` + `#232` coexistence in automated unit tests, refresh and run the `web-design-guidelines` audit, and verify all Focused-tier and coupled checks pass.

#### Boundaries

* Included: `src/api/tests/test_housing_resident_wcag_232.py`, WebFetch refresh of `web-design-guidelines`, and running `unittest`, `ruff`, `mypy`, and `rename-zava-tests.py`.
* Excluded: Creating new test files or loosening `src/api/pyproject.toml`.

#### Likely Targets

* `src/api/tests/test_housing_resident_wcag_232.py`

#### Dependencies

* P01-T01.

#### Validation Expectations

* `unittest` (both the 5-suite caller command and coupled specialist WCAG suites), `ruff check`, `ruff format --check`, `mypy`, `rename-zava-tests.py`, and refreshed `web-design-guidelines` `file:line` audit all pass cleanly.

#### Completion Evidence

* Exact test counts and command exit statuses captured for the changes artifact.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Record Cycle 1 changes artifact and Cycle 0 rebase addendum for `rpi-review` and post-review frozen commit

#### Context

Caller Step 4 requires updating `.copilot-tracking/` artifacts to record the rebase onto `origin/feat/demo-233-same-home-tensions-0825` (with `#230`) and the combined test verification, and Caller Step 5 requires leaving a clean Conventional Commit with the Copilot trailer and empty `git status --short` without pushing. Note that `rpi-implement` prepares and reconciles the changes/plan/details artifacts before `rpi-review`, while the parent RPI Agent performs the single atomic post-review `git commit` after `rpi-review` writes its review artifact and transitions `housing-resident-wcag-232-c1-state.json` to `Follow-up` so `git status --short` is 100% clean at the frozen commit.

#### Intent

Write `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-c1-changes.md`, append a concise Cycle 1 post-rebase addendum to `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`, reconcile `[x]` plan markers and `Complete` phase statuses, and hand off cleanly to `rpi-review` (after which the RPI Agent commits all Cycle 1 changes and re-verifies the 3 validation commands + empty `git status --short` on the frozen `HEAD`).

#### Boundaries

* Included: `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-c1-changes.md`, `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`, `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-c1-plan.md`, and `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-c1-phase-details.md`.
* Excluded: Editing Cycle 0 critique/review files or running `git push`.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-c1-changes.md`
* `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`
* `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-c1-plan.md`
* `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-c1-phase-details.md`

#### Dependencies

* P02-T01.

#### Validation Expectations

* All plan markers (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`) and phase-detail statuses are reconciled before `rpi-review`; post-review atomic commit leaves `git status --short` empty and re-passes Focused validation without pushing.

#### Completion Evidence

* Reconciled Cycle 1 changes/plan/details artifacts ready for single-pass `rpi-review`.

#### Unresolved Items

* None.
