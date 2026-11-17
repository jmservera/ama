<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #229 Data Steward and Digital Operator Screens WCAG 2.2 Navigation and State Meaning

## Metadata

* Task ID: 229
* Task slug: 229-data-steward-wcag
* Related plan: .copilot-tracking/plans/2026-11-15/229-data-steward-wcag-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/229-data-steward-wcag-research.md (`C1`–`C16`, `W1`)

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Add WCAG 2.2 Keyboard Jump Navigation and Textual State Meaning to Data Steward and Operator Screens | Complete | P01, P01-T01, P01-T02 |
| P02 | Expand WCAG 2.2 Unit Tests, Update UX Delivery Record, and Validate | Complete | P02, P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Add WCAG 2.2 Keyboard Jump Navigation and Textual State Meaning to Data Steward and Operator Screens

### Context

`src/api/src/zava_forward/api/web/role-screens.js` registers `data-operator` ("Data steward and operator view"). Commit `bcf2e8cf5` (`#1693`) added `exceptionJumpNav()` and `indicatorRows` ("State at a glance") to `exceptionRegisterPanel(data)` (`?exceptions=1`), but `data-operator.render(c)` (selected-home view) and `overview(signal, rows, c)` / `summary(entries)` (default overview and page-level conflict/return queue) still lack keyboard jump navigation, `tabindex="-1"` section targets, and explicit `State:` / `Source state:` prefixes (`C5`, `C6`).

### Intent

Equip `data-operator` with keyboard-accessible section jump navigation (`<nav aria-label="...">` with native `<a data-jump="...">` controls targeting `<section id="..." tabindex="-1">` landmarks/cards) and fail-closed non-colour textual state labels across every conflict, source-detail, eligibility, return/reopen, handoff, prerequisite, event, recovery, and exception-register indicator.

### Boundaries

* Included: `operator*` and `exception*` helpers and `data-operator` rendering in `src/api/src/zava_forward/api/web/role-screens.js`.
* Excluded: Backend Python API endpoints, `role-screens.js:268-275` shared `a[data-jump]` click listener formatting (`C3`), CSS token definitions in `style.css`, and any write/replay/simulator controls.

### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`: Define `operator*` section/state helpers around `operatorSide`/`operatorStatus` and apply them in `exceptionRegisterPanel`, `exceptionRegisterEntry`, `overview`, `summary`, and `render`.

### Dependencies

* Reuses `screenJumpNav(label, jumps)` (`role-screens.js:29-32`) and the delegated `a[data-jump]` click handler (`role-screens.js:268-275`).

### Validation Expectations

* `test_data_operator_screen.py`, `test_exception_register_screen.py`, `test_data_operator_ai_state.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_role_screens_conformance.py`, `test_specialist_keyboard_check.py`, `test_asset_exec_screen_wcag.py`, `test_finance_screens_wcag_225.py`, and `test_safety_screen_wcag_keyboard.py` all pass.

### Completion Evidence

* Clean diff in `src/api/src/zava_forward/api/web/role-screens.js` satisfying FR-1, FR-2, FR-3, and NFR-1.

### Unresolved Items

* None

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add fail-closed textual state helpers and section jump helpers for `data-operator`

#### Context

Research `C4`, `C7`, `C9`, `C11`, and `C13` established five helper-design constraints:
1. Top-level identifiers in `role-screens.js` must not collide with `app.js` (`RoleScreensGlobalScope`, `C4`).
2. Helpers must be defined near `operatorSide`/`operatorStatus` (before `async function exceptionRegisterView`) because `test_data_operator_screen.py:185-189` forbids `"method"`, `"onclick"`, `"POST"`, `"innerHTML"`, and `"fetch("` in the source slice between `async function exceptionRegisterView` and `registerRoleScreen` (`C9`).
3. UI literals must never contain banned terms matching `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b` (`test_content_standard.py`, `C13`) or `"No outage recorded"`, `"audit trail"`, `"audit history"` in the register panel (`data_operator_ai_state.py`, `C11`).
4. Synthetic fixtures supply `"Unverified"` (`role_screens_fixtures.py:67`), `"Unvalidated"` (`test_data_operator_screen.py:16`), and `"Validated"` (`C7`, `C11`).
5. Unrecognised, missing, non-string, colour-only (`"green"`, `"amber"`, `"red"`), or `Object.prototype` keys (`"constructor"`, `"toString"`) must fail closed to `Unknown` via `Object.hasOwn` (`C8`).

