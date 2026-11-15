---
title: "RPI Plan: Management Views AI Consumption Economics (Issue #100)"
description: "Implementation plan for Issue #100 AI consumption economics denominators and Unknown cost invariants across management views"
ms.date: 2026-11-15
---
<!-- markdownlint-disable-file -->

## Task Metadata

* Task ID: issue-100-mgmt-tokenomics
* Task slug: insight-100-mgmt-tokenomics
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/insight-100-mgmt-tokenomics-plan-critique.md

## Executive Summary

This plan delivers the unticked Tokenomics Acceptance Criterion of Issue `#100` (*Epic: Management insight, forecasting and evidence export*) by introducing a pure, deterministic core module (`src/core/src/zava_forward/core/tokenomics.py`) and surfacing a standardized `ai_consumption_economics` block across Zava Forward's management insight, progress, coordinator, and live AI report views. Management readers gain explicit integer denominators (`proposal_count`, `accepted_outcome_count`, `metered_call_count`, `unmetered_call_count`) alongside BRD Required Management Views fields (metered usage against limits, owned breach alerts, Total Cost of AI beside token/API cost, per-capability cost per accepted outcome beside the quality floor, and booked value), while every cost and cost-per-accepted-outcome field fails closed to `"Unknown"` (and never `0`, `0.0`, `"0"`, `"0.0"`, or `None`) whenever no approved price source (`price_source_configured=False` / BRD `OD-51` open) or no accepted outcome (`accepted_outcome_count == 0`) exists.

### User Decisions and Requirements Highlights

* Deliver the full automatic RPI loop (`research`, `plan`, `implement`, `review`) under `.copilot-tracking/.../2026-11-15/` on branch `feat/insight-100-mgmt-tokenomics` targeting `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) at the Focused validation tier, ending at a clean local commit without pushing.
* Include `ai_consumption_economics` with explicit denominators (`proposal_count`, `accepted_outcome_count`, `metered_call_count`, `unmetered_call_count`) in management views and guarantee `"Unknown"` (never `0` or `0.0`) whenever no price source or no accepted-outcome count exists.
* Add dedicated invariant tests in `src/core/tests/test_management_tokenomics_invariant_100.py` and `src/api/tests/test_management_tokenomics_api_100.py`, update component documentation (`src/core/README.md` and `src/api/README.md`), and pass `ruff check`, `mypy`, and `unittest`.

### What You May Not Know

* Existing API tests enforce exact top-level keys `{"evaluation", "chat_evaluation", "live", "registry", "consumption"}` on `GET /api/ai/report` and `None` on `Consumption.report()["cost_per_accepted_outcome"]["cost"]`. Preserving those exact shapes while placing `ai_consumption_economics` on `insights.stats` (`/api/stats`), `progress.report` (`/api/stats?report=progress` and `/api/cases.csv?report=progress`), `coordinator.read` (`/api/coordinator`), `api.progress.dashboard` (`/api/progress`), and `ai_tasks.live_report` (`/api/ai/report["live"]["ai_consumption_economics"]`) avoids regressions while covering all management views.
* Repeat-read determinism (`self.report() == baseline`), `progress.export_csv` JSON round-trip equality (`decoded == report`), read-only `_db_seq()` invariance, and privacy canary scans apply across `/api/stats`, `/api/progress`, and `/api/coordinator`. The new synthesis therefore avoids `datetime.now()`, performs zero database or audit writes, and emits only closed tokens, integer counts, booleans, Decimal strings, and `"Unknown"`.

### Unresolved Decisions or Blockers

* None. BRD `OD-51` remains intentionally `"open"` by default in runtime governance until the owner approves live pricing, spend ceilings, and alert owners; the implementation models `od_51_status="open"` (`price_source_configured=False`) by default and supports explicit priced/approved evaluation in tests and callers.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) writing dated artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`) under `2026-11-15/` for Issue `#100` (user prompt).
* Work in `/home/azureuser/source/ama-demo-wt/feat-100-mgmt-tokenomics` on branch `feat/insight-100-mgmt-tokenomics` targeting parent branch `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) under the Focused validation tier (user prompt).
* Prove the unticked Tokenomics Acceptance Criterion of Issue `#100`: management views include AI consumption economics (BRD Required Management Views) with explicit denominators (`proposal_count`, `accepted_outcome_count`, `metered_call_count`, `unmetered_call_count`), and show `"Unknown"`, not zero, where no price source (`price_source_configured=False` / `OD-51` open) or accepted-outcome count (`accepted_outcome_count == 0`) exists (user prompt; `docs/brds/agentic-retrofit-programme-brd.md` lines 863, 1388, 1720, 1769; `docs/prds/zava-forward-retrofit-programme-demonstrator.md` lines 664, 970).
* Add dedicated end-to-end invariant test `src/core/tests/test_management_tokenomics_invariant_100.py` and API coverage in `src/api/tests/` exercising management views with and without price source and accepted outcomes (user prompt).
* Update `src/core/README.md` for exported helpers, run `ruff check`, `mypy`, and `unittest` in `src/core` and `src/api`, and commit all code, tests, docs, and `.copilot-tracking/` artifacts locally with the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer without pushing (user prompt).

