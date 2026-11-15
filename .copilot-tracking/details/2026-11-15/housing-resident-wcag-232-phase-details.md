<!-- markdownlint-disable-file -->
# RPI Phase Details: Housing Officer and Resident Engagement WCAG 2.2 AA Baseline (#232)

## Metadata

* Task ID: 2026-11-15-housing-resident-wcag-232
* Task slug: housing-resident-wcag-232
* Related plan: .copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/housing-resident-wcag-232-research.md, docs/reference/research/ux/wcag-conformance-baseline.md, docs/reference/research/ux/design-system.md, docs/reference/research/ux/content-standard.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md

## Phase Index

| Phase ID | Name                                                                     | Status   | Detail sections          |
|----------|--------------------------------------------------------------------------|----------|--------------------------|
| P01      | Complete Staff Route, Live-Status, and Focus Parity in Web Host          | Complete | P01, P01-T01, P01-T02    |
| P02      | Upgrade Housing and Resident Case Panel Accessibility in `panels.js`     | Complete | P02, P02-T01, P02-T02    |
| P03      | Focused WCAG 2.2 Verification, Web Guidelines Audit, and Local Validation | Complete | P03, P03-T01, P03-T02    |

<!-- rpi:phase id=P01 -->
## P01: Complete Staff Route, Live-Status, and Focus Parity in Web Host

### Context

Research findings `C1`, `C2`, `C4`, `C6`, `C13`, and `C15` established that `#/role/housing_officer` and `#/role/resident_engagement` already route into `role-screens.js`, whereas `#/role/contact_centre` is missing from both `isRoleScreensDestination` (`app.js`) and `ROLE_HASH_SCREENS` (`role-screens.js`). In addition, `roleScreensView()` updates `#workspace-status` only at the settled render and omits explicit `aria-live="polite"` on three inline `role="status"` paragraphs.

### Intent

Ensure all three frontline/resident staff role hashes (`#/role/housing_officer`, `#/role/contact_centre`, `#/role/resident_engagement`) and specialist screens (`resident-choice`, `resident-service-issues`) share identical lazy-loading, nav state, default-deny alert, jump-heading focus, and `aria-live="polite"` lifecycle announcements.

### Boundaries

* Included: `src/api/src/zava_forward/api/web/app.js` and `src/api/src/zava_forward/api/web/role-screens.js`.
* Excluded: `style.css` focus selectors pinned by peer suites (`C7`), `setTimeout` or `api()` counts in `role-screens.js`, and any resident contact trigger or role simulator.

### Likely Targets

* `src/api/src/zava_forward/api/web/app.js`: Normalize `const target = String(destination || "").split("?")[0];` in `isRoleScreensDestination` across all role hashes and include `#/role/contact_centre`.
* `src/api/src/zava_forward/api/web/role-screens.js`: Add `"#/role/contact_centre": "resident-service-issues"` to `ROLE_HASH_SCREENS`, add `"aria-live": "polite"` on the 3 shared-host inline `role="status"` elements (`screenTable` truncation notice at line 51, loading state at line 129, queue count at line 145), guard `!signal.aborted` and set `#workspace-status` text on loading, chooser (branched on `installed.length`), invalid-page, unavailable-screen, and record-mismatch branches while keeping the settled status format exact, and resolve `document.getElementById(link.getAttribute("data-jump"))` once in the delegated click handler.

### Dependencies

* None.

### Validation Expectations

* Node VM route tests verify `#/role/contact_centre`, `#/role/housing_officer`, and `#/role/resident_engagement`, `aria-current="page"`, `/ops.js` non-loading, `#workspace-status` announcements across loading/error/chooser/settled states, and `a[data-jump]` focus + `scrollIntoView`.
* `test_role_screens.py`, `test_role_screens_conformance.py`, `test_housing_resident_screen_wcag.py`, `test_resident_screen_wcag.py`, and `test_frontline_screen_wcag.py` continue to pass.

### Completion Evidence