#### Intent

Define deterministic, fail-closed `operator*` and `exception*` state and panel helpers in `role-screens.js`:
* `operatorPanel(id, title, ...children)`: returns `h("section", { class: "card screen-record", id, tabindex: "-1" }, h("h2", {}, title), ...children)`. Explicitly omit `aria-labelledby` and `aria-label` on `<section>` so `<section>` does not become a duplicate-named `region` landmark colliding with inner `screenTable` `div.table-scroll[role="region"][aria-label=...]` containers (`PC-005`).
* `operatorJumps`: six `[id, label]` entries for `render(c)`:
  * `["operator-boundary", "Evidence boundary"]`
  * `["operator-conflicts", "Conflict queue"]`
  * `["operator-eligibility", "Eligibility and original source"]`
  * `["operator-returns", "Returns and reopens"]`
  * `["operator-handoff", "Handoff and exception queue"]`
  * `["operator-events", "Event metadata and recovery context"]`
* `operatorLookup(map, value, fallback)`: returns `typeof value === "string" && Object.hasOwn(map, value.trim().toLowerCase()) ? map[value.trim().toLowerCase()] : fallback`.
* `operatorSourceStates` & `operatorSourceState(value)`: `operatorLookup` mapping `validated` -> `"Source state: Validated on record (not a winning source)"`, `verified` -> `"Source state: Verified on record (not a winning source)"`, `unvalidated` -> `"Source state: Unvalidated (needs steward check)"`, `unverified` -> `"Source state: Unverified (needs steward check)"`, `disputed` -> `"Source state: Disputed (action needed; sources disagree)"`, `quarantined` -> `"Source state: Quarantined (not cleared for use)"`, `stale` -> `"Source state: Stale (needs refresh check)"`, `unknown` -> `"Source state: Unknown"`, and any other/missing/colour/prototype value -> `"Source state: Unknown"` (`PC-001`, `PC-003`).
* `operatorSide(a)`: when `exceptionRecord(a)`, returns `` `${screenValue(a.value)}; source ${screenValue(a.source_id)} v${screenValue(a.version)}; dated ${screenValue(a.date)}; ${operatorSourceState(a.validation_state)}` `` (never echoing raw `a.validation_state` so colour-only or prototype tokens cannot leak, `PC-003`); when missing, returns `"Source state: Unknown"`.
* `operatorEventStates` & `operatorEventState(value)`: `operatorLookup` mapping `unresolved` -> `"State: Unresolved (action needed; both source values kept)"`, `open` -> `"State: Open (action needed; waiting for steward review)"`, `withdrawn` -> `"State: Withdrawn (recorded disposition; not a winning source)"`, `reconciled` -> `"State: Reconciled on record"`, `resolved` -> `"State: Resolved on record (recorded disposition only)"`, `returned` -> `"State: Returned (action needed)"`, `quarantined` -> `"State: Quarantined (not cleared for use)"`, and any other/missing/colour/prototype value -> `"State: Unknown"` (`PC-001`).
* `operatorStatus(c, q)`: resolves the last matching `stock_reconciliation_events` entry for `q.id`; if no event exists for `q.id`, returns `operatorEventStates.unresolved`; if an event exists, passes `lastEvent.status` to `operatorEventState` so an event with missing/malformed/colour-only status fails closed to `"State: Unknown"`.
* `operatorReturnState(r)`: returns `r.reopened ? "State: Reopened (action needed)" : "State: Returned (action needed)"`.
* `operatorHandoffStates` & `operatorHandoffState(value)`: `operatorLookup` mapping `offered` -> `"State: Offered, awaiting acceptance (action needed)"`, `sent` -> `"State: Sent, awaiting acceptance (action needed)"`, `received` -> `"State: Received, awaiting acceptance (ownership unchanged; action needed)"`, `pending` -> `"State: Pending acceptance (action needed)"`, `escalated` -> `"State: Escalated (unaccepted handoff; action needed)"`, `declined` -> `"State: Declined by receiver (action needed)"`, `rejected` -> `"State: Rejected by receiver (action needed)"`, `returned` -> `"State: Returned (action needed)"`, `accepted` -> `"State: Accepted by receiver"`, `confirmed` -> `"State: Confirmed by receiver"`, `withdrawn` -> `"State: Withdrawn on record"`, `completed` -> `"State: Completed on record"`, `blocked` -> `"State: Blocked (action needed)"`, and any other/missing value -> `"State: Unknown (handoff not confirmed)"` (`PC-001`).
* `operatorBlockerStates` & `operatorBlockerState(b)`: inspects blocker object `b`: if `!exceptionRecord(b)`, returns `"State: Unknown"`; if `Object.hasOwn(b, "status")`, looks up `b.status` via `operatorBlockerStates` (`open` -> `"State: Open prerequisite (action needed)"`, `blocked` -> `"State: Blocked (action needed)"`, `resolved` -> `"State: Resolved on record"`, else `"State: Unknown"`); else if `Object.hasOwn(b, "current_stop")`, maps `b.current_stop === true` -> `"State: Active stop on current stage (action needed)"`, `b.current_stop === false` -> `"State: Open prerequisite (does not stop current stage; action needed)"`, and non-boolean -> `"State: Unknown"`; else returns `"State: Open prerequisite (action needed)"` (`PC-001`).
* `exceptionRegisterState(state)`, `exceptionItemState(status)`, & `exceptionEligibilityState(value)`: fail-closed `operatorLookup` helpers for `exceptionRegisterPanel` mapping register `state` `ok` -> `"State: Loaded (ok; not an all clear)"`, `roles_not_named` -> `"State: Action needed (roles_not_named)"`, other -> `"State: Unknown"` (never echoing raw `state`, `PC-003`); item `status` `open` -> `"State: Open (action needed)"`, `quarantined` -> `"State: Quarantined (not cleared for use)"`, `held` -> `"State: Paused for human review (held; action needed)"` (avoiding banned `\bholds?\b`), `rerun_requested` -> `"State: Re-run requested (human action needed; not replayed)"`, `closed` -> `"State: Closed on record"`, other/missing -> `"State: Unknown"` (`PC-001`); and `eligibility` `unknown` -> `"Unknown"`, `not assessed` / `not_assessed` -> `"Not assessed"`, `suppressed` -> `"Suppressed"`, other/missing -> `"Unknown"` (`PC-003`). CSV export `exceptionSummaryRows` remains untouched.

