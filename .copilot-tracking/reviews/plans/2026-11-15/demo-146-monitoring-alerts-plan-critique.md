<!-- markdownlint-disable-file -->
# RPI Plan Critique: Monitoring Alerts, Workbook, Runbooks, and Task/Release Harm Declarations (Issue #146)

## Metadata

* Task ID: issue-146
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Issue #146 (`Monitoring coverage: alerts, dashboards and runbooks`) in worktree `feat/demo-146-monitoring-alerts` stacked on `feat/demo-164-chat-grounding-provenance-0900` (PR #1641). Authoritative caller decisions fix a continuous single-run RPI loop without pausing for user input, the Focused validation tier only (`infra/tests`, `src/core` unit tests, `ruff`, `mypy`, without `tools/rpi-checks.py`), verification and completion of Bicep alerts, workbook, runbooks, and `src/core` task/serving-release harm monitoring declarations across all 6 canonical indicators (`unsupported_claims`, `critical_misses`, `stale_review_attempts`, `challenges`, `cohort_errors`, `complete_review_effort`), and a local commit using `Refs #146` without pushing.
* Research and evidence considered: `.copilot-tracking/research/2026-11-15/demo-146-monitoring-alerts-research.md` (`C1` through `C21`) and direct verification of referenced code and test contracts in `infra/modules/monitoring.bicep`, `infra/modules/operationalMonitoring.bicep`, `infra/main.bicep`, `infra/monitoring-workbook.json`, `infra/monitoring-runbooks.md`, `infra/tests/test_monitoring_alerts.py`, `infra/tests/test_alert_runbook_signal_matrix.py`, `infra/tests/test_ai_alert_runbook_ownership.py`, `infra/tests/test_monitoring_workbook.py`, `infra/tests/test_monitoring_workbook_sla_budget.py`, `infra/tests/test_ai_observability_workbook_budget.py`, `infra/tests/test_diagnostic_log_privacy.py`, `infra/tests/test_bicep_policy.py`, `src/core/src/zava_forward/core/monitoring_coverage.py`, `src/core/src/zava_forward/core/ai_registry.py`, `src/core/src/zava_forward/core/rai_release.py`, `src/core/src/zava_forward/core/assistant_release.py`, `src/core/src/zava_forward/core/assistants.py`, `src/core/src/zava_forward/core/heldout_eval.py`, `src/core/tests/release_support.py`, `src/core/tests/test_monitoring_coverage.py`, `src/core/tests/test_rai_release.py`, `src/core/tests/test_rai_release_invalidation.py`, `src/core/tests/test_rai_threshold_live_approval_guard.py`, `src/core/tests/test_ai_register_completeness.py`, `src/core/tests/test_heldout_eval.py`, and `src/api/tests/test_assistant_release.py`.
* Decisions, dependencies, and acceptance criteria considered: `FR-1` through `FR-4`, `NFR-1`, `NFR-2`, `AC-1` through `AC-5`, frozen eval version digests (`ai_registry.REGISTRY_VERSION == "2026-10-15.1"`, `assistants.VERSION == "1.0.0"`), disabled-by-default Bicep alert safety (`enableMonitoringAlerts = false`), Log Analytics privacy projection boundaries, and open governance blockers (`OD-51`, `OQ-017`, `OQ-018`) justifying `Refs #146`.
* Assessment boundary: Complete single-pass credibility audit of requirements, research claims, phases `P01` through `P03`, tasks `P01-T01` through `P03-T01`, acceptance criteria `AC-1` through `AC-5`, frozen-digest compatibility, release admission invariants, and Focused-tier validation gates.

## Coverage Assessment

