<!-- markdownlint-disable-file -->
# RPI Phase Details: Monitoring Alerts, Workbook, Runbooks, and Task/Release Harm Declarations (Issue #146)

## Metadata

* Task ID: issue-146
* Task slug: demo-146-monitoring-alerts
* Related plan: .copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/demo-146-monitoring-alerts-research.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/adrs/0001-azure-architecture.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Bicep Alert Parity, Workbook Boundary Accuracy, and Runbook Alignment | Ready | P01, P01-T01, P01-T02 |
| P02 | Task and Serving-Release Harm/Quality/Disparity/Review-Burden Declarations | Ready | P02, P02-T01, P02-T02, P02-T03 |
| P03 | Focused Tier Validation and Local Commit Closeout | Ready | P03, P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Bicep Alert Parity, Workbook Boundary Accuracy, and Runbook Alignment

### Context

`infra/main.bicep` wires `modules/monitoring.bicep` (Log Analytics, Application Insights, AMPLS, private endpoint, and `ag-{prefix}-ops`), installed core/ledger alerts (`foundry-throttle`, `sql-cpu`, `api-5xx`, `api-restarts`, `ledger-digest-mismatch`, `ledger-verify-missing`), `budget-{prefix}` (`80%` actual, `100%` forecast), and `modules/operationalMonitoring.bicep` (disabled candidate rules for `jobFailures`, `iotFailureAlerts`, `agentTasksPoison`, `aiLimitBreach`, plus `monitoring-workbook.json`). When `enableRankingArchiveBlob=true`, `main.bicep` appends `job-{prefix}-rank` / `job-{prefix}-rank-publish` to `jobNames`, but `operationalMonitoring.bicep` lacks a `-rank` / `-rank-publish` branch and misroutes the alert description to `#job-auth`. `infra/monitoring-runbooks.md` and `monitoring_coverage.ALERTS` also omit `job-rank`, and `infra/monitoring-workbook.json` (`status-and-boundary`) still states that no poison-queue or AI-limit candidate alert exists.

### Intent

Restore 1:1 parity across Bicep alert candidates, `infra/monitoring-runbooks.md`, `infra/monitoring-workbook.json`, `monitoring_coverage.ALERTS`, and `infra/tests` signal/ownership suites without changing existing `operationalMonitoring.bicep` parameter names, IoT metric tuples, or disabled-by-default candidate guards.

### Boundaries

* Included: `infra/modules/operationalMonitoring.bicep`, `infra/monitoring-runbooks.md`, `infra/monitoring-workbook.json`, `monitoring_coverage.ALERTS` entry for `job-rank`, and `#146` monitoring tests under `infra/tests/`.
* Excluded: Enabling candidate alerts by default, adding an `import-jobs-poison` rule without a producer, changing `infra/modules/monitoring.bicep` or `infra/main.bicep` resource topology, or reformatting unrelated scripts under `infra/scripts/`.

### Likely Targets

* `infra/modules/operationalMonitoring.bicep`: Add `-rank` / `-rank-publish` -> `'job-rank'` mapping in `jobFailures` description.
* `infra/monitoring-runbooks.md`: Add `### Job rank` (`#job-rank`) under `## New Disabled Job Candidates` and update Issue `#146` task-declaration status notes.
* `infra/monitoring-workbook.json`: Refresh stale candidate-alert sentence in `status-and-boundary` while retaining `"provisional"`, `"not an SLA"`, and `"no availability test"` markers.
* `src/core/src/zava_forward/core/monitoring_coverage.py`: Add `job-rank` (`CANDIDATE`) to `ALERTS`.
* `infra/tests/test_monitoring_alerts.py`, `infra/tests/test_alert_runbook_signal_matrix.py`, `infra/tests/test_ai_alert_runbook_ownership.py`, `infra/tests/test_monitoring_workbook.py`, `infra/tests/test_monitoring_workbook_sla_budget.py`, `infra/tests/test_ai_observability_workbook_budget.py`: Extend assertions for `job-rank` and ensure clean `--line-length 100` isolated `ruff` check/format.

### Dependencies

* None.

### Validation Expectations

* `python -m unittest discover -s infra/tests -v` passes all compiled Bicep, workbook, and signal-matrix tests.
* `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` and `ruff format --isolated --line-length 100 --check` pass on all `#146` monitoring test files in `infra/tests/`.

