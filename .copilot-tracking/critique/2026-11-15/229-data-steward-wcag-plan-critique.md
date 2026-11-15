<!-- markdownlint-disable-file -->
# RPI Plan Critique: Data steward and digital operator screens WCAG 2.2 keyboard jump navigation and textual state meaning (#229)

## Metadata

* Task ID: 229
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/229-data-steward-wcag-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/229-data-steward-wcag-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Add full WCAG 2.2 keyboard jump navigation (`<nav aria-label>` jump links to main sections, `tabindex="-1"` on target sections, explicit non-colour textual state meaning on all conflict, return, source-validation, handoff, blocker, recovery, and exception indicators, and keyboard-accessible controls) on `data-operator` matching `#226`, `#227`, and `#225`; expand `src/api/tests/test_data_steward_screen_wcag.py` (matched by `-p "test_*data_steward*.py"`); pass focused `unittest`, regression suites, `mypy`, and `ruff`; and commit locally on `feat/ux-229-data-steward-wcag` with `Refs #229` and Copilot `Co-authored-by` trailer without pushing.
* Research and evidence considered: `.copilot-tracking/research/2026-11-15/229-data-steward-wcag-research.md`, `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/style.css`, `src/api/src/zava_forward/api/web/index.html`, `src/core/src/zava_forward/core/stock.py`, `src/core/src/zava_forward/core/workflows.py`, `src/core/src/zava_forward/core/taskqueues.py`, `src/core/src/zava_forward/core/exception_register.py`, `src/core/src/zava_forward/core/exception_queue.py`, `src/api/tests/test_data_steward_screen_wcag.py`, `src/api/tests/test_data_operator_screen.py`, `src/api/tests/test_exception_register_screen.py`, `src/api/tests/test_data_operator_ai_state.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_content_standard.py`, `src/api/tests/test_specialist_keyboard_check.py`, `src/api/tests/test_screen_design_traceability.py`, `src/api/checks/data_operator_browser_check.py`, `src/api/checks/specialist_keyboard_browser_check.py`, `docs/reference/research/ux/customer-journeys/data.md`, and `docs/reference/research/ux/screen-design-traceability.md`.
* Decisions, dependencies, and acceptance criteria considered: `FR-1` through `FR-3`, `NFR-1`, `NFR-2`, `AC-1` through `AC-5`, `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`, `P02-T02`), lexical bans in `test_content_standard.py`, frozen CSV export contract (`exceptionSummaryRows`), and read-only DOM/landmark invariants.
* Assessment boundary: Evaluates plan and phase-detail accuracy, core domain vocabulary completeness, DOM/landmark/anchor invariants, fail-closed state semantics, regression test compatibility, and documentation traceability from repository sources; does not execute live Playwright browser sessions or modify plan/source files.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1, AC-1 (Named jump navs & unique `tabindex="-1"` targets) | Partial | Selected-home and exception-register sub-section targets are sound, but `P01-T02` places overview jump nav inside `data-operator.summary(entries)` targeting `#operator-register-entry`, which breaks on `exceptions=1` and standalone `summarise()`, and renders below the first section (`PC-002`). |
| FR-2, AC-2 (Shared `a[data-jump]` focus-then-scroll activation) | Covered | Reuses existing delegated `document.addEventListener("click", ...)` handler (`role-screens.js:268-275`) and `screenJumpNav` (`role-screens.js:29-32`) with native `<a class="btn alt">` keyboard activation and zero extra `<button>` controls. |
| FR-3, AC-3 (Explicit textual state labels & fail-closed `Unknown`) | Partial | `P01-T01` allowlists omit real core domain states (`Reconciled`, `Disputed`, `Offered`/`Received`/`Escalated`/`Declined`/`Withdrawn`/`Completed`, `held`/`rerun_requested`, and `current_stop` booleans) (`PC-001`), and `operatorSide`, `exceptionRegisterState`, and `Eligibility` cells leak raw colour/prototype tokens (`PC-003`). |
| NFR-1 (Plain-language lexical guard & frozen CSV contract) | Covered | All planned strings avoid `BANNED` regex `\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b` in `src/api/tests/test_content_standard.py:14`, and `exceptionSummaryRows` (`role-screens.js:1120-1129`) remains unchanged. |
| NFR-2, AC-4 (Existing regression & traceability compatibility) | Partial | Existing DOM/CSV/AI-state tests remain compatible once `PC-002` is fixed, but `P02-T02` does not guard `#data-screens-delivery-status-2026-11-04-229` enforced by `test_screen_design_traceability.py` (`PC-004`) or include `operatorPanel` landmark-collision guard and local browser checks (`PC-005`). |
| AC-5 (Focused validation & local commit on `feat/ux-229-data-steward-wcag`) | Covered | Branch, commit trailer, `Refs #229`, and no-push constraints are explicitly planned in `plan.md` and `P02-T02`. |
| P01, P01-T01 (Helper maps & `operatorPanel`) | Partial | Needs core state vocabulary additions (`PC-001`), strict fail-closed output without raw input echoing (`PC-003`), and explicit no-`aria-labelledby` guard on `operatorPanel` (`PC-005`). |
| P01-T02 (`data-operator` & `exceptionRegisterPanel` wiring) | Partial | Needs overview jump nav moved from `summary(entries)` to `overview(signal, rows, c)` plus `operatorPanel` on `exceptionUnavailable` (`PC-002`), and fail-closed `Eligibility` helper (`PC-003`). |
| P02, P02-T01 (`test_data_steward_screen_wcag.py` expansion) | Partial | Test #5 already catches raw `"green"`/`"constructor"` leaks that `P01-T01` currently emits (`PC-003`), and needs cases for core domain states (`PC-001`) and `exceptions=1` + overview composition (`PC-002`). |
| P02-T02 (Documentation update & validation commands) | Partial | Needs H2 anchor preservation in `customer-journeys/data.md`, `docs/reference/log.md` update, `test_screen_design_traceability.py`, and local Playwright check execution/disclosure (`PC-004`, `PC-005`). |

