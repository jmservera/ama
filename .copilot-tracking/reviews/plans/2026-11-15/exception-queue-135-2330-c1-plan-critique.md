<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #135 Cycle 1 Accessibility Baseline and List Export Inventory Alignment

## Metadata

* Task ID: issue-135-2330-c1
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/exception-queue-135-2330-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/exception-queue-135-2330-c1-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Cycle 1 remediation on branch `feat/ux-135-exception-queue-2330` (stacked PR #1757 for Issue #135) fixing all four hosted `src-api` Run `43662563387` unit test failures introduced by commit `39fc2e7fa` (`#/exceptions` in `src/api/src/zava_forward/api/web/app.js`): `test_accessibility_baseline.py:100` (`9 != 8`), `test_accessibility_baseline.py:146` (`14 != 13`), `test_epic149_form_error_summary_associations.py:117` (`9 != 8`), and `test_list_export_inventory.py:116` (`['/api/exceptions/recovery'] != []`), plus updating `docs/reference/research/ux/wcag-conformance-baseline.md`, synchronizing `docs/reference/README.md` and `docs/reference/log.md` under Knowledge Base Conventions, validating at the Focused tier (`unittest`, Epic #149 UX/doc-link checks, `ruff`, and `mypy`), and committing locally (`Refs #135` + Copilot trailer) without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/exception-queue-135-2330-c1-research.md, .copilot-tracking/plans/2026-11-15/exception-queue-135-2330-c1-plan.md, .copilot-tracking/details/2026-11-15/exception-queue-135-2330-c1-phase-details.md, src/api/src/zava_forward/api/web/app.js, src/api/src/zava_forward/api/server.py, src/api/pyproject.toml, src/api/tests/test_accessibility_baseline.py, src/api/tests/test_epic149_form_error_summary_associations.py, src/api/tests/test_list_export_inventory.py, src/api/tests/test_exception_queue_ui.py, src/api/tests/test_exception_register_screen.py, src/api/tests/test_epic149_ux_journey_requirement_traceability.py, src/api/tests/test_epic149_ux_evidence_results.py, src/api/tests/test_production_ux_acceptance_protocol.py, src/api/tests/test_ux_design_traceability.py, src/api/tests/test_screen_design_traceability.py, src/api/tests/test_content_standard.py, src/api/tests/test_data_steward_screen_wcag.py, src/api/tests/test_epic149_role_workbench_heading_hierarchy.py, src/core/tests/test_live_doc_links.py, tools/check-legacy-references.py, docs/reference/research/ux/wcag-conformance-baseline.md, docs/reference/README.md, and docs/reference/log.md.
* Decisions, dependencies, and acceptance criteria considered: Substantive WCAG 2.2 AA and Epic #149 compliance in `web/app.js` and `server.py` verified from source without runtime code edits; Focused validation tier; lock test edits to the three counted guard suites (`0` removed tests, `0` new test files, `1` added static test method); preserve pending human accessibility gates (`#151`, `#155`, `#619`) without conformance claims; satisfy `FR-1` through `FR-4`, `NFR-1`, `NFR-2`, and `AC-1` through `AC-5`.
* Assessment boundary: Evaluates plan completeness, exact substring/slice/regex compatibility against `web/app.js` and `server.py`, hidden documentation/traceability/link/lexical assertions across `src/api/tests/`, `src/core/tests/`, and `tools/`, and `ruff`/`mypy` configuration in `src/api/pyproject.toml`. Does not evaluate manual screen-reader, assistive-technology, 320 px reflow, or zoom testing, which remain explicitly open human gates under `#151` and `#155`.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1 / AC-1 / AC-2 (9th `aria-invalid` baseline & static wiring) | Covered | `P01-T01` updates `sites == 9` in `test_accessibility_baseline.py` (preserving exact `"self.assertEqual(sites, 9,"` substring checked by `test_epic149_form_error_summary_associations.py:114`), verifies all 9 exact DOM substrings in `renderExceptionRecoveryForm`, maps the 9th `SITES` entry and `RECOVERY_COPY` prompt without adding a `NO_FIELD_FOCUS` gap (`reasonInput.focus()` is +3 lines from `setAttribute` at `app.js:2118-2121`). Anchor slice with `function renderExceptionRecoveryForm(` for future-proof precision (`PC-001`). |
| FR-2 / AC-1 (14th script-built `<table>` baseline alignment) | Covered | `P01-T01` updates `tables == 14` in `test_accessibility_baseline.py:146`; `exceptionsView` at `app.js:2284-2293` has a first-child `sr-only` `<caption>`, four `th scope="col"` headers, `th scope="row"` value cells, and zero bare `h("th", {}` calls. |
| FR-3 / AC-3 (`/api/exceptions/recovery` inventory classification) | Covered | `server.py:1419` confirms `/api/exceptions/recovery` is `POST`-only while `GET /api/exceptions` (`server.py:790`) is already in `BROWSER_EXPORT`. `EXEMPT["/api/exceptions/recovery"]` ends with `.` and avoids all six banned stems (`gate|hold|provenance|trace|snapshot|envelope`), needing only `<= 100`-character formatting to satisfy `ruff` on `test_list_export_inventory.py` (`PC-001`). |
| FR-4 / AC-4 (WCAG baseline record & KB synchronization) | Covered | `P01-T02` updates `wcag-conformance-baseline.md`, `docs/reference/README.md`, and `docs/reference/log.md` while preserving all pinned phrases in `test_accessibility_baseline.py`, `test_epic149_ux_journey_requirement_traceability.py`, `test_epic149_ux_evidence_results.py`, and `test_production_ux_acceptance_protocol.py`, and citing only real runnable test modules (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_exception_queue_ui.py`). Minor statement-order phrasing polish noted in `PC-002`. |
| NFR-1 / NFR-2 / AC-5 (Focused validation, lint, types, style & local commit) | Covered | `P01-T03` covers all three guard suites, all three real `#135` test modules (`test_exception_register.py`, `test_exception_queue_ui.py`, `test_exception_register_screen.py`), Epic #149 UX/content suites, `src/core/tests/test_live_doc_links.py`, `ruff check .`, `ruff format --check .`, and `mypy`. Explicit `docs/reference/log.md` relative-link check noted in `PC-002`. |
| Research `C1`..`C10` | Covered | All ten codebase and CI findings are accurately translated into `P01-T01` through `P01-T03`, including the Contrarian catches on `POST /api/exceptions/recovery` and nonexistent `test_exception_recovery_api_135.py`. |
| P01 (`P01-T01`, `P01-T02`, `P01-T03`) | Covered | Credible and ready for implementation; two Low-severity planner-applicable polish items (`PC-001`, `PC-002`) prevent lint-wrap friction and keep source-audit prose exact. |

## Verdict

* Verdict: Pass
* Rationale: The candidate plan and phase details are complete, accurate, and directly executable with zero Critical, High, or Medium defects and zero unresolved user decisions. Cross-checking all hidden guard suites across `src/api/tests/`, `src/core/tests/`, `src/api/pyproject.toml`, and `tools/` confirms that every substring assertion, `window(..., 4, 4)` focus check, banned-vocabulary regex, runnable `test_*.py` doc-citation check, requirement-ID regex (`(?:FR|NFR|AC|SA|OD)-\d+`), non-conformance guard, and relative-link check will pass. Two Low-severity non-blocking polish items (`PC-001` on `ruff` 100-char formatting and slice anchoring in `P01-T01`, and `PC-002` on literal synchronous statement order in `P01-T02` plus `docs/reference/log.md` link verification in `P01-T03`) can be folded in directly by the planning parent before implementation.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Low]: `EXEMPT["/api/exceptions/recovery"]` single-line literal exceeds 100 characters under strict `ruff` rules on `test_list_export_inventory.py`, and `APP` slice start can anchor on `function `

* Related IDs: FR-1, FR-3, NFR-1, C4, C6, P01-T01
* Evidence: .copilot-tracking/details/2026-11-15/exception-queue-135-2330-c1-phase-details.md:77, .copilot-tracking/details/2026-11-15/exception-queue-135-2330-c1-phase-details.md:104, src/api/pyproject.toml:30-56, src/api/tests/test_list_export_inventory.py:50-94, src/api/tests/test_accessibility_baseline.py:106, src/api/src/zava_forward/api/web/app.js:2080
* Concern: Two minor precision details in `P01-T01`: (1) Unlike `test_accessibility_baseline.py`, `src/api/tests/test_list_export_inventory.py` is not in `per-file-ignores` or `ruff.format.exclude` in `src/api/pyproject.toml` (`line-length = 100`, `E501` enabled). Indented 4 spaces inside `EXEMPT`, `"/api/exceptions/recovery": "Decision on one exception item; the exception register exports its summary.",` is 110 characters, which triggers `E501` and `ruff format --check` failure unless wrapped with parentheses or shortened to `<= 100` characters (for example `"/api/exceptions/recovery": "One exception decision; the exception register exports.",`, 88 chars, matching `"/api/packages/": "One package action; the packages list exports.",`). (2) Slicing `APP` from `"function renderExceptionRecoveryForm("` to `"async function exceptionsView("` anchors strictly to the function declaration at `app.js:2080` (matching `text.index("function fundingSavedCopyCheck(")` in `test_accessibility_baseline.py:106`) so any future call site above line 2080 cannot widen the slice.
* Impact: Low; `P01-T03` already runs `ruff check .` and `ruff format --check .`, which would catch the 110-character line during implementation, but tightening both strings in `P01-T01` avoids an avoidable lint-fix round-trip and hardens the `APP` slice boundary.
* Smallest useful change: In `P01-T01`, either wrap `EXEMPT["/api/exceptions/recovery"]` across parenthesized lines per `ruff format` or use the `<= 100`-character single-line string `"/api/exceptions/recovery": "One exception decision; the exception register exports.",`, and slice `APP` starting at `"function renderExceptionRecoveryForm("`.
* Action owner: planning_parent
* Exact resolving evidence: `.copilot-tracking/details/2026-11-15/exception-queue-135-2330-c1-phase-details.md` (`P01-T01`) specifies a `ruff`-compliant `<= 100`-char or parenthesized `EXEMPT` entry and `"function renderExceptionRecoveryForm("` slice start, and `ruff check . && ruff format --check .` exits `0`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Low]: `P01-T02` `Error identification` prose slightly inverts the synchronous statement order in `app.js:2118-2121`, and `docs/reference/log.md` links are skipped by `test_live_doc_links.py`

