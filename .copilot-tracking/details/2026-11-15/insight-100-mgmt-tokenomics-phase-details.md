---
title: "RPI Phase Details: Management Views AI Consumption Economics (Issue #100)"
description: "Detailed phase and task specifications, contracts, test ownership, and validation criteria for Issue #100"
ms.date: 2026-11-15
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: issue-100-mgmt-tokenomics
* Task slug: insight-100-mgmt-tokenomics
* Related plan: .copilot-tracking/plans/2026-11-15/insight-100-mgmt-tokenomics-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/insight-100-mgmt-tokenomics-research.md, docs/brds/agentic-retrofit-programme-brd.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/reference/resources/ai-tokenomics.md

## Phase Index

| Phase ID | Name                                                            | Status    | Detail sections        |
|----------|-----------------------------------------------------------------|-----------|------------------------|
| P01      | Core AI Consumption Economics Synthesis (`tokenomics.py`)       | Ready     | P01, P01-T01           |
| P02      | Wire `ai_consumption_economics` Across Core and API Views       | Ready     | P02, P02-T01, P02-T02  |
| P03      | End-to-End Invariant and API Regression Tests                   | Ready     | P03, P03-T01, P03-T02  |
| P04      | Documentation Updates and Focused Validation Gate               | Ready     | P04, P04-T01           |

## Test Ownership and Coverage Lock

* Canonical production targets:
  * `src/core/src/zava_forward/core/tokenomics.py` (new)
  * `src/core/src/zava_forward/core/insights.py` (modified)
  * `src/core/src/zava_forward/core/progress.py` (modified)
  * `src/core/src/zava_forward/core/coordinator.py` (modified)
  * `src/core/src/zava_forward/core/ai_tasks.py` (modified)
  * `src/core/src/zava_forward/core/store.py` (modified)
  * `src/api/src/zava_forward/api/progress.py` (modified)
  * `src/api/src/zava_forward/api/server.py` (modified to forward optional explicit `start`/`end`/`as_of` query bounds to `s.ai_live_report(u, ...)` while keeping exact 5 top-level keys)
* Documentation targets:
  * `src/core/README.md` (modified)
  * `src/api/README.md` (modified)
* Generated targets: `none`
* Exact test removals: `none`
* Maximum test file additions: `2`
  * `src/core/tests/test_management_tokenomics_invariant_100.py` (semantic invariant ownership for core `tokenomics`, `Store.stats`, `Store.progress_report` + CSV round-trip, `coordinator.read`, and `Store.ai_live_report`)
  * `src/api/tests/test_management_tokenomics_api_100.py` (HTTP contract, role access, determinism, `_db_seq()` read-only invariance, and canary privacy ownership across `/api/stats`, `/api/stats?report=progress`, `/api/cases.csv?report=progress`, `/api/progress`, `/api/coordinator`, and `/api/ai/report`)
* Existing regression suites retained intact: `src/core/tests/test_*.py` and `src/api/tests/test_*.py` (`test_ai_consumption.py`, `test_ai_consumption_api.py`, `test_heldout_eval_api.py`, `test_progress_reports.py`, `test_progress_report_api.py`, `test_progress_dashboard.py`, `test_coordinator.py`, `test_coordinator_api.py`, `test_role_matrix.py`).

<!-- rpi:phase id=P01 -->
## P01: Core AI Consumption Economics Synthesis (`tokenomics.py`)

### Context

`ai_consumption.Consumption.report()` (`C8`) models ledger-window metering, pricing, billing reconciliation, quality status, and Total Cost of AI components on SQL stores, while `Store` (`C11`) also holds recommendations on JSON and SQL backends where `store.ai.consumption` may be `None` or where workflow/template fallbacks and unmetered AI records coexist. Management views currently lack a unified `ai_consumption_economics` structure (`C9`, `C10`, `C13`, `C14`, `C15`).

### Intent

Build `src/core/src/zava_forward/core/tokenomics.py` as a pure, read-only, deterministic synthesis module that produces a closed, content-free `ai_consumption_economics` dictionary meeting BRD Required Management Views (`C1`), `FR-052` (`C2`), `NFR-012` (`C3`), `OD-51` (`C4`), and PRD `FR-061` / `NFR-017` (`C5`, `C6`).

### Boundaries

