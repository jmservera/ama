---
description: "Primary evidence artifact for Issue #146 monitoring coverage: alerts, dashboards, runbooks, and RAI harm monitoring declarations"
---
<!-- markdownlint-disable-file -->

# Task Research: demo-146-monitoring-alerts

| Field              | Value                                                                             |
|--------------------|-----------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                        |
| Researcher / agent | RPI Agent (`rpi-research`)                                                        |
| Status             | Complete                                                                          |
| Research disposition | executed                                                                        |
| Planning Readiness | Ready                                                                             |
| Artifact path      | .copilot-tracking/research/2026-11-15/demo-146-monitoring-alerts-research.md      |

## Research Brief

* What to research: Current coverage and remaining gaps in `infra/modules/monitoring.bicep`, `infra/modules/operationalMonitoring.bicep`, `infra/main.bicep`, `infra/monitoring-workbook.json`, `infra/monitoring-runbooks.md`, `infra/tests/`, and `src/core` harm monitoring declarations (`monitoring_coverage.py` and callers) against the unchecked criteria of Issue #146.
* Why it matters: Determines exact surgical infrastructure, workbook, runbook, declaration, and test changes required to verify and complete Issue #146 monitoring coverage on stacked branch `feat/demo-146-monitoring-alerts`.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` within this automatic RPI session.
* Scope: `infra/modules/monitoring.bicep`, `infra/modules/operationalMonitoring.bicep`, `infra/main.bicep`, `infra/monitoring-workbook.json`, `infra/monitoring-runbooks.md`, `infra/tests/test_*monitoring*.py`, `infra/tests/test_alert_runbook_signal_matrix.py`, `infra/tests/test_ai_*.py`, `src/core/src/zava_forward/core/monitoring_coverage.py`, `src/core/tests/test_monitoring_coverage.py`, and related callers in `src/`.
* Non-goals: Live Azure subscription deployment, portal screenshot capture, paid inference, billing reconciliation against live Azure Cost Management APIs, adding a separate observability/governance platform, or pushing to remote.
* Criteria: Every unchecked scope item in the prompt for Issue #146 is audited against current branch code and tests, distinguishing source-deliverable coverage from live-deployment/human-approval gates.
* Requested outputs: Convergence recommendation with exact gap analysis, evidence IDs (`C#`), alternatives considered, and `Ready` planning state.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                   |
|----------------------------------|---------------------------------------------------------------------------------------------------------|
| Research question(s)             | What gaps remain across Bicep alerts, workbook panels, runbooks, and `src/core` RAI harm declarations for Issue #146? |
| Codebase scope                   | `infra/`, `src/core/`, `src/api/`, `src/agents/`, `src/orchestrator/`, `docs/adrs/0001-azure-architecture.md`, `docs/prds/` |
| External scope                   | none                                                                                                    |
| Initial internal candidate areas | `infra/modules/monitoring.bicep`, `infra/modules/operationalMonitoring.bicep`, `infra/main.bicep`, `infra/monitoring-workbook.json`, `infra/monitoring-runbooks.md`, `src/core/src/zava_forward/core/monitoring_coverage.py` |
| Initial external candidate areas | none                                                                                                    |
| Research posture                 | focused                                                                                                 |
| Posture provenance               | caller-specified (bounded internal task with named targets and focused validation tier)                  |
| Explicit limits / deadline       | Single continuous automatic RPI run; do not run `tools/rpi-checks.py`; do not push                      |
| Posture-specific completion basis| Focused scope and materiality: all named files, tests, and Issue #146 target criteria inspected and verified |
| Edits allowed during research?   | no, research-only                                                                                       |
| Resolved evidence root           | `.copilot-tracking/`                                                                                    |
| Known constraints / excluded sources | Preserve privacy exclusions (no personal data, raw readings, chat content in logs); constructed thresholds for offline tests only; live thresholds require named-human approval |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                              | Scoped authority or output contract          | Selected / skipped reason      |
|---------------------|---------------------------------------|---------------------------------------------------|----------------------------------------------|--------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` matches workspace and evidence    | Repository conventions, privacy, validation, markdown rules | Selected: mandatory repository instructions |
| Skill               | `telemetry-foundations` / `rai-standards` | Optional plugin skills on telemetry and RAI   | Advisory patterns only                       | Skipped: repository already has canonical Bicep/Python contracts and PRD v0.16.0+ schema |
| Research specialist | `hve-core-all:rpi-researcher`         | Available subagent for independent lanes          | Bounded lane artifact writer                 | Skipped (inline preferred): tightly coupled Bicep/workbook/runbook/Python contracts fit direct reads faster and more accurately |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                       | Answers / unanswered      | Resulting decision or selected further research    |
|------------------|-------------------------------------------------------------|---------------------------|----------------------------------------------------|
| Intake           | Non-interactive continuous RPI run with explicit scope, branch, validation tier, and commit rules | N/A (autonomous) | Proceed with `focused` posture in `convergence` mode |
| Direction change | None at intake                                              | N/A                       | Keep caller scope                                  |
| Convergence      | All four research questions answered with `C1`-`C21` evidence | Complete          | Converged on surgical Bicep/runbook/workbook/`src/core` declaration slice (`Ready` for `rpi-plan`) |

## Scope and Success Criteria

* Scope: Bicep alert definitions and wiring (`job failures`, `poison queue`, `ledger digest verification`, `IoT Hub ingestion when delivered`), workbook coverage (`availability`, `errors`, `latency`, `cost against budget`), runbook alignment, and `src/core` task/serving release RAI harm monitoring declarations (`unsupported claims`, `critical misses`, `stale review attempts`, `challenges`, `cohort errors`, `complete review effort`, denominators, windows, thresholds, owners, response, and offline-only constructed threshold guardrails).
* Assumptions: Prior PRs and commits on `feat/demo-164-chat-grounding-provenance-0900` (and earlier `146-*` slices) already delivered substantial parts of monitoring; we must verify what is actually on HEAD right now rather than trusting older tracking files.
* Success criteria:
  * Every research question is answered with exact `path:line` codebase evidence.
  * Existing tests in `infra/tests` and `src/core/tests` are inspected to see what is enforced and what gaps remain.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. Verify and complete Bicep/monitoring alert and workbook coverage (`infra/modules/monitoring.bicep`, `infra/main.bicep`, `infra/monitoring-runbooks.md`, and `src/core` harm monitoring declarations if needed) for the four listed criteria.
  2. Ensure all existing `infra/tests` and `src/core` monitoring tests pass, plus `ruff check`, `ruff format --isolated --line-length 100 --check` on `infra/`, and `mypy`.
  3. Commit all changes and `.copilot-tracking/` artifacts with `Refs #146` and trailer, without pushing.
