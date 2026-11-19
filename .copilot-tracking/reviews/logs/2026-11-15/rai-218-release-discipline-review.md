<!-- markdownlint-disable-file -->
# Review: Epic #218 Responsible AI Release, Challenge and Incident Control

## Scope and Evidence

* Task ID: issue-218-rai-release-discipline
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Epic #218 acceptance criteria (`OQ-017` live activation named-approval rejection and audit emission, 15-requirement traceability table and AST verifier, and separated `rai_exercise_acceptance` vs `real_ai_delivery_gate` readiness reporting across `src/core` and `src/api`), critique dispositions `PC-001` through `PC-005`, and focused-tier validation.
* Plan: .copilot-tracking/plans/2026-11-15/rai-218-release-discipline-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/rai-218-release-discipline-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-15/rai-218-release-discipline-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/rai-218-release-discipline-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/rai-218-release-discipline-research.md; workspace Git diff across `src/core` and `src/api`; focused validation outputs (`unittest`, `mypy`, `ruff check`, `ruff format --check`).

## Opening Review State

* Interpreted review goal: Verify once with read-only evidence comparison that the completed Epic #218 implementation satisfies all planned requirements, acceptance criteria, critique dispositions (`PC-001` through `PC-005`), and focused-tier validation constraints without material defects or unrecorded divergences.
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02`)
* Evidence readiness: Ready (plan, phase details, plan critique, changes log, research artifact, and workspace diff are present and reconciled)
* Acceptance basis: Issue #218 caller acceptance criteria (`AC-PLAN-01` through `AC-PLAN-05`), requirements (`FR-PLAN-01`..`FR-PLAN-03`, `NFR-PLAN-01`..`NFR-PLAN-02`), and critique dispositions (`PC-001`..`PC-005`)
* First comparison boundary: Reconcile plan markers and critique dispositions against `.copilot-tracking/changes/2026-11-15/rai-218-release-discipline-changes.md` and workspace source/test diffs before grading findings and outcome
* Active read-only boundaries: Review may update only `.copilot-tracking/reviews/logs/2026-11-15/rai-218-release-discipline-review.md` and has zero write authority over production files, tests, research, plan, details, critique, or changes artifacts
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed on 2026-11-15 across the full task boundary (`P01`, `P02`, `P03`) by comparing `.copilot-tracking/plans/2026-11-15/rai-218-release-discipline-plan.md`, `.copilot-tracking/details/2026-11-15/rai-218-release-discipline-phase-details.md`, `.copilot-tracking/reviews/2026-11-15/rai-218-release-discipline-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/rai-218-release-discipline-changes.md`, the workspace Git diff, focused validation runs, and an independent read-only review lens.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01`, `P01-T02` | Core RAI Control Plane (`P01`, `P01-T01`, `P01-T02`) | Reconciled | Plan markers `[x]` match created `rai_control_plane.py` and wired core modules; two runtime edge-case defects (`RV-001`, `RV-002`) identified below |
| `P02`, `P02-T01` | API Readiness Payloads and Documentation (`P02`, `P02-T01`) | Reconciled | Plan markers `[x]` match `server.py` forwarding on `/api/governance` (default and `?assessment=...`) and `/api/ai/report`, plus `src/core/README.md` and `src/api/README.md` |
| `P03`, `P03-T01`, `P03-T02` | Focused Unit Tests and Package Validation (`P03`, `P03-T01`, `P03-T02`) | Reconciled | Plan markers `[x]` match new focused unit/API test files (`5` + `3` methods, within `<= 20` budget) and recorded `unittest`, `mypy`, `ruff check`, and `ruff format --check` runs |
| `## Follow-Up Items` | Follow-Up Items (`None`) | Reconciled | Both plan and changes record report no out-of-scope follow-up items prior to Review |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/rai_control_plane.py` | Created central RAI control plane for `OQ-017` live approval validation, immediate rollback-safe audit emission, 15-ID traceability + AST verification, and separated `rai_exercise_acceptance` / `real_ai_delivery_gate` readiness | Present in workspace; `PC-001`, `PC-004`, and `PC-005` satisfied | `test_rai_control_plane_218.py` (5/5 OK), strict `mypy` (0 issues), `ruff` clean | Gap in `_inspect_sql_live_releases` runtime binding check (`RV-002`) |
| `P01-T02` | `src/core/src/zava_forward/core/rai_release.py`, `assistant_release.py`, `assistants.py`, `ai_tasks.py`, `governance.py`, `store.py`, `src/core/tests/release_support.py` | Wired `OQ-017` live release recording gate, rollback-safe rejection auditing, and separated readiness sections across `Store` and `Assistants` | Present in workspace; `record_release` and `Store.activate_ai_task_live` reject and audit unapproved live activation | 268 `src/core` RAI/governance/release tests OK | Gap in `rai_release.missing_binding` partial-key check and `assistant_release.assessment(..., live=True)` dispatch-time `OQ-017` admission (`RV-001`) |
| `P02-T01` | `src/api/src/zava_forward/api/server.py`, `src/core/README.md`, `src/api/README.md` | Forwarded `assistants_service=app.assistants` into `/api/governance` (both query branches) and `/api/ai/report`, and documented Epic #218 contract | Present in workspace; preserves exact 5 top-level keys of `/api/ai/report` | 849 `src/api` tests OK; `test_live_doc_links.py` & `test_cutover_audit.py` (11/11 OK) | Reconciled |
| `P03-T01`, `P03-T02` | `src/core/tests/test_rai_control_plane_218.py`, `src/api/tests/test_rai_release_readiness_api_218.py` | Added focused core and HTTP API tests for Epic #218 and executed focused-tier package checks | 8 focused tests + package suites + `mypy` + `ruff` all exit 0 | Passed across `src/core` and `src/api` | Needs regression tests for `RV-001` and `RV-002` in routed follow-up |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` local judgment in `exercise_acceptance_report` | Read `store.data["governance"]["breaches"]` without calling `store.paused_scopes()` so read-only `governance_view()` never mutates `store.data` | `test_governance.EvidenceRegister.test_inventory` caught in-place `setdefault` side effect; no user decision needed | Recorded under Completed Work in `.copilot-tracking/changes/2026-11-15/rai-218-release-discipline-changes.md`; preserves approved read-only intent | Not needed (preserves `PC-002` read-only invariant) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All five critique findings (`PC-001` immediate SQL `_audit_immediate` persistence, `PC-002` read-only non-nested SQL inspection + `not self.sql` + `?assessment=...`, `PC-003` `monitoring_coverage.check_monitoring_declaration` + `legacy:` normalization + live-first `OQ-017` ordering, `PC-004` AST-based cross-package test target verification, and `PC-005` strict `mypy` annotations) have explicit dispositions in the plan and were verified in code.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No pause was required because no material or divergent user decision arose.
* Justification assessment: Local read-only breach inspection adjustment is fully supported by `test_governance.py` evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| None | No prior plan follow-up items were open entering Review | None | Resolved (none present) |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Live release binding admission fails open when `approved_by` or `named_approval_id` keys are omitted on stored or partial records