* Included: `tokenomics.py` schema constants, denominator reconciliation across ledger records and recommendation items, fail-closed `"Unknown"` pricing/cost computation, per-capability breakdown, content-free alert sanitization, and runtime invariant assertion helper.
* Excluded: Mutating `ai_consumption.py` contracts, modifying database schemas, or writing audit/event records during reads.

### Likely Targets

* `src/core/src/zava_forward/core/tokenomics.py`: New module implementing AI consumption economics synthesis and invariant validation.

### Dependencies

* `zava_forward.core.ai_consumption` (`UNKNOWN`, `COMPONENTS`, `QUALITY`, `amount`, `Consumption`).

### Validation Expectations

* `python3 -m mypy` and `python3 -m ruff check` inside `src/core` pass with zero diagnostics; unit tests verify all denominator and `"Unknown"` rules.

### Completion Evidence

* `src/core/src/zava_forward/core/tokenomics.py` created and passing invariant checks across empty, unpriced, priced-zero-accepted, priced-accepted, and unmetered-gap inputs.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement `src/core/src/zava_forward/core/tokenomics.py`

#### Context

Issue `#100` requires explicit denominators (`proposal_count`, `accepted_outcome_count`, `metered_call_count`, `unmetered_call_count`) and strict `"Unknown"` (never `0` or `0.0`) cost / cost-per-accepted-outcome values whenever no price source (`price_source_configured=False` / `OD-51` open) or no accepted-outcome count (`accepted_outcome_count == 0`) exists.

#### Intent

Implement three clean, typed public functions in `zava_forward.core.tokenomics`:

1. `summarize_ai_consumption_economics(*, recommendations=None, consumption_report=None, ledger_records=None, start=None, end=None, as_of=None, od_51_status="open", price_source=None, components=None, quality_floor_status=None, booked_value=None, limit_configured=False, ledger_coverage=None) -> dict[str, Any]`
   * Extracts metered roots, metered calls, retries, failures, token totals, accepted roots, unjoined outputs/reviews, unknown liabilities, prices, reconciled bills, and alerts from either a supplied `consumption_report` (`Consumption.report(...)` dict) or raw deterministic `ledger_records` (filtered by optional `[start, end)` and `as_of` epoch bounds without calling `datetime.now()`). For explicit `[start, end)` bounds, reconciles a single complete single-currency billing record matching `(start, end)`; for unbounded or half-bounded management reads (`start is None` or `end is None`), reconciles complete, non-overlapping single-currency billing record(s) covering every in-scope metered call (`b["start"] <= c["at"] < b["end"]` and `b["budget"] in c["budgets"]`) within tolerances, failing closed to `"unreconciled"` otherwise (`PC-002`).
   * Reconciles `recommendations` (`Iterable[Mapping[str, Any]]`) using both `meter_root = rec.get("meter_root") or (rec.get("envelope") or {}).get("meter_root")` and SHA-256 `hashed_id = ai_consumption.reference(rec["id"])` (when `isinstance(rec.get("id"), str) and rec["id"]`) against ledger `reserved.root` and `output.output` (`PC-003`):
     * When `consumption_report` is supplied with `ledger_records=None`, recommendation items carrying a valid 64-hex `meter_root` are treated as covered by `consumption_report` rather than double-counted or flagged unmetered (`PC-003`).
     * Pure workflow/template items (`source != "ai"` with no `meter_root`) increment `workflow_only_excluded_count` and never count toward `proposal_count`, `accepted_outcome_count`, `metered_call_count`, or `unmetered_call_count`.
     * Publish-held metered fallbacks (`source == "template"` carrying `meter_root`) and ledger roots with `output.eligible is False` (such as chat turns or held fallbacks) count their calls in `metered_call_count`, never in `unmetered_call_count` or `accepted_outcome_count`; `proposal_count` counts proposal-eligible metered roots (`root not in outputs or outputs[root]["eligible"] is True`, plus proposal-bearing held roots tied to recommendation items) plus unmetered AI recommendations (`PC-003`).
     * AI-source items (`source == "ai"`) lacking a valid `meter_root` and absent from ledger output digests increment `unmetered_call_count` and `proposal_count`.
     * Human-accepted AI proposals (`status in ("Accepted", "Edited")` and eligible, not `"Hold"` / `"Quarantined"` / `"Rejected"` / `"Not reviewed"` / `"Proposed"`, and not unresolved/withdrawn in ledger) count toward `accepted_outcome_count`, except that unjoined ledger reviews fail closed just as `Consumption.report()` requires.
   * Sets `od_51_status` to `"open"` unless explicitly `"approved"`. Sets `price_source_configured` to `True` only when `od_51_status == "approved"`, `ledger_coverage not in ("ledger-hold", "unavailable")`, a non-empty dated price source exists (`tariff_basis != "Unknown"` or explicit `price_source`), billing reconciliation is `"reconciled"` with a single currency and non-`"Unknown"` `token_cost`, `unmetered_call_count == 0`, and no unknown liabilities or unjoined ledger outputs/reviews exist.
   * Enforces fail-closed `"Unknown"` invariants on every top-level and per-capability cost and unit-cost field (`PC-005`):
     * When `not price_source_configured`: `price_source = "Unknown"`, `currency = "Unknown"`, `token_cost = "Unknown"`, `total_cost_of_ai = "Unknown"`, `cost_per_accepted_outcome = "Unknown"`, `token_cost_per_accepted_outcome = "Unknown"`, `quality_qualified_cost_per_accepted_outcome = "Unknown"`, and every capability's `token_cost`, `total_cost_of_ai`, `token_cost_per_accepted_outcome`, and `cost_per_accepted_outcome` equal `"Unknown"`.
     * When `price_source_configured` is `True` and `accepted_outcome_count == 0`: `cost_per_accepted_outcome = "Unknown"`, `token_cost_per_accepted_outcome = "Unknown"`, `quality_qualified_cost_per_accepted_outcome = "Unknown"`, and every capability's `cost_per_accepted_outcome = "Unknown"` and `token_cost_per_accepted_outcome = "Unknown"`. In addition, if reconciled `billed == Decimal("0")` when `accepted_outcome_count == 0`, `token_cost` and `total_cost_of_ai` also report `"Unknown"` so numeric or string zero is never emitted for an unattributed zero-outcome state; if positive reconciled spend occurred on rejected/unreviewed calls (`billed > 0`), `token_cost` reports that positive Decimal string (`format(billed, "f")`) while all cost-per-accepted-outcome fields report `"Unknown"`.
     * When `price_source_configured` is `True` and `accepted_outcome_count > 0` and `billed > 0`: `token_cost = format(billed, "f")`, `token_cost_per_accepted_outcome = format(billed / accepted_outcome_count, "f")`, `total_cost_of_ai` equals the exact Decimal sum of `token_cost` + all 5 `COMPONENTS` if and only if all 5 `other_tca_components` are priced (else `"Unknown"`), `cost_per_accepted_outcome` equals `format(Decimal(total_cost_of_ai) / accepted_outcome_count, "f")` if `total_cost_of_ai != "Unknown"` and `quality_floor_status == "Pass"` (else `"Unknown"`), and `quality_qualified_cost_per_accepted_outcome` equals `token_cost_per_accepted_outcome` when `quality_floor_status == "Pass"` (else `"Unknown"`).
     * Per-capability attribution (`PC-005`): For each capability `cap` in `by_capability`, whenever `cap["accepted_outcome_count"] == 0`, `cap["cost_per_accepted_outcome"]` and `cap["token_cost_per_accepted_outcome"]` strictly equal `"Unknown"` even if overall `accepted_outcome_count > 0`. When `price_source_configured` is `True`, single-capability reconciled cohorts inherit exact `token_cost` and (when complete) `total_cost_of_ai`; multi-capability cohorts report exact per-capability `token_cost` only when reconciled variance is zero against per-call projected charges (else `"Unknown"`), and multi-capability `total_cost_of_ai` / `cost_per_accepted_outcome` fail closed to `"Unknown"` rather than inventing pro-rata overhead splits. No capability cost field ever emits `0`, `0.0`, `"0"`, `"0.0"`, or `None`.
     * `booked_value` defaults to `"Unknown"` (capacity released is never booked cash unless an explicit positive finance-confirmed `booked_value` Decimal is supplied while `price_source_configured` is `True`).
   * Sanitizes `owned_alerts` to closed, content-free tokens (`owner` scrubbed if containing `@` or spaces to `"configured-owner"`, closed `reason` code, closed `route` code) so user emails or private prose can never leak into management views.