* Clean diff in `app.js` and `role-screens.js` verified by Node VM assertions and zero conformance/timer/request/class-inventory regressions.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add `#/role/contact_centre` route support in `app.js` and `role-screens.js`

#### Context

Issue #232 (*Build or adapt the neighbourhood housing officer, contact-centre and resident engagement views*) and PRD FR-055 (`C15`) group neighbourhood housing officers and contact-centre officers on the service-issue/case-context view alongside resident engagement officers on the resident-choice view. Currently `app.js` (`isRoleScreensDestination`) and `role-screens.js` (`ROLE_HASH_SCREENS`) recognise `#/role/housing_officer` and `#/role/resident_engagement`, leaving `#/role/contact_centre` falling back to the default case list (`C1`, `C2`).

#### Intent

Route `#/role/contact_centre` (with optional `?case=` and `?page=` parameters) cleanly to `"resident-service-issues"` through `isRoleScreensDestination` and `ROLE_HASH_SCREENS`.

#### Boundaries

* Included: Adding `#/role/contact_centre` to `isRoleScreensDestination` in `app.js` and `"#/role/contact_centre": "resident-service-issues"` to `ROLE_HASH_SCREENS` in `role-screens.js`.
* Excluded: Adding new role simulator controls, changing server role names, or loading `/ops.js`.

#### Likely Targets

* `src/api/src/zava_forward/api/web/app.js`: Normalize `const target = String(destination || "").split("?")[0];` in `isRoleScreensDestination(destination)` and add `target === "#/role/contact_centre"`.
* `src/api/src/zava_forward/api/web/role-screens.js`: Update `ROLE_HASH_SCREENS`.

#### Dependencies

* None.

#### Validation Expectations

* Navigating to `#/role/contact_centre`, `#/role/contact_centre?case=ZF-01`, and `#/role/contact_centre?page=2` loads `/role-screens.js` (not `/ops.js`), marks Specialist screens nav link `aria-current="page"`, renders `"Resident service issue queue"`, and shows `role="alert"` `"Screen unavailable"` for `Contractor` and `Application Administrator`.

#### Completion Evidence

* Passing route and role-denial tests in `src/api/tests/test_housing_resident_wcag_232.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Complete `aria-live="polite"` announcements and jump-heading focus in `role-screens.js`

#### Context

`index.html` mounts `#workspace-status` with `role="status" aria-live="polite" aria-atomic="true"` (`C3`), and `specialist_keyboard_browser_check.py` asserts that settled specialist screens announce `"${me.user.role}. ${screen.title}. ${c ? 'Selected home ' + c.id + '.' : 'No home selected.'}"` (`C13`). However, `roleScreensView()` does not update `#workspace-status` when entering loading (`Loading recorded evidence.`), screen chooser (`!screen`), invalid page (`page === null`), unauthorized screen (`!screen.roles.includes(...)`), or record mismatch (`c && c.id !== caseId`), and inline `role="status"` paragraphs (`screenTable` truncation notice, loading message, home count) omit `"aria-live": "polite"` (`C4`). In addition, the `a[data-jump]` click handler queries `document.getElementById(...)` twice (`C6`).

#### Intent

Provide polite live-region announcements across every specialist view lifecycle state without changing the settled `#workspace-status` format, add `"aria-live": "polite"` to inline `role="status"` nodes, and resolve the target jump heading once before focusing and scrolling.

#### Boundaries

* Included: `screenTable` truncation `<p>`, `roleScreensView` loading/chooser/error/settled status updates, and `a[data-jump]` click listener in `role-screens.js`.
* Excluded: Modifying `setTimeout` calls, `api()` calls, undocumented CSS classes, or settled `#workspace-status` wording.

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: `screenTable`, `roleScreensView` (including preserving `"aria-label": "Evidence for ${c.id}"` alongside `id: "screen-evidence"` and `<h2 id="screen-evidence-heading" tabindex="-1">` so Playwright `get_by_role("region", name="Evidence for ZF-1")` and jump-link focus both hold), and the `document.addEventListener("click", ...)` jump handler.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Every shared-host `role="status"` node (`role-screens.js:51,129,145`) and every `role="status"` node rendered on `#232` screens (`resident-choice`, `resident-service-issues`) carries `aria-live="polite"`; when `!signal.aborted`, `#workspace-status` reflects loading, chooser (`installed.length > 0` vs `0`), invalid-page, unavailable-screen, record-mismatch, and settled states; jump-link clicks focus `<h2 tabindex="-1">` and scroll `{ block: "start" }`.

