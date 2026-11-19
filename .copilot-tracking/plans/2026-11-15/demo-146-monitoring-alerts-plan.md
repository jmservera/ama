<!-- markdownlint-disable-file -->
# RPI Plan: Monitoring Alerts, Workbook, Runbooks, and Task/Release Harm Declarations (Issue #146)

## Task Metadata

* Task ID: issue-146
* Task slug: demo-146-monitoring-alerts
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/demo-146-monitoring-alerts-plan-critique.md

## Executive Summary

This plan closes the remaining source-deliverable monitoring gaps for Issue `#146` on stacked branch `feat/demo-146-monitoring-alerts` (based on `feat/demo-164-chat-grounding-provenance-0900`, PR `#1641`). Research (`C1`-`C21`) verified that ledger digest alerts, `agent-tasks-poison` and `ai-limits` scheduled-query candidates, IoT Hub ingress/routing metric candidates, diagnostic log redaction, and the availability/errors/latency/cost-vs-budget workbook panels are already authored, while two concrete engineering gaps and minor `#146` test lint/format drift remain:

1. **Ranking publication job-failure alert misrouting (`infra/`)**: `infra/main.bicep` passes `job-{prefix}-rank` / `job-{prefix}-rank-publish` to `operationalMonitoring.bicep` when `enableRankingArchiveBlob=true`, but `infra/modules/operationalMonitoring.bicep` falls through its ternary to `#job-auth`, and `job-rank` is absent from `infra/monitoring-runbooks.md`, `monitoring_coverage.ALERTS`, and the signal-matrix tests. Meanwhile `infra/monitoring-workbook.json` retains one stale sentence in `status-and-boundary` claiming no poison-queue or AI-limit candidate alert exists.
2. **Per-task and per-serving-release harm/quality/disparity/review-burden declarations (`src/core/`)**: `monitoring_coverage.check_monitoring_declaration` exists as an unwired helper, and `infra/monitoring-runbooks.md` notes that no declaration is recorded for any real task. None of the 13 registered AI tasks in `ai_registry.tasks()` or serving release contracts (`rai_release.missing_contract` / `assistant_release.record`) carries or enforces the six required indicators (`unsupported_claims`, `critical_misses`, `stale_review_attempts`, `challenges`, `cohort_errors`, and complete `review_effort` covering preparation, review, correction, and re-review without treating approval rate as safety), denominators, observation windows, offline-only constructed vs named-human live thresholds, accountable monitoring/incident owners, and response.

### User Decisions and Requirements Highlights

* Run the full RPI loop continuously without pausing after `rpi-plan` (`rpi-research` -> `rpi-plan` -> `rpi-plan-critique` -> `rpi-implement` -> `rpi-review`) on `feat/demo-146-monitoring-alerts`.
* Verify and complete Bicep/monitoring alert, workbook, runbook, and `src/core` task/serving-release harm-monitoring declaration coverage for Issue `#146`.
* Apply the Focused validation tier (`infra/tests`, `src/core` unit tests, `ruff`, `mypy`; do not execute `tools/rpi-checks.py`) and commit locally with `Refs #146` and the Copilot trailer without pushing.

### What You May Not Know

* `import-jobs-poison` intentionally has no scheduled-query alert rule because `src/importer/` routes bad rows to `quarantine` and never enqueues poison messages; both `operationalMonitoring.bicep` and `src/core/tests/test_monitoring_coverage.py` enforce `import-jobs-poison` and `rai-harm` as explicit `GAP` entries (`C4`, `C16`).
* `ai_registry.REGISTRY_VERSION` (`2026-10-15.1`) and `assistants.VERSION` (`1.0.0`) are pinned in `heldout_eval.FROZEN_VERSIONS` and `FROZEN_CAPABILITY_VERSIONS` (`C17`) and must remain unchanged; `task_contract_version` hashes `ai_registry.get(task)` dynamically at runtime.
* Live threshold approvals must reject non-human (`system`, `agent`, `bot`, `copilot`) and placeholder/fictional (`placeholder`, `mock`, `fictional`, `tbd`, `unapproved`) attributions, keeping constructed thresholds offline-only (`live=False`) while preserving `LiveReleaseApprover`'s minimal 4-key direct calls to `rai_release.missing_binding` (`C14`, `C18`).

