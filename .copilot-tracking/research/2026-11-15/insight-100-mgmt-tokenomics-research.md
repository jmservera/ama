---
description: "Primary evidence artifact for issue #100 management views AI consumption economics"
---
<!-- markdownlint-disable-file -->

# Task Research: insight-100-mgmt-tokenomics

| Field              | Value                                                                               |
|--------------------|-------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                          |
| Researcher / agent | rpi-research (RPI Agent automatic mode)                                             |
| Status             | Complete                                                                            |
| Artifact path      | .copilot-tracking/research/2026-11-15/insight-100-mgmt-tokenomics-research.md       |
| Research disposition | executed                                                                          |
| Planning Readiness | Ready                                                                               |

## Research Brief

* What to research: How Zava Forward management views (`insights.stats`, `progress.report`, `api.progress.dashboard`, `store.py`, and HTTP routes `/api/stats`, `/api/progress`, `/api/ai/report`) currently represent or omit AI consumption economics, denominators, and unknown cost states for Issue `#100` (BRD Required Management Views, FR-052, NFR-012, OD-51; PRD FR-061, NFR-017).
* Why it matters: Issue `#100` has an unticked Tokenomics Acceptance Criterion requiring management views to include AI consumption economics with explicit denominators (`proposal_count`, `accepted_outcome_count`, `metered_call_count`, `unmetered_call_count`) and explicitly report `"Unknown"` (never `0` or `0.0`) whenever no price source or no accepted-outcome count exists.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` phases delivering Issue `#100` Tokenomics delta on `feat/insight-100-mgmt-tokenomics`.
* Scope: `src/core/src/zava_forward/core/` (`ai_consumption.py`, `insights.py`, `progress.py`, `store.py`, `governance.py`), `src/api/src/zava_forward/api/` (`server.py`, `progress.py`), unit/invariant tests in `src/core/tests/` and `src/api/tests/`, and `src/core/README.md` / `src/api/README.md`.
* Non-goals: Approving or closing BRD `OD-51`, inventing real prices/budgets/targets, altering live Azure resources, or modifying web frontend templates unless required by API schema tests.
* Criteria: Evidence-backed mapping of every management insight/view payload, consumption ledger/non-SQL store path, denominator provenance, and `"Unknown"` vs numeric zero invariants.
* Requested outputs: Convergence recommendation with exact module/payload design, file tree, and test strategy.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                              |
|----------------------------------|----------------------------------------------------------------------------------------------------|
| Research question(s)             | Which management views exist in `src/core` and `src/api`, how does `ai_consumption` compute denominators and costs, and how should `ai_consumption_economics` be synthesized and surfaced so `"Unknown"` (never `0` or `0.0`) holds whenever price source or accepted outcomes are absent? |
| Codebase scope                   | `src/core/`, `src/api/`, `docs/brds/agentic-retrofit-programme-brd.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/reference/resources/ai-tokenomics.md` |
| External scope                   | none (codebase and local specification evidence)                                                   |
| Initial internal candidate areas | `src/core/src/zava_forward/core/ai_consumption.py`, `insights.py`, `progress.py`, `store.py`; `src/api/src/zava_forward/api/server.py`, `progress.py` |
| Initial external candidate areas | none                                                                                               |
| Research posture                 | focused                                                                                            |
| Posture provenance               | caller-specified (bounded internal task with named targets and Focused validation tier)            |
| Explicit limits / deadline       | Non-interactive automatic RPI session; leave clean frozen HEAD without push                        |
| Posture-specific completion basis| focused scope and materiality                                                                      |
| Edits allowed during research?   | no, research-only                                                                                  |
| Resolved evidence root           | `.copilot-tracking/`                                                                               |
| Known constraints / excluded sources | Keep `OD-51` open; never emit `0` or `0.0` for unpriced or zero-accepted-outcome cost fields; no `.copilot-tracking/` paths in production code or commit messages |

## Extension Provenance and Participation

