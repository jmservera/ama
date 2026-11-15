# RPI Plan Critique: Procurement and Contractor Screens WCAG 2.2 Conformance (Issue #228)

## Metadata

* Task ID: issue-228-procurement-wcag
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/procurement-contractor-wcag-228-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Caller requirements assessed:
  * Requirement 1: Keyboard-operable section jump navigation (`role="navigation"`, `aria-label`) with `Go to ...` links for all section landmarks and delegated focus movement to target section headings (`tabindex="-1"`) across Procurement and Contracts Manager and staff-facing Contractor screens in `src/api/src/zava_forward/api/web/role-screens.js` and `src/api/src/zava_forward/api/web/app.js` (`#/role/procurement`, `#/role/contractor`, `#/screens?screen=procurement-packages`, `#/screens?screen=contractor-job-pack`, `contractorListView`, `contractorCaseView`).
  * Requirement 2: Explicit plain-language textual state cues and non-colour status signals across package queue rows, draft readiness cards, unmet prerequisite badges, contractor job pack submission/acknowledgement items, and independent review status badges while preserving contractor vulnerability-reason redaction.
  * Requirement 3: Focused conformance unit tests in `src/api/tests/test_procurement_contractor_screen_wcag.py` without `sys.modules` deletion hazards.
  * Requirement 4: Focused validation tier (`python3 -m unittest discover -s tests -p "test_*procurement*.py" -v`, `test_role_screens_conformance.py`, `python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .` in `src/api`), dated RPI artifacts under `.copilot-tracking/{research,plans,details,changes,reviews}/2026-11-15/`, and local commit with `Refs #228` without pushing.
* Plan and research artifacts assessed:
  * `.copilot-tracking/plans/2026-11-15/procurement-contractor-wcag-228-plan.md` (`FR-1`..`FR-4`, `NFR-1`..`NFR-2`, `P01`..`P03`)
  * `.copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md` (`P01-T01`, `P01-T02`, `P02-T01`, `P03-T01`)
  * `.copilot-tracking/research/2026-11-15/procurement-contractor-wcag-228-research.md` (`C1`..`C18`, `W1`)
* Repository source and regression-guard files cross-checked directly:
  * `src/api/src/zava_forward/api/web/role-screens.js`
  * `src/api/src/zava_forward/api/web/app.js`
  * `src/api/src/zava_forward/api/web/ops.js`
  * `src/api/tests/test_procurement_screens.py`
  * `src/api/tests/test_procurement_screen_wcag.py`
  * `src/api/tests/test_procurement_qa_screen_wcag.py`
  * `src/api/tests/test_role_screens.py`
  * `src/api/tests/test_role_screens_conformance.py`
  * `src/api/tests/test_role_screens_tensions_same_home.py`
  * `src/api/tests/test_safety_screen_wcag_keyboard.py`
  * `src/api/tests/test_safety_panel_ux.py`
  * `src/api/checks/procurement_screens_browser_check.py`
  * `docs/reference/research/ux/design-system.md` (cited by `C9` and `test_role_screens.py`)
