<!-- markdownlint-disable-file -->
# Review: Management Views AI Consumption Economics (Issue #100)

## Scope and Evidence

* Task ID: issue-100-mgmt-tokenomics
* Review date: 2026-11-15
* Review scope: Full task (`P01` through `P04`)
* Assessed boundary: Issue `#100` Tokenomics Acceptance Criterion (`ai_consumption_economics` summary across management views with explicit integer denominators and `"Unknown"`, never `0` or `0.0`, where no price source or accepted-outcome count exists), `PC-001` through `PC-005` critique dispositions, read-only store/DB invariance, synthetic data isolation, and Focused validation tier (`ruff check`, `mypy`, `unittest` in `src/core` and `src/api`).
* Plan: .copilot-tracking/plans/2026-11-15/insight-100-mgmt-tokenomics-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/insight-100-mgmt-tokenomics-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/insight-100-mgmt-tokenomics-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/insight-100-mgmt-tokenomics-research.md; `git diff` and new files in `src/core` and `src/api`; independent bounded review check.

## Opening Review State

* Interpreted review goal: Verify that completed full-plan implementation (`P01` through `P04`) satisfies Issue `#100`'s AI consumption economics acceptance criterion, resolves `PC-001` through `PC-005`, preserves read-only store/API contracts and synthetic privacy boundaries, and has passing Focused-tier validation evidence.
* Review scope: Full task (`P01`, `P01-T01`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`, `P04`, `P04-T01`)
* Evidence readiness: Ready (research, plan, phase details, plan critique, and reconciled changes record present)
* Acceptance basis: Plan FR-1 through FR-3, NFR-1 through NFR-3, AC-1 through AC-5, and critique dispositions `PC-001` through `PC-005`
* First comparison boundary: Plan-to-changes marker reconciliation and verification of `zava_forward.core.tokenomics` and management-view wiring against `AC-1` through `AC-5`
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/logs/2026-11-15/insight-100-mgmt-tokenomics-review.md` and does not mutate source files, plan, details, critique, research, or changes artifacts
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass post-implementation review on 2026-11-15 across full plan scope (`P01` through `P04`), comparing plan requirements (`FR-1` through `FR-3`, `NFR-1`, `NFR-2`), all five acceptance criteria, critique dispositions (`PC-001` through `PC-005`), implementation-time local updates, Focused-tier validation outputs, and an independent read-only review lens check.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01` | Core Tokenomics Synthesis and Invariant Module (`P01`, `P01-T01`) | Reconciled | Checked `[x]` in plan; `tokenomics.py` matches `FR-1` through `FR-3` and `PC-001` through `PC-005`. |
| `P02`, `P02-T01`, `P02-T02` | Management Views and HTTP Endpoints Wiring (`P02`, `P02-T01`, `P02-T02`) | Reconciled | Checked `[x]` in plan; `store.py`, `insights.py`, `progress.py`, `coordinator.py`, `ai_tasks.py`, `api/progress.py`, and `api/server.py` wired and verified. |
| `P03`, `P03-T01`, `P03-T02` | End-to-End Core Invariant and API Endpoint Tests (`P03`, `P03-T01`, `P03-T02`) | Reconciled | Checked `[x]` in plan; `test_management_tokenomics_invariant_100.py` (6 tests) and `test_management_tokenomics_api_100.py` (2 multi-endpoint HTTP tests) pass. |
| `P04`, `P04-T01` | Documentation and Focused Validation (`P04`, `P04-T01`) | Reconciled | Checked `[x]` in plan; `src/core/README.md` and `src/api/README.md` updated and `ruff`, `mypy`, and Focused `unittest` suites pass. |
| `Follow-Up Items` | `OD-51` tariff/spend governance approval and live Azure billing export reconciliation | Reconciled | Explicitly outside offline demonstrator code (`Refs #100`, `#108`, `#432`). |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01`, `P01-T01` | `src/core/src/zava_forward/core/tokenomics.py` | Added pure `Decimal`-based `ai-consumption-economics/v1` synthesis (`summarize_ai_consumption_economics`, `store_ai_consumption_economics`, `assert_tokenomics_invariants`) with explicit denominators and fail-closed `"Unknown"` pricing/unit-cost invariants. | Module present, strictly typed, enforces `OD-51`, reconciliation, unmetered poisoning, and `accepted_outcome_count == 0 -> "Unknown"` unit costs. | `ruff check`, `mypy` (355 files), `test_management_tokenomics_invariant_100.py` (6/6 passed). | Reconciled |
| `P02`, `P02-T01` | `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/insights.py`, `src/core/src/zava_forward/core/progress.py`, `src/core/src/zava_forward/core/coordinator.py`, `src/core/src/zava_forward/core/ai_tasks.py` | Added read-only `Store.ai_consumption_economics(...)` and wired `ai_consumption_economics` into `insights.stats`, `progress.report` (+ `export_csv`), `coordinator.read`, and `ai_tasks.live_report`. | All core management views emit `ai_consumption_economics` without mutating store or audit sequence. | `ruff check`, `mypy`, 177 focused core tests passed. | Reconciled |
| `P02`, `P02-T02` | `src/api/src/zava_forward/api/progress.py`, `src/api/src/zava_forward/api/server.py` | Added synthetic-admitted `_ai_economics` to `api.progress.dashboard` (`/api/progress`) without `datetime.now()` drift and forwarded optional `start`/`end`/`as_of` bounds to `s.ai_live_report(...)` on `GET /api/ai/report` while keeping its 5 top-level keys unchanged. | HTTP management views emit `ai_consumption_economics` with canary privacy isolation and repeat-read determinism. | `ruff check`, `mypy` (298 files), 250 focused API tests passed. | Reconciled |
| `P03`, `P03-T01` | `src/core/tests/test_management_tokenomics_invariant_100.py` | Added 6 invariant tests covering unpriced (`OD-51` open), priced with `accepted_outcome_count == 0`, priced with `accepted_outcome_count > 0` across TCA/quality/booked-value gates, unmetered call poisoning, and validator rejection of zero strings/numbers. | 6 unit/integration tests across `Store` and `SqlStore` + `Assistants`/`Consumption`. | `Ran 6 tests in 0.152s - OK`. | Reconciled |
| `P03`, `P03-T02` | `src/api/tests/test_management_tokenomics_api_100.py` | Added live `ThreadingHTTPServer` integration tests exercising `GET /api/stats`, `GET /api/stats?report=progress`, `GET /api/coordinator`, `GET /api/progress`, and `GET /api/ai/report` across JSON `Store` and `SqlStore` (`accepted_outcome_count == 0` vs `1`). | 2 multi-endpoint HTTP integration tests with zero `ResourceWarning`s under `-W error::ResourceWarning`. | `Ran 2 tests in 3.273s - OK`. | Reconciled |
| `P04`, `P04-T01` | `src/core/README.md`, `src/api/README.md` | Documented `zava_forward.core.tokenomics` and management-view `ai_consumption_economics` contracts (`2026-11-15, Refs #100`). | Dated sections added; link and cutover checks pass. | `test_live_doc_links.py` and `test_cutover_audit.py` (`Ran 11 tests - OK`). | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01`, `P02-T01` | Caught `(ValueError, OverflowError, OSError)` in `tokenomics.parse_record_timestamp(...)` and validated `progress.timestamp(...)` before `self.ai_consumption_economics(...)` in `Store.progress_report` so extreme out-of-range timezone strings (`0001-01-01T00:00:00+01:00`, `9999-12-31T23:59:59-01:00`) return HTTP `400` rather than `500`. | Surfaced by `test_progress_report_api.py::test_unrepresentable_utc_boundaries_are_explicit_400`; local judgment preserving approved error-handling contract (no user decision needed). | Recorded in `.copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-changes.md` under `## Implementation-Time Plan and Detail Updates` and verified in `test_progress_report_api.py`. | Not needed (preserves approved plan contract; `PC-001` through `PC-005` remain resolved). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All five single-pass plan critique findings (`PC-001` through `PC-005`) have explicit `resolved` dispositions in `.copilot-tracking/plans/2026-11-15/insight-100-mgmt-tokenomics-plan.md` and are verified in `tokenomics.py`, `store.py`, `coordinator.py`, `api/progress.py`, `api/server.py`, and the `P03` tests.
* Material revisions: None. The single implementation-time update (`OverflowError` guard on extreme UTC boundary strings) was an ordinary local judgment preserving existing HTTP `400` validation semantics.
* Dependent-work pause assessment: No dependent-work pause was required; phases executed strictly in dependency order (`P01` -> `P02` -> `P03` -> `P04`).
* Justification assessment: Supported by Focused-tier test and static-analysis evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| `OD-51` live tariff/spend-ceiling approval and Azure Cost Management billing export reconciliation | Requires owner commercial/governance sign-off (`OD-51`) and live Azure billing feed outside offline demonstrator code (`Refs #100`, `#432`). | Programme owner / Finance & Grants Lead (`OD-51`). | Open distinct governance follow-up; default runtime intentionally reports `od_51_status="open"` and `"Unknown"` costs. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Scope SQL `ai_meter` ledger events to synthetic-admitted roots in `/api/progress` hybrid databases

* Related scope: `P02-T02`
* Evidence: `src/api/src/zava_forward/api/progress.py` (`_ai_economics` filters `recommendations` via `_synthetic_recommendation(r, ids)` while reading `store`'s full `ai_meter` ledger when SQL metering is attached)
* Impact: On synthetic-only datasets (the supported operating mode of `/api/progress`), all ledger entries are synthetic; however, if a hybrid SQL database ever mixed non-synthetic `ai_meter` rows alongside synthetic cases, non-synthetic metered calls could contribute to `/api/progress` `metered_call_count` or alerts.
* Destination: follow_up
* Smallest useful next action: Filter `ledger_records` in `zava_forward.api.progress._ai_economics` to roots linked to admitted synthetic case IDs or `synthetic=True` tariff/billing scopes in a follow-up hardening pass.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Apply `resolved_at <= as_of` cutoff on unlinked JSON recommendations and clarify 5-external + 3-metered TCA split in `src/core/README.md`

* Related scope: `P01-T01`, `P04-T01`
* Evidence: `src/core/src/zava_forward/core/tokenomics.py` (standalone JSON recommendation branch checks `created <= cutoff` before reading current `status`, whereas SQL `Consumption` ledger reviews filter `review["at"] <= cutoff`) and `src/core/README.md` (prose names all eight conceptual BRD `FR-052` TCA components while `other_tca_components` keys the five external `ai_consumption.COMPONENTS` entries alongside metered token/retry/prompt tracking)
* Impact: Does not affect SQL ledger-backed reviews or bounded `[start, end)` progress windows where `resolved_at` lies in-window, but a historical point-in-time `as_of` query over JSON-only recommendations accepted after `as_of` (or carrying hypothetical `source="ai"` with `eligible=False`) could count post-`as_of` JSON acceptance; README prose could lead readers to expect eight keys inside `other_tca_components` instead of five external keys plus metered token usage.
* Destination: follow_up
* Smallest useful next action: Gate standalone JSON recommendation acceptance on `resolved_at <= cutoff` (and `rec.get("eligible") is not False and not rec.get("workflow_only")`) and note the 5-external (`ai_consumption.COMPONENTS`) + 3-metered TCA component mapping in `src/core/README.md`.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | Distinct follow-up item | Hardening follow-up on `src/api/src/zava_forward/api/progress.py` (`_ai_economics`) | Non-blocking defense-in-depth refinement for hybrid SQL datasets; all `AC-1` through `AC-5` invariants hold. |
| `RV-002` | Distinct follow-up item | Hardening/doc cleanup follow-up on `src/core/src/zava_forward/core/tokenomics.py` and `src/core/README.md` | Non-blocking JSON historical `resolved_at <= as_of` edge-case refinement and README prose clarification. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001`: Synthetic root-level filtering of SQL `ai_meter` rows in `zava_forward.api.progress._ai_economics` for hybrid databases.
* `RV-002`: Historical `resolved_at <= as_of` and defensive `eligible`/`workflow_only` check on unlinked JSON recommendations in `tokenomics.py`, plus `other_tca_components` key-count note in `src/core/README.md`.
* `OD-51`: Owner commercial/governance sign-off on live tariffs, spend ceilings, and Azure Cost Management billing export reconciliation (`Refs #100`, `#432`).

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None (`P01` through `P04` complete)

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m ruff check` | `src/core` | Passed | `All checks passed!` |
| `python3 -m mypy` | `src/core` | Passed | `Success: no issues found in 355 source files` |
| `python3 -m ruff check` | `src/api` | Passed | `All checks passed!` |
| `PYTHONPATH=../core/src:../agents/src python3 -m mypy` | `src/api` | Passed | `Success: no issues found in 298 source files` |
| `python3 -m unittest tests/test_management_tokenomics_invariant_100.py` | `src/core/tests` | Passed | `Ran 6 tests in 0.152s - OK` |
| `python3 -W error::ResourceWarning -m unittest src/api/tests/test_management_tokenomics_api_100.py -v` | `src/api/tests` | Passed | `Ran 2 tests in 3.273s - OK` |
| Focused core regression suite (`test_management_tokenomics_invariant_100.py`, `test_progress_reports.py`, `test_progress_event_capture.py`, `test_coordinator.py`, `test_ai_consumption.py`, `test_heldout_eval.py`, `test_tokenomics_comparison.py`) | `src/core/tests` | Passed | `Ran 177 tests in 5.844s - OK (skipped=18)` |
| Focused API regression suite (`test_management_tokenomics_api_100.py`, `test_progress_dashboard.py`, `test_progress_report_api.py`, `test_coordinator_api.py`, `test_ai_consumption_api.py`, `test_ai_tasks.py`, `test_heldout_eval_api.py`, `test_data_operator_ai_state.py`) | `src/api/tests` | Passed | `Ran 250 tests in 273.721s - OK (skipped=21)` |
| `python3 -m unittest tests/test_live_doc_links.py tests/test_cutover_audit.py -q` | `src/core/tests` | Passed | `Ran 11 tests in 7.334s - OK` |
| `python3 tools/rename-zava-tests.py` | repository root | Passed | `Ran 25 tests in 1.381s - OK` |
| Hosted GitHub Actions CI (`Source projects CI`) | `feat/insight-100-mgmt-tokenomics` | Unavailable | Local frozen-HEAD delivery requested without `git push`; hosted CI has not run on this local commit yet. |

## Outcome

* Outcome: Residual work
* Outcome rationale: Planned implementation across `P01` through `P04` is complete, all five acceptance criteria (`AC-1` through `AC-5`) and all plan critique items (`PC-001` through `PC-005`) are verified with passing static analysis (`ruff check`, `mypy`) and Focused test suites (`177` core tests, `250` API tests, `11` doc/cutover tests, `25` migration tests), and two low-severity non-blocking hardening/documentation refinements (`RV-001`, `RV-002`) plus open governance item `OD-51` are routed cleanly to distinct follow-up work.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up (`RV-001`, `RV-002`, `OD-51`) | Select ranked follow-up item in automatic post-Review checkpoint (`RV-002` JSON `resolved_at <= as_of` & README note, `RV-001` hybrid SQL synthetic ledger filter, or `OD-51` governance closure) |

* Execution status: Complete
* Outcome: Residual work
* Validation coverage: `ruff check` and bare `mypy` passed in `src/core` (355 files) and `src/api` (298 files); 177 core tests, 250 API tests, 11 doc/cutover tests, and 25 migration tests passed locally; hosted CI unobserved (no push per caller instruction).
* Blockers: None