## Goals

* Provide a single, deterministic, strictly typed core synthesis (`zava_forward.core.tokenomics`) for BRD Required Management Views AI consumption economics across JSON, SQLite, and MSSQL stores.
* Surface `ai_consumption_economics` with explicit integer denominators across management insight, programme progress/forecast (JSON and CSV), coordinator, progress dashboard, and live AI report payloads.
* Enforce fail-closed `"Unknown"` semantics (never numeric `0` or `0.0` or string `"0"`/`"0.0"` or `None`) on cost and cost-per-accepted-outcome fields whenever price source authority/reconciliation is absent (`price_source_configured=False`, `OD-51` open, or unmetered gaps) or `accepted_outcome_count == 0`.
* Prove the invariant end-to-end across core and HTTP management views without breaking existing schema, determinism, CSV round-trip, read-only sequence, or privacy-canary tests.

## Scope and Non-Goals

### In Scope

* Creating `src/core/src/zava_forward/core/tokenomics.py` with `summarize_ai_consumption_economics`, `store_ai_consumption_economics`, and `assert_tokenomics_invariants`.
* Wiring `ai_consumption_economics` into `insights.stats`, `Store.stats`, `Store.ai_consumption_economics` (with opt-in default-open `tokenomics_governance` hook), `progress.report`, `Store.progress_report`, `coordinator.read`, `ai_tasks.live_report` / `Store.ai_live_report`, `zava_forward.api.progress.dashboard`, and optional explicit query-bound forwarding into `s.ai_live_report(u, ...)` in `zava_forward.api.server`.
* Adding `src/core/tests/test_management_tokenomics_invariant_100.py` and `src/api/tests/test_management_tokenomics_api_100.py` (exact test removals: `none`; maximum test file additions: `2`).
* Updating `src/core/README.md` and `src/api/README.md` to document the exported `tokenomics` module and management-view `ai_consumption_economics` contract.

### Non-Goals

* Closing BRD `OD-51` or inventing live commercial tariffs, spend ceilings, or finance-confirmed booked savings.
* Modifying `Consumption.report()`'s existing `cost_per_accepted_outcome` field contract or adding top-level keys to `GET /api/ai/report`.
* Modifying web UI HTML/CSS/JS assets under `src/api/src/zava_forward/api/web/`.
* Pushing commits to the remote repository or opening/mutating a pull request.

## Functional Requirements

* FR-1: `zava_forward.core.tokenomics` synthesizes an `ai_consumption_economics` dictionary containing explicit non-negative integer denominators `proposal_count`, `accepted_outcome_count`, `metered_call_count`, and `unmetered_call_count` both at top level and under `denominators` (alongside `unreviewed_proposal_count`, `rejected_or_withdrawn_count`, `workflow_only_excluded_count`, and `basis`).
  * Observable acceptance criteria: Every management view's `ai_consumption_economics` block exposes all four explicit integer denominators (`isinstance(v, int) and not isinstance(v, bool) and v >= 0`) reconciled across ledger roots and store recommendations without double-counting metered roots or counting workflow fallbacks/unreviewed/rejected/held outputs as accepted AI outcomes.
* FR-2: `ai_consumption_economics` includes BRD Required Management Views companions: `od_51_status`, `price_source_configured`, `price_source`, `currency`, `metered_usage` (usage against limits, retries, failures, limit status, breach counts, content-free owned alerts), `token_cost`, `other_tca_components`, `total_cost_of_ai`, `cost_per_accepted_outcome`, `token_cost_per_accepted_outcome`, `quality_floor_status`, `quality_qualified_cost_per_accepted_outcome`, `booked_value`, `by_capability`, and `non_benefit_notice`.
  * Observable acceptance criteria: Core and HTTP management views (`GET /api/stats`, `GET /api/stats?report=progress`, `GET /api/cases.csv?report=progress`, `GET /api/progress`, `GET /api/coordinator`, and `GET /api/ai/report["live"]`) include the complete `ai_consumption_economics` structure and round-trip cleanly through `progress.export_csv`.
