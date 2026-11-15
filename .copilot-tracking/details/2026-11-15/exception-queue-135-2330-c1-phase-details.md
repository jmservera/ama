<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #135 Cycle 1 Accessibility Baseline and List Export Inventory Alignment

## Metadata

* Task ID: issue-135-2330-c1
* Task slug: exception-queue-135-2330-c1
* Related plan: .copilot-tracking/plans/2026-11-15/exception-queue-135-2330-c1-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/exception-queue-135-2330-c1-research.md, src/api/src/zava_forward/api/web/app.js, src/api/src/zava_forward/api/server.py, src/api/tests/test_accessibility_baseline.py, src/api/tests/test_epic149_form_error_summary_associations.py, src/api/tests/test_list_export_inventory.py, docs/reference/research/ux/wcag-conformance-baseline.md

## Phase Index

| Phase ID | Name                                                                        | Status | Detail sections                |
|----------|-----------------------------------------------------------------------------|--------|--------------------------------|
| P01      | Counted Guard Test Suites, WCAG Baseline Record, and Focused Validation     | complete | P01, P01-T01, P01-T02, P01-T03 |

<!-- rpi:phase id=P01 -->
## P01: Counted Guard Test Suites, WCAG Baseline Record, and Focused Validation

### Context

Hosted `src-api` Run `43662563387` executed 3,533 tests against commit `39fc2e7fa` on `feat/ux-135-exception-queue-2330` and failed exclusively on four counted baseline/inventory assertions (`C4`, `C5`, `C6`, `C10`). Research (`C1`–`C3`) verified that `renderExceptionRecoveryForm` and `exceptionsView` in `src/api/src/zava_forward/api/web/app.js` already satisfy every substantive WCAG 2.2 AA static rule, Epic #149 focus/association/copy rule, and `POST`-only endpoint boundary without needing edits to `web/app.js` or `server.py`.

### Intent

Align the three counted guard test suites in `src/api/tests/` and the maintained WCAG 2.2 baseline + KB index/log in `docs/reference/` with the audited `#/exceptions` implementation, and prove zero regressions across Focused-tier validation.

### Boundaries