### Completion Evidence

* Compiled ARM output from `main.bicep` (`enableRankingArchiveBlob=true`) emits `alert-job-forward-dev-rank-publish-failed` (and demo `alert-job-fdev-rank-failed`) referencing `#job-rank`, verified by unit tests.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Route ranking publication job failures to `#job-rank` and update runbook, workbook, and alert register

#### Context

`operationalMonitoring.bicep` maps job suffixes via a chained ternary expression (`-orch`/`-orchestrator`, `-audit`/`-ledger-verify`, `-load`/`-import`, else `'job-auth'`). Adding `endsWith(jobName, '-rank') || endsWith(jobName, '-rank-publish') ? 'job-rank'` before `'job-auth'` routes ranking publication job failures to `#job-rank`. `infra/monitoring-runbooks.md` requires a matching `### Job rank` section with signal, proposed owner (`Digital service owner, with Data and Performance Lead`), response, and recovery.

#### Intent

Ensure every job passed in `main.bicep` `jobNames` resolves to an accurate, dedicated runbook section and `monitoring_coverage.ALERTS` entry, and ensure `monitoring-workbook.json` `status-and-boundary` matches current candidate rules.

#### Boundaries

* Included: `infra/modules/operationalMonitoring.bicep`, `infra/monitoring-runbooks.md`, `infra/monitoring-workbook.json`, and `ALERTS` in `src/core/src/zava_forward/core/monitoring_coverage.py`.
* Excluded: Changing alert enablement defaults or workbook KQL projections.

#### Likely Targets

* `infra/modules/operationalMonitoring.bicep`: `jobFailures` description expression.
* `infra/monitoring-runbooks.md`: `## New Disabled Job Candidates` (`### Job rank`) and `## Issue 146 Remaining Gaps` / `## Status Summary Against Issue 146`.
* `infra/monitoring-workbook.json`: `status-and-boundary` markdown item.
* `src/core/src/zava_forward/core/monitoring_coverage.py`: `ALERTS` tuple.

#### Dependencies

* None.

#### Validation Expectations

* `az bicep build --file infra/main.bicep --stdout` and `az bicep build --file infra/modules/operationalMonitoring.bicep --stdout` succeed with zero warnings or errors.

#### Completion Evidence

* `#job-rank` exists in `operationalMonitoring.bicep`, `monitoring-runbooks.md`, and `monitoring_coverage.ALERTS`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Update `infra/tests` alert/runbook matrices and align `--line-length 100` `ruff` formatting on `#146` monitoring tests

#### Context

`infra/tests/test_alert_runbook_signal_matrix.py` (`MATRIX["alert-${jobName}-failed"]`) and `infra/tests/test_ai_alert_runbook_ownership.py` enumerate expected job anchors (`job-orchestrator`, `job-ledger`, `job-import`, `job-auth`). Additionally, four `#146` monitoring test files in `infra/tests/` were previously formatted at 88 columns instead of `--line-length 100`, and `test_ai_alert_runbook_ownership.py` lacks `strict=False` on `zip()`.

#### Intent

Lock `job-rank` in the Bicep compilation, signal-matrix, and ownership tests, and clear `ruff` check/format issues across `#146` `infra/tests/` monitoring files.

#### Boundaries

* Included: `infra/tests/test_monitoring_alerts.py`, `infra/tests/test_alert_runbook_signal_matrix.py`, `infra/tests/test_ai_alert_runbook_ownership.py`, `infra/tests/test_monitoring_workbook.py`, `infra/tests/test_monitoring_workbook_sla_budget.py`, `infra/tests/test_ai_observability_workbook_budget.py`, `infra/tests/test_diagnostic_log_privacy.py`.
* Excluded: Unrelated `infra/scripts/` files.

#### Likely Targets