* FR-3: Fail-closed `"Unknown"` pricing and zero-denominator protection governs all cost and unit-cost fields.
  * Observable acceptance criteria: Whenever `price_source_configured` is `False` (default while `od_51_status == "open"`, when dated price or reconciled billing is missing, or when `unmetered_call_count > 0` or ledger gaps exist), `token_cost`, `total_cost_of_ai`, `cost_per_accepted_outcome`, `token_cost_per_accepted_outcome`, `quality_qualified_cost_per_accepted_outcome`, `booked_value` (unless finance-confirmed), and per-capability cost fields equal `"Unknown"`. Whenever `accepted_outcome_count == 0` (even when `price_source_configured` is `True`), all cost-per-accepted-outcome fields (and any zero-billed unattributed cost field) equal `"Unknown"` and never `0`, `0.0`, `"0"`, `"0.0"`, or `None`. When `price_source_configured` is `True`, `od_51_status == "approved"`, `unmetered_call_count == 0`, reconciled positive billing exists, and `accepted_outcome_count > 0`, Decimal string ratios are computed accurately and gated by `quality_floor_status == "Pass"` and complete `other_tca_components`.

## Non-Functional Requirements

* NFR-1: Deterministic, side-effect-free read synthesis.
  * Objective threshold or evaluation condition: Two identical calls to `Store.stats()`, `Store.progress_report()`, `coordinator.read()`, or `api.progress.dashboard()` return identical payloads and leave `store._db_seq()` and the hash-chained audit log unchanged.
  * Operating condition or verification approach, if needed: Verified via repeat-read assertions, CSV round-trip checks, and `_db_seq()` checks in `unittest`.
  * Observable acceptance criteria: `test_progress_dashboard.py`, `test_progress_report_api.py`, `test_coordinator_api.py`, and new invariant tests pass with 0 mutations during read calls.
* NFR-2: Content-free projection and strict static typing.
  * Objective threshold or evaluation condition: Zero private case text, reviewer prose, or actor email addresses appear in `ai_consumption_economics`; `ruff check` and `mypy` pass with zero errors in `src/core` and `src/api`.
  * Operating condition or verification approach, if needed: Verified via canary substring assertions in HTTP tests and bare `python3 -m mypy` / `python3 -m ruff check`.
  * Observable acceptance criteria: All canary checks, `ruff check`, `mypy`, and `unittest` suites in `src/core` and `src/api` exit `0`.

## Acceptance Criteria

* `src/core/src/zava_forward/core/tokenomics.py` exists, is strictly typed, and computes `ai_consumption_economics` with explicit integer denominators (`proposal_count`, `accepted_outcome_count`, `metered_call_count`, `unmetered_call_count`) and BRD Required Management Views fields.
* Management views (`Store.stats` / `GET /api/stats`, `Store.progress_report` / `GET /api/stats?report=progress` and `GET /api/cases.csv?report=progress`, `coordinator.read` / `GET /api/coordinator`, `api.progress.dashboard` / `GET /api/progress`, and `Store.ai_live_report` / `GET /api/ai/report["live"]`) expose `ai_consumption_economics`.
* Whenever `price_source_configured=False` (`OD-51` open, missing dated price/reconciled bill, or unmetered calls) or `accepted_outcome_count == 0`, cost / cost-per-accepted-outcome fields explicitly report `"Unknown"` and never `0`, `0.0`, `"0"`, `"0.0"`, or `None`.
* `src/core/tests/test_management_tokenomics_invariant_100.py` and `src/api/tests/test_management_tokenomics_api_100.py` pass alongside all existing `src/core` and `src/api` unit/regression suites, `ruff check`, and `mypy`.
* `src/core/README.md` and `src/api/README.md` document the new helper and management-view payload contract.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/insight-100-mgmt-tokenomics-plan.md                                                                   |
| Phase details                    | .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md                                                        |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/insight-100-mgmt-tokenomics-plan-critique.md with Revise verdict; PC-001 through PC-005 resolved in plan and details |
| Relevant research                | .copilot-tracking/research/2026-11-15/insight-100-mgmt-tokenomics-research.md                                                            |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-changes.md is created by implementation as its evidence record          |
| Planning execution and readiness | Complete; Ready for implementation                                                                                                       |
| Continuation context             | Active confirmed automatic RPI Agent parent continues to Implement after all planning gates pass                                         |

## Sources

