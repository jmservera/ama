---
description: "Primary evidence artifact for Cycle 1 of Issue #135 (PR #1757) counted baseline and list export inventory alignment"
---
<!-- markdownlint-disable-file -->

# Task Research: exception-queue-135-2330-c1

| Field              | Value                                                                         |
|--------------------|-------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                    |
| Researcher / agent | rpi-research (via RPI Agent)                                                  |
| Status             | Complete                                                                      |
| Artifact path      | .copilot-tracking/research/2026-11-15/exception-queue-135-2330-c1-research.md |

## Research Brief

* What to research: Exact audit requirements and counted baseline contracts triggered in hosted `src-api` Run 43662563387 after commit `39fc2e7fa` added `#/exceptions` in `src/api/src/zava_forward/api/web/app.js` and `GET /api/exceptions/recovery` in `src/api/src/zava_forward/api/server.py`.
* Why it matters: Four counted guard assertions in `src/api/tests/` (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`) fail until the new `aria-invalid` site, `<table>`, form error summary mapping, list export/explanation disposition for `/api/exceptions/recovery`, and corresponding WCAG conformance baseline documentation are audited and updated accurately.
* Audience or intended use: Planning, implementation, and review phases (`rpi-plan`, `rpi-implement`, `rpi-review`) in this Cycle 1 automatic RPI loop.
* Scope: `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_epic149_form_error_summary_associations.py`, `src/api/tests/test_list_export_inventory.py`, `src/api/tests/test_exception_recovery_api_135.py`, and `docs/reference/research/ux/wcag-conformance-baseline.md` (plus any cross-referenced inventory/export docs).
* Non-goals: Pushing to remote, altering unrelated workbench screens, weakening WCAG 2.2 AA / Epic #149 / list export invariants, or touching `workbench_browser_check.py` unless strictly required.
* Criteria: Genuine accessibility and list-export audit of the new `#/exceptions` DOM and `/api/exceptions/recovery` endpoint—verifying whether `app.js` or `server.py` needs any code adjustment vs baseline/inventory registration—so all 4 assertions and the full `src/api` unit test suite, `mypy`, and `ruff` pass cleanly without shortcuts.
* Requested outputs: Complete audit of the 4 failing contracts, exact remediation recommendation, and Planning Readiness assessment.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                                                                             |
|--------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | Do the new `#/exceptions` `aria-invalid` site, `<table>`, form error summary association, and `/api/exceptions/recovery` endpoint genuinely satisfy every substantive rule enforced by the 3 guard test suites and UX baseline docs, or is a code change in `app.js`/`server.py` also required alongside updating the counted inventories and documentation? |
| Codebase scope                       | `src/api/src/zava_forward/api/`, `src/api/tests/`, `docs/reference/research/ux/`                                                                                                                  |
| External scope                       | Web Interface Guidelines source only if `web/app.js` requires modification in later phases (`none` during read-only codebase audit unless needed)                                                 |
| Initial internal candidate areas     | `src/api/tests/test_accessibility_baseline.py`, `src/api/tests/test_epic149_form_error_summary_associations.py`, `src/api/tests/test_list_export_inventory.py`, `src/api/src/zava_forward/api/web/app.js`, `src/api/src/zava_forward/api/server.py`, `docs/reference/research/ux/wcag-conformance-baseline.md` |
| Initial external candidate areas     | none                                                                                                                                                                                              |
| Research posture                     | focused                                                                                                                                                                                           |
| Posture provenance                   | default (bounded Cycle 1 CI remediation with exact named failing tests and commit `39fc2e7fa` scope)                                                                                              |
| Explicit limits / deadline           | Focused validation tier; commit locally with `Refs #135` and required Co-authored-by trailer; do NOT push; leave clean worktree                                                                   |
| Posture-specific completion basis    | focused scope and materiality across all 4 failing assertions, underlying `app.js`/`server.py` behavior, and `src/api` sibling guard tests                                                        |
| Edits allowed during research?       | no, research-only                                                                                                                                                                                 |
| Resolved evidence root               | `.copilot-tracking/` default                                                                                                                                                                      |
| Known constraints / excluded sources | Preserve Fluent 2 design system, WCAG 2.2 AA baseline, plain-language content standard, and knowledge-base conventions; no `.copilot-tracking/` paths in production code, docs, or commit messages |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                                        | Match and provenance                                            | Scoped authority or output contract                                                                  | Selected / skipped reason                                                                                                      |
|---------------------|------------------------------------------------------------------|-----------------------------------------------------------------|------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA Repository Instructions)  | `applyTo: "**"` matches workspace inputs and tracking artifacts | Enforces WCAG baseline, Fluent 2, plain-language content standard, KB log rules, and validation tier | Selected: mandatory repository governance for UX baseline docs, web audit, and commit workflow.                                |
| Skill               | `redesign-existing-projects` & `web-design-guidelines`           | Conditional match if `src/api/.../web/app.js` needs edits       | Guides accessible existing-app UI updates and web review                                             | Deferred during read-only Research; recorded for activation in Implement if `web/app.js` requires edits.                       |
| Skill               | `accessibility`                                                  | Topic match on WCAG 2.2 AA / form error summary / table headers | General WCAG 2.2 / ARIA reference                                                                    | Skipped during Research: repository test assertions and `wcag-conformance-baseline.md` encode the exact local contract directly. |
| Research specialist | `hve-core-all:rpi-researcher`                                    | Host-visible general research worker                            | Bounded subagent lane artifact                                                                       | Skipped (inline execution): 6 tightly coupled local files fit a direct single-context read with higher precision and zero drift. |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                      | Answers / unanswered | Resulting decision or selected further research                                          |
|------------------|------------------------------------------------------------------------------------------------------------|----------------------|------------------------------------------------------------------------------------------|
| Intake           | Non-interactive CLI session with exact hosted CI failure traceback, named files, and validation commands   | N/A (non-interactive)| Proceed with `focused` posture in `convergence` mode on Cycle 1 of Issue #135 (PR #1757).|
| Direction change | None at intake                                                                                             | N/A                  | Maintain initial Cycle 1 scope.                                                          |
| Convergence      | Completed Cycle 1 Wider, Deeper, and Contrarian audit across `app.js`, `server.py`, `style.css`, 3 failing guard suites, and UX docs | N/A (automatic mode) | Converged on updating counted baselines/mappings (`8 -> 9` invalid sites, `13 -> 14` tables), adding a focused static check for the 9th site, adding `/api/exceptions/recovery` to `EXEMPT` in `test_list_export_inventory.py`, and updating `wcag-conformance-baseline.md` + KB index/log with zero `app.js`/`server.py` mutations needed. |