* Criterion boundary: Evaluate technical correctness, WCAG 2.2 semantic/focus/non-colour conformance (`1.3.1`, `1.4.1`, `2.1.1`, `2.4.1`, `2.4.4`), cross-script execution safety, contractor redaction boundaries, and compatibility with existing unit and Playwright conformance guards across branch `feat/ux-228-procurement-wcag` targeting `feat/demo-233-same-home-tensions-0825`.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller Req 1 / `FR-1` (Jump nav, landmarks, focus targets) | Partial | Covered for named panels in `P01-T01` and `P02-T01`, but `journeyStageMap` inside `roleScreensView()` remains an unanchored `<section>` (`PC-003`), `contractorListView()` nests `<section id="contractor-work-orders">` inside `<section id="contractor-assigned-jobs">` unless `jobsSection.after(...)` is used (`PC-001`), and delegated click deduplication is order-dependent (`PC-004`). |
| Caller Req 2 / `FR-3` (Textual state cues, non-colour signals, redaction) | Partial | Avoids undocumented `.ux-state-cue` classes in `role-screens.js` (`C9`) and preserves redaction (`C14`), but `P01-T02` stutters `"Unmet or Unknown: Unmet or Unknown"` and breaks four exact string/row guards in `src/api/checks/procurement_screens_browser_check.py` (`PC-002`), while `P02-T01` references undefined `c.needs_notice` and omits `w.needs_notice` cues in `ops.js` (`PC-001`). |
| Caller Req 2 / `FR-2` (`#/role/procurement` and `#/role/contractor` route aliases) | Partial | `ROLE_SCREEN_HASHES` script-loader and `roleScreensView()` fallback cover route resolution (`C1`), but `app.js` `#nav` active-link highlighting and initial `routeStatus` announcement fall back to `"Case workspace"` on `#/role/*` (`PC-005`). |
| Caller Req 3 / `FR-4` (`test_procurement_contractor_screen_wcag.py`, no `sys.modules` deletion) | Partial | `P03-T01` defines Node `vm` DOM-tree assertions without `sys.modules` mutation (`C15`), but omits `ops.js` from top-level global lexical collision checks (`PC-004`), omits bidirectional listener-registration order checks (`PC-004`), and needs host-vs-panel landmark scoping for `roleScreensView()` (`PC-003`). |
| Caller Req 4 / `NFR-1`..`NFR-2` (Focused validation tier, RPI artifacts, local `Refs #228` commit) | Covered with minor gap | Validation commands, focused-tier basis, artifact paths, and `Refs #228` non-closing commit semantics are specified; `P03` omits `tests/test_regulatory_ux_check.py` despite `P02-T01` depending on its `#regulatory-supplier` invariant (`PC-005`). |
| Research `C1`..`C18`, `W1` | Covered | All 18 codebase findings and WAI-ARIA `W1` pattern are incorporated; `C18` (`procurement_screens_browser_check.py`) and `C16` (classic script global lexical scope) require tighter enforcement in `P01-T02`, `P02-T01`, and `P03-T01` (`PC-002`, `PC-004`). |
| `P01` (`P01-T01`, `P01-T02`) | Revise | Sound design-system class selection (`.flag`, `.flag.danger`, `.status-line`, `.wait`, `.screen-links`), no-control boundary (`C8`), and tension-title preservation (`C10`); requires `PC-002` and `PC-003` corrections. |
| `P02` (`P02-T01`) | Revise | Sound separation of `.ux-state-cue` in `app.js`/`ops.js` and vulnerability redaction; requires `PC-001`, `PC-004`, and `PC-005` corrections. |
| `P03` (`P03-T01`) | Revise | Strong Node `vm` test architecture; requires updates aligned with `PC-001`..`PC-005`. |

## Verdict

* Verdict: Revise
* Rationale: The plan's overall architecture, Fluent 2 / design-system class discipline, read-only role boundaries, and Node `vm` conformance test approach are strong, but two High-severity defects (`PC-001` runtime `ReferenceError` and nested landmark hazard in `contractorListView()` plus missing `ops.js` notice cues; `PC-002` string mutations that break `src/api/checks/procurement_screens_browser_check.py` and render `"Unmet or Unknown: Unmet or Unknown"`), two Medium-severity defects (`PC-003` unanchored `journeyStageMap` `<section>` on `#/role/procurement` and `#/role/contractor`; `PC-004` order-dependent `a[data-jump]` double-focus and unchecked `ops.js` global identifier collisions), and one Low-severity wiring/validation gap (`PC-005`) must be corrected in the plan and phase details before implementation. Every finding has a deterministic planner-owned fix requiring no divergent user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Staff contractor list view specification introduces a ReferenceError, nests landmarks across out.after(), and omits work-order visit-notice cues