#### Boundaries

* Included: Helper definitions in `role-screens.js`.
* Excluded: CSV export row serialization (`exceptionSummaryRows` / `exceptionSummaryCsv`), which is pinned byte-for-byte by `test_exception_register_screen.py` and `data_operator_browser_check.py`.

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`

#### Dependencies

* None

#### Validation Expectations

* Verified by unit tests in `P02-T01` and lexical/global-scope checks (`test_content_standard.py`, `test_safety_screen_wcag_keyboard.py`).

#### Completion Evidence

* Helpers present in `role-screens.js` with zero banned terms and zero global-scope clashes.

#### Unresolved Items

* None

<!-- rpi:task id=P01-T02 -->
### P01-T02: Wire keyboard jump navigation, `tabindex="-1"` section targets, and explicit textual state labels into `data-operator` and `exceptionRegisterPanel`

#### Context

`data-operator` renders three user surfaces (`C5`, `C6`, `C9`, `C10`, `C11`, `C14`):
1. `render(c)` (selected-home view): six `screenPanel` sections with no jump nav.
2. `overview(signal, rows, c)` (no home selected): renders `exceptionRegisterView(signal)` when `?exceptions=1`, or `exceptionRegisterEntry()` plus `this.summarise(rows, signal)` when `rows.length > 0`.
3. `summary(entries)` (page-level conflict and return queue): must contain zero `<a>` or `<button>` controls inside its returned panel (`test_data_operator_screen.py:157-158`), while `overview` with `rows == []` and no `exceptions=1` must contain exactly 1 `<a>` (`test_exception_register_screen.py:228-229`).

#### Intent

Update `exceptionUnavailable`, `exceptionRegisterPanel`, `exceptionRegisterEntry`, `overview`, `summary`, and `render` in `role-screens.js`:
* In `exceptionUnavailable(error)` and `exceptionRegisterPanel(data)`:
  * Convert outer `screenPanel("Exception register", ...)` to `operatorPanel("operator-register", "Exception register", ...)` (`PC-002`).
  * Format `Register state` via `exceptionRegisterState(data.state)` (keeps `"roles_not_named"` substring while failing closed to `"State: Unknown"` without echoing untrusted strings, `PC-003`).
  * Format the `"State"` column in `"Exception items returned for you"` via `exceptionItemState(item.status)` without altering column order (`Reference`, `Kind`, `State`, `Configured owner`, `What happened and reason`, `Manual next step`, `Source or run reference`, `Eligibility`) or `exceptionSummaryRows`.
  * Format `"Eligibility"` cells in `"Exception items returned for you"` (`State: ${exceptionEligibilityState(item.eligibility)}`) and `"Source conflicts with every returned value"` (`State: ${exceptionEligibilityState(item.eligibility)}. No winning source is selected.`, preserving `"Unknown. No winning source is selected."` substring while failing closed on untrusted inputs, `PC-003`).
* In `exceptionRegisterEntry()`:
  * Replace `screenPanel("Exception register", ...)` with `operatorPanel("operator-register-entry", "Exception register", ...)`.
* In `overview(signal, rows, c)`:
  * Compute `const isExceptions = screenScopeQuery().get("exceptions") === "1";`.
  * When `summary` is truthy (`!c && rows.length > 0`), render `screenJumpNav("Data steward overview sections", [[isExceptions ? "operator-register" : "operator-register-entry", "Exception register"], ["operator-page-queue", "Conflict and return queue"]])` at the top of the returned `div` before `register` and `summary` (`PC-002`). When `summary` is `null` (`rows` empty or `c` selected), omit the overview jump nav so single-panel `entry` keeps `len(links) == 1` and empty-rows `exceptions=1` keeps `len(navs) == 1`.
* In `summary(entries)`:
  * Keep a single `operatorPanel("operator-page-queue", "Conflict and return queue across this page of homes", ...)` containing both tables (`data_operator_browser_check.py:121-140`, `PC-002`).
  * Add plain-language non-colour state cue sentence in the intro paragraph (`"Every state is written in words with a State or Source state label, so meaning never relies on colour alone."`).
  * Use `operatorSide`, `operatorStatus`, `operatorReturnState`, and explicit `"State: Unavailable (action needed; not clear)"` / `"Source state: Unknown (Unavailable)"` in unavailable home rows while preserving `"Unavailable"` and `"Open the home to check."`.
* In `render(c)`:
  * Render `screenJumpNav("Data steward and operator sections", operatorJumps)` as the first child of the root `div`.
  * Convert all six `screenPanel(...)` calls to `operatorPanel(id, title, ...)` matching `operatorJumps` (`operator-boundary`, `operator-conflicts`, `operator-eligibility`, `operator-returns`, `operator-handoff`, `operator-events`).
  * Add plain-language non-colour state cue sentence in `operator-boundary` (`"Every state is written in words with a State or Source state label, so meaning never relies on colour alone."`).
  * Update `Eligibility and original source` fields:
    * `["Eligibility", "State: Unknown. Unresolved on this screen; not confirmed or cleared."]`
    * `["Original source values", queries.length ? "State: Preserved unchanged in the table above" : "State: Unknown (none supplied)"]`
    * `["Winning source", "State: Not selected. No latest-wins or silent correction is applied."]`
  * Update `Returns and reopens` table `"Type"` cell to `operatorReturnState(r)`.
  * Update `Handoff and exception queue`:
    * `["Handoff state", operatorHandoffState(handoff.state)]`
    * Add `"State"` column to `"Open exceptions and prerequisites"` (`["Step", "State", "Reason", "Owner", "Next action", "Source and version"]`) using `operatorBlockerState(b)`.
  * Update `Event metadata and recovery context`:
    * Format `"State"` column of `"Recorded stock query events"` with `operatorEventState(e.status)`.
    * Format `"Recovery context"` as `` work ? `State: Action needed. Next action: ${screenValue(work.next_action)}. Owner: ${screenValue(work.owner)}. Recorded as of ${screenValue(work.as_of)}.` : "State: Unknown. No recovery context is recorded." ``.
    * Format `"Integration run and queue state"` as `"State: Unknown. No interface run record is supplied to this screen."`.

#### Boundaries

* Included: `data-operator` and `exceptionRegisterPanel` VDOM rendering in `role-screens.js`.
* Excluded: Other role screens (`asset-board`, `safety-lead`, `finance-invoices`, `procurement-packages`, etc.).

#### Likely Targets

* `src/api/src/zava_forward/api/web/role-screens.js`

#### Dependencies

* `P01-T01`

#### Validation Expectations

* All existing tests in `test_data_operator_screen.py`, `test_exception_register_screen.py`, `test_data_operator_ai_state.py`, and `test_data_steward_screen_wcag.py` pass without weakening a single assertion.

#### Completion Evidence

* Rendered VDOM trees for `render(c)`, `overview`, `summary`, and `exceptionRegisterPanel` expose all jump links, `tabindex="-1"` targets, and `State:` / `Source state:` prefixes.

#### Unresolved Items

* None

<!-- rpi:phase id=P02 -->
## P02: Expand WCAG 2.2 Unit Tests, Update UX Delivery Record, and Validate

### Context

`src/api/tests/test_data_steward_screen_wcag.py` is discovered by the caller's required pattern `"test_*data_steward*.py"`, and currently contains 10 tests covering `exceptionRegisterView` (`?exceptions=1`) only (`C8`). Expanding `test_data_steward_screen_wcag.py` gives direct semantic and regression coverage of the newly added `data-operator.render(c)`, `overview`/`summary(entries)`, and `exceptionRegisterPanel` WCAG 2.2 features.

### Intent

Add focused, high-signal WCAG 2.2 unit/accessibility tests in `src/api/tests/test_data_steward_screen_wcag.py`, update `docs/reference/research/ux/customer-journeys/data.md` and `docs/reference/log.md` to record the `#229` engineering accessibility slice honestly, run all focused validation suites (`unittest`, `mypy`, `ruff`) plus refreshed `web-design-guidelines` review, and verify clean repository status.

