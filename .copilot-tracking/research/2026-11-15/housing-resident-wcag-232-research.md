<!-- markdownlint-disable-file -->

# Task Research: housing-resident-wcag-232

| Field              | Value                                                                |
|--------------------|----------------------------------------------------------------------|
| Date               | 2026-11-15                                                           |
| Researcher / agent | RPI Agent (`rpi-research`)                                           |
| Status             | Complete                                                             |
| Artifact path      | .copilot-tracking/research/2026-11-15/housing-resident-wcag-232-research.md |

## Research Brief

* What to research: Current WCAG 2.2 AA accessibility implementation across neighbourhood housing officer, contact-centre, and resident engagement staff screens (`resident-choice`, `resident-service-issues`, `#/role/housing_officer`, `#/role/resident_engagement`, and `resident_choice_queue` / frontline projections in `app.js`, `role-screens.js`, `index.html`, `style.css`, `taskqueues.py`, and `projection.py`), compared against peer `#228` and `#231` accessibility implementations and baseline guards.
* Why it matters: Issue #232 has one remaining unticked acceptance criterion (`Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation`). We need complete engineering coverage across both `app.js` and `role-screens.js` surfaces, `aria-live` status announcements, programmatic focus management, semantic landmarks/headings/tables, textual state meaning, no resident contact trigger or role simulator, and focused verification in `src/api/tests/test_housing_resident_wcag_232.py`.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` phases of the current automatic RPI loop for Issue #232.
* Scope: `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/index.html`, `src/api/src/zava_forward/api/web/style.css`, `src/core/src/zava_forward/core/taskqueues.py`, `src/core/src/zava_forward/core/projection.py`, `src/api/checks/`, `src/api/pyproject.toml`, `src/api/tests/test_housing_resident_wcag_232.py`, and directly related UX baseline documentation if materially changed.
* Non-goals: Adding resident-facing portal functionality (#154) or outbound resident contact triggers; adding a role simulator in user views; claiming WCAG 2.2 conformance or assistive-technology/human validation (#151, #155) without named human testers; pushing to remote.
* Criteria: Every housing-officer, contact-centre, and resident-engagement queue and detail element satisfies the WCAG 2.2 AA engineering baseline (#151) including explicit textual state meaning (no colour-only badges/status), semantic landmarks/headings/tables (`<caption>`, `<th scope="col">`, `<th scope="row">`), keyboard focusability and operable controls, SPA-safe programmatic focus management, and `aria-live` status announcements without resident contact triggers or role simulators; focused validation commands pass cleanly.
* Requested outputs: Synthesized findings, gap comparison against `#228` and `#231`, convergence recommendation, and Planning Readiness for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                                                  |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | Q1-Q6 covering housing/resident screen entrypoints, peer `#228`/`#231` parity, `aria-live` announcements, programmatic focus & keyboard nav, core projections, and baseline guards |
| Codebase scope                   | `src/api/`, `src/core/`, `docs/reference/research/ux/`, `.copilot-tracking/`                                                                                           |
| External scope                   | Vercel Web Interface Guidelines (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`)                                             |
| Initial internal candidate areas | `src/api/src/zava_forward/api/web/{app.js,role-screens.js,index.html,style.css}`, `src/core/src/zava_forward/core/{taskqueues.py,projection.py}`, `src/api/tests/*wcag*.py`, `src/api/checks/*browser_check.py` |
| Initial external candidate areas | Vercel Web Interface Guidelines (`command.md`)                                                                                                                         |
| Research posture                 | balanced                                                                                                                                                               |
| Posture provenance               | default (bounded internal UX/accessibility task with named source targets plus adjacent cross-screen `#228`/`#231`/`#229` interactions on the branch)                  |
| Explicit limits / deadline       | Non-interactive CLI run; Focused validation tier; commit locally with `Refs #232`; do NOT push                                                                         |
| Posture-specific completion basis| Balanced scope coverage and adequate evidence across all named web, core, check, and baseline guard surfaces                                                           |
| Edits allowed during research?   | no, research-only                                                                                                                                                      |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                                                   |
| Known constraints / excluded sources | Preserve Fluent 2 tokens, WCAG baseline (#151), plain-language content standard (#153), counted baseline guards (`test_accessibility_baseline.py`), read-only staff boundaries (no resident contact triggers, no role simulator), and honest human-AT boundaries (`Refs #232`, not `Closes #232`) |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                                            | Scoped authority or output contract                                              | Selected / skipped reason                                                                 |
|---------------------|---------------------------------------|-----------------------------------------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` matches workspace and evidence paths            | Enforces AMA repo rules, Fluent 2/WCAG/content standards, Focused tier, `Refs #232` | Selected: mandatory repository instruction                                                |
| Skill               | `rpi-research`                        | Phase skill for Research in RPI Agent                           | Governs three-wave research artifact and readiness handoff                       | Selected: active RPI phase contract                                                       |
| Skill               | `accessibility`                       | Matches WCAG 2.2 AA, ARIA APG, live regions, keyboard focus     | Supplies WCAG 2.2 / ARIA APG criteria and verification guidance                  | Selected: loaded at intake for WCAG 2.2 evaluation                                        |
| Skill               | `web-design-guidelines`               | Required by AMA Web Development Guidance before web edits       | Supplies fetched Vercel Web Interface Guidelines rules (`file:line` review)      | Selected: loaded and fetched at intake                                                    |
| Skill               | `redesign-existing-projects`          | Required by AMA Web Development Guidance for existing-app UX    | Targeted HTML/CSS/JS audit within existing stack without visual overhaul         | Selected: loaded at intake; constrained by Fluent 2, WCAG, and content standards          |
| Skill               | `design-taste-frontend`               | Public landing/marketing page art direction                     | Explicitly "Not for dashboards or app screens"                                   | Skipped: Zava Forward staff workbench is an internal app/dashboard                        |
| Research specialist | `hve-core-all:rpi-researcher`         | General research lane subagent                                  | Bounded lane evidence under `.copilot-tracking/research/subagents/`              | Skipped (inline preferred): tightly coupled 6-file web/core trace fits direct reads cleanly |
| Research specialist | `Housing Resident Engagement Lead` / `Neighbourhood Housing Officer` | Domain role research instruments | Elicits sector-informed hypotheses when requirements are unknown                 | Skipped: Issue #232 requirements and atlas contracts (O01-O05, O13, O15) are already fixed |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                 | Answers / unanswered | Resulting decision or selected further research                                           |
|------------------|-------------------------------------------------------------------------------------------------------|----------------------|-------------------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit caller scope, target files, test path, and validation rules | Not applicable       | Proceed in confirmed automatic mode with `balanced` posture and inline three-wave audit   |
| Direction change | No scope or boundary change encountered during Cycle 1                | Not applicable       | Keep active boundaries and complete Cycle 1 synthesis                                     |
| Convergence      | All Q1-Q6 questions answered with direct codebase and rule evidence   | Not applicable       | Converged on Selected Recommendation Option B; Planning Readiness = `Ready`               |

## Scope and Success Criteria

* Scope: Neighbourhood housing officer, contact-centre, and resident engagement staff views across `app.js`, `role-screens.js`, `index.html`, `style.css` (note caller prompt mentions `styles.css`; verify actual asset filename `style.css`), `taskqueues.py`, `projection.py`, browser/unit checks, and `src/api/tests/test_housing_resident_wcag_232.py`.
* Assumptions:
  * Earlier commits (`321a22960` `#1763`, `fe6398197` `#1764`, `db52dfff4`, `6176d744d`) already landed partial WCAG improvements on this branch lineage, so we must verify exact current code state rather than assuming either a greenfield screen or complete coverage.
  * Caller-named `styles.css`, `test_procurement_wcag_228.py`, and `test_retrofit_wcag_231.py` map to repository paths `style.css` and existing `#228`/`#231` WCAG test modules, while `src/api/tests/test_housing_resident_wcag_232.py` is an explicit deliverable required by Requirement 3 and Requirement 4.
* Success criteria:
  * Every research question is answered with `path:line` codebase evidence (`C#`) and external rule evidence (`W#`).
  * Any remaining WCAG 2.2 AA gaps (textual state meaning, landmarks/headings/tables, keyboard operability, programmatic focus, `aria-live` status announcements, content-standard/guard safety, no contact triggers or role simulator) are identified with exact locations.
  * Alternatives are evaluated and one convergence recommendation is selected.
  * Artifact self-check passes and Planning Readiness is recorded accurately.

## Task Research Requests

* Explicit requests:
  1. Inspect housing officer, contact-centre, and resident engagement staff screens (`resident_choice_queue` / resident engagement views in `app.js`, `index.html`, `style.css`/`styles.css`, `taskqueues.py`, `projection.py`) and compare with `#228` and `#231` accessibility implementations.
  2. Ensure all housing-officer and resident-engagement queue/detail elements satisfy WCAG 2.2 AA baseline (#151): explicit textual state meaning, semantic landmarks/headings/tables, keyboard focusability and operable controls, programmatic focus management, and `aria-live` status announcements without any resident contact trigger or role simulator.
  3. Add focused verification in `src/api/tests/test_housing_resident_wcag_232.py` (and update `src/api/pyproject.toml` mypy overrides if needed).
  4. Run the three specified Focused validation commands, commit with `Refs #232` and the Copilot trailer, leave a clean working tree, and do not push.
* Inferred research questions:
  * How do both `app.js` (main workbench routes `#/role/housing_officer`, `#/role/resident_engagement`, case/worklist/resident choice queue surfaces) and `role-screens.js` (`#/screens/resident-choice`, `#/screens/resident-service-issues`) render and announce state transitions via `aria-live`?
  * What did `#1763` (`321a22960`), `#1764` (`fe6398197`), and `#231` (`db52dfff4` / `6176d744d`) already implement, and what gaps remain across `app.js`, `role-screens.js`, `index.html`, `style.css`, `taskqueues.py`, `projection.py`, and browser/unit harnesses?
* Caller constraints and non-goals: No resident contact triggers, no role simulator in user views, preserve existing counted guards in `test_accessibility_baseline.py` and `test_content_standard.py`, do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                      |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|----------------------------------------------------------------------------------------|
| narrow                                                   | Target Issue #232 WCAG 2.2 baseline criterion (#151) and deliver `src/api/tests/test_housing_resident_wcag_232.py` | Caller intake       | Constrains implementation and verification to housing/resident staff screens and tests |
| exclude                                                  | No resident contact triggers, no resident-facing portal views (#154), no role simulator, no `git push`  | Caller intake       | Hard safety and workflow guardrails across all waves                                   |

## Research Questions

|  # | Sub-question                                                                                                                                   | Type (depth / breadth / straightforward) | Priority | Status |
|---:|------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|--------|
| Q1 | Which routes, components, and files render neighbourhood housing officer, contact-centre, and resident engagement staff screens in `web/` and `core/`? | breadth                                  | H        | answered |
| Q2 | How do `#228` and `#231` (and `#1763`/`#1764`) implement WCAG 2.2 AA textual state meaning, row headers, jump navigation, focus, and live announcements? | depth                                    | H        | answered |
| Q3 | Do housing-officer and resident-engagement screens emit `aria-live` status announcements and manage programmatic focus on route, home-selection, and jump transitions in both `app.js` and `role-screens.js`? | depth                                    | H        | answered |
| Q4 | Are there any remaining colour-only badges/flags/statuses, missing semantic landmarks/headings/tables, keyboard-inaccessible regions/controls, or banned jargon/contact/simulator leaks in `app.js`, `role-screens.js`, `index.html`, `style.css`, `taskqueues.py`, or `projection.py`? | depth                                    | H        | answered |
| Q5 | Which baseline static guards (`test_accessibility_baseline.py`, `test_content_standard.py`, `rename-zava-tests.py`, `pyproject.toml` mypy overrides, browser checks) constrain changes to `web/` and `tests/`? | straightforward                          | H        | answered |
| Q6 | What verification structure in `src/api/tests/test_housing_resident_wcag_232.py` provides thorough static + rendered DOM/Node-VM behavioral proof without duplicating fragile assumptions? | depth                                    | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed:
  * `docs/reference/research/ux/wcag-conformance-baseline.md`
  * `docs/reference/research/ux/design-system.md`
  * `docs/reference/research/ux/content-standard.md`
  * `.copilot-tracking/rpi-sessions/2026-11-15/retrofit-technical-quality-wcag-231-state.json`
* Reused (verified) findings:
  * Automated engineering checks and axe scans do not establish human assistive-technology testing (#151, #155), so commits must use `Refs #232` and never claim WCAG conformance.
  * `test_accessibility_baseline.py` enforces exact counts on script-built tables (`14` in `app.js` scope), `aria-invalid` sites (`9`), fixed-position CSS selectors, contrast ratios, and focus tokens.
* Superseded / stale:
  * Earlier 2026-11-13 status notes predated `321a22960` (#1763), `fe6398197` (#1764), `db52dfff4` (#231), and `6176d744d`; all current web and core files were inspected fresh at `HEAD` (`6176d744d`).

## Cycle 1 Execution

### Wave 1 — Wider (Breadth Discovery)

* Mode: Inline (tightly coupled single-repo web/core/test audit; subagent delegation skipped as recorded in the Extension Registry).
* Investigated all candidate surfaces across `src/api/src/zava_forward/api/web/`, `src/core/src/zava_forward/core/`, `docs/prds/`, `docs/reference/research/ux/`, `src/api/tests/`, and `src/api/checks/`:
  * Mapped shell landmarks in `index.html` (`skip-link` -> `main#app[tabindex="-1"]`, `#workspace-status` `role="status" aria-live="polite" aria-atomic="true"`).
  * Mapped stylesheet tokens and WCAG focus/reflow/reduced-motion/forced-colors rules in `style.css` (confirming the repo uses `style.css`, not `styles.css`).
  * Mapped peer WCAG test suites for `#228` (`test_procurement_screen_wcag.py`), `#231` (`test_technical_quality_screens_wcag.py`), `#227` (`test_safety_screen_wcag_keyboard.py`), `#229` (`test_data_steward_screen_wcag.py`), and `#232` (`test_housing_resident_screen_wcag.py`, `test_resident_screen_wcag.py`, `test_frontline_screen_wcag.py`).
  * Mapped all staff surfaces serving neighbourhood housing officers, contact-centre officers, and resident engagement staff:
    1. Specialist role-screen routes `#/role/housing_officer` -> `resident-service-issues` and `#/role/resident_engagement` -> `resident-choice` (plus `#/screens?screen=resident-choice|resident-service-issues`) in `app.js` and `role-screens.js`.
    2. Backend `resident_choice_queue` projection and role gates in `store.py`, `projection.py`, and `taskqueues.py`.
    3. Case workspace Resident panel (`residentPanel` + `actForm` in `panels.js`, mounted on `#/case/<id>?tab=resident`), explicitly designated in PRD FR-055 row 3 (`docs/prds/zava-forward-retrofit-programme-demonstrator.md:822`) as the *"Case view panel in the housing and resident engagement workbench"* for *"Neighbourhood officer and contact-centre officer"*.

### Wave 2 — Deeper (Detailed Contract & Accessibility Inspection)

* Prioritized and inspected line-by-line:
  * **Route aliases (`C1`, `C2`, `C15`)**: `app.js:370-376` (`isRoleScreensDestination`) and `role-screens.js:91-96` (`ROLE_HASH_SCREENS`) wire `#/role/housing_officer` and `#/role/resident_engagement`, but omit `#/role/contact_centre` -> `"resident-service-issues"`, even though Issue #232 and PRD line 822 explicitly include contact-centre staff alongside neighbourhood housing officers and resident engagement staff.
  * **Specialist host `aria-live` announcements (`C3`, `C4`, `C13`)**:
    * `index.html:21` mounts `#workspace-status` with `role="status" aria-live="polite" aria-atomic="true"`.
    * In `role-screens.js:180`, `roleScreensView()` sets the settled announcement `${me.user.role}. ${screen.title}. ${c ? 'Selected home ' + c.id + '.' : 'No home selected.'}` (pinned by `specialist_keyboard_browser_check.py:68-70`).
    * However, during intermediate and failure states in `roleScreensView()` (`Invalid screen page` at line 110, `Screen unavailable` at line 114, chooser `!screen` at line 122, loading at line 129, and mismatched `c.id !== caseId` at line 133), `workspaceStatus.textContent` is never updated from `route()`'s generic string. Furthermore, inline `<p role="status">` elements in `role-screens.js` at lines 34 (`screenTable` truncation notice), 129 (`Loading recorded evidence.`), and 145 (`Choose a home` count) omit explicit `aria-live="polite"`.
  * **Programmatic focus management (`C5`, `C6`, `C7`)**:
    * `app.js:114-124` (`show()`) focuses `<main id="app" tabindex="-1">` on route/selection/reset transitions unless focus is inside an open `.chat-widget` or an external shell element in the same route context.
    * `role-screens.js:97-98` (`residentJumpNav`) and `role-screens.js:304-311` (`a[data-jump]` click delegation) focus `<h2 id="...-heading" tabindex="-1">` and scroll it to `{ block: "start" }`; lines 309-310 duplicate `document.getElementById(...)` lookup and can resolve the target element once cleanly.
  * **Housing/contact-centre/resident-engagement case panel (`panels.js`, `C8`, `C9`)**:
    * `panels.js:43-64` (`actForm`, used for all 5 `recordForm(...)` controls in `residentPanel`) constructs input/select IDs as ``id: `f-${title}-${name}` `` — producing invalid HTML5 IDs containing whitespace (e.g. `id="f-Record what the resident said-measure"`), and omits explicit `type: "button"` on the action `<button>`.
    * `panels.js:229-231` (`Resident decisions by measure` table in `residentPanel`) lacks a keyboard-focusable scrollable wrapper (`<div class="table-scroll" role="region" aria-label="Resident decisions by measure" tabindex="0">`), uses `<td>` instead of `<th scope="row">` on the first column (measure name), and renders raw `${m.status}. ${m.readiness}` without the non-colour plain-language prefix (`Confirmed` / `Waiting for resident` / `Action needed`) used on `resident-choice`; contractor fallback `c.resident_readiness` (`panels.js:170-172`), `Resident-update commitment` (`panels.js:245`), and `Service requests and complaints` (`panels.js:255-270`) similarly omit explicit `State:` / cue prefixes.
  * **Core projections & safety boundaries (`C10`, `C11`, `C12`)**:
    * `projection.py:34-66` enforces default-deny `STAFF_ROLES` access to `resident_choice_queue`, hides vulnerability adjustment free text behind `DEFAULT_REASON_ROLES` (`NOTE_HELD`), and denies `Contractor` and `Application Administrator`.
    * `store.py:548-561` builds read-only `resident_choice_queue` items sorted deterministically by case ID without mutating state or sending messages.
    * `taskqueues.py:16-48` defines read-only queue metadata and `accountable_owner` / `safe_category` helpers without exposing safeguarding labels to unauthorized roles.

### Wave 3 — Contrarian (Counter-Evidence & Guardrail Challenges)

* Tested every proposed improvement against static/behavioral repository guards to prevent regressions:
  * **Challenge 1 — Can `[tabindex="-1"]:focus` in `style.css` (`RV-001` from `#1763`) be narrowed to headings only?**
    * *Counter-evidence (`C7`, `C14`)*: **NO.** `test_technical_quality_screens_wcag.py:306`, `test_data_steward_screen_wcag.py:741-742`, and `test_housing_resident_screen_wcag.py:676` all assert the exact standalone `[tabindex="-1"]:focus` CSS rule, and `main#app[tabindex="-1"]` relies on programmatic focus visibility during keyboard navigation. Keep `style.css` focus selectors intact.
  * **Challenge 2 — Will wrapping `Resident decisions by measure` in `panels.js` or upgrading `<td>` to `<th scope="row">` trip `test_accessibility_baseline.py`?**
    * *Counter-evidence (`C14`)*: `test_accessibility_baseline.py:106-119` asserts `len(tables) == 14` for exact literal `h("table", {}, ...)` across `web/*.js` and forbids bare `h("th", {}`. Wrapping the existing `h("table", {}, ...)` inside `h("div", { class: "table-scroll", role: "region", "aria-label": "Resident decisions by measure", tabindex: 0 }, h("table", {}, ...))` keeps `h("table", {}, ...)` at exactly `14`, and `h("th", { scope: "row" }, ...)` carries explicit `scope: "row"` (zero bare `h("th", {}`).
  * **Challenge 3 — Will adding textual state cues in `panels.js` break `test_content_standard.py` or `test_resident_api.py`?**
    * *Counter-evidence (`C16`)*: `test_content_standard.py:14-49` bans `gate(s)`, `hold(s)`, `provenance`, `trace(s)`, `snapshot(s)`, and `envelope(s)` in `panels.js` string literals! Therefore, when mapping contractor `m.flag` (`"Proceed"` vs `"Hold"`) in `panels.js:171`, we MUST compare `m.flag === "Proceed"` and never write the literal word `"hold"` in `panels.js`! Furthermore, `test_resident_api.py:875-895` waits for substrings `"Response: Closed."`, `"Remedy: Open."`, `"Remedy: Resolved."`, and `"Response: Open."` (`exact=False`), so `residentPanel` must preserve `Response: ${r.status}.` and `Remedy: ${remedyStatus}.` verbatim while appending/prepending non-colour state cues (e.g. `Response: ${r.status} (${panelServiceCue(r.status)}).`).
  * **Challenge 4 — Will updating `workspaceStatus.textContent` during loading/error states break `specialist_keyboard_browser_check.py` or `test_housing_resident_screen_wcag.py`?**
    * *Counter-evidence (`C13`)*: `specialist_keyboard_browser_check.py:249-252` uses `wait_for_function` until `#workspace-status` equals `expected_status(role, title, case_id)` once settled (`f"{role}. {title}. {state}"`). Keeping line 180's settled string byte-identical preserves 100% compatibility while adding real `aria-live` loading/error/chooser announcements beforehand.
  * **Challenge 5 — Does `src/api/pyproject.toml` need mypy overrides for `tests/test_housing_resident_wcag_232.py`?**
    * *Counter-evidence (`C17`)*: `src/api/pyproject.toml` sets `strict = true` globally and overrides `ignore_missing_imports = true` for `zava_forward.core.*`. Writing `test_housing_resident_wcag_232.py` with full strict PEP 484 annotations passes `python3 -m mypy tests/test_housing_resident_wcag_232.py` cleanly without loosening `pyproject.toml`.

## Evidence Log

### Codebase Evidence (`C#`)

| ID  | Path and lines                                                        | Verified fact                                                                                                                                      |
|-----|-----------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| C1  | `src/api/src/zava_forward/api/web/app.js:370-376,437-452`             | `isRoleScreensDestination` wires `#/screens`, `#/role/building_safety_lead`, `#/role/repairs`, `#/role/housing_officer`, `#/role/resident_engagement`, omitting `#/role/contact_centre`. |
| C2  | `src/api/src/zava_forward/api/web/role-screens.js:91-98`              | `ROLE_HASH_SCREENS` maps `#/role/housing_officer` -> `resident-service-issues` and `#/role/resident_engagement` -> `resident-choice` using `Object.hasOwn`; `residentJumpNav` renders `<nav role="navigation" aria-label class="screen-links">`. |
| C3  | `src/api/src/zava_forward/api/web/index.html:12-22`                   | App shell provides `<a class="skip-link" href="#app">Skip to main content</a>`, `#workspace-status` (`role="status" aria-live="polite" aria-atomic="true"`), and `<main id="app" tabindex="-1">`. |
| C4  | `src/api/src/zava_forward/api/web/role-screens.js:34,99-186`          | `roleScreensView` sets `workspaceStatus.textContent` only at settled render (line 180), omitting `workspaceStatus` updates on invalid page, unavailable screen, chooser, loading, and record-ID mismatch; inline `role="status"` nodes at lines 34, 129, and 145 omit explicit `aria-live="polite"`. |
| C5  | `src/api/src/zava_forward/api/web/app.js:114-124`                     | `show()` moves programmatic focus to `main#app` when prior focused element disconnects or route context changes, while preserving focus inside open `.chat-widget`. |
| C6  | `src/api/src/zava_forward/api/web/role-screens.js:304-311`            | Delegated `a[data-jump]` click listener calls `preventDefault()`, `.focus()`, and `.scrollIntoView({ block: "start" })` on target `<h2 tabindex="-1">`. |
| C7  | `src/api/src/zava_forward/api/web/style.css:370-379,450-480`          | Defines `:focus-visible`, `[tabindex="-1"] { scroll-margin-top: var(--sp-4); }`, `[tabindex="-1"]:focus`, `.screen-record h2[tabindex="-1"]:focus-visible`, `.screen-links a` (`min-height: 2.5rem; text-decoration: underline`), `.flag` borders, `prefers-reduced-motion`, and `forced-colors`. |
| C8  | `src/api/src/zava_forward/api/web/panels.js:43-64`                    | `actForm` builds field IDs with unslugified `f-${title}-${name}` (containing spaces) and `<button>` without `type="button"`.                       |
| C9  | `src/api/src/zava_forward/api/web/panels.js:169-290`                  | `residentPanel` renders `Resident decisions by measure` without `.table-scroll[role="region"][tabindex="0"]` or `<th scope="row">`, and omits plain-language non-colour state cues on measure answers, contractor readiness flags, update commitments, and service/remedy statuses. |
| C10 | `src/core/src/zava_forward/core/projection.py:34-66`                  | Default-deny server projection grants `resident_choice_queue` to `STAFF_ROLES` only, denies `Contractor` and `Application Administrator`, and gates adjustment reasons via `DEFAULT_REASON_ROLES`. |
| C11 | `src/core/src/zava_forward/core/store.py:548-561`                     | `Store.resident_choice_queue` projects read-only case summaries with `measure_decisions` and `resident_update` in deterministic ID order.          |
| C12 | `src/core/src/zava_forward/core/taskqueues.py:16-140`                 | Defines read-only queue definitions, `accountable_owner`, and `safe_category` safeguarding redaction.                                              |
| C13 | `src/api/checks/specialist_keyboard_browser_check.py:38-75,248-305`   | Browser keyboard check pins `#workspace-status` settled format `"{role}. {title}. {Selected home X.|No home selected.}"` and `EXPECTED_REGIONS["resident-choice"] == ("Measure choices by version",)`. |
| C14 | `src/api/tests/test_accessibility_baseline.py:88-140`                 | Static baseline pins `aria-invalid` count `== 9`, `h("table", {}, ...)` count `== 14`, zero bare `h("th", {}`, `position:fixed` count `== 2`, and Fluent 2 contrast ratios. |
| C15 | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:822`       | Explicitly pairs *"Neighbourhood officer and contact-centre officer"* on the housing and resident engagement workbench with strict no-contact/no-consent boundaries. |
| C16 | `src/api/tests/test_content_standard.py:14-56` & `test_resident_api.py:870-898` | Lexical copy guard bans `gate/hold/provenance/trace/snapshot/envelope` in `web/*.js`; Playwright resident test checks `"Response: Closed."`, `"Remedy: Open."`, `"Remedy: Resolved."`, and `"Response: Open."` substrings. |
| C17 | `src/api/pyproject.toml:25-65`                                        | Configures `mypy` `strict = true` with `zava_forward.core.*` import override already present, plus `ruff` `line-length = 100`.                     |

### External Evidence (`W#`)

| ID | Source URL                                                                                  | Retrieval date | Key applicable rules                                                                                                                  |
|----|---------------------------------------------------------------------------------------------|----------------|---------------------------------------------------------------------------------------------------------------------------------------|
| W1 | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`    | 2026-11-15     | Semantic landmarks/headings, `<label for>` form bindings, keyboard operability, visible focus rings with `scroll-margin-top`, `aria-live="polite"` status updates, non-colour state text, and tabular/overflow resilience. |

## Findings by Question

* **Q1 (Surfaces & Routes)**: Neighbourhood housing officer, contact-centre, and resident engagement staff use (a) specialist read-only screens `resident-service-issues` (`#/role/housing_officer`, missing `#/role/contact_centre`) and `resident-choice` (`#/role/resident_engagement`, backed by `/api/resident/choice-queue` / `store.resident_choice_queue`), and (b) the case workspace `residentPanel` (`panels.js:169-290` on `#/case/<id>?tab=resident`) (`C1`, `C2`, `C9`, `C11`, `C15`).
* **Q2 (Comparison with `#228` & `#231`)**: Peer `#228` (`test_procurement_screen_wcag.py`) and `#231` (`test_technical_quality_screens_wcag.py`) pair explicit plain-language state prefixes (`Confirmed` / `Waiting` / `Action needed` / `Unknown` via `Object.hasOwn`), `<th scope="row">` + `<th scope="col">` + `<caption>` inside `.table-scroll[role="region"][tabindex="0"]`, `<nav>` jump links targeting `<h2 tabindex="-1">`, and `sys.modules`-clean Node VM + static verification (`C2`, `C6`, `C7`). While `#1763` (`321a22960`) and `#1764` (`fe6398197`) brought `resident-choice` and `resident-service-issues` in `role-screens.js` up to par on jump links and `screenRecordTable`, three gaps remain: `#/role/contact_centre` route wiring, `roleScreensView` non-settled `aria-live` announcements, and `residentPanel` (`panels.js`) table/ID/state-cue parity (`C1`, `C4`, `C8`, `C9`).
* **Q3 (`aria-live` & Programmatic Focus)**: `index.html` mounts `#workspace-status` (`role="status" aria-live="polite" aria-atomic="true"`) and `app.js:show()` focuses `main#app[tabindex="-1"]` on route/selection changes (`C3`, `C5`). Adding `workspaceStatus.textContent` updates for loading, chooser, invalid-page, unavailable-screen, and record-mismatch transitions in `roleScreensView()` plus explicit `"aria-live": "polite"` on inline `role="status"` elements (`role-screens.js:34,129,145`) closes all `aria-live` gaps while preserving the settled status format (`C4`, `C13`).
* **Q4 (Textual State Meaning, Landmarks, Tables, Controls & Boundaries)**: `role-screens.js` has complete textual state cues (`choiceCues`, `readinessCue`, `safeRouteCue`, `formalRouteCue`, `updateCues`, `serviceCues`, `data-state-cue` on `.flag` badges) and zero write controls, contact triggers, or role simulators (`C2`, `C4`). In `panels.js`, `actForm` needs whitespace-free slugified control IDs and `type="button"`, and `residentPanel` needs `.table-scroll[role="region"][aria-label][tabindex="0"]`, `<th scope="row">`, and plain-language state cues (avoiding banned jargon literals and preserving `Response: ...` / `Remedy: ...` substrings) (`C8`, `C9`, `C14`, `C16`).
* **Q5 (Static & Behavioral Guards)**: All edits must preserve `h("table", {}, ...)` count `== 14`, `aria-invalid` count `== 9`, zero bare `h("th", {}`, `design-system.md` documented class names in `role-screens.js`, `[tabindex="-1"]:focus` in `style.css`, settled `#workspace-status` wording, and zero banned jargon words under `test_content_standard.py` (`C7`, `C13`, `C14`, `C16`).
* **Q6 (Verification Design)**: `src/api/tests/test_housing_resident_wcag_232.py` should combine Node VM behavioral execution of `app.js`, `role-screens.js`, and `panels.js`, Python unit checks of `projection.py` / `store.resident_choice_queue` / `taskqueues.py`, CSS/HTML static WCAG 2.2 AA baseline checks, and an AST `sys.modules`-hygiene check with full `mypy --strict` typing (`C10`–`C17`).

## Alternatives Considered and Convergence Recommendation

| Option | Summary                                                                                                                                         | Pros                                                                                   | Cons / Rejection or selection rationale                                                                                     |
|--------|-------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| A      | Test-only: add `src/api/tests/test_housing_resident_wcag_232.py` against current `HEAD` without touching `app.js`, `role-screens.js`, or `panels.js`. | Minimal diff.                                                                          | **Rejected**: Leaves `#/role/contact_centre` unwired, leaves `roleScreensView` loading/error transitions unannounced on `#workspace-status`, and leaves space-containing HTML IDs and un-wrapped/un-cued measure table in `panels.js`. |
| B      | **Selected**: Targeted WCAG 2.2 AA completion across `app.js` (`#/role/contact_centre`), `role-screens.js` (`#/role/contact_centre`, `aria-live="polite"` + `#workspace-status` lifecycle announcements, single-lookup jump focus), and `panels.js` (slugified `actForm` IDs + `type="button"`, `.table-scroll` region + `<th scope="row">` + plain-language state cues in `residentPanel`), paired with `src/api/tests/test_housing_resident_wcag_232.py`. | Closes every genuine WCAG 2.2 AA gap across all three staff roles while preserving every static/browser/copy invariant. | **Selected**: Complete, surgical, zero-regression engineering solution backed by `C1`–`C17` and `W1`.                       |
| C      | Redesign `role-screens.js` and `panels.js` layout/CSS (`style.css` selector rewrite for `RV-001` or custom badge components).                    | Addresses optional visual polish `RV-001`.                                             | **Rejected**: Breaks pinned `[tabindex="-1"]:focus` assertions in `test_technical_quality_screens_wcag.py` and `test_data_steward_screen_wcag.py` (`C7`) and risks undocumented CSS class failures in `test_role_screens.py`. |

## Risks, Constraints, and Current Decisions

* **Confirmed decisions**:
  * Wire `#/role/contact_centre` -> `"resident-service-issues"` in `app.js` and `role-screens.js`.
  * Keep settled `#workspace-status` text in `roleScreensView()` identical (`"${role}. ${screen.title}. ${c ? 'Selected home ' + c.id + '.' : 'No home selected.'}"`) while announcing loading, chooser, invalid-page, unavailable-screen, and record-mismatch transitions and adding explicit `aria-live="polite"` on inline `role="status"` elements.
  * Upgrade `actForm` and `residentPanel` in `panels.js` without changing the `h("table", {}, ...)` count (`14`), without introducing banned jargon (`hold`, `gate`, `provenance`, `trace`, `snapshot`, `envelope`), and while preserving `"Response: <status>."` / `"Remedy: <status>."` substrings.
  * Keep `style.css` `[tabindex="-1"]:focus` and `.screen-record h2[tabindex="-1"]:focus-visible` rules untouched.
  * Use `Refs #232` (never `Closes #232`) because human assistive-technology and 360px real-device validation (#151, #155) remain open.
* **Open blockers**: None.

## Further Research and Follow-Up Candidates

1. Human assistive-technology (NVDA, JAWS, VoiceOver) and 360px real-device walkthrough for `#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`, and `#/case/<id>?tab=resident` prior to closing Issue #232 (#151, #155).
2. Coordinated cross-test update if `style.css` `[tabindex="-1"]:focus` is ever narrowed (`RV-001`) across `#229`, `#231`, and `#232` WCAG suites simultaneously.

## Research Disposition and Planning Readiness

* Research execution status: Complete (1 full Wider -> Deeper -> Contrarian cycle executed; no second cycle required under `balanced` posture because all Q1–Q6 claims are verified against `HEAD` with zero unresolved contradictions).
* Research disposition: `executed`
* Output mode supports planning: Yes (`convergence`)
* Planning Readiness: `Ready`

## Artifact Self-Check

* [x] Research Brief, Parameters, Extension Registry, Participation, Scope, Direction Controls, Questions, and Prior Knowledge Gate recorded.
* [x] Cycle 1 completed Wider, Deeper, and Contrarian waves in order.
* [x] Every codebase claim cites a `C#` `path:line` and external guidance cites `W1` with URL and retrieval date.
* [x] Alternatives A, B, and C recorded with evidence-based selection of Option B.
* [x] Zero production/test source files modified during Research (`git status --short` has only `.copilot-tracking/`).
* [x] Research disposition (`executed`) and Planning Readiness (`Ready`) explicitly recorded.

