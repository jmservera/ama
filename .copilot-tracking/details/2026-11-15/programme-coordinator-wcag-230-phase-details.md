<!-- markdownlint-disable-file -->
# RPI Phase Details: Programme Coordinator WCAG 2.2 Verification and Screen Enhancements (#230)

## Metadata

* Task ID: 2026-11-15-programme-coordinator-wcag-230
* Task slug: programme-coordinator-wcag-230
* Related plan: .copilot-tracking/plans/2026-11-15/programme-coordinator-wcag-230-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/programme-coordinator-wcag-230-research.md, docs/reference/research/ux/wcag-conformance-baseline.md, docs/reference/research/ux/design-system.md, docs/reference/research/ux/content-standard.md, docs/reference/research/ux/customer-journeys/programme.md

## Phase Index

| Phase ID | Name                                                                            | Status | Detail sections        |
|----------|---------------------------------------------------------------------------------|--------|------------------------|
| P01      | Programme Queue and Role Route Alias WCAG 2.2 Enhancements                      | Ready  | P01, P01-T01, P01-T02  |
| P02      | Coordinator Flow (`#/coordinator`) Keyboard Jump Navigation and Non-Colour Cues | Ready  | P02, P02-T01           |
| P03      | Focused WCAG 2.2 Conformance Tests, Regression Verification, and Rebased Commit | Ready  | P03, P03-T01, P03-T02  |

<!-- rpi:phase id=P01 -->
## P01: Programme Queue and Role Route Alias WCAG 2.2 Enhancements

### Context

Research (`C2`, `C6`-`C8`, `C16`-`C18`) showed that `programme-queue` in `src/api/src/zava_forward/api/web/role-screens.js` landed in `efe14ef3d` before `#228` (`538462eba`) and `#231` (`a1d0be5f6`) standardized `#/role/*` hash route aliases, `<th scope="row">` record row headers via `screenRecordTable` / `screenTable(..., true)`, `data-jump-target` anchor parity, `aria-describedby` filter descriptions, and Fluent 2 `.flag` / `.status-line.wait` + `data-state-cue` non-colour state wrappers.

### Intent

Bring `programme-queue` and its `#/role/programme_manager` and `#/role/retrofit_coordinator` hash route aliases to full WCAG 2.2 AA parity with `#228` and `#231` without breaking any existing test, counted baseline, or Playwright selector.

### Boundaries

* Included: `ROLE_HASH_SCREENS` and `programme-queue` in `role-screens.js`; `isRoleScreensDestination` in `app.js`.
* Excluded: Changing `programmeJumpNav` `<nav>` `attrs` dict (`{"aria-label": label, "class": "screen-links"}`), changing the 8 existing `programme-queue` jump target IDs, changing `.screen-evidence` `aria-label="Evidence for ${c.id}"`, introducing banned words (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) or the word `ready` inside `programme-queue` connected-home text, or adding any `h("table", {},` literal.

### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: Add `#/role/programme_manager` and `#/role/retrofit_coordinator` to `ROLE_HASH_SCREENS`; upgrade `programmeQueue`, `programmeFunnel`, `programmeJumpNav`, and `programme-queue` `render()`.
* `src/api/src/zava_forward/api/web/app.js`: Add `#/role/programme_manager` and `#/role/retrofit_coordinator` to `isRoleScreensDestination`.

### Dependencies

* None.

### Validation Expectations

* `node --check` passes on `role-screens.js` and `app.js`; `test_programme_screen.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, and `test_workspace_scripts.py` pass without regression.

### Completion Evidence

* Updated `ROLE_HASH_SCREENS`, `isRoleScreensDestination`, and `programme-queue` table/form/state-cue rendering verified by Node VM tests.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Wire `#/role/programme_manager` and `#/role/retrofit_coordinator` route aliases

#### Context

`ROLE_HASH_SCREENS` (`role-screens.js`) and `isRoleScreensDestination` (`app.js`) currently wire six specialist role routes (`building_safety_lead`, `repairs`, `housing_officer`, `resident_engagement`, `procurement`, `contractor`), omitting the programme manager and retrofit coordinator routes (`C6`, `C7`).

