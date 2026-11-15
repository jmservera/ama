<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #228 Procurement and Contractor WCAG 2.2 Keyboard Jump Nav, Landmarks, and Textual State Signals

## Metadata

* Task ID: issue-228-procurement-wcag
* Task slug: procurement-contractor-wcag-228
* Related plan: .copilot-tracking/plans/2026-11-15/procurement-contractor-wcag-228-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/procurement-contractor-wcag-228-research.md (`C1`-`C18`, `W1`), `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/research/ux/design-system.md`, `docs/reference/research/ux/content-standard.md`, `docs/reference/research/ux/customer-journeys/suppliers.md`

## Phase Index

| Phase ID | Name                                                                                                   | Status    | Detail sections          |
|----------|--------------------------------------------------------------------------------------------------------|-----------|--------------------------|
| P01      | Upgrade Role-Screen Jump Navigation, Landmarks, and Non-Colour State Badges (`role-screens.js`)        | ready     | P01, P01-T01, P01-T02    |
| P02      | Wire Staff-Facing Contractor Views, `#/role/*` Route Aliases, and Global Jump Focus (`app.js`/`ops.js`) | ready     | P02, P02-T01             |
| P03      | Add Focused Conformance Unit Tests and Run Validation Gate (`test_procurement_contractor_screen_wcag.py`) | ready     | P03, P03-T01             |

## Test Ownership, Target Lock, and Coverage Contract

* Canonical production targets (`3` existing files, `0` new production files, `0` removals):
  * `src/api/src/zava_forward/api/web/role-screens.js`
  * `src/api/src/zava_forward/api/web/app.js`
  * `src/api/src/zava_forward/api/web/ops.js`
* Canonical test target (`1` new test file, `0` existing test removals, maximum file additions in `src/api`: `1`):
  * `src/api/tests/test_procurement_contractor_screen_wcag.py`
* Generated targets: `none` (vanilla JS web assets served directly from `src/api/src/zava_forward/api/web/`).
* Semantic-versus-regression coverage split:
  * **Semantic behavioral coverage** (in `test_procurement_contractor_screen_wcag.py` via Node `vm` DOM simulation):
    1. `procurement-packages` and `contractor-job-pack` set `ownsStageMap: true` and render `<nav role="navigation" aria-label="Sections of this view" class="screen-links">` with `Go to ...` links covering 100% of `section.screen-record` landmarks (including dynamic `Draft readiness <pkg.id>` panels, `Journey stages`, and empty-packages fallback) while `roleScreensView()` retains its two named host shell landmarks (`#screen-queue-heading` and `section.screen-evidence[aria-label]`); each panel `<section>` has `aria-labelledby="<id>-heading"`, and each `<h2 id="<id>-heading">` has `tabindex="-1"` (`-1` numeric on raw VNode, `"-1"` attribute in DOM).
    2. `roleScreensView()` and `app.js` route/script helpers resolve both `#/role/procurement` -> `procurement-packages` and `#/role/contractor` -> `contractor-job-pack` (with optional `?case=...` query strings), mapping both aliases to `#/screens` for primary `#nav` `aria-current="page"` and `routeStatus`.
    3. `app.js` `contractorListView()` (with `ops.js` `workOrdersCard(rows, true)` mounted via `jobsSection.after(...)` as a non-nested sibling `<section>`) and `contractorCaseView(id)` render `<nav role="navigation" aria-label="...">` with `Go to ...` links matching 100% of `<section>` landmarks and `<h2 tabindex="-1">` targets (preserving `section#regulatory-supplier`).
    4. Clicking any `a[data-jump]` link dispatches `preventDefault()` and invokes `.focus()` on the target heading element exactly once whether `app.js` runs alone, `role-screens.js` runs alone, `(app.js, role-screens.js)` runs in order, or `(role-screens.js, app.js)` runs in reverse order.
    5. All five Deliverable 2 status surfaces (package queue rows, draft readiness cards, unmet prerequisite badges, contractor job pack submission/acknowledgement items, and independent review status badges, plus contractor list/case/work-order status & visit-notice badges) pair `.flag` / `.flag.danger` / `.status-line.wait` / `.status-line` visual classes with `data-state-cue` and explicit plain-language textual state labels across normal, completed, withdrawn, over-committed, unrecognised, and empty states without prefix stuttering (`"Unmet or Unknown"`) or browser-check substring regressions.
    6. Contractor vulnerability-reason redaction holds across `contractor-job-pack`, `contractorListView()`, `workOrdersCard(rows, true)`, and `contractorCaseView(id)` when canary strings populate `vulnerability_reason`, `vulnerability_notes`, `household`, and work-order `vulnerability_reason`.
  * **Regression & static guardrail coverage**:
    * Assert `test_procurement_contractor_screen_wcag.py` itself contains no `sys.modules` deletion (`del sys.modules` or `sys.modules.pop`), assert pairwise disjoint top-level lexical declarations across `app.js`, `ops.js`, and `role-screens.js`, and execute existing regression suites (`test_procurement_screens.py`, `test_procurement_screen_wcag.py`, `test_procurement_qa_screen_wcag.py`, `test_role_screens_conformance.py`, `test_role_screens.py`, `test_role_screens_tensions_same_home.py`, `test_design_system.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_safety_screen_wcag_keyboard.py`, `test_safety_panel_ux.py`, `test_regulatory_ux_check.py`), `mypy`, and `ruff`.