## Scope and Success Criteria

* Scope: Audit `app.js`, `server.py`, the three failing test modules, any sibling `src/api` tests that inspect `wcag-conformance-baseline.md` or list exports, and `docs/reference/research/ux/wcag-conformance-baseline.md`.
* Assumptions: Commit `39fc2e7fa` passed qualitative accessibility checks on the individual elements or partially mapped them, and tripped counted ratchets—this assumption MUST be verified rather than trusted blindly.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Audit the new `#/exceptions` `aria-invalid` site and table in `app.js`, update `test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`, and `docs/reference/research/ux/wcag-conformance-baseline.md` (if referenced), validate, and commit without pushing.
* Inferred research questions: Does `#/exceptions` genuinely satisfy Epic #149 form error summary linking, WCAG 2.2 caption + `<th scope="col">`, `aria-describedby` message binding, and list export / non-export rationale rules? Do any other tests in `src/api/tests/` parse `wcag-conformance-baseline.md` or export inventories? Does modifying `docs/reference/research/ux/wcag-conformance-baseline.md` require a `docs/reference/log.md` update under Knowledge Base Conventions?
* Caller constraints and non-goals: Focused validation tier; do not push; leave clean worktree.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                             | Source / checkpoint | Effect on active brief, evidence, or revalidation                |
|----------------------------------------------------------|-----------------------------------------------------------------------------------|---------------------|------------------------------------------------------------------|
| narrow                                                   | Focused tier validation; local commit with `Refs #135`; do NOT push               | User intake         | Governs validation and closeout state.                           |

## Research Questions