* Included: `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_epic149_form_error_summary_associations.py`, `src/api/tests/test_list_export_inventory.py`, `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, and `docs/reference/log.md`.
* Excluded: Modifying `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/server.py`, `src/core/`, or `workbench_browser_check.py`; creating alias test files; pushing to remote.

### Likely Targets

* src/api/tests/test_accessibility_baseline.py: Update `sites` count (`8 -> 9`), add `test_exception_recovery_reason_field_is_tied_to_its_visible_message`, and update `tables` count (`13 -> 14`) with dated comment.
* src/api/tests/test_epic149_form_error_summary_associations.py: Update `SITES` (9th entry for `app.js` `reasonInput`), `RECOVERY_COPY` (new `app.js` audit-reason prompt), and `test_counted_baseline_is_unchanged_and_fully_mapped` (`8 -> 9`).
* src/api/tests/test_list_export_inventory.py: Add `"/api/exceptions/recovery"` to `EXEMPT`.
* docs/reference/research/ux/wcag-conformance-baseline.md: Update `ms.date` and append dated `2026-11-15 (#135)` source audits to `Error identification` and `Tables`.
* docs/reference/README.md and docs/reference/log.md: Update index row for `wcag-conformance-baseline.md` and append dated KB log entry.

### Dependencies

* None.

### Validation Expectations

* Focused unittest run (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`, `test_exception_register.py`, `test_exception_queue_ui.py`, `test_exception_register_screen.py`, `test_epic149_ux_journey_requirement_traceability.py`, `test_epic149_ux_evidence_results.py`, `test_production_ux_acceptance_protocol.py`, `test_content_standard.py`, plus `src/core/tests/test_live_doc_links.py`), `ruff check .`, `ruff format --check .`, and `mypy` in `src/api` exit `0`.

### Completion Evidence

* Updated test and documentation files, green Focused-tier test/lint/typecheck outputs recorded in `.copilot-tracking/changes/2026-11-15/exception-queue-135-2330-c1-changes.md`, and clean local commit after `rpi-review`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Update counted accessibility, form-error, and list-export inventory tests in src/api/tests/

#### Context

* `test_accessibility_baseline.py` currently asserts `self.assertEqual(sites, 8, ...)` and `self.assertEqual(tables, 13, ...)`, and includes a focused wiring check (`test_saved_held_copy_field_is_tied_to_its_visible_message`) for the 8th `aria-invalid` site (`C4`).
* `test_epic149_form_error_summary_associations.py` asserts `"self.assertEqual(sites, 8,"` in `test_accessibility_baseline.py`, `self.assertEqual(found, 8)`, `len(SITES) == found`, `.focus()` within +/-4 lines around each `invalid` string not in `NO_FIELD_FOCUS`, and plain-language `RECOVERY_COPY` free of `RAW_ERROR` (`C5`). Note: in `test_epic149_form_error_summary_associations.py`, `window(text, needle)` returns the first matching line, and `reasonInput.setAttribute("aria-invalid", "true")` is unique in `app.js` (line 2118, distinct from `why.setAttribute("aria-invalid", "true")` at line 530), with `reasonInput.focus()` 3 lines below at line 2121 (`C1`, `C5`).
* `test_list_export_inventory.py` requires every `/api/...` literal matched by `ENDPOINT` to appear in `EXPORTED`, `BROWSER_EXPORT`, or `EXEMPT`, and requires every `EXEMPT` value to end with `.` and avoid `r"\b(gate|hold|provenance|trace|snapshot|envelope)s?\b"` (`C6`).

#### Intent

Update all three test files with exact, non-vacuous assertions covering the audited `#/exceptions` form error site, table, and recovery POST endpoint.

#### Boundaries

* Included:
  * In `src/api/tests/test_accessibility_baseline.py`:
    * Change `self.assertEqual(sites, 8, ...)` to `self.assertEqual(sites, 9, ...)` (typed cleanly for `ruff` / `mypy`).
    * Add `test_exception_recovery_reason_field_is_tied_to_its_visible_message(self) -> None:` slicing `"function renderExceptionRecoveryForm("` through `"async function exceptionsView("` in `APP` and asserting:
      * `'const errId = `ex-err-${index}`;'`
      * `'h("p", { id: errId, class: "field-error", role: "alert", hidden: true })'`
      * `'"aria-describedby": `${hintId} ${errId}`'`
      * `'h("label", { for: reasonId }, "Audit reason (required, recorded in the audit log)")'`
      * `'reasonInput.setAttribute("aria-invalid", "true")'`, `'reasonInput.removeAttribute("aria-invalid")'`, `'errNode.hidden = false'`, `'errNode.hidden = true'`, and `'reasonInput.focus()'`
    * Update comment and assertion in `test_every_table_has_a_caption_and_column_headers` from `13` to `14` noting the `2026-11-15` source audit of the `#/exceptions` competing source values table (`#135`).
  * In `src/api/tests/test_epic149_form_error_summary_associations.py`:
    * Append 9th tuple to `SITES`:
      ```python
      (
          "app.js",
          'reasonInput.setAttribute("aria-invalid", "true")',
          '"aria-describedby": `${hintId} ${errId}`',
          'h("p", { id: errId, class: "field-error", role: "alert"',
      ),
      ```
    * Append recovery prompt tuple to `RECOVERY_COPY`:
      `("app.js", "Enter the audit reason before recording a recovery decision."),`
    * Update `test_counted_baseline_is_unchanged_and_fully_mapped` comment and assertions from `8` to `9` (`self.assertIn("self.assertEqual(sites, 9,", BASELINE_TEST.read_text())` and `self.assertEqual(found, 9)`).
    * Do NOT add `("app.js", 'reasonInput.setAttribute("aria-invalid", "true")')` to `NO_FIELD_FOCUS`, so `test_marking_a_field_invalid_moves_focus_or_records_the_gap` actively enforces `reasonInput.focus()`.
  * In `src/api/tests/test_list_export_inventory.py`:
    * Add `<= 100`-character `ruff`-clean entry to `EXEMPT` (matching `"/api/packages/"` and `"/api/workorders/"`):
      `"/api/exceptions/recovery": "One exception decision; the exception register exports.",`
* Excluded: Removing any existing test method (`none` removed), weakening regexes, or touching unrelated test files.

#### Likely Targets

* src/api/tests/test_accessibility_baseline.py: Count updates (`9`, `14`) and 9th-site static wiring test.
* src/api/tests/test_epic149_form_error_summary_associations.py: `SITES`, `RECOVERY_COPY`, and `9` count assertions.
* src/api/tests/test_list_export_inventory.py: `EXEMPT` entry for `"/api/exceptions/recovery"`.

#### Dependencies

* None.

#### Validation Expectations

* `PYTHONPATH=tests:src:../core/src:../agents/src:../orchestrator/src:../importer/src:../core/tests:../agents/tests python3 -B -m unittest tests/test_accessibility_baseline.py tests/test_epic149_form_error_summary_associations.py tests/test_list_export_inventory.py -v` exits `0`.

#### Completion Evidence

* All three guard test suites pass with zero failures and pass `ruff` and `mypy`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Record the 9th aria-invalid and 14th table source audits in WCAG baseline and synchronize KB index and log

#### Context

* `docs/reference/research/ux/wcag-conformance-baseline.md` records dated per-addition source audits in the `Error identification` row (currently 8 sites) and `Tables` row (currently 13 tables) (`C7`).
* `test_accessibility_baseline.py` forbids WCAG conformance claims (`\bfully conforms\b|\bis WCAG 2\.2 (AA )?compliant\b`), `test_epic149_ux_journey_requirement_traceability.py` verifies every `test_*.py` identifier named in `docs/reference/research/ux/*.md` exists and compiles, and `test_epic149_ux_evidence_results.py` verifies human-gate caveats remain intact (`C4`, `C8`).
* `docs/reference/README.md:1075` states `table inventory 13 on 2026-11-11`, and Knowledge Base Conventions require updating `docs/reference/README.md` and appending to `docs/reference/log.md` when a KB document materially changes (`C7`).

#### Intent

Document the dated `2026-11-15 (#135)` source audits honestly in `wcag-conformance-baseline.md` and synchronize `docs/reference/README.md` and `docs/reference/log.md`.

#### Boundaries

* Included:
  * In `docs/reference/research/ux/wcag-conformance-baseline.md`:
    * Update frontmatter `ms.date: 2026-11-15`.
    * In `Error identification` (`3.3.1, 3.3.3`) row, append `2026-11-15 (#135, Cycle 1): the inventory is now nine sites after a hosted 9 != 8 failure. The new site is the exception recovery audit-reason textarea (renderExceptionRecoveryForm on #/exceptions in app.js), read from source: named by a visible label for, aria-describedby linking its hint and a hidden field-error role="alert" paragraph; on blank submit the handler sets aria-invalid, reveals the paragraph and fills it with plain-language reason, owner and next action before calling reasonInput.focus(), and clears both on non-empty input or valid submit. Focused static checks in test_accessibility_baseline.py and test_epic149_form_error_summary_associations.py and Node-VM checks in test_exception_queue_ui.py cover markup and state transitions; not screen-reader, assistive-technology or human tested; no conformance claim`.
    * In `Tables` (`1.3.1, 4.1.2`) row, append `2026-11-15 (#135, Cycle 1): the regex-counted inventory is now 14. The new table is the competing source values table on #/exceptions (exceptionsView in app.js), read from source: first-child screen-reader-only caption, four th scope="col" headers (Value, Source, Date, Version), th scope="row" value cells (Unknown as plain text when absent), plain-text source, date and translate="no" version cells, inside a keyboard-focusable table-scroll region with tabindex="0" named for the conflict item. Node-VM tests in src/api/tests/test_exception_queue_ui.py cover rendering and structure; they are not accessibility tests. Not tested: screen-reader navigation, reflow at 320 px, zoom, assistive technology, manual acceptance. No conformance claim`.
  * In `docs/reference/README.md`:
    * Update `ms.date: 2026-11-15` if appropriate and update the `Zava Forward Workbench WCAG 2.2 Conformance Baseline` row summary and date (`2026-11-15`) to state `error-identification inventory 9 and table inventory 14 on 2026-11-15 (#135 exception queue, source audit only); no conformance claim`.
  * In `docs/reference/log.md`:
    * Append a `## [2026-11-15] update | Issue #135 exception queue WCAG baseline and export inventory alignment (Refs #135)` entry with `*` bullets, plain ASCII punctuation, relative links, and explicit non-conformance / unticked human-gate caveats.
* Excluded: Rewriting earlier `docs/reference/log.md` entries, altering blank `Not run` manual test cells, citing nonexistent test filenames, or using `.copilot-tracking/` links inside `docs/`.

#### Likely Targets

* docs/reference/research/ux/wcag-conformance-baseline.md: Frontmatter date, `Error identification` row, and `Tables` row.
* docs/reference/README.md: Index entry for `wcag-conformance-baseline.md`.
* docs/reference/log.md: Append-only KB log entry.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `test_accessibility_baseline.py`, `test_epic149_ux_journey_requirement_traceability.py`, `test_epic149_ux_evidence_results.py`, `test_production_ux_acceptance_protocol.py`, and `src/core/tests/test_live_doc_links.py` exit `0`.

#### Completion Evidence

* Updated Markdown files passing all UX traceability, non-conformance, and relative-link tests.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Execute Focused-tier unit, doc-traceability, ruff, and mypy checks and record implementation evidence

#### Context

Focused-tier validation requires running the targeted baseline guard suites, the `#135` API/UI test suites (`test_exception_register.py`, `test_exception_queue_ui.py`, `test_exception_register_screen.py` in place of the nonexistent `test_exception_recovery_api_135.py` shorthand), sibling UX/doc-link checks, `ruff check`, `ruff format --check`, and `mypy`.

#### Intent

Prove complete regression-free execution and capture verbatim validation evidence in `.copilot-tracking/changes/2026-11-15/exception-queue-135-2330-c1-changes.md`.

#### Boundaries

* Included:
  * Run `unittest` in `src/api` across `tests/test_accessibility_baseline.py`, `tests/test_epic149_form_error_summary_associations.py`, `tests/test_list_export_inventory.py`, `tests/test_exception_register.py`, `tests/test_exception_queue_ui.py`, `tests/test_exception_register_screen.py`, `tests/test_epic149_ux_journey_requirement_traceability.py`, `tests/test_epic149_ux_evidence_results.py`, `tests/test_production_ux_acceptance_protocol.py`, and `tests/test_content_standard.py`.
  * Run `python3 -B -m unittest tests/test_live_doc_links.py -v` from `src/core`, and explicitly verify that every relative link added in `docs/reference/log.md` (which `test_live_doc_links.py` skips as history) resolves to an existing file on disk.
  * Run `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `python3 -m mypy src tests/test_accessibility_baseline.py tests/test_epic149_form_error_summary_associations.py tests/test_list_export_inventory.py tests/test_exception_register.py tests/test_exception_queue_ui.py` (plus full `python3 -m mypy` matching `src-ci.yml`) from `src/api`.
* Excluded: Pushing to remote.

#### Likely Targets

* .copilot-tracking/changes/2026-11-15/exception-queue-135-2330-c1-changes.md: Implementation and validation evidence artifact.

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* Every listed command exits `0`.

#### Completion Evidence

* Verbatim command results recorded in `.copilot-tracking/changes/2026-11-15/exception-queue-135-2330-c1-changes.md`.

#### Unresolved Items

* None.