<!-- rpi:phase id=P01 -->
## P01: Upgrade Role-Screen Jump Navigation, Landmarks, and Non-Colour State Badges (`role-screens.js`)

### Context

`role-screens.js` already implements `procurement-packages` and `contractor-job-pack` (`C4`-`C6`), but `procurementJumpNav` omits `role: "navigation"`, `data-jump-target`, and `Go to ...` link text, leaves five `<section>` landmarks unanchored across the two screens, stringifies VNode/DOM objects inside `screenFields` and `screenTable` (`C1`), and renders several status cells/fields as unstyled plain strings without paired non-colour badge classes (`.flag` / `.flag.danger` / `.status-line.wait`) and `data-state-cue` metadata (`C4`-`C8`).

### Intent

Ensure 100% landmark-to-jump-link parity, `Go to ...` link naming, `#/role/{procurement,contractor}` alias resolution, deduplicated `a[data-jump]` focus movement, and paired non-colour visual styling + explicit plain-language textual state labels across `procurement-packages` and `contractor-job-pack` without violating any existing static or browser-harness guardrail.

### Boundaries

* Included: `src/api/src/zava_forward/api/web/role-screens.js`.
* Excluded: Adding undocumented CSS classes, adding extra `role="status"` elements inside `.screen-evidence`, adding `aria-label` onto individual `<a>` jump links, using banned internal vocabulary, or altering non-procurement/non-contractor screen outputs.

### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: Shared cell/panel helpers (`screenFields`, `screenWithheld`, `screenTension`, `screenTable`), `roleScreensView()`, `a[data-jump]` click handler, and the `procurement-packages` / `contractor-job-pack` region.

### Dependencies

* None.

### Validation Expectations

* `test_procurement_screens.py`, `test_procurement_screen_wcag.py`, `test_procurement_qa_screen_wcag.py`, `test_role_screens.py`, `test_role_screens_conformance.py`, `test_role_screens_tensions_same_home.py`, `test_design_system.py`, and `test_content_standard.py` all pass.

### Completion Evidence

* Clean diff in `role-screens.js` satisfying FR-1, FR-3, FR-4, and NFR-1.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add DOM/VNode cell pass-through, section anchors, jump nav `Go to ...` links, and `#/role/*` alias resolution in `role-screens.js`

#### Context

