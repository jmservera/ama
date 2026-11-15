<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #230 Programme Manager and Coordinator Screens WCAG 2.2 Compliance

## Metadata

* Task ID: 2026-11-15-issue-230-programme-mgr-wcag
* Task slug: issue-230-programme-mgr-wcag
* Related plan: .copilot-tracking/plans/2026-11-15/issue-230-programme-mgr-wcag-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-230-programme-mgr-wcag-research.md, docs/reference/research/ux/wcag-conformance-baseline.md, docs/reference/research/ux/design-system.md, docs/reference/research/ux/content-standard.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Upgrade `programme-queue` WCAG 2.2 keyboard jump navigation and textual state labels | complete | P01, P01-T01, P01-T02 |
| P02 | Reconcile and expand WCAG 2.2 unit tests and execute Focused Tier validation | complete | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Upgrade `programme-queue` WCAG 2.2 keyboard jump navigation and textual state labels

### Context

Research (`C1`–`C15`, `W1`) established that `programme-queue` in `src/api/src/zava_forward/api/web/role-screens.js` serves `Retrofit Programme Manager`, `Programme Support Officer`, and `Retrofit Coordinator` via `overview(signal, items, c, page)` and `render(c, extra)`. Currently:
* `overview()` has no `<nav aria-label>` jump links and no `tabindex="-1"` section targets.
* `render()` uses an older `<div class="row" role="group" aria-label="Jump to a section of this screen">` containing four `<button type="button" onclick={programmeJump(id)}>` elements instead of `<nav aria-label>` jump links (`a[data-jump]`), which both fails the #225/#226/#227 `<nav aria-label>` requirement and breaks `checks/programme_paging_browser_check.py` (`main button` set check).
* `programmeRow()` returned-work reason cells, `programmeFunnel()` summaries, and `render()` unblocked notices need explicit non-colour textual state prefixes while preserving existing substrings and banned-word rules.

### Intent

Deliver full WCAG 2.2 keyboard section jump navigation (`<nav aria-label>` + `a.btn.alt[data-jump]` + disjoint `tabindex="-1"` targets) and explicit textual state labels across both `overview()` and `render()` of `programme-queue` without regressing any conformance, glossary, stage-map, or browser-check invariant.

### Boundaries

* Included: Pre-edit skill confirmation (`web-design-guidelines` + `command.md` rules and `redesign-existing-projects`), plus edits to `programmeRow`, `programmeQueue`, `programmeFunnel`, `programmeOverviewSections`, `programmeSections`, and `registerRoleScreen({ id: "programme-queue", ... })` inside `src/api/src/zava_forward/api/web/role-screens.js`.
* Excluded: Other specialist screens in `role-screens.js`, `app.js`, `style.css`, backend endpoints, and `checks/*.py`.

### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: Replace `programmeJump` / `div[role="group"]` buttons with `screenJumpNav` + `screenJumpTarget` in both `overview()` and `render()`, and add explicit textual state cues in `programmeRow`, `programmeFunnel`, and `render()`.

### Dependencies

* Existing `screenJumpTarget`, `screenJumpNav`, and document `click` delegation on `a[data-jump]` in `src/api/src/zava_forward/api/web/role-screens.js`.

### Validation Expectations

* Node VDOM unit tests render `programme-queue` `overview()` and `render()` cleanly with no undefined CSS classes, no banned glossary words, no global scope collisions, no inline `onclick` on jump links, zero `<button>` tags in `render()`, and zero duplicate `id` attributes when mounted together.

### Completion Evidence

* Clean diff in `src/api/src/zava_forward/api/web/role-screens.js` passing all unit and conformance suites.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add disjoint `screenJumpNav` and `screenJumpTarget` navigation to `programme-queue` `overview()` and `render()`

#### Context

When a home `c` is selected in `roleScreensView()`, `div.main` mounts `[overview, selected]` simultaneously (`role-screens.js:203`). Therefore:
1. Overview target IDs and connected-home target IDs must be disjoint.
2. `checks/programme_paging_browser_check.py` focuses `aside a[data-reset]` and presses `Tab` up to `limit=6` times to reach `#programme-next`. Placing `screenJumpNav` at the top of `overview()` with exactly 4 links means `Tab` traverses 4 jump links and lands on `#programme-next` on the 5th `Tab` press (`5 <= 6`).
3. `tests/test_role_screens_stage_map_focus.py` requires zero `tabindex` attributes *inside* `<section><h2>Journey stages for ...</h2></section>`, which `screenJumpTarget("programme-journey", journeyStageMap(c))` (`<div id="programme-journey" tabindex="-1">`) satisfies because the wrapper `div` sits outside the `<section>`.

