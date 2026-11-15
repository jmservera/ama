---
description: "Primary evidence artifact for issue #230 programme manager and coordinator screens WCAG 2.2 compliance"
---
<!-- markdownlint-disable-file -->

# Task Research: issue-230-programme-mgr-wcag

| Field              | Value                                                                               |
|--------------------|-------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                          |
| Researcher / agent | rpi-research (under RPI Agent)                                                      |
| Status             | Complete                                                                            |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-230-programme-mgr-wcag-research.md      |

## Research Brief

* What to research: Remaining unchecked acceptance criterion on GitHub issue #230 (`Programme manager and coordinator screens`): WCAG 2.2 baseline (#151) compliance with explicit textual state meaning and keyboard section jump navigation (`nav aria-label` jump links, `tabindex="-1"` section targets, delegated jump focus, keyboard-accessible controls, and non-colour state labels across shared queue, returned work, connected same-home gates, and lifecycle/funnel views).
* Why it matters: Delivers the engineering accessibility contract for issue #230 consistent with sibling role screens (#225 finance/grants, #226 asset executive, #227 safety/repairs) without regressing existing conformance, table-count, `aria-invalid`-count, content-standard, or browser-check guardrails.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` phases in this RPI session, plus human reviewers auditing PR evidence for issue #230.
* Scope: `src/api/src/zava_forward/api/web/` (specifically `role-screens.js` and related programme/coordinator web modules and CSS if needed), `src/api/tests/` (`test_*programme*.py`, `test_accessibility_baseline.py`, `test_role_screens*.py`, `test_specialist_keyboard_check.py`), `src/api/checks/` (`specialist_keyboard_browser_check.py`, `role_screens_browser_check.py`), and `docs/reference/research/ux/` baselines.
* Non-goals: Claiming live human/screen-reader conformance (#155 / manual check record remains `Not run`), introducing a role simulator in user views, changing backend case-state mutations on reset, or pushing to remote.
* Criteria: Every programme manager / coordinator screen surface has keyboard jump navigation (`nav[aria-label]` to `tabindex="-1"` target sections with delegated focus), explicit textual state labels on returned-work/gate/funnel badges and indicators, plain-language glossary compliance (#153), Fluent 2 token alignment (#150), and focused unit/accessibility test coverage passing `unittest`, `mypy`, and `ruff`.
* Requested outputs: Converged implementation recommendation with exact file/function targets, invariant constraints, and test strategy for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                   |
|----------------------------------|---------------------------------------------------------------------------------------------------------|
| Research question(s)             | Where do programme manager and coordinator screens live, what WCAG 2.2 keyboard/state-label patternsalready exist or are missing compared with #225/#226/#227, and which cross-cutting repository invariants constrain edits? |
| Codebase scope                   | `src/api/src/zava_forward/api/web/`, `src/api/tests/`, `src/api/checks/`, `docs/reference/research/ux/` |
| External scope                   | Vercel Web Interface Guidelines (`command.md`) per repository Web Development Guidance                   |
| Initial internal candidate areas | `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_programme_screen.py`, `src/api/tests/test_programme_screen_wcag.py`, `src/api/tests/test_accessibility_baseline.py` |
| Initial external candidate areas | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`                |
| Research posture                 | focused                                                                                                 |
| Posture provenance               | default (bounded internal task with named source targets and explicit acceptance criteria)              |
| Explicit limits / deadline       | Non-interactive session; do not push to remote; leave clean frozen local commit on `feat/ux-230-programme-mgr-wcag` |
| Posture-specific completion basis| focused scope and materiality                                                                           |
| Edits allowed during research?   | no, research-only                                                                                       |
| Resolved evidence root           | `.copilot-tracking/`                                                                                    |
| Known constraints / excluded sources | Preserve `docs/case_study_48_original.md`, Fluent 2 tokens, plain-language glossary, and static audit counts (`aria-invalid`, table captions/headers, fixed-position rules) |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | AMA Repository Instructions      | `applyTo: "**"`                                   | Governance, UX/WCAG/content baselines, tier classification, branch/commit rules | Selected: mandatory repo-wide instructions |
| Skill               | `rpi-research`                   | Explicit RPI loop phase 1                         | Three-wave evidence artifact contract        | Selected: active RPI phase skill |
| Skill               | `web-design-guidelines`          | Repository Web Development Guidance               | Fetch current `command.md` rules and review `file:line` | Selected: mandatory before web edits/review |
| Skill               | `redesign-existing-projects`     | Repository Web Development Guidance               | Existing-app audit subordinate to Fluent 2 / WCAG / plain-language baselines | Selected: existing-app UI improvement guidance |
| Skill               | `accessibility`                  | WCAG 2.2 / ARIA APG reference contract            | WCAG 2.2 success criteria mapping            | Selected: directly matches WCAG 2.2 criterion |
| Research specialist | `hve-core-all:rpi-researcher`    | General delegated lane worker                     | Compact lane provenance under `subagents/`   | Skipped: tightly coupled single-module web/test trace fits inline investigation faster and cleaner |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit scope, branch, acceptance criterion, validation commands, and commit instructions | Not applicable (non-interactive) | Proceed with `focused` posture and `convergence` output mode |
| Direction change | No scope or direction ambiguity remained after Wave 1 verified `programme-queue` in `role-screens.js` | Not applicable | Retain narrow `src/api` scope on `programme-queue` (`overview` and `render`) |
| Convergence      | Cycle 1 Wider, Deeper, and Contrarian answered Q1-Q4 with zero open blockers | Not applicable | Converge on `screenJumpNav` + `screenJumpTarget` + explicit textual state prefixes across `programme-queue` |

## Scope and Success Criteria

* Scope: Programme manager, planner, and coordinator screen rendering, keyboard jump navigation, section focus targets, textual state labels, keyboard-operable controls, and focused unit/accessibility tests in `src/api/`.
* Assumptions:
  * The programme manager/coordinator screens may reside inside `role-screens.js` (like finance/asset/safety) rather than a standalone `programme_manager.js` file; must verify in Wave 1.
  * Partial WCAG work may already exist in `test_programme_screen_wcag.py`; must verify exact current coverage vs gaps against #225/#226/#227.
* Success criteria:
  * Every research question is answered with `path:line` evidence (`C#`) and external guideline evidence (`W#`).
  * Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian complete in order.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Inspect programme manager/coordinator screen module and existing tests; identify gaps for full WCAG 2.2 keyboard jump navigation (`nav aria-label`, `tabindex="-1"`, textual state meaning on all returned-work/gate/funnel badges and indicators, keyboard-accessible controls) matching #225/#226/#227; prepare test and validation plan.
* Inferred research questions: How `RoleScreenConformance`, `test_accessibility_baseline.py`, `test_content_standard.py`, and `specialist_keyboard_browser_check.py` constrain changes to `role-screens.js` or programme modules.
* Caller constraints and non-goals: Research-only in this phase; no source edits until `rpi-implement`; no remote push; engineering evidence does not claim human assistive-technology acceptance.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Focus on issue #230 unchecked WCAG 2.2 criterion in `src/api` | Caller intake prompt | Scopes Cycle 1 to programme/coordinator web module and `src/api/tests/` |
| exclude                                                  | Do not push to remote; do not add role simulator or mutate records on reset | Caller intake prompt | Preserves existing checked #230 criteria and local-commit-only boundary |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status                    |
|---:|------------------|------------------------------------------|-----------|---------------------------|
| Q1 | Which module(s) and routes implement the programme manager, planner, and coordinator screens (#230), and what is already tested in `test_programme_screen*.py`? | straightforward | H | answered |
| Q2 | How do `asset_executive`, `safety_repairs`, and `finance_grants` (#226, #227, #225) implement WCAG 2.2 keyboard jump navigation, `tabindex="-1"` targets, delegated jump focus, and textual state labels? | depth | H | answered |
| Q3 | Which badges, returned-work items, connected same-home gates, funnel/lifecycle indicators, or interactive controls on the programme/coordinator screen lack explicit textual state meaning or keyboard jump/focus support? | depth | H | answered |
| Q4 | What cross-cutting static/conformance invariants (`test_accessibility_baseline.py`, `test_role_screens_conformance.py`, `test_content_standard.py`, `specialist_keyboard_browser_check.py`, `test_epic149_*.py`) could break if modified carelessly? | breadth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/design-system.md`, `docs/reference/research/ux/content-standard.md`, `docs/reference/research/ux/atlas-screen-trace.md`, `.copilot-tracking/research/2026-11-14-225-finance-grants-wcag-research.md`, `.copilot-tracking/rpi-sessions/2026-11-14/issue-225-c2-conformance-fix-state.json`.
* Reused (verified) findings: Static inventory guards exist for `aria-invalid` site count (8), script-built table captions and `th scope` (13 literal `h("table", ...)` call sites), fixed-position rules (2), plain-language banned terms, and `RoleScreenConformance` forbidding inline styles and restricting `onclick` (`a[data-jump]` delegation at `role-screens.js:268-275` introduced in commit `d6f863e34`).
* Superseded / stale: Prompt mentions `programme_manager.js` "(or the programme manager / coordinator screen module under `src/api/src/zava_forward/api/web/`)"; verified that no standalone `programme_manager.js` exists and all specialist screens live in `src/api/src/zava_forward/api/web/role-screens.js`. Earlier partial commit `5bc6b8d81` added `div[role="group"]` jump `<button>` controls only inside `programme-queue.render()`, omitted `<nav aria-label>` jump links, omitted `overview()` jump navigation/targets, and left returned-work/funnel states without uniform explicit state prefixes.

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow to issue #230 WCAG 2.2 criterion in `src/api`; exclude remote push, role simulator, and record mutation on reset.
* Active research posture and completion basis: `focused`; focused scope and materiality.
* Explicit limits or deadline effect: non-interactive CLI session; all investigation performed inline against the worktree.

#### Wave 1: Wider

* Plan and independent lanes: Map all files under `src/api/src/zava_forward/api/web/`, `src/api/tests/`, `src/api/checks/`, and `docs/reference/research/ux/atlas-screen-trace.md` that implement or test the programme manager, planner, and coordinator screens (#230) and sibling WCAG 2.2 screens (#225, #226, #227).
* Worker evidence relationships or inline fallback: Inline investigation mapped Q1 -> `programme-queue` in `src/api/src/zava_forward/api/web/role-screens.js:353-680` (`C1`, `C2`), traced in `docs/reference/research/ux/atlas-screen-trace.md:31-32` (`C3`), tested in `src/api/tests/test_programme_screen.py:1-583` (`C4`) and `src/api/tests/test_programme_screen_wcag.py:1-130` (`C5`), alongside sibling WCAG tests `test_finance_screens_wcag_225.py`, `test_asset_exec_screen_wcag.py`, and `test_safety_screen_wcag_keyboard.py` (`C6`, `C7`, `C8`). Also inspected `coordinatorView` in `app.js:2302-2427` to confirm `#/coordinator` is the separate overview cohort drill route while #230's specialist role screen is `programme-queue`.
* Reflection: `programme-queue` serves `Retrofit Programme Manager`, `Programme Support Officer`, and `Retrofit Coordinator` via two rendered surfaces: `overview(signal, items, c, page)` (shared queue + scope filter/reset/paging + lifecycle/funnel + tension + withheld) and `render(c, extra)` (connected same-home 5-step view + journey stage map + tension + withheld). Prioritizing deeper comparison of `programme-queue` against #225/#226/#227 jump navigation and textual state conventions.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Exact DOM/event structure of `screenJumpNav`, `screenJumpTarget`, delegated `a[data-jump]` handling, CSS specificity on `nav a` vs `.btn.alt` / `.screen-links`, and textual state labels in `programmeRow`, `programmeQueue`, `programmeFunnel`, `programmeGates`, and `programme-queue.render`.
* Plan and independent lanes: Read `role-screens.js:1-355`, `role-screens.js:353-680`, `role-screens.js:890-1080`, `style.css:45-60,230-235,370-380`, and external Vercel Web Interface Guidelines (`W1`).
* Worker evidence relationships or inline fallback: Inline inspection established:
  * Q2 -> `role-screens.js:28-32` already provides `screenJumpTarget(id, panel)` (`<div id={id} tabindex="-1">`) and `screenJumpNav(label, jumps)` (`<nav class="row" aria-label={label}>` with `<a href="#id" class="btn alt" data-jump={id} data-jump-target={id}>Go to ...</a>`), backed by document-level delegated click handling at `role-screens.js:268-275` (`event.target.closest?.("a[data-jump]")`, `preventDefault()`, `getElementById(...).focus()`, `scrollIntoView`) (`C6`, `C9`). In `style.css:51` `.btn.alt` (`0,2,0`) overrides `nav a` (`0,0,2` at `style.css:231`) and enforces `min-height: 2.5rem` (40px target size, WCAG 2.5.8) (`C10`).
  * Q3 -> Identified four concrete WCAG/consistency gaps in `programme-queue`:
    1. `render()` (`role-screens.js:657-679`) currently renders `<div class="row" role="group" aria-label="Jump to a section of this screen">` with `<button type="button" onclick={programmeJump(id)}>` instead of `<nav aria-label="...">` jump links (`a[data-jump]`), violating the #225/#226/#227 `<nav aria-label>` jump-link pattern (`C2`, `C6`, `C7`, `C8`) and breaking `programme_paging_browser_check.py:193-203` (`C14`).
    2. `overview()` (`role-screens.js:638-652`) has zero section jump `<nav aria-label>` and zero `tabindex="-1"` section targets across its main sections (`Evidence boundary`, `Shared queue`, `Lifecycle and funnel`, `Not shown for this role`) (`C2`).
    3. Returned-work and handoff cells in `programmeRow(row)` (`role-screens.js:384-397`) output raw `work.returned.reason` (e.g., `"Missing survey"`) without an explicit textual state prefix (`"State: Returned — ..."` or `"State: Returned. ..."`), whereas non-returned rows say `"Not returned. Handoff state: ..."` or `"Not returned"`, and proposed-receiver / chase / update cells lack uniform state clarity when handoff is absent vs offered (`C1`).
    4. Lifecycle/funnel summary and stage rows in `programmeFunnel(report)` (`role-screens.js:476-484`) and the unblocked connected-home notice in `render()` (`role-screens.js:673`) can express explicit textual state labels (e.g., `"State: Unknown. Lifecycle and funnel counts are Unknown..."`, `"State: Recorded stage history (not a readiness pass)..."`, `"State: Warning — no recorded blocker (not a pass)..."`, and explicit state prefixes in `programmeGateRow` / `programmeQualityRow` or summary) without relying on visual styling (`C1`, `C2`, `W1`).
* Reflection: Deep design aligns cleanly with `screenJumpNav` + `screenJumpTarget`, but Contrarian testing is needed to check whether changing `<button>` to `<a>` in `render()`, adding jump links in `overview()`, or adjusting cell strings breaks any existing unit, conformance, lexical, or Playwright check.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge proposed DOM and text changes against every static guardrail, conformance test, stage-map focus test, heading-hierarchy test, and browser check in `src/api/tests/` and `src/api/checks/`.
* Plan and independent lanes: Inspect `test_accessibility_baseline.py`, `test_content_standard.py`, `test_role_screens_conformance.py`, `test_role_screens_stage_map_focus.py`, `test_safety_screen_wcag_keyboard.py`, `specialist_keyboard_browser_check.py`, `programme_paging_browser_check.py`, `atlas_tensions_browser_check.py`, and `connected_home_browser_check.py`.
* Worker evidence relationships or inline fallback: Contrarian verification surfaced seven critical constraints (`C11`–`C15`):
  1. **Playwright button set & Tab-count ceiling (`programme_paging_browser_check.py:89,193-212`) (`C14`)**:
     * Line 202 asserts `main button` texts equal `{"Previous page", "Next page", "Apply filter", "Reset to default view"}`! Replacing the 4 `<button>` jump controls in `render()` with `<nav aria-label> <a data-jump>` RESTORES `main button == QUEUE_CONTROLS` when a home is selected!
     * Line 206 focuses `aside a[data-reset]` and calls `press_until(page, "Tab", "programme-next")` with default `limit=6`! Because `overview` renders inside `div.main` right after `aside.side`, an overview jump `<nav>` placed before `#programme-next` MUST contain **at most 4 jump links** (4 link Tabs + 1 Tab to `#programme-next` = 5 Tabs `<= 6`) so keyboard paging traversal from `aside a[data-reset]` reaches `#programme-next` within 5 Tab presses!
  2. **Stage-map zero-`tabindex` invariant (`test_role_screens_stage_map_focus.py:55-96`) (`C13`)**:
     * Any element *inside* `<section><h2>Journey stages for ...</h2>...</section>` with `tabindex` fails `mapTabindex == 0`. Wrapping `journeyStageMap(c)` in an outer `screenJumpTarget("programme-journey", journeyStageMap(c))` (`<div id="programme-journey" tabindex="-1">`) keeps `tabindex="-1"` outside the stage-map `<section>`, preserving `mapTabindex == 0`.
  3. **Banned lexical terms (`test_content_standard.py:13-55`) (`C12`)**:
     * Standalone words `gate`, `gates`, `hold`, `holds`, `provenance`, `trace`, `traces`, `snapshot`, `snapshots`, `envelope`, `envelopes` are banned anywhere in `role-screens.js` (including comments and jump link labels!). Jump labels and state text must say `"Same-home step states"` / `"step"`, never `"gate"` or `"gates"`.
  4. **Specialist keyboard region tuple (`specialist_keyboard_browser_check.py:45`) (`C15`)**:
     * `EXPECTED_REGIONS["programme-queue"] == ("Same-home step states",)` checks `.screen-evidence table` captions inside `render()`. `render()` must keep exactly that one table with caption `"Same-home step states"`.
  5. **Static baseline counts (`test_accessibility_baseline.py:59-165`) (`C11`)**:
     * `setAttribute("aria-invalid", "true")` count across `web/*.js` must stay `8`; literal `h("table", ...)` call sites must stay `13`; CSS `position: fixed` rules must stay `2`.
  6. **Clear-case substring guard (`test_programme_screen.py:451`) (`C4`)**:
     * `self.assertNotIn("Blocked", clear)` asserts the word `"Blocked"` never appears anywhere in `render()` when all 5 steps have no recorded blocker! State text for unblocked steps must use `"Warning: No recorded blocker (not a pass)"` / `"No recorded blocker"` and never mention `"Blocked"` in the clear case.
  7. **Existing cell assertions in `test_programme_screen.py` & `test_programme_screen_wcag.py` (`C4`, `C5`)**:
     * `test_programme_screen.py` lines 385-386 and 538 were modified in `5bc6b8d81` to expect `tags(node).count("button") == 4` on `render()`; switching `render()` jump controls to `<nav aria-label>` + `<a data-jump>` restores `render()` to zero `<button>` elements (`self.assertNotIn("button", tags(node))`), matching `asset-board` and `safety-lead`. Meanwhile, substring assertions in `test_programme_screen.py` (`"Missing survey"`, `"Offered"`, `"No handoff proposed"`, `"No handoff recorded"`, `"Lifecycle and funnel counts are Unknown"`, `"Blocked: evidence missing"`, `"No recorded blocker"`) and `connected_home_browser_check.py` / `atlas_tensions_browser_check.py` must be preserved intact!
* Reflection: Contrarian wave caught two subtle potential regressions (`programme_paging_browser_check.py` `main button` + 6-Tab ceiling, and `test_content_standard.py` banning `"gate"`/`"gates"`). No gaps remain.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment  |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|-----------------------------|
| Implement `<nav aria-label>` jump links + `tabindex="-1"` targets in BOTH `programme-queue.overview()` (4 targets) and `programme-queue.render()` (4 targets) via `screenJumpNav` and `screenJumpTarget` | C2, C6, C9, C10, C13, C14 | accepted | Matches #225/#226/#227, uses existing delegated `a[data-jump]` handler (`role-screens.js:268-275`), keeps `<= 4` overview jump links (`5 <= 6` Tabs to `#programme-next`), avoids inline `onclick`, and restores zero `<button>` tags inside read-only `render()` | Selected Recommendation |
| Add explicit non-colour textual state prefixes to returned-work/handoff queue cells, funnel status/summary, and connected-home step states while preserving existing substrings and clear-case `"Blocked"` exclusion | C1, C2, C4, C5, C12, W1 | accepted | Satisfies WCAG 2.2 SC 1.4.1 / 1.3.1 / 2.4.6 and #230 criterion without breaking `test_programme_screen.py`, `test_content_standard.py`, or browser checks | Selected Recommendation |
| Keep `<div role="group">` + `<button onclick={programmeJump}>` in `render()` | C2, C5, C14 | rejected | Fails prompt requirement for `nav aria-label` jump links and breaks `programme_paging_browser_check.py:202` (`buttons == QUEUE_CONTROLS`) | Rejected Alternative 1 |
| Put `tabindex="-1"` directly on headings inside `journeyStageMap` | C13 | rejected | Breaks `test_role_screens_stage_map_focus.py` (`mapTabindex == 0`) | Rejected Alternative 2 |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: focused scope saturated; all four research questions (Q1-Q4) have high-confidence `path:line` and external guideline evidence, and contrarian checks resolved all cross-cutting test/browser constraints.
* Revised brief or revalidation required: none
* Readiness effect: `Ready`

## Evidence Log

* Delegation: inline: bounded single-module web and unit-test investigation in `src/api/` with tightly coupled invariants across `role-screens.js` and `src/api/tests/`.

### Codebase Evidence

| ID  | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|-----|-----------------|------------------------|------|------------|-------|
| C1  | `programmeScopes`, `programmeRow`, `programmeQueue`, `programmeFunnel`, `programmeGateRow`, `programmeQualityRow`, and `programmeGates` define the shared queue, filter/reset/pager controls, funnel table, and 5 connected-home step rows. | `src/api/src/zava_forward/api/web/role-screens.js:353-623` | view | high | Returned reason currently lacks `"State: Returned"` prefix; funnel lacks explicit `"State: ..."` prefix. |
| C2  | `registerRoleScreen({ id: "programme-queue", ... })` serves `Retrofit Programme Manager`, `Programme Support Officer`, and `Retrofit Coordinator` with `overview()` (no jump nav/targets) and `render()` (currently `div[role="group"]` + 4 `<button>` jump controls). | `src/api/src/zava_forward/api/web/role-screens.js:625-680` | view | high | Primary edit target for #230 WCAG compliance. |
| C3  | Atlas screen trace maps both `Programme coordinator` and `Retrofit case team` perspectives to `programme-queue` (`overview` and connected home view). | `docs/reference/research/ux/atlas-screen-trace.md:31-32` | view | high | Confirms `programme-queue` is the canonical #230 screen module. |
| C4  | `test_programme_screen.py` tests default/scope filtering, non-mutating reset, 50-case paging, connected-view row links, 5 independent same-home step states, and `assertNotIn("Blocked", clear)`. | `src/api/tests/test_programme_screen.py:1-583` | view | high | Lines 385-386 and 538 currently expect 4 jump `<button>`s in `render()` from partial commit `5bc6b8d81`. |
| C5  | `test_programme_screen_wcag.py` currently tests `State summary in words` prefixes and the `div[role="group"]` button jump bar, explicitly asserting `no <nav>` in `render()`. | `src/api/tests/test_programme_screen_wcag.py:1-130` | view | high | Must be updated and expanded for `<nav aria-label>` jump links across both `overview()` and `render()` and textual state labels across queue/funnel/step views. |
| C6  | `screenJumpTarget(id, panel)` and `screenJumpNav(label, jumps)` in `role-screens.js` implement `<nav class="row" aria-label={label}>` with `<a href="#id" class="btn alt" data-jump={id} data-jump-target={id}>Go to ...</a>` and `<div id={id} tabindex="-1">`, tested by `test_finance_screens_wcag_225.py`. | `src/api/src/zava_forward/api/web/role-screens.js:28-32` | view | high | Canonical sibling helper from #225 (`d6f863e34`). |
| C7  | `asset-board` (#226) uses `<nav aria-label="Jump to section" class="screen-links">` with `<a href="#..." data-jump-target="...">` and `tabindex="-1"` section headings, tested in `test_asset_exec_screen_wcag.py`. | `src/api/tests/test_asset_exec_screen_wcag.py:1-175` | view | high | Sibling WCAG pattern for #226. |
| C8  | `safety-lead` and `hazard-triage` (#227) use `<nav aria-label="Sections on this screen" class="screen-links">` with `Go to ...` links, `tabindex="-1"` targets, and textual state prefixes (`Stop-work indicator:`, `Escalation state:`), tested in `test_safety_screen_wcag_keyboard.py`. | `src/api/src/zava_forward/api/web/role-screens.js:972-1010` | view | high | Sibling WCAG pattern for #227; `test_safety_screen_wcag_keyboard.py` also enforces zero global identifier collisions with `app.js`. |
| C9  | Shared delegated click listener intercepts `a[data-jump]`, calls `event.preventDefault()` so SPA hash routing does not navigate away, focuses `document.getElementById(id)`, and scrolls into view respecting reduced motion. | `src/api/src/zava_forward/api/web/role-screens.js:268-275` | view | high | Zero inline `onclick` needed when links carry `data-jump`. |
| C10 | `.btn.alt` (`style.css:49-51`) sets `min-height: 2.5rem`, `background: var(--surface)`, `color: var(--brand)` with specificity `0,2,0`, overriding `nav a { color: #fff }` (`0,0,2` at `style.css:231`) and meeting WCAG 2.5.8 target size. | `src/api/src/zava_forward/api/web/style.css:49-54` | view | high | Confirms `screenJumpNav` links have high contrast and 40px height without CSS edits. |
| C11 | `test_accessibility_baseline.py` enforces exact repo-wide counts: 8 `aria-invalid` sites, 13 literal `h("table", ...)` sites, and 2 `position: fixed` rules, plus skip-link and `:focus-visible` checks. | `src/api/tests/test_accessibility_baseline.py:59-165` | view | high | Must not add `aria-invalid`, raw `h("table", ...)`, or `position: fixed`. |
| C12 | `test_content_standard.py` bans standalone words `gate`, `gates`, `hold`, `holds`, `provenance`, `trace`, `traces`, `snapshot`, `snapshots`, `envelope`, `envelopes` anywhere in `role-screens.js`. | `src/api/tests/test_content_standard.py:13-55` | view | high | Use `"Same-home step states"` / `"step"` in labels, state strings, and comments; never `"gate"`/`"gates"`. |
| C13 | `test_role_screens_stage_map_focus.py` requires `mapTabindex == 0` and no nested headings inside `<section><h2>Journey stages for ...</h2></section>`. | `src/api/tests/test_role_screens_stage_map_focus.py:55-96` | view | high | Keep `screenJumpTarget("programme-journey", journeyStageMap(c))` as an outer wrapper `<div id="programme-journey" tabindex="-1">`. |
| C14 | `programme_paging_browser_check.py` asserts `main button` texts equal `{"Previous page", "Next page", "Apply filter", "Reset to default view"}` and tabs from `aside a[data-reset]` to `#programme-next` with `limit=6`. | `src/api/checks/programme_paging_browser_check.py:89-95,193-212` | view | high | Using `<a>` in `<nav>` fixes `main button == QUEUE_CONTROLS`, and keeping `<= 4` jump links in `overview()` guarantees `#programme-next` is reached in `<= 5` Tabs. |
| C15 | `specialist_keyboard_browser_check.py` expects `.screen-evidence table` captions on `programme-queue` to equal `("Same-home step states",)`. | `src/api/checks/specialist_keyboard_browser_check.py:41-52` | view | high | Preserve single table `"Same-home step states"` in `programme-queue.render()`. |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|
| W1 | Interactive controls require native `<button>`/`<a>` semantics, visible `:focus-visible` rings, `aria-label` on landmark `<nav>` regions, explicit labels on form inputs, `aria-live="polite"` status updates, `tabular-nums` for numeric comparisons, and non-colour state text. | Vercel Web Interface Guidelines (`command.md`) | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` | 2026-11-15 | main (current) | high |

### Contradictions / Conflicts

* Jump control element type in `programme-queue.render()`: Partial commit `5bc6b8d81` (`C2`, `C5`) used `<div role="group">` with four `<button>` elements and asserted `no <nav>`, whereas the caller prompt, sibling screens #225/#226/#227 (`C6`–`C8`), and `programme_paging_browser_check.py:202` (`C14`) require `<nav aria-label>` with jump links (`<a data-jump>`) and no extra `<button>` elements in `main`; resolved by caller scope and consistency with #225/#226/#227 + `C14` -> replace `div[role="group"]` buttons with `screenJumpNav` (`<nav aria-label> <a data-jump>`) in both `overview()` and `render()` and update `test_programme_screen.py` / `test_programme_screen_wcag.py`.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | Programme manager, support officer, and coordinator specialist views live in `programme-queue` inside `src/api/src/zava_forward/api/web/role-screens.js` (`overview()` for shared queue + funnel, `render()` for connected same-home 5-step view + stage map). | C1, C2, C3, C4, C5 | high | Scopes implementation to `role-screens.js` and `src/api/tests/test_*programme*.py`. |
| Q2 | Sibling screens (#225, #226, #227) use `<nav aria-label="...">` containing `<a href="#id" data-jump="id" data-jump-target="id">Go to ...</a>` handled by the shared delegated listener (`role-screens.js:268-275`) and focusing `tabindex="-1"` section targets, paired with explicit text prefixes (`Action needed:`, `Warning:`, `State:`) on all status surfaces. | C6, C7, C8, C9, C10, W1 | high | Reuse `screenJumpNav` and `screenJumpTarget` directly rather than bespoke `onclick` handlers. |
| Q3 | `programme-queue.overview()` lacks `<nav aria-label>` jump links and `tabindex="-1"` section targets; `programme-queue.render()` uses `<div role="group">` `<button>`s instead of `<nav aria-label>` jump links; `programmeRow` returned-work cells, `programmeFunnel` summary/empty states, and connected-home step/readiness notices need consistent explicit textual state meaning; keyboard controls in `programmeQueue` (Previous/Next focus handoff when disabled, labelled `<select>`, Apply/Reset buttons, focusable scroll regions) are already native and should also support Escape-to-jump-nav or clean focus ergonomics without altering URL/record invariants. | C1, C2, C4, C5, W1 | high | Defines exact DOM and copy upgrades in `role-screens.js`. |
| Q4 | Seven repo guardrails constrain implementation: `main button == QUEUE_CONTROLS` and `<= 6` Tabs from `aside a[data-reset]` to `#programme-next` (`C14`), `mapTabindex == 0` inside `journeyStageMap` (`C13`), banned words `gate`/`gates`/`hold`/`snapshot` (`C12`), single `.screen-evidence table` `"Same-home step states"` (`C15`), fixed `aria-invalid`/`h("table")`/`position: fixed` counts (`C11`), no `"Blocked"` in clear connected-home view (`C4`), and zero global identifier collisions with `app.js` (`C8`). | C4, C8, C11, C12, C13, C14, C15 | high | Eliminates regression risk during `rpi-implement`. |

## Key Discoveries

* Reusing `screenJumpNav` and `screenJumpTarget` (`role-screens.js:28-32`) in `programme-queue` simultaneously satisfies the #225/#226/#227 `<nav aria-label>` + `tabindex="-1"` requirement, eliminates the inline `programmeJump` `onclick` helper, and fixes the `main button == QUEUE_CONTROLS` mismatch in `programme_paging_browser_check.py`.
* Keeping `overview()` jump navigation to 4 links (`Evidence boundary`, `Shared queue`, `Lifecycle and funnel`, `Not shown for this role`) ensures keyboard Tab from `aside a[data-reset]` reaches `#programme-next` on the 5th Tab press, staying strictly inside `programme_paging_browser_check.py`'s `limit=6`.
* Prefixing returned-work queue cells (`"State: Returned. <reason>"` vs `"State: Not returned. Handoff state: <state>."` vs `"State: Not returned"`), funnel status paragraphs (`"State: Unknown. Lifecycle and funnel counts are Unknown..."` and `"State: Recorded stage history (not a readiness pass)..."`), and connected-home step cells/summaries with explicit plain-language state cues delivers full WCAG 2.2 SC 1.4.1 non-colour meaning while preserving every existing substring checked by `test_programme_screen.py` and browser harnesses.

### Complete Examples

```javascript
const programmeOverviewSections = [
  ["programme-overview-boundary", "Evidence boundary"],
  ["programme-shared-queue", "Shared queue"],
  ["programme-funnel", "Lifecycle and funnel"],
  ["programme-overview-withheld", "Not shown for this role"]
];
const programmeSections = [
  ["programme-boundary", "Evidence boundary and state summary"],
  ["programme-steps", "Same-home step states"],
  ["programme-journey", "Journey stages"],
  ["programme-withheld", "Not shown for this role"]
];
```

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Upgrade `programme-queue` in `src/api/src/zava_forward/api/web/role-screens.js` to use `screenJumpNav` (`<nav class="row" aria-label="...">` with `<a href="#..." class="btn alt" data-jump="..." data-jump-target="...">Go to ...</a>`) and `screenJumpTarget` (`<div id="..." tabindex="-1">`) in both `overview()` (4 section targets) and `render()` (4 section targets), remove the bespoke `div[role="group"]` `<button onclick={programmeJump}>` bar, add explicit textual state meaning across returned-work/handoff queue cells, lifecycle/funnel states, and connected-home step states/summaries, and update/expand `src/api/tests/test_programme_screen_wcag.py` and `src/api/tests/test_programme_screen.py`.
* Rationale: Directly matches #225 (`d6f863e34`), #226, and #227, honours Fluent 2 `.btn.alt` contrast and 40px target sizing (`C10`), preserves `RoleScreenConformance` (`no onclick` needed via delegated `a[data-jump]`), preserves `programme_paging_browser_check.py` button set and Tab budget (`C14`), and preserves `journeyStageMap` zero-`tabindex` (`C13`) and plain-language glossary rules (`C12`).
* Evidence refs: C1, C2, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, W1
* Implementation impact: `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_programme_screen_wcag.py`, `src/api/tests/test_programme_screen.py`.
* Confidence: high: every target file, DOM helper, CSS rule, and test invariant has been verified in-tree.

File tree:

```text
src/api/
  src/zava_forward/api/web/
    role-screens.js                     (modify programme-queue jump nav, targets, and textual state labels)
  tests/
    test_programme_screen.py            (update render() button-count assertions to match <nav> <a> jump links)
    test_programme_screen_wcag.py       (expand WCAG 2.2 jump-nav, tabindex="-1", delegated focus, and textual state tests)
```

### Alternative: Retain `div[role="group"]` with `<button>` jump controls in `render()` and add a second button bar in `overview()`

* Approach: Keep `programmeJump` `<button>` elements inside `div[role="group"]` instead of `<nav aria-label>` with `<a data-jump>`.
* Trade-offs: Avoids touching two assertions in `test_programme_screen.py`, but fails the explicit caller specification (`nav aria-label` jump links), diverges from #225/#226/#227, requires inline `onclick` handlers, and breaks `programme_paging_browser_check.py:202` (`buttons == QUEUE_CONTROLS`).
* Evidence refs: C2, C4, C6, C14
* Rejection rationale: Violates explicit user requirement and breaks the programme paging browser check invariant.

### Alternative: Place `tabindex="-1"` directly inside `journeyStageMap(c)` heading

* Approach: Pass `{ anchor: "programme-journey" }` into `journeyStageMap` so its `<h2>` receives `tabindex="-1"`.
* Trade-offs: Removes one wrapper `<div>`, but adds `tabindex` inside the `Journey stages for ...` `<section>`, directly failing `test_role_screens_stage_map_focus.py`.
* Evidence refs: C13
* Rejection rationale: Breaks `StageMapAnnouncements.test_stage_map_adds_no_tab_stops_and_no_nested_headings`.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Ensure overview and connected-home jump target IDs are completely disjoint (`programme-overview-*` / `programme-shared-queue` / `programme-funnel` vs `programme-boundary` / `programme-steps` / `programme-journey` / `programme-withheld`) because `roleScreensView()` (`role-screens.js:203`) mounts `overview` AND `selected` simultaneously in `div.main` when a home `c` is selected! (Verified: distinct IDs prevent duplicate `id` attributes in the live DOM — WCAG 4.1.1 / DOM hygiene!)
* Follow-up: Live assistive-technology (NVDA/VoiceOver) and user validation remain tracked under #155 per `docs/reference/research/ux/wcag-conformance-baseline.md`; engineering tests must not claim manual AT sign-off.
* Residual uncertainty: none for engineering implementation.

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|-----------|--------------|--------------|
| Implement `<nav aria-label>` jump links + `tabindex="-1"` targets in both `programme-queue.overview()` and `programme-queue.render()` with disjoint DOM IDs | confirmed | user + evidence | Both surfaces mount simultaneously when a case is selected (`role-screens.js:203`); disjoint IDs prevent duplicate-ID defects while giving full keyboard jump navigation on both overview and connected-home views | C2, C6, C9, C14 | 4 overview targets + 4 connected-home targets using `screenJumpNav` and `screenJumpTarget` |
| Express explicit non-colour textual state prefixes across returned-work/handoff rows, funnel status, and connected-home step states without using banned glossary terms (`gate`/`gates`/`hold`/`snapshot`) | confirmed | user + constraint | Meets WCAG 2.2 SC 1.4.1 and #230 acceptance criterion while preserving `test_content_standard.py` and existing `test_programme_screen.py` substrings | C1, C4, C12, W1 | Zero lexical or functional test regressions |
| Classify validation as Focused Tier under Repository Instructions | confirmed | repository instruction | Scoped web UI + unit-test update in `src/api/` with no infra, SQL, workflow, dependency, Dockerfile, or security-control change | C2, C4, C5 | Run targeted `test_*programme*.py`, cross-cutting web/conformance tests, `mypy`, and `ruff` in `src/api` |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| None | None | N/A | None | non-blocking |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Manual assistive-technology screen-reader walkthrough (#155) | Validates live spoken announcements with NVDA/JAWS/VoiceOver | Dedicated #155 human testing session | deferred | Q2, Q3; C11 |

## Planning Readiness

* Status: Ready
* Decision state: Converged on `screenJumpNav` + `screenJumpTarget` with disjoint IDs across `programme-queue.overview()` and `programme-queue.render()`, plus explicit textual state prefixes across queue, funnel, and connected-home step surfaces.
* Evidence basis: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, W1
* Preconditions met: All target modules, sibling patterns, CSS rules, and test/browser invariants verified with exact `path:line` evidence.
* Blockers: none
* Smallest action to change readiness: none (already `Ready`)

## Closeout Record

| Field                            | Record |
|----------------------------------|--------|
| Research execution status        | Complete |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian completed in order |
| Lane evidence or inline fallback | Inline investigation across `src/api/src/zava_forward/api/web/`, `src/api/tests/`, `src/api/checks/`, and `docs/reference/research/ux/` |
| Research disposition             | executed |
| Planning Readiness               | Ready (C1-C15, W1) |
| Blockers                         | none |
| Continuation owner and state     | confirmed automatic RPI Agent; automatic continuation to `Plan` |

## Advisory Next Step

| Field                            | Record |
|----------------------------------|--------|
| Research disposition             | executed |
| Planning Readiness               | Ready (C1-C15, W1) |
| Output mode and planning support | convergence; yes, converged single implementation design |
| Acting owner                     | confirmed automatic RPI Agent |
| Required gates or confirmations  | Cycle 1 three waves passed; Evidence Log complete; Planning Readiness `Ready`; pre-transition state write passed |
| Continuation result              | automatic continuation to `rpi-plan` |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/issue-230-programme-mgr-wcag-research.md |
| Notes for planning or re-entry   | Keep overview and connected-home jump target IDs disjoint because `overview` and `selected` mount together when a home is selected; keep overview jump links `<= 4`; avoid banned words `gate`/`gates`/`hold`/`snapshot` in `role-screens.js`. |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All four research questions are answered with verified codebase (`C1`–`C15`) and external (`W1`) evidence; further research would be redundant.

## Sources

* W1 - Vercel Web Interface Guidelines (`command.md`) - https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-11-15, main)

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
