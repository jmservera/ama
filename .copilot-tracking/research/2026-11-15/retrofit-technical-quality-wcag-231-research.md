<!-- markdownlint-disable-file -->

# Task Research: retrofit-technical-quality-wcag-231

| Field              | Value                                                                                      |
|--------------------|--------------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                                 |
| Researcher / agent | rpi-research (under RPI Agent automatic mode)                                              |
| Status             | Complete                                                                                   |
| Artifact path      | .copilot-tracking/research/2026-11-15/retrofit-technical-quality-wcag-231-research.md      |

## Research Brief

* What to research: Current implementation, WCAG 2.2 baseline (#151) gaps, keyboard section jump navigation, textual state meaning, non-colour status signals, table semantics, routing aliases, and counted baseline/browser-check guards for the Retrofit Assessor, Retrofit Designer, and Quality Inspector screens (`technical-queue` and `quality-queue`) in `src/api` for GitHub issue #231.
* Why it matters: Four of five acceptance criteria on issue #231 are already checked (`[x]`), leaving `- [ ] Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation` to deliver on engineering side while preserving source facts, design version, missing references, separate sign-offs, competent-reviewer return routing, positive per-measure evidence, defect owner, return/reinspection, incomplete-evidence handover blocking, Fluent 2 design system components (#150), zero role simulator controls, and all counted baseline guards.
* Audience or intended use: Downstream `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` phases in this confirmed automatic RPI session, plus PR reviewers checking #231 evidence.
* Scope: `src/api/src/zava_forward/api/web/role-screens.js`, `app.js`, `style.css`, `index.html`, tests in `src/api/tests/`, browser check scripts in `src/api/checks/`, UX baseline/journey docs in `docs/reference/research/ux/`, PRD journey contract in `docs/prds/`, and Web Interface Guidelines.
* Non-goals: Adding mutation controls to read-only technical/quality screens; introducing role simulator UI; modifying backend domain authority; claiming human screen-reader or assistive-technology acceptance (#155); pushing to remote.
* Criteria: Every claim grounded in `path:line` or external `URL + retrieval date`; preserve all four checked #231 criteria and existing test/conformance/counted-guard contracts; satisfy Fluent 2 design system, WCAG 2.2 AA baseline, plain-language content standard, and Web Interface Guidelines.
* Requested outputs: Converged implementation recommendation with exact screen/helper/CSS/test touchpoints, rejected alternatives, risk analysis, and `Planning Readiness` assessment.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                   |
|----------------------------------|-------------------------------------------------------------------------|
| Research question(s)             | How do `technical-queue` and `quality-queue` (both per-home and cross-home summary views) currently implement keyboard jump navigation, focus targets, textual state meaning, non-colour status signals, table semantics, and hash routing, and what exact changes and tests satisfy #231's WCAG 2.2 baseline (#151) without breaking counted baseline guards or browser checks? |
| Codebase scope                   | `src/api/src/zava_forward/api/web/`, `src/api/tests/`, `src/api/checks/`, `docs/reference/research/ux/`, `docs/prds/` |
| External scope                   | Vercel Web Interface Guidelines (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`) |
| Initial internal candidate areas | `src/api/src/zava_forward/api/web/role-screens.js`, `app.js`, `style.css`, `src/api/tests/test_technical_quality_screens.py`, `test_assessor_screen_wcag.py`, `test_accessibility_baseline.py`, `src/api/checks/specialist_keyboard_browser_check.py`, `connected_home_browser_check.py`, `atlas_tensions_browser_check.py`, `role_screens_browser_check.py` |
| Initial external candidate areas | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` |
| Research posture                 | balanced                                                                |
| Posture provenance               | default (bounded UX/accessibility task with named screens, sibling #226/#227/#232 precedents, and strict counted-guard invariants) |
| Explicit limits / deadline       | Focused validation tier specified by caller; non-interactive CLI execution; do not push to remote |
| Posture-specific completion basis | balanced scope coverage and adequate evidence across both screens, routing, CSS, unit tests, and browser-check contracts |
| Edits allowed during research?   | no, research-only                                                       |
| Resolved evidence root           | `.copilot-tracking/`                                                    |
| Known constraints / excluded sources | Read-only reader screens only (no mutation forms, no role simulator controls); engineering checks do not establish human assistive-technology or usability acceptance (#151, #155) |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                        | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|----------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md` | `applyTo: "**"` matches repository and evidence paths | Enforces AMA knowledge-base rules, Fluent 2 (#150), WCAG 2.2 baseline (#151), plain-language content standard, Web Development Guidance, and Focused validation tier | Selected: mandatory repository contract |
| Skill               | `rpi-research`                   | Canonical RPI Phase 1 skill                       | Three-wave research artifact and readiness contract | Selected: active phase contract |
| Skill               | `accessibility`                  | Semantic match for WCAG 2.2 AA and ARIA APG       | Normative WCAG 2.2 / non-colour state / keyboard focus criteria | Selected: guides WCAG 1.3.1, 1.4.1, 2.1.1, 2.4.1, 2.4.7 analysis |
| Skill               | `web-design-guidelines`          | Required by Web Development Guidance before web edits | Fetched Vercel Web Interface Guidelines ruleset (`W1`) | Selected: mandatory pre-edit web audit ruleset |
| Skill               | `redesign-existing-projects`     | Required by Web Development Guidance for existing-app UX upgrades | Targeted in-stack accessibility/state improvements subordinate to Fluent 2 (#150) | Selected: constrained by Fluent 2 design-system inventory |
| Research specialist | `hve-core-all:rpi-researcher`    | General research worker visible in host           | Bounded subagent lane artifact               | Skipped: inline investigation selected because all target files (`role-screens.js`, `style.css`, tests, browser checks) are tightly coupled around shared exact-string and AST/DOM contracts |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Caller supplied exact issue (#231), branch, validation tier, target files, and counted-guard list in non-interactive CLI mode. | N/A (non-interactive)     | Proceed directly with Cycle 1 `balanced` research across `technical-queue`, `quality-queue`, CSS, tests, and browser checks. |
| Direction change | No scope ambiguity or conflicting direction emerged during research. | N/A                       | Keep active brief unchanged. |
| Convergence      | All five research sub-questions answered with high-confidence code and external evidence after one complete three-wave cycle. | N/A                       | Mark `Planning Readiness: Ready` and hand off to confirmed automatic RPI Agent parent for `Plan`. |

## Scope and Success Criteria

* Scope: `technical-queue` and `quality-queue` in `src/api/src/zava_forward/api/web/role-screens.js`, routing in `app.js`, focus/status/table styles in `style.css`, counted baseline guards (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`), existing screen/conformance tests (`test_technical_quality_screens.py`, `test_assessor_screen_wcag.py`, `test_role_screens_conformance.py`, `test_connected_home_check.py`, `test_content_standard.py`, `test_design_system.py`), and browser checks (`specialist_keyboard_browser_check.py`, `connected_home_browser_check.py`, `atlas_tensions_browser_check.py`, `role_screens_browser_check.py`).
* Assumptions: Verified whether dedicated Retrofit Assessor or Retrofit Designer screens exist separately from `technical-queue` and `quality-queue` (confirmed they do not: PAS 2035 assessment, design, building/safety, and coordination sign-offs plus source facts, design version, returns, and missing references live in `technical-queue`, while per-measure checklists, defects, and handover live in `quality-queue`).
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and why-rejected rationale in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Audit Retrofit Assessor, Retrofit Designer, and Quality Inspector (`technical-queue` and `quality-queue`) screens following `#226`, `#227`, and `#232`; ensure keyboard navigation (`class="screen-links"`, `tabindex="-1"` focus targets, visible focus indicators), explicit textual state meaning across source facts, design version, missing references, separate sign-offs, per-measure evidence, defect owner, and return/reinspection, table captions/headers, zero role simulator controls, compatibility with counted baseline guards and browser checks, and focused WCAG 2.2 tests in `src/api/tests/test_technical_quality_screens_wcag.py`.
* Inferred research questions: How `a[data-jump]` interacts with `app.js` hash routing and `test_assessor_screen_wcag.py`; which exact `<dt>`/`<dd>` labels, panel `<h2>` titles, table captions, and JSON string leaves are pinned by existing tests and Playwright browser checks; whether `role-screens.js` positive readiness banners use documented `.status-line.ok`; and whether table body rows provide `<th scope="row">`.
* Caller constraints and non-goals: Focused validation tier; no push to remote; preserve all four checked #231 criteria; engineering checks do not claim human assistive-technology acceptance (#151, #155).

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Focused validation tier (`src/api` unit/WCAG/baseline tests + `ruff` + `mypy` + `web-design-guidelines`) | Caller intake        | Bounds validation scope while requiring zero regressions in browser-check contracts |
| exclude                                                  | Zero role simulator controls in user views; do not push commits to remote | Caller intake        | Enforces static/rendered simulator absence checks and local-only git commit |

## Research Questions

|  # | Sub-question     | Type (depth / breadth / straightforward) | Priority  | Status                    |
|---:|------------------|------------------------------------------|-----------|---------------------------|
| Q1 | Which registered specialist screens implement the #231 Retrofit Assessor, Retrofit Designer, and Quality Inspector journeys, and how does `app.js` route to them? | straightforward | H | answered |
| Q2 | How do `technical-queue` and `quality-queue` currently implement `class="screen-links"` keyboard jump navigation, section landmarks, programmatic heading focus (`tabindex="-1"`), and visible focus styling? | depth | H | answered |
| Q3 | Where do `technical-queue` and `quality-queue` still rely on unprefixed text, undocumented status classes, or missing state cues across source facts, design version, missing references, separate sign-offs, per-measure evidence, defect owner, and return/reinspection? | depth | H | answered |
| Q4 | Do all rendered tables on `technical-queue` and `quality-queue` expose captions, `<th scope="col">`, `<th scope="row">`, and keyboard-focusable scroll regions without tripping counted baseline guards? | straightforward | H | answered |
| Q5 | Which exact panel titles, field values, substrings, static regexes, and region inventories are pinned by existing unit tests and Playwright browser checks? | breadth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-14/231-assessor-screens-wcag-research.md`, `.copilot-tracking/changes/2026-11-14/231-assessor-screens-wcag-changes.md`, `.copilot-tracking/reviews/2026-11-14/231-assessor-screens-wcag-review.md`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/design-system.md`, `docs/reference/research/ux/content-standard.md`, `docs/reference/research/ux/atlas-screen-trace.md`.
* Reused (verified) findings: Confirmed in `role-screens.js` that no standalone Assessor/lodgement screen exists; PAS 2035 assessment/design/building/coordination evidence is rendered on `technical-queue` and quality/handover evidence on `quality-queue` (`C1`, `C2`); confirmed `h()` is mocked as plain `{tag, attrs, kids}` objects in Node VM unit tests (`C11`, `C12`).
* Superseded / stale: Earlier slice `8627074ca` added partial sign-off/per-check prefixes and a `<ul><li><a href="#${id}">` nav on `technical-queue` only, leaving `technical-queue` jump links without `data-jump` (which breaks SPA hash routing when activated!), leaving `quality-queue` with zero jump links or section landmarks, leaving `Source facts`, `Design version`, `Missing references`, measure state, ownerless defect, and reinspection state without complete `Object.hasOwn`-safe textual cues, leaving positive readiness banners on bare `class: "ok"` instead of `.status-line.ok`, and leaving all 5 tables without `<th scope="row">` (`C2`, `C3`, `C4`, `C5`, `C6`).

## Research Cycle Log

### Cycle 1

* Active direction controls: Focused validation tier; zero role simulator controls; local commit without push.
* Active research posture and completion basis: `balanced`; complete coverage of both target screens, sibling WCAG patterns (`#226`, `#227`, `#228`, `#232`), CSS rules, counted baseline guards, and all browser-check contracts.
* Explicit limits or deadline effect: None blocking research; all code, tests, checks, and external Web Interface Guidelines (`W1`) were retrieved directly.

#### Wave 1: Wider

* Plan and independent lanes: Surveyed `role-screens.js`, `app.js`, `style.css`, UX baseline docs (`wcag-conformance-baseline.md`, `design-system.md`, `content-standard.md`, `atlas-screen-trace.md`), sibling WCAG commits (`#226` `0e8d6aabd`, `#227` `5536c3907`, `#228` `test_procurement_qa_screen_wcag.py`, `#232` `5a350916d`, earlier `#231` `8627074ca`), and fetched Vercel Web Interface Guidelines (`W1`).
* Worker evidence relationships or inline fallback: Inline investigation (`C1`–`C10`, `W1`) mapped how `roleScreensView` renders `#/screens?screen=<id>&case=<id>`, how `assetJumpNav`, `residentJumpNav`, and `procurementJumpNav` wire `a[data-jump]` to `<h2 id="...-heading" tabindex="-1">`, and how `stateCue` and `screenRecordTable` work across sibling screens.
* Reflection: Identified five distinct gaps between `technical-queue`/`quality-queue` and the `#226`/`#228`/`#232` WCAG pattern: missing `data-jump` on `technical-queue` (plus `<ul><li>` flex-layout wrapper), completely missing jump nav and section anchors on `quality-queue`, bare `class: "ok"` instead of `.status-line.ok`, incomplete non-colour textual state cues (including non-independent acceptance still showing `"Verified: Evidence noted"` on check items!), and missing `<th scope="row">` row headers.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Deep-dived exact helper mechanics (`screenPanel`, `screenRecordTable`, `a[data-jump]` click delegation, `evidenceLabel`, `qualityAcceptanceGap`), CSS focus/status rules (`style.css`), and counted baseline guards (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`, `test_role_screens_conformance.py`, `test_content_standard.py`, `test_design_system.py`).
* Plan and independent lanes: Verified exact counts (`setAttribute("aria-invalid", "true")` = 8; `h("table", {}, ...)` = 13; `setTimeout` = 2) and CSS rules (`.status-line.ok`, `.status-line.ok:before`, `:focus-visible`, `.screen-links`).
* Worker evidence relationships or inline fallback: Inline verification (`C3`, `C6`, `C7`, `C8`, `C9`, `C10`) confirmed `screenRecordTable` reuses `screenTable` (keeping `h("table", {}, ...)` at 13), read-only screens add zero `aria-invalid` calls (keeping count at 8) and zero `/api/...` endpoints, and styling `.screen-record h2[tabindex="-1"]:focus` in `style.css` guarantees visible focus rings when `a[data-jump]` moves focus programmatically via pointer click as well as keyboard `Enter` without introducing any `animation` or `transition` in `.screen-*` rules (`C6`, `C10`).
* Reflection: Candidate design is clean, surgical, and requires zero counted-guard inflation, provided every downstream test and browser-check expectation is respected.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenged candidate edits against every unit test and Playwright check (`test_assessor_screen_wcag.py`, `test_technical_quality_screens.py`, `test_learning_test_bundle_scenarios.py`, `test_connected_home_check.py`, `specialist_keyboard_browser_check.py`, `connected_home_browser_check.py`, `atlas_tensions_browser_check.py`, `role_screens_browser_check.py`) to catch hidden breakages!
* Plan and independent lanes: Audited exact AST/JSON/DOM assertions across all 8 test/check suites (`C11`–`C16`).
* Worker evidence relationships or inline fallback: Inline contrarian audit uncovered six critical constraints that naive edits would have broken:
  1. `test_assessor_screen_wcag.py:76-80` (`C11`) asserts `{a["attrs"]["href"][1:] for a in walk(nav)} == {s["attrs"]["id"] for s in sections_with_id}`. If `href` were `#${id}-heading` like `#226`/`#232`, `test_assessor_screen_wcag.py` would fail! Setting `href: "#${id}"` while setting `"data-jump": "${id}-heading"` and `"data-jump-target": "${id}-heading"` satisfies BOTH `test_assessor_screen_wcag.py` (`href` matches `<section id="${id}">`) AND the `a[data-jump]` delegated focus handler (which focuses `<h2 id="${id}-heading" tabindex="-1">` without mutating `location.hash`)! Furthermore, every `<section>` given an `id` on `technical-queue` or `quality-queue` must appear in `<nav class="screen-links">`, and `"Not shown for this role"` (`screenWithheld`) can either remain un-anchored or anchored consistently if included in the nav. Keeping `screenWithheld` un-anchored while anchoring `"Evidence boundary"` + all substantive panels keeps `targets == set(sections)` exact on both screens!
  2. `atlas_tensions_browser_check.py:424-441` (`C15`) and `connected_home_browser_check.py:242-243` (`C14`) assert exact `<dd>` equality for `Current design version` (`str(technical["design_version"])`) and `Recorded by` (`str(technical["design_name"])`). Therefore, textual design-version state must be added as a separate `<dt>`/`<dd>` row (`["Design state", ...]`), never concatenated into `Current design version`!
  3. `test_technical_quality_screens.py:306` (`C12`) asserts `self.assertIn('"Passed"', text)` on `json.dumps(tree)`! Therefore, the `"Reinspection"` `<dd>` leaf for accepted/handed-over defect records must remain exact `"Passed"` while a companion `["Reinspection state", ...]` field provides explicit `Verified:` / `Pending review:` / `Action needed:` textual state meaning!
  4. `role_screens_browser_check.py:260` (`C16`) queries `evidence.locator('p.ok[role="status"]')`. Changing `class: "ok"` to `class: "status-line ok"` preserves the `.ok` class selector match while activating the documented `.status-line.ok` border, background, and `✓ ` non-colour glyph (`C6`)!
  5. `specialist_keyboard_browser_check.py:41-55` (`C13`) pins `EXPECTED_REGIONS["technical-queue"] = ("Sign-off validity after design changes",)` and `NO_REGION_GAPS["quality-queue"]` on the default synthetic fixture (where `records` is empty). We must preserve the exact caption `"Sign-off validity after design changes"` and render no table on `quality-queue` when `records` is empty.
  6. `test_connected_home_check.py:215-235` (`C14`) statically parses `screenPanel("Literal title", ...)` in `role-screens.js` and forbids case-field references inside `"Evidence boundary"`. Passing `{ anchor: "technical-boundary" }` and `{ anchor: "quality-boundary" }` uses string literals only, keeping `RECORD_PANELS` and `EXCLUDED` 100% aligned!
* Reflection: Every contrarian constraint has a clean, zero-conflict design resolution. No unresolved gaps remain.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment  |
|------------------|---------------------------------|-----------------------------------------------------|--------------------------|-----------------------------|
| Wire `a[data-jump="${id}-heading"]` with `href="#${id}"` and direct `<a>` links inside `<nav aria-label="Sections on this screen" class="screen-links">` on both `technical-queue` and `quality-queue` (including dynamic per-measure anchors) | `C1`, `C2`, `C4`, `C11`, `W1` | accepted | Prevents SPA hash-route clobbering, focuses `<h2 id="${id}-heading" tabindex="-1">`, fixes `.screen-links` flex layout, and keeps `test_assessor_screen_wcag.py` green | Selected Recommendation |
| Style `.screen-record h2[tabindex="-1"]:focus` with Fluent 2 focus tokens and `.screen-evidence th` with `tabular-nums` in `style.css` | `C6`, `C10`, `W1` | accepted | Ensures visible focus indicator on programmatic jump-link focus (pointer or keyboard) without adding motion to `.screen-*` | Selected Recommendation |
| Upgrade positive readiness `<p role="status">` on both screens from `class: "ok"` to `class: "status-line ok"` | `C2`, `C5`, `C6`, `C9`, `C16` | accepted | Activates documented Fluent 2 `.status-line.ok` border + `✓` glyph while still matching `p.ok[role="status"]` in `role_screens_browser_check.py` | Selected Recommendation |
| Add `Object.hasOwn`-safe textual state cues for `Source facts` (`stateCue(assetConflictCues, ...)`), `Design state`, `Missing references` (`State` column), `Returns and routing` (`State` column), `quality-queue` `Measure state`, non-independent per-check evidence guard, ownerless `Defect owner`, and `Reinspection state` | `C2`, `C3`, `C5`, `C8`, `C11`, `C12`, `C14`, `C15`, `C16` | accepted | Eliminates remaining ambiguous/unprefixed state surfaces while preserving every pinned field value and substring | Selected Recommendation |
| Switch all 5 tables on `technical-queue` and `quality-queue` from `screenTable` to `screenRecordTable` (`rowHeader = true`) | `C1`, `C7`, `C16` | accepted | Adds `<th scope="row">` to every body row alongside `<caption>` and `<th scope="col">` without changing the pinned `h("table", {}, ...)` count of 13 | Selected Recommendation |
| Modify `Current design version` `<dd>` or replace `"Passed"` in `Reinspection` `<dd>` in-place | `C12`, `C14`, `C15` | rejected | Would break `atlas_tensions_browser_check.py`, `connected_home_browser_check.py`, and `test_technical_quality_screens.py` exact assertions | Alternative 1 (rejected) |
| Build a separate standalone Retrofit Assessor lodgement screen | `C2`, `C10` | deferred | Out of scope for #231's current registered screen architecture (`atlas-screen-trace.md`); already tracked as a future follow-up when lodgement workflow exists | Potential Next Research / Follow-up |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: `balanced` scope coverage and saturation achieved; all 5 sub-questions answered with exact line citations and contrarian verification across unit, conformance, and browser checks.
* Revised brief or revalidation required: none
* Readiness effect: `Ready`

## Evidence Log

* Delegation: inline: target files (`role-screens.js`, `style.css`, unit tests, and Playwright checks) share tightly coupled exact-string, regex, and counted-guard contracts best verified directly in one coherent pass.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`)           | Tool                                | Confidence       | Notes       |
|----|-----------------|----------------------------------|-------------------------------------|------------------|-------------|
| C1 | `screenPanel` sets `id`, `aria-labelledby="${id}-heading"`, and `<h2 id="${id}-heading" tabindex="-1">`; `screenRecordTable` wraps `screenTable(..., rowHeader=true)` adding `<th scope="row">`, `<caption>`, `<th scope="col">`, and `<div class="table-scroll" role="region" aria-label="..." tabindex="0">`; `stateCue` uses `Object.hasOwn`. | `src/api/src/zava_forward/api/web/role-screens.js:18-71` | view | high | Shared specialist-screen accessibility primitives |
| C2 | `technical-queue` renders `<nav class="screen-links"><ul><li><a href="#${id}">` without `data-jump`, uses `class: "ok"` on ready status, uses raw `assetStatus(c, q)` in `Source facts`, has no state column on `Missing references` or `Returns and routing`, and uses `screenTable` instead of `screenRecordTable`. | `src/api/src/zava_forward/api/web/role-screens.js:720-782` | view | high | Primary gaps on `technical-queue` |
| C3 | `quality-queue` has no `<nav class="screen-links">` and no panel anchors/section IDs, uses `class: "ok"` on ready status, stamps `"Verified: Evidence noted"` even when `qualityAcceptanceGap(r)` is non-empty, lacks a `Measure state` cue row, renders `"Unknown"` on blank defect owner, and uses `screenTable` instead of `screenRecordTable`. | `src/api/src/zava_forward/api/web/role-screens.js:784-854` | view | high | Primary gaps on `quality-queue` |
| C4 | Shared delegated click handler intercepts `a[data-jump]`, calls `event.preventDefault()`, focuses `document.getElementById(link.getAttribute("data-jump"))`, and calls `scrollIntoView({ block: "start" })` so SPA `#/screens?...` routing in `app.js` is preserved; `#226`, `#228`, and `#232` render direct `<a>` children in `<nav class="screen-links">`. | `src/api/src/zava_forward/api/web/role-screens.js:284-293` | view | high | Also see `app.js:409-466` and `role-screens.js:859-862,1404-1409` |
| C5 | `design-system.md` documents `.status-line`, `.ok`, `.blocked`, `.empty`, `.screen-links`, `.screen-record`, `.screen-evidence`, and `.table-scroll`; `style.css` defines `.status-line.ok` and `.status-line.ok:before { content: "\2713\00a0" }`, not standalone `.ok`. | `src/api/src/zava_forward/api/web/style.css:328-373` | view | high | Paired with `docs/reference/research/ux/design-system.md` |
| C6 | `style.css` defines global `:focus-visible` outline/box-shadow using `--focus-w`, `--focus-ink`, `--focus-off`, `--focus`, and `.screen-record[id], .screen-evidence h2[tabindex="-1"] { scroll-margin-top: var(--sp-5); }`, without `:focus` styling on `h2[tabindex="-1"]` after pointer-triggered programmatic `.focus()`. | `src/api/src/zava_forward/api/web/style.css:52-53` | view | high | Also `style.css:364-372` |
| C7 | Counted baseline guards pin `setAttribute("aria-invalid", "true")` at 8 occurrences across `web/*.js`, `h("table", {}, ...)` at 13 occurrences, and `/api/...` GET endpoints against the export inventory. | `src/api/tests/test_accessibility_baseline.py:85-175` | view | high | Also `test_epic149_form_error_summary_associations.py:35-60` and `test_list_export_inventory.py:1-90` |
| C8 | `test_content_standard.py` bans internal jargon (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) in all served web copy including `role-screens.js`. | `src/api/tests/test_content_standard.py:13-70` | view | high | Must avoid all 6 banned word families in new state copy |
| C9 | `test_design_system.py` enforces that every CSS class used in `role-screens.js` exists in `style.css` and `docs/reference/research/ux/design-system.md`. | `src/api/tests/test_design_system.py:68-76` | view | high | Any class in `role-screens.js` must already be in the #150 inventory |
| C10 | `test_role_screens_conformance.py` bans role simulator terms (`simulat`, `impersonat`, `act as role`, `switch role`), `innerHTML`, `href: "#"`, `onclick` on non-buttons, inline styles, `animation`/`transition` in `.screen-*` CSS rules, and extra timers. | `src/api/tests/test_role_screens_conformance.py:56-103` | view | high | Static UX conformance guardrails |
| C11 | `test_assessor_screen_wcag.py` asserts `nav["attrs"]["aria-label"] == "Sections on this screen"` and `{a["attrs"]["href"][1:] for a in walk(nav)} == {s["attrs"]["id"] for s in sections_with_id}` on `technical-queue`, plus sign-off and per-check prefixes. | `src/api/tests/test_assessor_screen_wcag.py:60-94` | view | high | Requires `href="#${id}"` paired with `data-jump="${id}-heading"` |
| C12 | `test_technical_quality_screens.py` asserts exact JSON string leaf `'"Passed"'` for reinspection after handover, plus substrings `"Recorded evidence is complete"`, `"Every measure has accepted evidence"`, `"Defect owner"`, `"Installer Ltd"`, and documented design-system classes. | `src/api/tests/test_technical_quality_screens.py:285-414` | view | high | Also `test_learning_test_bundle_scenarios.py:800-835` |
| C13 | `specialist_keyboard_browser_check.py` pins `EXPECTED_REGIONS["technical-queue"] = ("Sign-off validity after design changes",)` and `NO_REGION_GAPS["quality-queue"]` on the default synthetic fixture. | `src/api/checks/specialist_keyboard_browser_check.py:35-65` | view | high | Caption and empty-records behavior must not change |
| C14 | `connected_home_browser_check.py` and `test_connected_home_check.py` pin exact panel titles (`RECORD_PANELS` + `EXCLUDED`), exact `<dt>`/`<dd>` pairs (`Current design version`, `Recorded by`, `Submitted by`, `Accepted by`, `Handed over by`), and forbid home-record field reads inside `"Evidence boundary"`. | `src/api/checks/connected_home_browser_check.py:240-266` | view | high | Also `test_connected_home_check.py:215-235` |
| C15 | `atlas_tensions_browser_check.py` asserts `Current design version` `<dd>` equals `str(technical["design_version"])` and checks same-home technical and per-measure quality panel titles and substrings across 1280/768/360/320px viewports. | `src/api/checks/atlas_tensions_browser_check.py:424-510` | view | high | Preserves responsive layout and exact version `<dd>` |
| C16 | `role_screens_browser_check.py` checks `p.ok[role="status"]` on positive scenarios `231p` and `231qp`, verifies Tab reaches every `div.table-scroll[role="region"]` within 80 Tab presses, and defines `check_table_headers` requiring `<caption>`, `<th scope="col">`, and `<th scope="row">`. | `src/api/checks/role_screens_browser_check.py:255-355` | view | high | `class: "status-line ok"` and `screenRecordTable` align both screens with full checks |

### External Evidence

| ID | Claim / finding | Source (title) | URL     | Retrieved      | Version/date | Confidence       |
|----|-----------------|----------------|---------|----------------|--------------|------------------|
| W1 | Interactive elements need visible `:focus-visible` rings, semantic `<nav>`/`<a>`/`<table>` elements, `scroll-margin-top` on heading anchor targets, `tabular-nums` on data tables, and non-colour textual status indicators without layout-shifting animations. | Vercel Web Interface Guidelines (`command.md`) | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` | 2026-11-15 | `main` (retrieved 2026-11-15) | high |

### Contradictions / Conflicts

* Jump link `href` convention across sibling screens: `#226` and `#232` set `href: "#${id}-heading"` (`C4`), whereas `#231`'s earlier slice (`test_assessor_screen_wcag.py`, `C11`) asserts `href` equals `#${section.id}` while `section["aria-labelledby"]` and `h2["id"]` equal `${section.id}-heading`. Resolved by consistency with both contracts: set `href: "#${id}"` (matching `<section id="${id}">`) and `"data-jump": "${id}-heading"`, `"data-jump-target": "${id}-heading"` (focusing `<h2 id="${id}-heading" tabindex="-1">` via the delegated click listener without changing `location.hash`).

## Findings Mapped to Questions and Evidence

| Question | Finding             | Evidence IDs | Confidence          | Decision or readiness implication    |
|----------|---------------------|--------------|---------------------|--------------------------------------|
| Q1       | Retrofit Assessor, Retrofit Designer, and Quality Inspector views are served by `technical-queue` and `quality-queue` in `role-screens.js` under `#/screens?screen=<id>&case=<id>`; no separate Assessor/lodgement screen exists, and neither screen exposes role simulator controls. | `C1`, `C2`, `C3`, `C10` | high | Scope implementation to `technical-queue`, `quality-queue`, `style.css`, and focused WCAG tests. |
| Q2       | `technical-queue` jump links lack `data-jump` (clobbering SPA hash routing when clicked/activated) and wrap links in an unstyled `<ul><li>` inside flex `.screen-links`; `quality-queue` lacks `<nav class="screen-links">` and section/heading anchors completely; `h2[tabindex="-1"]:focus` needs explicit Fluent 2 focus styling for programmatic focus. | `C2`, `C3`, `C4`, `C6`, `C11`, `W1` | high | Use shared PAS 2035 jump-nav helper emitting direct `<a href="#${id}" data-jump="${id}-heading" data-jump-target="${id}-heading">` links on both screens and style `.screen-record h2[tabindex="-1"]:focus`. |
| Q3       | Positive readiness banners use bare `class: "ok"` instead of `.status-line.ok`; `Source facts` lacks `stateCue(assetConflictCues, ...)`; `Design version` lacks a textual `Design state` row; `Missing references` and `Returns and routing` lack a `State` column; `quality-queue` lacks a `Measure state` cue row, marks check items `"Verified: Evidence noted"` even when acceptance is self-certified or unnamed, shows `"Unknown"` instead of `"Action needed: ..."` for blank defect owner, and lacks a prefixed `Reinspection state` field. | `C2`, `C3`, `C5`, `C8`, `C11`, `C12`, `C16` | high | Add `Object.hasOwn`-safe textual cues across all 7 areas and switch ready banners to `class: "status-line ok"`. |
| Q4       | All 5 tables on `technical-queue` and `quality-queue` currently call `screenTable` (no `<th scope="row">`). Switching them to `screenRecordTable` adds `<th scope="row">` while keeping `<caption>`, `<th scope="col">`, `div.table-scroll[role="region"][tabindex="0"]`, and the pinned `h("table", {}, ...)` count of 13 unchanged. | `C1`, `C2`, `C3`, `C7`, `C16` | high | Convert all 5 tables to `screenRecordTable` with zero baseline-guard churn. |
| Q5       | Existing tests and browser checks pin exact panel titles, `Current design version` and `Recorded by` `<dd>` values, JSON leaf `'"Passed"'`, `p.ok[role="status"]`, caption `"Sign-off validity after design changes"`, and `NO_REGION_GAPS["quality-queue"]` when `records` is empty. | `C11`–`C16` | high | Add companion `<dt>`/`<dd>` fields (`Design state`, `Measure state`, `Reinspection state`) rather than mutating pinned `<dd>` values. |

## Key Discoveries

* Activating any jump link in `technical-queue` today navigates away from `#/screens?screen=technical-queue&case=...` because `<a href="#technical-readiness">` omits `data-jump` (`C2`, `C4`).
* `quality-queue` currently has zero jump navigation links and zero labelled `<section id="..." aria-labelledby="...-heading">` landmarks (`C3`).
* In `quality-queue`, a record in `"Accepted"` or `"Handed over"` state whose `qualityAcceptanceGap(r)` is non-empty (for example, accepted without a named inspector or self-accepted by `submitted_by`) rightly blocks `"Handover readiness"`, yet still labels per-check rows `"Verified: Evidence noted"` (`C3`). Guarding per-check `"Verified"` and `Measure state` on `!qualityAcceptanceGap(r)` closes an important PAS 2035 integrity/WCAG 1.4.1 gap!
* Using `class: "status-line ok"` on positive readiness banners satisfies Fluent 2 `.status-line.ok` (`✓ ` glyph + border/surface tokens) AND continues to match `p.ok[role="status"]` in `role_screens_browser_check.py` (`C5`, `C16`).

### Complete Examples

```javascript
const pasJumpNav = (sections) => h("nav", { "aria-label": "Sections on this screen", class: "screen-links" },
  sections.map(([id, label]) => h("a", { href: `#${id}`, "data-jump": `${id}-heading`, "data-jump-target": `${id}-heading` }, label)));
```

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Upgrade `technical-queue` and `quality-queue` in `role-screens.js` and `style.css` in place:
  1. Add `pasJumpNav(sections)` rendering `<nav aria-label="Sections on this screen" class="screen-links">` with direct `<a href="#${id}" data-jump="${id}-heading" data-jump-target="${id}-heading">` links on both `technical-queue` (7 anchored sections: `technical-boundary` plus the 6 domain sections) and `quality-queue` (`quality-boundary`, `quality-readiness`, and dynamic `qualityRecordAnchor(r, i)` per measure or `quality-evidence` when empty), plus an explicit plain-language note in `Evidence boundary` that every state is written in words first and colour is never the only signal.
  2. Style `.screen-record h2[tabindex="-1"]:focus` in `style.css` using the existing Fluent 2 focus tokens (`--focus-w`, `--focus-ink`, `--focus-off`, `--focus`) and include `.screen-evidence th` alongside `.screen-evidence td` for `tabular-nums`.
  3. Upgrade positive readiness `<p role="status">` elements on both screens from `class: "ok"` to `class: "status-line ok"` with explicit leading state cues while preserving exact required substrings.
  4. Complete `Object.hasOwn`-safe textual state cues across `Source facts` (`stateCue(assetConflictCues, assetStatus(c, q))`), `Design version` (`Design state` row), `Missing references` (`State` column: `"Action needed: Missing on record"`), `Returns and routing` (`State` column: `evidenceLabel(x)`), and `quality-queue` (`Measure state` row via `qualityMeasureState(r)`, `!qualityAcceptanceGap(r)` guard before `"Verified: Evidence noted"`, explicit `"Action needed: Unassigned (no defect owner named)"` when a defect lacks a named owner, and `Reinspection state` row via `qualityReinspectionState(r)` alongside the pinned `"Reinspection"` value).
  5. Convert all 5 tables on `technical-queue` and `quality-queue` from `screenTable` to `screenRecordTable` so every table exposes `<caption>`, `<th scope="col">`, `<th scope="row">`, and `<div class="table-scroll" role="region" aria-label="..." tabindex="0">`.
  6. Add comprehensive WCAG 2.2 unit/VM tests in `src/api/tests/test_technical_quality_screens_wcag.py` covering jump-link delegation (`preventDefault`, `focus`, `scrollIntoView`, hash preservation), focus indicators, non-colour textual state cues across all #231 states (including prototype-chain keys and non-independent acceptance), table semantics (`caption`, `scope="col"`, `scope="row"`, focusable region), and absence of role simulator or write controls.
* Rationale: Delivers every #231 WCAG 2.2 baseline engineering requirement (`#151`) and Fluent 2 (`#150`) alignment with zero counted-guard churn and 100% compatibility with all existing unit and Playwright checks.
* Evidence refs: `C1`–`C16`, `W1`
* Implementation impact: `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/style.css`, `src/api/tests/test_technical_quality_screens_wcag.py`. No counted baseline guard totals change (`aria-invalid` remains 8, `h("table", {}, ...)` remains 13, `/api/...` inventory unchanged).
* Confidence: high: all consumer tests and browser checks were inspected line by line.

File tree:

```text
src/api/
  src/zava_forward/api/web/
    role-screens.js          (modify: pasJumpNav, quality anchors, textual state cues, status-line ok, screenRecordTable)
    style.css                (modify: programmatic heading :focus ring and th tabular-nums)
  tests/
    test_technical_quality_screens_wcag.py  (create: focused WCAG 2.2 keyboard, state-cue, table, and simulator-absence tests)
```

### Alternative: Mutate existing `<dd>` fields (`Current design version`, `Reinspection`) and use `href="#${id}-heading"`

* Approach: Prepend `"Recorded: "` directly inside `Current design version` `<dd>`, replace `"Passed"` in `Reinspection` `<dd>` with `"Verified: Passed"`, and change `technical-queue` jump `href`s to `#${id}-heading`.
* Trade-offs: Slightly fewer `<dt>`/`<dd>` rows, at the cost of breaking existing test and browser-check contracts.
* Evidence refs: `C11`, `C12`, `C14`, `C15`
* Rejection rationale: Directly breaks `atlas_tensions_browser_check.py:440` (`value == str(expected)`), `connected_home_browser_check.py:242`, `test_technical_quality_screens.py:306` (`'"Passed"'`), and `test_assessor_screen_wcag.py:80` (`targets == set(sections)`).

### Alternative: Inline `<table>` markup or per-screen custom CSS status classes

* Approach: Build custom `<table>` nodes or new `.tech-ready` / `.quality-badge` CSS classes.
* Trade-offs: Custom layout control, at the cost of inflating counted `h("table", {}, ...)` guards and requiring design-system inventory additions.
* Evidence refs: `C5`, `C7`, `C9`
* Rejection rationale: Violates DRY reuse of `screenRecordTable` and `.status-line.ok`, needlessly mutates counted baseline guards (`test_accessibility_baseline.py`), and diverges from the Fluent 2 component inventory (#150).

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Engineering checks and VM/DOM tests verify markup, keyboard delegation, focus indicators, and textual state cues, not human assistive-technology or usability validation (#151, #155). Issue #231 must continue to use `Refs #231` rather than a closing keyword until human review/acceptance is recorded.
* Follow-up: When a dedicated PAS 2035 lodgement workflow screen is added in a future slice, apply the same `pasJumpNav`, `screenRecordTable`, and `Object.hasOwn` `stateCue` pattern.
* Residual uncertainty: Local Playwright browser binaries may or may not be installed in this shared machine environment; we will test whether `specialist_keyboard_browser_check.py` / `role_screens_browser_check.py` can run locally during Implement and accurately disclose what ran vs skipped.

## Current Decisions

| Decision     | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale     | Evidence IDs | Implications                       |
|--------------|-------------------------------------------------------|-----------------------------------------------|---------------|--------------|------------------------------------|
| Scope #231 WCAG upgrades to `technical-queue` and `quality-queue` in `role-screens.js` + `style.css` + `test_technical_quality_screens_wcag.py` | confirmed | evidence / caller | Those two registered screens implement the Retrofit Assessor, Designer, and Quality Inspector views (`atlas-screen-trace.md`) | `C1`, `C2`, `C3`, `C10` | Surgical diff with zero unrelated churn |
| Pair `href="#${id}"` with `data-jump="${id}-heading"` and `data-jump-target="${id}-heading"` on direct `<a>` links in `nav.screen-links` | confirmed | evidence | Preserves SPA hash route, focuses `<h2 id="${id}-heading" tabindex="-1">`, fixes flex wrapping, and keeps `test_assessor_screen_wcag.py` green | `C2`, `C4`, `C11` | Works identically across `technical-queue` and `quality-queue` |
| Add companion `<dt>`/`<dd>` state rows (`Design state`, `Measure state`, `Reinspection state`) and `screenRecordTable` row headers | confirmed | evidence | Provides complete WCAG 1.4.1 and 1.3.1 semantics without breaking pinned `<dd>` assertions or counted baseline guards | `C1`, `C7`, `C12`, `C14`–`C16` | Counted baseline guards stay unchanged (`8`, `13`) |

## Unresolved Decisions

| Decision     | Smallest evidence or answer needed     | Owner                                  | Impact     | Blocker status                       |
|--------------|----------------------------------------|----------------------------------------|------------|--------------------------------------|
| Human assistive-technology and user-validation sign-off for #231 / #151 / #155 | Manual screen-reader and role-representative walkthrough outside automated CI | Repository owner / human reviewer | Prevents closing #231 (`Refs #231` required instead of `Closes #231`) | follow-up (non-blocking for this engineering slice) |

## Potential Next Research

| Priority  | Research item                  | Expected value     | Trigger                            | Selected?               | Related questions / evidence |
|-----------|--------------------------------|--------------------|------------------------------------|-------------------------|------------------------------|
| L         | Dedicated PAS 2035 lodgement evidence screen UX | Extends textual state cues once lodgement records are introduced | Creation of a lodgement backlog slice | deferred                | Q1; `C2`, `C10`              |

## Planning Readiness

* Status: Ready
* Decision state: Converged on surgical in-place WCAG 2.2 upgrades to `technical-queue`, `quality-queue`, `style.css`, and `test_technical_quality_screens_wcag.py`.
* Evidence basis: `C1`–`C16`, `W1`
* Preconditions met: All target screens, helpers, CSS rules, counted baseline guards, existing unit tests, Playwright browser checks, and Web Interface Guidelines (`W1`) audited and reconciled.
* Blockers: none
* Smallest action to change readiness: none (already `Ready`).

## Closeout Record

| Field                            | Record                                                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                                       |
| Completed waves                  | Cycle 1: Wave 1 Wider, Wave 2 Deeper, Wave 3 Contrarian                                                                        |
| Lane evidence or inline fallback | Inline investigation across `role-screens.js`, `style.css`, `src/api/tests/`, `src/api/checks/`, and `W1` (tightly coupled contracts) |
| Research disposition             | executed                                                                                                                       |
| Planning Readiness               | Ready (`C1`–`C16`, `W1`)                                                                                                       |
| Blockers                         | none                                                                                                                           |
| Continuation owner and state     | Confirmed automatic RPI Agent parent; automatic continuation to `Plan`                                                         |

## Advisory Next Step

| Field                            | Record                                                                                                       |
|----------------------------------|--------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                     |
| Planning Readiness               | Ready (`C1`–`C16`, `W1`)                                                                                     |
| Output mode and planning support | `convergence`; yes — single evidence-backed implementation design selected                                   |
| Acting owner                     | confirmed automatic RPI Agent                                                                                |
| Required gates or confirmations  | Research three-wave completion: passed; Planning Readiness `Ready`: passed; pre-transition state write: passed |
| Continuation result              | automatic continuation to `Plan` (`rpi-plan`)                                                                |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/retrofit-technical-quality-wcag-231-research.md                        |
| Notes for planning or re-entry   | Preserve exact `<dd>` values for `Current design version`, `Recorded by`, and `Reinspection` (`"Passed"`), keep `href="#${id}"` + `data-jump="${id}-heading"`, and verify counted baseline guards stay at 8 and 13. |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: Further research is immaterial because every code path, CSS rule, counted guard, and browser check touching `technical-queue` and `quality-queue` has been directly inspected.

## Sources

* W1 - Vercel Web Interface Guidelines (`command.md`) - https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-11-15, `main`)

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
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry and Provenance, User Participation and Research Decisions, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings Mapped to Questions and Evidence, Key Discoveries, Alternatives and Decision State, Open Questions/Risks, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check.
* Missing or limited sections: none.