#### Intent

Enable `#/role/programme_manager` and `#/role/retrofit_coordinator` (including `?case=`, `?page=`, and `?scope=` query strings) to route cleanly into `roleScreensView()` for `"programme-queue"` with lazy script loading and role access enforcement.

#### Boundaries

* Included: Mapping `"#/role/programme_manager": "programme-queue"` and `"#/role/retrofit_coordinator": "programme-queue"` in `ROLE_HASH_SCREENS` and adding both paths to `isRoleScreensDestination(destination)` in `app.js`.
* Excluded: Modifying existing `test_workspace_scripts.py` cases or altering `.screen-evidence` `aria-label="Evidence for ${c.id}"`.

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: Extend `ROLE_HASH_SCREENS`.
* `src/api/src/zava_forward/api/web/app.js`: Extend `isRoleScreensDestination`.

#### Dependencies

* None.

#### Validation Expectations

* `missingWorkspaceScripts("#/role/programme_manager", false)` returns `["/chat.js", "/role-screens.js"]` for staff and `["/role-screens.js"]` for `Contractor`; permitted roles open `Programme queue and connected home view` and unpermitted roles receive `Screen unavailable` `role="alert"`.

#### Completion Evidence

* Passing route-alias and script-loader assertions in `test_programme_coordinator_wcag_230.py` and `test_workspace_scripts.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add `<th scope="row">`, `aria-describedby`, `data-jump-target`, and Fluent 2 non-colour state cues to `programme-queue`

#### Context

In `role-screens.js`, `programmeQueue` (`Shared queue: returned and handed-off work`), `programmeFunnel` (`Lifecycle and funnel by stage`), and `programme-queue.render` (`Same-home step states`) currently omit `rowHeader = true`, leaving column 0 as `<td>` instead of `<th scope="row">` (`C2`, `C8`). In addition, `#programme-scope` lacks `aria-describedby`, `programmeJumpNav` anchors lack `data-jump-target`, and state cells/banners lack Fluent 2 `.flag` / `.flag.danger` / `.status-line.wait` + `data-state-cue` wrappers (`C2`, `C11`).

#### Intent

Add `<th scope="row">` headers, `aria-describedby` scope-filter wiring, `data-jump-target` anchor parity, and Fluent 2 non-colour badge/banner cues across `programme-queue` while preserving exact visible text strings and zero write controls in connected view.

#### Boundaries

* Included:
  * Pass `true` as 6th `rowHeader` argument to `screenTable("Shared queue: returned and handed-off work", ...)` and format column 1 (`Return reason` / handoff state) in `programmeCell` with `h("span", { class: ..., "data-state-cue": ... }, screenValue(value))` (`"flag danger"` + `"returned"` for `State: Returned.`, `"flag"` + `"handoff"` for `Handoff state:`, and `data-state-cue: "not-returned"` for `State: Not returned`), keeping exact text content.
  * Add `"aria-describedby": "programme-page-status programme-filter-status"` to `#programme-scope` `<select>`.
  * Use `screenRecordTable` for `"Lifecycle and funnel by stage"` and add `data-state-cue` (`"unknown"` / `"stage-history"`) + `.status-line.wait` (when report exists) to `programmeFunnel` paragraphs without redundant `role: "status"` on static prose, preserving exact paragraph strings (`PC-005`).
  * Add `"data-jump-target": id` to `<a>` children in `programmeJumpNav` while preserving `nav` `attrs` (`{ "aria-label": label, "class": "screen-links" }`) and the exact 8 jump target IDs.
  * In `programme-queue.render()`, add `class: "status-line wait", "data-state-cue": "warning"` (without redundant `role: "status"` on static prose) to the unblocked warning paragraph (`"State: Warning. No blocker is recorded, which does not confirm readiness."`) and pass `rowHeader = true` plus a column-1 state badge cell formatter (`"flag danger"` + `"action-needed"` for `Blocked*`, `"flag"` + `"warning"` for `No recorded blocker`) to `screenTable("Same-home step states", ...)`, keeping exact cell text (`"Blocked"`, `"Blocked: evidence missing"`, `"No recorded blocker"`).