| Extension / Source | Type | Disposition | Rationale and Scope |
|---|---|---|---|
| `.github/copilot-instructions.md` | repository instructions | selected | Enforces knowledge-base grounding, pure ASCII Markdown style, focused validation tier (`ruff check`, `mypy`, `unittest`), and git privacy email rules. |
| `rpi-research` | phase skill | selected | Governs three-wave read-only research cycle, `C#` evidence anchors, and convergence synthesis. |
| `python-foundational` | domain skill | skipped | Codebase already uses standard `dataclasses`, `Decimal`, `typing`, and `unittest` conventions documented in `src/core` and `src/api`. |
| `RPI Researcher` | subagent | skipped (inline fallback) | All target files fit within direct, coupled trace across `src/core` and `src/api`; inline investigation completed all three waves without subagent overhead. |

## Cycle 1 Execution

### Wave 1: Wider (Specifications, Governance, and Surface Inventory)

* Verified the normative requirements in the BRD, PRD, and knowledge base:
  * BRD Required Management Views (`C1`), `FR-052` (`C2`), `NFR-012` (`C3`), and `OD-51` (`C4`) require management views to surface AI consumption economics: metered usage against limits, limit and alert breaches, Total Cost of AI alongside token/API cost, and AI cost per accepted outcome for each capability beside its quality floor and booked value, while keeping `OD-51` open until spend ceilings, alert owners, and dated price sources are approved.
  * PRD `FR-061` (`C5`) and `NFR-017` (`C6`) plus the AI Tokenomics reference synthesis (`C7`) require explicit denominators, forbid treating raw token counts or unreviewed drafts as accepted outcomes, and require `"Unknown"` rather than `0` whenever price sources, billing reconciliation, Total Cost of AI components, or accepted-outcome denominators are missing.
* Inventoried module layout across `src/core` and `src/api`:
  * `src/core/src/zava_forward/core/tokenomics.py` does not yet exist (`ai_consumption.py` and `tokenomics_comparison.py` exist). Creating `tokenomics.py` establishes a dedicated, pure core synthesis module without coupling `insights.py` to SQL internals.
  * `src/api/src/zava_forward/api/` has no `routers/` package; `server.py` serves all HTTP routes directly (`C12`).

### Wave 2: Deeper (Data Flows, Ledger Contracts, and Management Views)

* Audited every management insight, progress, coordinator, and live AI report surface:
  1. `insights.stats(...)` (`C9`) called by `Store.stats()` (`C11`) and served at `GET /api/stats` (`C12`) backs the `#/overview` management insights screen; it currently returns `kpis`, `stages`, `areas`, `waves`, `ages`, `funding`, `contractors`, and `team`, with no `ai_consumption_economics` block.
  2. `progress.report(...)` (`C10`) called by `Store.progress_report(...)` (`C11`) and served at `GET /api/stats?report=progress` and `GET /api/cases.csv?report=progress` (`C12`) returns programme flow denominators, histories, and forecast, and `progress.export_csv(...)` round-trips top-level dictionary sections via `json.dumps(..., sort_keys=True)`.
  3. `coordinator.read(...)` (`C13`) served at `GET /api/coordinator` (`C12`) wraps `progress.report(...)` with heatmap and saved-view state for programme coordinators.
  4. `zava_forward.api.progress.dashboard(...)` (`C14`) served at `GET /api/progress` (`C12`) builds the management progress dashboard (`coverage`, `daily`, `weekly`, `time_to_close`, `current`, `ai`) and currently summarizes review dispositions without tokenomics denominators or `"Unknown"` cost invariants.
  5. `ai_tasks.live_report(...)` (`C15`) called by `Store.ai_live_report(...)` (`C11`) and embedded under `"live"` in manager-only `GET /api/ai/report` (`C12`) summarizes live AI review dispositions and fallback reasons.