* `screenFields` and `screenTable` call `screenValue(value)` (`C1`), which converts VNode/DOM objects into `"[object Object]"` unless objects with `nodeType` or `tag` pass through directly.
* `screenWithheld = (items)` and `screenTension = (kind)` (`C1`) do not forward an optional `{ anchor }` option to `screenPanel`. `test_role_screens_tensions_same_home.py` (`C17`) slices from `const screenTensionText` to `function screenTable(` and checks zero occurrences of `("aria-invalid", "style", "icon", "<svg", "simulat", "impersonat")` and exact count `5` of `screenTension(`.
* `procurementJumpNav` (`C4`) lacks `role: "navigation"`, `data-jump-target`, and `Go to ${title}` link labels; five `<section>` landmarks across `procurement-packages` (`"Evidence boundary"`, `screenTension("choice")`, `"Contractor submission and review"`, `screenWithheld`) and `contractor-job-pack` (`screenWithheld`) lack `{ anchor }`; and `journeyStageMap(c, screen.id)` (`role-screens.js:149,610`) renders an unanchored `<section>` unless `journeyStageMap` accepts optional `anchor` and `procurement-packages` / `contractor-job-pack` set `ownsStageMap: true` and mount `journeyStageMap(c, ..., "package-journey" / "jobpack-journey")` directly with matching jump links (`PC-003`).
* `roleScreensView()` (`C2`) reads `query.get("screen")` only; resolving `{ "#/role/procurement": "procurement-packages", "#/role/contractor": "contractor-job-pack" }` when `(location.hash || "").split("?")[0]` matches allows `#/role/procurement` and `#/role/contractor` URLs to open their target role screens directly.
* Adding `if (event.defaultPrevented) return;` at the start of `role-screens.js`'s `a[data-jump]` listener (`C3`) paired symmetrically with `app.js` prevents duplicate `.focus()` calls regardless of script evaluation order (`PC-004`).

#### Intent

Deliver complete landmark anchor coverage (including `Journey stages`), `role="navigation"` + `Go to ...` jump links, `#/role/*` screen resolution, VNode/DOM pass-through in `screenFields`/`screenTable`, and symmetric deduplicated focus delegation in `role-screens.js`.

#### Boundaries

