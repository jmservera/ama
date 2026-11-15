<!-- markdownlint-disable-file -->
# RPI Plan Critique: WCAG 2.2 Conformance Baseline for the Workbench (#151 / #119)

## Metadata

* Task ID: 2026-11-15-wcag-baseline-151
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver GitHub issue #151 ("WCAG 2.2 conformance baseline for the workbench") and paired issue #119 on branch feat/ux-151-wcag-baseline under the focused validation tier across three caller requirements: (1) synchronized, keyboard-reachable, screen-reader-accessible equivalents for every workbench map, chart, and data table with explicit headings, captions or aria-labels, and textual state meaning; (2) a complete 8-dimension WCAG 2.2 AA structured workbench audit recorded in docs/reference/research/ux/wcag-conformance-baseline.md with synchronized updates to docs/reference/README.md and docs/reference/log.md; and (3) deterministic automated verification tests in src/api/tests/ asserting both 8-dimension audit coverage and map/chart/table accessible equivalents while preserving all repository test guards.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md, .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md, .copilot-tracking/research/2026-11-15/wcag-baseline-151-research.md (C1-C24, W1-W2), docs/reference/research/ux/wcag-conformance-baseline.md, docs/reference/README.md, src/api/src/zava_forward/api/web/index.html, src/api/src/zava_forward/api/web/welcome.html, src/api/src/zava_forward/api/web/law.html, src/api/src/zava_forward/api/web/app.js, src/api/src/zava_forward/api/web/progress.js, src/api/src/zava_forward/api/web/ops.js, src/api/src/zava_forward/api/web/panels.js, src/api/src/zava_forward/api/web/role-screens.js, src/api/src/zava_forward/api/web/staff-intake.js, src/api/src/zava_forward/api/web/style.css, src/api/src/zava_forward/api/web/progress.css, src/api/src/zava_forward/api/web/vendor/leaflet.css, src/api/tests/test_accessibility_baseline.py, src/api/tests/test_epic149_landmarks_skip_link_focus_order.py, src/api/tests/test_epic149_form_error_summary_associations.py, src/api/tests/test_epic149_ux_evidence_results.py, src/api/tests/test_epic149_ux_journey_requirement_traceability.py, src/api/tests/test_content_standard.py, src/api/tests/test_finance_exposure_screen.py, src/api/tests/test_design_system.py, src/api/tests/test_role_screens.py, src/api/tests/test_programme_coordinator_wcag_230.py, and src/api/checks/employee_acceptance_check.py.
* Decisions, dependencies, and acceptance criteria considered: Focused validation tier (src/core and src/api unit/focused suites, ruff, mypy, node --check, python3 tools/rename-zava-tests.py); preservation of non-full-conformance disclaimers, SURFACES tuples, shrink-only gap guards (NO_FIELD_FOCUS, NO_SKIP_LINK, NO_NAV, ## Recorded gaps), plain-language vocabulary rules, financeQueueView slice parser boundary, and employee_acceptance_check.py .maplist li expectations; acceptance criteria AC-1 through AC-6 in .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md.
* Assessment boundary: Static code, DOM-builder, stylesheet, documentation, and automated guard verification across all supplied workbench HTML/JS/CSS and test files. Live assistive-technology and human screen-reader/zoom usability testing remain explicitly outside automated engineering verification, consistent with repository policy and test_accessibility_baseline.py.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1 / FR-1, FR-2, FR-3, FR-4 | Partial | Overview bars() and mapPanel() equivalents are well-designed, but progress.js targets/variables (PC-001), role-screens.js screenTable rowHeader default (PC-002), and P01-T02 property/wrapper instructions (PC-003) mismatch actual source code. |
| Caller Req 2 / FR-6 / P02-T01, P02-T02 | Partial | Covers all 8 required WCAG 2.2 AA dimensions, SURFACES, Recorded gaps, disclaimers, README.md, and log.md, but repeats inaccurate progress.js/table claims (PC-001, PC-002) and cites test_wcag_workbench_baseline_151.py before P03-T01 creates it (PC-004). |
| Caller Req 3 / AC-1..AC-6 / P03-T01, P03-T02 | Partial | Test suite scope and focused validation commands cover all required checks, but P03-T01 specifies nonexistent progress.js globals/selectors (PC-001), fails 15-table row-header assertions unless role-screens.js is updated (PC-002), and needs hidden attribute/property sync in Node vm (PC-005). |
| Research C1-C8, C11-C24, W1-W2 | Covered | Verified against index.html, welcome.html, law.html, app.js, panels.js, style.css, and src/api/tests/ guard suites. |
| Research C9, C10 | Partial | C9 misstates progress.js helper names, container classes, and empty fallbacks (PC-001); C10 misstates ops.js:475 as lacking .table-scroll and omits role-screens.js screenTable rowHeader = false (PC-002, PC-003). |
| P01 / P01-T01 | Partial | bars() and mapPanel() design preserves test_accessibility_baseline.py and employee_acceptance_check.py, but progress.js meter expression throws ReferenceError on undefined label, hardcodes columns[1] on multi-series charts, and targets nonexistent tableWrap/ul.bars (PC-001); mapPanel hidden initialization differs from app.js boolean convention (PC-005). |
| P01 / P01-T02 | Partial | Excludes role-screens.js screenTable where 19 call sites lack th[scope="row"] (PC-002), uses nonexistent r.resident_name in app.js:2927 and r.metric in ops.js:40, and re-wraps ops.js:475 in a duplicate nested .table-scroll (PC-003). |
| P01 / P01-T03 | Partial | Token contrast (--muted: #595550, --warn: #b3360a) and summary/checkbox/radio target sizes are sound, but .leaflet-bar a (specificity 0,1,1) is overridden on touch devices by vendor/leaflet.css .leaflet-touch .leaflet-bar a (specificity 0,2,1) (PC-005). |
| P02 / P02-T01, P02-T02 | Partial | P02 validation runs test_epic149_ux_journey_requirement_traceability.py after citing test_wcag_workbench_baseline_151.py in wcag-conformance-baseline.md, failing deterministically before P03-T01 creates that test file (PC-004). |
| P03 / P03-T01, P03-T02 | Partial | Focused validation commands match repository rules, subject to fixing progress.js IIFE harness calls (PC-001), 15-table row-header scope (PC-002), and phase ordering with P02 (PC-004). |

## Verdict

* Verdict: Revise
* Rationale: The architecture, guard-preservation strategy, token contrast adjustments, and 8-dimension WCAG 2.2 AA audit structure are well aligned with #151 and #119, but direct verification against shipped workbench code and test guards uncovered four High-severity and one Medium-severity factual/ordering defects that would cause runtime ReferenceErrors, empty resident link labels, duplicate nested scroll regions, 19 unfixed data tables failing the 15-builder row-header sweep, and a deterministic P02 gate failure. Every finding is a direct planner correction requiring no user escalation.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Inaccurate progress.js variable names, multi-series column indexing, DOM selectors, and IIFE test targets across P01-T01, P02-T01, and P03-T01

* Related IDs: FR-3, AC-1, AC-4, C9, P01, P01-T01, P02-T01, P03-T01
* Evidence: src/api/src/zava_forward/api/web/progress.js (lines 3-65, 88, 144-150, 195), src/api/tests/test_role_screens.py (lines 66-85), .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md (FR-3, P01-T01, P03-T01), .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md (lines 25, 36, 52, 65-75, 199, 208, 267)
* Concern: (1) P01-T01 specifies `"aria-label": `${label}, ${columns[1]}: ${count} (highest shown: ${max})`` on `<meter>` inside `progress.js`, but `progress.js` (`"use strict"`, lines 55-60) has no `label` variable (the row label is `row[0]`) and iterates multi-series charts (`columns = ["Day", "Opened", "Closed", "Reopened"]` at lines 144-145) via `row.slice(1).map((count, index) => ...)`, where the series column header is `columns[index + 1]`, not `columns[1]`. (2) FR-3, P01-T01, P02-T01, and P03-T01 repeatedly reference nonexistent `tableWrap()`, `div.table-wrap`, `ul.bars`, `/app?view=progress`, and missing empty-row fallbacks (`"No cases recorded."`). In actual `progress.js`, `ProgressViews` is a closed IIFE returning only `{ dashboard, closed }` on hash routes `#/progress` and `#/closed`; `table()` (line 44) and `chart()` (line 52) are private inner functions; `table()` already renders `div.table-scroll[role="region"][tabindex="0"][aria-label="${title} table"]`; `chart()` renders `div.progress-bars[aria-hidden="true"]`; and both `table()` (line 50) and `chart()` (line 61) already implement `"No recorded data for this view."` (which remains accurate for non-case charts such as `"AI briefing review outcomes"` measuring `"Reviews"`).
* Impact: Copying the P01-T01 `<meter>` snippet throws `ReferenceError: label is not defined` at runtime and mislabels `"Closed"` and `"Reopened"` series meters as `"Opened"`; replacing `"No recorded data for this view."` with `"No cases recorded."` introduces inaccurate copy on review-outcome charts; P03-T01 Node `vm` tests calling global `chart()`/`tableWrap()` or asserting `div.table-wrap` will fail; and P02-T01 would record false route and selector claims in docs/reference/research/ux/wcag-conformance-baseline.md.
* Smallest useful change: Update FR-3, P01-T01, P02-T01, and P03-T01 to use `ProgressViews` (`#/progress` and `#/closed` in `/app`), inner `table()` (`div.table-scroll[role="region"][tabindex="0"]`), inner `chart()` (`div.progress-bars[aria-hidden="true"]`), and `"aria-label": `${row[0]}, ${columns[index + 1]}: ${number(count)} (highest shown: ${number(max)})`` on `<meter>`, keep the existing `"No recorded data for this view."` empty fallback in `chart()` and `table()`, and drive `ProgressViews.dashboard()` / `ProgressViews.closed()` in the P03-T01 Node `vm` harness (matching src/api/tests/test_role_screens.py).
* Action owner: planning_parent
* Exact resolving evidence: Revised .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md and .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md matching `progress.js` lines 3-65, 88, and 144-150 with zero references to `tableWrap`, `div.table-wrap`, `/app?view=progress`, or undefined `label`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: role-screens.js screenTable defaults rowHeader = false across 19 specialist and staff-intake tables while P01-T02 excludes role-screens.js

* Related IDs: FR-4, AC-1, AC-4, C10, P01, P01-T02, P02-T01, P03-T01
* Evidence: src/api/src/zava_forward/api/web/role-screens.js (lines 50-58, 279, 283, 289, 363, 368, 380, 385, 1172, 1179, 1222, 1891, 1906, 1946, 2077, 2130), src/api/src/zava_forward/api/web/staff-intake.js (lines 80, 81, 153, 159), .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md (FR-4, P01-T02, P03-T01), .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md (lines 82-115, 208, 269)
* Concern: FR-4, P02-T01, and P03-T01 item 5 require and assert that all 15 `h("table"` builders across `web/*.js` (`ops.js`, `panels.js`, `app.js`, `aftercare.js`, `role-screens.js`, `progress.js`) emit `<caption>`, `<th scope="col">`, `<th scope="row">` on data rows, and `.table-scroll`. However, `screenTable(label, headings, rows, limit = 50, cell = ..., rowHeader = false)` in `role-screens.js:50` defaults `rowHeader` to `false`. Only 3 call sites (`lines 336, 472, 736`) pass `true`, leaving 15 call sites in `role-screens.js` and 4 call sites in `staff-intake.js` emitting `<td>` on column 0 (`Owner`, `Capability`, `Component`, `Home`, `Query`, `Input`, `Check`, `Item`, `Home and item`, `Exception`, `Invoice line`, `Field`, `Grant`, `Event`, `Kind`), while P01-T02 excludes `role-screens.js` from its target files.
* Impact: P03-T01's 15-table sweep asserting `<th scope="row">` across all `web/*.js` table builders will fail against `role-screens.js` / `staff-intake.js`, and P02-T01's WCAG 1.3.1 audit claim will be false for 19 shipped tables.
* Smallest useful change: Add `src/api/src/zava_forward/api/web/role-screens.js` (`line 50`) to P01-T02 and change `screenTable`'s default parameter from `rowHeader = false` to `rowHeader = true` (no existing test in `src/api/tests/` asserts `cells[0].tag == "td"` on `screenTable`), and include `test_role_screens.py` / `test_role_screens_conformance.py` in P01-T02 validation.
* Action owner: planning_parent
* Exact resolving evidence: P01-T02 in .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md and .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md explicitly includes `role-screens.js` (`screenTable` `rowHeader = true` default) alongside role-screen regression checks.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: P01-T02 specifies nonexistent row fields (r.resident_name, r.metric) and re-wraps ops.js packagesView in a duplicate nested .table-scroll region

* Related IDs: FR-4, C10, C11, C12, P01, P01-T02
* Evidence: src/api/src/zava_forward/api/web/app.js (lines 2897-2905, 2925-2928), src/api/src/zava_forward/api/web/ops.js (lines 34-44, 474-478), src/api/src/zava_forward/api/web/panels.js (lines 143-145, 232-235, 591-595), .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md (lines 82-125)
* Concern: Three concrete target instructions in P01-T02 contradict actual source lines: (1) `app.js:2927` (`fundingView`) stores the resident label on `r.resident` (`h("a", { href: ... }, r.resident)`), not `r.resident_name` as written in P01-T02 line 124; (2) `ops.js:40` (`sensorTable`) uses `r.reading_id` and already renders `h("th", { scope: "row" }, r.reading_id)`, not `r.metric` as written in P01-T02 line 121; and (3) `ops.js:474` (`packagesView`) already wraps its table in `h("div", { class: "table-scroll", role: "region", "aria-label": `Capacity for ${p.id}`, tabindex: 0 }, ...)` (which disambiguates multiple package regions on `#/packages`), while `app.js:2898` (`Contractors`) and `app.js:2903` (`Team workload`) also already have `.table-scroll`, leaving 5 tables needing new `.table-scroll` wrappers (`ops.js:38`, `panels.js:143`, `panels.js:232`, `panels.js:591`, `app.js:2925`), not 6 including `ops.js:475`. Also in `panels.js:594` (`financeQueueView`), column 0 is the home link `h("a", { href: `#/case/${encodeURIComponent(r.case_id)}` }, r.address)` inside `<td>` which upgrades to `<th scope="row">`.
* Impact: Implementing P01-T02 as written renders `undefined` inside `<a href="#/case/..."></a>` links in `fundingView` and `undefined` row headers in `sensorTable` (introducing WCAG 2.4.4/4.1.2 link-name and data regressions), and creates nested duplicate `role="region"` scroll containers on `#/packages` while discarding per-package `${p.id}` region disambiguation.
* Smallest useful change: Correct P01-T02's per-file table specification to match exact source fields and existing wrappers: `ops.js:38` (`sensorTable`: add `.table-scroll` and `<caption>` replacing `aria-label`, keep existing `h("th", { scope: "row" }, r.reading_id)`), `ops.js:477` (`packagesView`: keep existing `Capacity for ${p.id}` `.table-scroll`, upgrade `k.contractor` cell to `<th scope="row">`), `panels.js:143, 232, 591` (wrap all three in `.table-scroll` and upgrade column-0 `<td>` cells `label`, `${m.measure}: ...`, and `h("a", ..., r.address)` to `<th scope="row">`), `app.js:2899, 2904` (keep existing `.table-scroll`, upgrade `c.name` and `t.name` to `<th scope="row">`), and `app.js:2925-2927` (wrap `fundingView` table in `.table-scroll` and upgrade `h("a", ..., r.resident)` cell to `<th scope="row">`).
* Action owner: planning_parent
* Exact resolving evidence: Updated P01-T02 in .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md and .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md reflecting exact property names (`r.resident`, `r.reading_id`) and the exact 5 missing `.table-scroll` wrappers.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Phase-ordering inversion between P02 and P03 causes P02's traceability test gate to fail on missing test_wcag_workbench_baseline_151.py

* Related IDs: FR-6, AC-5, AC-6, C16, P02, P02-T01, P03, P03-T01
* Evidence: src/api/tests/test_epic149_ux_journey_requirement_traceability.py (lines 32, 134-139), .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md (Phase Checklist, P02, P03), .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md (lines 184, 221, 235, 241)
* Concern: P02 runs before P03 (`P02` depends on `P01`; `P03` depends on `P01, P02`). P02-T01 (`line 221`) edits `docs/reference/research/ux/wcag-conformance-baseline.md` to cite `test_wcag_workbench_baseline_151.py`, and P02's Validation Expectations (`line 235`) require `test_epic149_ux_journey_requirement_traceability.py` to pass at the close of P02. However, `ControlClaimsMapToTests.test_every_test_module_named_in_the_ux_docs_exists_and_runs` in `test_epic149_ux_journey_requirement_traceability.py` scans every `test_[a-z0-9_]+\.py` token across `docs/reference/research/ux/*.md` and asserts `(TESTS / name).is_file()`, that it compiles, defines `test*` methods, and contains no `@unittest.skip`. Because `src/api/tests/test_wcag_workbench_baseline_151.py` is not created until P03-T01, P02's exit gate fails deterministically with `AssertionError: False is not true : test_wcag_workbench_baseline_151.py is missing`.
* Impact: Sequential phase-gated execution in `rpi-implement` will halt on a guaranteed P02 validation failure before reaching P03.
* Smallest useful change: Either swap phase order so creating `src/api/tests/test_wcag_workbench_baseline_151.py` precedes citing it in `docs/reference/research/ux/wcag-conformance-baseline.md`, or keep P01 -> P02 -> P03 while running `test_epic149_ux_evidence_results.py` in P02 and deferring `test_epic149_ux_journey_requirement_traceability.py` (or adding the `test_wcag_workbench_baseline_151.py` citation) until P03-T01 creates the test module.
* Action owner: planning_parent
* Exact resolving evidence: Updated phase sequence or phase validation gates in .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md and .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md such that `test_epic149_ux_journey_requirement_traceability.py` is only required after every `test_*.py` named in `docs/reference/research/ux/*.md` exists on disk.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Leaflet touch-mode CSS specificity override on .leaflet-bar a and hidden boolean attribute mismatch in mapPanel

* Related IDs: FR-2, FR-5, AC-1, AC-3, C7, C13, P01-T01, P01-T03, P03-T01
* Evidence: src/api/src/zava_forward/api/web/vendor/leaflet.css (lines 286-296, 326-331), src/api/src/zava_forward/api/web/app.js (lines 21-29, 2505, 2519-2525), .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md (lines 69, 145, 174, 266)
* Concern: (1) In `vendor/leaflet.css`, `.leaflet-bar a` (`line 286`, specificity 0,1,1) sets `26px`, and `.leaflet-touch .leaflet-bar a` (`line 326`, specificity 0,2,1) sets `width: 30px; height: 30px; line-height: 30px`. P01-T03 specifies only `.leaflet-bar a{min-width:1.5rem;min-height:1.5rem;width:2rem;height:2rem;line-height:2rem}` (specificity 0,1,1), so on touch-capable laptops, tablets, and mobile browsers where Leaflet adds `.leaflet-touch` on `#leaflet`, `vendor/leaflet.css:326` overrides `width`, `height`, and `line-height` back to `30px` instead of `2rem` (`32px`). (2) P01-T01 initializes `listEmpty` with `hidden: "hidden"` and mutates `listEmpty.hidden = d.items.length > 0`, whereas `app.js:27, 2505` uses boolean `hidden: true` (`el.setAttribute("hidden", "")`), and lightweight Node `vm` Element stubs in `src/api/tests/` track `attrs.hidden` separately from `.hidden` unless synchronized.
* Impact: Leaflet zoom controls render at inconsistent `30px` vs `32px` geometry on touch-capable devices, and P03-T01's Node `vm` test for `mapPanel` zero-item empty state risks false results if `.hidden` and `setAttribute("hidden", "")` are not kept consistent.
* Smallest useful change: In P01-T03, keep `.leaflet-bar a{min-width:1.5rem;min-height:1.5rem;width:2rem;height:2rem;line-height:2rem}` and add `.leaflet-touch .leaflet-bar a{width:2rem;height:2rem;line-height:2rem}` in `style.css` so both static regex checks on `.leaflet-bar a` and touch-device specificity succeed; in P01-T01 and P03-T01, initialize `listEmpty` with `hidden: true` (matching `homeCard` at `app.js:2505`) and specify synchronizing `el.hidden` with `attrs.hidden` in the P03-T01 Node `vm` DOM stub.
* Action owner: planning_parent
* Exact resolving evidence: Updated P01-T01, P01-T03, and P03-T01 details in .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md covering `.leaflet-touch .leaflet-bar a` and `hidden: true` / `vm` property synchronization.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Guard preservation is thorough and explicit: the plan accounts for `test_accessibility_baseline.py` (`"Show this chart as a table"`, `h("table", {},` count, non-conformance disclaimer), `employee_acceptance_check.py` (`.maplist li` preservation by placing `p.maplist-empty` outside `ul.plainlist`), `test_finance_exposure_screen.py` (`financeQueueView` `\n}\n` slice boundary), `test_content_standard.py` (banned jargon list), `test_epic149_form_error_summary_associations.py` (`NO_FIELD_FOCUS`), `test_epic149_landmarks_skip_link_focus_order.py` (`NO_SKIP_LINK`, `NO_NAV`), and `test_epic149_ux_evidence_results.py` (`SURFACES`, non-empty `## Recorded gaps` naming `/law.html` and `skip`).
* Contrast token adjustments (`--muted: #595550` giving >= 6.46:1 on `--bg: #f6f4ef` and >= 5.01:1 on `--soft: #ece8df`, and `--warn: #b3360a` giving >= 5.14:1 on `#ffffff` and >= 4.71:1 on `--bg`) satisfy WCAG 1.4.3 Level AA across all token pairings without introducing undocumented `:root` token names that would trip `test_design_system.py`.
* Accepted residual risk: Automated HTML/CSS/Node `vm` checks establish deterministic engineering baseline evidence, while assistive-technology traversal, screen-reader announcement timing, and browser reflow/zoom acceptance remain human testing gates explicitly disclosed in `docs/reference/research/ux/wcag-conformance-baseline.md`.

## Questions or Blocking Evidence Gaps

* None. All five findings are resolved directly from repository source files already in the workspace; no user clarification or additional research is needed.

## Limitations

* Critique evaluated static HTML/CSS/JS templates, DOM-construction logic, and Python/Node test harnesses in the workspace; live browser rendering and real screen-reader interaction were not executed during plan critique.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Directly revise .copilot-tracking/plans/2026-11-15/wcag-baseline-151-plan.md and .copilot-tracking/details/2026-11-15/wcag-baseline-151-phase-details.md to apply PC-001 through PC-005 (`progress.js` variables/multi-series indexing/IIFE contract, `role-screens.js:50` `rowHeader = true`, `P01-T02` exact field names and `.table-scroll` targets, `P02`/`P03` traceability gate ordering, and `.leaflet-touch .leaflet-bar a` + `hidden: true`), then finalize the plan without a second critique pass.
* User response required: No