2. `store_ai_consumption_economics(store, *, start=None, end=None, as_of=None, recommendations=None, consumption_report=None, od_51_status=None, price_source=None, components=None, quality_floor_status=None, booked_value=None, limit_configured=None) -> dict[str, Any]`
   * Snapshots `recommendations` (when not explicitly passed) and optional opt-in governance defaults (`gov = getattr(store, "tokenomics_governance", None) or store.data.get("tokenomics_governance")`, defaulting to `od_51_status="open"`, `limit_configured=False` when absent so runtime `OD-51` stays open unless explicitly configured by an authorised caller or test, `PC-002`).
   * Checks `ledger := getattr(getattr(store, "ai", None), "consumption", None)` and `port := getattr(ledger, "port", None)`. Touches SQL only when `bool(getattr(port, "sql", False))` is `True` and `getattr(port, "schema_error", None)` is `None` (`PC-001`). Reads `assistant_events` via a short-lived read-only connection (`port.store.assistant_connection()` plain `SELECT` + `close()` without `BEGIN IMMEDIATE` write-locking, falling back to `port.transaction()` only on standalone mock ports without `port.store`) and catches `(ai_consumption.DispatchHeld, ValueError, KeyError, TypeError, OSError, RuntimeError)` to fail closed to `ledger_coverage="ledger-hold"`, `price_source_configured=False`, and `"Unknown"` costs (`PC-001`).
3. `assert_tokenomics_invariants(summary: Mapping[str, Any]) -> None`
   * Validates presence and integer types of all 4 explicit denominators (`proposal_count`, `accepted_outcome_count`, `metered_call_count`, `unmetered_call_count`) at top level and in `denominators`, and verifies that no cost or cost-per-accepted-outcome field is `0`, `0.0`, `"0"`, `"0.0"`, `"0.00"`, `None`, or `bool`, and that unpriced or zero-accepted-outcome states strictly report `"Unknown"`.

#### Boundaries

* Included: `src/core/src/zava_forward/core/tokenomics.py`.
* Excluded: Route wiring and store wiring (covered in P02).

#### Likely Targets

* `src/core/src/zava_forward/core/tokenomics.py`: New module.

#### Dependencies

* None beyond Python stdlib (`decimal`, `datetime`, `typing`, `re`) and `zava_forward.core.ai_consumption`.

#### Validation Expectations

* `python3 -m mypy` and `python3 -m ruff check` pass on `tokenomics.py`.

#### Completion Evidence

* Module imports cleanly and passes `assert_tokenomics_invariants` across all matrix cases.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Wire `ai_consumption_economics` Across Core and API Management Views

### Context

Management insights and reporting are served by `insights.stats` / `Store.stats` (`/api/stats`), `progress.report` / `Store.progress_report` (`/api/stats?report=progress` and `/api/cases.csv?report=progress`), `coordinator.read` (`/api/coordinator`), `api.progress.dashboard` (`/api/progress`), and `ai_tasks.live_report` (`/api/ai/report["live"]`).

### Intent

Include deterministic `ai_consumption_economics` across all five management view pipelines plus `Store.ai_consumption_economics(...)` without breaking existing exact-key, CSV round-trip, repeat-read determinism, read-only DB sequence, or privacy canary assertions.

### Boundaries

* Included: `insights.py`, `progress.py`, `coordinator.py`, `ai_tasks.py`, `store.py` in `src/core`, and `progress.py` in `src/api`.
* Excluded: Adding top-level keys to `GET /api/ai/report` in `server.py` or changing `Consumption.report()` in `ai_consumption.py`.

### Likely Targets