* Excluded: Adding any `h("table", {},` literal, banned glossary term, or `ready` wording.

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: `programmeCell`, `programmeQueue`, `programmeFunnel`, `programmeJumpNav`, and `programme-queue.render`.

#### Dependencies

* None.

#### Validation Expectations

* `test_programme_screen.py` passes completely unchanged; `test_programme_screen_wcag.py` passes with updated `<th scope="col">` (`thead`) + `<th scope="row">` (`tbody`) check; `test_content_standard.py` and `test_accessibility_baseline.py` pass unchanged.

#### Completion Evidence

* Verified DOM structure and state cues across `overview`, `overviewAll`, `overviewDown`, `blocked`, and `ok` renders.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Coordinator Flow (`#/coordinator`) Keyboard Jump Navigation and Non-Colour State Cues

### Context

`coordinatorView()` (`#/coordinator` in `src/api/src/zava_forward/api/web/app.js`) is the primary coordinator workbench view for population filtering, denominator/coverage checks, stage/group heatmaps, lifecycle funnel inspection, and record drill-down (`C3`). Unlike the specialist screens upgraded in `#228` and `#231`, `coordinatorView()` currently has no keyboard section-jump navigation, no focusable section headings or `aria-labelledby` landmarks, no `aria-describedby` wiring for `#co-filter-error` or `#co-cutoff-note`, and relies on `.heat-present` background colour (`style.css`) and bare `Can move on` text without explicit non-colour status badges or `data-state-cue` attributes (`C3`, `C10`).

### Intent

Add WCAG 2.2 AA keyboard section-jump navigation, programmatic focus styling, `aria-describedby` form associations, and non-colour textual/badge cues to `#/coordinator` while preserving all counted static baselines and `test_map_fullscreen.py` boundaries.

### Boundaries

* Included: `coordinatorView()` body in `src/api/src/zava_forward/api/web/app.js` and `.coordinator h2[tabindex="-1"]:focus-visible` selector in `src/api/src/zava_forward/api/web/style.css`.
* Excluded: Placing any code between the end of `mapPanel` and `"\nasync function coordinatorView()"` (`test_map_fullscreen.py` split guard `C15`), adding `setAttribute("aria-invalid", "true")` (`sites == 9` guard `C12`, `C13`), adding any `h("table", {},` literal (`tables == 14` guard `C12`), removing `#coordinator-records` (`C15`), or using banned glossary words (`C14`).

### Likely Targets

* `src/api/src/zava_forward/api/web/app.js`: `mapPanel` (`#map-title` landmark/focus target) and inside `coordinatorView()`.
* `src/api/src/zava_forward/api/web/style.css`: Prepend `.coordinator h2[tabindex="-1"]:focus-visible, ` before `.screen-record h2[tabindex="-1"]:focus-visible {` (keeping `style.css:374` `[tabindex="-1"]:focus` untouched and keeping `.screen-record h2[tabindex="-1"]:focus-visible` immediately before `{` per `PC-001`) and add an inset border distinguisher to `.coordinator .heat-present`.

### Dependencies

* P01-T01 (`app.js` co-edit).

### Validation Expectations

* `test_map_fullscreen.py`, `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_technical_quality_screens_wcag.py`, `test_content_standard.py`, and `test_programme_coordinator_wcag_230.py` all pass.

### Completion Evidence

* Verified jump link click focus/scroll delegation, `aria-labelledby`/`aria-describedby` attributes, and non-colour cues in `coordinatorView()`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add keyboard section-jump nav, focusable section headings, `aria-describedby` associations, and non-colour state cues in `coordinatorView()` and `style.css`

#### Context

`app.js` already attaches a global `document.addEventListener("click", ...)` handler for `a[data-jump]` that calls `preventDefault()`, `target?.focus?.()`, and `target?.scrollIntoView?.({ block: "start" })` (`C9`), and `style.css` already provides `[tabindex="-1"] { scroll-margin-top: var(--sp-4); }` and `[tabindex="-1"]:focus` two-tone focus rings (`C10`).

