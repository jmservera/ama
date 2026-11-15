<!-- markdownlint-disable-file -->
# RPI Plan: Issue #135 Cycle 1 Accessibility Baseline and List Export Inventory Alignment

## Task Metadata

* Task ID: issue-135-2330-c1
* Task slug: exception-queue-135-2330-c1
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/exception-queue-135-2330-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/exception-queue-135-2330-c1-plan-critique.md

## Executive Summary

This Cycle 1 plan resolves all four hosted `src-api` unit test failures reported in GitHub Actions Run `43662563387` for stacked PR #1757 (`feat/ux-135-exception-queue-2330` -> `feat/demo-233-same-home-tensions-0825`, Issue #135). Commit `39fc2e7fa` introduced the interactive `#/exceptions` workbench view in `src/api/src/zava_forward/api/web/app.js` (adding 1 new `setAttribute("aria-invalid", "true")` site, 1 new competing-values `<table>`, and 1 `POST /api/exceptions/recovery` call), which tripped counted baseline ratchets in `test_accessibility_baseline.py` (`9 != 8`, `14 != 13`), `test_epic149_form_error_summary_associations.py` (`9 != 8`), and `test_list_export_inventory.py` (`['/api/exceptions/recovery'] != []`), while all 3,529 other `src-api` tests passed.

Source-level accessibility and HTTP route audits in Research (`C1`–`C10`) established that `web/app.js` and `server.py` already satisfy every substantive WCAG 2.2 AA static rule, Epic #149 focus/association/copy rule, and `POST`-action boundary without requiring runtime code changes. This plan updates the counted baselines, maps the 9th `aria-invalid` site and recovery error copy with a dedicated static wiring check, classifies `/api/exceptions/recovery` in `EXEMPT` as a single-item `POST` decision action alongside existing `BROWSER_EXPORT` coverage for `GET /api/exceptions`, and records the dated source audit in `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, and `docs/reference/log.md`.

### User Decisions and Requirements Highlights

* **Genuine audit before ratchet updates**: Both the new `#/exceptions` `aria-invalid` site (`reasonInput` in `renderExceptionRecoveryForm`) and competing-values `<table>` (`exceptionsView`) were audited against WCAG 2.2 AA static rules and Epic #149 requirements before updating the counted guard tests and UX conformance record.
* **Focused validation tier**: Validation runs the three counted guard test suites, the `#135` API/UI test suites, sibling Epic #149 / doc-link / content-standard regression suites, `ruff check`, `ruff format --check`, and `mypy`.
* **Local-only commit**: Commit cleanly on `feat/ux-135-exception-queue-2330` with a Conventional Commit message (`Refs #135`) and the Copilot `Co-authored-by` trailer; do NOT push, leaving an empty `git status --short`.

### What You May Not Know

* **`/api/exceptions/recovery` is `POST`-only (`server.py:1419`)**: `test_list_export_inventory.py` uses a lexical regex (`\b(?:api|get|fetch)\(\s*[`"'](/api/...)`) that matches `api("/api/exceptions/recovery", body)` even when a body makes `api()` send `POST`. Because `GET /api/exceptions` is already registered in `BROWSER_EXPORT` (`exception-register-visible-summary.csv`), `/api/exceptions/recovery` belongs in `EXEMPT` just like `/api/packages/`, `/api/workorders/`, and `/api/ai/review/`, using plain-language copy that avoids banned words (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`).
* **Doc-referenced test module validation (`test_epic149_ux_journey_requirement_traceability.py`)**: Every `test_*.py` filename mentioned anywhere under `docs/reference/research/ux/*.md` is parsed and verified to exist and compile. The `#135` test modules in `src/api/tests/` are `test_exception_register.py`, `test_exception_queue_ui.py`, and `test_exception_register_screen.py` (`test_exception_recovery_api_135.py` does not exist), so `wcag-conformance-baseline.md` must cite only real test modules.
* **Immediate focus already satisfied (`app.js:2118-2121`)**: `reasonInput.focus()` appears 3 lines after `reasonInput.setAttribute("aria-invalid", "true")`, within Epic #149's +/-4-line window, so no `NO_FIELD_FOCUS` gap exemption is needed.

### Unresolved Decisions or Blockers

* None blocking implementation. Assistive-technology, screen-reader, 320 px reflow, and zoom acceptance remain pending human gates under `#151` and `#155`, and no WCAG conformance claim is made.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`), adding dated artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`) for Cycle 1 of Issue #135 (PR #1757) in `/home/azureuser/source/ama-demo-wt/feat-135-c1` on branch `feat/ux-135-exception-queue-2330` (user prompt).
* Audit the new `#/exceptions` `aria-invalid` site and `<table>` in `src/api/src/zava_forward/api/web/app.js`, and fix all four hosted `src-api` Run `43662563387` failures across `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_epic149_form_error_summary_associations.py`, `src/api/tests/test_list_export_inventory.py`, and `docs/reference/research/ux/wcag-conformance-baseline.md` (user prompt).
* Follow Knowledge Base Conventions when materially updating `docs/reference/research/ux/wcag-conformance-baseline.md` by keeping `docs/reference/README.md` and `docs/reference/log.md` synchronized without rewriting prior log entries (`.github/copilot-instructions.md`).
* Validate at the Focused tier using `unittest` across the baseline guard suites and `#135` test suites plus `ruff check`, `ruff format --check`, and `mypy` in `src/api` (user prompt; `.github/copilot-instructions.md`).
* Commit locally with a Conventional Commit message (`Refs #135`) and trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, do NOT push, and leave a clean frozen worktree (`git status --short` empty) (user prompt).