#### Completion Evidence

* Passing `aria-live` and programmatic-focus tests in `test_housing_resident_wcag_232.py` and `test_specialist_keyboard_check.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Upgrade Housing and Resident Case Panel Accessibility in `panels.js`

### Context

PRD FR-055 designates the case workspace Resident panel (`residentPanel` + `actForm` in `src/api/src/zava_forward/api/web/panels.js`) as the housing officer, contact-centre officer, and resident engagement workbench case panel (`C9`, `C15`). Research (`C8`, `C9`, `C14`, `C16`) identified whitespace in `actForm` control IDs (`id="f-Record what the resident said-measure"`), missing `type="button"` on `actForm` submit buttons, missing `.table-scroll[role="region"][tabindex="0"]` and `<th scope="row">` on `Resident decisions by measure`, and missing non-colour textual state cues on contractor readiness, measure answers, update commitment, and service/remedy states.

### Intent

Bring `actForm` and `residentPanel` in `panels.js` to full WCAG 2.2 AA form, table, keyboard-overflow, and non-colour textual state-meaning conformance while preserving every counted guard (`test_accessibility_baseline.py`), plain-language copy rule (`test_content_standard.py`), and Playwright substring contract (`test_resident_api.py`, `test_case_journey.py`).

### Boundaries

* Included: `actForm` and `residentPanel` in `src/api/src/zava_forward/api/web/panels.js`.
* Excluded: Adding any new `h("table", {}, ...)` call (count must remain `14`), altering `setAttribute("aria-invalid", "true")` count (`9`), introducing banned words (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) or em dashes, or adding outbound resident contact triggers.

### Likely Targets

* `src/api/src/zava_forward/api/web/panels.js`: `actForm` ID slugification and `type: "button"`, plus `residentPanel` `.table-scroll` wrapper, `<th scope="row">`, and plain-language state-cue helpers scoped locally inside `residentPanel`.

### Dependencies

* P01.

### Validation Expectations

* Rendered `residentPanel` DOM has zero whitespace in `id` or `for` attributes, 1:1 `<label for>` -> control `id` bindings, `type="button"` on action buttons, a keyboard-focusable `.table-scroll[role="region"][aria-label="Resident decisions by measure"][tabindex="0"]` containing `<caption>`, `<th scope="col">`, and `<th scope="row">`, and plain-language state cues across all resident/contractor branches.
* `test_accessibility_baseline.py`, `test_content_standard.py`, and `test_case_journey.py` pass without regression.

### Completion Evidence

* Passing `panels.js` static and rendered DOM tests in `test_housing_resident_wcag_232.py` plus green baseline suites.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Slugify `actForm` field IDs and set explicit button `type="button"` in `panels.js`

#### Context

In `panels.js`, `actForm(title, fields, path, done)` builds `const id = \`f-${title}-${name}\`` (`C8`). Because `title` is a human sentence (such as `"Record what the resident said"`), every generated `id` and `<label for>` contains spaces, violating the HTML5 non-whitespace ID rule and breaking assistive-technology IDREF resolution under WCAG 1.3.1 / 3.3.2 / 4.1.2. The submit `<button>` also omits `type: "button"`.

#### Intent

Slugify `title` and `name` into valid lowercase hyphen-separated HTML5 IDs (`f-${slug}-${fieldSlug}`) and set `type: "button"` on `actForm`'s action button while keeping `test_case_journey.py` label-click and validation behavior intact.

#### Boundaries

