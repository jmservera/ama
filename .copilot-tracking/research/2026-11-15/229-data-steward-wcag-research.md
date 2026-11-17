<!-- markdownlint-disable-file -->

# Task Research: 229-data-steward-wcag

| Field              | Value                                                                    |
|--------------------|--------------------------------------------------------------------------|
| Date               | 2026-11-15                                                               |
| Researcher / agent | RPI Agent (`rpi-research`)                                               |
| Status             | Complete                                                                 |
| Artifact path      | .copilot-tracking/research/2026-11-15/229-data-steward-wcag-research.md  |

## Research Brief

* What to research: How the data steward, performance analyst, and digital operator screens are implemented in `src/api/src/zava_forward/api/web/`, what WCAG 2.2 keyboard jump navigation, `tabindex="-1"` section target, and explicit non-colour textual state meaning patterns were established in `#225`, `#226`, and `#227`, and what static/unit/browser checks guard those screens.
* Why it matters: Issue `#229` has four checked functional/design-system criteria and one remaining engineering accessibility slice ("Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation"). Changes to `role-screens.js` or companion operator web modules interact with hash routing, table/caption/aria-invalid static inventories, `connected_home_browser_check.py`, and `specialist_keyboard_browser_check.py`.
* Audience or intended use: Planning (`rpi-plan`), implementation (`rpi-implement`), and post-implementation review (`rpi-review`) in this automatic RPI loop.
* Scope: `src/api/src/zava_forward/api/web/` (`role-screens.js` and any data-steward/operator screen modules), `src/api/tests/` (`test_*data_steward*.py`, `test_*data_operator*.py`, `test_exception_register_screen.py`, `test_accessibility_baseline.py`, peer WCAG tests for `#225`/`#226`/`#227`), `src/api/checks/` (`specialist_keyboard_browser_check.py`, `connected_home_browser_check.py`, `data_operator_browser_check.py`), and `docs/reference/research/ux/` if directly coupled.
* Non-goals: Ticking the `#229` acceptance criterion that still requires named human assistive-technology testing (`#155`, `#151`), changing backend conflict/eligibility replay semantics, adding unapproved dependencies, or pushing to remote.
* Criteria: Every codebase claim carries a `C#` ID with `path:line`; external guidelines carry `W#` with URL and retrieval date; contrarian wave tests invariants (`aria-invalid` count, table count, `screenPanel("Title"` regexes, hash-router collisions, lexical copy audit).
* Requested outputs: Converged implementation recommendation with exact file/function targets, invariants to preserve, and focused test strategy.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                                     |
|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1-Q5: Which web surfaces implement `#229`, what is already delivered vs missing, how `#225`/`#226`/`#227` implement jump nav and textual state labels without router collisions, and which cross-cutting static/manifest checks constrain edits? |
| Codebase scope                       | `src/api/src/zava_forward/api/web/`, `src/api/tests/`, `src/api/checks/`, `docs/reference/research/ux/`                                                   |
| External scope                       | Vercel Web Interface Guidelines (`raw.githubusercontent.com/vercel-labs/web-interface-guidelines`)                                                        |
| Initial internal candidate areas     | `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_data_steward_screen_wcag.py`, `src/api/tests/test_data_operator_screen.py`, `src/api/tests/test_accessibility_baseline.py` |
| Initial external candidate areas     | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`                                                                  |
| Research posture                     | focused                                                                                                                                                   |
| Posture provenance                   | default (bounded internal task with named source targets and explicit peer examples)                                                                       |
| Explicit limits / deadline           | Single non-interactive RPI session; leave clean local commit on `feat/ux-229-data-steward-wcag`, do not push                                              |
| Posture-specific completion basis    | focused scope and materiality                                                                                                                             |
| Edits allowed during research?       | no, research-only                                                                                                                                         |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                                                      |
| Known constraints / excluded sources | Preserve Fluent 2 tokens, WCAG baseline invariants (`aria-invalid` count, table caption/scope checks, lexical banned-word guard), and read-only boundaries |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                       | Match and provenance                                      | Scoped authority or output contract                                   | Selected / skipped reason                                                       |
|---------------------|---------------------------------|-----------------------------------------------------------|-----------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA Repository Instructions) | `applyTo: "**"` matches all repository paths              | Enforces UX/WCAG baseline, Fluent 2, plain-language copy, validation tiers, and `Refs #229` | Selected: governs all repository changes and evidence boundaries                |
| Skill               | `rpi-research`                  | Active RPI phase skill                                    | Three-wave research protocol and primary artifact contract            | Selected: active phase protocol                                                 |
| Skill               | `accessibility`                 | Semantic match on WCAG 2.2 keyboard and state meaning     | WCAG 2.2 / ARIA APG criteria mapping                                  | Selected: loaded at intake for WCAG 2.2 criteria verification                   |
| Skill               | `web-design-guidelines`         | Mandatory per Web Development Guidance before web edits   | Fetched rules and `file:line` audit format                            | Selected: loaded and fetched at intake                                          |
| Skill               | `redesign-existing-projects`    | Mandatory per Web Development Guidance for existing app UI| Audit existing UI without breaking stack or Fluent 2 design system    | Selected: loaded at intake, subordinate to Fluent 2 and WCAG baseline           |
| Research specialist | `hve-core-all:rpi-researcher`   | Registered subagent for independent lanes                 | Delegated subagent lane artifact                                      | Skipped (inline): tightly coupled single-module inspection in `src/api` (<10 reads) |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                        | Answers / unanswered | Resulting decision or selected further research                                 |
|------------------|----------------------------------------------------------------------------------------------|----------------------|---------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI session with explicit scope, peer references (`#225`, `#226`, `#227`), and validation commands | N/A (non-interactive)| Proceed in focused convergence mode                                             |
| Direction change | No scope boundary crossed during Cycle 1                                                     | N/A                  | Retain focused posture within `src/api/`                                        |
| Convergence      | Cycle 1 evidence saturated all five research questions with high confidence                  | N/A                  | Converge on `screenJumpNav` + `operatorPanel` (`tabindex="-1"`) + fail-closed `State:` / `Source state:` helpers |

