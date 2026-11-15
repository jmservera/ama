<!-- markdownlint-disable-file -->
# Review: Issue #231 Retrofit Technical and Quality Screens WCAG 2.2 Baseline

## Scope and Evidence

* Task ID: 2026-11-15-retrofit-technical-quality-wcag-231
* Review date: 2026-11-15
* Review scope: full task (`P01`, `P02`, `P03`)
* Assessed boundary: WCAG 2.2 baseline engineering delivery (`#151`) for `technical-queue` and `quality-queue` in `src/api/src/zava_forward/api/web/role-screens.js` and `src/api/src/zava_forward/api/web/style.css`, focused WCAG 2.2 test coverage in `src/api/tests/test_technical_quality_screens_wcag.py`, `content-visibility: auto` and table-header browser-check alignment in `src/api/checks/role_screens_browser_check.py`, Focused-tier validation, and counted baseline guard stability.
* Plan: .copilot-tracking/plans/2026-11-15/retrofit-technical-quality-wcag-231-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/retrofit-technical-quality-wcag-231-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/retrofit-technical-quality-wcag-231-research.md; git diff across `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/src/zava_forward/api/web/style.css`, `src/api/checks/role_screens_browser_check.py`, and `src/api/tests/test_technical_quality_screens_wcag.py`; Focused-tier validation and pinned axe 4.10.3 browser outputs.

## Opening Review State