* Related IDs: FR-4, NFR-2, AC-4, AC-5, C1, C7, C8, P01-T02, P01-T03
* Evidence: .copilot-tracking/details/2026-11-15/exception-queue-135-2330-c1-phase-details.md:134, .copilot-tracking/details/2026-11-15/exception-queue-135-2330-c1-phase-details.md:166-168, src/api/src/zava_forward/api/web/app.js:2118-2121, src/core/tests/test_live_doc_links.py:14
* Concern: (1) In `P01-T02`, the draft `Error identification` sentence says `which the submit check fills with plain-language reason, owner and next action and reveals before setting aria-invalid and calling reasonInput.focus()` (mirroring site #8 in `role-screens.js`). In `app.js:2118-2121`, the submit handler executes `reasonInput.setAttribute("aria-invalid", "true")` first (line 2118), then `errNode.hidden = false` (line 2119) and `errNode.textContent = ...` (line 2120), before calling `reasonInput.focus()` (line 2121). (2) `src/core/tests/test_live_doc_links.py` skips `docs/reference/log.md` (`HISTORY = ("docs/capstone/", "docs/reference/log.md")`), so the relative link `[research/ux/wcag-conformance-baseline.md](research/ux/wcag-conformance-baseline.md)` added to `docs/reference/log.md` relies on explicit path verification during `P01-T03` diff review.
* Impact: Low; no automated test fails because of the prose phrasing, and `[research/ux/wcag-conformance-baseline.md](research/ux/wcag-conformance-baseline.md)` in `P01-T02` already resolves cleanly from `docs/reference/log.md`, but stating the exact source sequence keeps `wcag-conformance-baseline.md` strictly literal to `app.js:2118-2121`.
* Smallest useful change: Update the `P01-T02` `Error identification` prose fragment to `sets aria-invalid, reveals the paragraph and fills it with plain-language reason, owner and next action before calling reasonInput.focus()`, and verify the added `docs/reference/log.md` relative link target directly during `P01-T03` diff review.
* Action owner: planning_parent
* Exact resolving evidence: `.copilot-tracking/details/2026-11-15/exception-queue-135-2330-c1-phase-details.md` (`P01-T02`, `P01-T03`) reflects the literal `app.js:2118-2121` statement sequence and verifies the `docs/reference/log.md` relative link target.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Substantive compliance was verified before incrementing any ratchet: `renderExceptionRecoveryForm` (`app.js:2093-2159`) and `exceptionsView` (`app.js:2283-2293`) genuinely satisfy `<label for>`, `aria-describedby`, `role="alert"` `.field-error` with non-colour glyph, immediate `.focus()` within Epic #149's +/-4-line window, `sr-only` first-child `<caption>`, scoped column/row headers, and `tabindex="0"` scrollable table regions.
* Hidden UX documentation traps are already neutralized: `P01-T02` cites only real runnable test modules (`test_exception_queue_ui.py`, `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`), avoids unverified `(FR|NFR|AC|SA|OD)-\d+` tokens, preserves every pinned phrase required by `test_accessibility_baseline.py`, `test_epic149_ux_journey_requirement_traceability.py`, `test_epic149_ux_evidence_results.py`, and `test_production_ux_acceptance_protocol.py`, and synchronizes `docs/reference/README.md` and `docs/reference/log.md`.
* Explicitly accepted residual risk: Manual screen-reader, assistive-technology, 320 px reflow, and zoom acceptance remain unperformed human gates under `#151` and `#155`, and are honestly recorded as untested with no WCAG conformance claim.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* This critique is a static source, test-contract, and documentation audit over repository files and the supplied Research/Plan artifacts; execution of the test, lint, and type-check commands belongs to `rpi-implement` (`P01-T03`).

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply the two minor compatible Low-severity polish adjustments (`PC-001`, `PC-002`) in `P01-T01` through `P01-T03` (or record their disposition in `Critique Disposition`), mark the plan `Ready for implementation`, and proceed directly to `rpi-implement` without another critique pass.
* User response required: no