## Scope and Success Criteria

* Scope: Data steward and digital operator screen UI surfaces, keyboard jump navigation, `tabindex="-1"` section targets, explicit textual state meaning on conflict/return/provenance/exception badges and indicators, and focused unit/accessibility tests in `src/api/tests/`.
* Assumptions:
  * Prompt mentions `data_steward.js`, `asset_executive.js`, `safety_repairs.js`, `finance_grants.js` parenthetically ("or the data steward / digital operator screen modules under `src/api/src/zava_forward/api/web/`"): verify actual filenames and screen registrations in `src/api/src/zava_forward/api/web/`.
  * Check whether `test_data_steward_screen_wcag.py` already exists and what it currently tests.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Inspect data steward / digital operator screen modules and existing tests; add full WCAG 2.2 keyboard jump navigation (`nav aria-label` jump links, `tabindex="-1"` section targets, explicit textual state meaning on conflict/return/provenance/exception badges and indicators, keyboard-accessible controls) matching `#225`, `#226`, `#227`; add focused unit/accessibility tests; run focused validation (`test_*data_steward*.py`, `mypy`, `ruff`); commit locally with `Refs #229`.
* Inferred research questions: Identify all registered screen IDs for `#229`, inspect existing `#229` prior work (including `.copilot-tracking/reviews/2026-11-14/issue-229-c3-correction.md` and `test_data_steward_screen_wcag.py`), compare exact DOM/event patterns across `#225`/`#226`/`#227`, and check cross-screen invariant tests.
* Caller constraints and non-goals: Research-only during Research phase; do not push; do not claim human screen-reader conformance (`Refs #229`).

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                 | Source / checkpoint | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|---------------------------------------------------------------------------------------|---------------------|---------------------------------------------------|
| narrow                                                   | Match established `#225`/`#226`/`#227` WCAG 2.2 jump-nav and state-meaning patterns   | Caller intake       | Constrains solution alternatives to repo patterns |
| exclude                                                  | Do not push branch; leave clean frozen local commit with `Refs #229`                  | Caller intake       | Constrains closeout git workflow                  |

## Research Questions

|  # | Sub-question                                                                                                    | Type (depth / breadth / straightforward) | Priority | Status   |
|---:|-----------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|----------|
| Q1 | Which files and registered screen IDs implement the data steward, performance analyst, and digital operator screens for `#229`, and what is already implemented? | straightforward                          | H        | answered |
| Q2 | How do `#225` (finance), `#226` (asset-board), and `#227` (safety) implement `nav aria-label` jump navigation, `tabindex="-1"` section targets, and focus movement without hash-router side effects? | depth                                    | H        | answered |
| Q3 | Which conflict, return, provenance, exception, AI-state, or recovery badges/cells/indicators on the `#229` screen(s) lack explicit non-colour textual state meaning or keyboard accessibility? | depth                                    | H        | answered |
| Q4 | What do `test_data_steward_screen_wcag.py`, `test_data_operator_screen.py`, `test_exception_register_screen.py`, and `test_accessibility_baseline.py` currently verify, and what gaps remain? | depth                                    | H        | answered |
| Q5 | Which cross-cutting tests and checks (`test_connected_home_check.py`, `test_specialist_keyboard_check.py`, `test_content_standard.py`, `test_ux_design_traceability.py`, `test_screen_design_traceability.py`) inspect `role-screens.js` or `#229` screens? | breadth                                  | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/design-system.md`, `docs/reference/research/ux/content-standard.md`, `.copilot-tracking/research/2026-11-14/asset-exec-screen-wcag-research.md`
* Reused (verified) findings: `design-system.md` maps `Data operator and auditor` (`docs/reference/research/ux/customer-journeys/data.md`) to `screen:data-operator` and `test_data_operator_screen.py` (C15); `asset-exec-screen-wcag-research.md` correctly noted that hash links trigger the SPA router unless intercepted via delegated `a[data-jump]` (`event.preventDefault()`, C2).
* Superseded / stale: Caller prompt mentions `data_steward.js` / `asset_executive.js` / `safety_repairs.js` / `finance_grants.js` parenthetically, whereas all registered role screens live in `src/api/src/zava_forward/api/web/role-screens.js` (C1, C2, C3, C4).

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow (match `#225`/`#226`/`#227` WCAG 2.2 jump-nav and state-meaning patterns); exclude (do not push branch; use `Refs #229`)
* Active research posture and completion basis: focused; focused scope and materiality
* Explicit limits or deadline effect: Single non-interactive RPI session; research stayed strictly read-only across `src/api/` and `docs/reference/research/ux/`