| Area or ID | Coverage | Assessment |
| --- | --- | --- |
| `FR-1`, `AC-1`, `P01`, `P01-T01`, `P01-T02` (`C1`, `C2`, `C3`, `C4`, `C15`, `C20`) | Covered with minor validation-list gap | `job-rank` routing in `infra/modules/operationalMonitoring.bicep`, runbook anchor `### Job rank` in `infra/monitoring-runbooks.md`, and `CANDIDATE` ledger alignment in `src/core/src/zava_forward/core/monitoring_coverage.py` accurately close the rank-job collision while preserving parameter names, IoT tuples, disabled-by-default flags, and `GAP` invariants on `import-jobs-poison` and `rai-harm`. See `PC-004` for one omitted `#146` `infra/tests/` file in the `--line-length 100` `ruff` list. |
| `FR-2`, `AC-2`, `P01-T01`, `P01-T02` (`C5`, `C6`, `C7`, `C21`) | Covered | `infra/monitoring-workbook.json` already renders availability, errors, latency, cost-against-budget (`100 GBP`), and RAI panels; updating `status-and-boundary` to record `job-rank` routing and explicit task/release harm declarations while preserving live KQL drill and billing-export caveats is accurate and sufficient. |
| `FR-3`, `AC-3`, `AC-4`, `P02`, `P02-T01` (`C8`, `C9`, `C10`, `C16`, `C17`) | Substantive schema mismatch | The 13-task coverage strategy and preservation of `REGISTRY_VERSION` (`"2026-10-15.1"`) are sound, but `P02-T01` and `FR-3` specify field keys (`rationale`, `observation_window`, `manual_route`), a `threshold` shape without `min_sample`, dot-delimited missing tokens, title-case statuses (`"Declared"`/`"Blocked"`), and tuple-only `effort_stages` that conflict directly with `monitoring_coverage.check_monitoring_declaration`, `evaluate_indicator`, and JSON persistence (`PC-001`). |
| `FR-4`, `AC-3`, `AC-4`, `P02`, `P02-T02`, `P02-T03` (`C10`, `C11`, `C12`, `C18`, `C19`) | Substantive contract and target gaps | Guarding live threshold checks with `if live and "monitoring_declaration" in record:` correctly preserves `test_rai_threshold_live_approval_guard.py`, and keeping `assistants.VERSION` unchanged preserves `heldout_eval` digests. However, `P02-T02`/`P02-T03` omit `src/core/tests/test_rai_release.py` (which builds standalone dicts without `release_support.fixture` and fails when `missing_contract` requires `monitoring_declaration`), risk a circular import between `rai_release.py` and `monitoring_coverage.py` (`PC-002`), and misname `Assistants.registry` as `assistants.Service.registry` while overlooking its separate disabled-task branch (`PC-003`). |
| `NFR-1`, `NFR-2`, `AC-5`, `P03`, `P03-T01` (`C13`, `C14`, `C16`, `C17`) | Covered with minor command hygiene gap | Focused-tier selection, privacy constraints, frozen version guards, and `Refs #146` commit traceability match caller decisions; `P03-T01` needs `infra/tests/test_diagnostic_log_privacy.py` added to the `#146` `infra/` `ruff` check and a workspace-safe Python environment instruction (`PC-004`). |

## Verdict

* Verdict: Revise
* Rationale: The architectural split across `P01` through `P03`, alert-routing correction for `job-rank`, frozen-digest preservation, and `Refs #146` governance framing are well-grounded, but two High-severity specification mismatches in `P02` (`PC-001` schema/token conflicts with `monitoring_coverage.py` and `PC-002` unaccounted `src/core/tests/test_rai_release.py` breakage plus circular import risk) and two Medium/Low precision gaps (`PC-003`, `PC-004`) would cause implementation test failures if executed literally. Every finding is a direct planner correction requiring zero divergent user decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: P02-T01 and FR-3 field keys, threshold shape, status casing, and JSON tuple handling conflict with monitoring_coverage.py

* Related IDs: `FR-3`, `AC-3`, `AC-4`, `P02`, `P02-T01`
* Evidence: `.copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md` (`FR-3`), `.copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md` (`P02-T01`), `src/core/src/zava_forward/core/monitoring_coverage.py` (lines 185, 199-208, 262, 275-330), `src/core/tests/test_monitoring_coverage.py` (lines 82, 340-385), `src/core/src/zava_forward/core/assistant_release.py` (lines 56, 200)
* Concern: `P02-T01` and `FR-3` diverge from the implemented `monitoring_coverage` contract in six places:
  1. `FR-3` specifies `status == "Declared"` and `status == "Blocked"`, whereas `monitoring_coverage.py` defines lowercase `DECLARED = "declared"` and `BLOCKED = "blocked"`.
  2. `P02-T01` specifies `rationale` for non-applicable indicators (`applicable: False`), whereas `check_monitoring_declaration` (line 306) checks `entry.get("reason")` and reports `"indicator:<name>:inapplicability_reason"` when `reason` is absent.
  3. `P02-T01` specifies `observation_window`, whereas `check_monitoring_declaration` (line 310) checks `entry.get("window")`.
  4. `P02-T01` specifies `manual_route` for disabled tasks, whereas `check_monitoring_declaration` (lines 276, 296) requires non-empty `manual_route_status` whenever `task_enabled=False`.
  5. `P02-T01` specifies `threshold: {"limit": <float>, "constructed": True}` without `"min_sample": <int >= 0>` and describes `denominator` without stating it must be a positive `int` (`_count(entry.get("denominator")) > 0` at line 308); omitting `min_sample` causes `evaluate_indicator` (lines 199-208) to return `"blocked"`. In addition, `check_monitoring_declaration` emits colon-delimited missing entries such as `"indicator:challenges:threshold"` (locked by `test_monitoring_coverage.py` line 362), whereas `P02-T01` proposes dot-delimited `<name>.threshold.approved_by` and `<name>.threshold.live_approval`.
  6. `P02-T01` specifies `effort_stages` on `complete_review_effort` as a Python tuple `("preparation", "review", "correction", "re_review")`, whereas `assistant_release.record` serializes records through `json.dumps` and `assistant_release.releases` reloads them via `json.loads`, turning tuples into `list` instances.