* Interpreted review goal: Verify once and read-only whether the completed implementation across `P01`–`P03` satisfies all approved Issue #231 WCAG 2.2 requirements, acceptance criteria, critique dispositions (`PC-001`–`PC-003`), counted baseline guards, and browser-check contracts, and route any residual or follow-up items cleanly.
* Review scope: full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`)
* Evidence readiness: Ready; plan, phase details, single-pass critique, changes record, research record, source diff, unit/guard/lint/type outputs, Chromium + pinned axe 4.10.3 results, and refreshed Web Interface Guidelines audit are all present and reconciled.
* Acceptance basis: `FR-1`–`FR-4`, `NFR-1`–`NFR-2`, `AC-1`–`AC-5`, critique dispositions `PC-001`–`PC-003`, and caller Issue #231 guard constraints.
* First comparison boundary: Reconcile plan markers, phase details, and `Implementation-Time Plan and Detail Updates` in `.copilot-tracking/changes/2026-11-15/retrofit-technical-quality-wcag-231-changes.md` against the actual workspace diff before assessing findings and outcome.
* Active read-only boundaries: This stage may write only `.copilot-tracking/reviews/logs/2026-11-15/retrofit-technical-quality-wcag-231-review.md` (and parent RPI state pointers on return); zero production, test, plan, details, critique, or changes edits are permitted.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass read-only review on 2026-11-15 across all reconciled task artifacts, workspace git diff, Focused-tier unit/guard/lint/type results, Chromium + pinned axe 4.10.3 browser checks, refreshed Web Interface Guidelines audit, and an independent read-only review lens (`review-lens-231`).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01`, `P01-T02` | `Keyboard Section Navigation, Focus Styling, and Table Semantics (P01, P01-T01, P01-T02)` | Reconciled | `pasJumpNav`, `technical-boundary` and `quality-*` anchors, `screenRecordTable` across all five tables, `.screen-record h2[tabindex="-1"]:focus-visible`, and `.screen-evidence th, .screen-evidence td` tabular figures match the diff and passing tests. |
| `P02`, `P02-T01` | `Explicit Non-Colour Textual State Cues and Fluent 2 Readiness Banners (P02, P02-T01)` | Reconciled | Both `Evidence boundary` panels state colour is never the only signal, ready banners use `.status-line.ok`, and all planned `Object.hasOwn`-safe textual prefixes (`Source facts`, `Design state`, `Missing references`, `Returns and routing`, `Measure state`, `qualityCheckState`, ownerless `Defect owner`, and `Reinspection state`) match `FR-2` and `FR-3`. |
| `P03`, `P03-T01` | `Focused WCAG 2.2 Test Suite, Browser Harness Alignment, and Web Guidelines Review (P03, P03-T01)` | Partial | Focused tests, `role_screens_browser_check.py` `positive_text` + table-header/design-system/320px alignment, 16 unit/guard suites, `ruff`, `mypy`, Chromium + pinned axe 4.10.3 checks, and refreshed `web-design-guidelines` all ran and passed, while one test assertion in `test_technical_quality_screens_wcag.py` (`json.dumps(tree)` ASCII escaping before `\u2014` check) and two residual `:focus` prose occurrences in `plan.md`/`phase-details.md` were identified (`RV-001`, `RV-003`). |
| `Follow-Up Items` | `Follow-Up Items` | Reconciled | Parent-branch `resident-service-issues` / `programme-queue` browser-check items, human assistive-technology/usability validation (`#151`, `#155`), and future PAS 2035 lodgement screen remain outside active `P01`–`P03` scope in both `plan.md` and `changes.md`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/api/src/zava_forward/api/web/role-screens.js` | Added `pasJumpNav`, `technical-boundary` and `qualityRecordAnchor` section landmarks, and `screenRecordTable` `<th scope="row">` headers across all five tables on `technical-queue` and `quality-queue`. | Workspace diff and `test_jump_navigation_anchors_headings_and_delegated_click_focus` + `test_tables_row_headers_plain_ascii_and_no_controls_or_simulator`. | Passed in `unittest` and `role_screens_browser_check` (`231`, `231q`, `231p`, `231qp`). | Reconciled and conformant. |
| `P01-T02` | `src/api/src/zava_forward/api/web/style.css` | Added `.screen-record h2[tabindex="-1"]:focus-visible` Fluent 2 dual-ring focus indicator and extended `.screen-evidence th, .screen-evidence td` with `font-variant-numeric: tabular-nums`. | Workspace diff, Chromium `:focus-visible` verification, and `test_focus_ring_and_screen_css_invariants`. | Passed `test_design_system.py`, `test_role_screens_conformance.py`, `test_accessibility_baseline.py`, and refreshed `web-design-guidelines` (`✓ pass`). | Reconciled and conformant. |
| `P02-T01` | `src/api/src/zava_forward/api/web/role-screens.js` | Added non-colour state copy in `Evidence boundary`, `.status-line.ok` ready banners, and `Object.hasOwn`-safe textual prefixes across source facts, `technicalDesignState`, `Returns and routing`, `Missing references`, `qualityMeasureState`, `qualityCheckState`, ownerless `Defect owner`, and `qualityReinspectionState`. | Workspace diff (verified zero `\u2014` characters and zero banned words) and `test_technical_queue_textual_state_cues_and_ready_banner` + `test_quality_queue_textual_states_independence_and_reinspection`. | Passed `test_technical_quality_screens.py`, `test_assessor_screen_wcag.py`, `test_content_standard.py`, `test_connected_home_check.py`, and pinned axe 4.10.3 browser checks. | Reconciled and conformant with planned `FR-2`/`FR-3` (`RV-002` notes an optional follow-up enhancement on `defect.fixed_by`). |
| `P03-T01` | `src/api/tests/test_technical_quality_screens_wcag.py`, `src/api/checks/role_screens_browser_check.py` | Added 5-method WCAG 2.2 Node `vm` + CSS test suite and updated `role_screens_browser_check.py` to use `positive_text(page)` across `content-visibility: auto` panels plus `check_design_system_use`, `check_table_headers`, and 320px `reach_table_regions` on `STORY_231`/`STORY_POSITIVE`. | Test execution across 16 modules, `ruff`, `mypy`, and Chromium + pinned axe 4.10.3 runs. | All checks passed; however, `self.assertNotIn("\u2014", json.dumps(tree))` uses default `ensure_ascii=True`, escaping Unicode characters before the substring check (`RV-001`). | Test-assertion defect recorded as `RV-001`. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `Scope and Non-Goals`, `P03-T01` (`role_screens_browser_check.py`) | Switched `check_readonly_accessibility` from unscrolled `evidence.inner_text()` to `positive_text(page)` and enabled `check_design_system_use`, `check_table_headers`, and 320px `reach_table_regions` on `STORY_231`/`STORY_POSITIVE`. | Increasing #231 panel height pushed top readiness text past Chromium's `.screen-record { content-visibility: auto }` skip margin after `run_browser` scrolled to the bottom; preserves caller browser-compatibility requirement without user decision. | Reconciled across `plan.md`, `phase-details.md`, and `changes.md`. | Immediately relevant current-state update; no new planning/critique required. | Reconciled. |
| `NFR-1`, `AC-2`, `P01-T02`, `P03-T01` (`:focus-visible`) | Refined `.screen-record h2[tabindex="-1"]:focus` to `:focus-visible` to satisfy refreshed Web Interface Guidelines (`Use :focus-visible over :focus`) while retaining Chromium keyboard jump focus rings. | Refreshed `web-design-guidelines` rules and headless Chromium verification (`document.activeElement.matches(':focus-visible') == True` on keyboard `Enter`); local judgment within approved intent. | Updated in `Scope`, `NFR-1`, `AC-2`, `P01-T02`, `P03-T01`, and `changes.md`; two secondary prose occurrences in `Test Ownership and Validation Lock` (`plan.md`) and `Initial Phase Overview` (`phase-details.md`) still read `:focus`. | Local judgment refinement; no new critique required. | Minor tracking-prose residual recorded as `RV-003`. |
| `Follow-Up Items` (parent-branch browser checks) | Recorded pre-existing parent-branch failures on `resident-service-issues` (`Routes to ask` region in `specialist_keyboard_browser_check.py`) and `programme-queue` (`atlas_tensions_browser_check.py`) from parent commit `f26290cd1` (#1758). | Direct Chromium execution proving all five #231 roles and 15 negative controls pass when `resident-service-issues` is isolated. | Recorded in `plan.md` `## Follow-Up Items` and `changes.md` `## Follow-Up Items`. | Follow-up-only discovery outside #231 scope. | Reconciled. |