* Related IDs: `FR-1`, `FR-2`, `FR-3`, `P02`, `P02-T01`, `P03-T01`, `C2`, `C4`, `C12`
* Evidence: `src/api/src/zava_forward/api/web/app.js:1825-1846`; `src/api/src/zava_forward/api/web/ops.js:306-318`; `.copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md:254-262`
* Concern: Three defects exist in `P02-T01`'s specification for `contractorListView()` and `workOrdersCard()`:
  1. `P02-T01` specifies `c.needs_notice -> ...` inside `contractorListView()`, where the row parameter in `rows.map((r) => ...)` at `src/api/src/zava_forward/api/web/app.js:1830-1832` is `r`, causing a runtime `ReferenceError: c is not defined` if implemented literally.
  2. `contractorListView()` creates `const out = h("div", { "aria-live": "polite" })` and runs `show(..., out); await load(); out.after(await contractorOrders());` (`src/api/src/zava_forward/api/web/app.js:1826-1846`). Wrapping `out` inside `<section class="card" id="contractor-assigned-jobs">` while leaving `out.after(await contractorOrders())` unchanged inserts `<section id="contractor-work-orders">` inside `<section id="contractor-assigned-jobs">` instead of as a sibling landmark; conversely, placing `<section id="contractor-assigned-jobs">` inside `out.replaceChildren(...)` traps the landmark and `<h2 tabindex="-1">` focus target inside an `aria-live="polite"` region and recreates the heading node on `"Show more"` pagination.
  3. In `src/api/src/zava_forward/api/web/ops.js:309`, `workOrdersCard(rows, mine)` renders `w.needs_notice ? h("span", { class: "flag" }, "Needs notice") : "No extra notice needed"`, which `P02-T01` leaves untouched, leaving contractor work-order visit-notice indicators without `.flag.danger` warning-glyph styling, `data-state-cue`, or explicit textual state cues (`Visit notice required:` / `Standard visit:`).
* Impact: Runtime crash (`ReferenceError`) when signed-in `Contractor` staff open `#/`, malformed nested `<section>` landmarks or broken heading focus persistence across `"Show more"` pagination, and incomplete non-colour visit-notice cues in the contractor work-order table.
* Smallest useful change: Update `P02-T01` so that: (a) `contractorListView()` inspects `r.needs_notice` (not `c.needs_notice`); (b) `const jobsSection = h("section", { class: "card", id: "contractor-assigned-jobs", "aria-labelledby": "contractor-assigned-jobs-heading" }, h("h2", { id: "contractor-assigned-jobs-heading", tabindex: "-1" }, "Assigned jobs"), out)` wraps `out` statically in `show(...)` and `jobsSection.after(await contractorOrders())` mounts `#contractor-work-orders` as a sibling `<section>` landmark; and (c) when `mine` is truthy in `src/api/src/zava_forward/api/web/ops.js:309`, `w.needs_notice` renders `<span class="flag danger" data-state-cue="Visit notice required"><span class="ux-state-cue">Visit notice required: </span>Needs notice</span>` when true and `<span class="flag" data-state-cue="Standard visit"><span class="ux-state-cue">Standard visit: </span>No extra notice needed</span>` when false, keeping notice reasons redacted. Add sibling-landmark and `workOrdersCard` notice-cue assertions to `P03-T01`.
* Action owner: `planning_parent`
* Exact resolving evidence: Revised `P02-T01` and `P03-T01` task specifications in `.copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md`.
* Decision route: Direct planner correction; no divergent user decision required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: P01-T02 state-label rewrites break procurement_screens_browser_check.py substring/row guards and duplicate "Unmet or Unknown" prefixes