* Inferred research questions:
  * Q1: How are alerts for job failures, poison queue, ledger digest verification, and IoT Hub ingestion currently defined and wired across `infra/modules/monitoring.bicep`, `infra/modules/operationalMonitoring.bicep`, `infra/main.bicep`, and `infra/monitoring-runbooks.md`, and what is missing or incomplete?
  * Q2: How does `infra/monitoring-workbook.json` (and its Bicep deployment) display availability, errors, latency, and cost against the budget, and are any panels, KQL queries, or Bicep workbook resources missing or unwired?
  * Q3: Which task/serving releases exist in `src/` (including any newly added chat/grounding/resident/agent tasks from the parent branch `feat/demo-164-chat-grounding-provenance-0900`), and does `src/core/src/zava_forward/core/monitoring_coverage.py` declare all required indicators (`unsupported claims`, `critical misses`, `stale review attempts`, `challenges`, `cohort errors`, `complete review effort`), denominators, observation windows, offline vs live thresholds, accountable owners, and responses for every serving task/release?
  * Q4: What do existing `infra/tests` and `src/core` tests currently assert, do they currently pass, and what gaps exist between the tests and the target criteria?
* Caller constraints and non-goals: Focused validation tier only; do not run `tools/rpi-checks.py`; do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint  | Effect on active brief, evidence, or revalidation |
|----------------------------------------------------------|-----------------------|----------------------|---------------------------------------------------|
| narrow                                                   | Focused validation tier (`infra/tests`, `src/core` unit tests, `ruff`, `mypy`); exclude `tools/rpi-checks.py` and `git push` | Caller intake | Constrains validation and closeout actions |

## Research Questions