#### Intent

Wire `coordinatorView()` into the shared `a[data-jump]` keyboard jump system, connect filter error and date-cutoff hints via `aria-describedby`, and add explicit non-colour textual and `.flag` cues to heatmap and selected-record cells.

#### Boundaries

* Included:
  * Reuse `contractorJumpLinks` (`app.js:1898`) below the `Coordinator flow` header row (`<nav role="navigation" aria-label="Jump to a coordinator section" class="screen-links">`) with seven ordered `a[data-jump]` + `data-jump-target` links (`["coordinator-filters-heading", "Case population filters"]`, `["coordinator-summary-heading", "Denominator and coverage"]`, `["coordinator-heatmap-heading", "Heatmap of current cases"]`, `["coordinator-funnel-heading", "Lifecycle funnel"]`, `["coordinator-selection-heading", "Record selection"]`, `["map-title", "Map of open cases"]`, `["coordinator-records-heading", "Selected records"]`) (`PC-002`, `PC-004`).
  * Give all seven `<h2>` elements their matching `id` and `tabindex: "-1"`: bind `form` (`aria-labelledby="coordinator-filters-heading"`), `summary` (replace `"aria-label"` with `"aria-labelledby": "coordinator-summary-heading"`), `Record selection` (`aria-labelledby="coordinator-selection-heading"`), and `mapPanel` `box` (`aria-labelledby="map-title"` with `h2#map-title[tabindex="-1"]`), while keeping `table(title, headers, rows, headingId)` outer `<section class="card">` unlabelled so each inner `.table-scroll[role="region"][aria-label=title]` remains a single unique `region` landmark (`test_coordinator_api.py:293`) with zero extra `h("table", {},` literals (`PC-002`).
  * Give `error` `id: "co-filter-error"` (`class: "err", role: "alert"`), give the cutoff note paragraph `id: "co-cutoff-note"`, attach `"aria-describedby": "co-filter-error"` + change listener clearing `error.textContent = ""` on `values.view` and `values.group_by` (without `setAttribute("aria-invalid", "true")`), and attach `"aria-describedby": "co-cutoff-note"` on `values.as_of` and `values.start`.
  * On heatmap count `<td>`, branch tri-state on `typeof cell.count === "number" && Number.isFinite(cell.count)` (`cell.count > 0` -> `heat-count heat-present`, `data-state-cue="present"`, visible `.flag` `"Present"`, link `aria-label` `(present)`; `cell.count === 0` -> `heat-count`, `data-state-cue="zero"`, visible `.flag` `"None"`, link `aria-label` `(none recorded)`; otherwise -> `heat-count`, `data-state-cue="unknown"`, visible `.flag` `"Unknown"`, link `aria-label` `(unknown count)` so `Unknown != 0`) (`PC-003`).
  * On `Selected records` `Can move on` `<td>`, branch strictly on `row.stopped === true` (`h("span", { class: "flag danger", "data-state-cue": "stopped" }, "Action needed: Cannot move on")`), `row.stopped === false` (`h("span", { class: "flag", "data-state-cue": "no-stop" }, "State: No current stop recorded")`), and fallback (`h("span", { class: "flag", "data-state-cue": "unknown" }, "State: Unknown (stop state not supplied)")`) (`PC-003`).
  * In `style.css`, add `box-shadow:inset 3px 0 0 var(--brand)` to `.coordinator .heat-present` and prepend `.coordinator h2[tabindex="-1"]:focus-visible, ` immediately before `.screen-record h2[tabindex="-1"]:focus-visible {` while keeping `style.css:374` (`[tabindex="-1"]:focus`) untouched (`PC-001`, `PC-003`).
* Excluded: Any top-level helper inserted between `mapPanel` and `"\nasync function coordinatorView()"` that would disturb `test_map_fullscreen.py`.

#### Likely Targets