#### Intent

Wire `screenJumpNav` and `screenJumpTarget` across both `overview()` and `render()` and delete the obsolete `programmeJump` inline click helper.

#### Boundaries

* Included:
  * Define `programmeJumpNav = (label, sections) => h("nav", { "aria-label": label, class: "screen-links" }, sections.map(([id, text]) => h("a", { href: `#${id}`, "data-jump": id }, `Go to ${text}`)))`, matching the `.screen-links` `<nav>` pattern in `asset-board` (#226) and `safety_repairs` (#227) and relying on the shared document `a[data-jump]` click delegation (`role-screens.js:116-123`).
  * Define `programmeOverviewSections` with concise, distinct WCAG 2.4.4 link labels when co-mounted with `render()`:
    * `["programme-overview-boundary", "Overview boundary"]`
    * `["programme-shared-queue", "Shared queue"]`
    * `["programme-funnel", "Lifecycle and funnel"]`
    * `["programme-overview-withheld", "Overview withheld"]`
  * Define `programmeSections`:
    * `["programme-summary", "State summary"]`
    * `["programme-steps", "Same-home step states"]`
    * `["programme-journey", "Journey stages"]`
    * `["programme-withheld", "Not shown for this role"]`
  * Render `programmeJumpNav("Jump to a section of the programme overview", programmeOverviewSections)` at the start of `overview()` and wrap its four top-level panels in `screenJumpTarget(...)`, keeping `screenTension("disclosure")` between `programme-funnel` and `programme-overview-withheld`.
  * Render `programmeJumpNav("Jump to a section of the connected home view", programmeSections)` inside ``screenPanel(`Connected view for ${c.id}`, ...)`` right after the intro paragraph (preserving ``Connected view for ${c.id}`` within Chromium's initial `content-visibility: auto` viewport layout margin for `checks/role_screens_browser_check.py 230` while adding zero new literal `screenPanel("...")` calls), and place two non-nested sibling `screenJumpTarget` wrappers inside ``screenPanel(`Connected view for ${c.id}`, ...)`` (`screenJumpTarget("programme-summary", h("div", {}, ...))` around the state-summary block and `screenJumpTarget("programme-steps", screenTable("Same-home step states", ...))` around the step table), followed by `screenJumpTarget("programme-journey", journeyStageMap(c))`, `screenTension("disclosure")`, and `screenJumpTarget("programme-withheld", screenWithheld(...))`.
  * Remove `programmeJump` and the `<div class="row" role="group" ...>` `<button>` bar.
* Excluded: Modifying `journeyStageMap` internals or `screenJumpNav` shared helper signature.

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: `programmeOverviewSections`, `programmeSections`, and `programme-queue` `overview()` / `render()`.

#### Dependencies

* None.

#### Validation Expectations

* Every `a[data-jump]` link in `overview()` and `render()` has `href="#<id>"`, `class="btn alt"`, `data-jump="<id>"`, `data-jump-target="<id>"`, accessible text `"Go to <label>"`, no `onclick` attribute, and a matching `<div id="<id>" tabindex="-1">` target in the rendered tree; combined `[overview, render]` tree has 8 unique jump IDs; `render()` has 0 `<button>` elements.

#### Completion Evidence

* Verified by `test_programme_screen_wcag.py`, `test_programme_screen.py`, `test_role_screens_conformance.py`, and `test_role_screens_stage_map_focus.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add explicit non-colour textual state prefixes and polite live-region attributes across queue, funnel, and connected-home step surfaces

#### Context

WCAG 2.2 SC 1.4.1 (Use of Color), SC 1.3.1 / 2.4.6, and SC 4.1.3 (Status Messages) require every status badge, returned-work row, funnel indicator, step state, and queue status line to expose explicit textual meaning and polite live-region announcements without relying on visual treatment. Existing tests enforce specific substring contracts:
* `test_programme_screen.py` checks `"Missing survey"`, `"Reason 1"` (at end of cell without trailing period), `"Offered"`, `"No handoff proposed"`, `"No handoff recorded"`, `"Not returned. Pending handoff"` absence, `"Lifecycle and funnel counts are Unknown"`, `"Blocked: evidence missing"`, `"No recorded blocker"`, `"not a pass"`, and `assertNotIn("Blocked", clear)`.
* `checks/role_screens_browser_check.py` and `checks/connected_home_browser_check.py` rely on raw `"Blocked"`, `"Blocked: evidence missing"`, and `"No recorded blocker"` strings in `programmeGates` column 1 while `State summary in words` provides `Action needed:` / `Warning:` prefixes.
* `test_content_standard.py` forbids standalone words `gate`, `gates`, `hold`, `holds`, `provenance`, `trace`, `traces`, `snapshot`, `snapshots`, `envelope`, `envelopes` anywhere in `role-screens.js`.
* `checks/specialist_keyboard_browser_check.py` requires `.screen-evidence table` captions on `programme-queue` to remain `("Same-home step states",)`.

#### Intent

Add `"aria-live": "polite"` to `programmeQueue()` status paragraphs and add explicit, consistent plain-language textual state prefixes across returned-work/handoff queue cells, lifecycle/funnel status copy, and connected-home step notices while preserving every existing substring and lexical guardrail.

#### Boundaries

* Included:
  * `programmeQueue(first, total, loadPage, start)`:
    * Add `"aria-live": "polite"` alongside `role: "status"` on both `#programme-filter-status` and `#programme-page-status`.
  * `programmeRow(row)`:
    * Returned work cell: `` `State: Returned. ${screenValue(work.returned.reason)}` ``
    * Handed-off (not returned) cell: `` `State: Not returned. Handoff state: ${screenValue(work.handoff.state)}.` ``
    * Plain (neither returned nor handed-off) cell: `"State: Not returned"`
  * `programmeFunnel(report)`:
    * Missing `report?.funnel`: `"State: Unknown. Lifecycle and funnel counts are Unknown. No record was supplied."`
    * Present `report?.funnel`: `` `State: Recorded stage history (not a pass). Recorded as of ${screenValue(report.as_of)}. Audit integrity state: ${screenValue(report.audit_integrity)}. Conversion state: Unknown; counts are stage history only.` ``
  * `programme-queue.render(c, extra)`:
    * Retain raw step-table column-1 state cells (`"Blocked"`, `"Blocked: evidence missing"`, `"No recorded blocker"`) and `State summary in words` `<ul>` with `programmeStateLabel` (`Action needed: Blocked`, `Action needed: Blocked: evidence missing`, `Warning: No recorded blocker`).
    * Prefix unblocked readiness paragraph with `"State: Warning. No blocker is recorded, which does not confirm readiness."` (never using the word `"Blocked"` in the clear path) and retain `screenUnknown` blocked callout when any step is blocked.
* Excluded: Renaming `"Same-home step states"` table caption or adding extra `<table>` elements inside `render()`.

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: `programmeQueue`, `programmeRow`, `programmeFunnel`, and `programme-queue.render`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Queue rows, funnel panel, and connected-home view expose explicit textual state cues in words for every state variant while passing `test_programme_screen.py` and `test_content_standard.py`.

#### Completion Evidence

* Verified by `test_programme_screen.py`, `test_programme_screen_wcag.py`, and `test_content_standard.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Reconcile and expand WCAG 2.2 unit tests and execute Focused Tier validation

### Context

Test ownership and bounds locked prior to critique:
* Canonical test targets: `src/api/tests/test_programme_screen_wcag.py` and `src/api/tests/test_programme_screen.py`.
* Exact removals/replacements:
  1. In `src/api/tests/test_programme_screen.py`: replace the 2 obsolete `self.assertEqual(tags(node).count("button"), 4)` assertions on `render()` (lines 386 and 538, introduced when jump controls were `<button>`s) with `self.assertNotIn("button", tags(node))`.
  2. In `src/api/tests/test_programme_screen_wcag.py`: update module-level `SCRIPT` (to register `doc.addEventListener("click", ...)` delegation, execute async `overview()` as well as `render()`, and remove the obsolete `div[role="group"]` lookup), retain `test_existing_state_cells_are_unchanged`, and replace `test_section_links_use_documented_classes_and_move_focus` and `test_no_nav_element_or_other_controls` with `<nav aria-label>` + `a[data-jump]` jump-link, read-only control-absence, and delegated-click tests covering both `overview()` and `render()`.
* Maximum additions: up to 10 focused semantic test methods in `src/api/tests/test_programme_screen_wcag.py` (no duplicate restatement tests, 0 new test files required because `test_programme_screen_wcag.py` already matches `test_*programme*.py` and is the canonical WCAG test module for #230).
* Semantic-versus-regression coverage: semantic tests exercise live VDOM rendering and Node `vm` event execution of `role-screens.js` across roles, queue states, funnel states, connected-home step states, and delegated `a[data-jump]` clicks; cross-cutting suites verify repo-wide conformance and baseline invariants.

### Intent

Bring `test_programme_screen.py` and `test_programme_screen_wcag.py` into full alignment with the WCAG 2.2 contract, run all Focused Tier checks (`unittest`, `mypy`, `ruff`), and record implementation evidence in `.copilot-tracking/changes/2026-11-15/issue-230-programme-mgr-wcag-changes.md`.

### Boundaries

* Included: `src/api/tests/test_programme_screen.py`, `src/api/tests/test_programme_screen_wcag.py`, Focused Tier test/type/lint execution in `src/api`, and `.copilot-tracking/changes/2026-11-15/issue-230-programme-mgr-wcag-changes.md`.
* Excluded: Modifying `test_accessibility_baseline.py` static counts or `checks/*.py`.

### Likely Targets

* `src/api/tests/test_programme_screen.py`: Reconcile read-only `render()` button absence assertions.
* `src/api/tests/test_programme_screen_wcag.py`: Expand strict-typed WCAG 2.2 test coverage for `overview()` and `render()`.
* `.copilot-tracking/changes/2026-11-15/issue-230-programme-mgr-wcag-changes.md`: Record implementation changes and validation results.

### Dependencies

* P01.

### Validation Expectations

* `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m unittest discover -s tests -p "test_*programme*.py" -q` exits `0`.
* Cross-cutting conformance/baseline tests (`test_accessibility_baseline.py`, `test_content_standard.py`, `test_role_screens_conformance.py`, `test_role_screens.py`, `test_role_screens_tensions_same_home.py`, `test_role_screens_stage_map_focus.py`, `test_safety_screen_wcag_keyboard.py`, `test_specialist_keyboard_check.py`, `test_connected_home_check.py`, `test_atlas_tensions_checker.py`, `test_epic149_role_workbench_heading_hierarchy.py`) exit `0`.
* Local Playwright check `python3 -m checks.programme_paging_browser_check` is executed from `src/api` if Chromium and local packages are available, or explicitly disclosed as prerequisite-blocked if unavailable, alongside Focused Tier classification and unpushed hosted-CI status.
* Post-edit `command.md` Web Interface Guidelines review (`file:line` format) verifies zero open findings on changed web files.
* `python3 -m mypy` exits `0`.
* `python3 -m ruff check src tests && python3 -m ruff format --check src tests` exits `0`.

### Completion Evidence

* Passing command outputs recorded in `.copilot-tracking/changes/2026-11-15/issue-230-programme-mgr-wcag-changes.md` and `[x]` task/phase markers reconciled across plan and phase details.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Update `test_programme_screen.py` and expand `test_programme_screen_wcag.py`

#### Context

Both `test_programme_screen.py` and `test_programme_screen_wcag.py` are checked by `mypy --strict` and `ruff` (`line-length = 100`, rules `E, F, I, B, UP`).

#### Intent

Verify all WCAG 2.2 #230 behaviours semantically through Node `vm` execution of `role-screens.js`.

#### Boundaries

* Included:
  1. Update `test_programme_screen.py` lines 385-386 and 538 to assert `self.assertNotIn("button", tags(node))` on `render()`.
  2. Expand `test_programme_screen_wcag.py` to test:
     * `<nav aria-label="Jump to a section of the programme overview">` in `overview()` with 4 `a.btn.alt[data-jump]` links and 4 matching `tabindex="-1"` section targets in order.
     * `<nav aria-label="Jump to a section of the connected home view">` in `render()` with 4 `a.btn.alt[data-jump]` links and 4 matching `tabindex="-1"` section targets in order, across all 3 installed roles (`Retrofit Programme Manager`, `Programme Support Officer`, `Retrofit Coordinator`), with zero `<button>`, `<input>`, `<select>`, `<textarea>`, or `<form>` controls in `render()`.
     * Combined `overview()` + `render()` mounting uniqueness: all 8 jump target IDs are unique (`len(ids) == len(set(ids)) == 8`) and overview has `<= 4` jump links.
     * Document-level delegated `a[data-jump]` click dispatch across all 8 links: calls `event.preventDefault()`, focuses each matching `tabindex="-1"` target in order, has no inline `onclick`, and does not throw when a target element is absent or click target does not match `a[data-jump]`.
     * Explicit non-colour textual state labels across returned-work rows (`State: Returned. Missing survey`), handoff rows (`State: Not returned. Handoff state: Offered.`), plain rows (`State: Not returned`), funnel missing/populated states (`State: Unknown. ...`, `State: Recorded stage history (not a readiness pass). ...`), and connected-home blocked/missing/unblocked step states (`Action needed: Blocked`, `Action needed: Blocked: evidence missing`, `Warning: No recorded blocker`, and `State: Warning.` when clear without `"Blocked"`).
     * Keyboard-accessible controls in `overview()`: `<label for="programme-scope">` bound to `<select id="programme-scope">`, native `Apply filter` / `Reset to default view` / `Previous page` / `Next page` buttons, boundary focus handoff (`#programme-next` -> `#programme-prev` on last page and `#programme-prev` -> `#programme-next` on page 1 so focus never strand-drops on a disabled button), `role="status"` `aria-live="polite"` announcements, and focusable `.table-scroll` regions (`tabindex="0"`, `role="region"`, `aria-label`, `<caption>`, `<th scope="col">`).
* Excluded: Redundant tests checking trivial JS language behaviour or duplicating `test_programme_screen.py` business-logic assertions verbatim.

#### Likely Targets

* `src/api/tests/test_programme_screen.py`
* `src/api/tests/test_programme_screen_wcag.py`

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* `test_programme_screen.py` and `test_programme_screen_wcag.py` pass `unittest`, `mypy`, and `ruff`.

#### Completion Evidence

* Passing `unittest`, `mypy`, and `ruff` execution.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Run Focused Tier validation suites, `mypy`, and `ruff`, and write changes artifact

#### Context

Repository Instructions require Focused Tier validation for scoped web UI and unit-test updates: run planned targeted checks, cross-cutting local guardrails touched by the change, `mypy`, and `ruff`, and record the tier classification and exact results.

#### Intent

Execute all validation commands from `src/api`, author `.copilot-tracking/changes/2026-11-15/issue-230-programme-mgr-wcag-changes.md`, and reconcile `[x]` checklist markers in plan and phase details before transitioning to `Review`.

#### Boundaries

* Included: Validation execution in `src/api` and `.copilot-tracking/` artifact reconciliation.
* Excluded: `git commit` (performed after `rpi-review` completes so the review artifact and final `Follow-up` session state are included in the single frozen local commit) and `git push` (prohibited).

#### Likely Targets

* `.copilot-tracking/changes/2026-11-15/issue-230-programme-mgr-wcag-changes.md`
* `.copilot-tracking/plans/2026-11-15/issue-230-programme-mgr-wcag-plan.md`
* `.copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md`

#### Dependencies

* P02-T01.

#### Validation Expectations

* Every targeted and cross-cutting `unittest`, `mypy`, and `ruff` command exits `0`; `checks/programme_paging_browser_check` execution (or honest prerequisite-block disclosure), `command.md` `file:line` audit result, Focused Tier basis, and unpushed hosted-CI status are recorded in `.copilot-tracking/changes/2026-11-15/issue-230-programme-mgr-wcag-changes.md`.

#### Completion Evidence

* Recorded command outputs in `.copilot-tracking/changes/2026-11-15/issue-230-programme-mgr-wcag-changes.md`.

#### Unresolved Items

* None.