* Related IDs: `FR-3`, `NFR-1`, `P01`, `P01-T02`, `P03-T01`, `C9`, `C12`, `C18`
* Evidence: `src/api/src/zava_forward/api/web/role-screens.js:838,1427-1441,1473-1478`; `src/api/checks/procurement_screens_browser_check.py:103-112,135-160,185-205,351-364`; `.copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md:187-205`
* Concern: Four text changes in `P01-T02` conflict with live `Store` payloads and `src/api/checks/procurement_screens_browser_check.py` assertions:
  1. In live `Store` package readiness payloads (`src/api/checks/procurement_screens_browser_check.py:136`), `u.state` is already `"Unmet or Unknown"`. `P01-T02` item 3 unconditionally formats `` `Unmet or Unknown: ${wording(u.state)}` ``, producing stuttering `"Unmet or Unknown: Unmet or Unknown"` text.
  2. `P01-T02` item 4 alters `"Not recorded. An acknowledgement is not acceptance."` (`src/api/src/zava_forward/api/web/role-screens.js:1476`) to `"Not recorded: an acknowledgement is not acceptance."`, breaking `CONTRACTOR_ALWAYS` exact substring verification at `src/api/checks/procurement_screens_browser_check.py:109`.
  3. `P01-T02` item 5 alters `"Unknown. Review data is not available here. Done by someone other than you."` (`src/api/src/zava_forward/api/web/role-screens.js:1477`) to `"Unknown: review data is not available here. Done by someone other than you."`, breaking `State("Issued")` exact substring verification at `src/api/checks/procurement_screens_browser_check.py:190`.
  4. `P01-T02` item 5 rewrites `Contractor submission and review` table cell prefixes (`"None recorded: no corrections submitted"`, `"Correction recorded: ..."`, `"Not recorded: no completion record"`, `"Submitted, not accepted: Recorded by ..."`), breaking `r.startswith(row)` row assertions at `src/api/checks/procurement_screens_browser_check.py:142,155-156` (`"WO-0001 v1 | None recorded | Not recorded | Unknown. No independent review"` and `"WO-0001 v1 | Wrong depth (Pam Manager, 2026-05-01) | Recorded by Pam Manager on 2026-05-02. A recorded completion is not acceptance. | Unknown. No independent review"`).
* Impact: Avoidable regression of `src/api/checks/procurement_screens_browser_check.py` during Playwright gate validation and visibly duplicated `"Unmet or Unknown: Unmet or Unknown"` badge wording in `procurement-packages`.
* Smallest useful change: Revise `P01-T02` to: (a) deduplicate state prefixes (matching `stateCue` at `src/api/src/zava_forward/api/web/role-screens.js:838`) so `u.state` values already starting with `"Unmet"` or `"Unknown"` render without repeating `"Unmet or Unknown: "`; (b) preserve exact existing sentence punctuation inside `<span class="flag danger" data-state-cue="Not recorded">Not recorded. An acknowledgement is not acceptance.</span>` and `<span class="flag danger" data-state-cue="Unknown">Unknown. Review data is not available here. Done by someone other than you.</span>`; and (c) in `Contractor submission and review` (`src/api/src/zava_forward/api/web/role-screens.js:1438-1441`), wrap the existing explicit plain-language cell strings (`"None recorded"`, correction entries, `"Not recorded"`, `"Recorded by ... A recorded completion is not acceptance."`, `"Unknown. No independent review is recorded on this screen."`) in `.flag` / `.flag.danger` badges with `data-state-cue` attributes so CSS `:before` glyphs, borders, `data-state-cue` metadata, and plain-language words are all present while `textContent` continues to satisfy `r.startswith(row)` in `src/api/checks/procurement_screens_browser_check.py:142,155-156`. Add a `P03-T01` assertion confirming `u.state = "Unmet or Unknown"` does not duplicate its prefix and exact browser-check phrases remain intact.
* Action owner: `planning_parent`
* Exact resolving evidence: Revised `P01-T02` and `P03-T01` specifications in `.copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md`.
* Decision route: Direct planner correction; no divergent user decision required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Unanchored journeyStageMap section inside roleScreensView() leaves an unlabelled, unreachable section landmark on #/role/procurement and #/role/contractor

