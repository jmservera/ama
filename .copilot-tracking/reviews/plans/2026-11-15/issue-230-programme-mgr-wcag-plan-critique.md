<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #230 Programme Manager and Coordinator Screens WCAG 2.2 Compliance

## Metadata

* Task ID: 2026-11-15-issue-230-programme-mgr-wcag
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-230-programme-mgr-wcag-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Complete the remaining engineering acceptance criterion on GitHub issue #230 (`Programme manager and coordinator screens`): WCAG 2.2 baseline (#151) compliance with explicit non-colour textual state meaning and keyboard section jump navigation (`nav aria-label` jump links, `tabindex="-1"` section targets, delegated jump focus, and keyboard-accessible controls) matching #225, #226, and #227, while preserving all four delivered #230 criteria, passing `test_*programme*.py`, `mypy`, and `ruff` in `src/api`, and committing locally on `feat/ux-230-programme-mgr-wcag` with `Refs #230` and the Copilot trailer without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/issue-230-programme-mgr-wcag-research.md (`C1` to `C15`, `W1`), src/api/src/zava_forward/api/web/role-screens.js, src/api/tests/test_programme_screen.py, src/api/tests/test_programme_screen_wcag.py, src/api/tests/test_accessibility_baseline.py, src/api/tests/test_content_standard.py, src/api/tests/test_role_screens_conformance.py, src/api/tests/test_role_screens_tensions_same_home.py, src/api/tests/test_role_screens_stage_map_focus.py, src/api/tests/test_epic149_role_workbench_heading_hierarchy.py, src/api/tests/test_connected_home_check.py, src/api/tests/test_atlas_tensions_checker.py, src/api/tests/test_specialist_keyboard_check.py, src/api/checks/programme_paging_browser_check.py, src/api/checks/atlas_tensions_browser_check.py, src/api/checks/connected_home_browser_check.py, src/api/checks/specialist_keyboard_browser_check.py, and src/api/checks/role_screens_browser_check.py.
* Decisions, dependencies, and acceptance criteria considered: FR-01 through FR-05, NFR-01 through NFR-02, AC-01 through AC-05, shared `screenJumpNav` / `screenJumpTarget` / delegated `a[data-jump]` handler in src/api/src/zava_forward/api/web/role-screens.js, Focused Tier validation governance, and non-conformance boundary (#155 human/AT sign-off remains open).
* Assessment boundary: Evaluates plan and phase-details credibility, DOM/test-harness invariants, typing/lint gates, and repository workflow rules strictly against supplied artifacts and target source/test/check files; does not execute implementation edits, live browser runs, or assistive-technology walkthroughs.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-01 (`overview()` jump `<nav>` + 4 `tabindex="-1"` targets) | Covered | `P01-T01` maps all four top-level panels in `programme-queue.overview()` to `screenJumpNav` and `screenJumpTarget`, keeping `<= 4` jump links (`5 <= 6` Tabs to `#programme-next` in `programme_paging_browser_check.py:210`). |
| FR-02 (`render()` jump `<nav>` + 4 disjoint `tabindex="-1"` targets) | Partial | Disjoint IDs and zero `<button>` elements are sound, but `P01-T01` instructs wrapping "its four target panels" when `render()` has only three target `screenPanel`s and `Same-home step states` must stay nested inside ``screenPanel(`Connected view for ${c.id}`, ...)`` (`PC-001`). |
| FR-03 (Delegated `a[data-jump]` click `preventDefault()` + `.focus()`) | Covered | Reuses existing listener at `src/api/src/zava_forward/api/web/role-screens.js:268-275`; `P02-T01` tests all 8 jump links and missing-target resilience. |
| FR-04 (Explicit non-colour textual state prefixes on queue, funnel, and steps) | Covered | `P01-T02` prefixes preserve `test_programme_screen.py` substrings (including `Reason 1"` at line 206 and `assertNotIn("Blocked", clear)` at line 381), `test_content_standard.py` banned words, and `role_screens_browser_check.py:657,663` (`PROGRAMME_STATES` and `\bready\b` absence). |
| FR-05 (Native keyboard queue controls, `aria-live="polite"`, focus handoff) | Partial | `FR-05` and `P02-T01` require VDOM tests for `role="status"` `aria-live="polite"` regions in `overview()`, but `programmeQueue()` at `role-screens.js:412-413` currently omits `"aria-live": "polite"` and `P01` does not schedule adding it (`PC-002`). |
| NFR-01 (Static accessibility, content-standard, conformance, and stage-map guards) | Partial | Covers `test_accessibility_baseline.py`, `test_content_standard.py`, `test_role_screens_conformance.py`, and `test_role_screens_stage_map_focus.py`, but omits `test_connected_home_check.py` which audits `programme-queue` literal `screenPanel("...")` calls (`PC-001`). |
| NFR-02 (Strict `mypy` and `ruff` check/format in `src/api`) | Covered | `P02` and `P02-T02` specify exact `python3 -m mypy` and `python3 -m ruff check src tests && python3 -m ruff format --check src tests` commands. |
| AC-01 through AC-03 | Partial | Credible once `PC-001` (`Connected view for ${c.id}` panel nesting) is clarified in `P01-T01`. |
| AC-04 (Test updates and bounded semantic WCAG test additions) | Partial | `P02` cites nonexistent test method names in `test_programme_screen_wcag.py` and omits updating the module-level `SCRIPT` harness that crashes when `div[role="group"]` is removed (`PC-003`). |
| AC-05 (`command.md` Web Interface Guidelines review + tracking + local commit) | Partial | `AC-05` requires `command.md` review, but `P01` and `P02-T02` omit pre-edit skill loading, post-edit `file:line` guideline reporting, and Focused Tier browser-check execution/disclosure (`PC-004`). |
| Research `C1` through `C15` and `W1` | Partial | `C1` to `C15` are well grounded, except `connected_home_browser_check.py` / `test_connected_home_check.py` panel-title and scoped-row constraints on `Connected view for ${c.id}` were not carried into `P01-T01` (`PC-001`). |
| P01, P01-T01, P01-T02 | Partial | Require targeted boundary clarifications for `PC-001`, `PC-002`, and `PC-004`. |
| P02, P02-T01, P02-T02 | Partial | Require exact symbol names and cross-cutting check updates for `PC-001`, `PC-003`, and `PC-004`. |

## Verdict

* Verdict: Revise
* Rationale: The core architectural approach (`screenJumpNav` + disjoint `screenJumpTarget` containers + explicit plain-language state prefixes) is well evidenced and resolves two pre-existing browser-harness regressions from partial commit `5bc6b8d81`. However, four substantive planner-owned gaps (`PC-001` through `PC-004`, including two High-severity implementation/test contract mismatches on `Connected view for ${c.id}` panel nesting and `aria-live="polite"` attributes in `programmeQueue()`) would cause deterministic unit or harness failures during `rpi-implement` if left unrevised.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `P01-T01` ambiguous "wrap its four target panels" instruction in `render()` risks breaking `Connected view for ${c.id}` panel-inventory and scoped-row checks

* Related IDs: FR-02, NFR-01, AC-01, AC-04, P01, P01-T01, P02, P02-T02
* Evidence: .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md (lines 73-86, 197-201); src/api/src/zava_forward/api/web/role-screens.js (lines 657-679); src/api/tests/test_connected_home_check.py (lines 157, 194-205, 264); src/api/checks/connected_home_browser_check.py (lines 206-214, 261-265, 322, 362-370, 413-419); src/api/checks/atlas_tensions_browser_check.py (lines 238-250)
* Concern: `P01-T01` defines four `programmeSections` (`programme-boundary`, `programme-steps`, `programme-journey`, `programme-withheld`) and instructs the implementer to "wrap its four target panels in `screenJumpTarget(...)`". Unlike `overview()` (which has four separate `screenPanel`s), `render(c, extra)` has only three target `screenPanel`s: ``screenPanel(`Connected view for ${c.id}`, ...)`` (which encloses both the state-summary block and `screenTable("Same-home step states", ...)`), `journeyStageMap(c)`, and `screenWithheld(...)` (plus `screenTension("disclosure")`). Meanwhile, `P02` omits `test_connected_home_check.py` from its validation list.
* Impact: Extracting `programme-steps` into its own `screenPanel("Same-home step states", ...)` or renaming ``Connected view for ${c.id}`` will immediately break: (1) `test_connected_home_check.py:194-205`, which regex-scans `programme-queue` for literal `screenPanel("...", ...)` calls and rejects any title outside `{"Evidence boundary", "Shared queue", "Lifecycle and funnel"}`; (2) `connected_home_browser_check.py:206-214,413-419`, which queries `Same-home step states` `tbody tr` rows scoped inside the `.screen-record` panel whose `:scope > h2` is `Connected view for <home_id>`; and (3) `atlas_tensions_browser_check.py:239`, which requires `Connected view for ZF-1` in `.screen-record` panel titles. Conversely, wrapping the outer `Connected view for ${c.id}` panel in `programme-boundary` while wrapping `Same-home step states` inside it would nest `#programme-steps` inside `#programme-boundary`.
* Smallest useful change: Specify in `P01-T01` that `render()` preserves ``screenPanel(`Connected view for ${c.id}`, ...)`` as the single outer panel (adding zero new literal `screenPanel("...")` calls) and places two non-nested `screenJumpTarget` children inside it: `screenJumpTarget("programme-boundary", h("div", {}, ...))` around the intro/readiness/state-summary block and `screenJumpTarget("programme-steps", screenTable("Same-home step states", ...))` around the step table, followed by `screenJumpTarget("programme-journey", journeyStageMap(c))`, `screenTension("disclosure")`, and `screenJumpTarget("programme-withheld", screenWithheld(...))`. Add `test_connected_home_check.py` and `test_atlas_tensions_checker.py` to `P02` / `P02-T02` validation commands.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` boundaries in .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md explicitly preserving ``screenPanel(`Connected view for ${c.id}`, ...)`` with sibling `#programme-boundary` and `#programme-steps` wrappers inside it, plus `test_connected_home_check.py` and `test_atlas_tensions_checker.py` listed in `P02` / `P02-T02`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: `FR-05` and `P02-T01` require VDOM assertions for `aria-live="polite"` status announcements in `overview()`, but `P01` never adds `"aria-live": "polite"` to `programmeQueue()`

* Related IDs: FR-05, AC-04, P01, P01-T02, P02-T01
* Evidence: .copilot-tracking/plans/2026-11-15/issue-230-programme-mgr-wcag-plan.md (lines 92-95); .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md (lines 32-35, 129-145, 233); src/api/src/zava_forward/api/web/role-screens.js (lines 412-413, 1699)
* Concern: `FR-05` and `P02-T01` direct `test_programme_screen_wcag.py` to assert `role="status"` and `aria-live="polite"` on queue status regions in `overview()`. In `src/api/src/zava_forward/api/web/role-screens.js:412-413`, `programmeQueue()` currently constructs `#programme-filter-status` and `#programme-page-status` with `{ role: "status", id: ... }` and no `"aria-live": "polite"` property, and `P01` excludes `programmeQueue` from its edit list.
* Impact: Node `vm` VDOM tests inspect raw `node.attrs` objects without browser implicit ARIA role reflection, so `P02-T01`'s required `aria-live="polite"` assertion will fail against `P01`'s planned code (and explicit `"aria-live": "polite"` matches sibling status regions across `role-screens.js:1699`, `app.js`, `panels.js`, `ops.js`, and `index.html`).
* Smallest useful change: Add `programmeQueue` (`src/api/src/zava_forward/api/web/role-screens.js:412-413`) to `P01` / `P01-T02` boundaries so `#programme-filter-status` and `#programme-page-status` explicitly include `"aria-live": "polite"` alongside `role: "status"`.
* Action owner: planning_parent
* Exact resolving evidence: `P01` and `P01-T02` in .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md include adding `"aria-live": "polite"` to `#programme-filter-status` and `#programme-page-status` in `programmeQueue()`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `P02` cites nonexistent test method names in `test_programme_screen_wcag.py` and omits replacing the module-level `SCRIPT` button lookup that crashes `setUp()`

* Related IDs: AC-04, P02, P02-T01
* Evidence: .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md (lines 173-176, 219-236); .copilot-tracking/plans/2026-11-15/issue-230-programme-mgr-wcag-plan.md (line 111); src/api/tests/test_programme_screen_wcag.py (lines 16, 32-33, 90-113); src/api/checks/role_screens_browser_check.py (lines 654-658)
* Concern: `P02` Context instructs replacing `test_jump_bar_buttons_target_focusable_sections_in_order` and `test_jump_button_moves_focus_to_each_target_section` in `src/api/tests/test_programme_screen_wcag.py`. Neither method exists in that file: the actual button-bar test is `test_section_links_use_documented_classes_and_move_focus` (`lines 96-109`), and module-level `SCRIPT` (`lines 32-33`) unconditionally evaluates `ok.kids[0].kids.find(k => k.tag === "div" && k.attrs.role === "group").kids[0]` with a stub `doc` (`line 16`) that lacks `addEventListener`.
* Impact: Once `P01-T01` removes `div[role="group"]`, `SCRIPT` throws a Node `TypeError` in `setUp()` for every test in `ProgrammeScreenWcag` unless `SCRIPT` is updated to register `document.addEventListener("click", ...)` before `vm.runInContext(...)`. In addition, `test_existing_state_cells_are_unchanged` (`lines 90-94`) should be explicitly preserved because `role_screens_browser_check.py:657` and `connected_home_browser_check.py:208` rely on raw `"Blocked"` / `"Blocked: evidence missing"` / `"No recorded blocker"` strings in `programmeGates` column 1 while `State summary in words` provides the `Action needed:` / `Warning:` prefixes.
* Smallest useful change: Correct `P02` Context and `P02-T01` in .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md to reference `SCRIPT` (`doc.addEventListener` delegation + async `overview()` harness), `test_section_links_use_documented_classes_and_move_focus`, and `test_no_nav_element_or_other_controls` as the exact replacements, while explicitly retaining `test_existing_state_cells_are_unchanged`.
* Action owner: planning_parent
* Exact resolving evidence: `P02` and `P02-T01` in .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md name exact symbols present in `src/api/tests/test_programme_screen_wcag.py` and retain `test_existing_state_cells_are_unchanged`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: `P01` and `P02-T02` omit mandatory Web Development Guidance steps (`web-design-guidelines` load/review and local browser-check execution or disclosure) required by `AC-05`

* Related IDs: NFR-01, AC-05, P01, P02-T02
* Evidence: .copilot-tracking/plans/2026-11-15/issue-230-programme-mgr-wcag-plan.md (lines 115, 169); .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md (lines 19-48, 250-275); src/api/checks/programme_paging_browser_check.py (lines 1-35, 193-212)
* Concern: `AC-05` requires a completed Web Interface Guidelines (`command.md`) review with zero open findings on changed web code, and AMA Repository Instructions require loading `web-design-guidelines` and `redesign-existing-projects` before web edits, refreshing/reviewing changed web lines in `file:line` format before review, and running touched local browser checks (such as `checks/programme_paging_browser_check.py`) or explicitly disclosing unavailable/unrun checks and unpushed hosted CI under Focused Tier rules. Neither `P01` nor `P02-T02` includes these execution/recording steps in phase details.
* Impact: Implementing `P01` and `P02-T02` strictly from phase details risks omitting evidence required by `AC-05` and repository governance during `rpi-review`.
* Smallest useful change: Add pre-edit `web-design-guidelines` / `redesign-existing-projects` skill loading to `P01` and add post-edit `command.md` `file:line` verification, `python3 -m checks.programme_paging_browser_check` execution (or honest prerequisite-block disclosure if local Chromium/packages are absent), and Focused Tier / unpushed hosted-CI status recording to `P02-T02`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01` and `P02-T02` sections in .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md covering skill loading, `command.md` `file:line` audit output, and browser-check / Focused Tier disclosure in .copilot-tracking/changes/2026-11-15/issue-230-programme-mgr-wcag-changes.md.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Disjoint jump-target IDs across `overview()` (`programme-overview-boundary`, `programme-shared-queue`, `programme-funnel`, `programme-overview-withheld`) and `render()` (`programme-boundary`, `programme-steps`, `programme-journey`, `programme-withheld`) prevent duplicate DOM IDs when `roleScreensView()` mounts `[overview, selected]` together (`src/api/src/zava_forward/api/web/role-screens.js:203`).
* Replacing `div[role="group"]` `<button>` jump controls in `render()` with `screenJumpNav` (`<nav class="row" aria-label="...">` + `a.btn.alt[data-jump]`) aligns `programme-queue` with #225, #226, and #227 while simultaneously fixing two browser-check regressions from partial commit `5bc6b8d81`: `src/api/checks/programme_paging_browser_check.py:202` (`main button == QUEUE_CONTROLS`) and `src/api/checks/atlas_tensions_browser_check.py:213` (`evidence.locator("button, form, input, select, textarea").count() == 0`).
* Keeping `programmeOverviewSections` to 4 jump links ensures `Tab` from `aside a[data-reset]` reaches `#programme-next` on the 5th Tab press (`5 <= 6`), preserving `src/api/checks/programme_paging_browser_check.py:89,210`.
* Wrapping `journeyStageMap(c)` externally via `screenJumpTarget("programme-journey", journeyStageMap(c))` keeps zero `tabindex` attributes inside `<section><h2>Journey stages for ...</h2></section>`, preserving `src/api/tests/test_role_screens_stage_map_focus.py:55-96`.
* Planned `programmeRow` and `programmeFunnel` state prefixes (`State: Returned. <reason>` without a trailing period, `State: Not returned. Handoff state: <state>.`, `State: Not returned`, `State: Unknown. ...`, `State: Recorded stage history (not a readiness pass). ...`, and `State: Warning. No blocker is recorded...`) preserve all existing substring contracts in `src/api/tests/test_programme_screen.py` (including `Reason 1"` at line 206 and `assertNotIn("Blocked", clear)` at line 381), `src/api/tests/test_content_standard.py` banned-word rules, and `src/api/checks/role_screens_browser_check.py:663` (`\bready\b` exclusion).
* Accepted residual risk: Engineering unit and DOM checks do not establish WCAG 2.2 AA conformance or live assistive-technology/user acceptance (#155), which the plan properly reflects by scoping the commit trailer to `Refs #230`.

## Questions or Blocking Evidence Gaps

* None. All four findings are direct planner corrections fully resolved by in-tree source/test evidence and caller instructions.

## Limitations

* Critique verification was conducted statically against supplied planning, research, JavaScript source, unit-test, and Playwright-check files without modifying code or executing live browser suites.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Revise `P01-T01`, `P01-T02`, `P02`, `P02-T01`, and `P02-T02` directly in `.copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md` and record disposition in `.copilot-tracking/plans/2026-11-15/issue-230-programme-mgr-wcag-plan.md` to preserve ``screenPanel(`Connected view for ${c.id}`, ...)`` nesting + `test_connected_home_check.py` (`PC-001`), add `"aria-live": "polite"` on `programmeQueue()` status elements (`PC-002`), fix exact `test_programme_screen_wcag.py` symbol/harness names (`PC-003`), and include `command.md` / browser-check steps (`PC-004`), then finalize the plan as `Ready` without another critique pass.
* User response required: no