* `src/core/src/zava_forward/core/insights.py`: Accept optional `ai_consumption_economics` (or synthesize via `tokenomics.summarize_ai_consumption_economics` from `recommendations` when omitted) and include `"ai_consumption_economics"` in returned `stats(...)` dict.
* `src/core/src/zava_forward/core/progress.py`: Accept optional `ai_consumption_economics` in `report(...)` (defaulting via `tokenomics.summarize_ai_consumption_economics` bounded to `as_of` when omitted) so both JSON and `export_csv` / `_decode_report_csv` round-trip `"ai_consumption_economics"` cleanly.
* `src/core/src/zava_forward/core/coordinator.py`: Pass `ai_consumption_economics=store.ai_consumption_economics(start=query.get("start"), as_of=query.get("as_of"))` into `progress.report(...)` inside `coordinator.read(...)` and expose `"ai_consumption_economics": evidence["ai_consumption_economics"]` at top level of `_assemble(...)` (`PC-002`).
* `src/core/src/zava_forward/core/ai_tasks.py`: Expose `"ai_consumption_economics": tokenomics.store_ai_consumption_economics(store, start=start, end=end, as_of=as_of)` inside `live_report(store, user=None, *, start=None, end=None, as_of=None)`.
* `src/core/src/zava_forward/core/store.py`: Add `Store.ai_consumption_economics(self, **kwargs)`, support optional `start`/`end`/`as_of` on `Store.ai_live_report(self, user=None, **kwargs)`, and pass `self.ai_consumption_economics(...)` into `insights.stats(...)` in `Store.stats()` and `progress.report(...)` in `Store.progress_report(...)` (bounded deterministically by `start` and `as_of` when supplied).
* `src/api/src/zava_forward/api/progress.py`: Include `"ai_consumption_economics"` in `dashboard(store, user, query)` using synthetic-record admission (`is_synthetic is True` and synthetic case IDs) and deterministic `created` / `resolved_at` UTC normalization across `[start, end]` (`PC-004`).
* `src/api/src/zava_forward/api/server.py`: Forward explicit `start`/`end`/`as_of` query parameters (only when supplied in `url.query`) into `s.ai_live_report(u, **live_bounds)` on `GET /api/ai/report` while keeping the exact 5 top-level keys (`PC-002`).

### Dependencies

* P01 (`zava_forward.core.tokenomics`).

### Validation Expectations

* Existing tests (`test_progress_reports.py`, `test_progress_report_api.py`, `test_progress_dashboard.py`, `test_coordinator.py`, `test_coordinator_api.py`, `test_heldout_eval_api.py`, `test_ai_consumption_api.py`, `test_role_matrix.py`) continue to pass with zero modifications to existing assertions.

### Completion Evidence

* Every management view returns `"ai_consumption_economics"` satisfying `tokenomics.assert_tokenomics_invariants`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Wire `ai_consumption_economics` into `insights`, `progress`, `coordinator`, `ai_tasks`, and `Store`

#### Context

`Store.stats()`, `Store.progress_report()`, `coordinator.read()`, and `Store.ai_live_report()` are the core entrypoints used by both direct Python callers and the HTTP server (`C9`, `C10`, `C11`, `C13`, `C15`). Note that `progress.export_csv` (`C10`) iterates `report.items()` and JSON-encodes dict values, while `_decode_report_csv` in `test_progress_reports.py` and `test_progress_report_api.py` JSON-decodes any value starting with `{` or `[` (`C19`). Because `ai_consumption_economics` is a JSON-serializable `dict`, `export_csv` round-trips it automatically with zero CSV schema breakage.

#### Intent

Wire `tokenomics` cleanly into `Store`, `insights.stats`, `progress.report`, `coordinator.read`, and `ai_tasks.live_report` while keeping direct unit calls (`insights.stats(cases, staff)` and `progress.report(cases, audit, as_of=...)` without a `Store`) working seamlessly with deterministic defaults.

#### Boundaries

* Included: `insights.py`, `progress.py`, `coordinator.py`, `ai_tasks.py`, `store.py`.
* Excluded: `src/api/` files (handled in P02-T02).

#### Likely Targets

* `src/core/src/zava_forward/core/insights.py`: Optional `recommendations` / `ai_consumption_economics` keyword arguments on `stats(...)`.
* `src/core/src/zava_forward/core/progress.py`: Optional `ai_consumption_economics` keyword argument on `report(...)`.
* `src/core/src/zava_forward/core/coordinator.py`: Top-level `"ai_consumption_economics"` key in `read(...)`.
* `src/core/src/zava_forward/core/ai_tasks.py`: `"ai_consumption_economics"` key in `live_report(...)`.
* `src/core/src/zava_forward/core/store.py`: `Store.ai_consumption_economics(...)` method and wiring in `Store.stats(...)` and `Store.progress_report(...)`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `Store.stats()`, `Store.progress_report()`, `progress.export_csv()`, `coordinator.read()`, and `Store.ai_live_report()` all include valid `ai_consumption_economics` and pass `mypy` + existing unit tests.