## Goals

* Update the accessibility and form-error baseline guard suites (`test_accessibility_baseline.py` and `test_epic149_form_error_summary_associations.py`) to reflect and statically verify the audited 9th `aria-invalid` site and 14th script-built `<table>` introduced by `#/exceptions` in `web/app.js`.
* Update `test_list_export_inventory.py` to classify the `POST`-only `/api/exceptions/recovery` action in `EXEMPT` with plain-language, banned-term-free rationale referencing the existing exception register summary export.
* Record an accurate, non-conformance-claiming dated source audit in `docs/reference/research/ux/wcag-conformance-baseline.md` and synchronize `docs/reference/README.md` and `docs/reference/log.md` so all `src/api` and `src/core` documentation/traceability guards pass.

## Scope and Non-Goals

### In Scope

* Updating `src/api/tests/test_accessibility_baseline.py` (`sites` `8 -> 9`, `tables` `13 -> 14`, plus one focused static test `test_exception_recovery_reason_field_is_tied_to_its_visible_message`).
* Updating `src/api/tests/test_epic149_form_error_summary_associations.py` (`8 -> 9`, adding the 9th `SITES` entry for `app.js` `reasonInput` and its plain-language `RECOVERY_COPY` entry).
* Updating `src/api/tests/test_list_export_inventory.py` (`EXEMPT["/api/exceptions/recovery"]`).
* Updating `docs/reference/research/ux/wcag-conformance-baseline.md` (`ms.date`, `Error identification` row, and `Tables` row), `docs/reference/README.md` (index summary and date for `wcag-conformance-baseline.md`), and appending one entry to `docs/reference/log.md`.

### Non-Goals

* Modifying `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/server.py`, or any `src/core` production file (substantive compliance already verified in Research `C1`–`C3`).
* Adding an unrequested `GET /api/exceptions/recovery.csv` route or creating a dummy `test_exception_recovery_api_135.py` alias file.
* Pushing commits to any remote or modifying GitHub PR state.

## Functional Requirements

* **FR-1 (9th `aria-invalid` Baseline & Static Wiring Verification)**: `test_accessibility_baseline.py` asserts `sites == 9` and verifies in a dedicated static check (`test_exception_recovery_reason_field_is_tied_to_its_visible_message`) that `renderExceptionRecoveryForm` in `app.js` binds `<label for>`, `aria-describedby` (`${hintId} ${errId}`), `errNode` (`class: "field-error"`, `role: "alert"`), sets/clears `aria-invalid`, and calls `reasonInput.focus()`; `test_epic149_form_error_summary_associations.py` maps all 9 sites in `SITES` (without adding a `NO_FIELD_FOCUS` gap) and verifies the plain-language recovery prompt in `RECOVERY_COPY`.
  * Observable acceptance criteria: `Wcag22Baseline` and `FormErrorAssociations` pass completely with zero failures.
* **FR-2 (14th Script-Built `<table>` Baseline Alignment)**: `test_accessibility_baseline.py` asserts `tables == 14`, verifying that the `#/exceptions` competing-source-values table in `app.js` has a first-child `<caption>` and zero unscoped `<th>` cells.
  * Observable acceptance criteria: `Wcag22Baseline.test_every_table_has_a_caption_and_column_headers` passes with `tables == 14`.