#### Wave 1: Wider

* Plan and independent lanes: Enumerate all files in `src/api/src/zava_forward/api/web/`, locate all registered screen IDs for `#229`, `#225`, `#226`, and `#227`, locate all existing unit and browser checks referencing `data-operator` or `exceptionRegister`, and fetch the current Web Interface Guidelines.
* Worker evidence relationships or inline fallback: inline (tightly coupled single-file architecture in `role-screens.js`; Q1 -> C1, C5, C6; external guidelines -> W1).
* Reflection: All specialist role screens live in `src/api/src/zava_forward/api/web/role-screens.js`. Issue `#229` is served by `registerRoleScreen({ id: "data-operator", title: "Data steward and operator view", ... })`, which exposes three views: `exceptionRegisterView` (`?exceptions=1`), `summary(entries)` (page-level conflict and return queue when no home is selected), and `render(c)` (selected-home steward and operator view). Prior PR `#1693` added `exceptionJumpNav()` and `indicatorRows` ("State at a glance") to `exceptionRegisterPanel` only, leaving `render(c)` and `summary(entries)` without section jump navigation, `tabindex="-1"` section targets, or explicit `State:` / `Source state:` labels.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Q2 (`#225`/`#226`/`#227` jump-nav and state-cue implementations), Q3 (exact bare state strings in `data-operator` `render(c)`, `summary(entries)`, and `exceptionRegisterPanel`), and Q4 (exact assertions in `test_data_steward_screen_wcag.py`, `test_data_operator_screen.py`, `test_exception_register_screen.py`, and `test_data_operator_ai_state.py`).
* Plan and independent lanes: Read `role-screens.js` shared helpers (`screenPanel`, `screenJumpTarget`, `screenJumpNav`, `a[data-jump]` delegated listener), `#226` (`assetPanel`/`assetJump`), `#227` (`hazardPanel`/`hazardJump`), `#225` (`screenJumpNav`/`screenJumpTarget`/`fundingStateRows`), and `#229` (`operatorSide`, `operatorStatus`, `exceptionRegisterPanel`, `summary`, `render`). Inspect all `#229` and peer WCAG test suites.
* Worker evidence relationships or inline fallback: inline (Q2 -> C2, C3, C4; Q3 -> C5, C6, C7; Q4 -> C8, C9, C10, C11).
* Reflection: `role-screens.js:29-32` already provides `screenJumpNav(label, jumps)` rendering `<nav class="row" aria-label="..."><a href="#id" class="btn alt" data-jump="id" data-jump-target="id">Go to ...</a></nav>`, and `role-screens.js:268-275` already binds the shared document-level `click` listener for `a[data-jump]` that calls `event.preventDefault()` and focuses `document.getElementById(id)`. Meanwhile `#226` (`assetPanel`, `role-screens.js:318`) places `id` and `tabindex="-1"` directly on `<section class="card screen-record" id="..." tabindex="-1"><h2>...</h2>...</section>`. Combining `screenJumpNav` with an `operatorPanel(id, title, ...children)` helper puts `tabindex="-1"` directly on target `<section>` elements without adding `<button>` or inline `onclick` attributes.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge candidate edits against every cross-screen static, structural, lexical, global-scope, and browser-harness invariant in `src/api/tests/` and `src/api/checks/` (Q5).
* Plan and independent lanes: Inspect `test_data_operator_screen.py`, `test_exception_register_screen.py`, `data_operator_browser_check.py`, `data_operator_ai_state.py`, `role_screens_fixtures.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_role_screens_conformance.py`, `specialist_keyboard_browser_check.py`, `test_connected_home_check.py`, `test_asset_exec_screen_wcag.py`, and `test_safety_screen_wcag_keyboard.py`.
* Worker evidence relationships or inline fallback: inline (Q5 -> C9, C10, C11, C12, C13, C14, C15, C16).
* Reflection: Contrarian testing uncovered eight hard constraints that defeat naive implementations:
  1. `test_data_operator_screen.py:148-150` and `171-174` forbid `<button>`, `<form>`, `<input>`, `<select>`, `<textarea>`, and any `onclick` attribute anywhere in `data-operator.render(c)` (C9). Jump links in `render(c)` must therefore be `<a data-jump="...">` elements using the existing delegated click listener, never `<button onclick=...>`.
  2. `test_data_operator_screen.py:163-166` requires every `<section>` in `render(c)` to have exact `class="card screen-record"` and `kids[0].tag == "h2"` (C9). `operatorPanel(id, title, ...children)` (`h("section", { class: "card screen-record", id, tabindex: "-1" }, h("h2", {}, title), ...children)`) satisfies this and places `tabindex="-1"` directly on target `<section>` elements.
  3. `test_data_operator_screen.py:157-158` forbids `"a"` and `"button"` inside `s.summary(entries)` directly, and `test_exception_register_screen.py:228-229` pins `len(links) == 1` when `overview(signal, [], null)` renders `entry` with `rows = []` (C9, C10). Therefore `summary(entries)` itself must contain no `<a>`/`<button>`, while `overview(signal, rows, c)` can render an overview `screenJumpNav` only when `exceptions !== "1" && summary` (i.e. both panels are present).
  4. `test_data_operator_screen.py:185-189` slices `role-screens.js` between `async function exceptionRegisterView` and `registerRoleScreen` and forbids `"method"`, `"onclick"`, `"POST"`, `"innerHTML"`, and `"fetch("` in that slice (C9). Any new `operator*` helpers must be placed near `operatorSide`/`operatorStatus` (`role-screens.js:1073-1074`) rather than inside that slice.
  5. `test_content_standard.py:15` bans `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b` across `role-screens.js`, and `data_operator_ai_state.py:55` bans `"No outage recorded"`, `"audit trail"`, and `"audit history"` in the register panel (C11, C13). UI text must say `"source details"` / `"Source state:"` rather than `"provenance"`.
  6. `role_screens_fixtures.py:66-69` uses `validation_state="Unverified"` while `test_data_operator_screen.py:16` uses `validation_state="Unvalidated"`, and `data_operator_browser_check.py:23-49` pins exact substrings (`"D; source SYN-STOCK-A v1"`, `"Unresolved"`, `"Withdrawn"`, `"Returned"`, `"Preserved unchanged in the table above"`, `"Not selected. No latest-wins or silent correction is applied."`, `"No interface run record is supplied to this screen."`) (C9, C11). Appending `(Source state: ...)` in `operatorSide` and prefixing `State: ...` on status/eligibility/return/handoff/recovery values preserves every existing substring while failing closed to `Unknown` on missing, colour-only, or prototype-key inputs.
  7. `specialist_keyboard_browser_check.py:50` pins `EXPECTED_REGIONS["data-operator"] = ("Open exceptions and prerequisites",)` on the workbench fixture (where `queries`, `returns`, and `events` are empty) (C14). Adding a `"State"` column to the existing `"Open exceptions and prerequisites"` table (rather than adding a new unconditional `screenTable`) keeps region labels identical.
  8. `test_accessibility_baseline.py:51,100` pins exact `aria-invalid` count (`8`) and literal `h("table", {},` count (`13`), `test_asset_exec_screen_wcag.py:61-62` pins the exact formatting of the delegated `a[data-jump]` click listener at `role-screens.js:268-275`, and `RoleScreensGlobalScope` in `test_safety_screen_wcag_keyboard.py:163-175` forbids top-level identifier collisions with `app.js` (C3, C4, C12).

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment  |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|-----------------------------|
| Use `screenJumpNav` + `operatorPanel` (`<section class="card screen-record" id="..." tabindex="-1">`) in `data-operator.render(c)` and multi-panel non-exception `overview` | C2, C3, C5, C6, C9, C10, W1 | accepted | Satisfies WCAG 2.2 SC 2.1.1 / 2.4.1 keyboard bypass and programmatic focus without `<button>` or inline `onclick`, preservingSPA hash routes via `a[data-jump]` | Selected recommendation |
| Keep `exceptionJumpNav()` (`button[data-jump-target]`) on `exceptionRegisterPanel` (`?exceptions=1`) | C5, C8, C10, C11 | accepted | Already tested by `test_data_steward_screen_wcag.py` and `data_operator_browser_check.py`; changing buttons to anchors there would break existing tests without accessibility benefit | Selected recommendation |
| Add fail-closed `State:` and `Source state:` helpers across conflict status, source validation (`Unvalidated`/`Unverified`/`Validated`/`Verified`/`Quarantined`/`Stale`), eligibility, returns/reopens, handoff state, open prerequisites, event dispositions, recovery context, and register state | C5, C6, C7, C8, C9, C11, C13, W1 | accepted | Satisfies WCAG 2.2 SC 1.4.1 Use of Color and SC 1.3.1 Info and Relationships while preserving all pinned substrings and failing closed on missing/unrecognised/prototype keys | Selected recommendation |
| Use `<button onclick=...>` jump controls inside `data-operator.render(c)` (like `#227` `hazardJump`) | C4, C9 | rejected | `test_data_operator_screen.py:148-150` and `172` explicitly fail on any `<button>` or `onclick` attribute in `render(c)` | Rejected alternative |
| Add a new unconditional `screenTable` state summary table to `data-operator.render(c)` | C14 | rejected | Changes rendered `role="region"` table count on the empty-case fixture and would break `EXPECTED_REGIONS["data-operator"]` in `specialist_keyboard_browser_check.py:50` | Rejected alternative |
| Tick the `#229` WCAG 2.2 acceptance checkbox or claim full WCAG 2.2 conformance | C15, C16 | deferred | Repository governance requires assistive-technology and human validation (`#151`, `#155`); commit uses `Refs #229` | Unresolved / external human gate |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Scope saturation; all five research questions (`Q1`–`Q5`) are answered from direct source inspection with exact line references and contrarian invariant checks.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: single-module UI and test suite inspection in `src/api/` completed in <15 bounded reads without independent subagent lanes needed.