#### Completion Evidence

* Updated core modules pass `ruff check` and `mypy`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Wire `ai_consumption_economics` into `zava_forward.api.progress.dashboard` and `server.py` `/api/ai/report` query bounds

#### Context

`GET /api/progress` calls `zava_forward.api.progress.dashboard(store, user, query)` (`C14`), which resolves deterministic `start: date` and `end: date` bounds (defaulting `end` to `_default_end(events)` when query `end` is absent so repeat calls never depend on wall-clock `datetime.now()`, `C18`) and enforces synthetic-only isolation (`C18`, `PC-004`). `GET /api/ai/report` calls `s.ai_live_report(u)` in `server.py` (`C12`, `PC-002`).

#### Intent

In `src/api/src/zava_forward/api/progress.py`, filter recommendations to explicitly synthetic records (`record.get("is_synthetic") is True` whose `case_ids` list or `case_id` string links only to synthetic `ids`) whose stored `created` timestamp (falling back to `resolved_at`, normalizing date-only `YYYY-MM-DD` and timezone-naive ISO strings as UTC uniformly regardless of whether `start`/`end` were implicit or explicit in `query`) falls within `[start, end]`, and pass `start=f"{start.isoformat()}T00:00:00Z"`, `end=f"{(end + DAY).isoformat()}T00:00:00Z"`, `as_of=f"{(end + DAY).isoformat()}T00:00:00Z"` to `store.ai_consumption_economics(...)` (`PC-004`). In `src/api/src/zava_forward/api/server.py`, forward optional explicit `start`/`end`/`as_of` query parameters (only when present in `q`) to `s.ai_live_report(u, **live_bounds)` while keeping `set(report) == {"evaluation", "chat_evaluation", "live", "registry", "consumption"}` (`PC-002`).

#### Boundaries

* Included: `src/api/src/zava_forward/api/progress.py` and `src/api/src/zava_forward/api/server.py`.
* Excluded: Modifying `src/api/src/zava_forward/api/web/` frontend files or top-level keys of `GET /api/ai/report`.

#### Likely Targets

* `src/api/src/zava_forward/api/progress.py`: Add deterministic `_ai_economics(store, recs, ids, start, end)` helper and `"ai_consumption_economics"` field on `dashboard(...)`.
* `src/api/src/zava_forward/api/server.py`: Forward explicit `live_bounds` into `s.ai_live_report(u, **live_bounds)`.

#### Dependencies

* P01-T01, P02-T01.

#### Validation Expectations

* `test_progress_dashboard.py` (including repeat-read equality `self.assertEqual(self.report(), baseline)`) and `PYTHONPATH=../core/src:../agents/src python3 -m mypy` inside `src/api` pass cleanly.

#### Completion Evidence

* `GET /api/progress` returns deterministic `ai_consumption_economics` with explicit denominators and `"Unknown"` unpriced/zero-outcome costs.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: End-to-End Invariant and API Regression Tests

### Context

Issue `#100` specifically requires dedicated invariant tests proving that management views expose explicit denominators (`proposal_count`, `accepted_outcome_count`, `metered_call_count`, `unmetered_call_count`) and report `"Unknown"` (never `0` or `0.0`) whenever no price source or no accepted-outcome count exists.

### Intent

Add focused, high-signal invariant tests in `src/core/tests/test_management_tokenomics_invariant_100.py` and `src/api/tests/test_management_tokenomics_api_100.py` covering every management view and every pricing x accepted-outcome x metering-completeness state.

### Boundaries

* Included: `src/core/tests/test_management_tokenomics_invariant_100.py` and `src/api/tests/test_management_tokenomics_api_100.py`.
* Excluded: Deleting or weakening any existing test file.

### Likely Targets

* `src/core/tests/test_management_tokenomics_invariant_100.py`: Core and store-level invariant tests.
* `src/api/tests/test_management_tokenomics_api_100.py`: HTTP endpoint invariant, determinism, read-only sequence, and privacy canary tests.

### Dependencies

* P01, P02.

