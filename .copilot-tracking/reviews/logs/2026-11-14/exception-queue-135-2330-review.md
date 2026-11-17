<!-- markdownlint-disable-file -->
# Review: Issue #135 Data Steward and Digital Operator Exception Queue

## Scope and Evidence

* Task ID: issue-135-2330
* Review date: 2026-11-14
* Review scope: full task (`P01`, `P02`, `P03`)
* Assessed boundary: Issue #135 functional requirements (`FR-1`..`FR-5`), non-functional constraints (`NFR-1`..`NFR-3`), acceptance criteria (`AC-1`..`AC-6`), critique dispositions (`PC-001`..`PC-006`), Focused-tier validation evidence across `src/core` and `src/api`, and refreshed Web Interface Guidelines compliance for `src/api/src/zava_forward/api/web/app.js`
* Plan: .copilot-tracking/plans/2026-11-14/exception-queue-135-2330-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/exception-queue-135-2330-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/exception-queue-135-2330-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/exception-queue-135-2330-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/exception-queue-135-2330-research.md; git diff across `src/core` and `src/api`; Focused-tier `mypy`, `ruff check .`, `ruff format --check .`, and `unittest` outputs (`29` core tests; `231` API/UI/WCAG/copy-standard tests); refreshed Web Interface Guidelines (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`)

## Opening Review State

* Interpreted review goal: Perform a single evidence-based post-implementation review verifying that all five Issue #135 acceptance criteria, plan critique fixes (`PC-001`..`PC-006`), Focused-tier checks, and web accessibility/copy/design-system standards are satisfied without touching guarded files.
* Review scope: full task (`P01`, `P01-T01`..`T03`, `P02`, `P02-T01`..`T02`, `P03`, `P03-T01`)
* Evidence readiness: Ready; research, plan, phase details, plan critique, and changes record are complete and reconciled.
* Acceptance basis: `AC-1`..`AC-6`, `FR-1`..`FR-5`, `NFR-1`..`NFR-3`, critique dispositions `PC-001`..`PC-006`, repository UX/WCAG/content standards, and Web Interface Guidelines.
* First comparison boundary: Plan markers and phase details (`P01`–`P03`) compared against `.copilot-tracking/changes/2026-11-14/exception-queue-135-2330-changes.md` and actual `git diff`.
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/logs/2026-11-14/exception-queue-135-2330-review.md` (plus parent RPI session state transitions); no source, test, plan, detail, critique, or changes files are mutated during Review.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Executed once on 2026-11-14 across reconciled `P01`, `P02`, and `P03` artifacts, source/test diffs (`7` modified files, `1` new UI test file), Focused-tier check outputs, and refreshed Web Interface Guidelines rules.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`, `P01-T03`) | Core Exception Queue, Feeds, and Store Register Contract Enrichment | Reconciled | All planned core queue, feed, register, and unit-test changes are complete, checked `[x]`, and validated. |
| `P02` (`P02-T01`, `P02-T02`) | Interactive Employee Workbench Exception Queue View and End-to-End API/UI Tests | Reconciled | `#/exceptions` view in `web/app.js`, `test_exception_register.py` extensions, and `test_exception_queue_ui.py` are complete, checked `[x]`, and validated. |
| `P03` (`P03-T01`) | Interactive Employee Workbench Exception Queue View and End-to-End API/UI Tests + `## Validation Record` | Reconciled | `mypy`, `ruff check .`, `ruff format --check .`, `29` core tests, and `231` API/UI tests are recorded as Passed. |
| `## Follow-Up Items` | Standalone importer rejected-batch storage topology unification | Reconciled | Preserved distinctly outside active `P01`–`P03` scope in both plan and changes record with named owner. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/exception_queue.py`, `src/core/src/zava_forward/core/exception_feeds.py` | Added conflict `resolution_owner`, failure `failure_category`, deterministic `correlation_id` and `recovery_context`, timestamped multi-entry `audit_trail`, `record_detected_outage`, `OUTAGE_NEXT_STEPS`, envelope/batch `correlation_id` extraction, and sourceless `stranded_task` fallback `ref` (`PC-006`). | Diff verified in `exception_queue.py` and `exception_feeds.py`. | Passed (`mypy`, `ruff`, `29` core unit tests) | Reconciled and conformant (`AC-1`..`AC-5`) |
| `P01-T02` | `src/core/src/zava_forward/core/exception_register.py` | Added read-only rejected `import_batches` and `import_exceptions.rejected_batches` projection (`PC-002`), idempotent `deepcopy`-based `_with_recoveries` `audit_trail` reconstruction (`PC-005`), `viewer_roles` + `allowed_kinds` in `access`, and `actual_hold`-aware continuity/service outage projection across `ok` and `roles_not_named` banners (`PC-001`). | Diff verified in `exception_register.py`; `sqlstore.py` untouched. | Passed (`mypy`, `ruff`, `45` tests in `test_exception_register.py`) | Reconciled and conformant (`AC-2`..`AC-5`, `NFR-1`) |
| `P01-T03` | `src/core/tests/test_exception_queue.py`, `src/core/tests/test_exception_feeds.py` | Added `5` focused core unit tests covering `resolution_owner`, `failure_category`, `correlation_id`, `recovery_context`, timestamped `audit_trail`, preserved `Unknown` eligibility / `original_source`, and `outage_banner` `next_steps`. | `5` new test methods verified. | Passed (`Ran 29 tests in 0.006s — OK`) | Reconciled and conformant (`AC-1`..`AC-6`, `NFR-3`) |
| `P02-T01` | `src/api/src/zava_forward/api/web/app.js` | Implemented `#/exceptions` (`exceptionsView`), `"key"` in `mutationKey`, and plain-ASCII `#/exceptions` links in `handoffWaitingView` and `importView` while keeping `role-screens.js`, `workbench.py`, and `workbench_browser_check.py` untouched (`PC-003`, `PC-004`). | Diff verified in `web/app.js`; guarded files untouched. | Passed (`mypy`, `ruff`, `231` tests across 15 `src/api` suites including lexical/WCAG/design-system checks) | Reconciled and conformant (`AC-1`..`AC-5`, `NFR-1`) |
| `P02-T02`, `P03-T01` | `src/api/tests/test_exception_register.py`, `src/api/tests/test_exception_queue_ui.py` | Added `4` register/SQL/JSON/HTTP tests and `1` new Node-VM UI test suite (`5` tests; `14` new methods total across repo, within `<= 1` file and `<= 18` methods budget). | Test execution output verified. | Passed (`Ran 231 tests in 115.091s — OK (skipped=4)`) | Reconciled and conformant (`AC-1`..`AC-6`, `NFR-1`..`NFR-3`) |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T02` (`exception_register._apply_detected_outages`) | Handled both string (`"Pam Lead"`) and mapping (`{"name": ...}`) representations of `incident_owner` on `continuity` suspension records. | `ContinuityMixin.suspend(...)` stores `incident_owner` as a stripped string while raw dictionary fixtures may pass a mapping; no user decision needed. | Recorded in `.copilot-tracking/changes/2026-11-14/exception-queue-135-2330-changes.md` (`## Implementation-Time Plan and Detail Updates`). | Not material; preserves `PC-001` and `P01-T02` exact contract (`Ready`). | Reconciled and justified |

## Critique and Material Revision Assessment

* Latest critique dispositions: All six plan-critique findings (`PC-001`..`PC-006`) were applied before implementation and verified in code and tests (`PC-001`: `history_valid` + `actual_hold` continuity suspension detection and `NO_HEALTH_CHECK` preservation when zero outages exist; `PC-002`: `import_exceptions.rejected_batches` SQLite persistence without editing `sqlstore.py`; `PC-003`: `me.services?.cases === false` unchanged, `baseHash === "#/exceptions"`, `Owner: the programme owner.`, pure ASCII copy, unified `"Keep on hold"` mapper, `<h1>`-first hierarchy; `PC-004`: regression + table/heading suites executed; `PC-005`: `deepcopy`-based idempotent `_with_recoveries` with `POST`/`GET` `audit_trail` length parity `== 2`; `PC-006`: sourceless `stranded_task` fallback `ref = f"task:{case_id}:{task}"` and `meter_id`/import `correlation_id` extraction).
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: Sequential `P01 -> P02 -> P03` order respected with no early resumption.
* Justification assessment: Supported by unit, SQL/JSON restart, HTTP, and Node-VM UI tests.

## Web Interface Guidelines Review (`file:line`)

Refreshed `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` before review and audited all changed sections of `src/api/src/zava_forward/api/web/app.js` (`lines 64-67`, `433-463`, `887-888`, `1974-2331`), applying repository UX overrides where mandated (`docs/reference/research/ux/content-standard.md`, `design-system.md`, and `.github/copilot-instructions.md` mandate sentence case and plain ASCII punctuation rather than Unicode ellipses/curly quotes or Title Case):

```text
## src/api/src/zava_forward/api/web/app.js

✓ pass (accessibility: semantic <h1>-><h2>-><h3>-><h4>, <table/caption/th scope>, <label for>, aria-describedby, aria-invalid, role="status"/aria-live="polite", role="alert"; focus: native Fluent 2 :focus-visible preserved and first invalid control focused on submit; forms: autocomplete="off", meaningful name attributes, disabled + aria-busy submit state, inline error with owner and next action; navigation: <a href> links and URL query sync #/exceptions?kind=&status=; i18n: Intl.DateTimeFormat("en-GB") and <code translate="no"> on identifiers)
```

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Connect standalone importer process rejected-batch storage directly to the shared database without manual refusal-ledger transfer once importer storage topology is unified | Importer runs as a separate CLI/storage pipeline outside `#135`'s core/API/workbench exception queue scope; `ExceptionRegisterMixin` already supports both `import_batches` and `import_exceptions.rejected_batches`. | Owner: data engineering / programme support | Open distinct follow-up item; preserved outside active `P01`–`P03` acceptance scope. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Unsaved recovery reason text is tracked on the form element without a global router `beforeunload` prompt

* Related scope: `P02-T01`
* Evidence: `src/api/src/zava_forward/api/web/app.js` sets `form.dataset.unsaved = "true"` when `reasonInput` contains text and clears it on submit, while the workbench SPA does not attach a global `beforeunload` or `hashchange` confirmation guard for `[data-unsaved="true"]` forms.
* Impact: Non-blocking UX polish item; does not affect any Issue #135 acceptance criterion, WCAG 2.2 AA conformance, or controlled recovery safety guarantees.
* Destination: follow-up
* Smallest useful next action: Optionally wire a shared `[data-unsaved="true"]` `beforeunload` / route-change warning across workbench forms in a separate UX polish task if desired by UX owners.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | follow-up | Employee workbench UX follow-up: wire shared `[data-unsaved="true"]` navigation guard if desired | Non-blocking residual UX enhancement outside Issue #135 acceptance criteria |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Standalone importer rejected-batch storage unification (plan `## Follow-Up Items`; owner: data engineering / programme support).
* Optional shared `[data-unsaved="true"]` navigation warning across employee workbench forms (`RV-001`; owner: employee workbench UX).

## Blockers and Remaining Work

* Blockers: none (`workbench_browser_check.py`, `scenario-manifest.json`, `workbench.py`, `role-screens.js`, and `sqlstore.py` verified untouched; human PR review and hosted CI remain standard post-push pull-request gates outside this local-commit workflow).
* Remaining active work: none

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python -m mypy` | `src/core` | Passed | `Success: no issues found in 316 source files` |
| `python -m ruff check . && python -m ruff format --check .` | `src/core` | Passed | `All checks passed!`, `263 files already formatted` |
| `PYTHONPATH=tests python -m unittest discover -s tests -p 'test_*exception*.py' -q` | `src/core/tests` | Passed | `Ran 29 tests in 0.006s — OK` |
| `python -m mypy` | `src/api` | Passed | `Success: no issues found in 284 source files` |
| `python -m ruff check . && python -m ruff format --check .` | `src/api` | Passed | `All checks passed!`, `200 files already formatted` |
| `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest ... -q` (15 focused suites) | `src/api/tests` | Passed | `Ran 231 tests in 115.091s — OK (skipped=4)` covering `test_exception_register`, `test_exception_queue_ui`, `test_exception_register_screen`, `test_data_operator_screen`, `test_data_steward_screen_wcag`, `test_role_screens`, `test_role_endpoint_inventory`, `test_handoff_waiting_view`, `test_case_journey`, `test_epic149_role_workbench_heading_hierarchy`, `test_content_standard`, `test_design_system`, `test_app_js_notices_content`, `test_static_assets`, `test_workspace_scripts` |
| Web Interface Guidelines review (`web_fetch` + `file:line` audit) | `src/api/src/zava_forward/api/web/app.js` | Passed | `✓ pass` across accessibility, focus, forms, navigation, and locale/i18n rules; `RV-001` noted as optional non-blocking follow-up |
| Hosted GitHub Actions CI | branch `feat/ux-135-exception-queue-2330` | Skipped | User instruction explicitly forbade pushing (`Do NOT push`); hosted CI remains to run when the branch is pushed for PR review. |

## Outcome

* Outcome: Conformant
* Outcome rationale: All planned phases (`P01`, `P02`, `P03`) completed cleanly, all five Issue #135 acceptance criteria (`AC-1`..`AC-5`) and Focused-tier checks (`AC-6`, `NFR-1`..`NFR-3`) are deterministically enforced and verified end-to-end across `src/core`, `src/api`, and `web/app.js`, all plan-critique findings (`PC-001`..`PC-006`) are resolved, and zero defects or material decision/evidence gaps remain.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | 1. Data engineering / programme support: unify standalone importer rejected-batch persistence with shared DB. 2. Employee workbench UX (`RV-001`): optional shared `[data-unsaved="true"]` navigation guard. |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier Passed (`src/core` `mypy`/`ruff`/`29` unit tests; `src/api` `mypy`/`ruff`/`231` unit, SQL/JSON, HTTP, Node-VM UI, WCAG, design-system, and lexical copy-standard tests; Web Interface Guidelines `file:line` audit Passed; hosted CI Skipped per explicit `Do NOT push` instruction)
* Blockers: none