## Verdict

* Verdict: Revise
* Rationale: Three high/critical defects in `P01-T01` and `P01-T02` would regress real backend state rendering, produce a broken `#operator-register-entry` jump link when `exceptions=1` is open alongside page summaries, and cause `P02-T01`'s own fail-closed test to fail by echoing raw untrusted tokens (`"green"`, `"constructor"`). All five findings have deterministic, evidence-backed fixes that the planning parent can apply directly without user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Critical]: Planned `Object.hasOwn` state maps omit canonical core backend states and collapse `work.blockers[].current_stop`

* Related IDs: `FR-3`, `AC-3`, `P01`, `P01-T01`, `P01-T02`, `P02-T01`
* Evidence: `.copilot-tracking/details/2026-11-15/229-data-steward-wcag-phase-details.md` (`P01-T01` lines 90-97, `P01-T02` lines 133-138); `src/core/src/zava_forward/core/stock.py` (lines 98, 143, 159); `src/core/src/zava_forward/core/workflows.py` (lines 17-20, 211, 245-248); `src/core/src/zava_forward/core/taskqueues.py` (lines 11, 32-34, 276-286, 348-383); `src/core/src/zava_forward/core/exception_register.py` (lines 46-50, 238); `src/api/src/zava_forward/api/web/role-screens.js` (lines 189, 1322)
* Concern: Four planned allowlist maps omit canonical values stored and returned by `zava_forward.core`:
  1. `operatorHandoffStates` maps only `pending`, `returned`, `accepted`, `confirmed`, and `blocked`, omitting 6 of the 7 real `handoff.state` values in `workflows.py` (`"Offered"`, `"Received"`, `"Escalated"`, `"Declined"`, `"Withdrawn"`, `"Completed"`, plus `HANDOFF_STATUS` aliases `"Sent"` and `"Rejected"`).
  2. `operatorEventStates` maps `resolved` and `withdrawn` but omits `"reconciled"`, even though `stock.py:143, 159` enforces `event["status"] in ("Withdrawn", "Reconciled")` and stores `"Reconciled"` for every resolved stock conflict.
  3. `operatorSourceStates` omits `"disputed"`, even though `stock.py:98` enforces `validation_state in ("Unvalidated", "Validated", "Disputed", "Unknown")`.
  4. `exceptionItemState` omits `"held"` and `"rerun_requested"` from `exception_register.py:46-50` (`RECOVERY_STATUS`).
  5. `operatorBlockerState(b.status)` inspects only `b.status`, ignoring `b.current_stop` (`True` vs `False`) emitted by `taskqueues.py:276-286, 348-383` to distinguish active current-stage stops from future-step prerequisites.
