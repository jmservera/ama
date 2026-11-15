<!-- markdownlint-disable-file -->
# RPI Plan: Issue #230 Programme Manager and Coordinator Screens WCAG 2.2 Compliance

## Task Metadata

* Task ID: 2026-11-15-issue-230-programme-mgr-wcag
* Task slug: issue-230-programme-mgr-wcag
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-230-programme-mgr-wcag-plan-critique.md

## Executive Summary

This plan completes the remaining engineering acceptance criterion on GitHub issue #230 (`Programme manager and coordinator screens`): WCAG 2.2 baseline (#151) compliance with explicit non-colour textual state meaning and keyboard jump navigation across the `programme-queue` specialist screen in `src/api/src/zava_forward/api/web/role-screens.js`.

Both surfaces of `programme-queue` (`overview` for the shared queue, scope filter/reset/pager, and lifecycle/funnel view; and `render` for the connected same-home 5-step view and journey stage map) will expose landmark `<nav aria-label>` jump links (`a.btn.alt[data-jump]`) pointing to disjoint `tabindex="-1"` section targets via the shared `screenJumpNav` and `screenJumpTarget` helpers established in #225, #226, and #227. Returned-work rows, handoff states, lifecycle/funnel summaries, and connected-home step states will express explicit textual state cues so meaning never relies on colour or layout alone. Focused unit and accessibility tests in `src/api/tests/test_programme_screen_wcag.py` and `src/api/tests/test_programme_screen.py` will verify jump-link delegation, disjoint focus targets, keyboard control ergonomics, and textual state labels under Focused Tier validation (`unittest`, `mypy`, `ruff`).

### User Decisions and Requirements Highlights

* Deliver the remaining unchecked acceptance criterion on issue #230: WCAG 2.2 baseline (#151) keyboard navigation (`nav aria-label` jump links, `tabindex="-1"` target sections, keyboard-accessible controls) and explicit textual state meaning on returned-work, step, and funnel indicators, matching sibling role screens (#225, #226, #227).
* Preserve all four already-delivered #230 criteria: shared queue returned-work accountability fields, separate chase vs resident-update ownership with non-mutating reset, connected same-home 5-step view with missing steps blocked, and Fluent 2 design-system components (#150) without any role simulator.
* Add focused unit/accessibility tests in `src/api/tests/` and pass targeted `test_*programme*.py`, `mypy`, and `ruff` checks in `src/api`.
* Commit all implementation and `.copilot-tracking/` artifacts locally on `feat/ux-230-programme-mgr-wcag` with `Refs #230` and the Copilot `Co-authored-by` trailer, and do not push to remote.

### What You May Not Know