### Boundaries

* Included: `src/api/tests/test_data_steward_screen_wcag.py`, `docs/reference/research/ux/customer-journeys/data.md`, `docs/reference/log.md`, and local validation execution.
* Excluded: Modifying existing assertions in `test_data_operator_screen.py` or `test_accessibility_baseline.py` (which must remain untouched regression witnesses), ticking `#229` acceptance checkboxes, or pushing to remote.

### Likely Targets

* `src/api/tests/test_data_steward_screen_wcag.py`: Add `DataOperatorHomeAndOverviewWcag` (or methods on `DataStewardScreenWcag`) covering AC-1 through AC-4.
* `docs/reference/research/ux/customer-journeys/data.md`: Note the 2026-11-15 WCAG 2.2 keyboard jump navigation and textual state-meaning slice under `Data screens delivery status` while keeping `#151`/`#155` human AT validation explicitly unmet.
* `docs/reference/log.md`: Append a dated `2026-11-15` entry for `data.md`.

### Dependencies

* `P01`

### Validation Expectations

* `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m unittest discover -s tests -p "test_*data_steward*.py" -q` passes.
* Combined affected regression run (`test_data_operator_screen.py`, `test_data_operator_ai_state.py`, `test_exception_register_screen.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_role_screens_conformance.py`, `test_specialist_keyboard_check.py`, `test_connected_home_check.py`, `test_screen_design_traceability.py`, `test_ux_design_traceability.py`, `test_asset_exec_screen_wcag.py`, `test_finance_screens_wcag_225.py`, `test_safety_screen_wcag_keyboard.py`) passes.
* `python3 -m mypy` and `python3 -m ruff check src tests && python3 -m ruff format --check src tests` pass in `src/api`.
* Fresh `web_fetch` of `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` and `file:line` review of `role-screens.js` finds zero open issues.