* `src/api/src/zava_forward/api/web/app.js`: `coordinatorView()`.
* `src/api/src/zava_forward/api/web/style.css`: Focus-visible heading selector.

#### Dependencies

* P01-T01.

#### Validation Expectations

* All six jump links focus their target `h2[tabindex="-1"]` without mutating `location.hash`; required-select empty submit populates `#co-filter-error` referenced by `aria-describedby` and focuses the missing control; heatmap and `Selected records` cells expose `data-state-cue` and explicit plain-language state text.

#### Completion Evidence

* Node VM DOM execution in `test_programme_coordinator_wcag_230.py` + green `test_map_fullscreen.py` and `test_technical_quality_screens_wcag.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused WCAG 2.2 Conformance Tests and Regression Verification

### Context

To prove `#230` WCAG 2.2 conformance sustainably and meet Focused validation requirements, we need both updated row-header verification in `test_programme_screen_wcag.py` and a comprehensive, isolated Node VM + static contract suite `src/api/tests/test_programme_coordinator_wcag_230.py` (with zero `sys.modules` mutation), followed by Focused test/lint/typecheck runs prior to `rpi-review` and post-review single-commit closeout (`Refs #230`).

### Intent

Deliver automated test proof for every `#230` WCAG 2.2 enhancement and confirm zero regressions across `src/api` and `src/core`.

### Boundaries

* Included: `src/api/tests/test_programme_screen_wcag.py`, `src/api/tests/test_programme_coordinator_wcag_230.py`, and Focused test/lint/typecheck runs (with Git commit + rebase onto `origin/feat/demo-233-same-home-tensions-0825` executed after `rpi-review` writes the review log and `Follow-up` state record).
* Excluded: Modifying `test_accessibility_baseline.py` or `test_content_standard.py`, running `tools/rpi-checks.py`, or running `git push`.

### Likely Targets

* `src/api/tests/test_programme_screen_wcag.py`: Update `th` `scope` check in `test_queue_controls_live_regions_tables_and_pager_focus_handoff_are_keyboard_accessible` to assert `<th scope="col">` in `thead` and `<th scope="row">` in `tbody`.
* `src/api/tests/test_programme_coordinator_wcag_230.py`: New focused WCAG 2.2 test module.

### Dependencies

* P01, P02.

### Validation Expectations

* `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q` in `src/api`, `python3 -m unittest discover -s tests -q` in `src/core` (or targeted `test_scenario_manifest.py` + `test_needs_inventory.py`), `node --check`, `ruff check`, and `mypy` all exit `0`.

### Completion Evidence

* Passing test/linter outputs in `.copilot-tracking/changes/2026-11-15/programme-coordinator-wcag-230-changes.md`, post-implementation review in `.copilot-tracking/reviews/logs/2026-11-15/programme-coordinator-wcag-230-review.md`, and clean `git status --short` on `feat/demo-230-pm-wcag` rebased onto `origin/feat/demo-233-same-home-tensions-0825`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Update `test_programme_screen_wcag.py` row-header check and author `src/api/tests/test_programme_coordinator_wcag_230.py`

#### Context

`test_programme_screen_wcag.py` previously asserted `all(h["attrs"].get("scope") == "col" for h in headers)` before `programme-queue` adopted `<th scope="row">` row headers (`C18`). In addition, no dedicated WCAG 2.2 suite currently tests `#/role/programme_manager` and `#/role/retrofit_coordinator` route aliases or `#/coordinator` (`coordinatorView()`) keyboard jump navigation, `aria-describedby` associations, and non-colour state cues.

#### Intent

Update `test_programme_screen_wcag.py` to assert both `scope="col"` (`thead`) and `scope="row"` (`tbody` column 0), and create `src/api/tests/test_programme_coordinator_wcag_230.py` using subprocess `node -e` VM harnesses (zero `sys.modules` side effects) covering both `programme-queue` (`#/role/*` aliases + DOM cues) and `#/coordinator` (`coordinatorView()`).

#### Boundaries

