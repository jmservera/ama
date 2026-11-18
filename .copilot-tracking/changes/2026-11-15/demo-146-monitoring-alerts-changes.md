<!-- markdownlint-disable-file -->
# RPI Changes: Monitoring Alerts, Workbook, Runbooks, and Task/Release Harm Declarations (Issue #146)

## Metadata

* Task ID: issue-146
* Related plan: .copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P02-T03`, `P03`, `P03-T01`
* All remaining active-plan markers: None
* Status basis: All planned infrastructure alert/workbook/runbook updates (`P01`), 13-task and serving-release harm-monitoring declaration contracts and live human-approval guards (`P02`), and Focused tier validation suites (`P03`) completed and passed with zero temporary files remaining.

## Execution Summary

Full plan (`P01`, `P02`, `P03`) is complete. Ranking archive job failure alerts route to `#job-rank` across `operationalMonitoring.bicep`, `monitoring-runbooks.md`, `monitoring-workbook.json`, and `monitoring_coverage.ALERTS`; all 13 registered AI tasks and serving release contracts (`ai_registry`, `rai_release`, `assistant_release`, `assistants`) declare and enforce the 6 harm/quality/disparity/review-burden indicators (including complete 4-stage `review_effort` with `approval_rate_is_safety=False` and named-human non-fictional live threshold approval); and Focused validation passed across `infra/tests` (`598` tests), `src/core/tests` (`3,569` tests including `iothub` extra), `src/api/tests/test_assistant_release.py` (`65` tests), `mypy` (`342` files), and `ruff` check/format.

## Completed Work

Use a descriptive subheading for each completed-work item. Do not assign a per-entry formal ID.

### Ranking Archive Job Alert Routing, Runbook Section, and Workbook Boundary Clarification

* Related phase or task: `P01-T01`
* Files: `infra/modules/operationalMonitoring.bicep`, `infra/monitoring-runbooks.md`, `infra/monitoring-workbook.json`, `src/core/src/zava_forward/core/monitoring_coverage.py`
* What changed and why: Added `endsWith(jobName, '-rank') || endsWith(jobName, '-rank-publish') ? 'job-rank'` before `'job-auth'` in `operationalMonitoring.bicep` so ranking archive jobs do not silently misroute to `#job-auth`; added `### Job rank` (`#job-rank`) under `## New Disabled Job Candidates` and updated declaration/evidence rows in `monitoring-runbooks.md`; updated `status-and-boundary` and `ai-usage-and-harm` text in `monitoring-workbook.json`; added `job-rank` (`CANDIDATE`) to `monitoring_coverage.ALERTS`.
* Completion evidence: Compiled ARM output from `az bicep build --file infra/modules/operationalMonitoring.bicep --stdout` contains `'-rank'`, `'-rank-publish'`, and `'job-rank'` ahead of `'job-auth'`, and `#job-rank` resolves in `monitoring-runbooks.md`.
* Validation: Passed (`42` tests in `#146` `infra/tests/` suites; `598` tests in full `infra/tests`).

### Infrastructure Alert/Runbook Matrix Regression Tests and 100-Column Ruff Hygiene

* Related phase or task: `P01-T02`
* Files: `infra/tests/test_monitoring_alerts.py`, `infra/tests/test_alert_runbook_signal_matrix.py`, `infra/tests/test_ai_alert_runbook_ownership.py`, `infra/tests/test_monitoring_workbook.py`, `infra/tests/test_monitoring_workbook_sla_budget.py`, `infra/tests/test_ai_observability_workbook_budget.py`, `infra/tests/test_diagnostic_log_privacy.py`
* What changed and why: Added `test_ranking_archive_job_failure_alert_routes_to_job_rank_runbook` in `test_monitoring_alerts.py`, added `job-rank` to `MATRIX` and `test_poison_ledger_job_and_iot_signals_are_covered` in `test_alert_runbook_signal_matrix.py`, added `job-rank` and `strict=False` on `zip()` in `test_ai_alert_runbook_ownership.py`, and aligned all 7 `#146` `infra/tests/` monitoring suites with 100-column `ruff` formatting and lint rules.
* Completion evidence: `ruff format --isolated --line-length 100 --check` (`7 files already formatted`), `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` (`All checks passed!`), and `python3 -m unittest` (`Ran 42 tests — OK`).
* Validation: Passed.