### Unresolved Decisions or Blockers

* None blocking this source slice. External operational prerequisites — live owner appointments (`OD-51`), live human threshold sign-offs (`OQ-017`, `OQ-018`), live Log Analytics schema drills, and Azure Cost Management billing export ingestion — remain honest documented gaps (`Refs #146`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Execute `rpi-research`, `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` continuously in one run without pausing for user input, writing dated artifacts under `.copilot-tracking/` (caller prompt).
* Target worktree `/home/azureuser/source/ama-demo-wt/feat-146-monitoring-alerts` on branch `feat/demo-146-monitoring-alerts` stacked on `feat/demo-164-chat-grounding-provenance-0900` (PR `#1641`) (caller prompt).
* Verify and complete coverage across `infra/modules/monitoring.bicep`, `infra/modules/operationalMonitoring.bicep`, `infra/main.bicep`, `infra/monitoring-workbook.json`, `infra/monitoring-runbooks.md`, and `src/core` harm monitoring declarations for:
  * Alerts covering job failures, poison queue, ledger digest verification, and IoT Hub ingestion when delivered (`Issue #146`, caller prompt).
  * Dashboard/workbook showing availability, errors, latency, and cost against the budget (`Issue #146`, caller prompt).
  * Per-task and per-serving-release declarations of applicable harm, quality, disparity, and review-burden indicators (`unsupported_claims`, `critical_misses`, `stale_review_attempts`, `challenges`, `cohort_errors`, and complete `review_effort` where applicable), denominators, observation window, thresholds (constructed offline-only vs named-human live approval), accountable monitoring/incident owners, and response (`Issue #146`, caller prompt).
* Validate using the Focused tier (`infra/tests`, `src/core` unit tests, `ruff check`, `ruff format --isolated --line-length 100 --check` on `infra/` monitoring targets, and `mypy`), without running `tools/rpi-checks.py` (caller prompt).
* Commit all changes and `.copilot-tracking/` artifacts locally using repository-local privacy-safe GitHub noreply email, `Refs #146`, and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, without pushing (caller prompt, `.github/copilot-instructions.md`).

## Goals

* Ensure every Container Apps job passed from `infra/main.bicep` into `operationalMonitoring.bicep` (including `job-{prefix}-rank` / `job-{prefix}-rank-publish`) maps to a dedicated runbook anchor (`#job-rank`), `monitoring_coverage.ALERTS` entry, and signal-matrix assertion, while preserving all installed core/ledger alerts, poison-queue/IoT/AI-limit candidate guards, and workbook panels.
* Record complete, truthful 6-indicator harm/quality/disparity/review-burden monitoring declarations across all 13 registered AI tasks and enforce them on task registration (`ai_registry`) and serving release contracts (`rai_release`, `assistant_release`), keeping constructed thresholds strictly offline-only and requiring named-human non-fictional approval for live thresholds.
* Verify all `infra/tests`, `src/core` unit tests (plus affected `src/api` release admission tests), `ruff`, and `mypy` checks pass cleanly.

## Scope and Non-Goals

### In Scope

* `infra/modules/operationalMonitoring.bicep`: map `-rank` / `-rank-publish` job suffix to `#job-rank` while keeping existing parameters, candidate-alert disablement guards, IoT Hub metrics, `agent-tasks-poison`, `ai-limits`, and workbook resource wiring intact.
* `infra/monitoring-runbooks.md` and `infra/monitoring-workbook.json`: add `### Job rank` (`#job-rank`) runbook section, refresh the stale candidate-alert sentence in workbook `status-and-boundary`, and update the runbook's Issue `#146` declaration status note.
* `src/core/src/zava_forward/core/monitoring_coverage.py`: add `job-rank` (`CANDIDATE`) to `ALERTS`; enforce named-human non-fictional approvers on live indicator and AI-limit thresholds; validate `review_effort` complete effort stages (`preparation`, `review`, `correction`, `re_review`) and `approval_rate_is_safety is False`; and provide canonical `task_declaration(task_id)` / `task_declarations()` for all 13 registered AI tasks.
* `src/core/src/zava_forward/core/ai_registry.py`, `rai_release.py`, `assistant_release.py`, `assistants.py`, `src/core/tests/release_support.py`, and `src/core/tests/test_rai_release.py`: attach `monitoring_declaration` to registered tasks, validate declaration completeness in `ai_registry.missing_fields` and `rai_release.missing_contract` (using cycle-safe lazy imports between `rai_release` and `monitoring_coverage`), reject constructed/unapproved thresholds when `live=True` in `rai_release.missing_binding` (when `monitoring_declaration` is present), persist `monitoring_declaration` in `assistant_release.record`, expose `monitoring_status` in both disabled and enabled branches of `Assistants.registry`, and populate `release_support.fixture` and `ReleaseContract` fixtures.
* Focused unit/contract tests and `--line-length 100` `ruff` hygiene across `#146` `infra/tests/` monitoring files (including `infra/tests/test_diagnostic_log_privacy.py`) and `src/core/tests/`.

### Non-Goals

* Enabling disabled candidate alerts by default before live Log Analytics table/column verification and `OD-51` owner appointments.
* Adding a scheduled-query alert for `import-jobs-poison` or `rai-harm` while no source signal producer exists.
* Modifying `ai_registry.REGISTRY_VERSION` or `assistants.VERSION` (frozen in `heldout_eval.py`).
* Reformatting unrelated legacy scripts in `infra/scripts/` outside Issue `#146` monitoring scope.
* Running `tools/rpi-checks.py` or pushing commits to `origin`.

## Functional Requirements

* FR-1: Job-failure candidate alerts in `infra/modules/operationalMonitoring.bicep` must route every job family configured in `infra/main.bicep` (`orchestrator`/`orch`, `ledger-verify`/`audit`, `import`/`load`, `rank-publish`/`rank`, `auth-renewal`/`auth`) to its matching anchor in `infra/monitoring-runbooks.md` and matching `CANDIDATE` entry in `monitoring_coverage.ALERTS`.
  * Observable acceptance criteria: Compiling `infra/main.bicep` with `enableRankingArchiveBlob=true` produces `alert-job-forward-dev-rank-publish-failed` (and demo `alert-job-fdev-rank-failed`) pointing to `#job-rank`, with matching `### Job rank` runbook entry and `ALERTS` register entry.
* FR-2: `infra/monitoring-workbook.json` must accurately describe installed versus disabled-candidate versus missing-producer alerts alongside existing availability, request error/latency, operation error/latency, and cost-against-budget panels.
  * Observable acceptance criteria: Workbook JSON validates against all KQL privacy/sample-weighting/budget assertions and `status-and-boundary` accurately distinguishes disabled candidate rules (`agent-tasks-poison`, `ai-limits`, job, IoT) from producerless gaps (`import-jobs-poison`, `rai-harm`).
* FR-3: Every registered AI task (`ai_registry.tasks()`, all 13 tasks) must carry a `monitoring_declaration` conforming to `monitoring_coverage.check_monitoring_declaration` schema: covering `unsupported_claims`, `critical_misses`, `stale_review_attempts`, `challenges`, `cohort_errors`, and complete `review_effort` (`effort_stages: ["preparation", "review", "correction", "re_review"]` validated as a JSON-round-trip-safe sequence, `approval_rate_is_safety: False`), positive integer `denominator` plus `denominator_unit` (or `applicable: False` with explicit `reason`), `window` (`"P7D"` or `"P28D"`), `threshold` (`{"limit": <float 0..1>, "min_sample": <int >= 0>, "constructed": True}`), accountable role-level `monitoring_owner` and `incident_owner`, `response`, and `manual_route_status`.
  * Observable acceptance criteria: `ai_registry.missing_fields(entry)` returns `[]` for all 13 registered tasks and reports `"monitoring_declaration"` when mutated; `check_monitoring_declaration(entry["monitoring_declaration"], task_enabled=entry["enabled"])` returns `status == "declared"` offline (`live=False`) and `status == "blocked"` with colon-delimited `"indicator:<name>:threshold"` missing entries when `live=True`.
* FR-4: Every serving release contract (`rai_release.missing_contract` and `assistant_release.record`) must require a complete `monitoring_declaration` aligned to the task's enabled state, and live admission (`rai_release.missing_binding(..., live=True)`) must block constructed or non-human/fictional-approved thresholds.
  * Observable acceptance criteria: Recording or admitting a release without a valid `monitoring_declaration` fails closed; constructed thresholds pass offline admission (`live=False`) and fail live admission (`live=True`); system/agent/bot/placeholder `approved_by` strings are rejected on live thresholds in `evaluate_indicator`, `evaluate_ai_limits`, `check_monitoring_declaration(..., live=True)`, and `rai_release.missing_binding(..., live=True)`.

## Non-Functional Requirements

* NFR-1: Diagnostic and workbook privacy preservation.
  * Objective threshold or evaluation condition: Zero personal data, raw sensor readings, or chat/prompt/completion fields projected in workbook KQL or emitted by monitoring helpers.
  * Operating condition or verification approach: Verified by `infra/tests/test_monitoring_workbook_sla_budget.py`, `test_ai_observability_workbook_budget.py`, and `src/core/tests/test_monitoring_coverage.py`.
  * Observable acceptance criteria: All privacy allowlist and forbidden-column tests pass with zero exemptions.
* NFR-2: Frozen evaluation digest stability and strict static analysis.
  * Objective threshold or evaluation condition: `heldout_eval.FROZEN_MANIFEST_DIGEST` and `FROZEN_THRESHOLDS_DIGEST` remain untouched; `mypy` (`src/core`) and `ruff` checks pass with exit code `0`.
  * Operating condition or verification approach: Run `src/core` unit suite (including `test_heldout_eval.py` and `test_rai_release.py`), `src/api/tests/test_assistant_release.py`, `infra/tests`, `ruff`, and `mypy` using a cleaned-up workspace-local `.venv-146-tmp` virtualenv with editable `src/*` distributions installed.
  * Observable acceptance criteria: Zero test failures, zero `mypy` errors, and zero `ruff` check/format errors across `src/core` and `#146` `infra/` monitoring files (including `infra/tests/test_diagnostic_log_privacy.py`).

## Acceptance Criteria

* AC-1: `infra/modules/operationalMonitoring.bicep`, `infra/main.bicep`, `infra/modules/monitoring.bicep`, `infra/monitoring-runbooks.md`, and `monitoring_coverage.ALERTS` cover job failures (all 5 job families including `job-rank`), poison queue (`agent-tasks-poison` candidate + documented `import-jobs-poison` producerless gap), ledger digest verification (`ledger-digest-mismatch` and `ledger-verify-missing`), and IoT Hub ingestion (`iot-ingress-throttle`, `iot-routing-dropped`, `iot-routing-invalid`, `iot-routing-orphaned`) with 1:1 signal-matrix parity.
* AC-2: `infra/monitoring-workbook.json` shows availability, errors, p95 latency, and monthly budget (`150` GBP, `80%` actual / `100%` forecast notifications, `Unknown` actual/forecast cost, `Unreconciled` variance) with accurate status-and-boundary copy and full KQL privacy compliance.
* AC-3: All 13 tasks in `ai_registry.tasks()` and all serving release contracts in `rai_release.py` / `assistant_release.py` declare and enforce the 6 harm/quality/disparity/review-burden indicators (`unsupported_claims`, `critical_misses`, `stale_review_attempts`, `challenges`, `cohort_errors`, and complete `review_effort` across `preparation`, `review`, `correction`, `re_review`), denominators, observation windows, thresholds, accountable monitoring/incident owners, and response.
* AC-4: Constructed monitoring thresholds pass offline checks only (`live=False`) and fail closed for live use (`live=True`) unless approved by an explicit named human (rejecting system/agent/bot and placeholder/fictional tokens).
* AC-5: All `infra/tests`, `src/core` unit tests, targeted `src/api` release tests, `ruff`, and `mypy` checks pass, and all changes plus `.copilot-tracking/` artifacts are committed locally with `Refs #146` and the Copilot trailer without pushing.

## Test Ownership and Validation Lock

* Canonical targets modified:
  * `infra/modules/operationalMonitoring.bicep`
  * `infra/monitoring-runbooks.md`
  * `infra/monitoring-workbook.json`
  * `src/core/src/zava_forward/core/monitoring_coverage.py`
  * `src/core/src/zava_forward/core/ai_registry.py`
  * `src/core/src/zava_forward/core/rai_release.py`
  * `src/core/src/zava_forward/core/assistant_release.py`
  * `src/core/src/zava_forward/core/assistants.py`
  * `src/core/tests/release_support.py`
  * `src/core/tests/test_rai_release.py`
  * `src/api/tests/test_assistant_release.py` (immediately-relevant implementation-time update aligning actual-release and route contract-field fixtures with `monitoring_declaration`)
* Generated targets: `none` (Bicep compilation is verified dynamically in memory via `az bicep build --stdout` inside `infra/tests`).
* Test ownership, removals, and additions bound:
  * Exact test removals: `none`.
  * Maximum new test methods added: `<= 14` focused semantic/contract tests across existing suites (`infra/tests/test_monitoring_alerts.py`, `infra/tests/test_alert_runbook_signal_matrix.py`, `infra/tests/test_ai_alert_runbook_ownership.py`, `src/core/tests/test_monitoring_coverage.py`, `src/core/tests/test_ai_register_completeness.py`, `src/core/tests/test_rai_release.py`, `src/core/tests/test_rai_threshold_live_approval_guard.py`).
  * Semantic vs regression coverage: semantic tests prove `-rank`/`-rank-publish` Bicep compilation to `#job-rank`, 13-task 6-indicator declaration completeness (including complete 4-stage `review_effort` and non-applicability rationale), release contract rejection when `monitoring_declaration` is missing/incomplete, and live fail-closed rejection of constructed or bot/fictional-approved thresholds; regression runs cover full `infra/tests`, `src/core/tests`, and `src/api/tests/test_assistant_release.py`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md                                                                    |
| Phase details                    | .copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md                                                         |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/demo-146-monitoring-alerts-plan-critique.md with Revise disposition resolved (`PC-001`..`PC-004` applied directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/demo-146-monitoring-alerts-research.md (`executed`, `Ready`)                                       |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/demo-146-monitoring-alerts-changes.md is created by `rpi-implement` as its canonical evidence record |
| Planning execution and readiness | Complete and Ready for `rpi-implement` after incorporating single-pass critique findings `PC-001`..`PC-004`                               |
| Continuation context             | Confirmed automatic RPI Agent session; continuing immediately to `rpi-implement` and `rpi-review`                                         |

## Sources

* `.copilot-tracking/research/2026-11-15/demo-146-monitoring-alerts-research.md`: `C1`-`C21` codebase evidence, gap synthesis, and contrarian compatibility checks.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: Observability, tokenomics, and RAI harm-monitoring specification (`AC-029`, `AC-070`, `AC-073`, `OQ-017`, `OQ-018`).
* `docs/adrs/0001-azure-architecture.md`: Failure domains (`agent-tasks-poison`, `quarantine`), provisional SLO targets (`99.5%`, `p95 < 500 ms`), and monthly budget alerts (`80%` actual, `100%` forecast).
* `infra/modules/operationalMonitoring.bicep`, `infra/main.bicep`, `infra/modules/monitoring.bicep`, `infra/monitoring-workbook.json`, `infra/monitoring-runbooks.md`: Existing alert, workbook, and runbook contracts.
* `src/core/src/zava_forward/core/monitoring_coverage.py`, `ai_registry.py`, `rai_release.py`, `assistant_release.py`, `assistants.py`: Existing monitoring register, AI task registry, and serving release admission contracts.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Bicep Alert Parity, Workbook Boundary Accuracy, and Runbook Alignment

* Intent: Fix `job-rank` / `job-rank-publish` alert-to-runbook routing and align `infra/monitoring-runbooks.md`, `infra/monitoring-workbook.json`, `monitoring_coverage.ALERTS`, and `infra/tests` signal matrices.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Route ranking publication job failures to `#job-rank` and update runbook, workbook, and alert register

* Requirement and evidence: FR-1, FR-2, AC-1, AC-2 (`C4`, `C5`, `C6`, `C7`, `C8`, `C10`)
* Expected result: `operationalMonitoring.bicep` maps `-rank` / `-rank-publish` to `#job-rank`; `infra/monitoring-runbooks.md` defines `### Job rank` and updates Issue `#146` declaration notes; `infra/monitoring-workbook.json` accurately states candidate vs producerless-gap alert status; `monitoring_coverage.ALERTS` includes `job-rank` (`CANDIDATE`).
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Update `infra/tests` alert/runbook matrices and align `--line-length 100` `ruff` formatting on `#146` monitoring tests

* Requirement and evidence: FR-1, NFR-1, NFR-2, AC-1, AC-5 (`C15`, `C21`)
* Expected result: `test_monitoring_alerts.py` verifies compiled `enableRankingArchiveBlob=true` ranking job failure alerts target `#job-rank`; `test_alert_runbook_signal_matrix.py` (including `test_poison_ledger_job_and_iot_signals_are_covered`) and `test_ai_alert_runbook_ownership.py` include `job-rank`; all `#146` monitoring test files in `infra/tests/` (including `test_diagnostic_log_privacy.py`) pass isolated `ruff check` (`E,F,I,B,UP`) and `ruff format --isolated --line-length 100 --check`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Task and Serving-Release Harm/Quality/Disparity/Review-Burden Declarations

* Intent: Declare complete 6-indicator harm monitoring contracts for all 13 registered AI tasks and enforce offline-constructed vs named-human live threshold rules across `monitoring_coverage`, `ai_registry`, `rai_release`, `assistant_release`, and `assistants`.
* Dependencies: P01-T01 (`monitoring_coverage.py` shared module)

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add canonical 13-task harm declarations, complete review-effort validation, and named-human live threshold guards in `monitoring_coverage.py`

* Requirement and evidence: FR-3, FR-4, AC-3, AC-4 (`C1`, `C10`, `C11`, `C12`, `C14`)
* Expected result: `monitoring_coverage.py` enforces named-human non-fictional `approved_by` on live thresholds (`evaluate_indicator`, `evaluate_ai_limits`, `check_monitoring_declaration(..., live=True)`), validates 4-stage `review_effort` (`preparation`, `review`, `correction`, `re_review`, `approval_rate_is_safety=False`), and defines `task_declaration(task_id)` / `task_declarations()` for all 13 registered AI tasks.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Enforce `monitoring_declaration` on task registration and serving release contracts (`ai_registry`, `rai_release`, `assistant_release`, `assistants`, `release_support`)

* Requirement and evidence: FR-3, FR-4, NFR-2, AC-3, AC-4 (`C11`, `C12`, `C13`, `C17`, `C18`, `C19`, `C20`)
* Expected result: Every `ai_registry` entry carries and validates `monitoring_declaration`; `rai_release.missing_contract` and `assistant_release.record` require and persist a complete `monitoring_declaration` using cycle-safe lazy imports; `rai_release.missing_binding(..., live=True)` rejects constructed/non-human thresholds when `monitoring_declaration` is present; `Assistants.registry` exposes `monitoring_status` on both disabled and enabled task branches; `release_support.fixture` supplies offline constructed thresholds by default and named-human test approval when `cls == "actual"`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md

<!-- rpi:task id=P02-T03 -->
#### [x] P02-T03: Add focused unit tests for task/release harm declarations and live threshold approval guards

* Requirement and evidence: FR-3, FR-4, AC-3, AC-4, AC-5 (`C16`, `C18`, `C20`)
* Expected result: `test_monitoring_coverage.py`, `test_ai_register_completeness.py`, `test_rai_release.py`, `test_rai_threshold_live_approval_guard.py`, and `src/api/tests/test_assistant_release.py` verify all 13 task declarations, complete review-effort validation (including JSON list round-trip), release contract enforcement, offline-only constructed threshold acceptance, and live rejection of constructed/system/agent/fictional threshold approvals.
* Detail section: P02-T03 in .copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Tier Validation and Local Commit Closeout

* Intent: Verify all targeted test suites, linters, formatters, and typecheckers pass in an isolated editable virtualenv, reconcile RPI tracking artifacts, execute post-implementation review, and commit locally with `Refs #146` without pushing.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run Focused validation suite (`infra/tests`, `src/core` tests, `src/api` release tests, `ruff`, `mypy`) and reconcile artifacts

* Requirement and evidence: NFR-1, NFR-2, AC-5 (`C21`)
* Expected result: Editable `src/*` install in a workspace-local `.venv-146-tmp` virtualenv (removed immediately after validation) runs `infra/tests`, `src/core/tests`, `src/api/tests/test_assistant_release.py`, `src/core` `ruff` + `mypy`, and `#146` `infra/` `ruff` check/format with exit code `0`, leaving zero temporary files in the worktree.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md

## Dependencies

* Azure CLI with Bicep (`az bicep build`): Required by `infra/tests` to compile `main.bicep` and `modules/operationalMonitoring.bicep` (verified installed in environment).
* Editable `zava_forward.*` distributions (`src/core`, `src/agents`, `src/api`, `src/orchestrator`, `src/importer`): Installed in a temporary workspace-local `.venv-146-tmp` Python 3.12 virtualenv (removed before commit) so `infra/tests/test_bicep_policy.py` and `test_alert_runbook_signal_matrix.py` import current `src/core` and `src/orchestrator` symbols cleanly.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [High]: Schema/key/casing/tuple alignment with `monitoring_coverage.py` | Resolved | Updated `FR-3` and `P02-T01` to use `DECLARED = "declared"` / `BLOCKED = "blocked"`, `reason`, `window`, positive integer `denominator` (with `denominator_unit`), `threshold.min_sample`, `manual_route_status`, colon-delimited `indicator:<name>:...` tokens, and JSON-safe list `effort_stages` validated as a sequence. |
| `PC-002` [High]: `src/core/tests/test_rai_release.py` fixtures and `rai_release` / `monitoring_coverage` import cycle | Resolved | Added `src/core/tests/test_rai_release.py` to `Test Ownership` and `P02-T03`, and specified lazy function-local imports of `monitoring_coverage` inside `rai_release.missing_contract` and `missing_binding` in `P02-T02`. |
| `PC-003` [Medium]: `Assistants.registry` class name and dual disabled/enabled task branches | Resolved | Updated `In Scope`, `P02`, and `P02-T02` to target `Assistants.registry` and attach `monitoring_status` in both the disabled (`task_enabled=False`) and enabled (`task_enabled=True`) branches. |
| `PC-004` [Low]: Include `test_diagnostic_log_privacy.py`, `test_poison_ledger_job_and_iot_signals_are_covered`, and workspace-local `.venv-146-tmp` cleanup | Resolved | Added `infra/tests/test_diagnostic_log_privacy.py` and `test_poison_ledger_job_and_iot_signals_are_covered` to `P01-T02`, and replaced external `/tmp` venv path with cleaned-up workspace-local `.venv-146-tmp` in `P03-T01`. |

## Follow-Up Items

* Appoint named human operational and RAI owners (`OD-51`, `OQ-017`, `OQ-018`) and execute live Log Analytics table/field signal drills before enabling disabled candidate alerts in `operationalMonitoring.bicep`.
* Connect an approved Azure Cost Management billing export before replacing `Unknown` / `Unreconciled` Azure cost columns in `infra/monitoring-workbook.json`.
* Add an `import-jobs-poison` queue producer and corresponding scheduled-query alert only if `src/importer/` moves from `quarantine`-only row isolation to queue dead-lettering.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/demo-146-monitoring-alerts-changes.md
* Ready phase or task: Complete (`P01`, `P02`, `P03` checked; ready for `rpi-review`)
* Remaining provisional question or blocker: None