* Impact: Valid store records for reconciled stock conflicts, disputed source assertions, active/completed/declined/withdrawn/escalated handoffs, and recorded exception recovery requests (`held`, `rerun_requested`) will falsely render as `State: Unknown` or `Source state: Unknown`, destroying recorded operational meaning that `role-screens.js` currently displays.
* Smallest useful change: Update `P01-T01` and `P01-T02` so:
  1. `operatorHandoffStates` adds `offered` (`"State: Offered, awaiting acceptance (action needed)"`), `sent` (`"State: Sent, awaiting acceptance (action needed)"`), `received` (`"State: Received, awaiting acceptance (ownership unchanged; action needed)"`), `escalated` (`"State: Escalated (unaccepted handoff; action needed)"`), `declined` (`"State: Declined by receiver (action needed)"`), `rejected` (`"State: Rejected by receiver (action needed)"`), `withdrawn` (`"State: Withdrawn on record"`), and `completed` (`"State: Completed on record"`).
  2. `operatorEventStates` adds `reconciled` (`"State: Reconciled on record"`).
  3. `operatorSourceStates` adds `disputed` (`"Source state: Disputed (action needed; sources disagree)"`).
  4. `exceptionItemState` adds `held` (`"State: Paused for human review (held; action needed)"` -- avoiding banned `\bholds?\b`) and `rerun_requested` (`"State: Re-run requested (human action needed; not replayed)"`).
  5. `operatorBlockerState(b)` accepts the blocker object `b`: if `Object.hasOwn(b, "status")`, look up `b.status` via `operatorBlockerStates` (failing closed to `"State: Unknown"` on null/numeric/unknown); else if `Object.hasOwn(b, "current_stop")`, map `true` -> `"State: Active stop on current stage (action needed)"`, `false` -> `"State: Open prerequisite (does not stop current stage; action needed)"`, and non-boolean -> `"State: Unknown"`; else (synthetic fixture without either key) return `"State: Open prerequisite (action needed)"`. Expand `P02-T01` test #3/#4 to assert these canonical core states.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01`, `P01-T02`, and `P02-T01` in `.copilot-tracking/details/2026-11-15/229-data-steward-wcag-phase-details.md` listing every canonical `stock.py`, `workflows.py`, `taskqueues.py`, and `exception_register.py` state value and matching unit assertions.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Placing overview jump navigation inside `data-operator.summary(entries)` creates a broken `#operator-register-entry` link on `exceptions=1` and renders out of DOM order

* Related IDs: `FR-1`, `FR-2`, `AC-1`, `AC-2`, `P01`, `P01-T02`, `P02-T01`
* Evidence: `.copilot-tracking/details/2026-11-15/229-data-steward-wcag-phase-details.md` (`P01-T02` line 139, `P02-T01` line 213); `src/api/src/zava_forward/api/web/role-screens.js` (lines 1106-1114, 1256-1274); `src/api/tests/test_exception_register_screen.py` (lines 84-86, 229-232, 390-396, 418-431); `src/api/tests/test_data_operator_screen.py` (line 130)
* Concern: In `role-screens.js:1260-1264`, `data-operator.overview(signal, rows, c)` renders `h("div", {}, register, summary)` where `register` appears before `summary`, and `summary` (`!c && rows.length ? this.summarise(rows, signal) : null`) renders both when `exceptions !== "1"` and when `exceptions === "1"` (`HostIntegration` `"loaded"` and `"denied"` scenarios in `test_exception_register_screen.py:390-396`). Putting `screenJumpNav("Data steward overview sections", [..., ["operator-register-entry", "Exception register"]])` inside `data-operator.summary(entries)` causes three defects:
  1. When `exceptions === "1"` and `rows.length > 0`, `register` is `exceptionRegisterPanel(data)` (`id="operator-register"`) or `exceptionUnavailable(error)` (`role-screens.js:1106-1114`, which currently has no `id` at all), so `#operator-register-entry` does not exist in the DOM and the jump link is broken (violating `AC-1`).
  2. When `screen.summarise(rows, signal)` is called standalone (`test_data_operator_screen.py:130`), `#operator-register-entry` is absent from the returned subtree.
  3. When `exceptions !== "1"` and `rows.length > 0`, `register` (`#operator-register-entry`) renders above `summary`, so the overview jump `<nav>` is stranded below the first section and lists `Exception register` last despite it being first in DOM reading/tab order (WCAG 2.2 SC 1.3.2 / SC 2.4.3). Meanwhile, when `rows` is empty (`scenario("entry")` in `test_exception_register_screen.py:85, 230-232`), `test_no_controls_and_entry_is_a_plain_link` asserts `len(links) == 1` on `overview(signal, [], null)`.