* Related IDs: `FR-1`, `FR-2`, `FR-4`, `P01`, `P01-T01`, `P03-T01`, `C1`, `C3`
* Evidence: `src/api/src/zava_forward/api/web/role-screens.js:131,145-152,608-625,634,1387-1480`; `src/api/tests/test_procurement_screen_wcag.py:36-56`; `.copilot-tracking/plans/2026-11-15/procurement-contractor-wcag-228-plan.md:62-64`; `.copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md:145-160,295-305`
* Concern: Plan Acceptance Criterion 1, `FR-1`, and `P03-T01` require `Go to ...` jump links matching 100% of `<section>` landmarks on `#/role/procurement` and `#/role/contractor`, with every `<section>` carrying `aria-labelledby` pointing to an `<h2 tabindex="-1">`. When `roleScreensView()` renders a selected home (`src/api/src/zava_forward/api/web/role-screens.js:145-152`), it appends `!screen.ownsStageMap && journeyStageMap(c, screen.id)` inside `<section class="screen-evidence">`. Because `journeyStageMap` (`src/api/src/zava_forward/api/web/role-screens.js:610`) calls `screenPanel(\`Journey stages for ${c.id}\`, ...)` without `{ anchor }`, it emits `<section class="card screen-record"><h2>Journey stages for ...</h2></section>` with no `id`, no `aria-labelledby`, no `tabindex="-1"`, and no jump link in `procurementJumpNav`. Furthermore, `roleScreensView()` wraps the entire view in two outer shell `<section>` landmarks (`Choose a home` at `role-screens.js:131` and `section.screen-evidence[aria-label]` at `role-screens.js:145`), which `P03-T01` does not distinguish from evidence-panel `section.screen-record` landmarks.
* Impact: On `#/role/procurement?case=...` and `#/role/contractor?case=...`, the `Journey stages for ${c.id}` panel lacks `aria-labelledby`, `<h2 tabindex="-1">`, and keyboard jump navigation, and `P03-T01`'s 100% `<section>` landmark assertion fails when evaluating `roleScreensView()`.
* Smallest useful change: Update `P01-T01` to: (a) allow an optional `anchor` parameter in `journeyStageMap(c, current = null, anchor = null)` passed through to `screenPanel(\`Journey stages for ${c.id}\`, anchor ? { anchor } : {}, ...)` without altering existing callers; (b) set `ownsStageMap: true` on `procurement-packages` and `contractor-job-pack` (matching `programme-queue` at `src/api/src/zava_forward/api/web/role-screens.js:634`), render `journeyStageMap(c, "procurement-packages", "package-journey")` and `journeyStageMap(c, "contractor-job-pack", "jobpack-journey")` as the final panel in each screen's `render(c, extra)`, and append `["package-journey", "Journey stages"]` and `["jobpack-journey", "Journey stages"]` to `procurementJumpNav` (satisfying both isolated `screen.render()` in `src/api/tests/test_procurement_screen_wcag.py:36-56` and full `roleScreensView()`); and (c) specify in `P03-T01` and Plan Acceptance Criterion 1 that 100% of `section.screen-record` panels inside `screen.render()` / `.screen-evidence` (and 100% of `<section>` landmarks on `contractorListView` and `contractorCaseView`) map 1-to-1 to `Go to ...` links while `roleScreensView()` retains its two named host regions (`#screen-queue-heading` and `section.screen-evidence[aria-label]`).
* Action owner: `planning_parent`
* Exact resolving evidence: Revised `P01-T01` and `P03-T01` specifications in `.copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md` and Acceptance Criteria in `.copilot-tracking/plans/2026-11-15/procurement-contractor-wcag-228-plan.md`.
* Decision route: Direct planner correction; no divergent user decision required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Delegated a[data-jump] click deduplication is registration-order-dependent and global lexical scope guard omits ops.js