* `roleScreensView()` mounts `overview` and `selected` (`render`) in `div.main` simultaneously whenever a home is selected (`role-screens.js:203`), so overview jump-target IDs (`programme-overview-boundary`, `programme-shared-queue`, `programme-funnel`, `programme-overview-withheld`) must stay strictly disjoint from connected-home jump-target IDs (`programme-summary`, `programme-steps`, `programme-journey`, `programme-withheld`) to avoid duplicate DOM IDs, while keeping `#programme-summary` and `#programme-steps` as non-nested sibling `screenJumpTarget` containers inside ``screenPanel(`Connected view for ${c.id}`, ...)`` preserves `test_connected_home_check.py`, `connected_home_browser_check.py`, and `atlas_tensions_browser_check.py`.
* Replacing the earlier `div[role="group"]` jump `<button>` bar in `render()` with `<nav aria-label>` jump `<a>` links also resolves a button-set mismatch against `checks/programme_paging_browser_check.py` (`main button` expects only the four queue paging/filter buttons), while keeping the overview jump `<nav>` to four links keeps keyboard `Tab` from `aside a[data-reset]` to `#programme-next` at five presses (strictly within the browser check's six-press limit).
* `tests/test_content_standard.py` bans standalone glossary words `gate`, `gates`, `hold`, `holds`, `provenance`, `trace`, `traces`, `snapshot`, `snapshots`, `envelope`, and `envelopes` anywhere in `role-screens.js` (including comments and link labels), and `tests/test_role_screens_stage_map_focus.py` forbids `tabindex` inside `<section><h2>Journey stages for ...</h2></section>`.

### Unresolved Decisions or Blockers

* None. All engineering design choices are settled from repository evidence and caller instructions; manual screen-reader/user sign-off remains tracked separately under #155 per `docs/reference/research/ux/wcag-conformance-baseline.md`.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`, including plan `critique`) writing dated artifacts under `.copilot-tracking/` for GitHub issue #230 (`Programme manager and coordinator screens`) (source: user prompt).
* Inspect the programme manager / coordinator screen module under `src/api/src/zava_forward/api/web/` (`role-screens.js` `programme-queue`) and existing tests (`src/api/tests/test_programme_screen.py`, `src/api/tests/test_programme_screen_wcag.py`, `src/api/tests/test_accessibility_baseline.py`) (source: user prompt; verified in `.copilot-tracking/research/2026-11-15/issue-230-programme-mgr-wcag-research.md`).
* Add full WCAG 2.2 keyboard jump navigation (`nav aria-label` jump links to main sections, `tabindex="-1"` on target sections, explicit textual state meaning on all returned-work/step/funnel badges and indicators, and keyboard-accessible controls) matching #226, #227, and #225 (source: user prompt).
* Preserve delivered #230 behaviour: returned-work fields (reason, sender, current owner, proposed receiver), separate chase and resident-update responsibility, non-mutating reset, connected same-home 5-step states with missing evidence blocked, Fluent 2 design-system classes, and no role simulator (source: issue #230 + user prompt).
* Add focused unit/accessibility tests in `src/api/tests/` and run `test_*programme*.py`, `python3 -m mypy`, and `python3 -m ruff check src tests && python3 -m ruff format --check src tests` in `src/api` (source: user prompt).
* Commit all changes and `.copilot-tracking/` artifacts on `feat/ux-230-programme-mgr-wcag` with `Refs #230` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing (source: user prompt; `Refs #230` also honours Repository Instructions because live human/AT sign-off under #155 remains open).

## Goals

* Provide landmark `<nav aria-label>` keyboard jump navigation and programmatic `tabindex="-1"` section focus targets across both the overview (`overview()`) and connected same-home (`render()`) surfaces of `programme-queue` for all installed roles (`Retrofit Programme Manager`, `Programme Support Officer`, `Retrofit Coordinator`).
* Ensure every returned-work item, handoff status, lifecycle/funnel summary, and connected same-home step state communicates its status in plain, non-colour text first (WCAG 2.2 SC 1.4.1, 1.3.1, 2.4.6).
* Prove keyboard jump delegation, disjoint focus targets, keyboard-operable queue controls, textual state labels, and cross-cutting repository conformance through strict-typed unit/accessibility tests without breaking any existing static baseline or browser-check invariant.

## Scope and Non-Goals

### In Scope

* Updating `programme-queue` and its helper functions in `src/api/src/zava_forward/api/web/role-screens.js`.
* Updating `src/api/tests/test_programme_screen.py` where `render()` button-count assertions depended on the superseded `div[role="group"]` jump buttons.
* Updating and expanding `src/api/tests/test_programme_screen_wcag.py` with comprehensive WCAG 2.2 jump-link, `tabindex="-1"` target, delegated-click focus, keyboard control, and non-colour textual state tests.
* Running Focused Tier unit, conformance, type-checking (`mypy`), and lint/format (`ruff`) checks in `src/api` and creating one local commit on `feat/ux-230-programme-mgr-wcag`.

### Non-Goals

* Pushing commits or opening/updating a remote pull request (`git push` is explicitly excluded).
* Claiming live human or screen-reader acceptance (#155 / manual AT check records remain honest engineering non-claims).
* Modifying unrelated role screens, stylesheets (`style.css` already styles `nav.row > a.btn.alt`), backend API endpoints, SQL schemas, Dockerfiles, or GitHub workflows.

## Functional Requirements

* FR-01: `programme-queue.overview()` renders a `<nav class="screen-links" aria-label="Jump to a section of the programme overview">` via `programmeJumpNav` containing four `<a href="#<id>" data-jump="<id>">Go to <section></a>` links targeting four `screenJumpTarget` (`<div id="<id>" tabindex="-1">`) wrappers (`programme-overview-boundary`, `programme-shared-queue`, `programme-funnel`, `programme-overview-withheld`).
  * Observable acceptance criteria: Overview VDOM contains exactly one `<nav>` with `aria-label="Jump to a section of the programme overview"`, four `a[data-jump]` links without inline `onclick`, and four matching `tabindex="-1"` target containers in DOM order.
* FR-02: `programme-queue.render()` replaces `<div role="group">` jump `<button>`s and `programmeJump` with `<nav class="screen-links" aria-label="Jump to a section of the connected home view">` via `programmeJumpNav` inside ``screenPanel(`Connected view for ${c.id}`, ...)`` right after the intro paragraph, containing four `a[data-jump]` links targeting four non-nested `screenJumpTarget` (`<div id="<id>" tabindex="-1">`) wrappers (`programme-summary` and `programme-steps` as siblings inside ``screenPanel(`Connected view for ${c.id}`, ...)``, followed by `programme-journey` and `programme-withheld`), adding zero new literal `screenPanel("...")` calls.
  * Observable acceptance criteria: Connected-home VDOM contains `<nav aria-label="Jump to a section of the connected home view">`, four `a[data-jump]` links without inline `onclick`, zero `<button>` tags inside `render()`, ``Connected view for ${c.id}`` panel preserved with `#programme-summary` and `#programme-steps` inside it, zero `tabindex` attributes inside `journeyStageMap(c)`'s `<section>`, and zero ID collisions when mounted alongside `overview()`.
* FR-03: Activating any overview or connected-home `a[data-jump]` link invokes the shared document-level delegated click handler (`role-screens.js:116-123`), calling `event.preventDefault()` (preventing SPA hash router navigation) and `.focus()` on the matching `tabindex="-1"` target section while tolerating missing DOM targets safely.
  * Observable acceptance criteria: Node VM delegated-click test and Chromium keyboard Enter check dispatch activation across all eight jump links in `overview()` and `render()`, verifying `preventDefault()` / SPA route preservation, exact `.focus()` target sequence, and no-throw when a target ID is absent.
* FR-04: Returned-work/handoff rows in `programmeRow()`, lifecycle/funnel status copy in `programmeFunnel()`, and connected-home step states/banners in `programmeGates()` and `render()` express explicit textual state cues (`State: Returned. ...`, `State: Not returned. Handoff state: ...`, `State: Not returned`, `State: Unknown. ...`, `State: Recorded stage history (not a pass). ...`, `Action needed: Blocked...`, `Warning: No recorded blocker`, and `State: Warning. No blocker is recorded...`) while preserving all existing accountability substrings and keeping `"Blocked"` absent when all 5 steps are clear.
  * Observable acceptance criteria: Unit tests verify explicit textual state prefixes on returned, handed-off, and unreturned queue rows, unknown and populated funnel states, and blocked, missing-evidence, and unblocked connected-home step states across all installed roles.
* FR-05: Interactive queue controls (`#programme-prev`, `#programme-next`, `<select id="programme-scope">`, `Apply filter`, `Reset to default view`, scrollable table regions, and row `"Open connected view for <id>"` links) remain native keyboard-accessible elements with explicit accessible names, explicit `role="status"` `"aria-live": "polite"` attributes on `#programme-filter-status` and `#programme-page-status`, and focus handoff when boundary paging buttons disable.
  * Observable acceptance criteria: Unit tests verify native controls, `<label for="programme-scope">`, explicit `role="status"` and `aria-live="polite"` attributes on both queue status regions, focusable table scroll regions with `<caption>` and `<th scope="col">`, and Previous/Next focus handoff when a boundary button disables.

## Non-Functional Requirements

* NFR-01: Repository static accessibility, content-standard, connected-home, tension, and role-screen conformance guardrails remain green.
  * Objective threshold or evaluation condition: Zero banned glossary terms in `role-screens.js` (`test_content_standard.py`), exact static counts preserved (`aria-invalid` == 8, literal `h("table", ...)` == 13, `position: fixed` == 2 in `test_accessibility_baseline.py`), zero undefined CSS classes or forbidden inline styles/`onclick` (`test_role_screens_conformance.py`), zero unauthorized literal `screenPanel("...")` additions (`test_connected_home_check.py`, `test_atlas_tensions_checker.py`), zero global scope collisions with `app.js` (`test_safety_screen_wcag_keyboard.py`), zero `tabindex` inside `journeyStageMap` (`test_role_screens_stage_map_focus.py`), and single `.screen-evidence` table `"Same-home step states"` (`test_specialist_keyboard_check.py`).
  * Operating condition or verification approach, if needed: Execute all corresponding unit test modules in `src/api/tests/`.
  * Observable acceptance criteria: All targeted and cross-cutting `unittest` modules exit `0`.
* NFR-02: Strict Python typing and code formatting/linting in `src/api`.
  * Objective threshold or evaluation condition: Zero `mypy` errors under `strict = true` and zero `ruff check` / `ruff format --check` findings across `src` and `tests` in `src/api`.
  * Operating condition or verification approach, if needed: Run `python3 -m mypy` and `python3 -m ruff check src tests && python3 -m ruff format --check src tests` from `src/api`.
  * Observable acceptance criteria: Both commands exit `0`.

## Acceptance Criteria

* AC-01: `programme-queue.overview()` and `programme-queue.render()` both render `<nav class="screen-links" aria-label="...">` jump bars with four `a[data-jump]` links and four matching disjoint `tabindex="-1"` section targets, with zero `<button>` elements inside `render()` and zero inline `onclick` attributes on jump links.
* AC-02: Delegated `a[data-jump]` activation prevents default hash navigation and moves focus to each matching `tabindex="-1"` target across both `overview()` and `render()`.
* AC-03: Returned-work rows, handoff states, lifecycle/funnel empty and populated summaries, and all five connected-home step states/summaries carry explicit non-colour textual state prefixes without introducing banned glossary words or `"Blocked"` into clear same-home views.
* AC-04: Focused tests in `src/api/tests/test_programme_screen_wcag.py` and `src/api/tests/test_programme_screen.py` (updating module-level `SCRIPT` to register `doc.addEventListener` delegation, retaining `test_existing_state_cells_are_unchanged`, replacing `test_section_links_use_documented_classes_and_move_focus` and `test_no_nav_element_or_other_controls`, updating 2 obsolete button-count assertions in `test_programme_screen.py`, and adding at most 10 focused semantic test methods with 0 file deletions) pass alongside cross-cutting conformance suites (including `test_connected_home_check.py` and `test_atlas_tensions_checker.py`), `mypy`, and `ruff`.
* AC-05: `web-design-guidelines` (`command.md`) pre-edit loading and post-edit `file:line` review complete with zero open findings on changed web code, local browser-check execution (`checks/programme_paging_browser_check.py`) or prerequisite-block disclosure and Focused Tier / unpushed hosted-CI status are recorded, all `.copilot-tracking/` artifacts are reconciled, and one clean local commit (`Refs #230` + Copilot trailer) is recorded on `feat/ux-230-programme-mgr-wcag` without pushing.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/issue-230-programme-mgr-wcag-plan.md                                                                  |
| Phase details                    | .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md                                                       |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/issue-230-programme-mgr-wcag-plan-critique.md with Revise disposition (PC-001 to PC-004 resolved) |
| Relevant research                | .copilot-tracking/research/2026-11-15/issue-230-programme-mgr-wcag-research.md                                                           |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/issue-230-programme-mgr-wcag-changes.md is created by implementation as its evidence record         |
| Planning execution and readiness | Complete and Ready for implementation                                                                                                    |
| Continuation context             | Confirmed automatic RPI Agent parent return -> automatic transition to Implement                                                         |

## Sources

* .copilot-tracking/research/2026-11-15/issue-230-programme-mgr-wcag-research.md: Cycle 1 Wider/Deeper/Contrarian evidence (`C1`–`C15`, `W1`) establishing exact `role-screens.js` targets and cross-cutting invariants.
* docs/reference/research/ux/wcag-conformance-baseline.md: Repository WCAG 2.2 AA baseline (#151), programmatic landmarks/headings, focus visibility, non-colour state text, and engineering-vs-human evidence boundary.
* docs/reference/research/ux/design-system.md: Fluent 2 token and `.btn.alt` / `.card` / `.blocked` component rules (#150).
* docs/reference/research/ux/content-standard.md: Plain-language glossary and banned internal jargon terms (#153).
* src/api/src/zava_forward/api/web/role-screens.js: Canonical `screenJumpNav`, `screenJumpTarget`, delegated `a[data-jump]` handler, and `programme-queue` screen implementation.
* src/api/tests/test_programme_screen.py and src/api/tests/test_programme_screen_wcag.py: Existing functional and partial WCAG unit tests for `programme-queue`.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Upgrade `programme-queue` WCAG 2.2 keyboard jump navigation and textual state labels

* Intent: Align both `overview()` and `render()` in `programme-queue` (`role-screens.js`) with the canonical `<nav aria-label>` + `tabindex="-1"` jump-link delegation pattern and explicit non-colour textual state prefixes across returned work, handoffs, funnel states, and connected-home steps.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add disjoint `programmeJumpNav` and `screenJumpTarget` navigation to `programme-queue` `overview()` and `render()`

* Requirement and evidence: FR-01, FR-02, FR-03, NFR-01 (`C2`, `C6`, `C9`, `C10`, `C13`, `C14`)
* Expected result: Both `overview()` and `render()` render `<nav class="screen-links" aria-label="...">` with four `a[data-jump]` links targeting four disjoint `tabindex="-1"` section wrappers; `programmeJump` and `div[role="group"]` jump `<button>`s are removed; `render()` contains zero `<button>` elements and `journeyStageMap` keeps zero internal `tabindex` attributes.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add explicit non-colour textual state prefixes and polite live-region attributes across queue, funnel, and connected-home step surfaces

* Requirement and evidence: FR-04, FR-05, NFR-01 (`C1`, `C2`, `C4`, `C12`, `C15`, `W1`, `PC-002`)
* Expected result: `programmeQueue` sets `"aria-live": "polite"` on `#programme-filter-status` and `#programme-page-status`; `programmeRow`, `programmeFunnel`, and `programme-queue.render` lead status surfaces with explicit plain-language state cues (`State: Returned.`, `State: Not returned.`, `State: Unknown.`, `State: Recorded stage history (not a pass).`, `State: Warning.`, `Action needed:`, `Warning:`) while preserving raw step cell values (`"Blocked"`, `"Blocked: evidence missing"`, `"No recorded blocker"`), all existing accountability substrings, clear-case `"Blocked"` absence, and glossary compliance.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Reconcile and expand WCAG 2.2 unit tests and execute Focused Tier validation

* Intent: Prove WCAG 2.2 keyboard jump navigation, delegated focus, keyboard controls, and non-colour textual state labels in strict-typed unit tests, verify zero regressions across repository conformance suites, `mypy`, and `ruff`, and record implementation evidence.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update `test_programme_screen.py` and expand `test_programme_screen_wcag.py`

* Requirement and evidence: FR-01 through FR-05, AC-01 through AC-04 (`C4`, `C5`, `C6`, `C7`, `C8`)
* Expected result: `test_programme_screen.py` asserts zero `<button>` elements in read-only `render()`, and `test_programme_screen_wcag.py` verifies `<nav aria-label>` jump links, disjoint `tabindex="-1"` targets in combined `overview` + `render` views, Node VM delegated `a[data-jump]` click focus + `preventDefault()`, explicit textual state labels across queue/funnel/step views, and keyboard control/pager focus handoff across all three installed roles.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Run Focused Tier validation suites, `mypy`, and `ruff`, and write changes artifact

* Requirement and evidence: NFR-01, NFR-02, AC-04, AC-05 (`C11`–`C15`)
* Expected result: Targeted `test_*programme*.py`, cross-cutting conformance/baseline unit tests, `python3 -m mypy`, and `python3 -m ruff check src tests && python3 -m ruff format --check src tests` all exit `0` in `src/api`, and `.copilot-tracking/changes/2026-11-15/issue-230-programme-mgr-wcag-changes.md` records completed work and reconciled checklist markers.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/issue-230-programme-mgr-wcag-phase-details.md

## Dependencies

* Node.js (`node`) and Python 3.12+ (`unittest`, `mypy`, `ruff`) in the local environment: required to execute Node-backed VDOM unit tests (`test_*programme*.py`, conformance suites) and static Python checks in `src/api`.
* Shared `screenJumpNav`, `screenJumpTarget`, and document-level `a[data-jump]` click delegation in `src/api/src/zava_forward/api/web/role-screens.js`: already present on `feat/ux-230-programme-mgr-wcag` from #225 (`d6f863e34`).

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| PC-001 (High: `Connected view for ${c.id}` panel nesting and `test_connected_home_check.py`) | resolved | Updated `FR-02`, `NFR-01`, `P01-T01`, and `P02-T02` to preserve ``screenPanel(`Connected view for ${c.id}`, ...)`` with zero new literal `screenPanel("...")` calls and keep `#programme-summary` and `#programme-steps` as non-nested sibling `screenJumpTarget` wrappers inside it; added `test_connected_home_check.py` and `test_atlas_tensions_checker.py` to validation. |
| PC-002 (High: explicit `"aria-live": "polite"` missing on `programmeQueue()` status paragraphs) | resolved | Updated `FR-05`, `P01`, and `P01-T02` to include `programmeQueue()` (`role-screens.js:412-413`) and add `"aria-live": "polite"` on `#programme-filter-status` and `#programme-page-status`. |
| PC-003 (Medium: exact symbol names and `SCRIPT` harness in `test_programme_screen_wcag.py`) | resolved | Updated `AC-04`, `P02`, and `P02-T01` to name `SCRIPT` (`doc.addEventListener` delegation), `test_section_links_use_documented_classes_and_move_focus`, and `test_no_nav_element_or_other_controls` accurately while explicitly retaining `test_existing_state_cells_are_unchanged`. |
| PC-004 (Low: Web Development Guidance skill/review steps and local browser-check execution/disclosure) | resolved | Updated `AC-05`, `P01`, and `P02-T02` to require pre-edit `web-design-guidelines` + `redesign-existing-projects` loading, post-edit `command.md` `file:line` audit, `python3 -m checks.programme_paging_browser_check` execution (or honest prerequisite-block disclosure), and Focused Tier / unpushed hosted-CI status recording. |
| Accepted residual risk (Engineering vs #155 human/AT sign-off) | accepted with risk | Engineering VDOM/keyboard tests do not establish live screen-reader or human conformance (#155); commit uses `Refs #230` rather than a closing keyword. |

## Follow-Up Items

* Live assistive-technology (NVDA/JAWS/VoiceOver) and user walkthrough validation across specialist screens remains outside this engineering slice and is tracked under #155 per `docs/reference/research/ux/wcag-conformance-baseline.md`.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/issue-230-programme-mgr-wcag-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: none