### Canonical 13-Task Harm Monitoring Declarations, Complete Review Effort, and Live Human Threshold Guards

* Related phase or task: `P02-T01`
* Files: `src/core/src/zava_forward/core/monitoring_coverage.py`
* What changed and why: Added `FICTIONAL_APPROVER_TOKENS` and `_named_human_approver` wired into `evaluate_indicator` and `evaluate_ai_limits`; added `REVIEW_EFFORT_STAGES` (`preparation`, `review`, `correction`, `re_review`), `INDICATOR_CATEGORIES`, `live: bool = False` enforcement on `check_monitoring_declaration`, and sequence-safe `effort_stages` + `approval_rate_is_safety is False` validation; defined `TASK_DECLARATION_SPECS`, `task_declaration(task_id)`, and `task_declarations()` for all 13 registered AI tasks (with `stale_review_attempts` explicitly marked `applicable: False` with rationale on stateless `chat-case-conversation`, and `manual_route_status` recorded across enabled and disabled tasks).
* Completion evidence: `task_declarations()` produces `status == "declared"` (`offline_only=True`) offline and `status == "blocked"` when `live=True` across all 13 registered AI tasks.
* Validation: Passed (`mypy` strict across `342` files, `ruff`, and `DeclarationTests`).

### Task Registration and Serving-Release Monitoring Contract Enforcement

* Related phase or task: `P02-T02`
* Files: `src/core/src/zava_forward/core/ai_registry.py`, `src/core/src/zava_forward/core/rai_release.py`, `src/core/src/zava_forward/core/assistant_release.py`, `src/core/src/zava_forward/core/assistants.py`, `src/core/tests/release_support.py`
* What changed and why: Attached `monitoring_declaration` to every registered task in `ai_registry._entry` and validated completeness in `ai_registry.missing_fields` without changing `REGISTRY_VERSION`; added cycle-safe `rai_release.valid_monitoring_declaration(value, task)` enforced in `rai_release.missing_contract` (preventing missing or weakened indicator applicability/review-effort stages) and enforced named-human live threshold approval in `rai_release.missing_binding` when `live and "monitoring_declaration" in record`; persisted `monitoring_declaration` in `assistant_release.record`; exposed `monitoring_status` in both disabled and enabled branches of `Assistants.registry`; updated `release_support.fixture` to supply constructed offline thresholds by default and named-human test approval when `cls == "actual"`.
* Completion evidence: `test_heldout_eval.py` (`17` tests), `test_rai_release.py` (`9` tests), and `src/api/tests/test_assistant_release.py` (`65` tests) pass without touching frozen digests.
* Validation: Passed.

### Focused Harm-Declaration and Live-Approval Unit Tests

* Related phase or task: `P02-T03`
* Files: `src/core/tests/test_monitoring_coverage.py`, `src/core/tests/test_ai_register_completeness.py`, `src/core/tests/test_rai_release.py`, `src/core/tests/test_rai_threshold_live_approval_guard.py`, `src/api/tests/test_assistant_release.py`
* What changed and why: Added focused tests verifying all 13 task declarations, 4-stage `review_effort` and `approval_rate_is_safety=False` rejection on partial stages or `True`, bot/fictional approver rejection (`system`, `Copilot Agent`, `release-bot`, `Data lead (fictional)`, `DPO placeholder`, `Mock RAI Owner`, `TBD`, `Fixture Approver`), `ai_registry` registration rejection on missing `monitoring_declaration`, release contract enforcement and live constructed-threshold denial in `test_rai_release.py` and `src/api/tests/test_assistant_release.py`, and weakened applicability rejection in `test_rai_threshold_live_approval_guard.py`.
* Completion evidence: All targeted and full unit test suites pass with `7` focused new test methods added (`<= 14` bound respected) and `0` removals.
* Validation: Passed.

### Focused Tier Full-Suite Execution and Temporary Venv Cleanup