* Audited `ai_consumption.py` (`C8`):
  * `Consumption.report(start, end, as_of, ...)` computes ledger-backed `calls`, `accepted_proposals`, `token_cost`, `cost_per_accepted_proposal`, `cost_per_accepted_outcome`, `other_tca_components`, `total_cost_of_ai`, `quality_status`, `quality_qualified_cost`, `cash_value`, `owned_alerts`, and `by_capability` using `UNKNOWN = "Unknown"` and 80-digit `Decimal` arithmetic.
  * `Store` instances running on the JSON backend (or before `Assistants(store)` attaches `store.ai.consumption`) hold AI and workflow recommendations in `store.data["recommendations"]`, where each item tracks `kind`, `source` (`"ai"` vs `"template"`), `status` (`"Accepted"`, `"Edited"`, `"Rejected"`, `"Not reviewed"`, `"Proposed"`, `"Hold"`, `"Quarantined"`), `task`/`capability`, and `meter_root` / `envelope.meter_root`.

### Wave 3: Contrarian (Regression Traps, Determinism, Privacy, and Zero-Cost Edge Cases)

* Challenged naive integration designs against existing test suites and uncovered four hard constraints:
  1. Exact top-level keys on `GET /api/ai/report`: `test_heldout_eval_api.py` (`C16`) and `test_ai_consumption_api.py` (`C17`) assert `set(report) == {"evaluation", "chat_evaluation", "live", "registry", "consumption"}` and exact equality on `held["consumption"]` during meter holds, plus `assertIsNone(report["cost_per_accepted_outcome"]["cost"])` on `Consumption.report()`. Therefore, `Consumption.report()` and top-level keys of `/api/ai/report` must remain unchanged; `ai_consumption_economics` belongs on `insights.stats` (`/api/stats`), `progress.report` (`/api/stats?report=progress` and `/api/cases.csv?report=progress`), `coordinator.read` (`/api/coordinator`), `api.progress.dashboard` (`/api/progress`), and `ai_tasks.live_report` (`/api/ai/report["live"]["ai_consumption_economics"]`), plus `Store.ai_consumption_economics(...)`.
  2. Strict determinism and zero read-side mutations: `test_progress_dashboard.py` (`C18`), `test_progress_report_api.py` (`C19`), and `test_coordinator_api.py` (`C20`) assert byte-identical repeat reads, exact `progress.export_csv` round-trip (`decoded == report`), and unchanged `_db_seq()` across management GET calls. `tokenomics.py` must never call `datetime.now()`, never mutate the database or audit log, and derive deterministic ledger snapshots bounded by explicit timestamps when provided or full deterministic ledger state otherwise.
  3. Zero-cost fabrication edge case: In `ai_consumption.py` (`C8`), a reconciled bill with `billed = "0"` could produce `cost = "0"` if unguarded when `price_source_configured=False`, `od_51_status == "open"`, `unmetered_call_count > 0`, or `accepted_outcome_count == 0` with zero calls. `tokenomics.py` must fail closed so that whenever `not price_source_configured` (including `od_51_status != "approved"` or `unmetered_call_count > 0`) or `accepted_outcome_count == 0`, cost-per-accepted-outcome fields (and unpriced/zero-call cost fields) always emit `"Unknown"` and never `0`, `0.0`, `"0"`, `"0.0"`, or `None`.
  4. Content-free privacy canaries: Role-matrix and coordinator privacy tests scan `/api/stats`, `/api/progress`, `/api/coordinator`, and `/api/ai/report` for canary substrings (`PRIVATE`, `REASON`, `RESIDENT`, `SYNTH-VULN`, emails). `ai_consumption_economics` must emit only closed identifiers, integer denominators, booleans, fixed status tokens, Decimal strings, and `"Unknown"`, scrubbing or omitting raw alert owners if they contain `@` or free text unless bounded to closed role/owner tokens (or redacting free-text reasons to closed alert tokens).

## Evidence Log