* `infra/tests/test_monitoring_alerts.py`: Add assertion evaluating `operationalMonitoring` `jobNames` and `jobFailures` descriptions with `enableRankingArchiveBlob=True` (both normal `-rank-publish` and `demoDirectIngress` `-rank`).
* `infra/tests/test_alert_runbook_signal_matrix.py`: Include `job-rank` in `MATRIX["alert-${jobName}-failed"]` and in `test_poison_ledger_job_and_iot_signals_are_covered`.
* `infra/tests/test_ai_alert_runbook_ownership.py`: Include `job-rank` in job candidate anchor check and add `strict=False` to `zip()`.
* `infra/tests/test_monitoring_workbook.py`, `infra/tests/test_monitoring_workbook_sla_budget.py`, `infra/tests/test_ai_observability_workbook_budget.py`, `infra/tests/test_diagnostic_log_privacy.py`: `ruff format --isolated --line-length 100` alignment.

#### Dependencies

* P01-T01.

#### Validation Expectations

* All `infra/tests` pass and isolated `ruff check` + `ruff format --isolated --line-length 100 --check` pass on those files.

#### Completion Evidence

* Passing unittest and `ruff` command outputs recorded in `.copilot-tracking/changes/2026-11-15/demo-146-monitoring-alerts-changes.md`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Task and Serving-Release Harm/Quality/Disparity/Review-Burden Declarations

### Context

Issue `#146` and PRD `AC-029` / `AC-070` require each task and serving release to declare applicable harm, quality, disparity, and review-burden indicators (`unsupported_claims`, `critical_misses`, `stale_review_attempts`, `challenges`, `cohort_errors`, and complete `review_effort` covering preparation, review, correction, and re-review without using approval rate as safety), denominators, observation windows, offline-constructed vs named-human live thresholds, accountable monitoring/incident owners, and response. Currently `monitoring_coverage.check_monitoring_declaration` is unwired, no task in `ai_registry.tasks()` records a declaration, and `evaluate_indicator` / `evaluate_ai_limits` accept non-human strings such as `"system"` or `"Copilot Agent"` via `rai_release.named()`.

### Intent

Provide canonical, truthful harm-monitoring declarations for all 13 registered AI tasks, enforce declaration completeness on task registration and serving release contracts, and enforce named-human non-fictional approval on live monitoring thresholds while preserving offline constructed-fixture tests and frozen evaluation digests.

### Boundaries

* Included: `src/core/src/zava_forward/core/monitoring_coverage.py`, `ai_registry.py`, `rai_release.py`, `assistant_release.py`, `assistants.py`, `src/core/tests/release_support.py`, and focused tests in `src/core/tests/`.
* Excluded: Inventing fake employee appointments as real Zava North Homes live sign-off (`OD-51`), modifying `ai_registry.REGISTRY_VERSION` or `assistants.VERSION`, or breaking `LiveReleaseApprover`'s direct `rai_release.missing_binding` unit test.

### Likely Targets

* `src/core/src/zava_forward/core/monitoring_coverage.py`: Add `_named_human_approver`, `REVIEW_EFFORT_STAGES`, `live` check support on `check_monitoring_declaration`, `review_effort` completeness checks, and `task_declaration(task_id)` / `task_declarations()`.
* `src/core/src/zava_forward/core/ai_registry.py`: Include `monitoring_declaration` on every `_entry(...)` and validate it in `missing_fields(entry)`.
* `src/core/src/zava_forward/core/rai_release.py`: Validate `monitoring_declaration` completeness in `missing_contract(record, task)` and live threshold approval in `missing_binding(record, ...)` when `live=True` and `monitoring_declaration` is present.
* `src/core/src/zava_forward/core/assistant_release.py` and `assistants.py`: Persist `monitoring_declaration` in `assistant_release.record` and surface `monitoring_status` in both disabled and enabled branches of `Assistants.registry`.
* `src/core/tests/release_support.py` and `src/core/tests/test_rai_release.py`: Populate `monitoring_declaration` in `fixture()` and `ReleaseContract` (`constructed=True` for offline fixtures; named-human test approval when `cls == "actual"`).
* `src/core/tests/test_monitoring_coverage.py`, `test_ai_register_completeness.py`, `test_rai_release.py`, `test_rai_threshold_live_approval_guard.py`: Add focused semantic and edge-case tests.

### Dependencies

* P01-T01.

### Validation Expectations

* `cd src/core && python -m unittest discover -s tests -v`, `ruff check . && ruff format --check .`, and `mypy` pass; `src/api/tests/test_assistant_release.py` also passes.

### Completion Evidence