|  # | Sub-question | Type (depth / breadth / straightforward) | Priority | Status |
|---:|--------------|------------------------------------------|----------|--------|
| Q1 | Alert coverage and Bicep wiring for job failures, poison queue, ledger digest verification, and IoT Hub ingestion when delivered | depth | H | answered (`C3`-`C7`, `C9`, `C15`) |
| Q2 | Workbook/dashboard coverage and Bicep provisioning for availability, errors, latency, and cost against budget | depth | H | answered (`C4`, `C5`, `C8`) |
| Q3 | Task/serving release harm monitoring declarations in `src/core` and across `src/` serving tasks (including parent branch #164 tasks) | breadth | H | answered (`C6`, `C10`-`C14`, `C17`-`C20`) |
| Q4 | Current state of `infra/tests`, `src/core/tests`, `ruff`, and `mypy`, and contrarian edge cases | straightforward | H | answered (`C15`-`C21`) |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-04/monitoring-declaration-146-research.md`, `.copilot-tracking/research/2026-11-13/146-monitoring-bicep-2136-research.md`, `.copilot-tracking/reviews/2026-11-14/146-signal-runbook-matrix-review.md`, and `.copilot-tracking/reviews/2026-11-14/146-workbook-budget-panel-0327-review.md`.
* Reused (verified) findings: Prior PRs delivered `operationalMonitoring.bicep` candidate alerts (`jobFailures`, `iotFailureAlerts`, `agentTasksPoison`, `aiLimitBreach`), `monitoring-workbook.json` budget/usage/availability/latency panels, `diagnostic_logging.py` process-wide redaction, and `monitoring_coverage.check_monitoring_declaration` helper.
* Superseded / stale: Verified directly on HEAD (`243764945`) that two substantive gaps and four `#146` test formatting issues remain: (1) `job-{prefix}-rank` / `job-{prefix}-rank-publish` job-failure alert misroutes to `#job-auth` and lacks runbook/register/matrix entries, and (2) no real AI task in `ai_registry.tasks()` or serving release contract in `rai_release.py` / `assistant_release.py` records or enforces a 6-indicator harm/quality/disparity/review-burden `monitoring_declaration`.

## Cycle 1 Execution Log

### Wave 1: Wider

* Inspected case study and architecture specifications (`C1`, `C2`), live Issue `#146` checklist, all monitoring Bicep templates (`infra/modules/monitoring.bicep`, `infra/modules/operationalMonitoring.bicep`, `infra/main.bicep`, `infra/modules/containerapps.bicep`, `infra/modules/storage.bicep`, `infra/modules/iothub.bicep`), `infra/monitoring-workbook.json`, `infra/monitoring-runbooks.md`, `src/core/src/zava_forward/core/monitoring_coverage.py`, `ai_registry.py`, `rai_release.py`, `assistant_release.py`, `rai_metrics.py`, `diagnostic_logging.py`, and all monitoring test suites (`C3`-`C16`).

### Wave 2: Deeper

* **Alert coverage (`Q1`)**:
  * `infra/main.bicep:653-661` passes up to five Container Apps job families into `operationalMonitoring.params.jobNames`: `orchestrator`/`orch`, `ledger-verify`/`audit`, `import`/`load`, `rank-publish`/`rank` (when `enableRankingArchiveBlob=true`, defined at `containerapps.bicep:515`), and `auth-renewal`/`auth` (when `enableEntraTokenStore=true`, defined at `containerapps.bicep:590`) (`C5`, `C7`).
  * **Defect**: `infra/modules/operationalMonitoring.bicep:35` maps `-orch`/`-orchestrator`, `-audit`/`-ledger-verify`, and `-load`/`-import`, then falls through `else` to `'job-auth'`, silently misrouting `job-*-rank` and `job-*-rank-publish` failures to `#job-auth` (`C4`). `job-rank` is likewise missing from `infra/monitoring-runbooks.md`, `monitoring_coverage.ALERTS`, `infra/tests/test_alert_runbook_signal_matrix.py`, and `infra/tests/test_ai_alert_runbook_ownership.py` (`C6`, `C10`, `C15`).
  * Ledger digest verification is covered by installed `alert-{prefix}-ledger-digest-mismatch` and `alert-{prefix}-ledger-verify-missing` rules in `infra/main.bicep:587-640`, poison queue arrival by candidate `alert-{prefix}-agent-tasks-poison` in `operationalMonitoring.bicep:84-110`, and IoT Hub ingestion by candidate `iot-ingress-throttle`, `iot-routing-dropped`, `iot-routing-invalid`, and `iot-routing-orphaned` metric alerts in `operationalMonitoring.bicep:58-82` (`C4`, `C5`).
* **Workbook coverage (`Q2`)**:
  * `infra/monitoring-workbook.json` (provisioned by `operationalMonitoring.bicep:140-161`) displays availability (`availability`), sample-weighted request errors and p95 latency (`requests` and `operation-errors-latency`), configured monthly budget (`cost-and-budget` and `cost-vs-budget` showing `150` GBP default, `80%` actual and `100%` forecast notifications, `Unknown` actual/forecast cost, and `Unreconciled` variance), AI usage/variance, AI limit holds, and RAI harm status (`C4`, `C8`).
  * `status-and-boundary` (`infra/monitoring-workbook.json:7`) has a stale sentence stating `"No poison-queue, AI-limit or RAI-harm aggregate alert is installed by this candidate"` even though `agent-tasks-poison` and `ai-limits` disabled candidate alerts now exist (`C8`).
* **Task & serving-release harm monitoring declarations (`Q3`)**:
  * `infra/monitoring-runbooks.md:403` explicitly states: `"No declaration is recorded for any real task."` (`C6`).
  * `ai_registry.tasks()` registers 13 AI tasks (`stock-prioritisation`, `assessment-preparation`, `funding-evidence`, `works-resident-coordination`, `quality-evidence`, `briefing`, `message`, `summary`, `priority`, `funding_draft`, `read_document`, `chat-case-conversation`, `aftercare-concern-pack`); none carries a `monitoring_declaration`, and neither `rai_release.missing_contract` nor `assistant_release.record` validates or persists per-release `monitoring_declaration` contracts (`C11`, `C12`, `C13`).
  * `monitoring_coverage.evaluate_indicator` (`monitoring_coverage.py:213`) and `evaluate_ai_limits` (`monitoring_coverage.py:372`) check `rai_release.named(threshold.get("approved_by"))` instead of enforcing named-human non-fictional approval for live (`constructed=False`) thresholds (`C10`, `C12`, `C14`).

### Wave 3: Contrarian

* **Why `import-jobs-poison` must remain `GAP`**: `src/importer/` routes bad rows to `quarantine` and has no queue poison producer; `operationalMonitoring.bicep:12` and `src/core/tests/test_monitoring_coverage.py:70` explicitly assert `by_anchor["import-jobs-poison"] == mc.GAP` and `by_anchor["rai-harm"] == mc.GAP` (`C4`, `C9`, `C16`).
* **Why `operationalMonitoring.bicep` parameters and IoT tuples must not churn**: `infra/tests/test_monitoring_alerts.py:30-45` and `92-100` lock the exact 13 parameter names and 4 IoT `(suffix, metric)` tuples (`C15`).
* **Why `ai_registry.REGISTRY_VERSION` and `assistants.VERSION` must stay unchanged**: `heldout_eval.FROZEN_VERSIONS` and `FROZEN_CAPABILITY_VERSIONS` freeze `"2026-10-15.1"` and `"1.0.0"`, whereas `task_contract_version = digest(ai_registry.get(...))` is computed dynamically at runtime (`C17`).
* **Why `rai_release.missing_contract` owns required `monitoring_declaration` presence while `missing_binding(..., live=True)` checks live threshold approval when `monitoring_declaration` is present**: `test_rai_threshold_live_approval_guard.py:130` (`LiveReleaseApprover`) unit-tests `missing_binding` directly with a minimal 4-key record (`C18`), while `src/api/tests/test_assistant_release.py:1014-1021` tests full live admission via `release_support.fixture(..., cls="actual")` (`C19`, `C20`). Updating `release_support.fixture` so `cls == "actual"` stamps synthetic-test named-human threshold approval (`constructed=False`, `approved_by="Amina Okafor, RAI Assurance Lead"`) while `cls != "actual"` keeps `constructed=True` preserves every existing `src/core` and `src/api` test while enforcing fail-closed live threshold approval.
* **Baseline lint, format, and typecheck verification (`Q4`)**: `src/core` passes `ruff check .`, `ruff format --check .`, and `mypy` (`342` files). Under `infra/tests/`, 4 `#146` monitoring test files (`test_ai_alert_runbook_ownership.py`, `test_ai_observability_workbook_budget.py`, `test_monitoring_workbook.py`, `test_monitoring_workbook_sla_budget.py`) need `ruff format --isolated --line-length 100` alignment and `test_ai_alert_runbook_ownership.py:22` needs `strict=False` on `zip()` (`B905`) (`C21`).

## Evidence Log

| ID | Source (`path:line`) | Finding |
| --- | --- | --- |
| `C1` | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:455` | PRD observability, tokenomics, and RAI monitoring requirements (alerts, budget/SLO workbook, 6 harm/quality/disparity/review-burden indicators including complete preparation/review/correction/re-review effort, never approval rate as safety). |
| `C2` | `docs/adrs/0001-azure-architecture.md:274` | ADR 0001 defines `agent-tasks-poison`, `quarantine` for bad import rows, provisional 99.5% availability and p95 < 500 ms targets, and 80% actual / 100% forecast monthly budget alerts. |
| `C3` | `infra/modules/monitoring.bicep:1` | Provisions `log-{prefix}`, `appi-{prefix}`, AMPLS, private endpoint, and `ag-{prefix}-ops`. |
| `C4` | `infra/modules/operationalMonitoring.bicep:30` | Defines candidate `jobFailures`, `iotFailureAlerts`, `agentTasksPoison`, `aiLimitBreach`, and `workbook`; line 35 ternary misroutes `-rank` / `-rank-publish` jobs to `#job-auth`. |
| `C5` | `infra/main.bicep:493` | Installs core/ledger alerts and `budget-{prefix}`, and passes 5 job families (including `-rank` / `-rank-publish` at line 657) to `operationalMonitoring`. |
| `C6` | `infra/monitoring-runbooks.md:196` | Runbook catalogue omits `### Job rank` (`#job-rank`) and records at line 403 that no harm monitoring declaration is recorded for any real task. |
| `C7` | `infra/modules/containerapps.bicep:515` | Defines scheduled `rankingPublish` job (`job-{prefix}-rank` / `job-{prefix}-rank-publish`) and `authRenewal` job (line 590). |
| `C8` | `infra/monitoring-workbook.json:1` | Defines availability, errors, latency, cost-vs-budget, AI usage/variance/limit, and RAI harm panels; line 7 `status-and-boundary` text is stale on candidate poison/AI-limit rules. |
| `C9` | `infra/modules/storage.bicep:125` | Provisions `agent-tasks`, `agent-tasks-poison`, `import-jobs`, and producerless `import-jobs-poison`. |
| `C10` | `src/core/src/zava_forward/core/monitoring_coverage.py:39` | Defines `ALERTS` (missing `job-rank`), `HARM_INDICATORS`, `evaluate_indicator` (line 213 uses `named()`), `check_monitoring_declaration` (line 265), and `evaluate_ai_limits` (line 372). |
| `C11` | `src/core/src/zava_forward/core/ai_registry.py:21` | Registers 13 AI tasks without `monitoring_declaration`. |
| `C12` | `src/core/src/zava_forward/core/rai_release.py:60` | Defines `named_human()`, `missing_contract()` (line 86), and `missing_binding()` (line 206). |
| `C13` | `src/core/src/zava_forward/core/assistant_release.py:169` | Persists serving release records in `record()` and checks `rai_release.missing_contract(rec, spec)`. |
| `C14` | `src/core/src/zava_forward/core/cohort_eval.py:28` | Defines `FICTIONAL_OWNER_TOKENS` rejected on live owner approvals. |
| `C15` | `infra/tests/test_monitoring_alerts.py:25` | Asserts `operationalMonitoring` inputs and IoT metric pairs; `infra/tests/test_alert_runbook_signal_matrix.py:42` asserts Bicep-to-runbook-to-register matrix parity. |
| `C16` | `src/core/tests/test_monitoring_coverage.py:66` | Locks `agent-tasks-poison` and `ai-limits` as `CANDIDATE` and `import-jobs-poison` and `rai-harm` as `GAP`. |
| `C17` | `src/core/src/zava_forward/core/heldout_eval.py:59` | Freezes `ai_registry.REGISTRY_VERSION` (`2026-10-15.1`) and `assistants.VERSION` (`1.0.0`). |
| `C18` | `src/core/tests/test_rai_threshold_live_approval_guard.py:130` | Calls `rai_release.missing_binding` directly with a 4-key record lacking `monitoring_declaration`. |
| `C19` | `src/core/tests/release_support.py:10` | Shared `fixture()` builds offline (`constructed-fixture`) and live-shaped (`actual`) test release records. |
| `C20` | `src/api/tests/test_assistant_release.py:1014` | Tests live legacy release admission via `release_support.fixture(..., cls="actual")`. |
| `C21` | `.github/workflows/src-ci.yml:88` | Defines CI `ruff` and `mypy` flags for `src/*` and targeted `infra/` files. |

## Synthesis and Convergence Recommendation

1. **Fix `job-rank` / `job-rank-publish` alert routing, runbook, register, and workbook boundary copy**:
   * Route `-rank` and `-rank-publish` jobs to `#job-rank` in `infra/modules/operationalMonitoring.bicep:35`.
   * Add `### Job rank` (`#job-rank`) under `## New Disabled Job Candidates` in `infra/monitoring-runbooks.md`, update the Issue `#146` status note on recorded task/release declarations, add `job-rank` (`CANDIDATE`) to `monitoring_coverage.ALERTS`, and refresh the stale candidate sentence in `infra/monitoring-workbook.json:7` (`status-and-boundary`).
2. **Record and enforce per-task and per-serving-release harm/quality/disparity/review-burden declarations in `src/core`**:
   * Require named-human non-fictional approvers (`_named_human_approver`) for live thresholds in `monitoring_coverage.evaluate_indicator`, `evaluate_ai_limits`, and `check_monitoring_declaration(..., live=True)`, and validate complete review-effort coverage (`("preparation", "review", "correction", "re_review")`, `approval_rate_is_safety=False`) on `review_effort`.
   * Define canonical `task_declaration(task_id)` / `task_declarations()` in `monitoring_coverage.py` for all 13 tasks in `ai_registry.tasks()` (with `stale_review_attempts` explicitly `applicable=False` + rationale on non-persisted `chat-case-conversation`, and all 6 indicators `applicable=True` across the 5 assistants, 6 retained legacy tasks, and disabled `aftercare-concern-pack`, all carrying `constructed=True` offline thresholds, denominators, observation windows, proposed role-level `monitoring_owner` and `incident_owner` pending `OD-51`, `response`, and `manual_route`).
   * Attach and validate `monitoring_declaration` in `ai_registry._entry` / `ai_registry.missing_fields`, `rai_release.missing_contract` / `rai_release.missing_binding(..., live=True)`, `assistant_release.record`, `assistants.Service.registry`, and `src/core/tests/release_support.py:fixture()`.
3. **Add focused tests and clean `#146` `infra/tests/` formatting**:
   * Extend `infra/tests/test_monitoring_alerts.py`, `test_alert_runbook_signal_matrix.py`, `test_ai_alert_runbook_ownership.py`, `src/core/tests/test_monitoring_coverage.py`, `test_ai_register_completeness.py`, and `test_rai_threshold_live_approval_guard.py`, and format touched/monitoring `infra/tests/` files with `--isolated --line-length 100`.

### Rejected Alternatives

* Enabling candidate alerts by default without live workspace table/column drills or named owner appointments (`OD-51`).
* Adding a scheduled-query alert for producerless `import-jobs-poison` (conflicts with `operationalMonitoring.bicep:12` and `test_monitoring_coverage.py:70`).
* Changing `ai_registry.REGISTRY_VERSION` or `assistants.VERSION` (breaks `heldout_eval` frozen digests).

### Remaining External / Governance Items (Why Commit Uses `Refs #146`)

* Live owner appointments (`OD-51`), live workspace query drills, Azure Cost Management billing export ingestion, `import-jobs-poison` producer, and named-human live threshold approvals (`OQ-017`, `OQ-018`) remain external governance/deployment items.

## Self-Check

* Cycle 1 completed Wider, Deeper, and Contrarian waves in order.
* All research questions (`Q1`-`Q4`) are answered with `C1`-`C21` `path:line` citations.
* Research phase made zero edits to repository source files.
* `Research disposition`: `executed`; `Planning Readiness`: `Ready`.