### Codebase Evidence

| ID  | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
|-----|-----------------|------------------------|------|------------|-------|
| C1  | All 13+ specialist role screens are registered in `role-screens.js`; there is no separate `data_steward.js` file | `src/api/src/zava_forward/api/web/role-screens.js:3` | glob / view | high | `roleScreens` Map |
| C2  | Shared `screenJumpNav(label, jumps)` renders `<nav class="row" aria-label="..."><a href="#id" class="btn alt" data-jump="id" data-jump-target="id">Go to ...</a></nav>`, and document-level click delegation focuses `document.getElementById(id)` after `event.preventDefault()` | `src/api/src/zava_forward/api/web/role-screens.js:29-32` | view | high | Delegated listener at `role-screens.js:268-275`; used by `#225` (`finance-invoices`, `finance-funding`) |
| C3  | `#226` (`asset-board`) defines `assetPanel(id, title, ...children)` as `<section class="card screen-record" id="..." tabindex="-1"><h2>...</h2>...</section>` paired with `<nav aria-label="Asset and board sections"><a data-jump="...">` | `src/api/src/zava_forward/api/web/role-screens.js:318-323` | view | high | Verified by `src/api/tests/test_asset_exec_screen_wcag.py:37-65` |
| C4  | `#227` (`safety-lead`, `hazard-triage`) uses `hazardJump` + `hazardPanel`, and `test_safety_screen_wcag_keyboard.py` guards against top-level identifier collisions between `role-screens.js` and `app.js` | `src/api/src/zava_forward/api/web/role-screens.js:995-1035` | view | high | Global scope collision test at `src/api/tests/test_safety_screen_wcag_keyboard.py:163-175` |
| C5  | Prior `#229` commit (`#1693`) added `indicatorRows` ("State at a glance") and `exceptionJumpNav()` (`<nav aria-label="Data stewardship sections">` with 4 `button[data-jump-target]` targeting `<h3 id="..." tabindex="-1">`) to `exceptionRegisterPanel(data)` (`?exceptions=1`), while `Register state` and item `State` cells in `exceptionRegisterPanel` lack `State:` prefixes | `src/api/src/zava_forward/api/web/role-screens.js:1166-1243` | view | high | Existing `#229` exception-register view |
| C6  | `data-operator` (`overview`, `summary`, `render`) has no jump `<nav>` or `tabindex="-1"` section targets on `render(c)` or the default non-exception `overview`, and renders bare state strings in `operatorSide`, `operatorStatus`, `Eligibility`, `Returns and reopens`, `Handoff state`, `Open exceptions and prerequisites`, `Recorded stock query events`, and `Recovery context` | `src/api/src/zava_forward/api/web/role-screens.js:1073-1074` | view | high | Screen body at `role-screens.js:1259-1337` |
| C7  | Synthetic fixtures pass both `"Unverified"` (`role_screens_fixtures.py`) and `"Unvalidated"` (`test_data_operator_screen.py`) as `validation_state` on `stock_reconciliation` sides | `src/api/checks/role_screens_fixtures.py:66-69` | view | high | Must map both `unverified` and `unvalidated` (plus `validated`, `verified`, `quarantined`, `stale`) and fail closed otherwise |
| C8  | `test_data_steward_screen_wcag.py` matches discovery pattern `"test_*data_steward*.py"` and currently tests `exceptionRegisterView` (`?exceptions=1`) only; it has zero tests for `data-operator.render(c)` or `summary(entries)` | `src/api/tests/test_data_steward_screen_wcag.py:1-209` | view | high | Primary WCAG 2.2 test module for `#229` |
| C9  | `test_data_operator_screen.py` forbids `<button>`/`<form>`/`<input>`/`<select>`/`<textarea>` and `onclick` in `render(c)`, forbids `"a"` inside `s.summary(...)`, requires every `<section>` to have `class="card screen-record"` and `kids[0].tag == "h2"`, and forbids `"method"`/`"onclick"`/`"POST"` between `async function exceptionRegisterView` and `registerRoleScreen` | `src/api/tests/test_data_operator_screen.py:105-190` | view | high | Core structural regression guard for `data-operator` |
| C10 | `test_exception_register_screen.py` asserts `len(links) == 1` when `overview(signal, [], null)` renders `entry` (`rows = []`) and checks `"roles_not_named"` in empty register text | `src/api/tests/test_exception_register_screen.py:179-231` | view | high | Overview jump nav must render only when `exceptions !== "1" && summary` |
| C11 | `data_operator_browser_check.py` and `data_operator_ai_state.py` pin exact substrings (`EXPECTED`, `PAGE_EXPECTED`, `REGISTER_EXPECTED`, `CONFLICT_EXPECTED`) and forbid `"No outage recorded"`, `"audit trail"`, `"audit history"` in the register panel | `src/api/checks/data_operator_browser_check.py:22-96` | view | high | AI-state constants at `src/api/checks/data_operator_ai_state.py:42-64` |
| C12 | `test_accessibility_baseline.py` pins exact counts of `setAttribute("aria-invalid", "true")` (`8`) and literal `h("table", {},` (`13`) across `web/*.js`, plus CSS `:focus-visible`, `prefers-reduced-motion`, and `forced-colors` rules | `src/api/tests/test_accessibility_baseline.py:51-116` | view | high | Calling `screenTable(...)` reuses the single helper and preserves the `13` count |
| C13 | `test_content_standard.py` audits `role-screens.js` and rejects `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b` outside an explicit identifier allowlist; `test_role_screens_conformance.py` rejects inline styles, timers, motion, and non-native handlers | `src/api/tests/test_content_standard.py:15-55` | view | high | Conformance checks at `src/api/tests/test_role_screens_conformance.py:72-104` |
| C14 | `specialist_keyboard_browser_check.py` pins `EXPECTED_REGIONS["data-operator"] = ("Open exceptions and prerequisites",)` on the workbench synthetic fixture | `src/api/checks/specialist_keyboard_browser_check.py:50` | view / grep | high | Tested by `src/api/tests/test_specialist_keyboard_check.py:75-105` |
| C15 | `design-system.md`, `screen-design-traceability.md`, `atlas-screen-trace.md`, and `customer-journeys/data.md` trace `#229` to `data-operator` and state that engineering checks do not establish human WCAG 2.2 acceptance (`#151`, `#155`) | `docs/reference/research/ux/customer-journeys/data.md:103-117` | view | high | Traceability tests at `src/api/tests/test_screen_design_traceability.py:34-89` |
| C16 | `test_epic149_role_workbench_heading_hierarchy.py` requires every rendered role view to have sequential headings (`h1` -> `h2` -> `h3` with no skipped levels), named tables with scoped `th`, and accessible names on all links and buttons | `src/api/tests/test_epic149_role_workbench_heading_hierarchy.py:130-169` | view | high | `operatorPanel` keeps `<h2>` inside each `<section>` |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|
| W1 | Interactive navigation links require native `<a>` semantics, clear accessible names, visible `:focus-visible` outlines, non-colour state indicators, tabular or plain readable values, and `prefers-reduced-motion` support | Vercel Web Interface Guidelines (`command.md`) | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | 2026-11-15 | main (2026-11-15) | high |

