---
title: "Task Research: 111-reproducible-outputs"
description: "End-to-end deterministic sensor analysis, SENSOR_REVIEW_DUE task derivation, and replay digests from retained readings across Store and SqlStore (Refs #111)"
ms.date: 2026-11-15
---

| Field | Value |
| --- | --- |
| Date | 2026-11-15 |
| Researcher / agent | rpi-research (RPI Agent) |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-11-15/111-reproducible-outputs-research.md |

## Research Brief

* What to research: How `src/core` reproduces deterministic versioned sensor analysis outputs (`Signal`, `VersionProvenance`), `SENSOR_REVIEW_DUE` task candidates (`ReviewTaskCandidate`) and case-local review drafts, and canonical replay digests from retained readings across both in-memory/JSON `Store` and `SqlStore` under arbitrary SQL row ordering, duplicate/out-of-order retained-reading replay, and stale/missing `INSUFFICIENT` fallbacks.
* Why it matters: Issue #111's first remaining acceptance criterion (`Outputs are reproducible from retained readings`), PRD FR-050 / AC-067 / AC-068, and ADR 0003 decision 6 require every derived sensor signal, `SENSOR_REVIEW_DUE` proposal, and digest to be a deterministic pure function of the retained reading set, recorded home consent, window, `as_of`, and versioned `AnalysisPolicy`, without mutating portfolio priority or generating duplicate review tasks.
* Audience or intended use: `rpi-plan`, `rpi-implement`, and `rpi-review` on branch `feat/iot-111-reproducible-outputs` targeting `feat/demo-164-chat-grounding-provenance-0900` (#1641).
* Scope: `src/core/src/zava_forward/core/sensor_analysis.py`, `sensor_analysis_store.py`, `sensor_consumer.py`, `sensor_review_draft.py`, `sqlstore.py` / `store.py` read-only inspection, and new focused unit suite `src/core/tests/test_sensor_reproducibility_111.py`.
* Non-goals: Modifying `README.md` (root or `src/core/README.md`), `server.py`, or `test_role_endpoint_inventory.py` (prohibited by caller for conflict-free sibling-PR merge); modifying `pyproject.toml`; completing R1-R3 standards research or replacing `EXERCISE VALUE` labels; live Azure SQL / IoT Hub provisioning; pushing to remote.
* Criteria: 100% reproducible `Signal`, `ReviewTaskCandidate` (`SENSOR_REVIEW_DUE`), `VersionProvenance`, `input_digest`, `policy_digest`, `output_digest`, and case-local `sensor_review_drafts` across both `Store` and `SqlStore`; invariance to arbitrary SQL row order and exact-duplicate/out-of-order retained-reading replay; fail-closed `INSUFFICIENT` on conflicting duplicates, stale/missing readings, weather-only windows, or withheld/unconfigured consent without mutating ranking/priority or creating duplicate tasks; clean `unittest`, `ruff check`, `ruff format --check`, strict `mypy`, and `tools/rename-zava-tests.py`.
* Requested outputs: Dated primary research artifact with convergence recommendation for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field | Value |
| --- | --- |
| Research question(s) | Q1-Q4 below |
| Codebase scope | `src/core/`, `src/api/tests/test_sensor_*`, `tools/rename-zava-tests.py`, `docs/adrs/0003-*`, `docs/prds/zava-forward-*`, `docs/reference/research/iot-sensor-analytics-research-plan.md` |
| External scope | none (bounded internal repository specification and codebase slice) |
| Initial internal candidate areas | `src/core/src/zava_forward/core/sensor_analysis.py`, `sensor_analysis_store.py`, `sensor_review_draft.py`, `sensor_consumer.py`, `sqlstore.py`, `store.py` |
| Initial external candidate areas | none |
| Research posture | focused |
| Posture provenance | default (bounded internal task with named modules, explicit conflict-free file boundaries, and exact validation commands) |
| Explicit limits / deadline | Do not modify `README.md`, `server.py`, or `test_role_endpoint_inventory.py`; add focused tests in `src/core/tests/test_sensor_reproducibility_111.py`; do not push |
| Posture-specific completion basis | focused scope and materiality |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | `.copilot-tracking/` |
| Known constraints / excluded sources | Keep `EXERCISE VALUE` threshold labels; keep `SensorConsumer(json_store)` raising `UNSUPPORTED_STORE_SQL_REQUIRED`; keep unconfigured JSON `Store` failing closed (`consent-withheld` / `RETAINED_READINGS_UNAVAILABLE`); preserve `mock.patch.object(srd, "SensorConsumer")` on `SqlStore` |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | `.github/copilot-instructions.md` | `applyTo: "**"` matches workspace and `.copilot-tracking/` | Enforces AMA knowledge-base reading, tier classification disclosure, privacy-safe Git email, `Refs #111` discipline, and ASCII Markdown rules | Selected: mandatory repository governance |
| Skill | `python-foundational` | Python strict typing and `unittest` conventions | Typed Python 3.12 and `unittest` guidance | Skipped: `src/core/pyproject.toml` already enforces strict `mypy` and `ruff` rules directly |
| Research specialist | `hve-core-all:rpi-researcher` | General internal research lane worker | Compact subagent lane artifact | Skipped: inline fallback used because all target `src/core` modules are tightly coupled and directly readable in single context |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision or selected further research |
| --- | --- | --- | --- |
| Intake | Non-interactive confirmed automatic RPI run with explicit scope, file exclusions, target test path, validation commands, and no-push rule | No interaction needed | Execute full automatic RPI loop (`Research` -> `Plan` -> `Implement` -> `Review`) with `focused` research posture |
| Direction change | Caller prohibits editing `README.md`, `server.py`, and `test_role_endpoint_inventory.py` for conflict-free sibling-PR merge | Active caller constraint | Keep all implementation edits inside `src/core/src/zava_forward/core/sensor_*.py` and `src/core/tests/test_sensor_reproducibility_111.py` without touching `pyproject.toml` or `README.md` |
| Convergence | Cycle 1 answered Q1-Q4 completely from primary code, specs, and baseline test/type/lint execution | No interaction needed | Advance automatically to `rpi-plan` |

## Scope and Success Criteria

* Scope: Deterministic versioned sensor analysis, `SENSOR_REVIEW_DUE` task candidate and case-local draft derivation, and replay digests from retained readings across both in-memory/JSON `Store` and `SqlStore`.
* Assumptions: Verified against baseline command execution in this worktree (`299` sensor tests passing with `34` live-MSSQL skips, `341` `mypy` files clean, `287` `ruff format` files clean, `25` `rename-zava-tests` passing).
* Success criteria:
  * Every research question is answered with `C#` `path:line` evidence.
  * Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs.
  * Contrarian checks verify backwards compatibility with all existing `src/core/tests/` and `src/api/tests/` contracts.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Inspect `sensor_analysis.py`, `sensor_review_draft.py`, `sqlstore.py`, and `test_sensor_analysis*.py`; ensure 100% reproducible deterministic versioned sensor analysis outputs, `SENSOR_REVIEW_DUE` task derivation, and replay digests from retained readings across both in-memory/JSON `Store` and `SqlStore` (including arbitrary SQL row ordering, duplicate/out-of-order retained-reading replay, and stale/missing `INSUFFICIENT` fallback without mutating priority or generating duplicate tasks); add focused unit tests in `src/core/tests/test_sensor_reproducibility_111.py`; run the three focused validation commands; commit locally with `Refs #111` and Copilot trailer without pushing.
* Inferred research questions: Where do `sensor_analysis.py`, `sensor_consumer.py`, `sensor_analysis_store.py`, and `sensor_review_draft.py` diverge across exact-duplicate retained-reading replay, SQL tie ordering, and JSON `Store` vs `SqlStore` retained-reading access, and how do `Store._ranking()` and `SqlStore._row()` prove priority non-mutation?
* Caller constraints and non-goals: Do not edit `README.md`, `server.py`, or `test_role_endpoint_inventory.py`; do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint | Effect on active brief, evidence, or revalidation |
| --- | --- | --- | --- |
| exclude | Do not modify `README.md`, `server.py`, or `test_role_endpoint_inventory.py` | Caller prompt | Restricts changes to `src/core` sensor modules and `src/core/tests/test_sensor_reproducibility_111.py` |
| exclude | Do not push to remote; exit `0` with clean `git status --short` | Caller prompt | Routes external Full SQL gate (`ZF_SENSOR_MSSQL=1` + `tools/rpi-checks.py --all`) and hosted CI to pre-publication follow-up |

## Research Questions

| # | Sub-question | Type (depth / breadth / straightforward) | Priority | Status |
| ---: | --- | --- | --- | --- |
| Q1 | How does `sensor_analysis.py` handle out-of-order rows, exact-duplicate retained-reading replays, and conflicting duplicate readings across `derive_signal`, `reading_tuples`, `reproduce_sensor_analysis`, and `reproduce_review_task`? | depth | H | answered |
| Q2 | Does `SqlStore` / `SensorConsumer.retained_envelopes` guarantee deterministic row ordering and invariance under arbitrary SQL cursor row ordering? | depth | H | answered |
| Q3 | How can retained sensor readings and home consent be stored and replayed on in-memory/JSON `Store` with 100% parity to `SqlStore` across `sensor_analysis_store` and `sensor_review_draft` without breaking existing fail-closed JSON/SQL/API tests or `mypy --strict`? | depth | H | answered |
| Q4 | Do `Signal`, `ReviewTaskCandidate`, `INSUFFICIENT`/`STALE`/`DECLINED` fallbacks, or persisted `sensor_review_drafts` ever mutate case priority/ranking or create duplicate tasks in `Store` or `SqlStore`? | straightforward | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-research.md`, `.copilot-tracking/reviews/2026-11-14/111-sensor-reproducibility-2142-review.md`, `.copilot-tracking/reviews/2026-11-14/111-sensor-reproducibility-2142-c2-review.md`, `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/reference/research/iot-sensor-analytics-research-plan.md`.
* Reused (verified) findings: `VersionProvenance`, `policy_digest`, `output_digest`, `reproduce_review_task`, and `sensor_analysis_store.reproduce_retained` were landed in `745d1cf53` (#1741) for pure reading lists and `SensorConsumer`-backed SQL stores (C2, C3); `sensor_view.rows_digest` already establishes the repository convention that exact retained-reading order and repeats do not change canonical input digests (C9).
* Superseded / stale: Prior `111-sensor-reproducibility-2142` assumed retained-store reproduction was SQL-only (`SensorConsumer`) and assumed `_by_observation` only needed sorting rather than exact-replay set canonicalization; it also left `ORDER BY observed_at, sensor_id` without `reading_id` tie-breaking in `SensorConsumer.retained_envelopes` (C2, C3, C5).

## Research Cycle Log

### Cycle 1

* Active direction controls: exclude (`README.md`, `server.py`, `test_role_endpoint_inventory.py`), exclude (no push)
* Active research posture and completion basis: focused; focused scope and materiality
* Explicit limits or deadline effect: Keeps changes surgical within `src/core` while preserving zero-conflict boundaries with sibling PRs.

#### Wave 1: Wider

* Plan and independent lanes: Inspect Issue #111, PRD FR-050/AC-067/AC-068, ADR 0003 decision 6, `sensor_analysis.py`, `sensor_analysis_store.py`, `sensor_review_draft.py`, `sensor_consumer.py`, `sensor_view.py`, `store.py`, `sqlstore.py`, `pyproject.toml`, and existing `src/core/tests/test_sensor*.py` + `src/api/tests/test_sensor*.py`.
* Worker evidence relationships or inline fallback: Inline reads mapped Q1-Q4 -> C1-C12.
* Reflection: Pure `VersionProvenance` and SQL `SensorConsumer` reproduction exist, but three concrete cross-store and replay gaps remain across `sensor_analysis.py`, `sensor_consumer.py`, `sensor_analysis_store.py`, and `sensor_review_draft.py`.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Trace (1) `_by_observation`, `_row_digest_tuples`, and `comparator.analyse` on exact-duplicate replays vs conflicting duplicates, (2) `SensorConsumer.retained_envelopes` SQL `ORDER BY` and cursor ordering, (3) `Store` vs `SqlStore` paths in `sensor_analysis_store.py` and `sensor_review_draft.py`, and (4) `Store._ranking()` and `SqlStore._row()` ranking inputs.
* Plan and independent lanes: Line-by-line trace of `sensor_analysis.py:259-385`, `sensor_scenarios.py:116-165`, `sensor_consumer.py:958-1172`, `sensor_analysis_store.py:28-69`, `sensor_review_draft.py:165-365`, `store.py:114-215`, and `sqlstore.py:976-988`.
* Worker evidence relationships or inline fallback: Inline trace mapped Q1 -> C2, C4, C9; Q2 -> C5; Q3 -> C3, C6, C7, C10, C11, C12; Q4 -> C6, C7, C8.
* Reflection:
  1. `_by_observation` sorts rows without collapsing byte-identical retained-reading replays (`(_canonical_row(r), _schema_marker(r))`), so replaying an identical retained reading in a retained list changes `_digest` and causes `comparator.analyse` to emit `DUPLICATE`/`OUT_OF_ORDER` -> `INSUFFICIENT` (C2, C4).
  2. `SensorConsumer.retained_envelopes` orders by `observed_at, sensor_id` without `reading_id` tie-breaking (C5).
  3. `sensor_analysis_store.analyse_retained` and `reproduce_retained` accept only `SensorConsumer`, not `SqlStore` or JSON/in-memory `Store`, and JSON `Store` lacks a canonical retained-reading carrier (`store.data["sensor_retained"]`) that works across `analyse_retained`, `reproduce_retained`, `read_drafts`, and `draft_from_retained` (C3, C6, C7).
  4. Unconfigured `SqlStore` returns `refusal="SIGNAL_INSUFFICIENT"` in `draft_from_retained` because `analyse_retained` catches `ConsumerError` and returns `reasons=("RETAINED_READINGS_UNAVAILABLE",)`, whereas unconfigured JSON `Store` returns `refusal="RETAINED_READINGS_UNAVAILABLE"` (C3, C6).

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge whether deduplicating replays or adding JSON `Store` retained-reading support could break ANY existing unit/API test or mask genuine sensor data conflicts, or violate `mypy --strict` without touching `pyproject.toml`.
* Plan and independent lanes: Check all 4 critical contrarian hazards:
  1. `test_sensor_scenarios.py:163` calls `ss.analyse((rows[0], *rows), self.window)` expecting `INSUFFICIENT`, and `test_sensor_analysis.py:296-309` passes `dup_a`/`dup_b` (same `observed_at`, different `reading_id` and payload) expecting distinct `valid` and `input_digest`.
  2. `test_sensor_consumer.py` asserts `SensorConsumer(json_store)` raises `ConsumerError("UNSUPPORTED_STORE_SQL_REQUIRED")`.
  3. `test_sensor_review_draft.py:372-382` (`JsonDraftCases`) asserts unconfigured JSON `Store` returns `("consent-withheld", [])` on `read_drafts` and `refusal == "RETAINED_READINGS_UNAVAILABLE"` on `draft_from_retained`.
  4. `src/api/tests/test_sensor_review_draft_api.py:143` patches `mock.patch.object(srd, "SensorConsumer")` on `SqlStore`, and `src/core/pyproject.toml:147` scopes `disallow_untyped_calls = false` only to `sensor_review_draft` (not `sensor_analysis_store` or `test_sensor_reproducibility_111`).
* Worker evidence relationships or inline fallback: Contrarian checks confirmed every constraint (C4, C5, C6, C10, C11, C12) and shaped the exact design so zero existing contracts break.
* Reflection:
  * Deduplicating ONLY exact-identical rows keyed by `(type(r.get("home_id")).__qualname__, _canonical_row(r), _schema_marker(r))` inside `sensor_analysis.py` (`_dedupe_exact_rows` / `_by_observation` / `reading_tuples`) leaves `ss.analyse` untouched (`test_sensor_scenarios.py:163` passes) AND keeps conflicting rows (`dup_a`/`dup_b` or same `(sensor_id, reading_id)` with differing values) intact so `comparator.analyse` still fails closed with `DUPLICATE` -> `INSUFFICIENT`!
  * Keeping `SensorConsumer.__init__` SQL-only preserves `UNSUPPORTED_STORE_SQL_REQUIRED`, while adding `JsonRetainedStore` + `retain_json_readings` + `retained_source` in `sensor_analysis_store.py` (failing closed with `ConsumerError("RETAINED_READINGS_UNAVAILABLE")` whenever `"sensor_retained"` is absent from `store.data`) preserves `JsonDraftCases` when unconfigured AND gives 100% parity with `SqlStore` when configured!
  * Keeping `SensorConsumer(store)` for `_sql(store)` in `sensor_review_draft.py` preserves `mock.patch.object(srd, "SensorConsumer")` in `src/api/tests/test_sensor_review_draft_api.py:143`, and mapping `signal.reasons == (UNAVAILABLE,)` to `_refusal("RETAINED_READINGS_UNAVAILABLE")` aligns unconfigured `SqlStore` and unconfigured `Store`!
  * Using structural `Protocol` typing in `sensor_analysis_store.py` and typed factory helpers in `test_sensor_reproducibility_111.py` satisfies `mypy --strict` with zero `# type: ignore` comments and zero edits to `pyproject.toml`.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment |
| --- | --- | --- | --- | --- |
| Canonicalize exact-duplicate retained-reading replays in `sensor_analysis.py` (`_by_observation` and `reading_tuples`) while preserving conflicting duplicates for fail-closed `DUPLICATE` detection | C2, C4, C9 | accepted | Makes `Signal`, `ReviewTaskCandidate`, `input_digest`, and `output_digest` true functions of the retained reading set without masking conflicting rows or altering `ss.analyse` | Selected recommendation |
| Add `reading_id` tie-breaker to `SensorConsumer.retained_envelopes` SQL `ORDER BY observed_at, sensor_id, reading_id` | C5 | accepted | Eliminates unspecified SQL row order when two retained rows share `(observed_at, sensor_id)` while `derive_signal` also remains order-invariant | Selected recommendation |
| Add `RetainedReadingSource` protocol, `JsonRetainedStore`, `retain_json_readings`, and `retained_source` in `sensor_analysis_store.py`, and wire `sensor_review_draft.py` to support configured JSON `Store` alongside `SqlStore` | C3, C6, C7, C10, C11, C12 | accepted | Enables 100% identical retained-reading analysis, `SENSOR_REVIEW_DUE` candidate/draft derivation, and replay digests across `Store` and `SqlStore` while keeping unconfigured stores fail-closed and preserving `SensorConsumer` SQL-only + API mock contracts | Selected recommendation |
| Modify `SensorConsumer.__init__` to accept JSON `Store` directly | C5, C10 | rejected | Breaks `test_sensor_consumer.py` assertions requiring `UNSUPPORTED_STORE_SQL_REQUIRED` for SQL ingestion durability | Alternative 1 rejected |
| Deduplicate rows by `(sensor_id, reading_id)` or `observed_at` discarding conflicting payloads | C2, C4, C9 | rejected | Silently drops conflicting observations instead of failing closed to `INSUFFICIENT` (`DUPLICATE`) and breaks `test_sensor_analysis.py:296-309` | Alternative 2 rejected |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: All four research questions (Q1-Q4) are answered with high-confidence primary codebase evidence (`C1`-`C12`) and verified baseline tool runs.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: bounded four-module `src/core` slice where tight cross-module contracts (`sensor_analysis`, `sensor_analysis_store`, `sensor_consumer`, `sensor_review_draft`, `store`, `sqlstore`) fit direct single-context verification.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | PRD FR-050, AC-067, AC-068 and ADR 0003 decision 6 require versioned sensor signals and `SENSOR_REVIEW_DUE` proposals reproducible from retained readings, labelled sufficiency, no priority reduction on `INSUFFICIENT`/`STALE`/`DECLINED`, and no raw readings or sensor IDs in outputs | `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:149` | view | high | Confirmed with `docs/prds/zava-forward-retrofit-programme-demonstrator.md:384` |
| C2 | `_by_observation` sorts by `(observed_at, _canonical_row)` without collapsing exact-identical retained-reading replays, causing `_row_digest_tuples` and `comparator.analyse` to treat exact replays as `DUPLICATE`/`OUT_OF_ORDER` and alter `input_digest` | `src/core/src/zava_forward/core/sensor_analysis.py:272` | view | high | Lines 272-383 |
| C3 | `sensor_analysis_store.analyse_retained` and `reproduce_retained` accept only `SensorConsumer` (SQL-only), not `SqlStore` or JSON/in-memory `Store` | `src/core/src/zava_forward/core/sensor_analysis_store.py:29` | view | high | Lines 29-69 |
| C4 | `sensor_scenarios.analyse` directly tests raw sequence discipline (`test_sensor_scenarios.py:163` expects `INSUFFICIENT` on `(rows[0], *rows)`), while `test_sensor_analysis.py:296` expects conflicting same-timestamp rows (`dup_a` vs `dup_b`) to remain distinct | `src/core/tests/test_sensor_scenarios.py:163` | view | high | Confirmed with `src/core/tests/test_sensor_analysis.py:296` |
| C5 | `SensorConsumer.__init__` rejects non-SQL stores with `UNSUPPORTED_STORE_SQL_REQUIRED`, `process()` handles SQL delivery replays idempotently (`replay=True`), and `retained_envelopes` queries `ORDER BY observed_at, sensor_id` without `reading_id` | `src/core/src/zava_forward/core/sensor_consumer.py:389` | view | high | Confirmed at lines 389-393, 958-994, and 1079 |
| C6 | `sensor_review_draft.py` gates `read_drafts` and `draft_from_retained` through `SensorConsumer(store)` only, deduplicates persisted drafts by `candidate.task_key`, and never creates operational tasks or alters ranking | `src/core/src/zava_forward/core/sensor_review_draft.py:166` | view | high | Lines 166-365 |
| C7 | `Store` persists `self.data` atomically to `live.json` in `save()` and computes `_ranking()` purely from open `self.cases` via `ranking.rank(..., ranking.CURRENT)` | `src/core/src/zava_forward/core/store.py:114` | view | high | Confirmed at lines 114-120 and 207-212 |
| C8 | `SqlStore._row(c)` derives `rkey` (`ranking.sql_key(c)`), `hazard`, `support`, `days`, and `priority_correction` without reading `sensor_review_drafts` or any `sensor_*` table, and `projection.py` strips `sensor_review_drafts` from generic case detail | `src/core/src/zava_forward/core/sqlstore.py:977` | view | high | Confirmed with `src/core/src/zava_forward/core/projection.py:1` and `src/api/tests/test_sensor_non_authority_boundary.py:194` |
| C9 | `sensor_view.rows_digest` and `test_sensor_view_reproducibility.py:21` establish that canonical retained-reading digests ignore row order and exact repeats (`rows + rows[:3]`) while changing on any value or membership change | `src/core/src/zava_forward/core/sensor_view.py:523` | view | high | Confirmed with `src/core/tests/test_sensor_view_reproducibility.py:21` |
| C10 | `test_sensor_consumer.py` explicitly asserts `SensorConsumer(json_store)` raises `ConsumerError("UNSUPPORTED_STORE_SQL_REQUIRED")`, and `JsonDraftCases` in `test_sensor_review_draft.py:372` asserts unconfigured JSON `Store` returns `consent-withheld` and `RETAINED_READINGS_UNAVAILABLE` | `src/core/tests/test_sensor_review_draft.py:372` | grep / view | high | Confirmed with grep on `src/core/tests/test_sensor_consumer.py` |
| C11 | `src/api/tests/test_sensor_review_draft_api.py:143` patches `mock.patch.object(srd, "SensorConsumer")` on a `SqlStore`-backed `App` to simulate granted consent during `GET /api/cases/{cid}/sensor-drafts` | `src/api/tests/test_sensor_review_draft_api.py:143` | view | high | Must keep `SensorConsumer(store)` call path on `srd` when `_sql(store)` is `True` |
| C12 | `src/core/pyproject.toml` runs `mypy` with `strict = true` across `src` and `tests`, exempting `disallow_untyped_calls` only for named modules (not `sensor_analysis_store` or new test modules) | `src/core/pyproject.toml:34` | view | high | Verified via clean baseline `mypy` (341 files), `ruff`, and `rename-zava-tests` (25 tests) |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
| --- | --- | --- | --- | --- | --- | --- |

### Contradictions / Conflicts

* none

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
| --- | --- | --- | --- | --- |
| Q1 | `sensor_analysis.py` sorts by `(observed_at, _canonical_row)` but does not collapse byte-identical retained-reading replays; deduplicating exact canonical+schema-identical rows in `_by_observation` and `reading_tuples` makes signals, candidates, and digests idempotent under replay while preserving conflicting duplicates as `INSUFFICIENT` (`DUPLICATE`). | C2, C4, C9 | high | Update `_dedupe_exact_rows` / `_by_observation` and `reading_tuples` in `sensor_analysis.py`. |
| Q2 | `SensorConsumer.retained_envelopes` lacks `reading_id` in `ORDER BY observed_at, sensor_id`, leaving same-timestamp same-sensor rows subject to SQL physical order; adding `reading_id` makes SQL extraction deterministic while `derive_signal` guarantees invariance even if a SQL cursor returns arbitrary row order. | C2, C5 | high | Update `ORDER BY observed_at, sensor_id, reading_id` in `sensor_consumer.py` and test shuffled/reversed SQL row order in `test_sensor_reproducibility_111.py`. |
| Q3 | Adding `RetainedReadingSource`, `JsonRetainedStore`, `retain_json_readings`, and `retained_source` in `sensor_analysis_store.py` (backed by `store.data["sensor_retained"]` when configured and failing closed with `ConsumerError("RETAINED_READINGS_UNAVAILABLE")` when absent) plus wiring `sensor_review_draft.py` achieves 100% parity between `Store` and `SqlStore` without breaking `UNSUPPORTED_STORE_SQL_REQUIRED`, `JsonDraftCases`, `DraftApi`, or `mypy --strict`. | C3, C5, C6, C7, C10, C11, C12 | high | Implement typed JSON retained-reading adapter in `sensor_analysis_store.py` and connect `sensor_review_draft.py`. |
| Q4 | Neither `Signal`, `ReviewTaskCandidate`, `INSUFFICIENT`/`STALE`/`DECLINED` fallbacks, nor persisted `sensor_review_drafts` ever mutate `Store._ranking()` or `SqlStore._row()`/`rkey`/`priority_correction`/`queue_*`, and `_persist` deduplicates drafts by `candidate.task_key` across replays and `as_of` shifts. | C1, C6, C7, C8 | high | Lock cross-store ranking non-mutation and zero-duplicate-task invariants in `test_sensor_reproducibility_111.py`. |

## Key Discoveries

* Exact-duplicate retained-reading replay vs conflicting duplicate observations can be separated cleanly by keying exact deduplication on `(type(row.get("home_id")).__qualname__, _canonical_row(row), _schema_marker(row))`: byte-and-type-identical retained reading replays collapse idempotently, whereas any conflicting value, `reading_id`, extra field, or non-string type remains distinct and triggers fail-closed `INSUFFICIENT` (C2, C4).
* JSON/in-memory `Store` already atomically persists top-level `self.data` keys to `live.json` on `save()`; storing configured exercise controls and canonical retained reading envelopes under `store.data["sensor_retained"]` (with idempotent exact-replay acceptance and `IDENTITY_CONFLICT` rejection on conflicting `(sensor_id, reading_id)`) gives `Store` complete parity with `SqlStore` across `analyse_retained`, `reproduce_retained`, `read_drafts`, and `draft_from_retained`, while an unconfigured `Store` continues to raise `ConsumerError("RETAINED_READINGS_UNAVAILABLE")` (C3, C6, C7, C10).
* Keeping `SensorConsumer(store)` as the `_sql(store)` reader in `sensor_review_draft.py` preserves `src/api/tests/test_sensor_review_draft_api.py`'s `mock.patch.object(srd, "SensorConsumer")` seam, while normalizing `signal.reasons == (UNAVAILABLE,)` in `_from_retained` ensures unconfigured `SqlStore` and unconfigured `Store` return the exact same `"RETAINED_READINGS_UNAVAILABLE"` refusal (C6, C11).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach:
  1. In `sensor_analysis.py`, add `_dedupe_exact_rows` (keyed by exact runtime types, canonical JSON, and `_schema_marker`) and apply it in `_by_observation` and `reading_tuples` so out-of-order and exact-duplicate retained-reading replays produce identical `Signal`, `ReviewTaskCandidate`, `VersionProvenance`, `input_digest`, and `output_digest`, while conflicting duplicates still fail closed to `INSUFFICIENT` (`DUPLICATE`).
  2. In `sensor_consumer.py`, extend `retained_envelopes` SQL ordering to `ORDER BY observed_at, sensor_id, reading_id`.
  3. In `sensor_analysis_store.py`, define `RetainedReadingSource` (`Protocol`), `JsonRetainedStore`, `retain_json_readings`, and `retained_source`, and widen `analyse_retained` and `reproduce_retained` to accept `SensorConsumer | SqlStore | Store | RetainedReadingSource`.
  4. In `sensor_review_draft.py`, route non-SQL `Store` reads/writes through `retained_source(store)` (keeping `SensorConsumer(store)` for `_sql(store)`) and map `(UNAVAILABLE,)` signals in `_from_retained` to `_refusal("RETAINED_READINGS_UNAVAILABLE")`.
  5. Add comprehensive cross-store unit tests in `src/core/tests/test_sensor_reproducibility_111.py` covering `Store` vs `SqlStore` byte-for-byte parity, arbitrary SQL cursor row ordering, duplicate/out-of-order retained-reading replay, reload durability, stale/missing/declined/weather-only/conflicting `INSUFFICIENT` fallbacks, ranking/priority non-mutation, and idempotent `SENSOR_REVIEW_DUE` task/draft deduplication.
* Rationale: Delivers every requirement of Issue #111 criterion 1 across `Store` and `SqlStore` with zero breaking changes to existing `src/core` or `src/api` suites and zero conflict-prone edits to `README.md`, `server.py`, `test_role_endpoint_inventory.py`, or `pyproject.toml`.
* Evidence refs: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12
* Implementation impact: 4 existing `src/core` modules (`sensor_analysis.py`, `sensor_consumer.py`, `sensor_analysis_store.py`, `sensor_review_draft.py`) and 1 new test module (`src/core/tests/test_sensor_reproducibility_111.py`).
* Confidence: high: all code paths, types, and caller contracts were verified directly against the worktree.

File tree:

```text
src/core/
  src/zava_forward/core/
    sensor_analysis.py          (modify: exact-replay set canonicalization)
    sensor_analysis_store.py    (modify: Store/SqlStore RetainedReadingSource + JsonRetainedStore)
    sensor_consumer.py          (modify: deterministic reading_id SQL tie-break)
    sensor_review_draft.py      (modify: cross-store retained reader + unavailable refusal parity)
  tests/
    test_sensor_reproducibility_111.py (create: focused cross-store reproducibility suite)
```

### Alternative: Make `SensorConsumer` Accept JSON `Store` Directly

* Approach: Implement JSON file storage inside `SensorConsumer` and remove the `UNSUPPORTED_STORE_SQL_REQUIRED` guard in `SensorConsumer.__init__`.
* Trade-offs: Single ingestion class, but conflates transactional SQL ingestion/acknowledgement semantics with JSON retained-reading fixtures.
* Evidence refs: C5, C10
* Rejection rationale: Directly breaks `test_sensor_consumer.py` contracts that require `SensorConsumer(json_store)` to raise `ConsumerError("UNSUPPORTED_STORE_SQL_REQUIRED")`.

### Alternative: Deduplicate Readings by `(sensor_id, reading_id)` or `observed_at` Only

* Approach: Keep the first or last row per `(sensor_id, reading_id)` or `observed_at` regardless of payload differences.
* Trade-offs: Simpler key tuple, but silently masks corrupted or conflicting duplicate retained rows.
* Evidence refs: C2, C4, C9
* Rejection rationale: Violates fail-closed safety rules and breaks `test_sensor_analysis.py:296-309` (`dup_a` vs `dup_b`), where conflicting rows at the same timestamp must fail closed to `INSUFFICIENT` (`DUPLICATE`) with distinct `input_digest`s.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Validation-tier classification under `.github/copilot-instructions.md` and `src/README.md`: touching `sensor_analysis.py` / `sensor_consumer.py` places final PR merge/publication in the Full SQL tier (`tools/rpi-checks.py --all` with live `ZF_SENSOR_MSSQL=1` and verified external receipt plus hosted CI), which cannot be pushed in this session because the caller explicitly instructed `Do NOT push`. Record this transparently in changes/review follow-ups (`Refs #111`).
* Follow-up: Analytics research phases R1-R3 (`docs/reference/research/iot-sensor-analytics-research-plan.md`) remain open before replacing `EXERCISE VALUE` thresholds or approving an operational rule (`Refs #111`).
* Residual uncertainty: none within local `Store` and SQLite-backed `SqlStore` scope.

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
| --- | --- | --- | --- | --- | --- |
| Canonicalize exact-identical retained-reading replays while keeping conflicting duplicates fail-closed | confirmed | evidence | Satisfies set-based replay reproducibility without weakening `DUPLICATE` fault detection | C2, C4, C9 | Apply in `sensor_analysis.py` (`_by_observation` and `reading_tuples`) |
| Support retained readings on JSON `Store` via `JsonRetainedStore` + `retain_json_readings` while keeping unconfigured `Store` fail-closed and `SensorConsumer` SQL-only | confirmed | evidence / constraint | Gives 100% `Store` and `SqlStore` parity while preserving `test_sensor_consumer.py`, `JsonDraftCases`, and `DraftApi` | C3, C5, C6, C7, C10, C11 | Implement in `sensor_analysis_store.py` and `sensor_review_draft.py` |
| Do not touch `README.md`, `server.py`, `test_role_endpoint_inventory.py`, or `pyproject.toml` | confirmed | user | Guarantees conflict-free merge with sibling PRs and strict `mypy` compliance via `Protocol` typing | C12 | Put all new tests in `src/core/tests/test_sensor_reproducibility_111.py` |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
| --- | --- | --- | --- | --- |
| Operational sensor threshold approval (R1-R3) | Primary-standards synthesis and named domain reviewer sign-off | Research / domain reviewer | Keeps `EXERCISE VALUE` labels and `Refs #111` (not `Closes #111`) | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
| --- | --- | --- | --- | --- | --- |
| M | Analytics research phases R1-R3 (`docs/reference/research/iot-sensor-analytics-research-plan.md`) | Replaces fictional exercise humidity/staleness thresholds with sourced building-physics criteria | Operational rule sign-off workstream (#111 criterion 3) | deferred | C1 |

## Planning Readiness

* Status: Ready
* Decision state: Convergence recommendation selected for cross-store retained-reading reproducibility in `src/core`.
* Evidence basis: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12
* Preconditions met: All target modules inspected; baseline `unittest`, `ruff`, `mypy`, and `rename-zava-tests` verified clean; sibling-PR conflict boundaries locked.
* Blockers: none
* Smallest action to change readiness: none (Ready for `rpi-plan`)

## Closeout Record

| Field | Record |
| --- | --- |
| Research execution status | Complete |
| Completed waves | Cycle 1: Wider, Deeper, and Contrarian |
| Lane evidence or inline fallback | Inline single-context inspection across coupled `src/core` sensor and store modules |
| Research disposition | executed |
| Planning Readiness | Ready (C1-C12) |
| Blockers | none |
| Continuation owner and state | Confirmed automatic RPI Agent; automatic continuation to `Plan` |

## Advisory Next Step

| Field | Record |
| --- | --- |
| Research disposition | executed |
| Planning Readiness | Ready (C1-C12) |
| Output mode and planning support | convergence; yes, single evidence-backed design selected |
| Acting owner | confirmed automatic RPI Agent |
| Required gates or confirmations | Cycle 1 three-wave completion passed; Planning Readiness `Ready` passed; pre-transition state write next |
| Continuation result | automatic continuation to `rpi-plan` |
| Primary evidence file | .copilot-tracking/research/2026-11-15/111-reproducible-outputs-research.md |
| Notes for planning or re-entry | Preserve `UNSUPPORTED_STORE_SQL_REQUIRED`, unconfigured `JsonDraftCases`, `mock.patch.object(srd, "SensorConsumer")`, strict `mypy` without `pyproject.toml` edits, and zero edits to `README.md`, `server.py`, or `test_role_endpoint_inventory.py`. |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: Focused scope covered completely with primary codebase evidence (`C1`-`C12`); further research within this slice would be redundant.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