* Impact: Live `#/screens?screen=data-operator&exceptions=1` pages with queue rows contain a dead `a[data-jump="operator-register-entry"]` anchor that fails `AC-1`, and `#/screens?screen=data-operator` places its overview jump bar below the first section in contradicted tab/reading order.
* Smallest useful change: In `P01-T02`, convert `exceptionUnavailable(error)` (`role-screens.js:1107`) to `operatorPanel("operator-register", "Exception register", ...)` alongside `exceptionRegisterPanel(data)`; keep `data-operator.summary(entries)` returning `h("div", {}, operatorPanel("operator-overview-conflicts", ...), operatorPanel("operator-overview-returns", ...))` without a jump nav; and in `data-operator.overview(signal, rows, c)`, when `summary` is truthy (`!c && rows.length > 0`), prepend `screenJumpNav("Data steward overview sections", [[isExceptions ? "operator-register" : "operator-register-entry", "Exception register"], ["operator-overview-conflicts", "Attribute conflicts across this page of homes"], ["operator-overview-returns", "Returned or reopened steps across this page of homes"]])` before `register` and `summary` (`return h("div", {}, jumps, register, summary)`). When `rows` is empty (`summary === null`), omit `jumps` so single-section `scenario("entry")` keeps `len(links) == 1`. Update `P02-T01` test #1 to verify `overview(signal, rows, null)` across `exceptions !== "1"`, `exceptions === "1"` (loaded), and `exceptions === "1"` (403/500 unavailable).
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T02` and `P02-T01` in `.copilot-tracking/details/2026-11-15/229-data-steward-wcag-phase-details.md` placing `Data steward overview sections` at the top of `overview(signal, rows, c)` in DOM order and giving `exceptionUnavailable` `id="operator-register"`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: `operatorSide`, `exceptionRegisterState`, and `Eligibility` cell templates echo raw untrusted tokens, contradicting `FR-3`/`AC-3` and failing `P02-T01` test #5

* Related IDs: `FR-3`, `AC-3`, `P01`, `P01-T01`, `P01-T02`, `P02-T01`
* Evidence: `.copilot-tracking/plans/2026-11-15/229-data-steward-wcag-plan.md` (`FR-3` line 48, `AC-3` line 55); `.copilot-tracking/details/2026-11-15/229-data-steward-wcag-phase-details.md` (`P01-T01` lines 91 and 97, `P01-T02` line 133, `P02-T01` line 217); `src/api/src/zava_forward/api/web/role-screens.js` (lines 1081, 1175, 1229, 1236)
* Concern: `FR-3`, `AC-3`, and `P02-T01` test #5 require that colour-only strings (`"green"`, `"red"`), numeric/null values, false-assurance strings (`"Pass"`, `"Healthy"`, `"Clear"`), and `Object.prototype` keys (`"constructor"`, `"toString"`, `"__proto__"`) fail closed to `State: Unknown` or `Source state: Unknown` and never render raw `"green"`, `"Pass"`, `"Healthy"`, `"Clear"`, or `"constructor"`. Three planned expressions in `P01-T01`/`P01-T02` directly violate this invariant:
  1. `operatorSide(a)` (`P01-T01` line 91) renders `${screenValue(a.validation_state)} (${operatorSourceState(a.validation_state)})`, which outputs raw `"green (Source state: Unknown)"` or `"constructor (Source state: Unknown)"` whenever `a.validation_state` is invalid.
  2. `exceptionRegisterState(state)` (`P01-T01` line 97) maps unrecognised values to `` `State: Unknown (${exceptionText(state)})` ``, which outputs `"State: Unknown (green)"`, `"State: Unknown (Pass)"`, or `"State: Unknown (constructor)"`.
  3. `exceptionRegisterPanel` `"Eligibility"` cells (`P01-T02` line 133) use `State: ${exceptionText(item.eligibility)}`, where `exceptionText` (`role-screens.js:1081`) passes arbitrary strings and numbers straight through (`"State: green"`, `"State: Pass"`, `"State: 5"`, `"State: constructor"`).
* Impact: Implementing `P01-T01` and `P01-T02` as written will immediately fail `P02-T01` test #5 (`test_home_and_register_states_fail_closed_on_missing_colour_or_prototype_keys`) and leak colour-only or false-clear strings into the UI.
* Smallest useful change: Update `P01-T01` and `P01-T02` so:
  1. `operatorSide(a)` ends with `; ${operatorSourceState(a.validation_state)}` without repeating raw `${screenValue(a.validation_state)}` (since `operatorSourceState` already includes the canonical label when valid and `"Source state: Unknown"` when invalid, preserving `"D; source S-A v1"` in `test_data_operator_screen.py:72` and `"D; source SYN-STOCK-A v1"` in `data_operator_browser_check.py:71`).
  2. `exceptionRegisterState(state)` returns `"State: Unknown"` for any value other than `"ok"` or `"roles_not_named"`.
  3. Add an `Object.hasOwn` allowlist helper `exceptionEligibilityState(value)` (`unknown` -> `"Unknown"`, `not assessed` / `not_assessed` -> `"Not assessed"`, `suppressed` -> `"Suppressed"`, else `"Unknown"`) and render `State: ${exceptionEligibilityState(item.eligibility)}` and `State: ${exceptionEligibilityState(item.eligibility)}. No winning source is selected.` (preserving `"Unknown. No winning source is selected."` in `test_exception_register_screen.py:165` and `"Unknown"` in `data_operator_browser_check.py:167`). Include `items[].eligibility` in `P02-T01` test #5.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01`, `P01-T02`, and `P02-T01` in `.copilot-tracking/details/2026-11-15/229-data-steward-wcag-phase-details.md` removing raw value interpolation from `operatorSide`, `exceptionRegisterState`, and `Eligibility` cells.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: `P02-T02` documentation edit does not guard the `#data-screens-delivery-status-2026-11-04-229` traceability anchor or `docs/reference/log.md`