| ID | Location | Finding |
|---|---|---|
| `C1` | `docs/brds/agentic-retrofit-programme-brd.md:1769` | Required Management Views mandate AI consumption economics: metered usage against limits, limit and alert breaches, Total Cost of AI, and AI cost per accepted outcome per capability beside quality floor and booked value. |
| `C2` | `docs/brds/agentic-retrofit-programme-brd.md:863` | `FR-052` requires per-call/step metering, enforced limits, owned breach alerts, and spend attribution to accepted outcomes rather than raw token volume. |
| `C3` | `docs/brds/agentic-retrofit-programme-brd.md:1388` | `NFR-012` requires Total Cost of AI alongside token/API cost, cost per accepted outcome beside the quality floor, and capacity-not-cash treatment unless finance-defensible. |
| `C4` | `docs/brds/agentic-retrofit-programme-brd.md:1720` | `OD-51` leaves spend limits, loop/fan-out caps, alert owners, dated price sources, and acceptable cost-per-outcome ranges open. |
| `C5` | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:664` | `FR-061` requires metering, explicit denominators, owned alerts, and accepted-outcome attribution in the demonstrator. |
| `C6` | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:970` | `NFR-017` requires reporting `"Unknown"` rather than zero where dated price sources, reconciled billing, or accepted-outcome counts are absent. |
| `C7` | `docs/reference/resources/ai-tokenomics.md:45` | AI Tokenomics synthesis defines Total Cost of AI components, quality-floor gating, and anti-gaming rules against unreviewed or workflow-only counts. |
| `C8` | `src/core/src/zava_forward/core/ai_consumption.py:1399` | `Consumption.report()` computes ledger `calls`, `accepted_proposals`, `token_cost`, `cost_per_accepted_proposal`, `other_tca_components`, `total_cost_of_ai`, `quality_status`, `quality_qualified_cost`, and `cash_value` using `UNKNOWN = "Unknown"`. |
| `C9` | `src/core/src/zava_forward/core/insights.py:82` | `insights.stats(cases, staff, ...)` builds the overview management payload without `ai_consumption_economics`. |
| `C10` | `src/core/src/zava_forward/core/progress.py:599` | `progress.report(...)` and `progress.export_csv(...)` build and CSV-round-trip the programme progress/forecast management report using `json.dumps` on top-level sections. |
| `C11` | `src/core/src/zava_forward/core/store.py:1101` | `Store.stats()`, `Store.progress_report()`, and `Store.ai_live_report()` (line 2122) are the central store entrypoints backing HTTP management views across JSON, SQLite, and MSSQL stores. |
| `C12` | `src/api/src/zava_forward/api/server.py:570` | `server.py` serves `GET /api/progress` (570), `GET /api/coordinator` (579), `GET /api/stats?report=progress` and `/api/cases.csv?report=progress` (590), `GET /api/stats` (926), and `GET /api/ai/report` (949). |
| `C13` | `src/core/src/zava_forward/core/coordinator.py:113` | `coordinator.read(store, user, query)` builds the coordinator management flow payload from `progress.report(...)`. |
| `C14` | `src/api/src/zava_forward/api/progress.py:252` | `api.progress.dashboard(store, user, query)` builds the `/api/progress` management payload using deterministic `start`/`end` query bounds. |
| `C15` | `src/core/src/zava_forward/core/ai_tasks.py:564` | `ai_tasks.live_report(store, user)` summarizes live AI task review dispositions and fallback reasons for `GET /api/ai/report["live"]`. |
| `C16` | `src/api/tests/test_heldout_eval_api.py:107` | Asserts exact top-level keys `{"evaluation", "chat_evaluation", "live", "registry", "consumption"}` on `GET /api/ai/report`. |
| `C17` | `src/api/tests/test_ai_consumption_api.py:947` | Asserts `report["cost_per_accepted_outcome"]["cost"] is None` on `Consumption.report()` and exact `held["consumption"]` dict on meter holds (line 2096). |
| `C18` | `src/api/tests/test_progress_dashboard.py:656` | Asserts deterministic repeat equality `self.assertEqual(self.report(), baseline)` on `/api/progress`. |
| `C19` | `src/api/tests/test_progress_report_api.py:258` | Asserts exact `progress.export_csv` determinism and CSV round-trip (`decoded == report`, line 324). |
| `C20` | `src/api/tests/test_coordinator_api.py:242` | Asserts read-only `_db_seq()` invariance and zero private canary leakage (line 127) across coordinator reads. |