## Critique and Material Revision Assessment

* Latest critique dispositions: `PC-001` (`qualityReinspectionState` independence scoping), `PC-002` (plain ASCII punctuation in production code/comments + rendered-tree assertion), and `PC-003` (`python3 -m checks.*` invocation and `231`/`231q`/`231p`/`231qp` selectors) are all explicitly disposed in `plan.md` `## Critique Disposition`. Production code satisfies all three; `PC-002`'s regression test assertion has the `json.dumps` ASCII-escaping defect recorded in `RV-001`.
* Material revisions: None. Both implementation-time updates preserved approved user intent and architecture without requiring planning reconsideration or a second critique.
* Dependent-work pause assessment: No material revision occurred; execution respected `P01` -> `P02` -> `P03` dependency order without premature resumption.
* Justification assessment: Supported by Chromium `content-visibility: auto` and `:focus-visible` evidence recorded in `changes.md`.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Parent-branch `resident-service-issues` (`Routes to ask` region in `specialist_keyboard_browser_check.py`) and `programme-queue` write-control check (`atlas_tensions_browser_check.py`) | Introduced by parent commit `f26290cd1` (#1758) on unrelated screens outside #231 (`technical-queue` and `quality-queue`). | Parent/aftercare workstream owner to reconcile `EXPECTED_REGIONS["resident-service-issues"]` and `atlas_tensions_browser_check.py`. | Open distinct follow-up; kept outside active #231 completion claims. |
| Human assistive-technology and role-representative walkthrough for #231 (`#151`, `#155`) | Automated VM, static CSS, and Chromium/axe checks prove engineering mechanics only and cannot establish assistive-technology usability acceptance. | Human reviewer / role representative before Issue #231 transitions from `Refs #231` to closed. | Open distinct human gate; preserved via `Refs #231`. |
| Dedicated PAS 2035 lodgement workflow screen | No lodgement screen exists in `role-screens.js` under #231's registered screen inventory. | Future PAS 2035 lodgement backlog item to adopt `pasJumpNav`, `screenRecordTable`, and `Object.hasOwn` `stateCue`. | Open distinct follow-up; outside #231 scope. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: `test_technical_quality_screens_wcag.py` checks `\u2014` against ASCII-escaped `json.dumps(tree)` output

* Related scope: `P03-T01` (critique disposition `PC-002`)
* Evidence: `src/api/tests/test_technical_quality_screens_wcag.py` (`test_tables_row_headers_plain_ascii_and_no_controls_or_simulator`) computes `dumped = json.dumps(tree)` with Python's default `ensure_ascii=True` before asserting `self.assertNotIn("\u2014", dumped)`. Because `json.dumps(..., ensure_ascii=True)` serializes `\u2014` as the six ASCII characters `\u2014`, a future Unicode em dash introduced into rendered text would not fail that assertion (verified separately via `grep` that `role-screens.js` currently contains zero `\u2014` characters).
* Impact: Weakens automated regression detection for `PC-002` (plain ASCII em-dash avoidance) without affecting current production `role-screens.js` output.
* Destination: `rpi-implement`
* Smallest useful next action: Pass `ensure_ascii=False` to `json.dumps(tree, ensure_ascii=False)` (or assert against `node_text(tree)`) in `test_tables_row_headers_plain_ascii_and_no_controls_or_simulator` and confirm with a one-line negative control that `\u2014` is caught.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: `qualityAcceptanceGap(r)` checks inspector independence against `submitted_by` only, not `defect.fixed_by`

* Related scope: `P02-T01` (domain follow-up adjacent to `qualityAcceptanceGap`)
* Evidence: `src/api/src/zava_forward/api/web/role-screens.js` (`qualityAcceptanceGap`, `qualityNext`, `qualityMeasureState`, `qualityCheckState`, `qualityReinspectionState`). The pre-existing `qualityAcceptanceGap(r)` helper compares `r.accepted_by` with `r.submitted_by` (matching planned `FR-3`), whereas `qualityNext(r)` states reinspection must be by `"a Quality Inspector not involved in the work or fix"`. If a third party named in `r.defect.fixed_by` differs from `r.submitted_by` and equals `r.accepted_by`, `qualityAcceptanceGap(r)` returns `""`.
* Impact: Edge-case PAS 2035 domain gap when remediating contractor/fixer differs from original submitter and also records acceptance; current planned `FR-3` acceptance criteria and existing `#231` domain tests (`test_technical_quality_screens.py`) only model `submitted_by` vs `accepted_by`.
* Destination: distinct follow-up item
* Smallest useful next action: Evaluate extending `qualityAcceptanceGap(r)` (and backend quality acceptance validation, if mirrored) to reject `accepted_by` matching `r.defect?.fixed_by` as well as blank `submitted_by` in a dedicated PAS 2035 quality-independence follow-up.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Two secondary prose mentions of `:focus` remain in `plan.md` and `phase-details.md` after `:focus-visible` reconciliation

* Related scope: `P01-T02` tracking artifacts
* Evidence: `.copilot-tracking/plans/2026-11-15/retrofit-technical-quality-wcag-231-plan.md` (`## Test Ownership and Validation Lock`) and `.copilot-tracking/details/2026-11-15/retrofit-technical-quality-wcag-231-phase-details.md` (`## Initial Phase Overview`) still write `.screen-record h2[tabindex="-1"]:focus`, whereas `Scope and Non-Goals`, `NFR-1`, `AC-2`, `P01-T02`, `P03-T01`, `changes.md`, `style.css`, and `test_technical_quality_screens_wcag.py` all consistently use `:focus-visible`.
* Impact: Documentation-only minor wording inconsistency inside two tracking-artifact summary lines; zero impact on production CSS, tests, or runtime behavior.
* Destination: distinct follow-up item
* Smallest useful next action: Align those two summary mentions if the tracking plan/details are reopened alongside `RV-001`.

## Defects

* `RV-001` [Medium] -> `rpi-implement`: Use `json.dumps(tree, ensure_ascii=False)` (or `node_text(tree)`) in `src/api/tests/test_technical_quality_screens_wcag.py` so `self.assertNotIn("\u2014", ...)` actively detects Unicode em dashes in rendered screen trees.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Update `json.dumps(tree)` to `json.dumps(tree, ensure_ascii=False)` in `src/api/tests/test_technical_quality_screens_wcag.py` and re-run `unittest` + `ruff` + `mypy`. | Test-assertion implementation defect within accepted `PC-002` direction. |
| `RV-002` | `follow-up` | Scoped PAS 2035 quality-independence follow-up comparing `accepted_by` with `defect.fixed_by` across UI and domain checks. | Domain enhancement beyond planned `FR-3` `qualityAcceptanceGap(r)` reuse. |
| `RV-003` | `follow-up` | Optional tracking-prose cleanup in `plan.md` (`Test Ownership and Validation Lock`) and `phase-details.md` (`Initial Phase Overview`) if reopened. | Non-blocking minor tracking-prose residual. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-002`: Extend `qualityAcceptanceGap(r)` independence comparison to `r.defect?.fixed_by` (distinct follow-up item outside planned `FR-3`).
* `RV-003`: Minor `:focus` -> `:focus-visible` wording cleanup in two summary lines of `plan.md` and `phase-details.md` if reopened.
* Retained plan follow-up items: parent-branch `resident-service-issues` / `programme-queue` browser-check alignment (`#1758`), human assistive-technology and role-representative validation (`#151`, `#155`), and future PAS 2035 lodgement workflow screen.

## Blockers and Remaining Work

* Blockers: none for the engineering RPI loop (human assistive-technology/usability sign-off under `#151` and `#155` remains an external closure gate on Issue #231, honoured via `Refs #231`).
* Remaining active work: none in the completed task pass; `RV-001` is routed to a subsequent user-selected `rpi-implement` follow-up pass per single-pass Review rules.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -B -m unittest` (16 modules: `test_accessibility_baseline`, `test_epic149_form_error_summary_associations`, `test_list_export_inventory`, `test_technical_quality_screens_wcag`, `test_assessor_screen_wcag`, `test_technical_quality_screens`, `test_procurement_qa_screen_wcag`, `test_resident_screen_wcag`, `test_role_screens_conformance`, `test_role_screens`, `test_connected_home_check`, `test_specialist_keyboard_check`, `test_content_standard`, `test_design_system`, `test_learning_test_bundle_scenarios`, `test_safety_screen_wcag_keyboard`) | `src/api` unit, WCAG, and counted baseline guards | Passed | All 16 suites exited `0`; counted baseline guards unchanged (`aria-invalid` = 8, `h("table", {}, ...)` = 13, `/api/...` list/export inventory unchanged). |
| `python3 -m ruff check src/ tests/ checks/` and `python3 -m ruff format --check src/ tests/ checks/` | `src/api` lint and formatting | Passed | `All checks passed!`, `203 files already formatted`. |
| `python3 -m mypy src/ tests/ checks/` | `src/api` static type check | Passed | `Success: no issues found in 288 source files`. |
| `ZF_AXE_JS=/tmp/axepk/package/axe.min.js python3 -B -m checks.role_screens_browser_check` across default (`parent`), `231`, `231q`, `231p`, `231qp` | Headless Chromium 156.0.8078.4 + pinned axe 4.10.3 | Passed | Zero axe violations (`[]`) across WCAG 2.0/2.1/2.2 A+AA tags, zero undocumented design-system classes, all rendered tables verified for `<caption>`, `<th scope="col">`, and `<th scope="row">`, and 320px/390px/1280px reflow + 320px keyboard Tab reach passed. |
| `python3 -B -m checks.connected_home_browser_check` and `python3 -B -m checks.simulator_control_browser_check` | Headless Chromium 156.0.8078.4 | Passed | Both exited `0` cleanly. |
| `specialist_keyboard_browser_check` targeted walk across all five roles serving `technical-queue` and `quality-queue` + 15 negative sabotage controls | Headless Chromium 156.0.8078.4 | Passed (targeted) / Failed (full suite on unrelated parent screen) | All #231 roles (`Retrofit Programme Manager`, `Retrofit Coordinator`, `Building Safety Liaison`, `Quality Inspector`, `Programme Support Officer`) and 15 negative controls passed; full-suite run stops on unrelated parent-branch `resident-service-issues` (`Routes to ask` region from `f26290cd1`, `#1758`), routed as follow-up. |
| Refreshed `web-design-guidelines` (`vercel-labs/web-interface-guidelines` `command.md`) | `role-screens.js`, `style.css` | Passed | Zero open Web Interface Guidelines findings (`✓ pass` on both files). |

## Outcome

* Outcome: Defects found
* Outcome rationale: Production changes in `role-screens.js`, `style.css`, and `role_screens_browser_check.py` satisfy `FR-1`–`FR-4`, `NFR-1`–`NFR-2`, `AC-1`–`AC-4`, all counted baseline guards, and pinned axe 4.10.3 browser checks with zero production defects and zero `\u2014` characters; however, `RV-001` [Medium] identifies that `test_technical_quality_screens_wcag.py` runs `self.assertNotIn("\u2014", json.dumps(tree))` with default `ensure_ascii=True`, which escapes Unicode characters before the check and therefore requires a small `ensure_ascii=False` follow-up in `rpi-implement` to make `PC-002`'s regression test effective. Per RPI Stop rules, a conformant outcome is not claimed while `RV-001` remains open.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` | Resolve `RV-001` (`json.dumps(tree, ensure_ascii=False)` in `src/api/tests/test_technical_quality_screens_wcag.py`). |
| Decision gap or invalid assumption | `none` | None. |
| Material evidence gap | `none` | None. |
| Non-blocking residual work | `distinct follow-up` | `RV-002` (`defect.fixed_by` independence check), `RV-003` (two tracking-prose `:focus` mentions), parent-branch `resident-service-issues`/`programme-queue` browser-check alignment, human assistive-technology sign-off (`#151`, `#155`), and future PAS 2035 lodgement screen. |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: 16 `unittest` suites, `ruff check`, `ruff format --check`, `mypy`, `role_screens_browser_check` (`parent`, `231`, `231q`, `231p`, `231qp` + pinned axe 4.10.3), `connected_home_browser_check`, `simulator_control_browser_check`, targeted `specialist_keyboard_browser_check` (#231 roles + 15 negative controls), and refreshed `web-design-guidelines` all passed
* Blockers: none