* Included: `actForm` in `src/api/src/zava_forward/api/web/panels.js`.
* Excluded: Changing `setAttribute("aria-invalid", "true")` calls (`test_accessibility_baseline.py` pins count `== 9`) or form submission payload keys.

#### Likely Targets

* `src/api/src/zava_forward/api/web/panels.js`: `actForm` helper (keep slug logic locally inside `actForm` so `test_case_journey.py` substring split anchors remain intact), plus coupled selector update in `src/api/checks/case_journey_browser_check.py` (`#f-raise-a-commitment-supplier`).

#### Dependencies

* None.

#### Validation Expectations

* Every `id` and `for` attribute rendered by `actForm` matches `^[a-z0-9-]+$` (and every `id`/`for` across `residentPanel` has zero whitespace) with 1:1 label-to-control pairing and `type="button"` on the submit control; `test_case_journey.py` passes.

#### Completion Evidence

* Node VM form-accessibility assertions in `test_housing_resident_wcag_232.py` and green `test_case_journey.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Add keyboard-scrollable table region, `<th scope="row">`, and textual state cues in `residentPanel`

#### Context

In `panels.js`, `residentPanel(c, reload)` renders:
1. Contractor view (`!c.resident`): `.flag` badges (`m.flag === "Proceed"` vs non-proceed) without a `Confirmed:` / `Action needed:` prefix (`C9`).
2. Staff `Resident decisions by measure` table: unwrapped `h("table", {}, ...)` without `.table-scroll[role="region"][tabindex="0"]`, first-column `h("td", {}, ...)` instead of `h("th", { scope: "row" }, ...)`, and raw `${m.status}. ${m.readiness}` without plain-language state cues (`C9`).
3. `Resident-update commitment` and `Service requests and complaints`: raw status strings without `Confirmed` / `Waiting for resident` / `Action needed` cues (`C9`).

Static/copy guards (`C14`, `C16`) require keeping exact `h("table", {}, ...)` count `== 14`, zero bare `h("th", {}`, zero banned jargon words (`hold`, `gate`, `provenance`, `trace`, `snapshot`, `envelope` — so contractor readiness must check `m.flag === "Proceed"` rather than comparing against `"Hold"`), keeping `test_case_journey.py:698-706,990` substring split anchors (`"  const residentForm = "`, `"  const serviceForm"`, `"  const staff"`) intact, and preserving contiguous `"Response: ${r.status}. Owner: ${named(r.status_owner)}."` and `"Remedy: ${remedyStatus}. Owner: ${named(r.remedy?.owner)}."` substrings (`test_resident_api.py:875-916`).

#### Intent

Wrap the existing `h("table", {}, ...)` in `h("div", { class: "table-scroll", role: "region", "aria-label": "Resident decisions by measure", tabindex: 0 }, ...)`, upgrade column 0 to `h("th", { scope: "row" }, ...)`, and attach local `Object.hasOwn`-safe plain-language textual state cues (`Confirmed`, `Waiting for resident`, `Action needed`, `Unknown`) to contractor readiness badges (`data-state-cue` + text prefix), measure answers, update commitment status, and service/remedy items (prepending `State: ${cue}. ` outside `"Response: ${r.status}. Owner: ..."` and `"Remedy: ${remedyStatus}. Owner: ..."`) while preserving `test_case_journey.py` anchors.

#### Boundaries

* Included: `residentPanel` in `src/api/src/zava_forward/api/web/panels.js` using local helpers inside `residentPanel` (avoiding global identifier collisions across concatenated browser scripts).
* Excluded: Adding new top-level globals that could collide with `app.js`/`role-screens.js`, changing `h("table", {}, ...)` count, or writing banned content-standard words.

#### Likely Targets

* `src/api/src/zava_forward/api/web/panels.js`: `residentPanel`.

#### Dependencies

* P02-T01.

#### Validation Expectations

* `test_accessibility_baseline.py`, `test_content_standard.py`, and `test_housing_resident_wcag_232.py` verify scrollable region semantics, `<th scope="row">`, non-colour state cues, preserved `Response: ...` / `Remedy: ...` substrings, and zero banned jargon.

#### Completion Evidence

* Passing `residentPanel` WCAG assertions in `test_housing_resident_wcag_232.py` and green `test_accessibility_baseline.py` + `test_content_standard.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused WCAG 2.2 Verification, Web Guidelines Audit, and Local Validation

### Context

Requirement 3 and Requirement 4 mandate focused verification in `src/api/tests/test_housing_resident_wcag_232.py`, strict `ruff` and `mypy` cleanliness in `src/api`, `python3 tools/rename-zava-tests.py`, and AMA Web Development Guidance requires refreshing `web-design-guidelines` before reviewing changed web files (`W1`, `C17`).

### Intent

Prove end-to-end WCAG 2.2 AA baseline coverage for neighbourhood housing officer, contact-centre, and resident engagement staff screens in `src/api/tests/test_housing_resident_wcag_232.py`, audit all changed web files against refreshed Web Interface Guidelines, execute all Focused-tier and coupled regression suites, and record durable implementation evidence in `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`.

### Boundaries

* Included: Creating `src/api/tests/test_housing_resident_wcag_232.py`, refreshing `web-design-guidelines`, running validation suites, and writing `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`.
* Excluded: Mutating `sys.modules`, loosening `src/api/pyproject.toml` strict typing unless genuinely required (not expected because `zava_forward.core.*` override already exists), or claiming human AT sign-off.

### Likely Targets

* `src/api/tests/test_housing_resident_wcag_232.py`: New focused WCAG 2.2 AA verification module.
* `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`: Implementation and validation record.

### Dependencies

* P01, P02.

### Validation Expectations

* `PYTHONPATH=src/core/src:src/core/tests:src/agents/src:src/agents/tests:src/api/src:src/api/tests python3 -m unittest src/api/tests/test_housing_resident_wcag_232.py src/api/tests/test_accessibility_baseline.py src/api/tests/test_content_standard.py -q` exits `0`.
* `(cd src/api && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy src tests)` exits `0`.
* `python3 tools/rename-zava-tests.py` exits `0`.
* Coupled suites (`test_housing_resident_screen_wcag.py`, `test_resident_screen_wcag.py`, `test_frontline_screen_wcag.py`, `test_role_screens.py`, `test_role_screens_conformance.py`, `test_content_standard.py`, `test_specialist_keyboard_check.py`, `test_case_journey.py`, and `test_resident_api.py` including `ZF_RESIDENT_BROWSER=1` if Playwright Chromium is installed) exit `0`.

### Completion Evidence

* Recorded command outputs and zero-finding `file:line` Web Interface Guidelines review in `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Create `src/api/tests/test_housing_resident_wcag_232.py` covering routes, semantics, state text, keyboard/focus, `aria-live`, and safety boundaries

#### Context

Peer suites `#228` (`test_procurement_screen_wcag.py`) and `#231` (`test_technical_quality_screens_wcag.py`) verify rendered DOM trees via Node `vm` + Python core unit tests + CSS/HTML baseline assertions (`C13`–`C17`). Sibling `#231` Review (`RV-001`) highlighted ensuring `json.dumps(..., ensure_ascii=False)` when checking rendered trees for Unicode em dashes so `\u2014` is never masked by JSON ASCII escaping.

#### Intent

Write `src/api/tests/test_housing_resident_wcag_232.py` with full PEP 484 type annotations covering:
1. `#/role/housing_officer`, `#/role/contact_centre`, and `#/role/resident_engagement` routing in `app.js` + `role-screens.js` (`?case=`, `?page=`, `aria-current="page"`, `/ops.js` non-loading, unauthorized `Contractor`/`Application Administrator` `role="alert"` denial).
2. `roleScreensView` `aria-live="polite"` announcements across loading, chooser, invalid-page, unavailable-screen, record-mismatch, and settled states (`#workspace-status` + inline `role="status"` nodes).
3. `resident-choice` and `resident-service-issues` queue/detail rendering: landmarks, heading hierarchy (`h1` -> `h2` -> `h3`), `.table-scroll[role="region"][aria-label][tabindex="0"]`, `<caption>`, `<th scope="col">`, `<th scope="row">`, explicit textual state cues across every choice/readiness/update/safe-route/service/formal-route status (including unmapped `Object.hasOwn` fallback), jump-link programmatic focus + `scrollIntoView`, `show()` programmatic focus on `main#app[tabindex="-1"]` (preserving open `.chat-widget` focus), zero write controls, zero contact triggers (`mailto:`, `tel:`, send/call/SMS/email buttons), zero role simulators, and `ensure_ascii=False` plain-language/ASCII check.
4. `panels.js` (`residentPanel` + `actForm`) rendering: whitespace-free slugified `id`/`for` bindings (`actForm` matching `^[a-z0-9-]+$`), `type="button"` on action controls, `.table-scroll[role="region"][aria-label="Resident decisions by measure"][tabindex="0"]`, `<th scope="row">`, non-colour state cues on contractor and staff views, and preserved contiguous `"Response: <status>. Owner: <name>."` and `"Remedy: <status>. Owner: <name>."` substrings.
5. Backend `projection.py` / `store.resident_choice_queue` / `taskqueues.py` default-deny role gates, deterministic ordering, and `DEFAULT_REASON_ROLES` / `NOTE_HELD` safeguarding redaction, plus AST check forbidding `sys.modules` mutation.

#### Boundaries

* Included: `src/api/tests/test_housing_resident_wcag_232.py` (max new test files: `1`; removals: `none`).
* Excluded: Modifying existing test modules or adding permissive `mypy` ignore overrides unless needed.

#### Likely Targets

* `src/api/tests/test_housing_resident_wcag_232.py`.

#### Dependencies

* P01, P02.

#### Validation Expectations

* Fails if any `#/role/contact_centre` wiring, `aria-live` status update, `panels.js` slugified ID / scrollable region / `<th scope="row">` / state cue, or role gate is reverted; passes cleanly under `unittest`, `ruff`, and `mypy --strict`.

#### Completion Evidence

* Passing execution of `test_housing_resident_wcag_232.py` and strict `mypy` check.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Refresh Web Interface Guidelines, execute Focused-tier and coupled test suites, and reconcile implementation evidence

#### Context

AMA Web Development Guidance requires refreshing `web-design-guidelines` immediately before reviewing changed web files and reporting `file:line` compliance, and `rpi-implement` requires reconciling plan `[x]` markers, phase details, and `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md` before entering `rpi-review`.

#### Intent

Fetch fresh `web-design-guidelines`, review `app.js`, `role-screens.js`, and `panels.js` against all rules, execute all three user-specified validation commands plus coupled WCAG/resident unit suites (including `test_resident_api.py` with `ZF_RESIDENT_BROWSER=1` if Playwright Chromium is available, disclosing any missing browser prerequisite), mark completed tasks `[x]` in the plan, and write `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md` (with post-review git closeout committing with exact title `feat(ux): add WCAG 2.2 keyboard jump nav, row headers and state cues for housing and resident screens (Refs #232)` and trailer, then fetching and rebasing cleanly onto `origin/feat/demo-233-same-home-tensions-0825`).

#### Boundaries

* Included: Read-only guideline refresh + audit, running local validation suites, updating plan/details status markers, and writing the changes artifact.
* Excluded: Unplanned edits outside the approved scope.

#### Likely Targets

* `.copilot-tracking/plans/2026-11-15/housing-resident-wcag-232-plan.md`
* `.copilot-tracking/details/2026-11-15/housing-resident-wcag-232-phase-details.md`
* `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md`

#### Dependencies

* P03-T01.

#### Validation Expectations

* All Focused-tier commands and coupled test suites exit `0` with zero lint, format, type, or Web Interface Guidelines findings.

#### Completion Evidence

* Complete `.copilot-tracking/changes/2026-11-15/housing-resident-wcag-232-changes.md` artifact ready for `rpi-review`.

#### Unresolved Items

* None.