### Completion Evidence

* Passing command outputs recorded in `.copilot-tracking/changes/2026-11-15/229-data-steward-wcag-changes.md`.

### Unresolved Items

* None

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add focused WCAG 2.2 keyboard jump-link, `tabindex="-1"`, and textual state tests in `test_data_steward_screen_wcag.py`

#### Context

Locked test plan before critique:
* Canonical test target: `src/api/tests/test_data_steward_screen_wcag.py` (matches `"test_*data_steward*.py"`).
* Exact removals: `none` (all 10 existing `DataStewardScreenWcag` test methods remain untouched).
* Maximum additions: `<= 10` focused test methods covering semantic WCAG 2.2 behaviour and fail-closed edge cases that would fail without `P01`:
  1. `test_home_view_jump_nav_links_target_focusable_sections`: verifies `<nav aria-label="Data steward and operator sections">` has 6 native `<a href="#..." data-jump="...">` links, every target `<section class="card screen-record" id="..." tabindex="-1">` starts with `<h2>`, and no other arbitrary `-1` or positive `tabindex` removes content from focus order.
  2. `test_delegated_jump_link_click_focuses_section_without_hash_change`: executes `role-screens.js` with a mock `document.addEventListener("click", ...)` harness (like `test_finance_screens_wcag_225.py`), clicks every `a[data-jump]` in `render(c)` and two-panel `overview`, and verifies `preventDefault()` is called, `location.hash` stays `#/screens?screen=data-operator&case=C-1`,each target `<section>` receives `.focus()`, and non-jump links (`Open the exception register`) are not intercepted.
  3. `test_overview_jump_nav_targets_matching_register_and_page_queue_in_dom_order`: verifies `overview` with non-empty `rows` renders `<nav aria-label="Data steward overview sections">` as first child targeting `operator-register-entry` + `operator-page-queue` (default) and `operator-register` + `operator-page-queue` (`exceptions=1`, both loaded and 403/503 unavailable), while `overview` with `rows=[]` renders zero overview jump nav and `s.summary(...)` contains zero `<a>` or `<button>` elements.
  4. `test_home_conflict_source_return_handoff_and_event_states_are_written_out`: verifies `render(c)`, `summary(entries)`, and `exceptionRegisterPanel` emit explicit `Source state:` and `State:` labels across canonical `zava_forward.core` states (`Unvalidated`, `Unverified`, `Validated`, `Disputed`, `Unresolved`, `Withdrawn`, `Reconciled`, `Returned`, `Reopened`, `Unavailable`, `Offered`, `Received`, `Escalated`, `Declined`, `Completed`, `current_stop: true/false`, `held`, `rerun_requested`, `Not assessed`, `Suppressed`).
  5. `test_home_and_register_states_fail_closed_on_missing_colour_or_prototype_keys`: verifies colour-only values (`"green"`, `"red"`), false-assurance values (`"Pass"`, `"Healthy"`, `"Clear"`), numeric/null values, and `Object.prototype` keys (`"constructor"`, `"toString"`, `"__proto__"`) in `validation_state`, `stock_reconciliation_events[].status`, `handoff.state`, `blockers[].status` / `current_stop`, and `exceptionRegisterPanel` `state`/`items[].status`/`items[].eligibility` all render `State: Unknown` or `Source state: Unknown` and never echo `"Pass"`, `"Healthy"`, `"Clear"`, `"green"`, or `"constructor"`.
  6. `test_home_and_summary_tables_are_keyboard_focusable_named_and_scoped`: verifies every rendered `table` in `render(c)` and `summary(entries)` has a non-empty `<caption>`, `<th scope="col">` headers, and an enclosing `<div class="table-scroll" role="region" aria-label="..." tabindex="0">`, `<section>` omits `aria-labelledby`/`aria-label` so landmarks never collide, and zero `<button>`, `<input>`, `<select>`, `<textarea>`, `onclick`, or `aria-invalid` attributes exist.