* All 13 registered tasks and serving releases carry validated `monitoring_declaration` objects, offline fixtures pass, and unapproved/constructed/bot-attributed live thresholds fail closed.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add canonical 13-task harm declarations, complete review-effort validation, and named-human live threshold guards in `monitoring_coverage.py`

#### Context

`monitoring_coverage.HARM_INDICATORS` already defines the 6 canonical keys: `unsupported_claims`, `critical_misses`, `stale_review_attempts`, `challenges`, `cohort_errors`, and `review_effort`. To satisfy complete review effort and live named-human approval without breaking existing `DeclarationTests` in `test_monitoring_coverage.py`:
1. Add `_named_human_approver(value: object) -> bool` using `rai_release.named_human(value)` plus token-level rejection of fictional/placeholder tokens (`fictional`, `placeholder`, `mock`, `synthetic`, `example`, `todo`, `tbd`, `unapproved`, `unknown`). Existing test fixtures `"Named Assurance Lead"` and `"Finance budget owner"` remain valid, while `"system"`, `"Copilot Agent"`, `"release-bot"`, `"TBD"`, and `"DPO placeholder"` are rejected.
2. Update `evaluate_indicator` and `evaluate_ai_limits` to check `_named_human_approver(threshold.get("approved_by"))` when `not constructed`.
3. Extend `check_monitoring_declaration(declaration, *, task_enabled=True, live=False)`:
   * Preserve existing schema keys (`DECLARED = "declared"`, `BLOCKED = "blocked"`, `reason` for `applicable: False`, positive integer `denominator`, `window`, `manual_route_status`, and colon-delimited `indicator:<name>:...` missing tokens) so existing minimal offline dicts in `DeclarationTests` remain 100% compatible.
   * When `effort_stages` is provided on `review_effort`, require a non-string sequence where `tuple(effort_stages) == ("preparation", "review", "correction", "re_review")` (reporting `"indicator:review_effort:effort_stages"` otherwise, and supporting JSON `list` round-trips); when `approval_rate_is_safety` is provided on `review_effort`, require it to be strictly `False` (reporting `"indicator:review_effort:approval_rate_is_safety"` otherwise).
   * Because `evaluate_indicator` now checks `_named_human_approver(threshold.get("approved_by"))` when `not constructed`, unapproved or bot/fictional-attributed live thresholds automatically report `"indicator:<name>:threshold"`.
   * When `live=True`, also report `"indicator:<name>:threshold"` whenever an applicable indicator's threshold has `constructed=True` (so constructed thresholds pass offline tests only and block live admission).
4. Provide `task_declaration(task_id: str) -> dict[str, Any]` and `task_declarations() -> dict[str, dict[str, Any]]` covering all 13 task IDs (`5` assistants, `6` retained legacy tasks, `chat-case-conversation`, `aftercare-concern-pack`), declaring indicator `category` (`harm`, `quality`, `disparity`, `review_burden`), `applicable` (`False` with explicit `reason` for `stale_review_attempts` on stateless `chat-case-conversation`; `True` elsewhere), positive integer `denominator` (e.g. `20` or `50`) plus `denominator_unit` string, `window` (`"P7D"` or `"P28D"`), `threshold` (`{"limit": <float>, "min_sample": <int>, "constructed": True}`), `effort_stages: ["preparation", "review", "correction", "re_review"]` and `approval_rate_is_safety: False` on `review_effort`, role-level `monitoring_owner` and `incident_owner` (noting live appointment pending `OD-51`), `response`, and `manual_route_status`.

#### Intent

Centralize pure, strictly typed harm-monitoring declarations and live threshold approval validation in `monitoring_coverage.py`.

#### Boundaries

* Included: `src/core/src/zava_forward/core/monitoring_coverage.py`.
* Excluded: I/O, store access, or live authority claims.

#### Likely Targets

* `src/core/src/zava_forward/core/monitoring_coverage.py`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Passes `mypy` (`strict = true`), `ruff check`, and `ruff format --check` in `src/core`.

#### Completion Evidence

* `task_declarations()` returns valid `declared` offline declarations (`live=False`) and `blocked` live declarations (`live=True`) for all 13 registered tasks.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Enforce `monitoring_declaration` on task registration and serving release contracts (`ai_registry`, `rai_release`, `assistant_release`, `assistants`, `release_support`)

#### Context