* Included:
  * Update `test_programme_screen_wcag.py` table header check so every `thead th` has `scope == "col"` and every `tbody tr` starts with `<th scope="row">`.
  * Create `src/api/tests/test_programme_coordinator_wcag_230.py` testing:
    1. `#/role/programme_manager` and `#/role/retrofit_coordinator` lazy script requirements (`missingWorkspaceScripts`), top-nav `aria-current="page"` on `#/screens`, permitted-role rendering (`Retrofit Programme Manager`, `Programme Support Officer`, `Retrofit Coordinator`) with and without `?case=C-1`, and unpermitted-role `Screen unavailable` `role="alert"` (`Contractor`, `Resident Liaison Officer`).
    2. `programme-queue` `<th scope="row">` row headers across all 3 tables, `#programme-scope` `aria-describedby="programme-page-status programme-filter-status"`, `data-jump-target` attributes, and Fluent 2 `.flag` / `.flag.danger` / `.status-line.wait` + `data-state-cue` non-colour state wrappers without write controls or readiness claims.
    3. `#/coordinator` (`coordinatorView()`) keyboard jump `<nav>` (`contractorJumpLinks` `a[data-jump]`) focusing and scrolling all 7 `h2[tabindex="-1"]` section headings (including `#map-title`) without changing `location.hash`, unique landmark naming (no duplicate `region` names around `.table-scroll` and no dual `aria-label` on `summary`), `#co-filter-error` (`co-view`, `co-group_by`) and `#co-cutoff-note` (`co-as_of`, `co-start`) `aria-describedby` associations + validation focus/recovery, tri-state (`count > 0`, `0`, `null`) heatmap visible `.flag` + `data-state-cue` and `(present)` / `(none recorded)` / `(unknown count)` link `aria-label`, and `Selected records` `<th scope="row">`, `#coordinator-records` scroll region, and tri-state (`true`, `false`, `null`) `.flag.danger` / `.flag` stop/clear/unknown state cues.
    4. CSS focus-visible rule contract (`.coordinator h2[tabindex="-1"]:focus-visible`, `.screen-record h2[tabindex="-1"]:focus-visible`, `[tabindex="-1"]:focus`) and plain-ASCII / plain-language copy checks.
* Excluded: Editing `test_accessibility_baseline.py` or `test_content_standard.py`.

#### Likely Targets

* `src/api/tests/test_programme_screen_wcag.py`
* `src/api/tests/test_programme_coordinator_wcag_230.py`

#### Dependencies

* P01, P02.

#### Validation Expectations

* Both test modules pass standalone and within full `src/api` `unittest discover`, `ruff check`, and `mypy`.

#### Completion Evidence

* Zero failures across `test_programme_screen_wcag.py` and `test_programme_coordinator_wcag_230.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Execute Focused validation suites (`unittest`, `node --check`, `ruff`, `mypy`)

#### Context

All Focused verification suites must pass cleanly before transitioning to `rpi-review`, and again after rebasing onto `origin/feat/demo-233-same-home-tensions-0825` when committing all implementation and `.copilot-tracking/` artifacts (`changes`, `review`, and `Follow-up` `state.json`).

#### Intent

Verify all Focused checks pass cleanly across `src/api` and `src/core`, `node --check`, `ruff check`, `ruff format --check`, and `mypy`.

#### Boundaries

* Included: `node --check`, `unittest` suites in `src/api` and `src/core`, `ruff check`, `ruff format --check`, and `mypy` (with Git noreply email configuration, staging, single clean commit, and rebase onto `origin/feat/demo-233-same-home-tensions-0825` completed immediately after `rpi-review` artifacts are persisted).
* Excluded: `tools/rpi-checks.py` and `git push`.

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/programme-coordinator-wcag-230-changes.md`

#### Dependencies

* P03-T01.

#### Validation Expectations

* Focused `unittest` suites in `src/api` and `src/core`, `node --check`, `ruff check`, `ruff format --check`, and `mypy` all exit `0`.

#### Completion Evidence

* Passing Focused verification outputs recorded in `.copilot-tracking/changes/2026-11-15/programme-coordinator-wcag-230-changes.md`.

#### Unresolved Items

* None.