* Related IDs: `AC-4`, `P02`, `P02-T02`
* Evidence: `.copilot-tracking/plans/2026-11-15/229-data-steward-wcag-plan.md` (Affected Areas lines 31-36, `P02` line 82); `.copilot-tracking/details/2026-11-15/229-data-steward-wcag-phase-details.md` (`P02-T02` lines 242-270); `docs/reference/research/ux/customer-journeys/data.md` (line 103); `docs/reference/research/ux/screen-design-traceability.md` (line 55); `src/api/tests/test_screen_design_traceability.py` (lines 48-55)
* Concern: `docs/reference/research/ux/screen-design-traceability.md:55` links to `./customer-journeys/data.md#data-screens-delivery-status-2026-11-04-229`, and `test_screen_design_traceability.py:48-55` asserts that every linked `#anchor` resolves to an exact heading slug in the target file. `P02-T02` instructs updating `Data screens delivery status` in `customer-journeys/data.md` for `2026-11-15` without instructing the implementer to keep the H2 heading `## Data screens delivery status (2026-11-04, #229)` unchanged (or update `screen-design-traceability.md` in lockstep), omits `test_screen_design_traceability.py` from the `P02-T02` test command, and omits appending a knowledge-base entry to `docs/reference/log.md` if `docs/reference/research/ux/customer-journeys/data.md` is materially updated.
* Impact: Changing `(2026-11-04, #229)` to `(2026-11-15, #229)` in the H2 heading of `customer-journeys/data.md` breaks `test_screen_design_traceability.py` in CI, and omitting `docs/reference/log.md` leaves a material `docs/reference/` update unlogged.
* Smallest useful change: Update `plan.md` Affected Areas and `P02-T02` in `phase-details.md` to keep the H2 heading `## Data screens delivery status (2026-11-04, #229)` verbatim (adding the `2026-11-15` update inside the section body so `#data-screens-delivery-status-2026-11-04-229` continues to resolve), append an entry to `docs/reference/log.md` recording the `customer-journeys/data.md` update, and include `tests/test_screen_design_traceability.py` in the `P02-T02` regression unittest run.
* Action owner: planning_parent
* Exact resolving evidence: Updated `plan.md` and `P02-T02` in `phase-details.md` preserving `#data-screens-delivery-status-2026-11-04-229`, listing `docs/reference/log.md`, and running `test_screen_design_traceability.py`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: Stale `#226` `assetPanel` citation, implicit `operatorPanel` landmark-collision constraint, and omitted local Playwright checks in `P02-T02`