Registering declarations in `monitoring_coverage.py` alone is insufficient unless `ai_registry`, `rai_release`, and `assistant_release` bind and enforce them without creating circular imports (`monitoring_coverage` imports `rai_release` at module top level):
* `ai_registry._entry(...)` attaches `"monitoring_declaration": monitoring_coverage.task_declaration(id)` to every registered task without changing `REGISTRY_VERSION`. `ai_registry.missing_fields(entry)` appends `"monitoring_declaration"` when `monitoring_coverage.check_monitoring_declaration(entry.get("monitoring_declaration"), task_enabled=bool(entry.get("enabled", True)))["missing"]` is non-empty.
* `rai_release.missing_contract(record, task)` uses a lazy function-local `from . import monitoring_coverage` import to validate `record.get("monitoring_declaration")` via `monitoring_coverage.check_monitoring_declaration(..., task_enabled=bool(task.get("enabled", True)), live=False)` and ensures the declared applicable indicators cover every applicable indicator in `task.get("monitoring_declaration")` (plus requiring `effort_stages` and `approval_rate_is_safety is False` on `review_effort` when `task` declares them), appending `"monitoring_declaration"` to `missing` when invalid or weakened.
* `rai_release.missing_binding(record, binding, bound, now, live=False)`: when `live and "monitoring_declaration" in record`, uses a lazy `from . import monitoring_coverage` import to check `monitoring_coverage.check_monitoring_declaration(record.get("monitoring_declaration"), task_enabled=True, live=True)["missing"]` and appends `"named-human approved live monitoring thresholds"` if non-empty (preserving `LiveReleaseApprover`'s 4-key direct unit test where `"monitoring_declaration"` is omitted).
* `assistant_release.record(...)` copies `"monitoring_declaration"` from `body` (before `rai_release.missing_contract(rec, spec)` validates it).
* `Assistants.registry(...)` attaches `"monitoring_status"` from `monitoring_coverage.check_monitoring_declaration(...)` in BOTH `registered.append(...)` branches: `(spec["monitoring_declaration"], task_enabled=False, live=False)` on the disabled `spec.get("enabled") is False` branch, and `((selected or spec).get("monitoring_declaration"), task_enabled=True, live=live)` on the enabled branch.
* `src/core/tests/release_support.py:fixture(...)` attaches `copy.deepcopy(spec["monitoring_declaration"])`, upgrading applicable thresholds to `constructed=False, approved_by="Amina Okafor, RAI Assurance Lead"` only when `cls == "actual"`.

#### Intent

Wire fail-closed task and serving-release harm-monitoring enforcement end to end without breaking frozen held-out evaluation manifests or existing release admission tests.

#### Boundaries

* Included: `src/core/src/zava_forward/core/ai_registry.py`, `rai_release.py`, `assistant_release.py`, `assistants.py`, `src/core/tests/release_support.py`.
* Excluded: Changing `ai_registry.REGISTRY_VERSION` or `assistants.VERSION`.

#### Likely Targets

* `src/core/src/zava_forward/core/ai_registry.py`
* `src/core/src/zava_forward/core/rai_release.py`
* `src/core/src/zava_forward/core/assistant_release.py`
* `src/core/src/zava_forward/core/assistants.py`
* `src/core/tests/release_support.py`

#### Dependencies

* P02-T01.

#### Validation Expectations

* `src/core/tests/test_rai_release_invalidation.py`, `src/core/tests/test_heldout_eval.py`, and `src/api/tests/test_assistant_release.py` pass without regressions.

#### Completion Evidence

* Missing, incomplete, weakened, or unapproved-live `monitoring_declaration` blocks release recording/admission cleanly.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T03 -->
### P02-T03: Add focused unit tests for task/release harm declarations and live threshold approval guards

#### Context

Focused tests must fail without P02-T01/P02-T02 and cover edge cases: all 13 registered tasks, complete 4-stage `review_effort` (`approval_rate_is_safety=False`), `chat-case-conversation` non-applicable `stale_review_attempts` rationale, disabled `aftercare-concern-pack` manual route, serving-release rejection of missing/weakened `monitoring_declaration`, offline acceptance vs live rejection of constructed thresholds, and rejection of system/agent/bot/fictional threshold approvers.

#### Intent

Lock the task and serving-release harm-monitoring declaration invariants with concise unit tests in existing test modules.

#### Boundaries

* Included: `src/core/tests/test_monitoring_coverage.py`, `src/core/tests/test_ai_register_completeness.py`, `src/core/tests/test_rai_release.py`, `src/core/tests/test_rai_threshold_live_approval_guard.py`, and `src/api/tests/test_assistant_release.py`.
* Excluded: Adding redundant test files or modifying unrelated suites.

#### Likely Targets

* `src/core/tests/test_monitoring_coverage.py`
* `src/core/tests/test_ai_register_completeness.py`
* `src/core/tests/test_rai_release.py`
* `src/core/tests/test_rai_threshold_live_approval_guard.py`
* `src/api/tests/test_assistant_release.py`

#### Dependencies

* P02-T01, P02-T02.

#### Validation Expectations

* `cd src/core && python -m unittest discover -s tests -v`, `ruff check . && ruff format --check .`, and `mypy` pass with exit code `0`.

#### Completion Evidence

* Passing unit test execution output recorded in `.copilot-tracking/changes/2026-11-15/demo-146-monitoring-alerts-changes.md`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Tier Validation and Local Commit Closeout

### Context

The caller specified the Focused validation tier (`infra/tests`, `src/core` unit tests, `ruff`, `mypy`; do not run `tools/rpi-checks.py`) and a local commit (`Refs #146` + Copilot trailer, no push) using the authenticated GitHub user's privacy-safe noreply email (`{id}+{login}@users.noreply.github.com`).

### Intent

Execute all Focused validation checks in a cleaned-up workspace-local `.venv-146-tmp` virtualenv (removed before commit), reconcile plan/details/changes/state artifacts, complete the single `rpi-review` pass, and create the local commit cleanly.

### Boundaries

* Included: Temporary `.venv-146-tmp` editable installation and test/lint/type execution, RPI artifact reconciliation, `rpi-review` artifact creation, local `git config --local user.email`, and `git commit`.
* Excluded: `tools/rpi-checks.py`, `git push`, or leaving temporary files inside the repository.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/demo-146-monitoring-alerts-changes.md`
* `.copilot-tracking/reviews/2026-11-15/demo-146-monitoring-alerts-review.md`
* `.copilot-tracking/rpi-sessions/2026-11-15/demo-146-monitoring-alerts-state.json`

### Dependencies

* P01, P02.

### Validation Expectations

* `infra/tests` (`unittest`), `src/core/tests` (`unittest`), `src/api/tests/test_assistant_release.py` (`unittest`), `ruff check` + `ruff format --check` (`src/core` and `#146` `infra/` monitoring files), and `mypy` (`src/core`) all exit `0`.

### Completion Evidence

* Clean `git status --short` after commit and verified `git log -1` showing `Refs #146` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run Focused validation suite (`infra/tests`, `src/core` tests, `src/api` release tests, `ruff`, `mypy`) and reconcile artifacts

#### Context

`infra/tests/test_bicep_policy.py` and `test_alert_runbook_signal_matrix.py` import `zava_forward.core` and `zava_forward.orchestrator`. Installing `-e src/core -e src/agents -e src/api -e src/orchestrator -e src/importer` into `.venv-146-tmp` (`python3 -m venv --system-site-packages .venv-146-tmp`) satisfies editable distribution rules from `.github/copilot-instructions.md` and is removed cleanly before `git status` and commit.

#### Intent

Verify zero regressions across infrastructure, core monitoring/release logic, formatting, linting, and strict typing, then remove `.venv-146-tmp` and reconcile all RPI tracking records.

#### Boundaries

* Included: Running unit tests, `ruff`, and `mypy`, cleaning `.venv-146-tmp`, and updating `.copilot-tracking/` artifacts.
* Excluded: Running `tools/rpi-checks.py`.

#### Likely Targets

* `.copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md`
* `.copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md`
* `.copilot-tracking/changes/2026-11-15/demo-146-monitoring-alerts-changes.md`

#### Dependencies

* P01, P02.

#### Validation Expectations

* Exit code `0` on every validation command.

#### Completion Evidence

* Exact command summary and counts recorded in `.copilot-tracking/changes/2026-11-15/demo-146-monitoring-alerts-changes.md`.

#### Unresolved Items

* None.