* `.copilot-tracking/research/2026-11-15/insight-100-mgmt-tokenomics-research.md`: Primary codebase and specification evidence (`C1` through `C20`), contrarian test constraints, and convergence design.
* `docs/brds/agentic-retrofit-programme-brd.md`: Normative requirements `FR-052`, `NFR-012`, `OD-51`, and Required Management Views.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: Demonstrator requirements `FR-061` and `NFR-017` for explicit denominators and `"Unknown"` unpriced/zero-outcome reporting.
* `docs/reference/resources/ai-tokenomics.md`: Total Cost of AI component taxonomy, quality-floor qualification, and anti-gaming rules.
* `src/core/src/zava_forward/core/ai_consumption.py`, `insights.py`, `progress.py`, `coordinator.py`, `ai_tasks.py`, `store.py`, and `src/api/src/zava_forward/api/progress.py`, `server.py`: Existing ledger and management view implementations.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core AI Consumption Economics Synthesis (`tokenomics.py`)

* Intent: Create a pure, deterministic, `mypy`-clean core module synthesizing `ai_consumption_economics` with explicit denominators and fail-closed `"Unknown"` cost invariants.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement `src/core/src/zava_forward/core/tokenomics.py`

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-1, NFR-2 (`C1`-`C8`, `C16`-`C20`)
* Expected result: `tokenomics.py` exports `UNKNOWN`, `SCHEMA`, `summarize_ai_consumption_economics(...)`, `store_ai_consumption_economics(store, ...)`, and `assert_tokenomics_invariants(summary)` supporting both recommendation-only (`Store`) and ledger-backed (`SqlStore`/`Consumption`) stores without mutating state or emitting `0`/`0.0` for unpriced or zero-outcome costs.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Wire `ai_consumption_economics` Across Core and API Management Views

* Intent: Surface `ai_consumption_economics` across every management insight, progress/forecast, coordinator, progress dashboard, and live AI report view while preserving backward-compatible contracts.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Wire `ai_consumption_economics` into `insights`, `progress`, `coordinator`, `ai_tasks`, and `Store`

* Requirement and evidence: FR-1, FR-2, NFR-1, NFR-2 (`C9`, `C10`, `C11`, `C13`, `C15`, `C19`, `C20`)
* Expected result: `Store.ai_consumption_economics(...)`, `insights.stats(...)` / `Store.stats()`, `progress.report(...)` / `Store.progress_report(...)` (including `progress.export_csv` round-trip), `coordinator.read(...)`, and `ai_tasks.live_report(...)` / `Store.ai_live_report(...)` include deterministic `ai_consumption_economics`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Wire `ai_consumption_economics` into `zava_forward.api.progress.dashboard` and `server.py` `/api/ai/report` query bounds

* Requirement and evidence: FR-2, NFR-1, NFR-2 (`C12`, `C14`, `C16`, `C17`, `C18`)
* Expected result: `GET /api/progress` exposes deterministic synthetic-admitted `ai_consumption_economics` scoped to `[start, end + 1 day)` using stored `created`/`resolved_at` timestamps without `datetime.now()`, while `GET /api/ai/report` preserves its exact 5 top-level keys and forwards optional explicit `start`/`end`/`as_of` query parameters to `s.ai_live_report(u, ...)`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: End-to-End Invariant and API Regression Tests

* Intent: Prove explicit denominators and `"Unknown"` (never `0` or `0.0`) invariants across unpriced, zero-accepted-outcome, priced-with-accepted-outcomes, and unmetered-gap scenarios in both `src/core` and `src/api`.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Create `src/core/tests/test_management_tokenomics_invariant_100.py`

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-1 (`C1`-`C11`, `C19`)
* Expected result: Dedicated core invariant test suite passes across JSON `Store`, `SqlStore` + `Assistants`/`Consumption`, `insights.stats`, `progress.report` + `export_csv`, `coordinator.read`, and `ai_live_report` across all pricing (`OD-51` open vs approved/reconciled) and outcome (`accepted_outcome_count == 0` vs `> 0`, workflow fallback exclusion, unmetered call poisoning) combinations.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Create `src/api/tests/test_management_tokenomics_api_100.py`

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-1, NFR-2 (`C12`-`C20`)
* Expected result: Dedicated API test suite exercises `GET /api/stats`, `GET /api/stats?report=progress`, `GET /api/cases.csv?report=progress`, `GET /api/progress`, `GET /api/coordinator`, and `GET /api/ai/report` with and without price source and accepted outcomes, verifying denominators, `"Unknown"` cost invariants, repeat-read determinism, `_db_seq()` invariance, and zero private canary leakage.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md