* **FR-3 (`/api/exceptions/recovery` Endpoint Inventory Classification)**: `test_list_export_inventory.py` registers `"/api/exceptions/recovery"` in `EXEMPT` with a plain-language explanation ending in `.` and containing zero banned internal stems (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`).
  * Observable acceptance criteria: `InventoryIsComplete`, `ExportRowContracts`, and `ExportsLeaveStateUnchanged` in `test_list_export_inventory.py` pass completely.
* **FR-4 (WCAG Conformance Baseline Record & KB Synchronization)**: `docs/reference/research/ux/wcag-conformance-baseline.md` updates `ms.date` to `2026-11-15` and appends dated `2026-11-15 (#135)` source-audit notes to `Error identification` (9 sites) and `Tables` (14 tables) citing real runnable tests (`test_exception_queue_ui.py`, `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`), stating what remains untested, and claiming no WCAG conformance; `docs/reference/README.md` updates the index row and `docs/reference/log.md` appends a dated entry.
  * Observable acceptance criteria: `test_accessibility_baseline.py`, `test_epic149_ux_journey_requirement_traceability.py`, `test_epic149_ux_evidence_results.py`, `test_production_ux_acceptance_protocol.py`, and `src/core/tests/test_live_doc_links.py` all pass.

## Non-Functional Requirements

* **NFR-1 (Lint, Format, and Static Type Safety)**: All modified Python test files in `src/api/tests/` pass `ruff check`, `ruff format --check`, and `mypy` with zero errors or warnings.
  * Objective threshold or evaluation condition: Exit code `0` for `ruff check`, `ruff format --check`, and `mypy` in `src/api`.
  * Operating condition or verification approach, if needed: Run tools from `src/api` against `src` and the modified/targeted test modules.
  * Observable acceptance criteria: All three commands exit `0`.
* **NFR-2 (Test Ownership Lock & Markdown Style Discipline)**: Lock test changes strictly to the 3 existing guard test modules (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`), with exact test removals = `none`, new test files = `0`, and maximum added test methods = `1`; use plain ASCII punctuation, `*` list markers, no em dashes, and no `.copilot-tracking/` references in docs, tests, or commit messages.
  * Objective threshold or evaluation condition: `0` removed tests, `0` new test files, `1` added test method (`test_exception_recovery_reason_field_is_tied_to_its_visible_message`), `0` unresolved doc links, and `0` `.copilot-tracking/` citations outside `.copilot-tracking/`.
  * Operating condition or verification approach, if needed: Inspect `git diff` and run link/traceability checks.
  * Observable acceptance criteria: All checks pass and `git status --short` is empty after local commit.

## Acceptance Criteria

* AC-1: `test_accessibility_baseline.py` passes with `sites == 9`, `tables == 14`, and `test_exception_recovery_reason_field_is_tied_to_its_visible_message` green.
* AC-2: `test_epic149_form_error_summary_associations.py` passes with `found == 9`, 9 mapped `SITES` entries, no added `NO_FIELD_FOCUS` gap, and the new `app.js` recovery message verified in `RECOVERY_COPY`.
* AC-3: `test_list_export_inventory.py` passes with `/api/exceptions/recovery` explained in `EXEMPT` in plain language without banned vocabulary.
* AC-4: `docs/reference/research/ux/wcag-conformance-baseline.md`, `docs/reference/README.md`, and `docs/reference/log.md` accurately document the 9th `aria-invalid` site and 14th `<table>` source audits without claiming WCAG conformance, and pass all Epic #149 UX traceability and live-doc-link tests.
* AC-5: Focused validation (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`, `test_exception_register.py`, `test_exception_queue_ui.py`, `test_exception_register_screen.py`, Epic #149 UX doc tests, `test_live_doc_links.py`, `ruff check .`, `ruff format --check .`, and `mypy`) passes with exit code `0`, and changes are committed locally on `feat/ux-135-exception-queue-2330` (`Refs #135` + Copilot trailer) without pushing.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                                 |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/exception-queue-135-2330-c1-plan.md                                                                     |
| Phase details                    | .copilot-tracking/details/2026-11-15/exception-queue-135-2330-c1-phase-details.md                                                          |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/exception-queue-135-2330-c1-plan-critique.md with Pass (PC-001, PC-002 applied)                 |
| Relevant research                | .copilot-tracking/research/2026-11-15/exception-queue-135-2330-c1-research.md                                                              |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/exception-queue-135-2330-c1-changes.md is created by implementation as its evidence record            |
| Planning execution and readiness | Complete; Ready for implementation                                                                                                         |
| Continuation context             | Confirmed automatic RPI Agent session continues directly to `rpi-implement` once critique passes or compatible revisions are applied       |

## Sources

* .copilot-tracking/research/2026-11-15/exception-queue-135-2330-c1-research.md: Cycle 1 Wider/Deeper/Contrarian audit (`C1`–`C10`) of `app.js`, `server.py`, `style.css`, hosted Run `43662563387`, and UX/KB guards.
* src/api/src/zava_forward/api/web/app.js and src/api/src/zava_forward/api/server.py: Audited `#/exceptions` DOM wiring (`renderExceptionRecoveryForm`, `exceptionsView`) and `POST /api/exceptions/recovery`.
* src/api/tests/test_accessibility_baseline.py, src/api/tests/test_epic149_form_error_summary_associations.py, and src/api/tests/test_list_export_inventory.py: Counted accessibility, form-error, and endpoint-export guard suites.
* docs/reference/research/ux/wcag-conformance-baseline.md, docs/reference/README.md, and docs/reference/log.md: Maintained WCAG 2.2 AA audit baseline, KB index, and append-only KB log.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Counted Guard Test Suites, WCAG Baseline Record, and Focused Validation

* Intent: Update the three counted `src/api/tests/` guard modules and synchronize the WCAG 2.2 baseline record, KB index, and KB log, then run all Focused-tier unit, doc-traceability, lint, format, and `mypy` checks.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update counted accessibility, form-error, and list-export inventory tests in src/api/tests/

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-1, NFR-2; research evidence `C1`, `C2`, `C3`, `C4`, `C5`, `C6`.
* Expected result: `test_accessibility_baseline.py` asserts `sites == 9` and `tables == 14` and adds `test_exception_recovery_reason_field_is_tied_to_its_visible_message`; `test_epic149_form_error_summary_associations.py` asserts `9` sites and adds the `app.js` `reasonInput` row in `SITES` and prompt in `RECOVERY_COPY`; `test_list_export_inventory.py` registers `"/api/exceptions/recovery"` in `EXEMPT` with plain-language non-banned rationale.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/exception-queue-135-2330-c1-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Record the 9th aria-invalid and 14th table source audits in WCAG baseline and synchronize KB index and log

* Requirement and evidence: FR-4, NFR-2; research evidence `C1`, `C3`, `C4`, `C7`, `C8`, `C9`.
* Expected result: `docs/reference/research/ux/wcag-conformance-baseline.md` updates `ms.date: 2026-11-15` and appends dated `2026-11-15 (#135)` source-audit entries to `Error identification` and `Tables` citing real test modules without conformance claims; `docs/reference/README.md` updates the index row and date; `docs/reference/log.md` appends a dated update entry.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/exception-queue-135-2330-c1-phase-details.md

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Execute Focused-tier unit, doc-traceability, ruff, and mypy checks and record implementation evidence

* Requirement and evidence: AC-1 through AC-5, NFR-1, NFR-2; research evidence `C8`, `C9`, `C10`.
* Expected result: Guard suites, `#135` API/UI suites (`test_exception_register.py`, `test_exception_queue_ui.py`, `test_exception_register_screen.py`), Epic #149 UX/traceability suites, `test_live_doc_links.py`, `ruff check .`, `ruff format --check .`, and `mypy` pass with exit code `0`, recorded in `.copilot-tracking/changes/2026-11-15/exception-queue-135-2330-c1-changes.md`.
* Detail section: P01-T03 in .copilot-tracking/details/2026-11-15/exception-queue-135-2330-c1-phase-details.md

## Dependencies

* Editable `zava-forward-core`, `zava-forward-agents`, and `zava-forward-api` packages plus `ruff`, `mypy`, and `node` in workspace environment: Required to run Focused-tier unit, Node-VM UI, lint, format, and type checks in `src/api`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| 2026-11-15 PC-001 [Low]  | Applied     | Updated `P01-T01` in phase details to use the `<= 100`-character `ruff`-clean string `"/api/exceptions/recovery": "One exception decision; the exception register exports.",` in `test_list_export_inventory.py` and anchor the `APP` slice start on `"function renderExceptionRecoveryForm("`. |
| 2026-11-15 PC-002 [Low]  | Applied     | Updated `P01-T02` `Error identification` prose to match the literal statement order in `app.js:2118-2121` (`sets aria-invalid, reveals the paragraph and fills it... before calling reasonInput.focus()`), and added explicit disk-resolution verification in `P01-T03` for the relative link added to `docs/reference/log.md`. |

## Follow-Up Items

* Wire a shared `[data-unsaved="true"]` `beforeunload` and hash-navigation guard across employee workbench forms in `src/api/src/zava_forward/api/web/app.js` (carried forward from parent task review `RV-001`; outside Cycle 1 CI baseline fix scope).
* Connect standalone importer process rejected-batch storage directly to the shared database without manual refusal-ledger transfer once importer storage topology is unified (carried forward from parent plan; outside `#135` workbench/register scope).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/exception-queue-135-2330-c1-changes.md
* Ready phase or task: Complete (all P01 tasks verified; ready for rpi-review)
* Remaining provisional question or blocker: none