* Impact: Implementing `P02-T01` as written causes `check_monitoring_declaration` to return `"blocked"` across all 13 `ai_registry` tasks (breaking `ai_registry.is_registered`), breaks `test_unapproved_live_threshold_and_missing_denominator_block` in `src/core/tests/test_monitoring_coverage.py` if `"indicator:<name>:threshold"` is replaced by dot-delimited keys, and fails `rai_release.missing_contract` after JSON round-trip in `assistant_release.releases` if `effort_stages` only accepts a `tuple`.
* Smallest useful change: Revise `FR-3` and `P02-T01` so `task_declaration(task_id)` and `check_monitoring_declaration` use the canonical schema: lowercase `"declared"` and `"blocked"` statuses; top-level `manual_route_status` (plus optional `manual_route` context) for disabled tasks; per-indicator `reason` when `applicable` is `False`; positive integer `denominator` (with optional `denominator_basis` string if unit prose is also kept), `window` (`"P7D"` or `"P28D"`), and `threshold: {"limit": <float>, "min_sample": <int>, "constructed": True}`; colon-delimited `indicator:<name>:...` missing tokens that preserve `"indicator:<name>:threshold"` when live approval fails; and `list(REVIEW_EFFORT_STAGES)` storage validated as a non-string sequence where `tuple(stages) == REVIEW_EFFORT_STAGES`.
* Action owner: planning parent
* Exact resolving evidence: Updated `FR-3` in `.copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md` and `P02-T01` in `.copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md` specifying `reason`, `window`, integer `denominator`, `threshold.min_sample`, `manual_route_status`, colon-delimited `indicator:<name>:...` missing tokens, lowercase `"declared"`/`"blocked"`, and sequence-safe `effort_stages`.
* Decision route: direct planner correction; no divergent user decision required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: P02-T02 and P02-T03 omit src/core/tests/test_rai_release.py breakage and circular import risk between rai_release.py and monitoring_coverage.py

* Related IDs: `FR-4`, `NFR-2`, `AC-3`, `AC-4`, `AC-5`, `P02`, `P02-T02`, `P02-T03`
* Evidence: `src/core/tests/test_rai_release.py` (lines 7, 17-87), `src/core/src/zava_forward/core/rai_release.py` (lines 1-90, 206-246), `src/core/src/zava_forward/core/monitoring_coverage.py` (line 18), `.copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md` (`Test Ownership and Validation Lock`, `P02-T02`, `P02-T03`), `.copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md` (`P02-T02`, `P02-T03`)
* Concern: Two coupled `rai_release` issues are unaddressed in `P02-T02` and `P02-T03`:
  1. `src/core/tests/test_rai_release.py` (`ReleaseContract.setUp`) constructs hardcoded `self.task` and `self.record` dicts directly rather than calling `release_support.fixture`, asserts `self.select(self.record) == []`, and in `test_complete_fixture_matches_but_is_not_actual_authorization` (lines 59-66) sets `self.record["evidence_class"] = "actual"` and asserts `self.select(self.record, live=True) == []`. Once `rai_release.missing_contract` requires `monitoring_declaration` and `rai_release.missing_binding(..., live=True)` enforces named-human live threshold approval, `src/core/tests/test_rai_release.py` fails unless updated in `P02-T03`.
  2. `monitoring_coverage.py` line 18 executes `from zava_forward.core.rai_release import named` at module import time. When a caller imports `rai_release` before `monitoring_coverage` (as `src/core/tests/test_rai_release.py` line 7 does), a top-level `from zava_forward.core import monitoring_coverage` at the top of `rai_release.py` triggers a circular `ImportError` before `named` is defined.
