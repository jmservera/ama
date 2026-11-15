<!-- markdownlint-disable-file -->
# RPI Plan: Programme Coordinator WCAG 2.2 Verification and Screen Enhancements (#230)

## Task Metadata

* Task ID: 2026-11-15-programme-coordinator-wcag-230
* Task slug: programme-coordinator-wcag-230
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/programme-coordinator-wcag-230-plan-critique.md

## Executive Summary

This plan completes the engineering WCAG 2.2 AA conformance enhancements for GitHub issue `#230` (`Programme manager and coordinator screens`) across both the specialist `programme-queue` screen (`src/api/src/zava_forward/api/web/role-screens.js`) and the primary `Coordinator flow` workbench route `#/coordinator` (`src/api/src/zava_forward/api/web/app.js` and `style.css`), matching the sibling `#228` (`538462eba`) and `#231` (`a1d0be5f6`) standards on parent branch `feat/demo-233-same-home-tensions-0825`. It wires `#/role/programme_manager` and `#/role/retrofit_coordinator` hash route aliases, upgrades all three `programme-queue` tables to emit `<th scope="row">` first-column headers alongside Fluent 2 non-colour `.flag` / `.status-line.wait` cues and `aria-describedby` scope-filter wiring, adds `.screen-links` keyboard section-jump navigation (`a[data-jump]` + focusable `h2[tabindex="-1"]` targets across all seven major `<h2>` sections including `Map of open cases`), `aria-describedby` error/cutoff associations, and tri-state (`present` / `zero` / `unknown` and `stopped` / `no-stop` / `unknown`) visible non-colour state cues to `#/coordinator`, and delivers a dedicated regression and semantic conformance suite in `src/api/tests/test_programme_coordinator_wcag_230.py`.

### User Decisions and Requirements Highlights

* Target parent integration branch `origin/feat/demo-233-same-home-tensions-0825` (PR `#1639`, tip `a1d0be5f6`) under the Focused validation tier without running `tools/rpi-checks.py` or pushing to remote.
* Preserve `src/api/tests/test_accessibility_baseline.py` and `src/api/tests/test_content_standard.py` (plus `src/core/tests/test_scenario_manifest.py` and `test_needs_inventory.py`) completely green.
* Commit locally with repository-local privacy-safe GitHub noreply email (`gh api user` -> `{id}+{login}@users.noreply.github.com`), exact title `feat(ux): complete WCAG 2.2 keyboard and state-cue conformance for programme coordinator screens (Refs #230)`, and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, keeping `Refs #230` because manual human assistive-technology acceptance (`#151`, `#155`) remains outside automated checks.

### What You May Not Know

* Counted static guards in `src/api/tests/test_accessibility_baseline.py` and `test_epic149_form_error_summary_associations.py` pin exact counts across `web/*.js` and `web/*.css`: `9` `setAttribute("aria-invalid", "true")` sites, `14` `h("table", {},` sites, and `2` `position:fixed` rules. By reusing `screenRecordTable` / `screenTable(..., true)` in `role-screens.js`, keeping the existing `table` helper in `coordinatorView()`, and associating `#co-filter-error` via `aria-describedby` without adding a 10th `setAttribute("aria-invalid", "true")` call, all counted guards remain intact.
* `src/api/tests/test_map_fullscreen.py` splits `app.js` on the exact literal `"\nasync function coordinatorView()"`, and `src/api/checks/role_screens_browser_check.py` queries `get_by_role("region", name="Evidence for ZF-1", exact=True)` and forbids `\bready\b` inside `programme-queue` connected-home text. Every planned edit preserves those exact structural boundaries.

### Unresolved Decisions or Blockers