### Validation Expectations

* Both new test modules fail if any denominator is omitted or if any cost/unit-cost field returns `0`, `0.0`, `"0"`, `"0.0"`, or `None` when unpriced or when `accepted_outcome_count == 0`, and pass against the implementation.

### Completion Evidence

* Full `unittest` discovery passes in both `src/core` and `src/api`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Create `src/core/tests/test_management_tokenomics_invariant_100.py`

#### Context

Core callers consume `tokenomics.summarize_ai_consumption_economics`, `Store.ai_consumption_economics`, `Store.stats`, `Store.progress_report` (+ `progress.export_csv`), `coordinator.read`, and `Store.ai_live_report` on both JSON `Store` and SQLite `SqlStore` with `Assistants`/`Consumption`.

#### Intent

Test and prove:
1. Default empty and seeded store states (`OD-51` open, `price_source_configured=False`, `accepted_outcome_count == 0`): all 4 explicit integer denominators present; all cost and cost-per-accepted-outcome fields equal `"Unknown"` (recursive walk proves zero `0`, `0.0`, `"0"`, `"0.0"`, or `None` values on cost keys).
2. Unpriced store with human-accepted AI outcomes (`price_source_configured=False`, `accepted_outcome_count > 0`): `proposal_count >= accepted_outcome_count >= 1`, workflow/template fallbacks and unreviewed/rejected records excluded from `accepted_outcome_count`, and all cost / cost-per-accepted-outcome fields still `"Unknown"`.
3. Priced + reconciled ledger (`od_51_status="approved"`, dated non-synthetic price + reconciled billing, `price_source_configured=True`) with `accepted_outcome_count == 0` (both positive spend on rejected/unreviewed proposals AND zero-call `$0` bill edge case): all cost-per-accepted-outcome fields (`cost_per_accepted_outcome`, `token_cost_per_accepted_outcome`, `quality_qualified_cost_per_accepted_outcome`, and per-capability `cost_per_accepted_outcome`) equal `"Unknown"`, and zero-call `$0` bill also reports `"Unknown"` rather than `"0"`.
4. Priced + reconciled + complete TCA components + quality-floor `"Pass"` with `accepted_outcome_count > 0`: exact Decimal strings computed for `token_cost`, `total_cost_of_ai`, `token_cost_per_accepted_outcome`, `cost_per_accepted_outcome`, and `quality_qualified_cost_per_accepted_outcome`, while `quality_floor_status != "Pass"` or missing TCA component returns `"Unknown"` for `cost_per_accepted_outcome`, multi-capability cohorts with one zero-accepted capability keep that capability's `cost_per_accepted_outcome == "Unknown"` even when overall `accepted_outcome_count > 0` (`PC-005`), and adding an unmetered AI record (`unmetered_call_count > 0`) immediately downgrades `price_source_configured` to `False` and costs to `"Unknown"`.
5. Ledger hold / schema-unavailable (`ai_consumption.DispatchHeld` and `port.sql = False`) fail-closed resilience (`PC-001`): management views degrade gracefully to `price_source_configured=False` and `"Unknown"` costs instead of crashing `Store.stats()`, `Store.progress_report()`, or `Store.ai_live_report()`.
6. Exact `progress.export_csv` round-trip equality (`decoded == report`).

#### Boundaries

* Included: `src/core/tests/test_management_tokenomics_invariant_100.py`.
* Excluded: HTTP socket/WSGI server routing (covered in P03-T02).

#### Likely Targets

* `src/core/tests/test_management_tokenomics_invariant_100.py`.

#### Dependencies

* P01-T01, P02-T01.

#### Validation Expectations

* `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_management_tokenomics_invariant_100.py' -v` inside `src/core` exits `0`.

#### Completion Evidence

* Passing test output recorded in `.copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-changes.md`.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Create `src/api/tests/test_management_tokenomics_api_100.py`

#### Context

HTTP consumers access management views via `GET /api/stats`, `GET /api/stats?report=progress`, `GET /api/cases.csv?report=progress`, `GET /api/progress`, `GET /api/coordinator`, and manager-only `GET /api/ai/report`.

#### Intent

