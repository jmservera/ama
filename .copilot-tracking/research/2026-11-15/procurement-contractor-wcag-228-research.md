<!-- markdownlint-disable-file -->

# Task Research: procurement-contractor-wcag-228

| Field              | Value                                                                                      |
|--------------------|--------------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                                 |
| Researcher / agent | rpi-research (RPI Agent automatic mode)                                                    |
| Status             | Complete                                                                                   |
| Artifact path      | .copilot-tracking/research/2026-11-15/procurement-contractor-wcag-228-research.md          |

## Research Brief

* What to research: Current DOM structure, landmark semantics, keyboard jump navigation, heading focus targets, status badges/state cues, contractor vulnerability redaction, CSS classes, and conformance tests for the Procurement and Contracts Manager (`#/role/procurement`) and staff-facing Contractor (`#/role/contractor`) screens in `src/api`, compared against sibling WCAG 2.2 role-screen implementations (such as `#1715` for `#225`).
* Why it matters: Issue `#228` has 5 of 6 acceptance criteria satisfied; delivering a complete, surgical engineering slice for the remaining code-testable criterion (`Accessible per the WCAG 2.2 baseline (#151) with textual state meaning and keyboard navigation`) requires aligning with existing `role-screens.js`, `app.js`, `style.css`, design-system, WCAG baseline, and plain-language content-standard contracts without regressing contractor redaction or existing role conformance tests.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` phases of the automatic RPI session for `#228`.
* Scope: `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/style.css` (read/verify `.ux-state-cue` and jump-nav styling), `src/api/tests/test_procurement_contractor_screen_wcag.py`, `src/api/tests/test_role_screens_conformance.py`, sibling role-screen WCAG tests, and UX reference documentation (`docs/reference/research/ux/`).
* Non-goals: Provider portal, external contractor identity, self-approval, booking workflows, exposing vulnerability reasons in contractor views, visual aesthetic overhauls, framework swaps, pushing to remote, or claiming human/screen-reader accessibility conformance (`#155` / `#151` manual checks remain separate).
* Criteria: Every section landmark on `#/role/procurement` and `#/role/contractor` is reachable via keyboard jump navigation (`role="navigation"`, `aria-label`, `Go to ...` links) with delegated focus movement to target section headings (`tabindex="-1"`); package queue rows, draft readiness cards, unmet prerequisite badges, contractor job pack submission/acknowledgement items, and independent review status badges pair visual styling with explicit plain-language textual state cues while preserving contractor vulnerability-reason redaction; focused unit tests verify these invariants without `sys.modules` deletion hazards.
* Requested outputs: Synthesized evidence log, comparison against established sibling role-screen WCAG patterns, converged implementation recommendation, and planning readiness assessment.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                                                   |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | How are `#/role/procurement` and `#/role/contractor` currently rendered and wired in `role-screens.js`/`app.js`/`style.css`, what exact WCAG jump-nav and `.ux-state-cue` patterns do sibling screens use, and how should focused tests assert them cleanly? |
| Codebase scope                   | `src/api/src/zava_forward/api/web/`, `src/api/tests/`, `docs/reference/research/ux/`                                                                                    |
| External scope                   | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` (required by repository Web Development Guidance)                              |
| Initial internal candidate areas | `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/web/style.css`, `src/api/tests/test_role_screens_conformance.py`, commit `d6f863e34` |
| Initial external candidate areas | Vercel Web Interface Guidelines (`command.md`) and W3C WCAG 2.2 baseline synthesis in `docs/reference/research/ux/wcag-conformance-baseline.md`                         |
| Research posture                 | focused                                                                                                                                                                 |
| Posture provenance               | caller-specified bounded scope with named source targets (`role-screens.js`, `app.js`, `test_procurement_contractor_screen_wcag.py`) and focused validation tier        |
| Explicit limits / deadline       | Focused increment in `src/api`; dated artifacts under `.copilot-tracking/*/2026-11-15/`; do not push                                                                    |
| Posture-specific completion basis| focused scope and materiality: all target components, sibling patterns, test harnesses, and regression guards inspected across Wider, Deeper, and Contrarian waves      |
| Edits allowed during research?   | no, research-only                                                                                                                                                       |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                                                    |
| Known constraints / excluded sources | Preserve Fluent 2 tokens, WCAG 2.2 baseline (`#151`), plain-language content standard (`#153`), contractor vulnerability redaction, and no `sys.modules` deletion hazards |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                      | Match and provenance                                                        | Scoped authority or output contract                                              | Selected / skipped reason                                                                 |
|---------------------|------------------------------------------------|-----------------------------------------------------------------------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`              | `applyTo: "**"` matches repository and `.copilot-tracking/` paths           | Enforces UX/WCAG/content-standard rules, validation tiers, and commit discipline | Selected: mandatory repository governance                                                 |
| Skill               | `rpi-research`                                 | Invoked for Research phase of requested RPI loop                            | Owns three-wave research artifact and readiness handoff                          | Selected: active phase skill                                                              |
| Skill               | `web-design-guidelines`                        | Required by Web Development Guidance before web edits and reviews           | Fetches current Web Interface Guidelines rules (`command.md`)                    | Selected: loaded and source fetched at intake                                             |
| Skill               | `redesign-existing-projects`                   | Referenced by Web Development Guidance for existing-app UI improvements     | Scoped subordinate to Fluent 2, WCAG baseline, and plain-language standard       | Selected: loaded for interaction/focus/semantic checks without overriding Fluent 2        |
| Skill               | `accessibility`                                | Matches WCAG 2.2 keyboard navigation and non-colour textual state cues      | Supplies WCAG 2.2 criterion mapping (1.3.1, 1.4.1, 2.1.1, 2.4.1, 2.4.3, 2.4.6)   | Selected: loaded at intake for normative criterion grounding                              |
| Research specialist | `hve-core-all:rpi-researcher`                  | Host-registered subagent for independent research lanes                     | Bounded lane artifact under `.copilot-tracking/research/subagents/`              | Skipped (inline): tightly coupled 3-file JS/CSS/test target fits direct inline waves      |
| Research specialist | `Housing Procurement and Contracts Lead`       | Domain persona agent in `.github/agents/`                                   | Domain hypothesis exploration anchored to case study                             | Skipped: issue `#228` UX requirements are already codified in PRD/journey docs and code   |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                     | Answers / unanswered      | Resulting decision or selected further research                                           |
|------------------|---------------------------------------------------------------------------------------------------------------------------|---------------------------|-------------------------------------------------------------------------------------------|
| Intake           | Non-interactive session with explicit caller scope, target files, acceptance criteria, validation commands, and commit rules | Not applicable (autonomous) | Proceed in `focused` posture under `convergence` output mode                              |
| Direction change | No scope boundary crossed during Cycle 1                                                                                  | Not applicable            | Retained `focused` posture inside `src/api`                                               |
| Convergence      | All four research questions answered with direct codebase and external guideline evidence (`C1`-`C18`, `W1`)              | Not applicable            | Converged on reusing documented Fluent 2 status classes + explicit state labels + jump nav |

## Scope and Success Criteria

* Scope: Inspect `role-screens.js`, `app.js`, `style.css`, existing WCAG/content/conformance tests in `src/api/tests/`, and supplier journey docs to determine the exact DOM, event-delegation, state-cue, redaction, and test requirements for `#/role/procurement` and `#/role/contractor`.
* Assumptions:
  * Sibling role screens (such as finance `#225` in commit `d6f863e34`) already established reusable CSS classes (`.ux-state-cue`, jump-nav styling) and JS helpers for keyboard jump navigation and textual state labels that should be reused rather than duplicated.
  * Existing conformance tests (`test_role_screens_conformance.py`, `test_content_standard.py`, `test_accessibility_baseline.py`) enforce strict invariants on tables, banned vocabulary, fixed positioning, or `aria-invalid` counts that any markup changes must preserve.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  * Expose keyboard-operable section jump navigation (`role="navigation"`, `aria-label`) with `Go to ...` links for all section landmarks on Procurement and Contracts Manager (`#/role/procurement`) and staff-facing Contractor (`#/role/contractor`) screens, wiring delegated focus movement to target section headings (`tabindex="-1"`).
  * Pair visual styling on package queue rows, draft readiness cards, unmet prerequisite badges, contractor job pack submission/acknowledgement items, and independent review status badges with explicit plain-language textual state cues (`.ux-state-cue` or explicit textual state labels) while preserving contractor vulnerability-reason redaction.
  * Add or extend focused unit tests in `src/api/tests/test_procurement_contractor_screen_wcag.py` (without `sys.modules` deletion hazards).
* Inferred research questions:
  * What helper functions and event handlers already implement jump navigation and `.ux-state-cue` in `role-screens.js`, `panels.js`, or `app.js`?
  * What exact sections, headings, rows, cards, and badges are rendered on `#/role/procurement` and `#/role/contractor` today, and how is contractor vulnerability redaction implemented and tested?
  * Are any static regex counters in `test_accessibility_baseline.py` or `test_content_standard.py` sensitive to edits in `role-screens.js` and `app.js`?
* Caller constraints and non-goals: Keep changes focused in `src/api`, preserve existing design-system and content-standard rules, avoid `sys.modules` deletion hazards in tests, and do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                                  |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------------------------|
| narrow                                                   | Deliver focused local-testable increment in `src/api` on `feat/ux-228-procurement-wcag` without pushing | Caller intake       | Restricts implementation target to `src/api` web assets and unit tests             |
| exclude                                                  | Preserve contractor vulnerability-reason redaction; avoid `sys.modules` deletion hazards in tests       | Caller intake       | Constrains state-cue wording and test-import patterns across all three waves       |

## Research Questions

|  # | Sub-question                                                                                                                     | Type (depth / breadth / straightforward) | Priority | Status |
|---:|----------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|--------|
| Q1 | What reusable jump-navigation, heading-focus, and `.ux-state-cue` patterns already exist across `src/api` web assets and commit `d6f863e34`? | breadth                                  | H        | answered |
| Q2 | What exact section landmarks, headings, package queue rows, readiness cards, prerequisite badges, contractor submission/ack items, and review status badges exist in `#/role/procurement` and `#/role/contractor`? | depth                                    | H        | answered |
| Q3 | How is contractor vulnerability-reason redaction enforced, and what cross-cutting static/conformance test invariants (`test_accessibility_baseline.py`, `test_content_standard.py`, `test_role_screens_conformance.py`) constrain edits in `role-screens.js` and `app.js`? | depth                                    | H        | answered |
| Q4 | How are sibling `test_*_wcag.py` tests structured in `src/api/tests/` to test JS/HTML/API behavior cleanly without `sys.modules` deletion hazards or external browser dependencies? | straightforward                          | H        | answered |

## Cycle 1

### Wave 1: Wider

* Execution mode: inline (`focused` posture; tightly coupled `src/api` web assets and test harnesses inspected directly).
* Breadth findings:
  * Sibling WCAG 2.2 role-screen commit `d6f863e34` (`#1715` for `#225`) introduced `screenJumpNav(sections, label)` (`C1`), `stateCue(labels, raw, fallback)` (`C1`), `screenCapacityState(cap)` (`C1`), and `screenExpiryState(dateStr)` (`C1`) in `role-screens.js`, plus a delegated `document.addEventListener("click", ...)` handler for `a[data-jump]` (`C3`).
  * Earlier partial slice `29c2e0755` (`#1716` for `#228`) added `procurementJumpNav` (`C4`), `workOrderCues`, and `evidenceCues`, alongside `test_procurement_screen_wcag.py` (`C13`) and `test_procurement_qa_screen_wcag.py` (`C14`), but left concrete gaps against the `#228` WCAG 2.2 contract across both `role-screens.js` and `app.js`.
  * Repository-wide search confirmed `.ux-state-cue` does not exist in `style.css` (`C8`) or `docs/reference/research/ux/design-system.md` (`C9`). Instead, the documented Fluent 2 component inventory uses `.flag`, `.flag.danger`, `.status-line`, `.ok`, `.wait`, and `.danger` paired with CSS `:before` non-colour glyphs (`\26A0`, `\23F3`, `\2713`) and plain-language state text (`C8`, `C9`).
  * Fetched Vercel Web Interface Guidelines (`W1`) reinforce visible `:focus-visible` rings, semantic `<nav>` and `<a href>` navigation, landmark heading hierarchy, and non-colour status meaning.

### Wave 2: Deeper

* Execution mode: inline.
* Detailed gap analysis across Procurement and Contractor surfaces:
  1. **Jump navigation markup and section landmark coverage in `role-screens.js`**:
     * `procurementJumpNav` (`C4`) currently renders `<nav aria-label="Sections of this view" class="screen-links">` without explicit `role: "navigation"`, without `data-jump-target`, and with bare section titles rather than `Go to ...` link text (unlike `screenJumpNav` at `C1`).
     * On `procurement-packages` (`C5`), four `<section>` panels lack `{ anchor: ... }` (`"Evidence boundary"`, `screenTension("choice")`, `"Contractor submission and review"`, and `screenWithheld([...])`), leaving them without `id`, `aria-labelledby`, `<h2 tabindex="-1">` focus targets, and jump links.
     * On `contractor-job-pack` (`C6`), `screenWithheld([...])` lacks an anchor, leaving `"Not shown for this role"` out of the jump navigation and without a focusable `<h2 tabindex="-1">` target.
     * `screenWithheld` and `screenTension` (`C1`) currently do not accept an optional anchor argument.
  2. **Route aliases (`#/role/procurement`, `#/role/contractor`), staff-facing Contractor views, and focus delegation in `app.js` / `ops.js`**:
     * `app.js` currently dispatches `roleScreensView()` only when `hash.split("?")[0] === "#/screens"` (`C7`), so direct navigation to `#/role/procurement` or `#/role/contractor` (named in the `#228` issue specification) falls through instead of loading `/role-screens.js` and resolving `procurement-packages` or `contractor-job-pack` (`C2`, `C7`).
     * `app.js` has no global `a[data-jump]` click delegation (`C7`), meaning jump links on staff-authenticated Contractor views (`#/` `contractorListView` and `#/case/:id` `contractorCaseView`, where `/role-screens.js` is not loaded) have no delegated focus movement unless `app.js` handles `a[data-jump]` directly and `role-screens.js` skips already-handled `event.defaultPrevented` clicks (`C3`, `C7`).
     * `contractorListView()` and `contractorCaseView(id)` in `app.js` (`C7`) plus `workOrdersCard(rows, mine)` in `ops.js` (`C10`) currently have no section jump navigation, lack `aria-labelledby` and `<h2 tabindex="-1">` focus targets on their `<section>` landmarks, and rely on `.ai` / `.flag` / `.status` styling with bare status/notice strings rather than explicit state cues.
  3. **Explicit textual state meaning and non-colour visual status signals across the five `#228` elements**:
     * `screenFields` (`C1`) and `screenTable` (`C1`) pass cell/field values through `screenValue(value)` (`String(value)`), which would serialize virtual/DOM badge nodes to `"[object Object]"` unless DOM/VNode objects (`value.nodeType || value.tag`) pass through untouched.
     * Package queue rows (`C5`) render raw strings for capacity headroom and `wording(cap.evidence_status)` without `.flag` / `.flag.danger` non-colour badge styling, and bare unrecognised `evidence_status` strings lack an explicit textual state prefix.
     * Draft readiness cards (`C5`) render `h("p", { role: "status" }, "Draft readiness only. This is not a release or approval.")` without `.status-line.wait` non-colour hourglass styling or an explicit `State:` prefix, and `"Named reviewer"` lacks an explicit state badge (`Action needed: Unassigned...`).
     * Unmet prerequisite cells (`C4`, `C5`), contractor submission/acknowledgement items (`C5`, `C6`), evidence checklist items (`C6`), and independent review status items (`C4`, `C5`, `C6`) render plain text without pairing `.flag` / `.flag.danger` visual badge styling (`\26A0` warning glyph on unmet/blocked/pending/unknown states) and explicit state cues (`data-state-cue` + plain-language prefix).
  4. **Contractor vulnerability-reason redaction**:
     * Both `contractor-job-pack` (`C6`) and `contractorListView`/`contractorCaseView` (`C7`) derive visit-notice state strictly from `Boolean(c.needs_notice)` and `c.named_contact`, never reading `vulnerability_reason`, `vulnerability_notes`, `household`, or work-order vulnerability fields (`C12`).

### Wave 3: Contrarian

* Execution mode: inline adversarial check of existing regression, static-analysis, and browser-harness contracts to uncover hidden failure modes before planning:
  1. **Design-system class-inventory guard (`C9`, `C15`, `C16`)**: `test_role_screens.py` (`test_role_screens_use_documented_design_system_classes`) and `test_design_system.py` assert `used_classes - documented_inventory_classes == set()`. Introducing an undocumented `.ux-state-cue` CSS class would fail those suites unless `docs/reference/research/ux/design-system.md` were also modified outside `src/api`. Reusing the documented `.flag`, `.flag.danger`, `.status-line`, and `.wait` classes alongside `data-state-cue` attributes and explicit plain-language textual prefixes satisfies Deliverable 2 (`(.ux-state-cue or explicit textual state labels)`) cleanly inside `src/api`.
  2. **Tension helper slice & call-count guard (`C17`)**: `test_role_screens_tensions_same_home.py` slices `role-screens.js` from `const screenTensionText` to `function screenTable(` and asserts none of `("aria-invalid", "style", "icon", "<svg", "simulat", "impersonat")` appear in that block and `len(re.findall(r"screenTension\(", SCREENS)) == 5`. Adding an optional second parameter `const screenTension = (kind, anchor) => ...` without adding extra `screenTension(` occurrences or banned substrings preserves both invariants.
  3. **Browser harness keyboard & text contracts (`C18`)**:
     * `checks/procurement_screens_browser_check.py` collects Tab-stop `aria-label` values (`[s["label"] for s in stops if s["label"]]`) and compares them to table-region labels. Putting `aria-label` on individual `<a>` jump links would break that list; keeping `aria-label` on `<nav role="navigation">` while using visible link text `Go to ${title}` on `<a>` satisfies WCAG 2.4.4 / 2.5.3 and keeps `s["label"]` empty on jump links.
     * `procurement_screens_browser_check.py` asserts `evidence.locator('[role="status"]').count() == 1` when one package is rendered (`0` when empty), exact substring `"Draft readiness only. This is not a release or approval."`, and `r.startswith("WO-0001 v1 | ... | Unknown. No independent review")` on record rows. Therefore no extra `role="status"` regions may be added inside `.screen-evidence`, `"State: Draft readiness only. This is not a release or approval."` must retain the exact trailing sentence, and `workOrderRecordRows` column 4 must retain `"Unknown. No independent review..."` as its leading text inside `.flag.danger`.
  4. **Static counters & lexical guards (`C11`, `C15`, `C16`)**:
     * `test_content_standard.py` (`C11`) forbids `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b` anywhere (including comments and identifiers) across all 19 web files.
     * `test_accessibility_baseline.py` (`C11`) enforces exact counts across `web/*.js`: `8` `aria-invalid` sites, `2` `position:fixed` rules, and `13` literal `h("table", {},` occurrences.
     * `test_role_screens.py` (`C15`) asserts literal substring `return await roleScreensView()` precedes `return await (m ? contractorCaseView` in `app.js`.
     * `test_safety_panel_ux.py` (`C17`) slices `app.js` up to literal `async function contractorListView`, and `test_safety_screen_wcag_keyboard.py` (`C17`) asserts zero top-level identifier overlap between `app.js` and `role-screens.js`.
     * `test_procurement_screen_wcag.py` (`C13`) asserts numeric `target["attrs"]["tabindex"] == -1` on `screenPanel` virtual nodes in `role-screens.js`.
  5. **Test isolation without `sys.modules` deletion hazards (`C14`)**: Sibling `test_finance_screens_wcag_225.py` demonstrates clean Node `vm` execution and Python `unittest` structure without mutating or deleting `sys.modules` entries.

### Cycle 1 Synthesis

* Accepted:
  * Upgrade `procurementJumpNav` (`role: "navigation"`, `aria-label`, `data-jump`, `data-jump-target`, `Go to ${title}` visible link text) and add anchors to all remaining `<section>` panels on `procurement-packages` and `contractor-job-pack` (`C1`, `C4`, `C5`, `C6`, `C18`).
  * Support `#/role/procurement` and `#/role/contractor` route aliases in `app.js` and `roleScreensView()`, add jump navigation + section landmarks + `<h2 tabindex="-1">` + explicit state cues to `contractorListView`/`contractorCaseView` (`app.js`) and `workOrdersCard` (`ops.js`), and wire delegated `a[data-jump]` focus movement in `app.js` with `event.defaultPrevented` deduplication in `role-screens.js` (`C2`, `C3`, `C7`, `C10`, `C15`).
  * Allow DOM/VNode values in `screenFields` and `screenTable` via a shared `screenCell` helper and pair `.flag` / `.flag.danger` / `.status-line.wait` non-colour visual styling with explicit plain-language state cues across all five Deliverable 2 surfaces while preserving every existing substring and contractor vulnerability-reason redaction (`C1`, `C4`-`C9`, `C12`, `C18`).
* Rejected:
  * Inventing a new `.ux-state-cue` CSS class in `style.css` — rejected because `test_role_screens.py` and `test_design_system.py` block any CSS class absent from `docs/reference/research/ux/design-system.md` (`C9`, `C15`).
  * Adding `aria-label` attributes onto individual `<a>` jump links — rejected because visible `Go to ${title}` text already provides the accessible name and `aria-label` on `<a>` would break `procurement_screens_browser_check.py`'s region-label Tab check (`C18`).
* Re-entry decision: Cycle 1 answered `Q1`-`Q4` completely with verified codebase (`C1`-`C18`) and external (`W1`) evidence; no second cycle is required.

## Evidence Log

| ID  | Kind     | Location / URL                                                                                                                   | Summary                                                                                                                               |
|-----|----------|----------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| C1  | codebase | `src/api/src/zava_forward/api/web/role-screens.js:15-69`                                                                         | `screenFields`, `screenPanel` (`tabindex: -1`), `screenJumpNav`, `screenWithheld`, `screenTension`, `screenTable`, `stateCue`, `screenCapacityState`, `screenExpiryState`. |
| C2  | codebase | `src/api/src/zava_forward/api/web/role-screens.js:88-120`                                                                        | `roleScreensView()` resolves the active screen from URL query parameters and checks `s.roles.includes(me.user.role)`.                  |
| C3  | codebase | `src/api/src/zava_forward/api/web/role-screens.js:268-275`                                                                       | Document click listener delegating `a[data-jump]` focus to `document.getElementById(link.getAttribute("data-jump"))?.focus()`.        |
| C4  | codebase | `src/api/src/zava_forward/api/web/role-screens.js:1340-1378`                                                                     | `procurementJumpNav`, `workOrderCues`, `evidenceCues`, `workOrderRecordRows`, and `packagePrerequisites`.                              |
| C5  | codebase | `src/api/src/zava_forward/api/web/role-screens.js:1379-1435`                                                                     | `procurement-packages` screen definition, landmarks, package queue, expiry, work orders, record rows, draft readiness, and withheld list. |
| C6  | codebase | `src/api/src/zava_forward/api/web/role-screens.js:1437-1480`                                                                     | `contractor-job-pack` screen definition, landmarks, work orders, notice redaction, evidence checklist, submission/review, and withheld list. |
| C7  | codebase | `src/api/src/zava_forward/api/web/app.js:354-370,438-446,1825-1867,1995-1998`                                                    | `missingWorkspaceScripts`, `route()` dispatch, `contractorListView()`, `contractorCaseView(id)`, and global document click listener.   |
| C8  | codebase | `src/api/src/zava_forward/api/web/style.css:149-151,325-330,367-370`                                                             | `.flag`, `.flag.danger` (`\26A0`), `.status-line`, `.wait` (`\23F3`), `.ok` (`\2713`), and `.screen-links` styling rules.              |
| C9  | codebase | `docs/reference/research/ux/design-system.md:128-195`                                                                            | Fluent 2 component inventory and non-colour status-signal rules enforced by `test_design_system.py` and `test_role_screens.py`.        |
| C10 | codebase | `src/api/src/zava_forward/api/web/ops.js:306-318`                                                                                | `workOrdersCard(rows, mine)` and `contractorOrders()` rendered inside `contractorListView()`.                                          |
| C11 | codebase | `src/api/tests/test_content_standard.py:13-68` and `src/api/tests/test_accessibility_baseline.py:72-125`                         | Lexical ban on internal terms (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) and static WCAG baseline counters.       |
| C12 | codebase | `src/api/tests/test_procurement_screens.py:94-325`                                                                               | Procurement/contractor functional assertions and `test_vulnerability_canaries_never_reach_contractor_view` redaction canary test.      |
| C13 | codebase | `src/api/tests/test_procurement_screen_wcag.py:1-145`                                                                            | Existing procurement WCAG unit tests including numeric `tabindex == -1` check on `screenPanel` virtual nodes.                         |
| C14 | codebase | `src/api/tests/test_procurement_qa_screen_wcag.py:1-120` and `src/api/tests/test_finance_screens_wcag_225.py:1-160`              | Clean Node `vm` test harnesses without `sys.modules` deletion hazards.                                                                 |
| C15 | codebase | `src/api/tests/test_role_screens.py:345-380` and `src/api/tests/test_role_screens_conformance.py:1-130`                          | Route-order guard (`return await roleScreensView()`), design-system class inventory guard, no `innerHTML`, no inline styles, `setTimeout == 2`. |
| C16 | codebase | `src/api/tests/test_design_system.py:80-120`                                                                                     | Verifies every component class is present in both `style.css` and `design-system.md` and non-colour `:before` glyphs exist.            |
| C17 | codebase | `src/api/tests/test_role_screens_tensions_same_home.py:90-102`, `test_safety_panel_ux.py:14-20`, `test_safety_screen_wcag_keyboard.py:1-90` | Enforces 5 `screenTension(` occurrences, `async function contractorListView` slice boundary, and disjoint top-level identifiers between `app.js` and `role-screens.js`. |
| C18 | codebase | `src/api/checks/procurement_screens_browser_check.py:85-205,315-395`                                                             | Playwright/axe check asserting `status_regions`, exact row/text substrings, `#regulatory-supplier`, and Tab-stop `aria-label` order.   |
| W1  | external | `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` (retrieved 2026-11-15)                  | Current Web Interface Guidelines rules covering keyboard operability, `:focus-visible`, landmark headings, link semantics, and status cues. |

## Findings and Analysis

* **Q1 (Reusable WCAG patterns)**: `role-screens.js` already provides `screenJumpNav`, `screenPanel` (`aria-labelledby` + `<h2 tabindex="-1">`), `stateCue`, `screenCapacityState`, and `screenExpiryState` (`C1`, `C3`), while `style.css` and `design-system.md` provide `.screen-links`, `.flag`, `.flag.danger`, `.status-line`, and `.wait` with CSS `:before` glyphs (`C8`, `C9`).
* **Q2 (Target Procurement and Contractor gaps)**: `procurementJumpNav` lacks `role="navigation"`, `data-jump-target`, `Go to ...` labels, and 5 unanchored sections across `procurement-packages` and `contractor-job-pack` (`C4`-`C6`); `app.js` lacks `#/role/procurement` and `#/role/contractor` route aliases, delegated `a[data-jump]` focus handling, and jump-nav/section-landmark/state-cue wiring on `contractorListView` and `contractorCaseView` (`C7`, `C10`); and the five Deliverable 2 status surfaces need paired `.flag` / `.flag.danger` / `.status-line.wait` visual badges plus explicit textual state cues (`C1`, `C4`-`C8`).
* **Q3 (Redaction & regression invariants)**: Contractor views must only inspect `needs_notice` and `named_contact` (`C6`, `C7`, `C12`). Edits must preserve documented CSS classes (`C9`, `C15`, `C16`), banned-term rules (`C11`), static counters (`C11`, `C15`, `C17`), numeric `tabindex: -1` in `role-screens.js` (`C13`), and browser-check substrings/Tab-stop expectations (`C18`).
* **Q4 (Focused test architecture)**: `src/api/tests/test_procurement_contractor_screen_wcag.py` should evaluate `role-screens.js`, `app.js`, and `ops.js` in isolated Node `vm` harnesses via `subprocess.run` without touching or deleting `sys.modules` (`C14`), and test runs from the worktree must set `PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests` so editable installs in the shared environment cannot shadow the worktree.

## Alternatives and Recommendation

| Option | Summary | Trade-offs | Disposition |
|--------|---------|------------|-------------|
| Option A (Recommended) | Reuse documented `.flag`, `.flag.danger`, `.status-line`, `.wait`, and `.screen-links` classes with `data-state-cue` attributes and explicit plain-language textual prefixes; wire complete jump nav + `<h2 tabindex="-1">` across `role-screens.js`, `app.js`, and `ops.js`, plus `#/role/procurement` and `#/role/contractor` aliases. | Zero changes outside `src/api`; satisfies every unit, design-system, content-standard, and browser-check invariant (`C8`-`C18`). | **Selected** |
| Option B | Introduce a new `.ux-state-cue` CSS class in `style.css` and `role-screens.js`. | Fails `test_role_screens.py` and `test_design_system.py` unless `docs/reference/research/ux/design-system.md` and `docs/reference/log.md` are also edited outside the `src/api` scope (`C9`, `C15`, `C16`). | Rejected |
| Option C | Update `role-screens.js` only and leave `app.js` (`contractorListView`, `contractorCaseView`, `#/role/*` routes, global `a[data-jump]` delegation) unchanged. | Leaves `app.js` staff-authenticated Contractor views and `#/role/procurement` / `#/role/contractor` aliases incomplete against Deliverable 1 & 2 (`C7`). | Rejected |

## Decision State

* Selected convergence recommendation: **Option A** (`C1`-`C18`, `W1`).
* Confirmed caller constraints: Focused validation tier in `src/api`, dated RPI artifacts under `.copilot-tracking/{research,plans,details,changes,reviews}/2026-11-15/`, local commit with `Refs #228` without pushing.

## Risks, Limitations, and Open Questions

* **Shared Python environment editable-install shadowing**: Running `python3 -m unittest` without `PYTHONPATH=src:...` could import `zava_forward.api` from the primary checkout rather than this worktree; mitigate by running both with explicit worktree `PYTHONPATH` and verifying `Path(__file__)` resolution in `test_procurement_contractor_screen_wcag.py`.
* **Manual accessibility boundary**: Automated unit and DOM checks verify code-testable WCAG 2.2 semantics, keyboard jump links, focus delegation, and textual state cues (`#228` criterion 6), but do not claim human screen-reader or resident/staff acceptance testing (`#151` / `#155`), hence commit uses `Refs #228`.
* Open questions: None blocking planning.

## Potential Further Research

* Manual assistive-technology (NVDA/JAWS/VoiceOver) and forced-colours walkthrough across all specialist role screens under `#151` / `#155` once all role-screen WCAG slices merge into the demo integration branch.

## Planning Handoff

* Research disposition: `executed`
* Planning Readiness: `Ready`
* Canonical evidence IDs: `C1`-`C18`, `W1`
* Target implementation files for `rpi-plan`:
  * `src/api/src/zava_forward/api/web/role-screens.js`
  * `src/api/src/zava_forward/api/web/app.js`
  * `src/api/src/zava_forward/api/web/ops.js`
  * `src/api/tests/test_procurement_contractor_screen_wcag.py`

## Self-Check

* [x] Every research question (`Q1`-`Q4`) is answered with grounded `C#`/`W#` citations.
* [x] Wider, Deeper, and Contrarian waves completed in order before synthesis.
* [x] Alternatives compared and a single convergence recommendation selected with evidence-based rejection rationale.
* [x] Research remained strictly read-only on repository source files (`git status` clean except `.copilot-tracking/`).
* [x] Planning Readiness (`Ready`) and Research disposition (`executed`) explicitly recorded.