* None for the engineering slice. Manual assistive-technology and screen-reader acceptance checks remain tracked under `#151` and `#155` and are respected by citing `Refs #230`.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Continue the automatic RPI loop (`hve-core-all:rpi-agent`) on branch `feat/demo-230-pm-wcag` targeting parent integration branch `origin/feat/demo-233-same-home-tensions-0825` (PR `#1639`, `a1d0be5f6`) for GitHub issue `#230` (Caller prompt).
* Complete `rpi-plan` (with single-pass `rpi-plan-critique`), `rpi-implement`, and `rpi-review` for `#230` programme coordinator WCAG 2.2 verification and screen enhancements (Caller prompt).
* Preserve `test_accessibility_baseline.py` and `test_content_standard.py` as well as core synthetic manifest SHA checks (`test_scenario_manifest.py`, `test_needs_inventory.py`) (Caller prompt; `.copilot-tracking/research/2026-11-15/programme-coordinator-wcag-230-research.md` `C12`-`C14`, `C19`).
* Run Focused validation tier checks (targeted unit/WCAG/content/manifest tests, `ruff`, `mypy`, `node --check`) without executing `tools/rpi-checks.py` (Caller prompt).
* Configure repository-local commit email via `gh api user` (`{id}+{login}@users.noreply.github.com`), stage all implementation and `.copilot-tracking/` files, commit with title `feat(ux): complete WCAG 2.2 keyboard and state-cue conformance for programme coordinator screens (Refs #230)` and Copilot `Co-authored-by` trailer, fetch and rebase cleanly onto `origin/feat/demo-233-same-home-tensions-0825`, leave `git status --short` empty, and do NOT push (Caller prompt).

## Goals

* Align `programme-queue` (`role-screens.js`) and `Coordinator flow` (`#/coordinator` in `app.js` and `style.css`) with the WCAG 2.2 AA engineering baseline (`#151`) and sibling specialist screen conventions (`#228`, `#231`) for hash route aliases, `<th scope="row">` table row headers, keyboard section-jump focus navigation, programmatic focus visibility, `aria-describedby` control descriptions, and Fluent 2 non-colour status cues.
* Prove those semantics, keyboard paths, and plain-language/read-only boundaries with focused automated tests (`src/api/tests/test_programme_coordinator_wcag_230.py` and updated row-header assertions in `src/api/tests/test_programme_screen_wcag.py`) without regressing any existing test or counted baseline guard.

## Scope and Non-Goals

### In Scope

* Route alias wiring for `#/role/programme_manager` and `#/role/retrofit_coordinator` -> `"programme-queue"` in `src/api/src/zava_forward/api/web/role-screens.js` and `src/api/src/zava_forward/api/web/app.js`.
* `programme-queue` WCAG 2.2 upgrades in `src/api/src/zava_forward/api/web/role-screens.js`: `<th scope="row">` row headers on all three data tables, `aria-describedby="programme-page-status programme-filter-status"` on `#programme-scope`, `data-jump-target` parity on `programmeJumpNav` anchors, and Fluent 2 `.flag` / `.flag.danger` / `.status-line.wait` + `data-state-cue` wrappers preserving exact rendered text strings.
* `coordinatorView()` (`#/coordinator`) WCAG 2.2 upgrades in `src/api/src/zava_forward/api/web/app.js` (`mapPanel` `#map-title` landmark/focus target + `coordinatorView()`) and `src/api/src/zava_forward/api/web/style.css`: keyboard section-jump `<nav class="screen-links">` (`contractorJumpLinks` `a[data-jump]`) targeting all seven `<h2>` sections (`Choose the current case population`, `Denominator and coverage`, `Heatmap of current cases`, `Lifecycle funnel: current and observed cases`, `Record selection`, `Map of open cases`, `Selected records`) without duplicate nested `region` names, `aria-describedby` links for `#co-filter-error` (`co-view`, `co-group_by`) and `#co-cutoff-note` (`co-as_of`, `co-start`), visible tri-state (`present` / `zero` / `unknown` and `stopped` / `no-stop` / `unknown`) `.flag` / `.flag.danger` + `data-state-cue` non-colour state cues on heatmap count cells and `Selected records` `Can move on` cells, and `.coordinator h2[tabindex="-1"]:focus-visible` prepended before `.screen-record h2[tabindex="-1"]:focus-visible { ... }`.
* Test coverage in `src/api/tests/test_programme_coordinator_wcag_230.py` (new) and `src/api/tests/test_programme_screen_wcag.py` (updated row-header scope check).