#### Intent

Provide focused, strictly typed (`mypy`-clean, `ruff`-clean) automated WCAG 2.2 tests in `src/api/tests/test_data_steward_screen_wcag.py`.

#### Boundaries

* Included: `src/api/tests/test_data_steward_screen_wcag.py`.
* Excluded: Trivial constant restatements or modifying existing assertions in `test_data_operator_screen.py`.

#### Likely Targets

* `src/api/tests/test_data_steward_screen_wcag.py`

#### Dependencies

* `P01-T01`, `P01-T02`

#### Validation Expectations

* `test_*data_steward*.py`, `mypy`, and `ruff` pass with zero warnings/errors.

#### Completion Evidence

* New tests fail against unpatched `role-screens.js` semantics and pass with `P01` applied.

#### Unresolved Items

* None

<!-- rpi:task id=P02-T02 -->
### P02-T02: Update UX delivery status documentation, run focused validation and Web Interface Guidelines review

#### Context

Repository instructions require keeping directly related UX documentation current (`docs/reference/research/ux/customer-journeys/data.md` and `docs/reference/log.md` when a knowledge-base synthesis changes materially), refreshing `web-design-guidelines` before reviewing changed web files, and classifying validation tier (`focused` tier: small UI/test slice with no SQL, infra, workflow, Dockerfile, dependency-manifest, or security-control edits).

