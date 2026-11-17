---
description: "Primary evidence artifact for Issue #226 Asset executive and board views WCAG 2.2 accessibility & keyboard navigation"
---
<!-- markdownlint-disable-file -->

# Task Research: ux-226-asset-exec-wcag-2358

| Field              | Value                                                                               |
|--------------------|-------------------------------------------------------------------------------------|
| Date               | 2026-11-14                                                                          |
| Researcher / agent | rpi-research (RPI Agent)                                                            |
| Status             | Complete                                                                            |
| Artifact path      | .copilot-tracking/research/2026-11-14/ux-226-asset-exec-wcag-2358-research.md       |

## Research Brief

* What to research: How PR #1715 (`#225`) implemented WCAG 2.2 keyboard jump navigation (`role="navigation"`, `aria-label`, delegated jump links) and explicit textual state meaning (non-colour status prefixes / accessible labels) on Finance screens, how the Asset Executive and Board views are structured in `src/api/src/zava_forward/api/web/`, how role-screen conformance and recipe SHA invariants work, and what DOM/unit tests are needed for Issue #226.
* Why it matters: Delivers the remaining local WCAG 2.2 engineering criterion on Issue #226 (`Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation`) without breaking read-only executive boundaries, content standard rules, or workbench/scenario-manifest SHA invariants.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` in this RPI session.
* Scope: `src/api/src/zava_forward/api/web/` (`role-screens.js`, `index.html`, `app.js`, `style.css` / `styles.css`), `src/api/src/zava_forward/api/workbench.py`, `scenario-manifest.json` / `workbench-manifest.json` checks, and `src/api/tests/*` covering Asset Executive / Board views and WCAG conformance.
* Non-goals: Claiming full human/assistive-technology WCAG conformance (#151/#155 manual gates remain open), adding investment approval actions to read-only executive views, using bulk `del sys.modules[...]` in tests, or pushing to remote.
* Criteria: Grounded in exact `path:line` evidence across web assets, Python checks, and existing unit tests; preserves read-only conformance, plain-language glossary (#153), Fluent 2 tokens (#150), and recipe SHA invariants.
* Requested outputs: Converged implementation recommendation, affected file map, conformance/invariant constraints, and verification commands for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                   |
|--------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Q1-Q5 covering PR #1715 pattern, Asset/Board screen DOM structure, textual state gaps, conformance/SHA invariants, and test harness fit |
| Codebase scope                       | `src/api/`, `docs/reference/research/ux/`, `.copilot-tracking/` (for PR #1715 comparison)                                               |
| External scope                       | Vercel Web Interface Guidelines (`command.md`) per repository Web Development Guidance                                                  |
| Initial internal candidate areas     | `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_asset_board_screen.py`, `src/api/tests/test_asset_exec_screen_wcag.py`, `src/api/tests/test_finance_screens_wcag_225.py`, `src/api/tests/test_role_screens_conformance.py`, `src/api/src/zava_forward/api/workbench.py` |
| Initial external candidate areas     | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`                                                |
| Research posture                     | focused                                                                                                                                 |
| Posture provenance                   | default (bounded internal task with named source targets and precedent PR #1715)                                                        |
| Explicit limits / deadline           | Non-interactive session; do not push; never use bulk `del sys.modules[...]` in test files                                               |
| Posture-specific completion basis    | focused scope and materiality                                                                                                           |
| Edits allowed during research?       | no, research-only                                                                                                                       |
| Resolved evidence root               | `.copilot-tracking/`                                                                                                                    |
| Known constraints / excluded sources | Preserve read-only Asset/Board boundary, Fluent 2 design system (#150), WCAG baseline (#151), and plain-language content standard (#153) |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                                            | Scoped authority or output contract                                         | Selected / skipped reason                                                       |
|---------------------|---------------------------------------|-----------------------------------------------------------------|-----------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | AMA Repository Instructions           | `applyTo: "**"`                                                 | Project context, UX/WCAG/content standards, validation tiers, git hygiene   | Selected: governs web edits, plain language, and validation rules               |
| Skill               | `rpi-research`                        | Explicit caller RPI workflow                                    | Three-wave research artifact and readiness gate                             | Selected: active RPI phase skill                                                |
| Skill               | `web-design-guidelines`               | Repository Web Development Guidance mandatory before web edits  | Fetched `command.md` rules and `file:line` review format                    | Selected: loaded and source fetched                                             |
| Skill               | `redesign-existing-projects`          | Repository Web Development Guidance for existing-app UI updates | Targeted stack-preserving accessibility/focus/state audit                   | Selected: loaded; subordinate to Fluent 2 (#150) and WCAG (#151) rules          |
| Skill               | `accessibility`                       | WCAG 2.2 / ARIA landmark & non-colour status semantics          | Normative WCAG 2.2 criteria mapping (1.3.1, 1.4.1, 2.1.1, 2.4.1, 2.4.7, 4.1.2) | Selected: loaded for WCAG 2.2 criteria grounding                             |
| Research specialist | `hve-core-all:rpi-researcher`         | General research lane worker                                    | Bounded independent research lane                                           | Skipped: tightly coupled single-module investigation in `src/api`; inline faster and cleaner |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                 | Answers / unanswered | Resulting decision or selected further research                                  |
|------------------|-------------------------------------------------------------------------------------------------------|----------------------|----------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI run with explicit target files, precedent PR #1715, constraints, and test rules.  | N/A (non-interactive)| Proceed inline in `focused` posture with `convergence` output mode.              |
| Direction change | No scope or direction changes needed during Cycle 1.                                                  | N/A                  | Retain `asset-board` screen, `style.css`, and `src/api/tests/` scope.            |
| Convergence      | All 5 research questions answered with direct codebase and precedent evidence; no blocker remains.    | N/A                  | Converge on anchored landmark jump navigation + textual state cues + DOM tests.  |

## Scope and Success Criteria

* Scope: Asset Executive and Board views in `src/api/src/zava_forward/api/web/` and their WCAG/DOM tests in `src/api/tests/`, plus verification of any `workbench.py` / `scenario-manifest.json` / conformance invariants.
* Assumptions: Verify whether Asset Executive and Board views live in `role-screens.js`, `index.html`, `app.js`, or multiple files, and verify what `test_asset_exec_screen_wcag.py` already covers.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and a single recommendation is selected.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Inspect PR #1715 (`#225`), add equivalent WCAG 2.2 keyboard jump navigation and explicit textual state labels to Asset Executive and Board views, preserve `workbench.py` / `scenario-manifest.json` recipe SHA invariants, add focused unit/DOM tests without bulk `del sys.modules[...]`, validate with `mypy`, `ruff`, and `unittest`, and commit locally with `Refs #226`.
* Inferred research questions: How are Asset Executive and Board views rendered, routed, and tested today? Which badges/pills/states currently rely on colour or lack explicit textual state prefixes/labels? Which conformance guards restrict HTML tags, event handlers, or panel counts on read-only executive views?
* Caller constraints and non-goals: Research-only during `rpi-research`; no `del sys.modules[...]` bulk sweeps; do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                        | Source / checkpoint | Effect on active brief, evidence, or revalidation                          |
|----------------------------------------------------------|------------------------------------------------------------------------------|---------------------|----------------------------------------------------------------------------|
| narrow                                                   | Deliver WCAG 2.2 keyboard jump nav + textual state meaning for #226 views    | Caller brief        | Focuses investigation on Asset/Board screens and PR #1715 precedent        |
| exclude                                                  | Do NOT use bulk `del sys.modules[...]` in test files                         | Caller brief        | Constrains test module import pattern to strict-mypy-safe loader           |
| exclude                                                  | Preserve `workbench.py` / `scenario-manifest.json` SHA invariants            | Caller brief        | Avoid unnecessary `workbench.py` edits unless required and synced          |

## Research Questions

|  # | Sub-question                                                                                                    | Type            | Priority | Status   |
|---:|-----------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | How did PR #1715 (`#225`) implement keyboard jump navigation, focus delegation, and textual state labels?       | straightforward | H        | answered |
| Q2 | Where and how are the Asset Executive and Board views (`asset` / `reviewer` / `executive`) rendered and styled? | depth           | H        | answered |
| Q3 | What WCAG 2.2 gaps exist on the Asset Executive and Board views compared to `test_asset_exec_screen_wcag.py` and PR #1715? | depth | H | answered |
| Q4 | What `RoleScreenConformance`, read-only guardrails, content-standard rules, and `workbench.py` / `scenario-manifest.json` invariants apply? | depth | H | answered |
| Q5 | How should unit/DOM tests be structured without bulk `del sys.modules[...]` while passing `mypy` and `ruff`?    | straightforward | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/design-system.md`, `docs/reference/research/ux/content-standard.md`, `docs/reference/research/ux/customer-journeys/asset.md`, `docs/reference/research/ux/customer-journeys/reviewer.md`, `docs/reference/research/ux/atlas-screen-trace.md`, `.copilot-tracking/rpi-sessions/2026-11-14/issue-225-c2-conformance-fix-state.json`.
* Reused (verified) findings: Issue #226 has 5 of 6 checkboxes ticked; only `Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation` remains unchecked (`asset.md` notes engineering checks do not establish AT/human conformance, so we use `Refs #226` rather than `Closes #226`). PR #1715 (`d6f863e34`) recently solved the sibling Finance screen WCAG slice (#225), and PR #1694 (`6a629153b`) added an initial partial slice on `asset-board` that left 3 panels un-anchored and several state fields/cells without explicit state prefixes.
* Superseded / stale: Any inline `onclick` jump-link pattern from earlier commits was superseded in `d6f863e34` by delegated `a[data-jump]` handling.

## Research Cycle Log

### Cycle 1

* Active direction controls: `narrow` (#226 WCAG 2.2 keyboard jump nav + textual state meaning), `exclude` (no bulk `del sys.modules[...]`), `exclude` (preserve `workbench.py` / `scenario-manifest.json` SHA invariants).
* Active research posture and completion basis: `focused`; focused scope and materiality.
* Explicit limits or deadline effect: Non-interactive run; commit locally without pushing.

#### Wave 1: Wider

* Plan and independent lanes: Survey UX/WCAG documentation (`atlas-screen-trace.md`, `wcag-conformance-baseline.md`, `design-system.md`, `content-standard.md`, `asset.md`, `reviewer.md`), web files (`role-screens.js`, `index.html`, `app.js`, `progress.js`, `style.css`), precedent PRs (`d6f863e34` #1715, `29c2e0755` #1716, `6a629153b` #1694), and manifest/workbench invariants (`workbench.py`, `scenario_manifest.py`, `scenario-manifest.json`).
* Worker evidence relationships or inline fallback: Inline investigation (`C1`, `C2`, `C3`, `C10`, `W1`) mapped Asset Executive and Board Pack Reader directly to `id: "asset-board"` (`Asset and board view`) in `role-screens.js` and confirmed `scenario_manifest.py` hashes `workbench-manifest.json`, `workbench_browser_check.py`, `dataset.py`, and `test_workbench.py`.
* Reflection: `asset-board` in `role-screens.js` is the canonical Asset Executive and Board view (`C1`, `C3`). PR #1694 (`6a629153b`) added `assetSummary` and a 7-link `assetJumpNav`, so Wave 2 needed a line-by-line audit of remaining WCAG 2.2 keyboard, landmark, target-size, focus-obscured, state-cue, and runtime test gaps against PR #1715 (`C2`).

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Compare `asset-board` (`role-screens.js:162-352`) and `style.css:371-377` against PR #1715 (`role-screens.js:20-32`, `test_finance_screens_wcag_225.py`) and PR #1716 (`role-screens.js:1337-1470`).
* Plan and independent lanes: Inspect every `screenPanel`, field row, table cell, jump link, CSS rule, and WCAG/DOM test for `asset-board`.
* Worker evidence relationships or inline fallback: Inline deep read (`C3`, `C4`, `C5`, `C6`, `C11`, `W1`) identified five concrete gaps:
  1. Three of the 10 `<section>` panels on `asset-board` (`Evidence boundary`, `Eligibility`, and `Ledger-wide AI usage, alerts and cost components (all homes, not this home)`) lack `{ anchor: ... }`, so they emit no `id`, no `aria-labelledby`, no focusable `<h2 tabindex="-1">`, and have no link in `assetJumpNav()` (`C3`, `C4`).
  2. `assetJumpNav()` lacks explicit `role="navigation"`, `data-jump-target` parity with PR #1715 `screenJumpNav`, and self-describing `Go to ${title}` link labels (`C2`, `C3`), while the delegated `a[data-jump]` handler calls `.focus()` without `.scrollIntoView?.({ block: "start" })` and `.screen-links a` / anchored headings in `style.css` lack comfortable target sizing (`min-height: 2.5rem`) and `scroll-margin-top` to avoid sticky-header focus obscuration (`WCAG 2.2 SC 2.4.11` & `SC 2.5.8`, `C5`, `W1`).
  3. Multiple status/state surfaces on `asset-board` still omit explicit textual state cues (`State: ...` or `stateCue(...)`): `Stock conflict comparison` `Status` column (`Unresolved` / `Reconciled ...` / `Withdrawn ...`), `Open stock conflicts by home` `Investment inputs` column (`Unknown. See missing investment inputs.`), `Eligibility` panel (`Eligibility` = `"Unknown"`, unlike PR #1715's `"State: Unknown. This page cannot confirm eligibility."`), `assetCost` (`Overall AI cost per accepted outcome`, `Quality floor`, `Value status`), and `assetUsage` (`Reconciliation with the bill`, `Total Cost of AI`) (`C3`).
  4. `test_asset_exec_screen_wcag.py` only performs a static substring check on `role-screens.js` for jump-link routing instead of a runtime Node VM delegated-click and keyboard-target focus/missing-target harness like `test_finance_screens_wcag_225.py`, and lacks tests for 10-of-10 landmark coverage, prototype-safe `stateCue` fallback, CSS target-size / `scroll-margin-top`, and strict-mypy-safe `importlib` loading (`C6`, `C11`).
* Reflection: Every identified improvement must be stress-tested in Wave 3 against browser/conformance harnesses (`connected_home_browser_check.py`, `specialist_keyboard_browser_check.py`, `test_content_standard.py`, `test_role_screens_conformance.py`, `test_asset_board_screen.py`) to avoid hidden regressions.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge candidate changes against (a) adding an unselected-home `overview()` method on `asset-board`, (b) switching `asset-board` from `{ anchor }` `<h2 tabindex="-1">` targets to `screenJumpTarget` `<div tabindex="-1">` wrappers, (c) changing `assetStatus(c, q)` directly, (d) introducing banned vocabulary from `test_content_standard.py`, and (e) modifying `assetCost` / `assetUsage` fields pinned by `test_asset_board_screen.py`.
* Plan and independent lanes: Inspect `roleScreensView()`, `connected_home_browser_check.py`, `test_connected_home_check.py`, `specialist_keyboard_browser_check.py`, `test_content_standard.py`, `test_role_screens_conformance.py`, and `test_asset_board_screen.py`.
* Worker evidence relationships or inline fallback: Inline contrarian audit (`C6`, `C7`, `C8`, `C9`, `C12`) disproved three risky approaches and confirmed exact safe boundaries:
  1. Disproved adding `overview()` on `asset-board`: `roleScreensView()` executes `screen.overview(...)` even when a home `c` is selected (`role-screens.js:123,157`), which would inject unindexed panels/tables and break both `connected_home_browser_check.py` (`C7`) and `specialist_keyboard_browser_check.py` (`EXPECTED_REGIONS["asset-board"]`, `C8`).
  2. Disproved replacing `{ anchor }` with `screenJumpTarget`: `test_asset_exec_screen_wcag.py:54-62` explicitly requires every `<nav>` link's `data-jump` attribute to match an `<h2 id="...-heading" tabindex="-1">` (`C6`), whereas `screenPanel(title, { anchor: id }, ...)` already sets `<section id="${id}" aria-labelledby="${id}-heading">` AND `<h2 id="${id}-heading" tabindex="-1">` (`C4`).
  3. Disproved mutating `assetStatus(c, q)` return strings directly: `role-screens.js:310` and `role-screens.js:724` (`technical-queue`) compare `assetStatus(c, q) === "Unresolved"` (`C3`). Wrapping the rendered table cell with `stateCue(assetConflictCues, assetStatus(c, q))` preserves `assetStatus(c, q)` callers AND satisfies `connected_home_browser_check.py:225,331` substring checks (`part in cell` for `RECONCILED` and `"Unresolved"`, `C7`).
  4. Confirmed `test_asset_board_screen.py` pins exact `dd` values on `Evidence class` (`"Unknown"`), `AI report` when loaded (`"Loaded"`), and integer count strings (`"5"`, `"3"`, `"12"`, `"Unknown"`) (`C12`), plus `test_content_standard.py` scans every line of `role-screens.js` (including anchor IDs and comments) for `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b` (`C9`), and `test_asset_exec_screen_wcag.py:63` checks the exact substring `"event.preventDefault();\n    document.getElementById"` (`C6`).
  5. Confirmed `PYTHONPATH` order when running `test_connected_home_check.py`: `tests` must precede `../core/tests` (or use `unittest discover -s tests`) because both `src/api/tests` and `src/core/tests` define `test_dependency_rule.py` (`C7`).
* Reflection: Contrarian evidence eliminated every potential regression while confirming a clean, complete WCAG 2.2 upgrade path across `role-screens.js`, `style.css`, and `src/api/tests/`.

#### Parent Synthesis and Disposition

| Material / claim                                                                                      | Evidence IDs      | Parent disposition | Evidence-based rationale                                                                                              | Primary-artifact treatment          |
|-------------------------------------------------------------------------------------------------------|-------------------|--------------------|-----------------------------------------------------------------------------------------------------------------------|-------------------------------------|
| Anchor all 10 `asset-board` `screenPanel` sections via `{ anchor }` and expose all 10 in `assetJumpNav` | C2, C3, C4, C6, C7| accepted           | Gives 100% of `asset-board` sections `aria-labelledby`, focusable `h2[tabindex="-1"]`, and keyboard jump links safely | Selected Recommendation             |
| Add `role="navigation"`, `data-jump-target`, `Go to ${title}` labels, and optional `scrollIntoView`   | C2, C3, C6, W1    | accepted           | Aligns `assetJumpNav` with PR #1715 `screenJumpNav` and WCAG 2.4.1 / 2.4.4 while keeping `test_asset_exec_screen_wcag`| Selected Recommendation             |
| Add explicit textual state labels (`assetState` / `stateCue`) to conflict, queue, eligibility, AI rows | C2, C3, C7, C12   | accepted           | Eliminates bare status/unknown cells without breaking `assetStatus` callers, `RECONCILED` substring, or pinned `dd`s  | Selected Recommendation             |
| Add `.screen-links a` min target height (`2.5rem`) and `scroll-margin-top` on anchored headings/panels | C5, C9, W1        | accepted           | Satisfies WCAG 2.2 SC 2.5.8 Target Size & SC 2.4.11 Focus Not Obscured under sticky `.top` header with zero motion    | Selected Recommendation             |
| Add runtime Node VM delegated-click + DOM/ARIA/state-cue tests without bulk `del sys.modules[...]`    | C6, C11           | accepted           | Matches PR #1715 `test_finance_screens_wcag_225.py` strict-mypy-safe pattern and caller constraint                    | Selected Recommendation             |
| Add `overview()` on `asset-board` or switch to `screenJumpTarget` `<div>` wrappers                    | C4, C6, C7, C8    | rejected           | Would break `connected_home_browser_check.py`, `EXPECTED_REGIONS["asset-board"]`, and `h2` target assertions          | Rejected Alternatives               |
| Modify `workbench.py` or `scenario-manifest.json`                                                     | C10               | rejected           | Not needed; `asset-board` routes and SHA-pinned recipe files require zero changes                                     | Current Decisions                   |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Focused scope covered; all 5 research questions answered with direct codebase (`C1`-`C12`) and external guideline (`W1`) evidence, and Wave 3 contrarian checks verified every invariant.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: bounded single-component investigation across `src/api/src/zava_forward/api/web/` and `src/api/tests/` where every finding is tightly coupled to regex/AST conformance tests in the same package.

### Codebase Evidence

| ID  | Claim / finding                                                                                                                   | Location (`path:line`)                                                    | Tool | Confidence | Notes                                                                                  |
|-----|-----------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------|------|------------|----------------------------------------------------------------------------------------|
| C1  | `asset-board` (`Asset and board view`) is the canonical role screen for Asset Executive and Board Pack Reader (`#226`).           | `docs/reference/research/ux/atlas-screen-trace.md:27`                     | view | high       | Confirmed alongside `customer-journeys/asset.md:1` and `reviewer.md:1`                 |
| C2  | PR #1715 (`#225`) added `screenJumpNav` (`Go to ${text}`, `data-jump`, `data-jump-target`) and `State: ...` / `stateCue` labels. | `src/api/src/zava_forward/api/web/role-screens.js:29`                     | bash | high       | Verified via `git show d6f863e34` and `git show 29c2e0755` (#1716)                     |
| C3  | `asset-board` renders 10 `screenPanel` sections, 3 un-anchored (`Evidence boundary`, `Eligibility`, `Ledger-wide AI usage...`), and `assetStatus` is shared with `technical-queue`. | `src/api/src/zava_forward/api/web/role-screens.js:178` | view | high | Also covers lines `201-351` and `724` (`assetStatus(c, q) === "Unresolved"`)          |
| C4  | `screenPanel(title, { anchor: id }, ...)` emits `<section id="${id}" aria-labelledby="${id}-heading">` and `<h2 id="${id}-heading" tabindex="-1">`, and `stateCue` uses `Object.prototype.hasOwnProperty.call`. | `src/api/src/zava_forward/api/web/role-screens.js:21` | view | high | Also `role-screens.js:421` (`stateCue`)                                               |
| C5  | `.top` is `position: sticky; top: 0; z-index: 1000`, while `.screen-links a` lacks `min-height: 2.5rem` padding and `.screen-record` / `[tabindex="-1"]` lack `scroll-margin-top`. | `src/api/src/zava_forward/api/web/style.css:371` | view | high | `.screen-*` styles must contain no `animation` or `transition`                        |
| C6  | `test_asset_exec_screen_wcag.py` requires `<nav>` `a[data-jump]` targets to be `<h2 id="..." tabindex="-1">` and checks `"event.preventDefault();\n    document.getElementById"`. | `src/api/tests/test_asset_exec_screen_wcag.py:42` | view | high | Lines `42-65` and `84-93`                                                             |
| C7  | `connected_home_browser_check.py` audits exact `screenPanel("...")` titles on `asset-board` and checks `Stock conflict comparison` rows via substring containment (`part in cell`). | `src/api/checks/connected_home_browser_check.py:224` | view | high | Also `331`, `388`, `424-446`, and `src/api/tests/test_connected_home_check.py:194-224`|
| C8  | `specialist_keyboard_browser_check.py` pins `EXPECTED_REGIONS["asset-board"] = ("Investment inputs", "Phase checks and benefits", "Portfolio summary in words")`. | `src/api/checks/specialist_keyboard_browser_check.py:46` | view | high | Adding tables to default fixture render would fail the keyboard walk                   |
| C9  | `CopyAudit` rejects `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b` on any line of `role-screens.js`, and `RoleScreenConformance` requires every class in `role-screens.js` to exist in `style.css` with no motion. | `src/api/tests/test_content_standard.py:15` | view | high | Also `src/api/tests/test_role_screens_conformance.py:62-160`                          |
| C10 | `scenario-manifest.json` recipe SHA hashes only `workbench-manifest.json`, `workbench_browser_check.py`, `dataset.py`, and `test_workbench.py`; `workbench.py` needs no edit. | `src/core/src/zava_forward/core/scenario_manifest.py:20` | view | high | Leaving `workbench.py` and those 4 files untouched preserves SHA invariants           |
| C11 | `test_finance_screens_wcag_225.py` demonstrates strict-mypy-safe sibling test module import via `if TYPE_CHECKING: ... else: importlib.import_module(...)` and Node VM delegated-click verification without `del sys.modules[...]`. | `src/api/tests/test_finance_screens_wcag_225.py:12` | view | high | Directly satisfies caller's no-bulk-`del sys.modules[...]` constraint                 |
| C12 | `test_asset_board_screen.py` pins no `<button>/<form>/<input>/<select>/<textarea>`, no `<h1>/<h3>`, exact `dd` `"Unknown"` for `Evidence class`, `"Loaded"` when AI report has `consumption`, and exact usage count strings. | `src/api/tests/test_asset_board_screen.py:92` | view | high | Also lines `154-170`, `228-230`, `289-293`, and `346-352`                             |

### External Evidence

| ID | Claim / finding                                                                                                                  | Source (title)                         | URL                                                                                       | Retrieved  | Version/date | Confidence |
|----|----------------------------------------------------------------------------------------------------------------------------------|----------------------------------------|-------------------------------------------------------------------------------------------|------------|--------------|------------|
| W1 | Heading anchors require `scroll-margin-top`, sticky headers must not cover focused elements, `:focus-visible` must remain visible, and links need descriptive names. | Vercel Web Interface Guidelines (`command.md`) | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | 2026-11-14 | main         | high       |

### Contradictions / Conflicts

* `redesign-existing-projects` generic advice suggests smooth transitions (`200-300ms`) and font swaps, whereas repository instructions and `RoleScreenConformance.test_screen_styles_add_no_motion` (`C9`) forbid motion on `.screen-*` rules and mandate preserving Fluent 2 tokens (`#150`); resolved by extension precedence -> repository instructions and enforced conformance tests take strict priority over generic skill suggestions.

## Findings Mapped to Questions and Evidence

| Question | Finding                                                                                                                                                                     | Evidence IDs       | Confidence | Decision or readiness implication                                                     |
|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|------------|---------------------------------------------------------------------------------------|
| Q1       | PR #1715 (`#225`) uses `<nav>` with `aria-label`, `Go to ...` links carrying `href`, `data-jump`, and `data-jump-target`, delegated `a[data-jump]` focus handling, and explicit `State: ...` / `stateCue` text prefixes tested via Node VM DOM simulation. | C2, C4, C11 | high | Mirror `Go to ...`, `data-jump-target`, `stateCue` / `assetState`, and Node VM click tests while preserving `asset-board` `<h2 tabindex="-1">` targets. |
| Q2       | Asset Executive and Board Pack Reader views are rendered by `id: "asset-board"` (`Asset and board view`) in `role-screens.js` inside the `#/screens?screen=asset-board` shell and styled by `style.css`. | C1, C3, C5 | high | Scope production edits to `role-screens.js` and `style.css` only.                     |
| Q3       | `asset-board` leaves 3 of 10 panels un-anchored (`Evidence boundary`, `Eligibility`, `Ledger-wide AI usage...`), lacks `role="navigation"`, `data-jump-target`, `Go to ...` link text, `.screen-links a` min target size, heading `scroll-margin-top`, explicit state prefixes on conflict/queue/eligibility/AI state rows, and runtime delegated-click tests. | C3, C5, C6, W1 | high | Close all 5 gaps cleanly in `role-screens.js`, `style.css`, and `src/api/tests/`.     |
| Q4       | Keep all 10 literal `screenPanel("...")` titles unchanged, keep `assetStatus(c, q)` return values intact for callers, avoid banned copy-audit words, add zero `<button>/<form>/<input>` or extra default tables, add zero CSS motion, and leave `workbench.py` / `scenario-manifest.json` untouched. | C3, C7, C8, C9, C10, C12 | high | Zero invariant or SHA drift; all existing conformance and connected-home checks pass. |
| Q5       | Use `if TYPE_CHECKING:` + `importlib.import_module` (no bulk `del sys.modules[...]`) in a dedicated `test_ux_asset_executive_screens.py` (and extend `test_asset_exec_screen_wcag.py`) verified under `mypy`, `ruff`, and `unittest`. | C6, C11 | high | Satisfies strict `mypy`, `ruff`, `unittest`, and caller constraints.                  |

## Key Discoveries

* Anchor completeness: Adding `{ anchor: "asset-boundary" }`, `{ anchor: "asset-eligibility" }`, and `{ anchor: "asset-usage" }` and listing all 10 sections in `assetSections` upgrades every `<section>` on `asset-board` to an `aria-labelledby` landmark with a focusable `<h2 id="...-heading" tabindex="-1">` and a matching keyboard jump link (`C3`, `C4`, `C6`, `C7`).
* Non-breaking state cues: Wrapping the `Stock conflict comparison` status cell in `stateCue(assetConflictCues, assetStatus(c, q))` yields `"Action needed: Unresolved"`, `"Recorded: Reconciled (recorded by a named person)"`, and `"Withdrawn: Withdrawn (recorded by a named person)"` with prototype-safe fallback (`"Action needed: <value>"`), while preserving `assetStatus(c, q) === "Unresolved"` callers in `asset-board` and `technical-queue` (`C3`, `C4`) and `connected_home_browser_check.py` substring checks (`C7`).
* WCAG 2.2 focus & target-size polish: Adding `min-height: 2.5rem; display: inline-flex; align-items: center; padding: var(--sp-1) var(--sp-2);` on `.screen-links a` and `scroll-margin-top: 4.5rem;` on `.screen-record[id], .screen-evidence h2[tabindex="-1"]` satisfies WCAG 2.2 SC 2.5.8 Target Size (Minimum) and SC 2.4.11 Focus Not Obscured (Minimum) under the sticky `.top` bar without introducing motion (`C5`, `C9`, `W1`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Complete WCAG 2.2 keyboard jump navigation and explicit textual state labels on `asset-board` in `src/api/src/zava_forward/api/web/role-screens.js` and `style.css`, backed by runtime Node VM delegated-click, landmark, ARIA, CSS, and textual-state unit/DOM tests in `src/api/tests/test_ux_asset_executive_screens.py` and `src/api/tests/test_asset_exec_screen_wcag.py` (with zero `workbench.py` or `scenario-manifest.json` changes and zero `del sys.modules[...]`).
* Rationale: Delivers 10-of-10 landmark and jump-link coverage, explicit `role="navigation"` + `aria-label` + `Go to ...` links + `data-jump`/`data-jump-target` + `scrollIntoView`, explicit `State: ...` / `stateCue(...)` non-colour state labels across every status cell and field, and WCAG 2.2 SC 2.4.11 / SC 2.5.8 CSS ergonomics while preserving every existing `connected_home_browser_check`, `specialist_keyboard_browser_check`, `CopyAudit`, and `RoleScreenConformance` contract.
* Evidence refs: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, W1
* Implementation impact: `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/style.css`, `src/api/tests/test_asset_exec_screen_wcag.py`, `src/api/tests/test_ux_asset_executive_screens.py`.
* Confidence: high: all callers, browser check manifests, and conformance assertions were directly inspected and run.

File tree:

```text
src/api/
├── src/zava_forward/api/web/
│   ├── role-screens.js          (modify: 10-section jump nav, role="navigation", data-jump-target, scrollIntoView, stateCue/assetState labels)
│   └── style.css                (modify: .screen-links a target sizing + scroll-margin-top on anchored sections/headings)
└── tests/
    ├── test_asset_exec_screen_wcag.py        (modify: verify 10-of-10 anchored landmarks, role="navigation", textual states)
    └── test_ux_asset_executive_screens.py    (create: Node VM delegated jump-click, missing-target safety, stateCue prototype safety, CSS target/scroll-margin checks)
```

### Alternative: Switch `asset-board` panels to `screenJumpTarget` `<div tabindex="-1">` wrappers

* Approach: Wrap `asset-board` panels in `screenJumpTarget(id, screenPanel(...))` like PR #1715 did for `finance-invoices` and `finance-funding`.
* Trade-offs: Reuses `screenJumpTarget` verbatim, but targets outer `<div>` nodes rather than `<section aria-labelledby>` + `<h2 tabindex="-1">`.
* Evidence refs: C2, C4, C6
* Rejection rationale: Directly breaks `test_asset_exec_screen_wcag.py:54-62` (`C6`), which asserts every `nav a[data-jump]` targets an `<h2 id="..." tabindex="-1">`, and loses `screenPanel`'s automatic `<section aria-labelledby="${id}-heading">` landmark binding (`C4`).

### Alternative: Add an unselected-home `overview()` summary panel to `asset-board`

* Approach: Implement `overview(signal, items, c, page)` on `asset-board` to render portfolio tables before a home is selected.
* Trade-offs: Shows portfolio data before selecting a case, but `roleScreensView()` renders `overview` above `selected` even when a case `c` is selected (`role-screens.js:123,157`).
* Evidence refs: C3, C7, C8
* Rejection rationale: Injects extra panels and tables during selected-home rendering, breaking `connected_home_browser_check.py` panel audits (`C7`) and `specialist_keyboard_browser_check.py` `EXPECTED_REGIONS["asset-board"]` (`C8`).

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Automated DOM and unit checks verify engineering baseline criteria only; human assistive-technology walkthroughs (`#151`, `#155`) remain separate acceptance evidence, so the commit must reference `Refs #226` and never `Closes #226`.
* Follow-up: none
* Residual uncertainty: none within local engineering scope.

## Current Decisions

| Decision                                                                                  | Status    | Owner / source    | Rationale                                                                                   | Evidence IDs       | Implications                                                               |
|-------------------------------------------------------------------------------------------|-----------|-------------------|---------------------------------------------------------------------------------------------|--------------------|----------------------------------------------------------------------------|
| Target `asset-board` in `role-screens.js` + `style.css` without touching `workbench.py`   | confirmed | evidence / caller | `asset-board` owns Asset Executive & Board views; leaving `workbench.py` untouched keeps SHA | C1, C3, C5, C10    | Minimal blast radius and guaranteed `scenario-manifest.json` SHA stability |
| Anchor all 10 `screenPanel` sections with `{ anchor }` and keep `<h2 tabindex="-1">` IDs  | confirmed | evidence          | Preserves `test_asset_exec_screen_wcag.py` and gives all 10 sections `aria-labelledby`      | C3, C4, C6, C7     | Every panel on `asset-board` is landmark-named and jump-reachable          |
| Format status cells/fields with `stateCue` and `assetState` without altering `assetStatus`| confirmed | evidence          | Protects `assetStatus(c, q) === "Unresolved"` in `asset-board` and `technical-queue`        | C3, C4, C7, C12    | Explicit textual state meaning with zero cross-screen or test regressions  |
| Use `TYPE_CHECKING` + `importlib.import_module` in new tests (no `del sys.modules[...]`)  | confirmed | caller / evidence | Caller forbids bulk `del sys.modules[...]`; PR #1715 pattern passes strict `mypy` and `ruff`| C11                | Clean static typing and isolated test discovery                            |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| none     | none                               | none  | none   | none           |

## Potential Next Research

| Priority | Research item                                                  | Expected value                                              | Trigger                                    | Selected? | Related questions / evidence |
|----------|----------------------------------------------------------------|-------------------------------------------------------------|--------------------------------------------|-----------|------------------------------|
| L        | Live assistive-technology walkthrough for `#151` / `#155`      | Human screen-reader confirmation beyond DOM checks          | Separate human validation issue `#155`     | deferred  | Q3; C1, C6                   |

## Planning Readiness

* Status: Ready
* Decision state: Converged on `role-screens.js` + `style.css` + `test_asset_exec_screen_wcag.py` + `test_ux_asset_executive_screens.py` implementation plan.
* Evidence basis: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, W1
* Preconditions met: All 5 research questions answered; all three waves completed; conformance, copy-audit, connected-home, keyboard-region, and recipe SHA invariants verified.
* Blockers: none
* Smallest action to change readiness: none (already Ready)

## Closeout Record

| Field                            | Record                                                                                     |
|----------------------------------|--------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                   |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian                                                     |
| Lane evidence or inline fallback | Inline investigation across `src/api/` and `docs/reference/research/ux/`                   |
| Research disposition             | executed                                                                                   |
| Planning Readiness               | Ready (C1-C12, W1)                                                                         |
| Blockers                         | none                                                                                       |
| Continuation owner and state     | Confirmed automatic RPI Agent; automatic continuation to `Plan` (`rpi-plan`)               |

## Advisory Next Step

| Field                            | Record                                                                                     |
|----------------------------------|--------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                   |
| Planning Readiness               | Ready (C1-C12, W1)                                                                         |
| Output mode and planning support | convergence; yes, single evidence-backed approach selected                                 |
| Acting owner                     | confirmed automatic RPI Agent                                                              |
| Required gates or confirmations  | Research disposition recorded (passed); Planning Readiness Ready (passed); state persisted |
| Continuation result              | automatic continuation to `rpi-plan`                                                       |
| Primary evidence file            | .copilot-tracking/research/2026-11-14/ux-226-asset-exec-wcag-2358-research.md              |
| Notes for planning or re-entry   | Preserve exact `screenPanel` titles, `assetStatus` return contract, pinned `dd` values, copy-audit rules, and `tests`-first `PYTHONPATH` |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All in-scope files, precedents, and contrarian regression vectors were directly inspected; additional cycles would be redundant.

## Sources

* W1 - Vercel Web Interface Guidelines (`command.md`) - https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-11-14, main)

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
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings Mapped to Questions, Key Discoveries, Alternatives and Decision State, Open Questions, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check.
* Missing or limited sections: none