### Non-Goals

* Claiming human screen-reader, assistive-technology, or user-acceptance sign-off (`#151`, `#155`).
* Modifying `scenario-manifest.json` hashed files (`workbench-manifest.json`, `workbench_browser_check.py`, `dataset.py`, `test_workbench.py`) or bumping counted `aria-invalid` (`9`), `h("table", {},` (`14`), or `position:fixed` (`2`) inventories.
* Running `tools/rpi-checks.py` or pushing commits to `origin`.

## Functional Requirements

* FR-01: `#/role/programme_manager` and `#/role/retrofit_coordinator` (with optional `?case=`, `?page=`, and `?scope=` parameters) must lazy-load `/role-screens.js` (and `/chat.js` for staff), highlight `#/screens` in primary navigation, open `programme-queue` for permitted roles (`Retrofit Programme Manager`, `Programme Support Officer`, `Retrofit Coordinator`), and render the `Screen unavailable` `role="alert"` fallback for unpermitted roles (`Contractor`, `Resident Liaison Officer`).
  * Observable acceptance criteria: `missingWorkspaceScripts` and `route()` resolve both `#/role/programme_manager` and `#/role/retrofit_coordinator` identically to `#/screens?screen=programme-queue` with role enforcement verified in automated tests.
* FR-02: All three `programme-queue` tables (`Shared queue: returned and handed-off work`, `Lifecycle and funnel by stage`, and `Same-home step states`) must render `<th scope="col">` column headers in `<thead>` and `<th scope="row">` record headers in column 0 of `<tbody>`, `#programme-scope` must reference `programme-page-status programme-filter-status` via `aria-describedby`, `programmeJumpNav` links must carry `data-jump` and `data-jump-target`, and returned/handoff/funnel/unblocked/step states must pair plain-text prefixes with Fluent 2 `.flag` / `.flag.danger` / `.status-line.wait` classes and `data-state-cue` attributes without altering existing visible copy or adding write controls.
  * Observable acceptance criteria: `test_programme_screen.py`, `test_programme_screen_wcag.py`, and `test_programme_coordinator_wcag_230.py` confirm `<th scope="row">`, `aria-describedby`, `data-jump-target`, `data-state-cue`, exact copy preservation, and zero write controls in connected view.
* FR-03: `#/coordinator` (`coordinatorView()`) must render a keyboard section-jump `<nav aria-label="Jump to a coordinator section" class="screen-links">` (via `contractorJumpLinks`) whose `a[data-jump]` links move programmatic focus (`tabindex="-1"`) without route change to all seven major section `<h2>` headings (`Choose the current case population`, `Denominator and coverage`, `Heatmap of current cases`, `Lifecycle funnel: current and observed cases`, `Record selection`, `Map of open cases`, `Selected records`), binding `<form>`, `summary`, `Record selection`, and `section.map-panel` via single `aria-labelledby` attributes while keeping the three `table()` outer `<section class="card">` containers unlabelled so each inner `.table-scroll[role="region"]` remains a unique `region` landmark.
  * Observable acceptance criteria: Delegated `a[data-jump]` click activation on `#/coordinator` calls `preventDefault()`, leaves `location.hash` unchanged, and moves focus + scroll to every one of the 7 target `h2[tabindex="-1"]` headings in document order, styled with a two-tone `:focus` / `:focus-visible` ring and unique landmark names.