Exercise `zava_forward.api.server.App` over `SqlStore` across unpriced (`OD-51` open), priced-without-accepted-outcomes (`accepted_outcome_count == 0`), and priced-with-accepted-outcomes states, proving:
1. All six management endpoints expose `ai_consumption_economics` with explicit integer denominators (`proposal_count`, `accepted_outcome_count`, `metered_call_count`, `unmetered_call_count`).
2. Whenever price source or accepted outcomes are absent, cost / cost-per-accepted-outcome fields equal `"Unknown"` (never `0`, `0.0`, `"0"`, `"0.0"`, or `None`).
3. `GET /api/ai/report` retains exact top-level keys `{"evaluation", "chat_evaluation", "live", "registry", "consumption"}` with `ai_consumption_economics` under `report["live"]`.
4. Repeat GET requests return identical payloads, leave `store._db_seq()` and `store.verify_audit()` intact, and leak zero private case/reviewer/email canary substrings across authorised roles.

#### Boundaries

* Included: `src/api/tests/test_management_tokenomics_api_100.py`.
* Excluded: Browser Playwright specs (no `web/` files modified).

#### Likely Targets

* `src/api/tests/test_management_tokenomics_api_100.py`.

#### Dependencies

* P01-T01, P02-T01, P02-T02.

#### Validation Expectations

* `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -p 'test_management_tokenomics_api_100.py' -v` inside `src/api` exits `0`.

#### Completion Evidence

* Passing HTTP test output recorded in `.copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-changes.md`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P04 -->
## P04: Documentation Updates and Focused Validation Gate

### Context

Repository instructions require updating component READMEs when new helpers/contracts are exported and matching `.github/workflows/src-ci.yml` locally for modified `src/<project>` packages (`ruff check`, bare `mypy`, and `unittest` discovery).

### Intent

Document `zava_forward.core.tokenomics` and management-view `ai_consumption_economics` in `src/core/README.md` and `src/api/README.md`, and run all Focused-tier linters, type checks, and unit test suites across `src/core` and `src/api`.

### Boundaries

* Included: `src/core/README.md`, `src/api/README.md`, and local validation runs (`ruff check`, `mypy`, `unittest`, `tools/rename-zava-tests.py`).
* Excluded: Full external `--all` gate (not required for Focused validation tier per caller direction and repository tier rules).

### Likely Targets

* `src/core/README.md`: Document `zava_forward.core.tokenomics` exports, explicit denominators, and fail-closed `"Unknown"` invariants.
* `src/api/README.md`: Note `ai_consumption_economics` presence across management endpoints (`/api/stats`, `/api/stats?report=progress`, `/api/cases.csv?report=progress`, `/api/progress`, `/api/coordinator`, and `/api/ai/report["live"]`).

### Dependencies

* P01, P02, P03.

### Validation Expectations

* `python3 -m ruff check src/core src/api` exits `0`.
* `(cd src/core && python3 -m mypy)` exits `0`.
* `(cd src/api && PYTHONPATH=../core/src:../agents/src python3 -m mypy)` exits `0`.
* `(cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -q)` exits `0`.
* `(cd src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q)` exits `0`.

### Completion Evidence

* Clean command exit codes and test counts captured in `.copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Update `src/core/README.md` and `src/api/README.md` and run `ruff`, `mypy`, and `unittest`

#### Context

Prompt requirement 4 specifies updating `src/core/README.md` if a new helper is exported, and requirement 5 specifies running `ruff check`, `mypy`, and `unittest` in `src/core` (and `src/api` if modified).

#### Intent

Update both component READMEs concisely in repository Markdown style (`*` unordered lists, plain ASCII punctuation, no `.copilot-tracking/` links) and execute the complete Focused validation commands.

#### Boundaries

* Included: `src/core/README.md`, `src/api/README.md`, and validation runs.
* Excluded: Unrelated README sections or web UI docs.

#### Likely Targets

* `src/core/README.md`
* `src/api/README.md`

#### Dependencies

* P01, P02, P03.

#### Validation Expectations

* Zero `ruff`, `mypy`, or `unittest` failures; Markdown diff contains no `.copilot-tracking/` paths or non-ASCII punctuation regressions.

#### Completion Evidence

* README diffs verified via `git diff` and validation results logged in `.copilot-tracking/changes/2026-11-15/insight-100-mgmt-tokenomics-changes.md`.

#### Unresolved Items

* None.