## Parent Synthesis and Convergence Recommendation

### Answered Questions and Decisions

1. **Where should AI consumption economics synthesis live?**
   * **Accepted recommendation**: Create `src/core/src/zava_forward/core/tokenomics.py` exporting pure, strictly typed helpers (`summarize_ai_consumption_economics(...)`, `store_ai_consumption_economics(store, ...)`, and `assert_tokenomics_invariants(summary)`) and expose `Store.ai_consumption_economics(...)` on `Store`.
   * **Rejected alternative**: Mutating `Consumption.report()`'s existing `cost_per_accepted_outcome` shape in `ai_consumption.py` or adding a 6th top-level key to `GET /api/ai/report`. Rejected because `C16` and `C17` enforce exact backward-compatible contracts on both surfaces.
2. **Which management views should include `ai_consumption_economics`?**
   * **Accepted recommendation**: Include `"ai_consumption_economics"` in:
     * `insights.stats(...)` / `Store.stats()` (`GET /api/stats`),
     * `progress.report(...)` / `Store.progress_report(...)` (`GET /api/stats?report=progress` and `GET /api/cases.csv?report=progress`),
     * `coordinator.read(...)` (`GET /api/coordinator`),
     * `zava_forward.api.progress.dashboard(...)` (`GET /api/progress`), and
     * `ai_tasks.live_report(...)` / `Store.ai_live_report(...)` (`GET /api/ai/report["live"]["ai_consumption_economics"]`).
3. **How are explicit denominators and `"Unknown"` invariants defined?**
   * Explicit integer denominators (`proposal_count`, `accepted_outcome_count`, `metered_call_count`, `unmetered_call_count`) appear both at top level of `ai_consumption_economics` and inside `ai_consumption_economics["denominators"]` (alongside `unreviewed_proposal_count`, `rejected_or_withdrawn_count`, and `workflow_only_excluded_count`).
   * Workflow/template fallbacks (`source != "ai"` without meter attribution), unreviewed drafts, rejected proposals, held/quarantined outputs, and unresolved withdrawals never count toward `accepted_outcome_count`.
   * AI-source recommendations without durable meter attribution increment `unmetered_call_count` so metering gaps are surfaced rather than hidden, and force cost fields to `"Unknown"`.
   * Whenever `price_source_configured` is `False` (default while `od_51_status == "open"`, when dated price or reconciled billing is missing, or when ledger holds/gaps exist) OR `accepted_outcome_count == 0`, `cost_per_accepted_outcome`, `token_cost_per_accepted_outcome`, `quality_qualified_cost_per_accepted_outcome`, and per-capability `cost_per_accepted_outcome` explicitly equal `"Unknown"` (never `0`, `0.0`, `"0"`, `"0.0"`, or `None`), and when `not price_source_configured` (or zero-call zero-bill with `accepted_outcome_count == 0`), `token_cost` and `total_cost_of_ai` also equal `"Unknown"`.
   * Content-free projection: no case IDs, actor emails, or reviewer prose are included in `ai_consumption_economics`, preserving role-matrix and coordinator privacy guarantees (`C20`).

### Unresolved Decisions, Risks, and Further Research

* **Open governance item preserved**: BRD `OD-51` remains `"open"` by default in runtime state (`od_51_status: "open"`, `price_source_configured: False`); tests will exercise both default unpriced (`OD-51` open) and explicit priced/configured scenarios (`od_51_status: "approved"`, `price_source_configured: True` with `accepted_outcome_count == 0` vs `accepted_outcome_count > 0`).
* **Cycle re-entry evaluation**: Single complete three-wave cycle saturated all codebase contracts, specifications, and contrarian test constraints. No second research cycle is needed.
* **Planning Readiness**: `Ready` (Research disposition: `executed`).