* Related IDs: `FR-1`, `FR-4`, `NFR-1`, `P01-T01`, `P02-T01`, `P03-T01`, `C5`, `C6`, `C16`
* Evidence: `src/api/src/zava_forward/api/web/app.js:354-365,1995-1998`; `src/api/src/zava_forward/api/web/role-screens.js:268-275,838,1345`; `src/api/src/zava_forward/api/web/ops.js:306-318`; `src/api/tests/test_safety_screen_wcag_keyboard.py:72-95`; `.copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md:155-158,249-252,300-310`
* Concern: Two multi-script runtime risks are left open across `app.js`, `ops.js`, and `role-screens.js`:
  1. `P01-T01` adds `if (event.defaultPrevented) return;` only to `src/api/src/zava_forward/api/web/role-screens.js:269-274`, whereas `P02-T01` (`phase-details.md:250`) does not check `e.defaultPrevented` in `src/api/src/zava_forward/api/web/app.js:1995` and leaves `const menu = document.getElementById("account"); if (!menu.contains(e.target))` unguarded when `#account` is absent in minimal Node `vm` harnesses. If `role-screens.js` registers its click listener before `app.js`, both handlers fire `.focus()` (focus count = 2), and missing `#account` throws `TypeError`.
  2. `app.js`, `ops.js`, and `role-screens.js` execute as classic top-level `"use strict"` scripts sharing one global lexical scope in the browser, yet `RoleScreensGlobalScope` (`src/api/tests/test_safety_screen_wcag_keyboard.py:92-95`) only compares `role-screens.js` against `app.js` and never inspects `ops.js` (`role-screens.js:838,1345` already declares top-level `const stateCue` and `const workOrderCues`).
* Impact: Double `.focus()` calls or `null.contains` `TypeError` depending on script evaluation order, and risk of an uncaught browser `SyntaxError: Identifier '...' has already been declared` if `ops.js` introduces top-level `const`/`let`/`function` names colliding with `role-screens.js` or `app.js`.
* Smallest useful change: Update `P02-T01` to check `if (!e.defaultPrevented)` in `app.js`'s `a[data-jump]` branch (making single-focus deduplication symmetric with `role-screens.js`), guard `if (menu && !menu.contains(e.target))` in `app.js:1996`, keep `ops.js` work-order cue helpers function-scoped inside `workOrdersCard` (or uniquely prefixed), and extend `P03-T01` to assert pairwise disjoint top-level lexical declarations across `app.js`, `ops.js`, and `role-screens.js` and verify single `.focus()` invocation under both `(app.js, role-screens.js)` and `(role-screens.js, app.js)` load orders.
* Action owner: `planning_parent`
* Exact resolving evidence: Revised `P02-T01` and `P03-T01` specifications in `.copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md`.
* Decision route: Direct planner correction; no divergent user decision required.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: Route aliases #/role/procurement and #/role/contractor omit primary #nav aria-current/routeStatus mapping, and P03 omits test_regulatory_ux_check.py

* Related IDs: `FR-2`, `NFR-1`, `P01-T01`, `P02-T01`, `P03`, `P03-T01`, `C1`, `C17`
* Evidence: `src/api/src/zava_forward/api/web/app.js:429-455`; `src/api/tests/test_role_screens.py:240`; `.copilot-tracking/plans/2026-11-15/procurement-contractor-wcag-228-plan.md:107-120`; `.copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md:247-249,264,312-322`
* Concern: Two minor integration/validation gaps exist:
  1. In `src/api/src/zava_forward/api/web/app.js:431-437`, `const active = ... hash.split("?")[0]` matches `#nav a` `href` (`#/screens` in `me.navigation`, pinned by `src/api/tests/test_role_screens.py:240`) and sets initial `routeStatus` via `routeTitle[active] || "Case workspace"`. On `#/role/procurement` and `#/role/contractor`, `#nav a[href="#/screens"]` loses `aria-current="page"` and `routeStatus` announces `"Case workspace"` until `roleScreensView()` finishes (or permanently when `!screen` renders `"Screen unavailable"` for an unauthorized role).
  2. `P02-T01` (`phase-details.md:264`) relies on preserving `id="regulatory-supplier"` in `contractorCaseView()` for `test_regulatory_ux_check.py`, yet `P03` Validation Expectations (`plan.md:107-120`, `phase-details.md:312-322`) omits `tests/test_regulatory_ux_check.py` from the targeted unittest run.