|  # | Sub-question                                                                                                                                      | Type (depth / breadth / straightforward) | Priority | Status   |
|---:|---------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------|----------|----------|
| Q1 | How is `#/exceptions` implemented in `web/app.js` and `server.py` (specifically its `aria-invalid` input, error summary/message wiring, `<table>`, and `/api/exceptions/recovery` endpoint)? | depth                                    | H        | answered |
| Q2 | What exact substantive and counted checks do `test_accessibility_baseline.py` and `test_epic149_form_error_summary_associations.py` enforce, and does `#/exceptions` satisfy all substantive rules or need an `app.js` fix? | depth                                    | H        | answered |
| Q3 | What exact rules does `test_list_export_inventory.py` enforce for screen-read endpoints, and should `/api/exceptions/recovery` be CSV-exported or documented as a justified non-list action? | depth                                    | H        | answered |
| Q4 | How is `docs/reference/research/ux/wcag-conformance-baseline.md` (and any other UX doc or `docs/reference/log.md`) referenced by tests and Knowledge Base Conventions? | breadth                                  | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/rpi-sessions/2026-11-14/exception-queue-135-2330-state.json`, `.copilot-tracking/research/2026-11-14/exception-queue-135-2330-research.md`, `.copilot-tracking/reviews/logs/2026-11-14/exception-queue-135-2330-review.md`, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/reference/research/ux/wcag-conformance-baseline.md`.
* Reused (verified) findings: Commit `39fc2e7fa` on `feat/ux-135-exception-queue-2330` delivered `#/exceptions` in `web/app.js` and comprehensive tests in `src/api/tests/test_exception_register.py` and `src/api/tests/test_exception_queue_ui.py` (`C1`, `C2`, `C9`). Hosted `src-api` Run `43662563387` ran 3,533 tests with 3,529 passing and only the 4 counted baseline/inventory assertions failing (`C10`).
* Superseded / stale: Caller prompt referenced `tests/test_exception_recovery_api_135.py` and `GET /api/exceptions/recovery`; direct codebase and Git history inspection proved that `/api/exceptions/recovery` is a `POST`-only action endpoint in `server.py` (`C2`) and that the `#135` API/UI test modules in `src/api/tests/` are `test_exception_register.py`, `test_exception_queue_ui.py`, and `test_exception_register_screen.py` (`C9`).

## Research Cycle Log

### Cycle 1

* Active direction controls: Focused validation tier; local commit with `Refs #135`; do NOT push.
* Active research posture and completion basis: `focused`; focused scope and materiality across all 4 failing assertions, underlying `app.js`/`server.py`/`style.css` contracts, and sibling `src/api` UX/traceability guard suites.
* Explicit limits or deadline effect: None restricted investigation of any relevant file or hosted CI log.

#### Wave 1: Wider