* Included: `screenNodeValue` helper in `role-screens.js`, optional `anchor` parameter on `screenWithheld(items, anchor)`, `screenTension(kind, anchor)`, and `journeyStageMap(c, current = null, anchor = null)`, `ownsStageMap: true` on `procurement-packages` and `contractor-job-pack`, `roleScreensView()` hash-alias fallback, `event.defaultPrevented` guard on `a[data-jump]`, `procurementJumpNav` attributes/labels, and `{ anchor }` wiring for every `section.screen-record` panel on `procurement-packages` and `contractor-job-pack`.
* Excluded: Putting `aria-label` on `<a>` jump links (`C18`) or changing numeric `tabindex: -1` in `screenPanel` (`C13`).

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`

#### Dependencies

* None.

#### Validation Expectations

* Every `<section>` rendered by `procurement-packages` (both with packages and with `packages = []`) and `contractor-job-pack` has `id`, `aria-labelledby="<id>-heading"`, `<h2 id="<id>-heading" tabindex="-1">`, and a corresponding `<a href="#<id>-heading" data-jump="<id>-heading" data-jump-target="<id>-heading">Go to ...</a>` inside `<nav role="navigation" aria-label="Sections of this view" class="screen-links">`.

#### Completion Evidence

* Passing Node `vm` assertions on landmark/jump-link 1:1 bijection and existing `test_role_screens_tensions_same_home.py` / `test_procurement_screen_wcag.py` checks.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Pair visual status styling with explicit plain-language state cues across `procurement-packages` and `contractor-job-pack`

#### Context

Deliverable 2 requires pairing visual styling with explicit plain-language textual state cues across five elements while preserving contractor vulnerability-reason redaction and existing text contracts (`C4`-`C9`, `C12`, `C18`):

1. **Package queue rows** (`package-queue` table):
   * Recorded headroom cell: wrap `screenCapacityState(cap)` in `procurementStateBadge(cue, text, danger)` using `class: "flag danger"` when `headroom < 0` or non-numeric (`Unknown`), and `class: "flag"` when `headroom >= 0` (`Fully committed: 0` / `Offered capacity remaining: N`).
   * Capacity evidence status cell: normalize `cap.evidence_status` so strings starting with `"Evidenced"` render `<span class="flag" data-state-cue="Evidenced">...</span>`, missing/blank values render `<span class="flag danger" data-state-cue="Unknown">Unknown: capacity evidence not supplied</span>`, strings starting with `"Unknown"` (such as `"Unknown - not confirmed: missing"`) render `<span class="flag danger" data-state-cue="Unknown">...</span>` (preserving exact existing wording!), and any other bare status renders `<span class="flag danger" data-state-cue="Action needed">Action needed: ...</span>`.
   * Work-order state cells (`package-orders` and `jobpack-orders`): wrap `stateCue(workOrderCues, o.state)` in `.flag` (`Open` / `Completed on record, not accepted`) or `.flag.danger` (`Withdrawn` / `Action needed`).
2. **Draft readiness cards** (`Draft readiness: ${wording(p.id)}`):
   * Status paragraph: `h("p", { class: "status-line wait", role: "status", "data-state-cue": "Draft readiness only" }, "State: Draft readiness only. This is not a release or approval.")` — keeps exact `1` `[role="status"]` per package, pairs `.status-line.wait` non-colour hourglass styling, and preserves exact substring `"Draft readiness only. This is not a release or approval."` (`C18`).
   * Reviewer summary fields: wrap `"Named reviewer"` value in `<span class="flag danger" data-state-cue="Action needed">Action needed: Unassigned. Contracts manager to name a person.</span>` (preserving `"Unassigned. Contracts manager to name a person."`).
3. **Unmet prerequisite badges** (`packagePrerequisites` in `Draft readiness` card):
   * Wrap each prerequisite's `"State"` cell in `.flag` (`data-state-cue="Met on record"`) when `stateText.startsWith("Met on record")`, and `.flag.danger` (`data-state-cue="Blocked"` / `"Unknown"` / `"Unmet"`) when unmet, blocked, or unknown, deduplicating prefixes (`PC-002`) so existing `"Met on record..."`, `"Unmet"`, `"Unmet or Unknown"`, `"Blocked: ..."`, and `"Unknown. ..."` strings never stutter `"Unmet or Unknown: Unmet or Unknown"`.
4. **Contractor job pack submission/acknowledgement items** (`procurement-packages` `"Contractor submission and review"` & `contractor-job-pack` `"Submission and review are separate"`, `"Evidence checklist"`, and `"Your job pack"` notice):
   * On `procurement-packages` (`Contractor submission and review`): wrap `"Contractor submission"` (`Unknown: Recorded outside this screen; not shown here`, `.flag.danger`), `"Acknowledgement"` (`Pending review: A contractor acknowledgement is not acceptance`, `.flag.danger`), and `"Independent review and acceptance"` (`Pending independent review: Separate step by a named reviewer; not available from this screen`, `.flag.danger`).
   * On `contractor-job-pack` (preserving `self.assertNotIn("Not supplied", text)` and exact `procurement_screens_browser_check.py` phrases, `PC-002`):
     * `"Notice before visit"`: `c.needs_notice` -> `<span class="flag danger" data-state-cue="Visit notice required">Visit notice required: Needs notice</span>` vs `<span class="flag" data-state-cue="Standard visit">Standard visit: No extra notice needed</span>` (strictly reading `c.needs_notice` only; zero access to `vulnerability_*` or `household`).
     * `"Evidence checklist"`: `"Recorded"` row -> `.flag` (`data-state-cue="Recorded"`), `"Unknown"` rows -> `.flag.danger` (`data-state-cue="Unknown"`), keeping exact cell text `"Recorded: Recorded on a work order"` and `"Unknown: Not assessed on this screen"` (`C18`).
     * `"Submission and review are separate"`: wrap `"Your submission"` (`.flag.danger`, `data-state-cue="Not recorded"`, `"Not recorded on this screen"`), `"Completion on the work order"` (`.flag`, `data-state-cue="Completed on record, not accepted"`, `"Completed on record, not accepted: Marked Completed on the work order by staff. This is a record, not acceptance."` when any order is `Completed`, else `.flag.danger`, `data-state-cue="Not marked Completed"`, `"Pending completion: Not marked Completed"`), `"Acknowledgement"` (`.flag.danger`, `data-state-cue="Not recorded, not acceptance"`, exact text `"Not recorded. An acknowledgement is not acceptance."`), and `"Independent review and acceptance"` (`.flag.danger`, `data-state-cue="Unknown: pending independent review"`, exact text `"Unknown. Review data is not available here. Done by someone other than you."`).
5. **Independent review status badges** (`workOrderRecordRows` + submission/review panels above):
   * In `workOrderRecordRows(orders)` (`PC-002`), wrap the corrections cell (`"None recorded"` in `.flag` `data-state-cue="None recorded"`, recorded corrections in `.flag.danger` `data-state-cue="Corrections recorded"`), completion cell (`"Not recorded"` in `.flag` `data-state-cue="Not recorded"`, recorded completion in `.flag` `data-state-cue="Completed on record, not accepted"`, unknown recorder in `.flag.danger` `data-state-cue="Completed on record, recorder unknown"`), and independent review cell (optional `o.independent_review === "Accepted"` -> `.flag` `"Accepted: ..."`, other supplied review -> `.flag.danger` `"Action needed: ..."`, absent -> `<span class="flag danger" data-state-cue="Unknown: pending independent review">Unknown. No independent review record is supplied to this screen.</span>`), preserving exact cell `textContent` prefixes asserted by `procurement_screens_browser_check.py:142,155-156` (`C18`) and `test_procurement_screens.py` (`C12`).

#### Intent

Ensure every status row, readiness banner, prerequisite cell, submission/acknowledgement item, and independent review status cell pairs documented non-colour visual styling with explicit plain-language textual state cues while preserving redaction and existing substring contracts.

#### Boundaries

* Included: `procurementStateBadge` and `packageEvidenceBadge` helpers and badge wrapping across `procurement-packages` and `contractor-job-pack` in `role-screens.js`.
* Excluded: Modifying CSS files, using undocumented class names, or reading resident vulnerability fields.

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`