#### Intent

1. Update `docs/reference/research/ux/customer-journeys/data.md` inside `## Data screens delivery status (2026-11-04, #229)` (keeping that exact H2 heading verbatim so `#data-screens-delivery-status-2026-11-04-229` in `screen-design-traceability.md:55` resolves cleanly, `PC-004`) to note the 2026-11-15 WCAG 2.2 keyboard section jump navigation (`tabindex="-1"` section targets, delegated `a[data-jump]`) and fail-closed `State:` / `Source state:` labels across per-home, overview, and exception-register views while preserving the unmet `#151`/`#155` human assistive-technology boundary, and append one entry to `docs/reference/log.md`.
2. Re-fetch `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` and audit all changed lines of `src/api/src/zava_forward/api/web/role-screens.js`.
3. Run focused validation commands in `src/api`:
   * `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m unittest discover -s tests -p "test_*data_steward*.py" -q`
   * Focused regression runner covering `test_data_operator*.py`, `test_exception_register_screen.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_role_screens_conformance.py`, `test_specialist_keyboard_check.py`, `test_connected_home_check.py`, `test_screen_design_traceability.py`, `test_ux_design_traceability.py`, `test_asset_exec_screen_wcag.py`, `test_finance_screens_wcag_225.py`, and `test_safety_screen_wcag_keyboard.py`
   * Touched local browser checks `PYTHONPATH=.:src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m checks.data_operator_browser_check` and `python3 -m checks.specialist_keyboard_browser_check` (or explicit disclosure if Chromium/axe runtime prerequisites are unavailable in this environment, `PC-005`)
   * `python3 -m mypy`
   * `python3 -m ruff check src tests && python3 -m ruff format --check src tests`

#### Boundaries

* Included: `docs/reference/research/ux/customer-journeys/data.md`, `docs/reference/log.md`, and focused verification runs.
* Excluded: Rewriting earlier entries in `docs/reference/log.md` or claiming WCAG 2.2 conformance (`Closes #229`).

#### Likely Targets

* `docs/reference/research/ux/customer-journeys/data.md`
* `docs/reference/log.md`

#### Dependencies

* `P02-T01`

#### Validation Expectations

* Markdown relative links resolve, traceability tests (`test_screen_design_traceability.py`, `test_ux_design_traceability.py`) pass, and all Python/JS checks exit `0`.

#### Completion Evidence

* Validation transcript and `web-design-guidelines` findings recorded in `.copilot-tracking/changes/2026-11-15/229-data-steward-wcag-changes.md`.

#### Unresolved Items

* None
