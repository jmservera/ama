<!-- markdownlint-disable-file -->
# RPI Plan Critique: Programme Coordinator WCAG 2.2 Verification and Screen Enhancements (#230)

## Metadata

* Task ID: 2026-11-15-programme-coordinator-wcag-230
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/programme-coordinator-wcag-230-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver GitHub issue #230 programme coordinator WCAG 2.2 AA verification and screen enhancements on branch `feat/demo-230-pm-wcag` targeting stacked parent `origin/feat/demo-233-same-home-tensions-0825` (`a1d0be5f6`), preserving `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_content_standard.py`, and core `scenario-manifest.json` guards under the focused validation tier (`unittest`, `node --check`, `ruff`, `mypy`; without running `tools/rpi-checks.py`), ending in a single clean `Refs #230` commit with no `git push`.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/programme-coordinator-wcag-230-research.md, .copilot-tracking/plans/2026-11-15/programme-coordinator-wcag-230-plan.md, .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md, src/api/src/zava_forward/api/web/role-screens.js, src/api/src/zava_forward/api/web/app.js, src/api/src/zava_forward/api/web/style.css, src/api/tests/test_programme_screen.py, src/api/tests/test_programme_screen_wcag.py, src/api/tests/test_technical_quality_screens_wcag.py, src/api/tests/test_coordinator_api.py, src/api/tests/test_accessibility_baseline.py, src/api/tests/test_content_standard.py, src/api/tests/test_map_fullscreen.py, src/api/tests/test_epic149_form_error_summary_associations.py, src/api/checks/role_screens_browser_check.py, src/api/checks/specialist_keyboard_browser_check.py, src/api/checks/programme_paging_browser_check.py, src/api/checks/connected_home_browser_check.py, and src/api/checks/atlas_tensions_browser_check.py.
* Decisions, dependencies, and acceptance criteria considered: `FR-01` through `FR-04`, `NFR-01` through `NFR-02`, `AC-01` through `AC-05`, phases `P01` through `P03` (`P01-T01`, `P01-T02`, `P02-T01`, `P03-T01`, `P03-T02`), stacked parent dependency `a1d0be5f6` (#231), and issue #155 assistive-technology / lived-experience boundary (`Refs #230` only, never `Closes #230`).
* Assessment boundary: Assesses technical credibility, DOM/ARIA/WCAG 2.2 AA semantics, fail-closed governance rules, and test/regression compatibility against the supplied artifacts and worktree codebase at `a1d0be5f6`. Does not establish assistive-technology, screen-reader, or user acceptance, which remain gated on issue #155.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-01 / AC-01 / P01-T01 | Covered | Adding `#/role/programme_manager` and `#/role/retrofit_coordinator` to `ROLE_HASH_SCREENS` in `src/api/src/zava_forward/api/web/role-screens.js` cleanly reuses `isRoleScreensDestination(baseHash)` (`src/api/src/zava_forward/api/web/app.js:378`), `programmeKeepScope` (`role-screens.js:398-413`), and existing `role="alert"` denial handling (`role-screens.js:117`). |
| FR-02 / AC-02 / P01-T02 | Partial | Row headers (`<th scope="row">`) and `.flag` / `.status-line.wait` cues preserve existing `test_programme_screen.py` and browser-check selectors, and `P03-T02` properly updates `test_programme_screen_wcag.py:373`; however, `P01-T02` attaches `role="status"` live-region semantics to static `programmeFunnel` prose (`PC-005`). |
| FR-03 / AC-03 / P02-T01 | Partial | `P02-T01` breaks `test_technical_quality_screens_wcag.py:293-301` CSS regexes (`PC-001`), creates duplicate-named `region` landmarks around `.table-scroll[role="region"]` that break Playwright strict mode in `test_coordinator_api.py:293`, leaves dual `aria-label` + `aria-labelledby` on `summary`, omits `#map-title` (`Map of open cases`) from coordinator jump navigation/landmarks (`PC-002`), and uses undefined `.screen-jumps` instead of `.screen-links` (`PC-004`). |
| FR-04 / NFR-02 / AC-03 / AC-04 / P02-T01 | Partial | `P02-T01` maps `cell.count === null` (`Unknown`) to `data-state-cue="zero"` / `"none recorded"` and treats non-boolean/missing `row.stopped` as `"No current stop recorded"`, violating `Unknown != 0`, and leaves `.heat-present` visually distinguished by background colour alone for sighted and forced-colors users (`PC-003`). |
| NFR-01 / AC-05 / P03-T01 / P03-T02 | Partial | Preserves `aria-invalid` count (`9`), `h("table", {},` count (`>= 14`), `position:fixed` count (`<= 2`), content-standard lexicon, and focused validation commands, provided `PC-001` through `PC-005` are corrected in `P02-T01`, `P03-T01`, and `P03-T02`. |
| Research C1-C19, W1 | Covered | Supplied research accurately identifies `ROLE_HASH_SCREENS`, `programme-queue`, `#/coordinator`, counted baseline invariants, and issue #230 / #155 boundaries; only two post-#231 details in `style.css` and `app.js` drifted when translating research into `P02-T01` (`PC-001`, `PC-002`, `PC-004`). |

## Verdict

* Verdict: Revise
* Rationale: Phase 1 route aliasing and `programme-queue` table/state-cue plans are largely sound, but Phase 2 (`P02-T01`) contains three High-severity defects and one Medium-severity defect that would cause an immediate unit-test regression in `test_technical_quality_screens_wcag.py`, create duplicate-named ARIA `region` landmarks that fail Playwright strict mode in `test_coordinator_api.py`, conflate `Unknown` (`null`) coordinator counts/stop flags with `zero` / `no-stop` while leaving `.heat-present` visually colour-only (`WCAG 1.4.1`), and render `#/coordinator` jump links with an undefined `.screen-jumps` CSS class lacking `.screen-links` spacing and 40px target height. All five findings are direct, bounded planner corrections requiring no user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: P02-T01 CSS selector edit assumes stale style.css rules and breaks test_technical_quality_screens_wcag.py

* Related IDs: FR-03, NFR-01, AC-03, AC-05, P02, P02-T01, C7, C11
* Evidence: .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md (`P02-T01`, `style.css` bullet); src/api/src/zava_forward/api/web/style.css (lines 377-378); src/api/tests/test_technical_quality_screens_wcag.py (lines 293-301).
* Concern: `P02-T01` instructs the implementer to widen `.screen-record h2[tabindex="-1"]:focus-visible` to `.screen-record h2[tabindex="-1"]:focus-visible,.coordinator h2[tabindex="-1"]:focus-visible` while `"preserving [tabindex=\"-1\"]:focus{outline:none}"`. On parent `a1d0be5f6` (#231), `style.css:377` actually sets `[tabindex="-1"]:focus { outline: var(--focus-w) solid var(--focus-ink); outline-offset: var(--focus-off); box-shadow: 0 0 0 var(--focus-off) var(--focus); }`, and `test_technical_quality_screens_wcag.py:293-301` enforces both `r'\[tabindex="-1"\]:focus\s*\{\s*outline:\s*var\(--focus-w\)\s+solid\s+var\(--focus-ink\)'` and `r'\.screen-record\s+h2\[tabindex="-1"\]:focus-visible\s*\{[^}]*outline:\s*var\(--focus-w\)\s+solid\s+var\(--focus-ink\)'`. Placing `,.coordinator h2[tabindex="-1"]:focus-visible` immediately after `.screen-record h2[tabindex="-1"]:focus-visible` inserts a comma before `{` and fails the second regex; reverting `[tabindex="-1"]:focus` to `outline:none` fails the first regex and removes programmatic focus outlines on `programme-queue`'s `<div tabindex="-1">` jump targets.
* Impact: Guaranteed test regression in `src/api/tests/test_technical_quality_screens_wcag.py` (`AC-05`, `NFR-01`) and potential loss of focus visibility (`WCAG 2.4.7`) on programmatic jump targets.
* Smallest useful change: Update `P02-T01` in `.copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md` (and `P02` summary in `.copilot-tracking/plans/2026-11-15/programme-coordinator-wcag-230-plan.md`) to keep `style.css:377` (`[tabindex="-1"]:focus { outline: var(--focus-w) solid var(--focus-ink); ... }`) intact and either prepend `.coordinator h2[tabindex="-1"]:focus-visible, ` before `.screen-record h2[tabindex="-1"]:focus-visible { ... }` or add a separate `.coordinator h2[tabindex="-1"]:focus-visible` rule so `.screen-record h2[tabindex="-1"]:focus-visible` remains immediately followed by `{`.
* Action owner: planning parent (rpi-plan)
* Exact resolving evidence: Revised `P02` / `P02-T01` specification in `.copilot-tracking/plans/2026-11-15/programme-coordinator-wcag-230-plan.md` and `.copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md` preserving `style.css:377` and keeping `.screen-record h2[tabindex="-1"]:focus-visible` immediately before `{`.
* Decision route: Direct planner correction (no user decision required).

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: P02-T01 creates duplicate-named nested region landmarks, leaves dual naming on coordinator-summary, and omits Map of open cases (#map-title)

* Related IDs: FR-03, NFR-01, AC-03, AC-05, P02, P02-T01, P03-T01, C9
* Evidence: .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md (`P02-T01`); src/api/src/zava_forward/api/web/app.js (lines 2530-2538, 2768-2773, 2800-2826); src/api/tests/test_coordinator_api.py (lines 293-295); src/api/tests/test_map_fullscreen.py (lines 14-24).
* Concern: Three landmark/navigation defects occur in `coordinatorView()` under `P02-T01`:
  1. `table(title, headers, rows)` (`app.js:2768-2771`) already renders an inner `<div class="table-scroll" tabindex="0" role="region" aria-label="${title}">` named `"Heatmap of current cases"`, `"Lifecycle funnel: current and observed cases"`, and `"Selected records"`. Binding the outer `<section class="card">` in `table()` via `aria-labelledby` to the `<h2>` with the exact same `title` creates three pairs of nested `region` landmarks with identical accessible names (violating ARIA APG landmark uniqueness) and breaks Playwright strict mode at `src/api/tests/test_coordinator_api.py:293` (`page.get_by_role("region", name="Selected records", exact=True)` resolves to 2 elements).
  2. `summary` (`app.js:2772`) already sets `"aria-label": "Coordinator denominator and coverage"`; adding `"aria-labelledby": "coordinator-summary-heading"` without removing `"aria-label"` leaves redundant, conflicting naming attributes on the same `<section>`.
  3. `mp.box` (`app.js:2530-2538`) renders `<section class="card map-panel">` with `<h2 id="map-title">Map of open cases</h2>` directly between `Record selection` and `Selected records` (`app.js:2825`). `P02-T01` omits `map-title` from the `Coordinator sections` jump nav and leaves `section.map-panel` without `aria-labelledby="map-title"` and `h2#map-title` without `tabindex: -1`, even though the Leaflet map is the largest multi-stop keyboard block on `#/coordinator` and `FR-03` requires every major `<h2>` section on `#/coordinator` to be a named landmark reachable via keyboard jump links.
* Impact: Fails ARIA landmark uniqueness, breaks `test_coordinator_api.py:293` under Playwright strict mode, and omits `#/coordinator`'s 7th `<h2>` section (`Map of open cases`) from section-jump bypass (`WCAG 2.4.1`, `1.3.1`, `2.4.6`).
* Smallest useful change: Revise `FR-03`, `P02-T01`, and `P03-T01` so that: (a) `table(title, headers, rows)` puts `id` and `tabindex: -1` on its `<h2>` for jump-link targeting while leaving the outer `<section class="card">` unlabelled so the inner `.table-scroll[role="region"][aria-label=title]` remains the single unique `region` landmark for those three tables (retaining `id="coordinator-records"` uniquely on `records.querySelector(".table-scroll")`); (b) `summary` replaces `"aria-label"` with `"aria-labelledby": "coordinator-summary-heading"`; and (c) `mapPanel`'s `box` (`app.js:2530-2536`) adds `"aria-labelledby": "map-title"` and `tabindex: -1` on `h2#map-title`, with `["map-title", "Map of open cases"]` added as the 6th of 7 ordered jump links before `["coordinator-records-heading", "Selected records"]`.
* Action owner: planning parent (rpi-plan)
* Exact resolving evidence: Updated `FR-03`, `P02-T01`, and `P03-T01` in `.copilot-tracking/plans/2026-11-15/programme-coordinator-wcag-230-plan.md` and `.copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md` specifying all 7 `<h2>` jump targets (including `map-title`), single naming attribute on `summary`, and no duplicate outer `aria-labelledby` on `table()`.
* Decision route: Direct planner correction (no user decision required).

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: P02-T01 conflates null/missing Unknown values with zero/no-stop in #/coordinator state cues and leaves .heat-present visually colour-only

* Related IDs: FR-04, NFR-02, AC-03, AC-04, P02, P02-T01, P03-T01, C9, C19
* Evidence: .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md (`P02-T01`); src/api/src/zava_forward/api/web/app.js (lines 2722, 2788-2793, 2806); src/api/src/zava_forward/api/web/style.css (line 99).
* Concern: Two accessibility and fail-closed data-quality gaps exist in `P02-T01`'s `#/coordinator` state cues:
  1. `number(n)` (`app.js:2722`) renders `null` as `"Unknown"`, yet `P02-T01` specifies `"data-state-cue": cell.count ? "present" : "zero"` and `aria-label` `"${number(cell.count)} current cases (${cell.count ? "present" : "none recorded"})..."`. When `cell.count` is `null` or non-numeric, `Boolean(cell.count)` evaluates to `false`, emitting `data-state-cue="zero"` and `"Unknown current cases (none recorded)..."` in violation of `NFR-02` (`"Unknown is never zero"`). Likewise, `row.stopped ? ... : ...` treats `null`/`undefined` as `"State: No current stop recorded"` and non-boolean strings such as `"false"` as truthy instead of failing closed to `Unknown`.
  2. `.coordinator .heat-present` (`style.css:99`) uses only `background: var(--soft); color: var(--ink)`, which is stripped in `forced-colors: active` mode. Putting the `present` / `zero` / `unknown` state cue exclusively in `data-state-cue` and `aria-label` gives sighted colour-vision-deficient and forced-colors users no visible non-colour styling or textual cue (`WCAG 1.4.1`).
* Impact: Misstates `Unknown` counts/stop states as `zero` / `No current stop recorded` (`NFR-02`) and leaves `.heat-present` cells visually differentiated by background colour alone (`WCAG 1.4.1`, `FR-04`, `AC-03`).
* Smallest useful change: Update `P02-T01` and `P03-T01` in `.copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md` so that: (a) heatmap count cells branch explicitly on `typeof cell.count === "number" && Number.isFinite(cell.count)` (`cell.count > 0` -> `heat-present`, `data-state-cue="present"`, `"present"`; `cell.count === 0` -> `data-state-cue="zero"`, `"none recorded"`; otherwise -> `data-state-cue="unknown"`, `"unknown count"`) AND render a visible non-colour cue (for example a visible `.flag` / text token in the cell or non-colour border/weight rule on `.coordinator .heat-present` that survives `forced-colors`); and (b) `Selected records` stop cells branch strictly on `row.stopped === true` (`"Action needed: Cannot move on"`, `flag danger`, `data-state-cue="stopped"`), `row.stopped === false` (`"State: No current stop recorded"`, `flag`, `data-state-cue="no-stop"`), and fallback (`"State: Unknown (stop state not supplied)"`, `flag`, `data-state-cue="unknown"`), with unit-test coverage for `null`/missing/non-boolean inputs in `P03-T01`.
* Action owner: planning parent (rpi-plan)
* Exact resolving evidence: Updated `P02-T01` and `P03-T01` in `.copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md` covering tri-state `present` / `zero` / `unknown` cues for `cell.count` and `row.stopped` plus a visible non-colour distinguisher on heatmap count cells.
* Decision route: Direct planner correction (no user decision required).

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: P02-T01 uses undefined .screen-jumps class on #/coordinator jump navigation instead of existing .screen-links helper

* Related IDs: FR-03, AC-03, P02, P02-T01, P03-T01, C9, C11
* Evidence: .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md (`P02-T01`); src/api/src/zava_forward/api/web/style.css (lines 364-367); src/api/src/zava_forward/api/web/app.js (lines 1898-1900).
* Concern: `P02-T01` renders `h("nav", { class: "card screen-jumps", "aria-label": "Coordinator sections" }, ...)` with bare `<a>` children. `.screen-jumps` is not defined anywhere in `style.css`; the repository's established jump-navigation class is `.screen-links` (`style.css:364-367`), which sets `display: flex; flex-wrap: wrap; gap: var(--sp-3)` and `.screen-links a { display: inline-flex; align-items: center; min-height: 2.5rem; padding: var(--sp-1) var(--sp-2); ... }`, already wrapped by `contractorJumpLinks(targets, label)` in `app.js:1898-1900` (`data-jump`, `data-jump-target`, `"Go to ${title}"`). Without `.screen-links`, adjacent `<a>` links render inline with zero gap and ~19px inline height, risking WCAG 2.5.8 Target Size Minimum (24x24 CSS px) failure when links wrap at 320px.
* Impact: Unspaced inline jump links on `#/coordinator` lacking 40px (`2.5rem`) touch/pointer target sizing (`WCAG 2.5.8`) and flex-wrap layout at 320px (`WCAG 1.4.10`).
* Smallest useful change: Update `P02-T01` and `P03-T01` in `.copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md` to reuse `contractorJumpLinks(coordinatorSections, "Coordinator sections")` (or a shared helper emitting `class: "screen-links"` / `class: "card screen-links"`, `data-jump`, `data-jump-target`, and `"Go to ${title}"`).
* Action owner: planning parent (rpi-plan)
* Exact resolving evidence: Updated `P02-T01` and `P03-T01` in `.copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md` specifying `.screen-links` instead of undefined `.screen-jumps`.
* Decision route: Direct planner correction (no user decision required).

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: P01-T02 adds redundant role="status" live-region attributes to static programmeFunnel summary paragraphs

* Related IDs: FR-02, NFR-01, AC-02, P01, P01-T02, P03-T02, C4
* Evidence: .copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md (`P01-T02`); src/api/src/zava_forward/api/web/role-screens.js (lines 463-464, 517-524); src/api/tests/test_data_steward_screen_wcag.py (line 189).
* Concern: `P01-T02` adds `role: "status"` to both branches of `programmeFunnel(report)` (`role-screens.js:519,521`). Unlike `#programme-filter-status` and `#programme-page-status` (`role-screens.js:463-464`), which announce dynamic filter and paging updates (`WCAG 4.1.3`), `programmeFunnel(report)` renders static prose once during `overview()` and is never mutated in place. Sibling WCAG slice #229 (`test_data_steward_screen_wcag.py:189`) explicitly avoids adding `role="status"` to static state cues.
* Impact: Creates redundant polite live regions in `programme-queue` overview without supporting any dynamic status message update.
* Smallest useful change: Update `P01-T02` and `P03-T02` in `.copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md` to retain `data-state-cue` (`"unknown"` / `"stage-history"`) and `.status-line.wait` (when `report` is present) on `programmeFunnel` paragraphs while omitting `role: "status"` on static `programmeFunnel` paragraphs.
* Action owner: planning parent (rpi-plan)
* Exact resolving evidence: Updated `P01-T02` and `P03-T02` in `.copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md` omitting `role: "status"` from static `programmeFunnel` prose.
* Decision route: Direct planner correction (no user decision required).

## Strengths and Residual Risk

* Route alias architecture (`P01-T01`) cleanly leverages `ROLE_HASH_SCREENS`, `isRoleScreensDestination(baseHash)`, and `programmeKeepScope` without duplicating route guards or weakening fail-closed role checks.
* Counted baseline invariants in `src/api/tests/test_accessibility_baseline.py` (`9` `aria-invalid` occurrences in `app.js`, `>= 14` `h("table", {},` calls, `<= 2` `position:fixed` rules) and plain-language rules in `src/api/tests/test_content_standard.py` are explicitly respected, avoiding `aria-invalid` edits in `app.js` by binding `#co-filter-error` through `aria-describedby` and `focus()`.
* `P01-T02` and `P03-T02` accurately identify and update the existing `scope="col"`-only assertion at `src/api/tests/test_programme_screen_wcag.py:373` while preserving `programme_paging_browser_check.py` (`querySelector('th, td')`), `connected_home_browser_check.py`, and `atlas_tensions_browser_check.py` selectors.
* Residual risk (explicitly accepted by repository boundary): Node VM DOM contract tests and Playwright checks verify engineered DOM/ARIA/keyboard semantics only and do not establish assistive-technology or lived-experience WCAG acceptance, which remains tracked under issue #155 (`Refs #230`, never `Closes #230`).

## Questions or Blocking Evidence Gaps

* None. All five findings are fully resolved by direct planner updates using existing repository evidence.

## Limitations

* This critique is a static codebase and plan-credibility verification under the caller's read-only source constraint; focused validation suites (`unittest`, `node --check`, `ruff`, `mypy`) were not executed during critique and must run during `rpi-implement` and `rpi-review`.

## Recommended Next Action

* Highest-impact finding: PC-001 (paired with High findings PC-002 and PC-003 in P02-T01)
* Action owner: planning parent (rpi-plan)
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-15/programme-coordinator-wcag-230-plan.md` and `.copilot-tracking/details/2026-11-15/programme-coordinator-wcag-230-phase-details.md` to apply PC-001 through PC-005, then finalize the plan for `rpi-implement` without re-running critique.
* User response required: No