* Impact: Missing `aria-current="page"` on the `"Specialist screens"` primary navigation link and misleading `"Case workspace"` polite live-region announcement on `#/role/*` routes, plus unexecuted `test_regulatory_ux_check.py` coverage after modifying `contractorCaseView()`.
* Smallest useful change: Update `P02-T01` so `app.js` maps `ROLE_SCREEN_HASHES` paths to `#/screens` when setting `#nav` `aria-current="page"` and defines `routeTitle["#/role/procurement"]` and `routeTitle["#/role/contractor"]`, and include `tests/test_regulatory_ux_check.py` in `P03`'s targeted unittest selector.
* Action owner: `planning_parent`
* Exact resolving evidence: Revised `P02-T01` and `P03` validation commands in `.copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md` and `.copilot-tracking/plans/2026-11-15/procurement-contractor-wcag-228-plan.md`.
* Decision route: Direct planner correction; no divergent user decision required.

## Strengths and Residual Risk

* Strengths:
  * Accurately catches the strict design-system class allowlist enforced by `src/api/tests/test_role_screens.py:276-285` and `src/api/tests/test_design_system.py:80-89` (`C9`), using documented `.flag`, `.flag.danger`, `.status-line`, `.wait`, and `.screen-links` tokens in `role-screens.js` and scoping `.ux-state-cue` to `app.js` and `ops.js`.
  * Preserves read-only zero-control boundaries (`button`, `form`, `input`, `select`, `textarea` forbidden in `procurement-packages` and `contractor-job-pack`), same-home tension panel headings (`C10`), content-standard banned terminology (`C11`), contractor vulnerability-reason redaction (`C14`), and `sys.modules` test isolation (`C15`).
  * Aligns focused validation tier classification with repository instructions (D4 / issue #1294) and uses `Refs #228` rather than a premature closing keyword.
* Residual risks:
  * Local Node `vm` unit tests and static source guards do not replace full live screen-reader user testing or full hosted Playwright execution (`src/api/checks/procurement_screens_browser_check.py`); the plan appropriately discloses this evidence boundary and avoids closing `#228` prematurely (`Refs #228`).
  * Note that `src/api/checks/procurement_screens_browser_check.py:139,347` already interacts with earlier `screenCapacityState` and `journeyStageMap` changes on the parent workstream; keeping `P01-T02` compatible with `procurement_screens_browser_check.py` (`PC-002`) avoids introducing any new regression from `#228`.

## Questions or Blocking Evidence Gaps

* None. All five findings (`PC-001`..`PC-005`) are fully resolved by supplied repository evidence and require no user clarification or additional research.

## Limitations

* This critique is a static, read-only credibility assessment against the supplied plan, phase details, research (`C1`..`C18`, `W1`), and repository source/test files; no source edits, test runs, or live browser sessions were executed during critique.

## Recommended Next Action

* Highest-impact finding: `PC-001` (`[High]`: Staff contractor list view specification introduces a `ReferenceError`, nests landmarks across `out.after()`, and omits work-order visit-notice cues), closely paired with `PC-002` (`[High]`: `P01-T02` state-label rewrites break `procurement_screens_browser_check.py` substring/row guards and duplicate `"Unmet or Unknown"` prefixes).
* Action owner: `planning_parent`
* Smallest next action: Revise `.copilot-tracking/plans/2026-11-15/procurement-contractor-wcag-228-plan.md` and `.copilot-tracking/details/2026-11-15/procurement-contractor-wcag-228-phase-details.md` directly to apply `PC-001`..`PC-005`, then finalize the plan for `rpi-implement` without another critique pass.
* User response required: No