* FR-04: `#/coordinator` must associate `#co-filter-error` (`role="alert"`) with `co-view` and `co-group_by` via `aria-describedby` (clearing stale error text when either control changes), associate `#co-cutoff-note` with `co-as_of` and `co-start` via `aria-describedby`, expose visible tri-state non-colour `.flag` badges + `data-state-cue` (`present` / `zero` / `unknown`, keeping `Unknown != 0`) and `(present)` / `(none recorded)` / `(unknown count)` link `aria-label` text on heatmap count cells, and render tri-state non-colour `.flag.danger` / `.flag` + `data-state-cue` (`stopped` / `no-stop` / `unknown`) badges (`"Action needed: Cannot move on"`, `"State: No current stop recorded"`, `"State: Unknown (stop state not supplied)"`) in `Selected records` `Can move on` cells while keeping `#coordinator-records` focusable (`tabindex="0"`).
  * Observable acceptance criteria: `test_programme_coordinator_wcag_230.py` verifies `aria-describedby` wiring, empty-filter validation focus + alert text + change clearing, tri-state heatmap visible non-colour state cues (`count > 0`, `0`, `null`), and tri-state `Selected records` non-colour stop/clear/unknown badges (`true`, `false`, `null`).

## Non-Functional Requirements

* NFR-01: Static accessibility, plain-language content standard, map-split, and synthetic scenario-manifest guards must remain 100% intact.
  * Objective threshold or evaluation condition: `sites == 9` (`aria-invalid`), `tables == 14` (`h("table", {},`), `len(fixed) == 2` (`position:fixed`), zero banned words under `test_content_standard.py`, intact `"\nasync function coordinatorView()"` split in `test_map_fullscreen.py`, intact `Evidence for ${c.id}` region label and absence of `\bready\b` in `programme-queue` connected view, and zero changes to `scenario-manifest.json` recipe SHA inputs.
  * Operating condition or verification approach, if needed: Run `test_accessibility_baseline.py`, `test_content_standard.py`, `test_epic149_form_error_summary_associations.py`, `test_map_fullscreen.py`, `test_scenario_manifest.py`, and `test_needs_inventory.py`.
  * Observable acceptance criteria: All counted/lexical/manifest test suites exit `0` with zero modifications to `test_accessibility_baseline.py` or `test_content_standard.py`.
* NFR-02: Code quality, typing, and test isolation.
  * Objective threshold or evaluation condition: Zero `node --check` syntax errors across modified `web/*.js`, zero `ruff check` or `mypy` issues across modified/added Python tests, and zero `sys.modules` pollution when running full `unittest discover` in `src/api` and `src/core`.
  * Operating condition or verification approach, if needed: Execute `node --check`, `ruff check`, `mypy`, and `unittest` suites under Focused validation.
  * Observable acceptance criteria: All linters, type checks, and test suites pass cleanly; maximum new test files added = `1` (`src/api/tests/test_programme_coordinator_wcag_230.py`), test files removed = `none`.

## Acceptance Criteria

* AC-01: `#/role/programme_manager` and `#/role/retrofit_coordinator` route aliases resolve to `programme-queue` with lazy script loading, navigation active state, same-home `?case=` support, and role-based denial alerts (`FR-01`).
* AC-02: `programme-queue` renders `<th scope="col">` and `<th scope="row">` across all three tables, links `#programme-scope` to `programme-page-status programme-filter-status` via `aria-describedby`, sets `data-jump-target` on jump links, and wraps returned/handoff/funnel/warning/step states in Fluent 2 non-colour cues without breaking `test_programme_screen.py` or `test_programme_screen_wcag.py` (`FR-02`).
* AC-03: `#/coordinator` provides `.screen-links` keyboard section-jump links to all seven focusable `h2[tabindex="-1"]` headings (with unique landmark naming and `#map-title` coverage), `aria-describedby` associations for `#co-filter-error` and `#co-cutoff-note`, and visible tri-state (`Unknown != 0`) non-colour textual/badge cues on heatmap count and `Selected records` `Can move on` cells (`FR-03`, `FR-04`).
* AC-04: `src/api/tests/test_programme_coordinator_wcag_230.py` passes alongside `test_programme_screen.py`, `test_programme_screen_wcag.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_epic149_form_error_summary_associations.py`, `test_map_fullscreen.py`, `test_workspace_scripts.py`, `test_procurement_contractor_screen_wcag.py`, `test_technical_quality_screens_wcag.py`, `test_data_steward_screen_wcag.py`, `test_scenario_manifest.py`, `test_needs_inventory.py`, `ruff`, and `mypy` (`NFR-01`, `NFR-02`).
* AC-05: All implementation and `.copilot-tracking/` artifacts are committed in one clean commit with title `feat(ux): complete WCAG 2.2 keyboard and state-cue conformance for programme coordinator screens (Refs #230)` and Copilot trailer, cleanly rebased onto `origin/feat/demo-233-same-home-tensions-0825` with `git status --short` empty and no push.