* Related scope: `P01-T02`
* Evidence: `src/core/src/zava_forward/core/rai_release.py` (`missing_binding`) gates `OQ-017` validation behind `if live and ("approved_by" in record or "named_approval_id" in record):` and repeats `"approved_by" in record` and `"named_approval_id" in record` independently on each field; `src/core/src/zava_forward/core/assistant_release.py` (`assessment`) relies solely on `rai_release.select(..., live=True)` without checking `approved_by` and `named_approval_id` when `live=True`.
* Impact: Supplying only one of `approved_by` or `named_approval_id` passes `rai_release.missing_binding(..., live=True)`, and a persisted pre-Epic-#218 `actual` SQL row in `assistant_releases` lacking `approved_by` or `named_approval_id` is admitted by `assistant_release.assessment(..., live=True)` at live dispatch time without `OQ-017` rejection.
* Destination: `rpi-implement`
* Smallest useful next action: Remove the inner key-presence guards in `rai_release.missing_binding` so supplying either `OQ-017` field requires both valid `approved_by` and `named_approval_id`, enforce both `valid_named_human_approver` and `valid_named_approval_id` unconditionally in `assistant_release.assessment(..., live=True)`, and add focused unit tests covering partial-key and stored-row live dispatch rejection.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: `_inspect_sql_live_releases` marks drifted or unattested SQL release rows as valid live releases without runtime-binding admission

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/rai_control_plane.py` (`_inspect_sql_live_releases`) checks raw stored fields on `assistant_releases` rows rather than calling `assistant_release.assessment(cursor_db, cap, binding, now_ts, live=True)` against the current `assistants.runtime_binding` / `ai_registry.legacy_binding` (and does not exclude `bool` from `isinstance(rec.get("expires"), (int, float))`).
* Impact: If an active `actual` SQL release row has drifted `prompt_version`, `model_version`, `policy_version`, `endpoint`, or `deployment`—or an `"unattested"` serving model—`real_ai_delivery_gate.checks.oq017_named_live_releases_recorded` reports the task in `approved_live_tasks` even though live runtime dispatch denies it.
* Destination: `rpi-implement`
* Smallest useful next action: Evaluate each enabled assistant and legacy task inside `with _assistant_release.read_only():` via `_assistant_release.assessment(cursor_db, cap, binding, now_ts, live=True)` using the current runtime/legacy binding (plus `OQ-017` named-approval verification), exclude `bool` expiries, and add a focused regression test for drifted/stale SQL rows.

## Defects

* `RV-001` [High] -> `rpi-implement`
* `RV-002` [Medium] -> `rpi-implement`

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Child follow-up task hardening `rai_release.missing_binding` and `assistant_release.assessment(..., live=True)` with regression tests | Implementation defect within approved `OQ-017` architecture |
| `RV-002` | `rpi-implement` | Child follow-up task updating `rai_control_plane._inspect_sql_live_releases` to call `assistant_release.assessment(..., live=True)` against current bindings | Implementation defect within approved separated-readiness architecture |

Later implementation of a routed finding does not require another Review.

## Residual Work

* None

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None inside `issue-218-rai-release-discipline` (`RV-001` and `RV-002` are routed to follow-up implementation)

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m unittest src/core/tests/test_rai_control_plane_218.py src/api/tests/test_rai_release_readiness_api_218.py` | Focused Epic #218 core and API tests | Passed | 5 core tests + 3 HTTP API tests OK |
| `python3 -m unittest` (13 `src/core` RAI/governance/release/doc-link modules + 26 `src/api` RAI/release/contract/route modules) | `src/core` and `src/api` regression & traceability targets | Passed | 268 + 11 `src/core` tests OK; 377 + 472 = 849 `src/api` tests OK |
| `python3 -m mypy` | `src/core` (`strict = true`) and `src/api` | Passed | 0 issues in 357 `src/core` files; 0 issues in 298 `src/api` files |
| `python3 -m ruff check .` and `python3 -m ruff format --check` (`--isolated --line-length 100` on new/non-excluded files) | `src/core` and `src/api` | Passed | All lint and format checks passed with exit code 0 |
| `python3 tools/rpi-checks.py` | Full repository gate | Skipped | Explicitly excluded by caller focused-tier instruction |

## Outcome

* Outcome: Defects found
* Outcome rationale: Planned tasks `P01-T01` through `P03-T02` executed completely and pass focused validation, proving deterministic `OQ-017` rejection on `record_release` / `activate_ai_task_live`, complete 15-ID AST-verified traceability, and separated `rai_exercise_acceptance` vs `real_ai_delivery_gate` payloads, while post-implementation review identified two concrete edge-case defects (`RV-001` dispatch-time/partial-key `OQ-017` admission and `RV-002` drifted-binding SQL readiness inspection) routed to follow-up implementation.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` | Close `RV-001` and `RV-002` in child follow-up task `rai-218-release-admission-hardening` |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | none | None |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: Focused tier passed across `src/core` and `src/api` (`unittest`, strict `mypy`, `ruff check`, `ruff format --check`); `tools/rpi-checks.py` skipped per caller instruction
* Blockers: None