#### Dependencies

* P01-T01 (`screenFields` and `screenTable` VNode/DOM pass-through).

#### Validation Expectations

* All existing assertions in `test_procurement_screens.py`, `test_procurement_screen_wcag.py`, and `test_procurement_qa_screen_wcag.py` pass without modification, and every status element exposes both a documented visual class (`.flag`, `.flag.danger`, or `.status-line.wait`) and `data-state-cue` + explicit plain-language text.

#### Completion Evidence

* Passing procurement unit tests and new semantic badge assertions in `test_procurement_contractor_screen_wcag.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Wire Staff-Facing Contractor Views, `#/role/*` Route Aliases, and Global Jump Focus Delegation (`app.js` & `ops.js`)

### Context

`app.js` renders staff-authenticated Contractor views (`contractorListView` at `#/` and `contractorCaseView(id)` at `#/case/:id`, `C7`) and loads `contractorOrders()` from `ops.js` (`workOrdersCard(rows, true)`, `C10`). Neither view currently exposes keyboard section jump navigation or `aria-labelledby` + `<h2 tabindex="-1">` section focus targets; `app.js` also lacks global `a[data-jump]` click delegation and `#/role/procurement` / `#/role/contractor` route dispatch (`C7`).

### Intent

Equip `app.js` and `ops.js` with `#/role/{procurement,contractor}` route/script support, global `a[data-jump]` focus delegation, keyboard jump navigation (`role="navigation"`, `aria-label`, `Go to ...`), section landmarks with `<h2 tabindex="-1">` focus targets, and paired non-colour badges + explicit textual state cues on `contractorListView`, `contractorCaseView`, and contractor `workOrdersCard` while preserving redaction and all `app.js` static-test boundaries.