## Test Ownership and Canonical Target Lock

* Canonical edited source targets:
  * `src/api/src/zava_forward/api/web/role-screens.js`
  * `src/api/src/zava_forward/api/web/app.js`
  * `src/api/src/zava_forward/api/web/style.css`
* Generated targets: `none` (web assets are served directly from `src/api/src/zava_forward/api/web/`).
* Test ownership and bounds:
  * Exact test removals: `none`.
  * Preserved unchanged guard files: `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_content_standard.py`.
  * Updated existing test file (`1`): `src/api/tests/test_programme_screen_wcag.py` (update row-header `<th scope="row">` assertion at line `373` to verify `<th scope="col">` in `thead` and `<th scope="row">` in `tbody`).
  * Maximum new test files (`1`): `src/api/tests/test_programme_coordinator_wcag_230.py` covering semantic conformance (WCAG 1.3.1 row/col headers and `aria-labelledby`/`aria-describedby`, 1.4.1 non-colour textual/badge cues, 2.1.1/2.4.1/2.4.3/2.4.7 keyboard jump navigation and programmatic focus styling, 3.3.1/3.3.2 filter error/cutoff associations) and regression coverage (`#/role/*` alias routing/RBAC/script loader, read-only connected view, plain-language glossary compliance).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/programme-coordinator-wcag-230-plan.md                                                                |