### Contradictions / Conflicts

* Caller prompt example filenames vs repository layout: Caller prompt parenthetically mentions `data_steward.js`, `asset_executive.js`, `safety_repairs.js`, and `finance_grants.js` ("or the data steward / digital operator screen modules under `src/api/src/zava_forward/api/web/`"), whereas C1–C6 show all specialist role screens are consolidated in `src/api/src/zava_forward/api/web/role-screens.js` and WCAG tests live in `src/api/tests/test_data_steward_screen_wcag.py`, `test_asset_exec_screen_wcag.py`, `test_safety_screen_wcag_keyboard.py`, and `test_finance_screens_wcag_225.py`; resolved by primary codebase evidence -> edit `role-screens.js` and `test_data_steward_screen_wcag.py`.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
|----------|---------|--------------|------------|-----------------------------------|
| Q1 | `#229` is implemented by `data-operator` ("Data steward and operator view") in `role-screens.js:1073-1337`. `exceptionRegisterPanel` (`?exceptions=1`) already has `exceptionJumpNav()` and `State at a glance`, while `render(c)` and `summary(entries)` lack jump navigation, `tabindex="-1"` section targets, and explicit textual state prefixes. | C1, C5, C6 | high | Target `data-operator` (`render`, `overview`, `summary`, and `exceptionRegisterPanel` table/register state labels) in `role-screens.js`. |
| Q2 | `#225` and `#226` use native `<a href="#id" class="btn alt" data-jump="id">` inside `<nav class="row" aria-label="...">` (`screenJumpNav`) paired with `<section class="card screen-record" id="..." tabindex="-1">` (`assetPanel`) and the shared document-level `a[data-jump]` click handler (`event.preventDefault()` + `focus()`), avoiding SPA hash-route changes and inline `onclick`. | C2, C3, C4, W1 | high | Reuse `screenJumpNav` + `operatorPanel` (`tabindex="-1"` on `<section>`) and existing `a[data-jump]` click delegation without modifying lines `268-275`. |
| Q3 | Bare or colour/position-dependent states remain in: `operatorSide` validation state (`Unvalidated`/`Unverified`/`Validated`), `operatorStatus` conflict state (`Unresolved`/`Withdrawn`), `Eligibility and original source` fields, `Returns and reopens` type (`Returned`/`Reopened`) and unavailable rows, `Handoff state`, `Open exceptions and prerequisites` rows, `Recorded stock query events` state column, `Recovery context` / `Integration run and queue state`, and `exceptionRegisterPanel` `Register state` + item `State` column. | C5, C6, C7, C11, C13 | high | Introduce fail-closed `operatorSourceState`, `operatorEventState`, `operatorReturnState`, `operatorHandoffState`, `operatorBlockerState`, and `exceptionItemState` / `exceptionRegisterState` helpers that emit explicit `State:` / `Source state:` prefixes while preserving all existing substrings and banned-word rules. |
| Q4 | `test_data_steward_screen_wcag.py` covers `exceptionRegisterView` (`?exceptions=1`) only; it does not test `data-operator.render(c)` or `overview`/`summary(entries)` jump links, `<section tabindex="-1">` targets, delegated `a[data-jump]` focus + `preventDefault()`, or fail-closed textual state labels on conflicts, source validation, returns, eligibility, handoff, blockers, and events. | C8, C9, C10, C12 | high | Expand `src/api/tests/test_data_steward_screen_wcag.py` (which matches `"test_*data_steward*.py"`) with comprehensive WCAG 2.2 unit tests covering both views and delegated keyboard/click focus behaviour. |
| Q5 | Edits must preserve: no `<button>`/`onclick` in `render(c)`, no `<a>`/`<button>` inside `summary(entries)`, `len(links) == 1` on `overview` when `rows == []`, no forbidden tokens between `exceptionRegisterView` and `registerRoleScreen`, zero banned copy words (`provenance`, `hold`, `gate`, `trace`, `snapshot`, `envelope`, `audit trail`), `EXPECTED_REGIONS["data-operator"]`, `aria-invalid` count (`8`), `h("table", {},` count (`13`), and no global identifier clashes with `app.js`. | C4, C9, C10, C11, C12, C13, C14, C15, C16 | high | Verified every constraint; design avoids all collisions and requires updating `docs/reference/research/ux/customer-journeys/data.md` + `docs/reference/log.md` only if material KB synthesis changes (keep code + tests surgical unless doc update improves traceability). |