### Boundaries

* Included: `src/api/src/zava_forward/api/web/app.js` and `src/api/src/zava_forward/api/web/ops.js`.
* Excluded: Altering non-contractor views in `app.js`/`ops.js`, breaking the `async function contractorListView` slice boundary (`C17`), introducing top-level identifiers that collide with `role-screens.js` (`C17`), or altering literal `return await roleScreensView()` (`C15`).

### Likely Targets

* `src/api/src/zava_forward/api/web/app.js`
* `src/api/src/zava_forward/api/web/ops.js`

### Dependencies

* P01 (`roleScreensView()` hash-alias fallback and `event.defaultPrevented` deduplication in `role-screens.js`).

### Validation Expectations

* `test_role_screens.py`, `test_safety_panel_ux.py`, `test_safety_screen_wcag_keyboard.py`, `test_accessibility_baseline.py`, and `test_content_standard.py` pass alongside the new contractor screen WCAG unit tests.

### Completion Evidence

* Verified route dispatch, jump nav, landmark focus delegation, state cues, and vulnerability redaction across `app.js` and `ops.js`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add `#/role/{procurement,contractor}` route/script support, global `a[data-jump]` delegation, and Contractor view WCAG landmarks & state cues in `app.js` and `ops.js`

#### Context

* In `app.js` (`C7`, `C15`, `PC-001`, `PC-004`, `PC-005`):
  * Define `const ROLE_SCREEN_HASHES = { "#/role/procurement": "procurement-packages", "#/role/contractor": "contractor-job-pack" };` (disjoint from all top-level identifiers in `role-screens.js` and `ops.js`, placed near `missingWorkspaceScripts`).
  * In `missingWorkspaceScripts(hash, caseRoute)`: treat `const roleScreenRoute = destination === "#/screens" || Object.hasOwn(ROLE_SCREEN_HASHES, destination);`, load `/role-screens.js` when `Boolean(me) && roleScreenRoute`, and exclude `roleScreenRoute` from the `contractor && !caseRoute` `/ops.js` trigger so `#/role/contractor` only loads `/role-screens.js`.
  * In `route()`: map `Object.hasOwn(ROLE_SCREEN_HASHES, hash.split("?")[0])` to `"#/screens"` when computing `active` so `#nav a[href="#/screens"]` receives `aria-current="page"` and `routeStatus` announces `"Specialist screens"` (`PC-005`), and dispatch `if (hash.split("?")[0] === "#/screens" || Object.hasOwn(ROLE_SCREEN_HASHES, hash.split("?")[0])) return await roleScreensView();` — preserving literal substring `"return await roleScreensView()"` before `"return await (m ? contractorCaseView"` (`C15`).
  * In global `document.addEventListener("click", (e) => ...)` (`app.js:1995`): guard `const menu = document.getElementById("account"); if (menu && !menu.contains(e.target)) menu.open = false;`, then if `!e.defaultPrevented`, intercept `const jump = e.target?.closest?.("a[data-jump]");`, call `e.preventDefault()`, and invoke `document.getElementById(jump.getAttribute("data-jump"))?.focus()` (`PC-004`).
  * Place helper functions (`contractorJumpLinks`, `contractorVisitNoticeBadge`) strictly AFTER `contractorCaseView` (below `async function contractorListView`, preserving `test_safety_panel_ux.py`'s slice boundary at `async function contractorListView`, `C17`).
  * In `contractorListView()` (`PC-001`):
    * Create `const jobsSection = h("section", { class: "card", id: "contractor-assigned-jobs", "aria-labelledby": "contractor-assigned-jobs-heading" }, h("h2", { id: "contractor-assigned-jobs-heading", tabindex: "-1" }, "Assigned jobs"), out);`.
    * Render `contractorJumpLinks([["contractor-assigned-jobs-heading", "Assigned jobs"], ["contractor-work-orders-heading", "Your work orders"]], "Sections of your jobs")` and `jobsSection` via `show(...)`, then after `await load()` call `jobsSection.after(await contractorOrders())` so `#contractor-work-orders` mounts as a sibling `<section>` landmark rather than inside `#contractor-assigned-jobs`.
    * Inside `rows.map((r) => ...)`, pair job status (`<span class="flag" data-state-cue="Case status">Status: ${r.status || "Unknown"}</span>`) and notice cue using `r.needs_notice` (`contractorVisitNoticeBadge(r.needs_notice)` -> `<span class="flag danger" data-state-cue="Visit notice required">Visit notice required: Needs notice</span>` vs `<span class="flag" data-state-cue="Standard visit">Standard visit: No extra notice needed</span>`) while never reading vulnerability fields.
  * In `ops.js` `workOrdersCard(rows, mine)` (`C10`, `PC-001`, `PC-004`):
    * Keep state-cue and notice-badge helpers function-scoped inside `workOrdersCard` so zero new top-level identifiers are added to `ops.js` (`PC-004`).
    * When `mine` is truthy, attach `id: "contractor-work-orders"`, `"aria-labelledby": "contractor-work-orders-heading"` to `<section class="card">`, render `<h2 id="contractor-work-orders-heading" tabindex="-1">Your work orders</h2>` (preserving exact heading name `"Your work orders"` for `procurement_browser_check.py`), render each work order's state with a documented `.flag` / `.flag.danger` + `data-state-cue` state cue (`Open: Issued`, `Open: Appointed`, `Completed on record, not accepted: Completed`, `Withdrawn: Withdrawn`, `Action needed: <other>`), and render `w.needs_notice` with `.flag.danger` / `.flag` + `data-state-cue` + explicit text (`Visit notice required: Needs notice` vs `Standard visit: No extra notice needed`), keeping notice reasons redacted.
  * In `contractorCaseView(id)` (`app.js:1848-1867`):
    * Render `<div class="status-line" role="status" data-state-cue="Case status">Status: ${c.status || "Unknown"}</div>`.
    * Render `contractorJumpLinks([["regulatory-supplier-heading", "Requirements and doubt route"], ["contractor-before-visit-heading", "Before you visit"], ["contractor-job-details-heading", "The job"], ["contractor-visits-heading", "Visits"]], "Sections of this job")`.
    * Equip all four `<section>` elements with `id` (keeping `id="regulatory-supplier"` on the first section for `test_regulatory_ux_check.py`), `aria-labelledby="...-heading"`, and `<h2 id="...-heading" tabindex="-1">`.
    * In `"Before you visit"`, pair `.card.ai` with `contractorVisitNoticeBadge(c.needs_notice)` while preserving `"The reason for any notice is not shared with contractors."` and zero vulnerability field access.
    * In `"Visits"`, pair visit outcome with explicit textual label `Outcome: ${a.outcome || "Not recorded"}`.

#### Intent

Complete WCAG 2.2 keyboard jump navigation, section landmarks, delegated focus movement, route aliases, and explicit non-colour state labels across `app.js` and `ops.js` Contractor views.

#### Boundaries

* Included: `app.js` and `ops.js` regions specified above.
* Excluded: Any banned vocabulary (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`), any new `aria-invalid` or `h("table", {},` calls, or any identifier overlap with `role-screens.js`.

#### Likely Targets

* `src/api/src/zava_forward/api/web/app.js`
* `src/api/src/zava_forward/api/web/ops.js`

#### Dependencies

* P01-T01.

#### Validation Expectations

* `contractorListView`, `contractorCaseView`, `#/role/procurement`, `#/role/contractor`, and global `a[data-jump]` delegation pass Node `vm` behavioral tests and all existing `app.js` static guards.

#### Completion Evidence

* Clean diff in `app.js` and `ops.js` verified by `test_procurement_contractor_screen_wcag.py` and existing `src/api/tests/` suites.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Add Focused Conformance Unit Tests and Run Validation Gate (`test_procurement_contractor_screen_wcag.py`)

### Context

Issue `#228` requires focused unit tests in `src/api/tests/test_procurement_contractor_screen_wcag.py` (without `sys.modules` deletion hazards) verifying keyboard jump navigation, section landmarks, heading focus targets, textual state cues, and contractor vulnerability-reason redaction, validated alongside `test_*procurement*.py`, `test_role_screens_conformance.py`, `mypy`, and `ruff`.

### Intent

Create `src/api/tests/test_procurement_contractor_screen_wcag.py` with crisp semantic and regression coverage and execute all planned validation checks from `src/api`.

### Boundaries

* Included: `src/api/tests/test_procurement_contractor_screen_wcag.py` (`1` file addition, `0` removals) and focused validation runs.
* Excluded: Mutating/deleting `sys.modules`, modifying unrelated test files, or pushing to remote.

### Likely Targets

* `src/api/tests/test_procurement_contractor_screen_wcag.py`

### Dependencies

* P01, P02.

### Validation Expectations

* From `src/api` (with `PYTHONPATH=src:../core/src:../agents/src:../core/tests:../agents/tests`):
  * `python3 -m unittest discover -s tests -p "test_*procurement*.py" -v`
  * `python3 -m unittest tests/test_role_screens_conformance.py tests/test_role_screens.py tests/test_role_screens_tensions_same_home.py tests/test_design_system.py tests/test_accessibility_baseline.py tests/test_content_standard.py tests/test_safety_screen_wcag_keyboard.py tests/test_safety_panel_ux.py tests/test_regulatory_ux_check.py -v`
  * `python3 -m mypy`
  * `python3 -m ruff check . && python3 -m ruff format --check .`

### Completion Evidence

* Zero failures across all targeted unit/conformance suites, `mypy`, and `ruff`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Create `src/api/tests/test_procurement_contractor_screen_wcag.py` and execute focused validation suite

#### Context

Following `test_finance_screens_wcag_225.py` (`C14`), `test_procurement_contractor_screen_wcag.py` uses Python's standard `unittest`, `json`, `subprocess`, `ast`, and `pathlib` (zero `sys.modules` mutations) to run Node `vm` harnesses against `role-screens.js`, `app.js`, and `ops.js` directly from `Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"`.

#### Intent

Verify every `#228` WCAG 2.2 requirement with tests that would fail without P01 and P02, cover edge cases (empty packages, multiple packages, completed vs issued vs withdrawn orders, over-committed/unknown capacity, unmet vs met vs blocked prerequisites, `#/role/procurement` and `#/role/contractor` aliases, single-focus deduplication when both `app.js` and `role-screens.js` listeners are attached, and contractor vulnerability canaries), and enforce the no-`sys.modules`-deletion invariant via AST check.

#### Boundaries

* Included: `src/api/tests/test_procurement_contractor_screen_wcag.py` and validation command execution.
* Excluded: Network or external browser dependencies inside unit tests.

#### Likely Targets

* `src/api/tests/test_procurement_contractor_screen_wcag.py`

#### Dependencies

* P01-T01, P01-T02, P02-T01.

#### Validation Expectations

* All test cases in `test_procurement_contractor_screen_wcag.py`, all `test_*procurement*.py` tests, `test_role_screens_conformance.py`, sibling guard suites, `mypy`, and `ruff` pass cleanly.

#### Completion Evidence

* Recorded command outputs and exit codes (`0`) in `.copilot-tracking/changes/2026-11-15/procurement-contractor-wcag-228-changes.md`.

#### Unresolved Items

* None.