| Phase details                    | .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md                                                     |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/programme-coordinator-wcag-230-plan-critique.md (`Revise` -> `PC-001`..`PC-005` applied directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/programme-coordinator-wcag-230-research.md                                                         |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/programme-coordinator-wcag-230-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete and `Ready` after single-pass `rpi-plan-critique` disposition                                                                   |
| Continuation context             | Confirmed automatic `RPI Agent` loop (`2026-11-15-programme-coordinator-wcag-230`)                                                       |

## Sources

* `.copilot-tracking/research/2026-11-15/programme-coordinator-wcag-230-research.md`: Cycle 1 Wider/Deeper/Contrarian findings and `C1`-`C19`, `W1` evidence log.
* `docs/reference/research/ux/wcag-conformance-baseline.md`: WCAG 2.2 AA conformance baseline (`#151`), counted static checks, and manual AT boundary.
* `docs/reference/research/ux/design-system.md` & `docs/reference/research/ux/content-standard.md`: Fluent 2 design tokens, `.flag` / `.status-line` non-colour state components, and banned internal vocabulary rules (`#153`).
* `docs/reference/research/ux/customer-journeys/programme.md`: Programme management and coordinator journey, shared queue separation of responsibilities, and read-only boundary (`#230`).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Programme Queue and Role Route Alias WCAG 2.2 Enhancements

* Intent: Bring `#/role/programme_manager`, `#/role/retrofit_coordinator`, and `programme-queue` (`role-screens.js`) to full WCAG 2.2 AA parity with `#228` and `#231` while preserving every counted and browser check invariant.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Wire `#/role/programme_manager` and `#/role/retrofit_coordinator` route aliases

* Requirement and evidence: `FR-01`, `AC-01`; `role-screens.js:92-108`, `app.js:370-455` (`C6`, `C7`).
* Expected result: Both hash routes load `/role-screens.js` (and `/chat.js` for staff), set `#/screens` active in `#nav`, open `programme-queue` for permitted roles, and render `Screen unavailable` `role="alert"` for unpermitted roles.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add `<th scope="row">`, `aria-describedby`, `data-jump-target`, and Fluent 2 non-colour state cues to `programme-queue`

* Requirement and evidence: `FR-02`, `AC-02`, `NFR-01`; `role-screens.js:443-725` (`C2`, `C8`, `C12`, `C14`, `C16`-`C18`).
* Expected result: All three `programme-queue` tables emit `<th scope="col">` in `thead` and `<th scope="row">` in `tbody` column 0 without adding a table literal; `#programme-scope` carries `aria-describedby="programme-page-status programme-filter-status"`; `programmeJumpNav` links carry `data-jump-target`; queue return/handoff cells, funnel banners, unblocked warning banner, and step state cells carry Fluent 2 `.flag` / `.flag.danger` / `.status-line.wait` and `data-state-cue` while keeping exact rendered text strings.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Coordinator Flow (`#/coordinator`) Keyboard Jump Navigation and Non-Colour State Cues

* Intent: Upgrade `coordinatorView()` (`#/coordinator` in `app.js` and `style.css`) with keyboard section-jump navigation, programmatic heading focus rings, `aria-describedby` error/cutoff associations, and non-colour textual/badge cues without altering counted `aria-invalid` or `h("table", {},` baselines or the `test_map_fullscreen.py` split boundary.
* Dependencies: P01-T01 (`app.js` co-edit)

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add keyboard section-jump nav, focusable section headings, `aria-describedby` associations, and non-colour state cues in `coordinatorView()` and `style.css`

* Requirement and evidence: `FR-03`, `FR-04`, `AC-03`, `NFR-01`; `app.js:1898-1900,2390-2400,2530-2538,2705-2829`, `style.css:98-100,374-375` (`C3`, `C9`, `C10`, `C12`-`C15`, `PC-001`..`PC-004`).
* Expected result: `#/coordinator` renders `contractorJumpLinks` (`<nav aria-label="Jump to a coordinator section" class="screen-links">`) targeting all seven `h2[tabindex="-1"]` section headings (including `#map-title`, keeping outer `table()` sections unlabelled so inner `.table-scroll` regions remain unique, replacing dual `aria-label` on `summary` with `aria-labelledby`, and prepending `.coordinator h2[tabindex="-1"]:focus-visible, ` before `.screen-record h2[tabindex="-1"]:focus-visible {` in `style.css`), associates `#co-filter-error` with `co-view`/`co-group_by` and `#co-cutoff-note` with `co-as_of`/`co-start`, and adds visible tri-state (`Unknown != 0`) `.flag` / `.flag.danger` + `data-state-cue` cues on heatmap and `Selected records` cells while keeping `\nasync function coordinatorView()` and `#coordinator-records` intact.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused WCAG 2.2 Conformance Tests and Regression Verification

* Intent: Prove all `#230` WCAG 2.2 semantics and regressions via `src/api/tests/test_programme_coordinator_wcag_230.py` and `test_programme_screen_wcag.py` and verify Focused validation suites, linters, and typechecks prior to `rpi-review` and local branch closeout.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Update `test_programme_screen_wcag.py` row-header check and author `src/api/tests/test_programme_coordinator_wcag_230.py`

* Requirement and evidence: `FR-01` through `FR-04`, `AC-01` through `AC-04`, `NFR-01`, `NFR-02`; `test_programme_screen_wcag.py:372-375`, `test_procurement_contractor_screen_wcag.py`, `test_technical_quality_screens_wcag.py` (`C18`).
* Expected result: `test_programme_screen_wcag.py` asserts `<th scope="col">` in `thead` and `<th scope="row">` in `tbody`, and `src/api/tests/test_programme_coordinator_wcag_230.py` exercises `#/role/programme_manager` and `#/role/retrofit_coordinator` routing/RBAC/loader contracts, `programme-queue` row headers/state cues/`aria-describedby`/jump focus, and `#/coordinator` jump focus/`aria-describedby`/non-colour heatmap & stop cues/plain-language copy.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Execute Focused validation suites (`unittest`, `node --check`, `ruff`, `mypy`)

* Requirement and evidence: `AC-04`, `NFR-01`, `NFR-02`; Caller prompt Focused validation instructions (single local commit and rebase onto `origin/feat/demo-233-same-home-tensions-0825` under `AC-05` execute at closeout immediately after `rpi-review` persists its review log and `Follow-up` state record).
* Expected result: All targeted `src/api` and `src/core` tests, `node --check`, `ruff check`, `ruff format --check`, and `mypy` pass cleanly with zero `sys.modules` mutation and zero modifications to `test_accessibility_baseline.py`, `test_content_standard.py`, or `scenario-manifest.json` inputs.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md

## Dependencies

* `origin/feat/demo-233-same-home-tensions-0825` (`a1d0be5f6`): Parent integration branch providing `ROLE_HASH_SCREENS`, `screenRecordTable`, `stateCue`, and standalone `[tabindex="-1"]` CSS focus rules from `#228` and `#231`.
* Node.js (`node`) and Python 3 environment with `ruff` and `mypy`: Required by Node VM DOM tests and Focused validation checks.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `2026-11-15` `PC-001` [High]: CSS selector ordering vs `test_technical_quality_screens_wcag.py` | Applied directly | Kept `style.css:374` (`[tabindex="-1"]:focus`) untouched and specified prepending `.coordinator h2[tabindex="-1"]:focus-visible, ` before `.screen-record h2[tabindex="-1"]:focus-visible {` so `.screen-record h2[tabindex="-1"]:focus-visible` remains immediately followed by `{`. |
| `2026-11-15` `PC-002` [High]: Duplicate nested `region` landmarks, dual naming on `summary`, and missing `#map-title` jump target | Applied directly | Left `table()` outer `<section class="card">` unlabelled so inner `.table-scroll[role="region"]` remains unique (`test_coordinator_api.py:293`), replaced `"aria-label"` with `"aria-labelledby": "coordinator-summary-heading"` on `summary`, and added `aria-labelledby="map-title"` + `h2#map-title[tabindex="-1"]` in `mapPanel` as the 6th of 7 ordered jump links. |
| `2026-11-15` `PC-003` [High]: `null`/`Unknown` conflated with `zero`/`no-stop` and `.heat-present` visually colour-only | Applied directly | Added explicit tri-state (`present` / `zero` / `unknown` for `cell.count` and `stopped` / `no-stop` / `unknown` for `row.stopped`) visible `.flag` / `.flag.danger` badges + `data-state-cue` attributes (`Unknown != 0`) plus non-colour inset border on `.coordinator .heat-present` and `null`/non-boolean test cases in `P03-T01`. |
| `2026-11-15` `PC-004` [Medium]: Jump nav helper consistency on `#/coordinator` | Applied directly | Standardized `P02-T01` on existing `contractorJumpLinks(..., "Jump to a coordinator section")` (`class: "screen-links"` with `2.5rem` target height and `320px` flex-wrap). |
| `2026-11-15` `PC-005` [Low]: Redundant `role="status"` on static `programmeFunnel` prose | Applied directly | Omitted `role="status"` from static `programmeFunnel` and static unblocked-warning paragraphs in `P01-T02`, keeping `data-state-cue` and `.status-line.wait` styling. |
| Residual risk: Automated DOM/VM checks vs human AT sign-off | Accepted by boundary | Automated tests verify engineered DOM/ARIA/keyboard semantics only; assistive-technology and lived-experience acceptance remain tracked under `#151` and `#155` (`Refs #230`, never `Closes #230`). |

## Follow-Up Items

* Execute manual assistive-technology and screen-reader validation across `programme-queue` (`#/role/programme_manager`, `#/role/retrofit_coordinator`) and `#/coordinator` under issues `#151` and `#155` before transitioning `#230` from `Refs #230` to `Closes #230` (Owner: human accessibility / UX reviewer).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/programme-coordinator-wcag-230-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None