## Key Discoveries

* `role-screens.js:29-32` and `268-275` already provide the shared `screenJumpNav(label, jumps)` helper and delegated `a[data-jump]` click handler introduced for `#225` and `#226`, so `data-operator` can adopt native anchor jump links with zero inline `onclick` handlers and zero SPA hash-router interference (C2, C3, C9).
* `data-operator.render(c)` enforces strict read-only structural tests (`test_data_operator_screen.py:148-174`) that forbid `<button>` and `onclick` attributes while requiring `<section class="card screen-record">` with `<h2>` first child — making `operatorPanel(id, title, ...children)` (`<section class="card screen-record" id="..." tabindex="-1"><h2>...</h2>...</section>`) the exact structural match (C3, C9, C16).
* Synthetic browser fixtures supply `"Unverified"` (`role_screens_fixtures.py:67`) whereas unit tests supply `"Unvalidated"` (`test_data_operator_screen.py:16`), and `data_operator_browser_check.py:22-49` checks exact substrings such as `"D; source SYN-STOCK-A v1"`, `"Preserved unchanged in the table above"`, and `"Not selected. No latest-wins or silent correction is applied."` (C7, C9, C11). Fail-closed `State:` and `Source state:` formatting preserves every pinned phrase while ensuring unrecognised, missing, numeric, colour-only (`"green"`), or prototype-key (`"constructor"`, `"toString"`) inputs render `Unknown` rather than a pass or raw unlabelled token.

