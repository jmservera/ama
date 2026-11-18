<!-- markdownlint-disable-file -->
# RPI Changes: Epic #218 Responsible AI Release, Challenge and Incident Control

## Metadata

* Task ID: issue-218-rai-release-discipline
* Related plan: .copilot-tracking/plans/2026-11-15/rai-218-release-discipline-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/rai-218-release-discipline-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01` through `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02`
* All remaining active-plan markers: none
* Status basis: Completed all planned core control-plane (`P01`), API readiness forwarding and documentation (`P02`), and focused unit tests plus validation (`P03`) markers with passing `unittest`, strict `mypy`, `ruff check`, and `ruff format --check` across `src/core` and `src/api`.

## Execution Summary

Implemented `src/core/src/zava_forward/core/rai_control_plane.py` and integrated deterministic `OQ-017` live named-approval gating (`approved_by` and `named_approval_id`), rollback-safe rejection audit emission (`rai_live_activation_rejected` + SQL `live-activation-rejected`), 15-requirement AST-verified traceability (`FR-051`..`FR-054`, `NFR-014`, `AC-069`..`AC-073`, `OQ-017`..`OQ-019`, `RULE-024`, `RULE-020`), and separated `rai_exercise_acceptance` vs `real_ai_delivery_gate` readiness reporting across `src/core` and `src/api`.

## Completed Work

### Core RAI Control Plane (`P01`, `P01-T01`, `P01-T02`)

* Created `src/core/src/zava_forward/core/rai_control_plane.py` with `LiveActivationApprovalError` (`OQ-017`), `valid_named_human_approver` (including CI/pipeline/system/placeholder rejection), `valid_named_approval_id`, `validate_live_task_approval`, `activate_live_task`, rollback-safe `_persist_audit_immediately` (`SqlStore._audit_immediate` 5-tuple and JSON `Store.audit` under `store.lock`), `REQUIREMENT_TRACEABILITY` (all 15 IDs), MRO-aware AST `verify_traceability_targets`, `traceability_summary`, and strictly read-only `exercise_acceptance_report`.
* Integrated `rai_control_plane` across `rai_release.py`, `assistant_release.py`, `assistants.py`, `ai_tasks.py`, `governance.py`, `store.py`, and `src/core/tests/release_support.py`.
* Local judgment fix during validation: replaced `store.paused_scopes()` inside `exercise_acceptance_report` with strictly read-only inspection of `store.data.get("governance", {}).get("breaches", ())` so read-only `governance_view()` calls never initialize `store.data["governance"]` in place (`test_governance.EvidenceRegister.test_inventory`).

### API Readiness Payloads and Documentation (`P02`, `P02-T01`)

* Wired `assistants_service=app.assistants` into `/api/governance` (both default and `?assessment=...` query paths) and `/api/ai/report` in `src/api/src/zava_forward/api/server.py`, preserving the exact 5 top-level keys on `GET /api/ai/report` and existing route/export inventories.
* Updated `src/core/README.md` and `src/api/README.md` with Epic `#218` control-plane, traceability, and separated readiness documentation.

### Focused Unit Tests and Package Validation (`P03`, `P03-T01`, `P03-T02`)

* Added `src/core/tests/test_rai_control_plane_218.py` (5 focused test methods) covering `OQ-017` rejection + rollback-safe JSON/SQL audit persistence, valid named-human activation + `rai_release.missing_binding` compatibility, all 15 requirement traceability IDs + fail-closed AST verification, and `rai_exercise_acceptance` vs `real_ai_delivery_gate` independence across offline, `ZF_AI=off`, unapproved-SQL, and named-human-approved states.
* Added `src/api/tests/test_rai_release_readiness_api_218.py` (3 focused HTTP test methods) covering `POST /api/assistants/releases` HTTP 403 `OQ-017` rejection with durable audit/event persistence, separated `rai_exercise_acceptance` vs `real_ai_delivery_gate` sections on `GET /api/assistants`, `GET /api/governance` (with and without `?assessment=...`), and `GET /api/ai/report` (`live`), manager RBAC 403 checks, and runtime `importlib` + `getattr` resolution of all traceability targets across `src/core/tests` and `src/api/tests`.

## Implementation-Time Plan and Detail Updates

None.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Focused `#218` unit tests | `src/core/tests/test_rai_control_plane_218.py` (5) and `src/api/tests/test_rai_release_readiness_api_218.py` (3) | Passed | 8/8 tests OK |
| Targeted RAI, governance, and release unit tests | `src/core` (13 modules, including all `REQUIREMENT_TRACEABILITY` core targets and `test_governance.py`) | Passed | 268 tests ran, OK (`skipped=16`) |
| Targeted RAI, release, contract, and route unit tests | `src/api` (26 modules covering all `REQUIREMENT_TRACEABILITY` API targets, `test_dependency_rule.py`, `test_heldout_eval_api.py`, `test_role_endpoint_inventory.py`, `test_list_export_inventory.py`, and every API test touching `/api/governance`, `/api/ai/report`, or `/api/assistants`) | Passed | 377 + 472 = 849 tests ran, OK (`skipped=202`) |
| `mypy` | `src/core` (`strict = true`) and `src/api` | Passed | `Success: no issues found in 357 source files` (`src/core`); `Success: no issues found in 298 source files` (`src/api`) |
| `ruff check` and `ruff format --check` | `src/core`, `src/api`, and `ruff format --isolated --line-length 100 --check` on new/non-excluded `#218` files | Passed | `All checks passed!`; `304 files already formatted` (`src/core`), `214 files already formatted` (`src/api`), `4 files already formatted` (isolated check) |
| `tools/rpi-checks.py` | Repository gate | Skipped | Explicitly excluded by caller focused-tier instruction |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02` all checked `[x]`)
* Completed-work evidence and handoff prose: Reconciled with workspace files and validation results
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining plan markers, `0` follow-up items)
* Review readiness: Ready

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/rai-218-release-discipline-plan.md, `## Follow-Up Items`
* None

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P03-T02`; remaining: none
* Validation coverage: Focused tier passed (`src/core` and `src/api` unit tests, `mypy`, `ruff check`, `ruff format --isolated --line-length 100 --check`; `tools/rpi-checks.py` skipped per caller instruction)
* Blockers: None
* Current plan and detail updates: None
* Planning and critique state: Ready (`PC-001` through `PC-005` resolved directly)
* Follow-up items: None
* Review readiness or no-handoff reason: Ready for single post-implementation `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