* Plan and independent lanes: Inline sweep of commit `39fc2e7fa`, hosted CI Run `43662563387` failure log, the 3 failing test files (`test_accessibility_baseline.py`, `test_epic149_form_error_summary_associations.py`, `test_list_export_inventory.py`), `.github/workflows/src-ci.yml`, and sibling UX/traceability test modules referencing `wcag-conformance-baseline.md`.
* Worker evidence relationships or inline fallback: Inline fallback (tightly coupled local audit across 6 files): Q1 -> `C1`, `C2`, `C3`; Q2 -> `C4`, `C5`; Q3 -> `C2`, `C6`; Q4 -> `C7`, `C8`, `C9`, `C10`.
* Reflection: Hosted Run `43662563387` confirmed that 3,529 of 3,533 `src-api` unit tests already pass (`C10`), isolating the failures strictly to the 4 counted guard assertions (`C4`, `C5`, `C6`). Wave 2 needed to audit whether `app.js` genuinely satisfies every substantive WCAG 2.2 / Epic #149 / Issue #80 rule before incrementing any count.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Line-by-line audit of `renderExceptionRecoveryForm` (`app.js:2081-2160`), the competing source values `<table>` in `exceptionsView` (`app.js:2283-2293`), CSS token/visibility rules (`style.css:25,263-264,337-339`), and HTTP route wiring (`server.py:790,1419`).
* Plan and independent lanes:
  1. Audit 9th `aria-invalid` site (`app.js:2118`): `reasonInput` (`textarea#ex-reason-${index}`) has visible `<label for="ex-reason-${index}">`, `"aria-describedby": "${hintId} ${errId}"`, `errNode` (`p#ex-err-${index}.field-error`, `role="alert"`, `hidden: true` hidden via `[hidden]{display:none!important}` in `style.css:25`). On blank submit, sets `aria-invalid="true"` (2px `--warn` border, 3.8:1 contrast), un-hides `errNode` (renders `\26A0` warning glyph + 5.6:1 contrast plain-language Reason/Owner/Next action copy), and calls `reasonInput.focus()` 3 lines later (satisfying Epic #149's 4-line focus window without needing a `NO_FIELD_FOCUS` gap exemption). Clears `aria-invalid`, hides `errNode`, and empties text on valid `input` or submit (`C1`, `C3`, `C4`, `C5`).
  2. Audit 14th `<table>` (`app.js:2284`): First child is `h("caption", { class: "sr-only" }, "Competing source values for ${item.id} with source, date and version")`; `<thead>` defines 4 `th scope="col"` cells (`Value`, `Source`, `Date`, `Version`); `<tbody>` uses `th scope="row"` for the value column (rendering `"Unknown"` as text when null) and plain-text `<td>` cells (`<code translate="no">` for version); wrapped in keyboard-focusable `div.table-scroll[tabindex="0"][role="region"][aria-label="Competing source values for ${item.id}"]` with global two-tone `:focus-visible` (`C1`, `C3`, `C4`).
  3. Audit `/api/exceptions/recovery` in `test_list_export_inventory.py`: `server.py:1419` defines `/api/exceptions/recovery` exclusively under `do_POST` (`s.request_exception_recovery(...)`), while `GET /api/exceptions` (`server.py:790`) is already covered in `BROWSER_EXPORT` (`exception-register-visible-summary.csv` in `role-screens.js`, `C2`, `C6`). `test_list_export_inventory.py`'s `ENDPOINT` regex (`\b(?:api|get|fetch)\(\s*[`"'](/api/...)`) matches `await api("/api/exceptions/recovery", { key, action, reason })` (`app.js:2131`) even though passing a second argument to `api()` sends `POST`. Every analogous single-record `POST` action matched by `ENDPOINT` (`/api/ai/priority/`, `/api/ai/review/`, `/api/packages/`, `/api/workorders/`, `/api/login`, `/api/logout`, `/api/import-check`) is registered in `EXEMPT` with a plain-language reason ending in `.` and avoiding banned vocabulary (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) (`C6`).
* Worker evidence relationships or inline fallback: Inline audit confirmed substantive compliance across `C1`–`C6`.
* Reflection: Neither `app.js` nor `server.py` requires modification; all substantive accessibility, focus, plain-language, and route contracts are already met. Wave 3 needed to challenge whether updating `wcag-conformance-baseline.md`, `EXEMPT`, or test references could trip any sibling Epic #149, content-standard, doc-link, or KB-governance check.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries:
  1. Could `/api/exceptions/recovery` require a new CSV export route instead of an `EXEMPT` entry?
  2. Could citing a nonexistent test module (like `test_exception_recovery_api_135.py`) or claiming conformance in `wcag-conformance-baseline.md` break `test_epic149_ux_journey_requirement_traceability.py` or `test_epic149_ux_evidence_results.py`?
  3. Does updating `docs/reference/research/ux/wcag-conformance-baseline.md` require updating `docs/reference/README.md` and `docs/reference/log.md`, and do any link checkers (`test_live_doc_links.py`) validate them?
* Plan and independent lanes: Inspected `test_epic149_ux_journey_requirement_traceability.py`, `test_epic149_ux_evidence_results.py`, `test_production_ux_acceptance_protocol.py`, `test_content_standard.py`, `test_live_doc_links.py`, `docs/reference/README.md`, and `docs/reference/log.md`.
* Worker evidence relationships or inline fallback:
  1. Disproved CSV-export alternative for `/api/exceptions/recovery`: `server.py:1419` has no `GET /api/exceptions/recovery` route; it is a single-item `POST` mutation, and `ExportsLeaveStateUnchanged` in `test_list_export_inventory.py` requires every `EXPORTED` entry to be a read-only `GET` CSV route with a download link (`C2`, `C6`). Furthermore, the underlying queue list `GET /api/exceptions` already has its summary export registered in `BROWSER_EXPORT` (`C6`). Therefore `EXEMPT` is the exact, truthful classification.
  2. Confirmed critical doc-test trap: `ControlClaimsMapToTests.test_every_test_module_named_in_the_ux_docs_exists_and_runs` (`C8`) parses every `test_[a-z0-9_]+\.py` mention in `docs/reference/research/ux/*.md` and asserts the file exists and compiles! Citing `test_exception_recovery_api_135.py` would fail `test_epic149_ux_journey_requirement_traceability.py` because that filename does not exist (`C9`); citing `test_exception_queue_ui.py`, `test_accessibility_baseline.py`, and `test_epic149_form_error_summary_associations.py` resolves cleanly (`C8`, `C9`).
  3. Confirmed KB governance and link invariants: `docs/reference/README.md:1075` explicitly states `table inventory 13 on 2026-11-11` (`C7`). Under Knowledge Base Conventions, materially updating `wcag-conformance-baseline.md` requires updating its `docs/reference/README.md` row and appending a dated entry to `docs/reference/log.md`, while ensuring all relative Markdown links pass `test_live_doc_links.py` and `RelativeLinks` (`C7`, `C8`).
* Reflection: Contrarian sweep caught two subtle traps (`test_every_test_module_named_in_the_ux_docs_exists_and_runs` and banned vocabulary in `EXEMPT` reasons) and confirmed exact KB index/log alignment. No material uncertainty remains.

#### Parent Synthesis and Disposition

| Material / claim                                                                                                           | Evidence IDs   | Parent disposition | Evidence-based rationale                                                                                                                     | Primary-artifact treatment       |
|----------------------------------------------------------------------------------------------------------------------------|----------------|--------------------|----------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------|
| `#/exceptions` `reasonInput` (`app.js:2118`) and competing-values `<table>` (`app.js:2284`) satisfy substantive WCAG/Epic #149 rules without editing `app.js` | `C1, C3, C4, C5` | accepted           | Visible `<label for>`, `aria-describedby` (`hintId` + `errId`), `.field-error` alert with glyph, `reasonInput.focus()`, `sr-only` caption, `scope="col"`/`"row"`, and focusable `table-scroll` region are all present in `app.js`. | Selected recommendation          |
| Update counted baseline (`8 -> 9` invalid sites, `13 -> 14` tables), add focused 9th-site static test in `test_accessibility_baseline.py`, and map 9th site + recovery copy in `test_epic149_form_error_summary_associations.py` | `C1, C4, C5`   | accepted           | Matches the exact pattern established for the 8th site (`test_saved_held_copy_field_is_tied_to_its_visible_message`) and Epic #149 `SITES` / `RECOVERY_COPY`. | Selected recommendation          |
| Register `"/api/exceptions/recovery"` in `EXEMPT` in `test_list_export_inventory.py` with plain-language non-banned wording | `C2, C6`       | accepted           | `/api/exceptions/recovery` is a single-item `POST` decision route (`server.py:1419`), while `GET /api/exceptions` is already in `BROWSER_EXPORT`. | Selected recommendation          |
| Add a new `GET /api/exceptions/recovery.csv` route instead of `EXEMPT`                                                     | `C2, C6`       | rejected           | `/api/exceptions/recovery` is not a `GET` list endpoint; adding an artificial CSV route for a `POST` action violates KISS and misrepresents the API. | Recorded as rejected alternative |
| Update `wcag-conformance-baseline.md`, `docs/reference/README.md`, and `docs/reference/log.md` citing only real test modules (`test_exception_queue_ui.py`) and claiming no conformance | `C7, C8, C9`   | accepted           | Required by `test_accessibility_baseline.py`, `test_epic149_ux_journey_requirement_traceability.py`, `test_epic149_ux_evidence_results.py`, and KB conventions. | Selected recommendation          |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: Focused scope is 100% covered with direct source, CSS, HTTP route, sibling test, and hosted CI log evidence; further cycles would re-read identical files.
* Revised brief or revalidation required: none
* Readiness effect: Ready (`C1`–`C10`)

## Evidence Log

* Delegation: inline: 6 tightly coupled files across one counted-baseline contract fit direct single-context inspection without subagent coordination overhead.

### Codebase Evidence

| ID  | Claim / finding                                                                                                                                      | Location (`path:line`)                                                          | Tool | Confidence | Notes                                                                                          |
|-----|------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|------|------------|------------------------------------------------------------------------------------------------|
| C1  | `renderExceptionRecoveryForm` binds `<label for>`, `aria-describedby` (`${hintId} ${errId}`), `.field-error` (`role="alert"`), `aria-invalid="true"`, and `reasonInput.focus()`; `exceptionsView` builds a `table-scroll` (`tabindex="0"`, `role="region"`) table with first-child `sr-only` `<caption>`, 4 `th scope="col"`, and `th scope="row"` value cells | `src/api/src/zava_forward/api/web/app.js:2093-2159`, `src/api/src/zava_forward/api/web/app.js:2283-2293` | view | high       | Added in commit `39fc2e7fa`; substantive markup already satisfies all static WCAG/Epic #149 rules |
| C2  | `/api/exceptions` is `GET` (`server.py:790`) while `/api/exceptions/recovery` is `POST`-only (`server.py:1419`) calling `s.request_exception_recovery(...)` | `src/api/src/zava_forward/api/server.py:790`, `src/api/src/zava_forward/api/server.py:1419-1427` | view | high       | Confirms `/api/exceptions/recovery` is a single-item POST decision action, not a GET list route |
| C3  | `[hidden]{display:none!important}` hides `errNode` until flagged; `textarea[aria-invalid=true]` adds a 2px `--warn` border; `.field-error:before` adds `\26A0` warning glyph; `.table-scroll:focus-visible` renders two-tone focus | `src/api/src/zava_forward/api/web/style.css:25`, `src/api/src/zava_forward/api/web/style.css:263-264`, `src/api/src/zava_forward/api/web/style.css:337-339` | grep | high       | Proves non-colour error cues and scrollable-region focus styling                               |
| C4  | `Wcag22Baseline` asserts `sites == 8` (`line 100`) and `tables == 13` (`line 146`), includes a dedicated per-site static test (`test_saved_held_copy_field_is_tied_to_its_visible_message`), and forbids conformance claims in `wcag-conformance-baseline.md` | `src/api/tests/test_accessibility_baseline.py:86-156`                           | view | high       | Explains hosted failures #1 (`9 != 8`) and #2 (`14 != 13`)                                     |
| C5  | `FormErrorAssociations` asserts `"self.assertEqual(sites, 8,"` in `test_accessibility_baseline.py`, `found == 8`, `len(SITES) == found`, `.focus()` within +/-4 lines unless in `NO_FIELD_FOCUS`, and plain-language `RECOVERY_COPY` free of `RAW_ERROR` | `src/api/tests/test_epic149_form_error_summary_associations.py:16-190`          | view | high       | Explains hosted failure #3 (`9 != 8`); `reasonInput.focus()` at +3 lines satisfies focus rule   |
| C6  | `InventoryIsComplete` scans JS literals via `ENDPOINT` (`api|get|fetch`), records `/api/exceptions` in `BROWSER_EXPORT`, and requires non-list/POST action paths in `EXEMPT` to end with `.` and omit `gate|hold|provenance|trace|snapshot|envelope` | `src/api/tests/test_list_export_inventory.py:49-125`                            | view | high       | Explains hosted failure #4 (`['/api/exceptions/recovery'] != []`)                              |
| C7  | `wcag-conformance-baseline.md` documents the 8 `aria-invalid` sites (`Error identification` row) and 13 script-built tables (`Tables` row), and `docs/reference/README.md:1075` mirrors the table count and date | `docs/reference/research/ux/wcag-conformance-baseline.md:54-57`, `docs/reference/README.md:1075` | view | high       | Both require dated Cycle 1 updates plus an append-only `docs/reference/log.md` entry           |
| C8  | `ControlClaimsMapToTests.test_every_test_module_named_in_the_ux_docs_exists_and_runs` verifies that every `test_*.py` named in `docs/reference/research/ux/*.md` exists and compiles; `HumanGatesStayPending` enforces non-conformance wording | `src/api/tests/test_epic149_ux_journey_requirement_traceability.py:155-177`, `src/api/tests/test_epic149_ux_evidence_results.py:98-124` | view | high       | Prevents citing nonexistent test module names or claiming WCAG conformance                     |
| C9  | The `#135` test modules in `src/api/tests/` are `test_exception_register.py`, `test_exception_queue_ui.py`, and `test_exception_register_screen.py`; `test_exception_recovery_api_135.py` does not exist in workspace or Git history | `src/api/tests/test_exception_register.py:615-700`, `src/api/tests/test_exception_queue_ui.py:1-616` | glob | high       | Clarifies validation command target modules                                                    |
| C10 | Hosted `src-api` Run `43662563387` executed 3,533 unit tests (`Ran 3533 tests in 893.852s`) with 3,529 passing, 647 skipped, and only the exact 4 counted inventory/baseline failures | `.github/workflows/src-ci.yml:87-96` (verified via `gh run view 43662563387`)   | bash | high       | Confirms zero other regressions exist in `src-api`                                             |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
|----|-----------------|----------------|-----|-----------|--------------|------------|

### Contradictions / Conflicts

* Caller prompt shorthand vs workspace filenames/verbs: The prompt referred to `GET /api/exceptions/recovery` and `tests/test_exception_recovery_api_135.py`; direct inspection of `server.py:1419` (`C2`) and `src/api/tests/` (`C9`) established that `/api/exceptions/recovery` is a `POST`-only endpoint matched by `test_list_export_inventory.py`'s `api(...)` regex (`C6`) and tested in `tests/test_exception_register.py` and `tests/test_exception_queue_ui.py` (`C9`). Resolved by primary codebase truth -> classify `/api/exceptions/recovery` in `EXEMPT` as a single-item recovery decision action and run the actual `#135` test modules (`test_exception_register.py`, `test_exception_queue_ui.py`, `test_exception_register_screen.py`) alongside the 3 guard test modules.

## Findings Mapped to Questions and Evidence

| Question | Finding                                                                                                                                                                                                 | Evidence IDs       | Confidence | Decision or readiness implication                                                                                  |
|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|------------|--------------------------------------------------------------------------------------------------------------------|
| Q1       | `#/exceptions` in `web/app.js` adds 1 `aria-invalid` site (`reasonInput` in `renderExceptionRecoveryForm`), 1 `<table>` (competing source values in `exceptionsView`), and 1 `POST /api/exceptions/recovery` call. | `C1, C2, C3`       | high       | No edits to `app.js` or `server.py` are needed.                                                                    |
| Q2       | Both the 9th `aria-invalid` site and the 14th `<table>` satisfy all substantive WCAG 2.2 AA static rules and Epic #149 focus/association/copy rules; updating counts (`8 -> 9`, `13 -> 14`), adding a 9th-site static test, and mapping `SITES` + `RECOVERY_COPY` cleanly resolves failures #1–#3. | `C1, C3, C4, C5`   | high       | Ready for exact surgical edits in `test_accessibility_baseline.py` and `test_epic149_form_error_summary_associations.py`. |
| Q3       | `/api/exceptions/recovery` is a single-item `POST` decision endpoint while `GET /api/exceptions` already exports via `BROWSER_EXPORT`; adding `/api/exceptions/recovery` to `EXEMPT` with plain-language wording free of banned terms resolves failure #4. | `C2, C6`           | high       | Ready for surgical edit in `test_list_export_inventory.py`.                                                        |
| Q4       | `wcag-conformance-baseline.md` must record the source audit of the 9th `aria-invalid` site and 14th `<table>` without conformance claims and citing only real test modules (`test_exception_queue_ui.py`), accompanied by `docs/reference/README.md` and `docs/reference/log.md` updates. | `C7, C8, C9, C10`  | high       | Preserves Epic #149 doc-test invariants, link checks, and KB conventions.                                          |

## Key Discoveries

* Substantive accessibility compliance is already complete in `web/app.js`: `renderExceptionRecoveryForm` provides a visible `<label for>`, dual `aria-describedby` (`${hintId} ${errId}`), `.field-error` (`role="alert"`) with warning glyph and Reason/Owner/Next action copy, and immediate `reasonInput.focus()`, while `exceptionsView`'s competing-values table provides a first-child `sr-only` `<caption>`, four `th scope="col"` headers, `th scope="row"` value headers, and a `tabindex="0"` `table-scroll` region (`C1`, `C3`).
* `/api/exceptions/recovery` was flagged by `test_list_export_inventory.py` because `ENDPOINT` matches `api("/api/exceptions/recovery", body)` (`POST`) as well as `GET` calls; its queue list `GET /api/exceptions` is already covered in `BROWSER_EXPORT`, so `/api/exceptions/recovery` belongs in `EXEMPT` alongside `/api/packages/`, `/api/workorders/`, and `/api/ai/review/` (`C2`, `C6`).
* `test_epic149_ux_journey_requirement_traceability.py` validates every `test_*.py` identifier written in `docs/reference/research/ux/*.md`, so `wcag-conformance-baseline.md` must cite `test_exception_queue_ui.py` rather than the nonexistent `test_exception_recovery_api_135.py` (`C8`, `C9`).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Keep `web/app.js` and `server.py` unchanged after verifying substantive compliance; update `src/api/tests/test_accessibility_baseline.py` (`sites` `8 -> 9`, `tables` `13 -> 14`, plus `test_exception_recovery_reason_field_is_tied_to_its_visible_message`), `src/api/tests/test_epic149_form_error_summary_associations.py` (`8 -> 9`, 9th `SITES` tuple, `RECOVERY_COPY` tuple), `src/api/tests/test_list_export_inventory.py` (`EXEMPT["/api/exceptions/recovery"]`), and `docs/reference/research/ux/wcag-conformance-baseline.md` + `docs/reference/README.md` + `docs/reference/log.md`.
* Rationale: Directly addresses all 4 hosted `src-api` failures with genuine source-level accessibility and endpoint-inventory audits while preserving every Epic #149, content-standard, link-check, and KB convention.
* Evidence refs: `C1, C2, C3, C4, C5, C6, C7, C8, C9, C10`
* Implementation impact: 3 test files in `src/api/tests/` and 3 documentation files in `docs/reference/`.
* Confidence: high: all 3,529 other `src-api` tests already passed in Run `43662563387` (`C10`).

File tree:

```text
src/api/tests/
  test_accessibility_baseline.py                  (update counts 8->9, 13->14 + add 9th-site static test)
  test_epic149_form_error_summary_associations.py (update count 8->9 + add SITES & RECOVERY_COPY entries)
  test_list_export_inventory.py                   (add /api/exceptions/recovery to EXEMPT)
docs/reference/
  README.md                                       (update WCAG baseline index summary & date)
  log.md                                          (append 2026-11-15 #135 Cycle 1 baseline audit entry)
  research/ux/wcag-conformance-baseline.md        (record 9th aria-invalid site & 14th table source audits)
```

### Alternative: Add a `GET /api/exceptions/recovery.csv` export endpoint

* Approach: Add a new CSV route for recovery requests and register `/api/exceptions/recovery` in `EXPORTED`.
* Trade-offs: Would satisfy `known` membership in `test_list_export_inventory.py` only by inventing a new server endpoint and UI download link that were not requested.
* Evidence refs: `C2, C6`
* Rejection rationale: `/api/exceptions/recovery` is a `POST`-only single-item decision endpoint (`C2`), and `GET /api/exceptions` already exports visible summary rows via `BROWSER_EXPORT` (`C6`).

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Ensure `EXEMPT["/api/exceptions/recovery"]` reason ends with `.` and omits banned internal vocabulary (`gate`, `hold`, `provenance`, `trace`, `snapshot`, `envelope`) (`C6`), and ensure `wcag-conformance-baseline.md` cites only real runnable test modules and makes no WCAG conformance claim (`C4`, `C8`).
* Follow-up: Manual assistive-technology, screen-reader, 320 px reflow, and zoom checks remain open human gates under `#151` / `#155` (`C7`, `C8`).
* Residual uncertainty: none within focused Cycle 1 engineering scope.

## Current Decisions

| Decision                                                                                                                                              | Status    | Owner / source   | Rationale                                                                                                       | Evidence IDs       | Implications                                                                                      |
|-------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|------------------|-----------------------------------------------------------------------------------------------------------------|--------------------|---------------------------------------------------------------------------------------------------|
| Preserve `web/app.js` and `server.py` unchanged and update the 3 counted guard test suites + WCAG baseline & KB index/log after verifying compliance  | confirmed | evidence         | Source audit proved all substantive WCAG 2.2 AA, Epic #149 focus/association, and `POST` action rules already hold. | `C1, C2, C3, C4, C5, C6` | Surgical test + documentation update with zero runtime regression risk in `web/app.js`.           |
| Run actual `#135` API/UI test modules (`test_exception_register.py`, `test_exception_queue_ui.py`, `test_exception_register_screen.py`) in validation | confirmed | evidence         | `test_exception_recovery_api_135.py` does not exist; those 3 modules contain the actual `#135` coverage.         | `C9, C10`          | Honest validation reporting and prevents citing a nonexistent module in UX docs (`C8`).           |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
|----------|------------------------------------|-------|--------|----------------|
| none     | none                               | N/A   | none   | non-blocking   |

## Potential Next Research

| Priority | Research item                                                                    | Expected value                                               | Trigger                                            | Selected? | Related questions / evidence |
|----------|----------------------------------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------------|-----------|------------------------------|
| L        | Shared `[data-unsaved="true"]` navigation guard across employee workbench forms  | Prevents accidental hash-navigation loss of typed form notes | Post-PR #1757 follow-up selection (parent RV-001)  | deferred  | Q1; `C1`                     |

## Planning Readiness

* Status: Ready
* Decision state: Converged on surgical updates to the 3 counted guard test modules and 3 `docs/reference/` files with zero `web/app.js` or `server.py` changes.
* Evidence basis: `C1, C2, C3, C4, C5, C6, C7, C8, C9, C10`
* Preconditions met: All 4 hosted `src-api` failures reproduced and audited against source, CSS, HTTP routing, and sibling doc/traceability guards.
* Blockers: none
* Smallest action to change readiness: none (already Ready)

## Closeout Record

| Field                            | Record                                                                                                        |
|----------------------------------|---------------------------------------------------------------------------------------------------------------|
| Research execution status        | Complete                                                                                                      |
| Completed waves                  | Cycle 1: Wider, Deeper, and Contrarian                                                                        |
| Lane evidence or inline fallback | Inline execution across tightly coupled `src/api` and `docs/reference` files                                  |
| Research disposition             | executed                                                                                                      |
| Planning Readiness               | Ready (`C1`–`C10`)                                                                                            |
| Blockers                         | none                                                                                                          |
| Continuation owner and state     | Confirmed automatic RPI Agent; automatic continuation to `Plan` (`rpi-plan`)                                  |

## Advisory Next Step

| Field                            | Record                                                                                                        |
|----------------------------------|---------------------------------------------------------------------------------------------------------------|
| Research disposition             | executed                                                                                                      |
| Planning Readiness               | Ready (`C1`–`C10`)                                                                                            |
| Output mode and planning support | `convergence`; yes, single evidence-backed remediation selected                                               |
| Acting owner                     | Confirmed automatic RPI Agent                                                                                 |
| Required gates or confirmations  | Research disposition recorded (passed); Planning Readiness `Ready` (passed); pre-transition state write (next)|
| Continuation result              | Automatic continuation to `Plan` (`rpi-plan`)                                                                 |
| Primary evidence file            | .copilot-tracking/research/2026-11-15/exception-queue-135-2330-c1-research.md                                 |
| Notes for planning or re-entry   | Plan single implementation + validation phase covering the 3 test files, 3 KB docs, focused tests, mypy, ruff |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All 4 hosted CI failures and sibling UX/KB invariants are completely verified from primary codebase files; further research is redundant.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings Mapped to Questions, Key Discoveries, Alternatives and Decision State, Open Questions, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources, Artifact Self-Check.
* Missing or limited sections: none