### Complete Examples (when applicable)

```javascript
const operatorPanel = (id, title, ...children) =>
  h("section", { class: "card screen-record", id, tabindex: "-1" }, h("h2", {}, title), ...children);
const operatorJumps = [
  ["operator-boundary", "Evidence boundary"],
  ["operator-conflicts", "Conflict queue"],
  ["operator-eligibility", "Eligibility and original source"],
  ["operator-returns", "Returns and reopens"],
  ["operator-handoff", "Handoff and exception queue"],
  ["operator-events", "Event metadata and recovery context"]
];
```

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Add `operatorPanel` (`<section class="card screen-record" id="..." tabindex="-1">`) and `screenJumpNav` jump links (`a[data-jump]`) to `data-operator.render(c)` (all 6 sections) and to multi-panel default `overview` (`operator-register-entry` and `operator-page-queue` when `exceptions !== "1" && summary`), keep `exceptionJumpNav()` intact on `exceptionRegisterPanel`, add fail-closed `State:` and `Source state:` helpers across all conflict, source-validation, eligibility, return/reopen, handoff, open-prerequisite, event, recovery, and exception-register state fields/cells, and add focused WCAG 2.2 unit tests in `src/api/tests/test_data_steward_screen_wcag.py`.
* Rationale: Directly satisfies every requirement in issue `#229` and WCAG 2.2 baseline (`#151`: SC 1.3.1, 1.4.1, 2.1.1, 2.4.1, 2.4.3, 2.4.6, 4.1.2) using the exact repository idioms from `#225` and `#226` while preserving 100% compatibility with all existing unit, conformance, lexical, and browser checks.
* Evidence refs: C2, C3, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C16, W1
* Implementation impact: `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_data_steward_screen_wcag.py`, and `docs/reference/research/ux/customer-journeys/data.md` + `docs/reference/log.md` (recording the `#229` WCAG engineering slice while keeping human AT review explicitly open).
* Confidence: high: direct inspection of all source helpers and regression guards leaves no unverified assumptions.

File tree:

```text
src/api/src/zava_forward/api/web/role-screens.js          (modify)
src/api/tests/test_data_steward_screen_wcag.py            (modify)
docs/reference/research/ux/customer-journeys/data.md      (modify)
docs/reference/log.md                                     (modify)
```

### Alternative: Button-based jump navigation (`<button onclick=...>`) in `data-operator.render(c)`

* Approach: Mirror `#227` (`hazardJump`) or `exceptionJumpNav()` by rendering `<button type="button" onclick=...>` jump controls inside `data-operator.render(c)`.
* Trade-offs: Avoids `href="#..."` altogether, but introduces `<button>` elements and `onclick` properties on VDOM nodes in `render(c)`.
* Evidence refs: C4, C5, C9, C13
* Rejection rationale: Rejected because `test_data_operator_screen.py:148-150` and `172` explicitly forbid both `<button>` tags and `onclick` attributes anywhere in `data-operator.render(c)`, whereas `screenJumpNav` (`<a data-jump="...">`) with the existing delegated click listener already prevents hash-route navigation cleanly.

### Alternative: Wrap existing `screenPanel(...)` calls in `screenJumpTarget(id, panel)` (`<div id="..." tabindex="-1">`)