<!-- rpi:phase id=P04 -->
### [x] P04: Documentation Updates and Focused Validation Gate

* Intent: Document exported helpers and management-view tokenomics fields, and verify clean `ruff check`, `mypy`, and `unittest` execution across `src/core` and `src/api`.
* Dependencies: P01, P02, P03

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Update `src/core/README.md` and `src/api/README.md` and run `ruff`, `mypy`, and `unittest`

* Requirement and evidence: User prompt requirements 4 and 5; `.github/copilot-instructions.md` Focused validation tier
* Expected result: `src/core/README.md` and `src/api/README.md` document `tokenomics.py` and `ai_consumption_economics`; `python3 -m ruff check`, `python3 -m mypy`, and full `unittest` suites in `src/core` and `src/api` pass with zero errors.
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md

## Dependencies

* `zava_forward.core.ai_consumption`: Supplies `UNKNOWN`, `COMPONENTS`, `QUALITY`, `amount`, and `Consumption` ledger state on SQL stores.
* Existing management view contracts (`test_heldout_eval_api.py`, `test_ai_consumption_api.py`, `test_progress_dashboard.py`, `test_progress_report_api.py`, `test_coordinator_api.py`): Constrain top-level `/api/ai/report` keys, `Consumption.report()` shape, repeat-read determinism, CSV round-tripping, read-only DB sequence, and content-free privacy.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` (High: `DispatchHeld`, `port.sql` guard, read-only SQL connection) | resolved | Updated P01-T01 and P02-T01 to check `bool(getattr(port, "sql", False))` and `getattr(port, "schema_error", None) is None`, open a short-lived read-only `assistant_connection()` without `BEGIN IMMEDIATE` write-locking, and catch `(ai_consumption.DispatchHeld, ValueError, KeyError, TypeError, OSError, RuntimeError)` to fail closed to `price_source_configured=False` and `"Unknown"`. |
| `PC-002` (High: `coordinator.read` store wiring, opt-in governance hook, unbounded billing reconciliation, `server.py` bounds) | resolved | Updated P01-T01, P02-T01, P02-T02, P03-T02, and Test Ownership so `coordinator.read` passes `store.ai_consumption_economics(...)` into `progress.report(...)`, `Store` supports an opt-in default-absent `tokenomics_governance` config (`od_51_status="open"` by default), unbounded/half-bounded reads reconcile complete non-overlapping single-currency billing records covering all in-scope calls, and `server.py` forwards explicit `?start=&end=&as_of=` query bounds into `s.ai_live_report(u, ...)`. |
| `PC-003` (High: SHA-256 `reference(rec["id"])` output matching, `consumption_report`-only roots, publish-held fallbacks, `eligible=False`) | resolved | Updated P01-T01 to deduplicate recommendations via both `meter_root` and `ai_consumption.reference(rec["id"])`, treat valid 64-hex `meter_root` items as metered when `consumption_report` is supplied without `ledger_records`, count publish-held metered fallbacks (`source="template"` with `meter_root`) in `metered_call_count` (never `accepted_outcome_count` or `unmetered_call_count`), and exclude `eligible=False` ledger roots from `proposal_count` and `accepted_outcome_count`. |
| `PC-004` (Medium: `created`/`resolved_at` UTC normalization and synthetic admission in `api.progress.dashboard`) | resolved | Updated P02-T02 to normalize stored `created` (falling back to `resolved_at`, handling date-only `YYYY-MM-DD` and naive ISO strings as UTC) uniformly across `[start, end]` and enforce synthetic-record admission (`is_synthetic is True` and linked synthetic case IDs) matching `zava_forward.api.progress._ai`. |
| `PC-005` (Medium: per-capability cost attribution and `accepted_outcome_count == 0 -> "Unknown"` inside positive cohorts) | resolved | Updated P01-T01 and P03-T01 so each capability with `accepted_outcome_count == 0` strictly emits `"Unknown"` unit-cost fields even when overall `accepted_outcome_count > 0`, and multi-capability unallocated TCA/billing splits fail closed to `"Unknown"` unless single-capability or zero-variance call-charge attributable. |
| Residual risk: default runtime `OD-51` open | accepted with risk | BRD `OD-51` remains intentionally `"open"` in default runtime until owner approval of live tariffs and spend ceilings; default runtime views report `"Unknown"` costs by design while priced states are verified via explicit governance fixtures in P03. |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-changes.md
* Ready phase or task: P01 (`P01-T01` through `P04-T01`)
* Remaining provisional question or blocker: None
