<!-- markdownlint-disable-file -->

# Task Research: housing-resident-screens-wcag-232

| Field              | Value                                                                                 |
|--------------------|---------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                            |
| Researcher / agent | RPI Agent (`rpi-research`)                                                            |
| Status             | Complete                                                                              |
| Artifact path      | .copilot-tracking/research/2026-11-15/housing-resident-screens-wcag-232-research.md   |

## Research Brief

* What to research: Current implementation, sibling role-screen WCAG patterns, DOM/accessibility gaps, and test conventions for the Housing Officer (`#/role/housing_officer`) and Resident Engagement (`#/role/resident_engagement`) screens in `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/style.css`, and `src/api/tests/`.
* Why it matters: GitHub issue #232 has 4 of 5 acceptance criteria checked; the remaining code-testable criterion requires WCAG 2.2 baseline (#151) keyboard navigation (section jump nav, landmarks, heading focus targets) and explicit plain-language textual state meaning paired with every status badge, resident choice indicator, pause/withdrawal state, update commitment row, and safe-route indicator.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` in the active automatic RPI loop for #232.
* Scope: `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/style.css` (if shared `.ux-state-cue` or jump-nav styling is needed), and `src/api/tests/` (`test_housing_resident_screen_wcag.py`, `test_role_screens_conformance.py`, and existing accessibility/content tests).
* Non-goals: Resident contact/portal implementation (#154), live assistive-technology/screen-reader conformance claims (#151/#155), unrelated role screens outside `housing_officer` and `resident_engagement` unless shared helpers require safe extension, `sys.modules` deletion in tests, or pushing to remote.
* Criteria: Keyboard-operable section jump navigation (`role="navigation"` or `<nav>`, `aria-label`) with `Go to ...` links for every section landmark; activating jump links moves focus to target headings (`tabindex="-1"`); every status badge, resident choice indicator, pause/withdrawal state, update commitment row, and safe-route indicator pairs colour/badge styling with explicit plain-language textual state cues (`.ux-state-cue` or explicit `State:` / `Meaning:` text) compliant with the content standard (#153); focused unit tests without `sys.modules` deletion hazards.
* Requested outputs: Converged implementation recommendation grounded in exact `path:line` codebase and UX-baseline evidence, ready for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                                              |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | How do `housing_officer` and `resident_engagement` currently render landmarks, jump navigation, focus targets, and state signals, and what exact pattern aligns them with sibling WCAG role screens and existing conformance gates? |
| Codebase scope                   | `src/api/src/zava_forward/api/web/`, `src/api/tests/`, `docs/reference/research/ux/`, `.copilot-tracking/` prior #232 and sibling WCAG artifacts                   |
| External scope                   | Vercel Web Interface Guidelines (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`, required by repository web instructions) |
| Initial internal candidate areas | `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/style.css`, `src/api/tests/test_role_screens_conformance.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/design-system.md`, `docs/reference/research/ux/content-standard.md` |
| Initial external candidate areas | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`                                                                           |
| Research posture                 | focused                                                                                                                                                            |
| Posture provenance               | default (bounded internal task with named source targets, explicit issue #232 criteria, and focused validation tier specified by caller)                           |
| Explicit limits / deadline       | Focused validation tier; keep changes scoped to `src/api` and `.copilot-tracking/*/2026-11-15/`; commit locally with `Refs #232` and do NOT push                   |
| Posture-specific completion basis| focused scope and materiality: all #232 jump-nav, landmark, focus, textual-state, and test-safety questions answered with verified `path:line` evidence            |
| Edits allowed during research?   | no, research-only                                                                                                                                                  |
| Resolved evidence root           | `.copilot-tracking/` default                                                                                                                                       |
| Known constraints / excluded sources | Preserve Fluent 2 tokens (#150), WCAG 2.2 baseline (#151), plain-language glossary (#153: no banned terms `gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope` in guarded UI copy), no resident contact actions (#154), no `sys.modules` deletion in tests, no screen-reader conformance claim |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                                                   | Scoped authority or output contract                                                      | Selected / skipped reason                                                                                      |
|---------------------|----------------------------------|------------------------------------------------------------------------|------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`| `applyTo: "**"` matches repository, `src/api`, and tracking paths      | Enforces Fluent 2, WCAG 2.2 baseline, plain-language content standard, web guideline fetch, and focused validation rules | Selected: mandatory repository instruction set.                                                                |
| Skill               | `rpi-research`                   | Explicit caller RPI phase 1                                            | Three-wave research protocol and primary evidence artifact contract                      | Selected: active RPI phase skill.                                                                              |
| Skill               | `web-design-guidelines`          | Repository web development rule before web edits                       | Fetched `command.md` rules for keyboard, focus, landmarks, `scroll-margin-top`, and ARIA | Selected: mandatory pre-edit web guideline source check.                                                       |
| Skill               | `redesign-existing-projects`     | Repository web development rule for existing-app UI improvements       | Targeted existing-stack upgrades subordinate to Fluent 2, WCAG, and content standard     | Selected: informs semantic HTML and focus/state hygiene without authorizing visual overhauls.                  |
| Skill               | `accessibility`                  | Semantic match for WCAG 2.2 keyboard navigation and non-colour signals | WCAG 2.2 Level AA criteria mapping (1.3.1, 1.4.1, 2.1.1, 2.4.1, 2.4.3, 2.4.6, 4.1.2)     | Selected: canonical accessibility reference contract.                                                          |
| Skill               | `design-taste-frontend`          | Evaluated under web development instructions                           | Public marketing/landing pages only ("Not for dashboards or app screens")                | Skipped: explicitly inapplicable to internal staff workbench screens.                                          |
| Research specialist | `hve-core-all:rpi-researcher`    | Host-registered general RPI lane worker                                | Bounded subagent research lane under `.copilot-tracking/research/subagents/`             | Skipped (inline execution): targets are tightly coupled within `role-screens.js`, `app.js`, and `src/api/tests`.|
| Research specialist | `Neighbourhood Housing Officer` / `Housing Resident Engagement Lead` | Host-registered company role agents | Elicit domain hypotheses from case-study documents                                       | Skipped: #232 domain criteria (1-3, 5) are already delivered; remaining work is code-level WCAG 2.2 mechanics. |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                     | Answers / unanswered | Resulting decision or selected further research                                                  |
|------------------|---------------------------------------------------------------------------------------------------------------------------|----------------------|--------------------------------------------------------------------------------------------------|
| Intake           | Non-interactive session with complete caller brief, target branch, file scope, acceptance focus, and validation commands. | N/A (non-interactive)| Proceed in `focused` posture with `convergence` output mode across all three research waves.     |
| Direction change | Pending cycle execution.                                                                                                  | None                 | Retain caller boundaries.                                                                        |
| Convergence      | All 4 research questions answered with `path:line` evidence across Waves 1-3; contrarian gate catches resolved. | N/A (non-interactive) | Converged on unified route-alias + dynamic jump-nav + plain-language `State:`/state-cue design. |

## Scope and Success Criteria

* Scope: Inspect `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/style.css`, sibling WCAG role-screen implementations and tests in `src/api/tests/`, and prior #232 tracking evidence.
* Assumptions:
  * Sibling role screens (for example finance, procurement, or other `#/role/*` views) or current `role-screens.js` / `app.js` may already define jump-nav or `.ux-state-cue` conventions that `#/role/housing_officer` and `#/role/resident_engagement` should match consistently.
  * Existing static accessibility tests (`test_accessibility_baseline.py`, `test_content_standard.py`, `test_role_screens_conformance.py`, `test_design_system.py`) enforce invariants such as table counts/captions, banned glossary words, or CSS rules that any new markup must satisfy.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and one recommendation is selected in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  * Research and deliver keyboard-operable section jump navigation (`role="navigation"`, `aria-label`) with `Go to ...` links for every section landmark on `#/role/housing_officer` and `#/role/resident_engagement`, focusing target headings (`tabindex="-1"`).
  * Research and deliver explicit plain-language textual state cues (`.ux-state-cue` or explicit `State:` / `Meaning:` text) paired with every status badge, resident choice indicator, pause/withdrawal state, update commitment row, and safe-route indicator on both views.
  * Research and deliver focused conformance tests in `src/api/tests/test_housing_resident_screen_wcag.py` without `sys.modules` deletion hazards.
* Inferred research questions:
  * How does `app.js` handle hash routes (`#/role/housing_officer`, `#/role/resident_engagement`) vs in-page jump links so clicking a jump link focuses the target heading without breaking `#/role/...` routing?
  * What existing `.ux-state-cue`, jump-nav, landmark, heading hierarchy, table-count, and banned-term invariants exist across `src/api/web/` and `src/api/tests/`?
* Caller constraints and non-goals: Focused tier validation; no `sys.modules` deletion in tests; commit locally with `Refs #232` (criterion 4 still requires manual/AT verification per #151/#155 before closing #232); do NOT push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Scope code changes to `src/api` for `housing_officer` and `resident_engagement` WCAG 2.2 increment      | Caller intake       | Restricts implementation target to `src/api` web assets and focused unit tests     |
| exclude                                                  | Do not delete entries from `sys.modules` in tests; do not make resident contact from staff screens; do not push | Caller intake | Constrains test harness design, UI actions, and git closeout                       |

## Research Questions

|  # | Sub-question                                                                                                                                           | Type            | Priority | Status   |
|---:|--------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | How are `#/role/housing_officer` and `#/role/resident_engagement` currently structured in `role-screens.js` and wired in `app.js`?                      | depth           | H        | answered |
| Q2 | What jump-navigation, landmark, and heading-focus conventions already exist in `role-screens.js`, `app.js`, `style.css`, or sibling WCAG role screens? | breadth         | H        | answered |
| Q3 | Which status badges, resident choice indicators, pause/withdrawal states, update commitment rows, and safe-route indicators currently lack explicit textual state cues? | depth | H | answered |
| Q4 | What static/DOM invariants do existing tests (`test_role_screens_conformance.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, existing `*housing*` tests) enforce, and how do we test without `sys.modules` hazards? | breadth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed:
  * `docs/reference/research/ux/wcag-conformance-baseline.md` (#151 WCAG 2.2 AA baseline: native landmarks, focus order, focus visibility, non-colour status signals, and honest automated vs manual AT boundary).
  * `docs/reference/research/ux/design-system.md` (#150 Fluent 2 token and component-class inventory).
  * `docs/reference/research/ux/content-standard.md` (#153 plain-language glossary and banned terms).
  * `docs/reference/research/ux/customer-journeys/frontline.md` and `docs/reference/research/ux/atlas-screen-trace.md` (mapping Housing Officer continuity to `resident-service-issues` and Resident Engagement choice/updates to `resident-choice`).
  * Commit `5a350916d` (initial #232 slice introducing `stateCue`, `residentJumpNav`, `test_resident_screen_wcag.py`, and `test_frontline_screen_wcag.py`).
* Reused (verified) findings:
  * `resident-choice` and `resident-service-issues` are registered in `role-screens.js` (`C1`, `C2`) and share the delegated `a[data-jump]` click handler (`C4`).
  * `stateCue()` and `serviceMeaning()` already classify basic measure/update/service states (`C5`, `C6`), and existing tests assert those exact prefixes (`C9`).
* Superseded / stale:
  * Assuming `#/role/housing_officer` and `#/role/resident_engagement` already exist in `app.js` is invalidated: neither hash route is wired yet (`C3`).
  * Assuming `residentJumpNav` already covers every section landmark with `role="navigation"` and `Go to ...` links is invalidated (`C5`).

## Research Cycle Log

### Cycle 1

#### Wave 1 — Wider (Breadth across UX standards, web router, role-screen host, and sibling WCAG suites)

* Scanned UX baseline specs (`wcag-conformance-baseline.md`, `design-system.md`, `content-standard.md`, `frontline.md`, `atlas-screen-trace.md`), fetched external Web Interface Guidelines (`W1`), and inventoried all role screens and WCAG test suites in `src/api/tests/` (`test_resident_screen_wcag.py`, `test_frontline_screen_wcag.py`, `test_procurement_screen_wcag.py`, `test_finance_screens_wcag_225.py`, `test_role_screens_conformance.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_design_system.py`).
* Identified how sibling role screens (`technical-queue`, `quality-queue`, `safety-hazards`, `finance-invoices`, `procurement-packages`) implement section jump navigation (`screenJumpNav` at `role-screens.js:30` and `hazardJump` at `role-screens.js:996` both emit `Go to ${text}` anchors paired with `screenPanel(..., { anchor })` headings carrying `tabindex: -1`).

#### Wave 2 — Deeper (Exact code inspection of `app.js`, `role-screens.js`, `style.css`, and test harnesses)

* **Routing & lazy script loading (`Q1`)**:
  * `app.js:346` (`missingWorkspaceScripts`) only loads `/role-screens.js` when `destination === "#/screens"`, and `app.js:421` (`route`) only dispatches `#/screens` to `roleScreensView()` (`C3`). Direct navigation to `#/role/housing_officer` or `#/role/resident_engagement` currently falls through to `myCasesView()`.
  * Mapping `#/role/housing_officer` to default screen `"resident-service-issues"` and `#/role/resident_engagement` to default screen `"resident-choice"` in `app.js` and `roleScreensView()` (`role-screens.js:89-105`) connects both named role routes cleanly while keeping `#/screens?screen=...` canonical (`C1`, `C2`, `C3`).
* **Jump navigation, section landmarks, and heading focus (`Q2`)**:
  * `residentJumpNav` (`role-screens.js:839-841`) currently omits `role: "navigation"`, renders bare `title` instead of `` `Go to ${title}` ``, and covers only 4 of 9 `<section>` landmarks in `resident-choice.render(c)` (`Evidence boundary`, `Choice comes before offered capacity`, `Tension: utilisation versus choice`, `Tension: continuity versus disclosure`, and `Not shown for this role` lack `{ anchor }`, `id`, `aria-labelledby`, `tabindex="-1"` on `<h2>`, and jump links) (`C5`).
  * In `resident-service-issues.render(c)` (`role-screens.js:1867-1896`), `Evidence boundary` lacks `{ anchor }`, conditional `Response history` lacks `{ anchor }` and a jump link when present, and missing `c.redress_route` returns a non-section `screenUnknown(...)` while `"service-redress"` remains listed in `serviceSections`, breaking the 1-to-1 link-to-heading target contract when `redress_route` is absent (`C2`, `C6`)! Wrapping missing redress in `screenPanel("Independent human review and formal complaints, without detriment", { anchor: "service-redress" }, screenUnknown(...))` and building `serviceSections` dynamically (`...(hasHistory ? [["service-history", "Response history"]] : [])`) guarantees an exact 1-to-1 bijection across every data state!
  * Both `resident-choice.summary(queue)` (`role-screens.js:904`) and `resident-service-issues.summary(entries)` (`role-screens.js:1866`) also render `<section>` landmarks when no home is selected; anchoring their `<section>` panels and exposing `residentJumpNav` in `summary()` ensures `#/role/housing_officer` and `#/role/resident_engagement` expose keyboard jump navigation in both summary and selected-home states (`C1`, `C2`).
  * Delegated click focus in `role-screens.js:274-280` finds `event.target?.closest?.("a[data-jump]")`, calls `event.preventDefault()`, resolves `document.getElementById(link.dataset.jump)`, calls `heading.focus()`, and calls `heading.scrollIntoView?.({ block: "nearest" })` (`C4`). `style.css:355` defines `.screen-record h2:focus { outline: 3px solid var(--focus); outline-offset: 2px }` and `scroll-margin-top` can be added to `.screen-record h2` per `W1` without adding motion (`C7`).
* **Explicit textual state cues across all indicators (`Q3`)**:
  * Existing `stateCue()` (`role-screens.js:835-838`) prefixes `Confirmed:`, `Waiting for resident:`, or `Action needed:` on `m.status`, `update.status`, `r.status`, `m.accessibility`, and `choiceQueueRow`, and `serviceMeaning()` (`role-screens.js:1825-1827`) prefixes `serviceMeaningText` (`C5`, `C6`).
  * However, the following indicators on Housing Officer (`resident-service-issues`) and Resident Engagement (`resident-choice`) STILL lack explicit textual state cues (`State:` / `Meaning:` / `stateCue`):
    1. **Safe-route indicator** (`safe_contact_ref`): In `resident-choice` `Linked update commitment` (`role-screens.js:933`), `choiceQueueRow` (`role-screens.js:886`), `resident-service-issues` `Linked update commitment` (`role-screens.js:1892`), and `serviceQueueRow` (`role-screens.js:1857`), `safe_contact_ref` renders raw `"SC-77"` or `"Unknown"`. Formatting through a helper `safeRouteCue(ref)` -> ``ref ? `State: Confirmed safe route (${ref}; route reference only, contact details withheld)` : "State: Action needed — Safe route not recorded (Unknown)"`` preserves substring `"SC-77"` and `"Unknown"` while making safe-route state explicit in plain text!
    2. **Measure readiness & pause/withdrawal history cues** (`resident-choice`):
       * `m.readiness` (`role-screens.js:856`) renders raw `screenValue(m.readiness)`. Formatting via `readinessCue(m.readiness)` (e.g. `"Resident decision current"` -> `"State: Confirmed — Resident decision current"`, `"Needs human review"` or unrecorded -> `"State: Action needed — Needs human review"` / `"State: Waiting for resident — Unknown"`) gives explicit state text while preserving `"Needs human review"` and `"Resident decision current"`.
       * `stoppedChoiceRows` (`role-screens.js:870-874`) and `choiceLatest` (`role-screens.js:844-849`) can include explicit `State: Paused by resident — ...` / `State: Withdrawn by resident — ...` prefix in `stoppedChoiceRows` (wait: check `test_resident_choice_screen.py` substrings first! `test_resident_choice_screen.py` checks `Withdrawn (current answer Not recorded), scope S-9, revision 2, design 3` and `Paused (current answer Waiting), scope S-9, revision 2, design 3` as substrings! Prefixing `"State: Action needed — "` before `"Withdrawn (current answer ...)"` and `"Paused (current answer ...)"` preserves the exact substring!).
    3. **Redress formal route status, reviewable decision state, & response history step state** (`resident-service-issues`):
       * `redressRoutePanel` (`role-screens.js:1834-1840`): `d.status` (`stateCue(d.status)`) and `x.formal_route_status` (`formalRouteCue(x.formal_route_status)` -> `"Acknowledged"` => `"State: Confirmed — Acknowledged"`, `"Unconfigured"` / other => `"State: Action needed — Unconfigured"`). Preserves `"Unconfigured"` and `"Paused"` substrings!
       * `Recorded response steps` (`role-screens.js:1886`): `x.status` -> `serviceMeaning(x.status)` (or `stateCue(x.status)`), preserving `"In progress"` while pairing explicit state meaning!
       * Summary open issues (`serviceQueueRow`, `role-screens.js:1848-1859`): `${r.id} ${screenValue(r.route)}: ${r.status} (${stateCue(r.status)})` preserves exact substring `"SR-1 Complaint: Resolved"` required by `test_resident_service_screen.py:124` while adding explicit state cue!
    4. **Queue & header `.flag` / `.flag.danger` badges on Housing Officer & Resident Engagement views** (`role-screens.js:135, 144`):
       * `.flag.danger` (`"Safety issue open"`) and `.flag` (`"Same home: case ..."`): On `resident-choice` and `resident-service-issues`, pair each `.flag` badge with an explicit sibling `<span class="muted" data-state-cue="badge">State: ...</span>` so `span.flag.danger` retains its exact text `"Safety issue open"` (`test_role_screens.py:240`) while giving every badge on both views an explicit plain-language `State:` cue!

#### Wave 3 — Contrarian (Challenging candidate designs against strict repository regression gates)

* **Contrarian Challenge 1 — Adding `.ux-state-cue` CSS class vs `test_design_system.py` (`C8`)**:
  * Hypothesis tested: Add a new `.ux-state-cue` class to `role-screens.js` and `style.css`.
  * Counter-evidence found: `test_design_system.py:96-105` (`test_role_screen_classes_are_defined_and_documented`) parses every `class: "..."` token in `role-screens.js` and asserts it appears in BOTH `style.css` AND `docs/reference/research/ux/design-system.md`! Because the caller scoped this increment cleanly to `src/api` and explicitly allowed `(.ux-state-cue or explicit State: / Meaning: text)`, using existing design-system classes (`muted`, `status-line`, `flag`, `screen-links`, `screen-record`) plus `data-state-cue` attributes and explicit `State:` / `Meaning:` / `Confirmed:` / `Waiting for resident:` / `Action needed:` text satisfies every #232 requirement without violating `test_design_system.py` or touching `docs/`.
* **Contrarian Challenge 2 — Global `screenWithheld` / `screenTension` anchors vs sibling screen tests (`C10`)**:
  * Hypothesis tested: Make `screenWithheld` and `screenTension` unconditionally emit `<section id="...">`.
  * Counter-evidence found: `test_assessor_screen_wcag.py` asserts `targets_in_nav == sections_with_id` on `technical-queue`! Making `anchor` an **optional** parameter (`screenWithheld(items, anchor = null)` and `screenTension(kind, anchor = null)`) leaves all other role screens untouched while giving `resident-choice` anchored landmarks for every `<section>`.
* **Contrarian Challenge 3 — Jump-link labels containing `"capacity"` or `"utilisation"` on `resident-choice` (`C11`)**:
  * Hypothesis tested: Use raw `<h2>` panel titles directly as `Go to ${title}` link text in `residentJumpNav` at the top of `resident-choice.render(c)`.
  * Counter-evidence found: `test_role_screens.py:288-294` (`test_resident_choice_states_choice_precedence_after_choice_panels`) concatenates all panel/nav text BEFORE the `"Choice comes before offered capacity"` section and asserts `"capacity"`, `"utilisation"`, and `"headroom"` do NOT appear before that section! Using concise plain-language jump labels `"Go to Choice precedence rule"` and `"Go to Design tension on resident choice"` (matching `hazardJump`'s short-label pattern at `role-screens.js:986-995`) keeps capacity/utilisation framing below the resident's choices AND passes `test_role_screens.py`!
* **Contrarian Challenge 4 — Table count, control-free, and banned-glossary-word gates (`C12`)**:
  * `test_accessibility_baseline.py` pins raw `h("table", {},` across `web/*.js` to `13`; `test_resident_choice_screen.py` pins `3` tables in `render` and `1` in `overview`; `test_resident_service_screen.py` pins `2` tables in `render` (without `redress_route` formal requests) and `1` in `summary`; both tests ban `<button>`, `<form>`, `<input>`, `<select>`, `<textarea>`; `test_content_standard.py` bans `gate(s)`, `hold(s)`, `provenance`, `trace(s)`, `snapshot(s)`, `envelope(s)`; `test_connected_home_check.py` checks `screenPanel("...")` titles and `EXCLUDED["resident-choice"]` anchors. Our converged design preserves every single invariant.
* **Cycle Re-entry Evaluation**: All 4 questions (`Q1`-`Q4`) and all contrarian challenges have verified `path:line` evidence; no unresolved uncertainty remains. Cycle 1 is sufficient under `focused` posture.

## Evidence Log

| ID   | Location / URL                                                                                     | Finding                                                                                                                                                 |
|------|----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `C1` | `src/api/src/zava_forward/api/web/role-screens.js:901-958`                                         | `resident-choice` registration, `summary(queue)`, and `render(c)` panels (9 `<section>` panels, only 4 currently anchored).                             |
| `C2` | `src/api/src/zava_forward/api/web/role-screens.js:1862-1897`                                       | `resident-service-issues` registration, `summary(entries)`, and `render(c)` panels (`Evidence boundary`, `Response history`, and missing `redress_route` gap). |
| `C3` | `src/api/src/zava_forward/api/web/app.js:335-351,405-425`                                          | `missingWorkspaceScripts` and `route()` only handle `#/screens`, not `#/role/housing_officer` or `#/role/resident_engagement`.                          |
| `C4` | `src/api/src/zava_forward/api/web/role-screens.js:19-31,274-280`                                   | `screenPanel` sets `id`, `aria-labelledby`, and `<h2 tabindex="-1">` when `{ anchor }` is given; delegated click listener focuses `a[data-jump]` target.|
| `C5` | `src/api/src/zava_forward/api/web/role-screens.js:835-899`                                         | `stateCue` and `residentJumpNav` (currently lacks `role="navigation"`, `Go to ...` prefix, `readiness` state cue, and `safe_contact_ref` state cue).    |
| `C6` | `src/api/src/zava_forward/api/web/role-screens.js:1815-1860`                                       | `serviceMeaning`, `redressRoutePanel` (`formal_route_status` lacks state cue; missing `redress_route` omits section landmark), and `serviceQueueRow`.   |
| `C7` | `src/api/src/zava_forward/api/web/style.css:342-360`                                               | `.screen-links` and `.screen-record h2:focus` focus ring rules; `.screen-*` rules enforced motion-free by `test_role_screens_conformance.py`.           |
| `C8` | `src/api/tests/test_design_system.py:96-105`                                                       | Every CSS class used in `role-screens.js` must exist in both `style.css` and `docs/reference/research/ux/design-system.md`.                             |
| `C9` | `src/api/tests/test_resident_screen_wcag.py:55-88`, `src/api/tests/test_frontline_screen_wcag.py:55-75` | Existing #232 unit tests pin `Confirmed:`, `Waiting for resident:`, `Action needed:`, `tabindex == -1`, and literal `screenPanel("...")` strings.  |
| `C10`| `src/api/tests/test_role_screens_tensions_same_home.py:67-95`                                      | Pins `screenTension(` call count (`5`) and bans `style`, `icon`, `<svg`, `aria-invalid`, `simulat`, `impersonat` between `screenTensionText` and `screenTable`. |
| `C11`| `src/api/tests/test_role_screens.py:236-295`                                                       | Pins `.flag.danger` exact text `"Safety issue open"` and bans `"capacity"`, `"utilisation"`, `"headroom"` before `"Choice comes before offered capacity"`. |
| `C12`| `src/api/tests/test_connected_home_check.py:183-214`, `src/api/tests/test_content_standard.py:1-60`| Enforces exact `screenPanel` title inventory, `EXCLUDED` source anchors, table counts, zero form controls, and banned glossary words.                    |
| `W1` | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` (retrieved 2026-11-15) | Requires keyboard operability, visible `:focus-visible` / `:focus` outlines, `scroll-margin-top` on heading anchor targets, semantic landmarks, and non-colour status text. |

## Synthesis and Converged Recommendation

### Alternatives Compared

| Option | Summary | Pros | Cons / Rejection Reason |
|---|---|---|---|
| **Option A (Selected)** | Wire `#/role/housing_officer` (`resident-service-issues`) and `#/role/resident_engagement` (`resident-choice`) in `app.js` and `roleScreensView()`; upgrade `residentJumpNav` with `role="navigation"`, `aria-label`, and `Go to ...` links covering 100% of rendered `<section>` landmarks (via optional `anchor` on `screenTension`/`screenWithheld` and dynamic section lists); add explicit plain-language `State:` / `Meaning:` / `stateCue` cues + `data-state-cue` attributes across every status badge, choice/readiness cell, pause/withdrawal row, update commitment row, redress/history row, and safe-route indicator using existing documented design-system classes; add `scroll-margin-top` to `.screen-record h2` in `style.css`; verify in `src/api/tests/test_housing_resident_screen_wcag.py` via Node `vm` + JSDOM-free/clean DOM harness without `sys.modules` deletion. | Satisfies 100% of caller deliverables within `src/api`; preserves every existing invariant across `test_design_system.py`, `test_role_screens.py`, `test_connected_home_check.py`, `test_role_screens_tensions_same_home.py`, `test_accessibility_baseline.py`, and `test_content_standard.py`. | Jump-link labels on `resident-choice` must use `"Go to Choice precedence rule"` and `"Go to Design tension on resident choice"` to avoid capacity/utilisation wording above resident choices (`C11`). |
| **Option B (Rejected)** | Introduce a new `.ux-state-cue` CSS class in `role-screens.js` and `style.css` without editing `docs/reference/research/ux/design-system.md`. | Explicit CSS class name matching one prompt example. | Rejected: `test_design_system.py:96-105` (`C8`) fails immediately if `role-screens.js` references any CSS class not documented in `docs/reference/research/ux/design-system.md`, violating the `src/api`-scoped increment. |
| **Option C (Rejected)** | Globally mutate `screenWithheld` and `screenTension` to always emit `id` attributes on `<section>`. | Slightly shorter helper signature. | Rejected: Adds unlinked `<section id=...>` landmarks to `technical-queue` and `procurement-packages`, breaking sibling jump-nav bijection tests (`C10`). |

### Current Decisions and Readiness

* **Research disposition**: `executed` (complete 3-wave cycle: Wider, Deeper, Contrarian).
* **Planning Readiness**: `Ready`.
* **Residual risks & boundaries**:
  * Keep exact `screenTension(` count at `5` in `role-screens.js` (`test_role_screens_tensions_same_home.py:94`, `C10` — note `function screenTension(` counts as 1 of the 5 matches of `screenTension\(`! Let's preserve `function screenTension(kind, anchor)` so `screenTension(` count stays `5`!).
  * Do not claim live assistive-technology / screen-reader sign-off (#151 / #155); keep commit trailer `Refs #232` rather than `Closes #232`.
  * Never delete from `sys.modules` in `src/api/tests/test_housing_resident_screen_wcag.py`.

## Further Research (Deferred / Out of Scope)

* Manual assistive-technology (NVDA/JAWS/VoiceOver) and resident-facing validation remain tracked under #151 and #155 before closing #232's final checkbox on `main`.