* Approach: Mirror `#225` (`finance-invoices`/`finance-funding`) by wrapping `<section>` inside `<div id="..." tabindex="-1">`.
* Trade-offs: Works with `screenJumpNav`, but places `tabindex="-1"` on an outer wrapper `<div>` rather than on the `<section>` landmark/card itself.
* Evidence refs: C2, C3, C9
* Rejection rationale: Rejected in favour of `operatorPanel` (`#226` `assetPanel` pattern) because the caller explicitly requested `tabindex="-1"` on target sections (`<section class="card screen-record" id="..." tabindex="-1">`), which avoids extra wrapper DOM nodes while still satisfying `test_data_operator_screen.py:163-166`.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Human assistive-technology verification and screen-reader sign-off under `#151` and `#155` remain required before ticking the `#229` issue checkbox; commit must use `Refs #229`, not `Closes #229` (C15).
* Follow-up: Live Chromium execution of `checks/data_operator_browser_check.py` with pinned `ZF_AXE_JS` remains an optional browser harness check beyond the unit/static tier when Playwright Chromium + axe bundle are provisioned.
* Residual uncertainty: none within engineering scope.

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
|----------|-------------------------------------------------------|-----------------------------------------------|-----------|--------------|--------------|
| Implement keyboard section jump links in `data-operator.render(c)` and two-panel default `overview` using `screenJumpNav` (`a[data-jump]`) and `operatorPanel` (`<section id="..." tabindex="-1">`) | confirmed | user + evidence | Matches `#225`/`#226`, avoids hash-router navigation, and satisfies `test_data_operator_screen.py` no-button/no-onclick rules | C2, C3, C6, C9, C10 | Zero changes needed to shared `a[data-jump]` listener at `role-screens.js:268-275` |
| Preserve `exceptionJumpNav()` and `indicatorRows` in `exceptionRegisterPanel` while adding explicit `State:` labels to `Register state` and item `State` cells | confirmed | evidence + constraint | Keeps all 10 existing `test_data_steward_screen_wcag.py` tests and `data_operator_browser_check.py` green while closing bare state cells in the register table | C5, C8, C10, C11 | Column indices in `Exception items returned for you` remain unchanged |
| Add fail-closed `State:` and `Source state:` helpers across all conflict, source-detail, eligibility, return/reopen, handoff, prerequisite, event, and recovery fields without using banned internal copy terms | confirmed | user + constraint | Satisfies WCAG 2.2 SC 1.4.1 non-colour textual state meaning and `test_content_standard.py` copy rules | C6, C7, C9, C11, C13, W1 | Never emit `"provenance"`, `"hold"`, `"gate"`, `"trace"`, `"snapshot"`, `"envelope"`, or `"audit trail"` in new UI literals |
| Use `Refs #229` (never `Closes #229`) on the local commit and do not push | confirmed | user + repository instruction | Human AT/usability acceptance (`#151`, `#155`) remains open, and caller instructed leaving a frozen local commit without pushing | C15 | Commit locally on `feat/ux-229-data-steward-wcag` at closeout |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| Human assistive-technology and user-validation sign-off for `#229` under `#151` / `#155` | Named human screen-reader and keyboard review with representative data steward / operator tasks | Repository owner / accessibility reviewer | Required before closing `#229` or ticking its final acceptance checkbox | follow-up (non-blocking for `Refs #229` engineering slice) |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
|----------|---------------|----------------|---------|-----------|------------------------------|
| L | Inspect live screen-reader announcements across `data-operator` with NVDA/VoiceOver protocol | Supplies human AT acceptance evidence for `#151` / `#155` | When human accessibility evaluation session runs | deferred | Q2, Q3; C15 |

## Planning Readiness

* Status: Ready
* Decision state: Converged on `screenJumpNav` + `operatorPanel` (`<section tabindex="-1">`) + fail-closed `State:` / `Source state:` textual helpers in `role-screens.js`, backed by expanded unit/accessibility tests in `test_data_steward_screen_wcag.py`.
* Evidence basis: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14, C15, C16, W1
* Preconditions met: Target files, peer reference patterns, exact DOM/copy/test constraints, and validation commands verified.
* Blockers: none
* Smallest action to change readiness: none (already Ready)

## Closeout Record

| Field                            | Record                                                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                                       |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian completed in order                                                                      |
| Lane evidence or inline fallback | Inline execution across `src/api/` and `docs/reference/research/ux/` (tightly coupled single-file screen module)               |
| Research disposition             | executed                                                                                                                       |
| Planning Readiness               | Ready (C1–C16, W1)                                                                                                             |
| Blockers                         | none                                                                                                                           |
| Continuation owner and state     | Confirmed automatic RPI Agent; automatic continuation to `Plan` (`rpi-plan`)                                                   |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (C1–C16, W1)                                                                                           |
| Output mode and planning support | convergence; yes, single recommended implementation approach selected with verified constraints              |
| Acting owner                     | confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | Research disposition recorded (passed); Planning Readiness Ready (passed); pre-transition state write (next) |
| Continuation result              | automatic continuation to `Plan` (`rpi-plan`)                                                                |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/229-data-steward-wcag-research.md                                      |
| Notes for planning or re-entry   | Place `operator*` helpers near `operatorSide`/`operatorStatus` (`role-screens.js:1073`), keep `role-screens.js:268-275` unchanged, avoid banned terms in `test_content_standard.py`, and place new WCAG tests in `src/api/tests/test_data_steward_screen_wcag.py`. |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: Further research is immaterial because all affected code paths, fixtures, and regression suites in `src/api/` have been inspected directly.

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
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