* Impact: `src/core` unit test discovery fails with `ImportError` or `AssertionError` in `src/core/tests/test_rai_release.py`.
* Smallest useful change: Add `src/core/tests/test_rai_release.py` to `Test Ownership and Validation Lock` and `P02-T03` (adding a valid `monitoring_declaration` to `ReleaseContract.setUp`, stamping named-human live threshold approval in `test_complete_fixture_matches_but_is_not_actual_authorization` after asserting constructed-threshold rejection, and adding `"monitoring_declaration"` to `test_every_required_contract_field_fails_closed_when_missing`), and specify a cycle-safe import in `P02-T02` (lazy function-local import of `monitoring_coverage` inside `rai_release.missing_contract` and `rai_release.missing_binding`, or placing the import after `named` and `named_human` definitions).
* Action owner: planning parent
* Exact resolving evidence: Updated `Test Ownership and Validation Lock`, `P02-T02`, and `P02-T03` in `.copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md` and `.copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md` covering `src/core/tests/test_rai_release.py` and cycle-safe `rai_release` / `monitoring_coverage` imports.
* Decision route: direct planner correction; no divergent user decision required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: P02-T02 misidentifies Assistants.registry as assistants.Service.registry and misses the early-continue disabled-task branch

* Related IDs: `FR-3`, `AC-3`, `P02`, `P02-T02`
* Evidence: `src/core/src/zava_forward/core/assistants.py` (lines 1031, 1528, 1554-1596), `.copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md` (`In Scope`, `P02-T02`), `.copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md` (`P02`, `P02-T02`)
* Concern: `assistants.py` defines `class Assistants` (no `Service` class exists), and `Assistants.registry(self, user)` appends entries to `registered` in two separate branches: an early-`continue` branch for `spec.get("enabled") is False` (`chat-case-conversation` and `aftercare-concern-pack`, lines 1557-1571) and a second branch for enabled tasks (lines 1588-1596). Describing a single `assistants.Service.registry` entry risks omitting `monitoring_status` on disabled tasks where `task_enabled=False` and `manual_route_status` verification apply.
* Impact: Implementer target ambiguity and incomplete `monitoring_status` reporting for the 2 disabled tasks (`chat-case-conversation`, `aftercare-concern-pack`) in `Assistants.registry()["registered_tasks"]`.
* Smallest useful change: Update `In Scope`, `P02`, and `P02-T02` to name `Assistants.registry` in `src/core/src/zava_forward/core/assistants.py` and require attaching `monitoring_status` in both `registered.append(...)` branches (`task_enabled=False, live=False` on the disabled branch, and `(selected or spec).get("monitoring_declaration")` with `task_enabled=True` and the branch's `live` flag on the enabled branch).
* Action owner: planning parent
* Exact resolving evidence: Updated `In Scope`, `P02`, and `P02-T02` in `.copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md` and `.copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md` referencing `Assistants.registry` and both disabled and enabled `registered_tasks` branches.
* Decision route: direct planner correction; no divergent user decision required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: P01-T02 and P03-T01 omit infra/tests/test_diagnostic_log_privacy.py from 100-column ruff checks and hardcode an external temporary venv path

* Related IDs: `FR-1`, `NFR-2`, `AC-1`, `AC-5`, `P01-T02`, `P03-T01`
* Evidence: `infra/tests/test_diagnostic_log_privacy.py` (line 1 `Issue 146 criterion 4`, lines 88-90), `infra/tests/test_alert_runbook_signal_matrix.py` (lines 169-184), `.copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md` (`NFR-2`, `Dependencies`, `P01-T02`, `P03-T01`), `.copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md` (`P01-T02`, `P03`, `P03-T01`)
* Concern: First, `infra/tests/test_diagnostic_log_privacy.py` is an Issue #146 monitoring test (`Issue 146 criterion 4`) whose lines 88-90 wrap at 88 columns and fail `ruff format --isolated --line-length 100 --check` when all `#146` `infra/` monitoring files are checked; additionally, `test_poison_ledger_job_and_iot_signals_are_covered` in `infra/tests/test_alert_runbook_signal_matrix.py` (lines 171-181) enumerates explicit `job-*` runbook sections (`job-orchestrator`, `job-ledger`, `job-import`, `job-auth`) where `job-rank` should also be asserted alongside `MATRIX["alert-${jobName}-failed"]`. Second, `P03-T01` hardcodes creating a temporary virtualenv outside the workspace root, which violates workspace-only file-creation constraints when an isolated venv is needed.
* Impact: `ruff format --isolated --line-length 100 --check` on `infra/` `#146` targets will fail if `infra/tests/test_diagnostic_log_privacy.py` is included in gate checks, and `P03-T01` environment bootstrapping will conflict with workspace-only write rules unless kept in the active Python environment or a cleaned-up workspace-local `.venv` directory.
* Smallest useful change: Add `infra/tests/test_diagnostic_log_privacy.py` to the `#146` `infra/tests/` `ruff` check/format list in `P01-T02` and `P03-T01` (reformatting lines 88-90 to 100-column style only if needed), include `"job-rank"` in `test_poison_ledger_job_and_iot_signals_are_covered` in `P01-T02`, and update `P03-T01`, `NFR-2`, and `Dependencies` to reuse installed packages or create and remove a workspace-local virtualenv before `git status` and commit.
* Action owner: planning parent
* Exact resolving evidence: Updated `NFR-2`, `Dependencies`, `P01-T02`, and `P03-T01` in `.copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md` and `.copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md`.
* Decision route: direct planner correction; no divergent user decision required.

## Strengths and Residual Risk

* Strengths:
  * The root-cause diagnosis and 3-way reconciliation of the `job-rank` / `job-rank-publish` substring collision (`operationalMonitoring.bicep`, `monitoring-runbooks.md`, and `monitoring_coverage.ALERTS`) cleanly resolves silent misrouting to `job-orchestrator` without altering Bicep parameter signatures, IoT metric tuples, disabled-by-default flags, or locked `GAP` entries (`import-jobs-poison`, `rai-harm`).
  * Keeping `ai_registry.REGISTRY_VERSION` (`"2026-10-15.1"`) and `assistants.VERSION` (`"1.0.0"`) unchanged avoids breaking `heldout_eval.FROZEN_VERSIONS`, `FROZEN_CAPABILITY_VERSIONS`, `FROZEN_THRESHOLDS_DIGEST`, and `FROZEN_MANIFEST_DIGEST`.
  * Guarding live threshold checks in `rai_release.missing_binding` with `if live and "monitoring_declaration" in record:` preserves `test_rai_threshold_live_approval_guard.py` while `rai_release.missing_contract` enforces declaration presence on full release admission (`rai_release.select` and `assistant_release.record`).
  * `task_contract_version = digest(ai_registry.get(...))` is already included in `rai_release.TRIGGER_KEYS["evidence"]`, so task-level `monitoring_declaration` changes automatically trigger active-release invalidation without altering `TRIGGER_KEYS`.
* Accepted residual risks:
  * Named human monitoring/incident ownership (`OD-51`), live workspace alert drills (`OQ-017`, `OQ-018`), Azure Cost Management billing export wiring, and producer code for `import-jobs-poison` remain external operational/governance dependencies; the plan appropriately keeps `import-jobs-poison` and `rai-harm` at `GAP`, keeps constructed default thresholds blocked when `live=True` without named-human approval, and links the commit with `Refs #146` rather than a closing keyword.

## Questions or Blocking Evidence Gaps

* None. All evidence required to revise the plan and proceed directly to implementation is present in the repository and research artifact.

## Limitations

* This critique audited code, Bicep modules, JSON workbook templates, Markdown runbooks, and unit tests statically inside the worktree without mutating files or running live Azure deployments or live Log Analytics KQL queries.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: planning parent
* Smallest next action: Apply direct planner revisions `PC-001` through `PC-004` to `.copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md` and `.copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md` (aligning `P02-T01` and `FR-3` to exact `monitoring_coverage.py` keys/types/tokens, adding `src/core/tests/test_rai_release.py` and cycle-safe imports to `P02-T02`/`P02-T03`, naming both `Assistants.registry` branches, and adding `infra/tests/test_diagnostic_log_privacy.py` plus workspace-local venv hygiene to `P01-T02`/`P03-T01`), then finalize planning without a second critique pass and continue directly into `rpi-implement`.
* User response required: no