* Related phase or task: `P03-T01`
* Files: `.copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md`, `.copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md`, `.copilot-tracking/changes/2026-11-15/demo-146-monitoring-alerts-changes.md`
* What changed and why: Installed editable `src/core[iothub]`, `src/agents`, `src/api`, `src/orchestrator`, and `src/importer` distributions into temporary workspace-local `.venv-146-tmp`, ran all Focused validation suites, removed `.venv-146-tmp`, and verified `git status --short` contains only intended repository and `.copilot-tracking/` artifacts.
* Completion evidence: Zero failures across all test, lint, format, and `mypy` runs; `.venv-146-tmp` deleted cleanly.
* Validation: Passed.

## Implementation-Time Plan and Detail Updates

* Classification: Immediately relevant current-state update
  * Discovery: `src/api/tests/test_assistant_release.py` (`test_live_provider_needs_actual_release_with_serving_proof` and `test_contract_fields_required_on_authenticated_record_route`) mutated a `constructed-fixture` release dict to `evidence_class="actual"` directly and enumerated required authenticated record route contract fields without `monitoring_declaration`.
  * Plan and detail updates: Added `src/api/tests/test_assistant_release.py` to `Test Ownership` and `P02-T03` in `.copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md` and `.copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md`, asserting first that `evidence_class="actual"` with constructed thresholds is denied with `"named-human approved live monitoring thresholds"` before admitting `release_support.fixture(..., cls="actual")`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `unittest discover -s infra/tests` | Full `infra/tests` suite (including Bicep compilation, alert/runbook signal matrix, workbook SLA/budget/privacy) | Passed | `Ran 598 tests in 227.927s — OK (skipped=4)` |
| `unittest discover -s src/core/tests` | Full `src/core` unit suite (`3,530` base + `39` `test_device_registry_azure` with `src/core[iothub]`) | Passed | `3,569` total tests passed (`0` failures, `0` errors after `src/core[iothub]` editable install) |
| `unittest discover -s src/api/tests -p 'test_assistant_release.py'` | Serving release record and live admission route tests | Passed | `Ran 65 tests in 106.901s — OK (skipped=7)` (`ZF_TEST_MSSQL=1` disposable SQL Server tests skipped in Focused tier) |
| `ruff format --check . && ruff check .` (`src/core` + `src/api/tests/test_assistant_release.py`) | Core library/tests (`289` files) and updated API release test | Passed | `289 files already formatted`, `All checks passed!` |
| `ruff check` & `ruff format --isolated --line-length 100 --check` (`infra/tests` `#146` suites) | All `7` `#146` monitoring/privacy test modules in `infra/tests/` | Passed | `All checks passed!`, `7 files already formatted` |
| `mypy` (`src/core`) | Strict type checking across `src/core` (`src` + `tests`) | Passed | `Success: no issues found in 342 source files` |
| `tools/rpi-checks.py` | Full local gate script | Skipped | Explicitly excluded by caller instruction (`Validation Tier: Focused`; do NOT run `tools/rpi-checks.py`) |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P02`, `P03` and all `P01-T01`..`P03-T01` markers checked `[x]`; `src/api/tests/test_assistant_release.py` recorded in plan and details)
* Completed-work evidence and handoff prose: Reconciled
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining active-plan markers)
* Review readiness: Ready for `rpi-review`

## Blockers

* None.

## Remaining Work

* None in active `rpi-implement` scope; proceeding to single-pass `rpi-review` and local git commit (`Refs #146`, no push).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md, `## Follow-Up Items`
* Appoint named human operational and RAI owners (`OD-51`, `OQ-017`, `OQ-018`) and execute live Log Analytics table/field signal drills before enabling disabled candidate alerts in `operationalMonitoring.bicep`.
* Connect an approved Azure Cost Management billing export before replacing `Unknown` / `Unreconciled` Azure cost columns in `infra/monitoring-workbook.json`.
* Add an `import-jobs-poison` queue producer and corresponding scheduled-query alert only if `src/importer/` moves from `quarantine`-only row isolation to queue dead-lettering.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P02-T03`, `P03`, `P03-T01` all completed)
* Validation coverage: Focused tier passed (`infra/tests` `598` tests, `src/core/tests` `3,569` tests, `src/api/tests/test_assistant_release.py` `65` tests, `ruff`, `mypy`)
* Blockers: None
* Current plan and detail updates: Recorded immediately-relevant fixture update in `src/api/tests/test_assistant_release.py`
* Planning and critique state: Ready (`PC-001`..`PC-004` resolved)
* Follow-up items: Mirrored from canonical plan
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