* Related IDs: `NFR-2`, `AC-1`, `AC-4`, `P01-T01`, `P02-T02`
* Evidence: `.copilot-tracking/plans/2026-11-15/229-data-steward-wcag-plan.md` (Sources line 25, Risk Register lines 99-104); `.copilot-tracking/details/2026-11-15/229-data-steward-wcag-phase-details.md` (`P01-T01` line 89, `P02-T02` lines 250-264); `src/api/src/zava_forward/api/web/role-screens.js` (lines 20-26, 316-345, 1281-1315); `src/api/checks/data_operator_browser_check.py` (lines 73, 107); `src/api/checks/specialist_keyboard_browser_check.py` (lines 201-244)
* Concern: `plan.md:25` cites `#226 assetPanel (318-323)` (from `research.md` `C3`), whereas `role-screens.js:20-26, 316-345` actually uses `screenPanel(title, { anchor }, ...)` which attaches `aria-labelledby: "${id}-heading"` to `<section>`. On `data-operator`, several section `<h2>` titles (`"Open exceptions and prerequisites"`, `"Recorded stock query events"`, `"Attribute conflicts across this page of homes"`) are identical to their inner `screenTable` captions (`div.table-scroll[role="region"][aria-label=...]`). If an implementer copies `aria-labelledby` from `screenPanel` onto `operatorPanel`, `<section>` becomes a duplicate-named `region` landmark that breaks Playwright strict mode at `data_operator_browser_check.py:73` (`get_by_role("region", name="Open exceptions and prerequisites", exact=True)`) and axe `landmark-unique` at `data_operator_browser_check.py:107`. In addition, `P02-T02` omits executing (or disclosing missing runtime prerequisites for) the touched local browser checks `checks/data_operator_browser_check.py` and `checks/specialist_keyboard_browser_check.py` per the focused validation tier.
* Impact: An implementer aligning `operatorPanel` with `screenPanel` could accidentally introduce duplicate `region` landmarks that pass Node VDOM unit tests but fail Playwright/axe browser checks.
* Smallest useful change: Replace the stale `assetPanel (318-323)` reference in `plan.md` with `screenPanel (20-26)` / `screenJumpTarget (28)`, add an explicit note in `P01-T01` that `operatorPanel` must omit `aria-labelledby`/`aria-label` on `<section>` to avoid colliding with `screenTable`'s `div.table-scroll[role="region"]` labels, and add `checks/data_operator_browser_check.py` and `checks/specialist_keyboard_browser_check.py` to `P02-T02` focused validation (recording execution or disclosing browser-prerequisite unavailability).
* Action owner: planning_parent
* Exact resolving evidence: Updated `plan.md` Sources/Risk Register, `P01-T01` `operatorPanel` constraint note, and `P02-T02` browser-check validation step in `.copilot-tracking/details/2026-11-15/229-data-steward-wcag-phase-details.md`.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Reusing shared `screenJumpNav` (`<a class="btn alt" href="#..." data-jump="...">`) and the existing delegated `a[data-jump]` click handler (`role-screens.js:268-275`) satisfies native keyboard link activation, `40px` (`2.5rem`) minimum target height in `style.css`, and zero-form-control invariants in `test_data_operator_screen.py`, `test_exception_register_screen.py`, and `data_operator_browser_check.py`.
* Leaving `exceptionSummaryRows`, `exceptionSummaryHeader`, `exceptionSummaryKinds`, `exceptionSummaryRoles`, and `exceptionSummaryCell` untouched preserves the frozen 4-column CSV export contract and formula-injection neutralisation tested in `test_exception_register_screen.py`.
* All planned visible strings and helper identifiers comply with the plain-language lexical guard in `src/api/tests/test_content_standard.py` (`\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b`), and preserving `"roles_not_named"`, `"ok"`, and `"Unknown. No winning source is selected."` substrings avoids breaking `test_exception_register_screen.py` and `test_data_operator_ai_state.py`.
* Residual risk: Node VDOM tests validate markup, attributes, fail-closed state maps, and delegated click focus-before-scroll call ordering, whereas full axe-core WCAG 2.2 AA and computed focus-indicator checks rely on Chromium Playwright (`data_operator_browser_check.py` and `specialist_keyboard_browser_check.py`).

## Questions or Blocking Evidence Gaps

* None. Every finding is fully resolved by existing repository code and test contracts; no user decision is required.

## Limitations

* This critique inspected repository source files, core domain contracts, documentation traceability links, and test suites directly in read-only mode; it did not execute unit tests or launch a Chromium browser.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: `planning_parent`
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-15/229-data-steward-wcag-plan.md` and `.copilot-tracking/details/2026-11-15/229-data-steward-wcag-phase-details.md` to incorporate `PC-001` through `PC-005`, then finalize the plan without another critique pass.
* User response required: No
