<!-- markdownlint-disable-file -->
# RPI Plan: Deterministic Sensor Analysis, Review Task, and Digest Reproducibility Across Store and SqlStore

## Task Metadata

* Task ID: 111-reproducible-outputs
* Task slug: 111-reproducible-outputs
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/111-reproducible-outputs-plan-critique.md

## Executive Summary

This plan delivers the first remaining unticked acceptance criterion of Issue #111 (`Outputs are reproducible from retained readings`, PRD FR-050 / AC-067 / AC-068, ADR 0003 decision 6) end to end across both in-memory/JSON `Store` and `SqlStore` in `src/core`. It closes three reproducibility gaps identified in research: (1) pure sensor analysis now canonicalizes exact-duplicate retained-reading replays into a deterministic reading set while still failing closed on conflicting duplicates, (2) SQL retained-envelope extraction adds `reading_id` tie-breaking so SQL row ordering is total as well as order-invariant downstream, and (3) `sensor_analysis_store` and `sensor_review_draft` gain a typed JSON retained-reading adapter (`JsonRetainedStore` + `retain_json_readings`) so `Store` and `SqlStore` produce byte-for-byte identical versioned `Signal` outputs, `SENSOR_REVIEW_DUE` task candidates and case-local drafts, and canonical replay digests without mutating priority or creating duplicate tasks.

### User Decisions and Requirements Highlights

* **Cross-store retained-reading reproducibility**: Deterministic versioned sensor analysis outputs, `SENSOR_REVIEW_DUE` task derivation, and replay digests must reproduce identically across both in-memory/JSON `Store` and `SqlStore`, including arbitrary SQL row ordering, duplicate/out-of-order retained-reading replay, and stale/missing `INSUFFICIENT` fallbacks without mutating priority or generating duplicate tasks.
* **Conflict-free sibling-PR boundary**: Do not modify `README.md` (including `src/core/README.md`), `server.py`, or `test_role_endpoint_inventory.py`, and add all new focused unit tests in `src/core/tests/test_sensor_reproducibility_111.py`.
* **Focused local verification and no-push commit**: Pass `test_sensor*.py`, `ruff check`, `ruff format --check`, strict `mypy`, and `tools/rename-zava-tests.py`, then commit locally with `Refs #111` and the Copilot trailer without pushing.

### What You May Not Know

* **Existing SQL-only and API mock contracts stay intact**: `SensorConsumer(json_store)` must continue raising `ConsumerError("UNSUPPORTED_STORE_SQL_REQUIRED")` (`test_sensor_consumer.py`), unconfigured JSON `Store` must continue failing closed with `consent-withheld` and `RETAINED_READINGS_UNAVAILABLE` (`JsonDraftCases`), and `sensor_review_draft` must continue calling `SensorConsumer(store)` for SQL stores so `src/api/tests/test_sensor_review_draft_api.py`'s `mock.patch.object(srd, "SensorConsumer")` seam remains unbroken.
* **Zero `pyproject.toml` edits needed for strict `mypy`**: Typing `JsonRetainedStore` against a structural `Protocol` in `sensor_analysis_store.py` and wrapping untyped `Store`/`SqlStore` constructors in typed test helpers in `test_sensor_reproducibility_111.py` satisfies `mypy --strict` with zero `# type: ignore` comments and zero `pyproject.toml` merge risk.
* **Pre-publication Full SQL gate remains a distinct follow-up**: Under `src/README.md`, touching `sensor_analysis.py` and `sensor_consumer.py` requires the external Full SQL gate (`tools/rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1` and `--verify-receipt`) plus hosted CI before pushing or merging a PR; because the caller explicitly forbade `git push`, that publication check is recorded transparently under `## Follow-Up Items`.

### Unresolved Decisions or Blockers

* None for this `src/core` slice. Operational rule approval and analytics research phases R1-R3 remain separate follow-up work under Issue #111 (`Refs #111`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`), writing dated artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`) for Issue #111 on branch `feat/iot-111-reproducible-outputs` targeting `feat/demo-164-chat-grounding-provenance-0900` (#1641) (caller prompt).
* Deliver the first remaining unticked acceptance criterion of Issue #111: `Outputs are reproducible from retained readings` (PRD FR-050, AC-067, AC-068; ADR 0003 decision 6).
* Inspect `src/core/src/zava_forward/core/sensor_analysis.py`, `sensor_review_draft.py`, `sqlstore.py`, and existing `src/core/tests/test_sensor_analysis*.py` (completed in `.copilot-tracking/research/2026-11-15/111-reproducible-outputs-research.md`).
* Ensure deterministic versioned sensor analysis outputs, `SENSOR_REVIEW_DUE` task derivation, and replay digests are 100% reproducible from retained readings across both in-memory/JSON `Store` and `SqlStore`, including arbitrary SQL row ordering, duplicate/out-of-order retained-reading replay, and stale/missing `INSUFFICIENT` fallback without mutating priority or generating duplicate tasks (caller prompt; PRD FR-050 / AC-067 / AC-068; ADR 0003 decision 6).
* Add focused unit tests in `src/core/tests/test_sensor_reproducibility_111.py` and do not modify `README.md`, `server.py`, or `test_role_endpoint_inventory.py` so the branch merges conflict-free with sibling PRs (caller prompt).
* Validate with `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_sensor*.py' -q`, `(cd src/core && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy)`, and `python3 tools/rename-zava-tests.py` (caller prompt).
* Commit locally with `Refs #111` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, leave `git status --short` empty, and do not push (caller prompt).

## Goals

* Make pure and retained-store sensor analysis (`Signal`, `VersionProvenance`), `SENSOR_REVIEW_DUE` task candidate and draft derivation (`ReviewTaskCandidate`, `sensor_review_draft`), and canonical replay digests (`input_digest`, `policy_digest`, `output_digest`, `draft_digest`) 100% deterministic functions of the retained reading set, home consent, window, `as_of`, and `AnalysisPolicy` across both `Store` and `SqlStore`.
* Guarantee idempotence under arbitrary SQL row ordering and exact-duplicate/out-of-order retained-reading replay while failing closed (`INSUFFICIENT` / `IDENTITY_CONFLICT`) on conflicting observations, stale/missing windows, weather-only inputs, and withheld or unconfigured consent.
* Prove with focused automated tests in `src/core/tests/test_sensor_reproducibility_111.py` that priority/ranking is never mutated and duplicate `SENSOR_REVIEW_DUE` tasks/drafts are never generated on either store backend.

## Scope and Non-Goals

### In Scope

* Exact-replay reading-set canonicalization in `src/core/src/zava_forward/core/sensor_analysis.py` (`_exact_row_key`, `_dedupe_exact_rows`, `_by_observation`, `reading_tuples`).
* Total deterministic SQL ordering (`ORDER BY observed_at, sensor_id, reading_id`) in `src/core/src/zava_forward/core/sensor_consumer.py`.
* Store-neutral `RetainedReadingSource` protocol, JSON/in-memory `Store` retained-reading carrier (`JsonRetainedStore`, `retain_json_readings`, `retained_source`), and cross-store `analyse_retained` / `reproduce_retained` support in `src/core/src/zava_forward/core/sensor_analysis_store.py`.
* Cross-store retained consent/analysis reader and unconfigured-store `RETAINED_READINGS_UNAVAILABLE` refusal parity in `src/core/src/zava_forward/core/sensor_review_draft.py`.
* New focused unit test suite `src/core/tests/test_sensor_reproducibility_111.py` (<= 10 test methods, zero removals/renames of existing tests).

### Non-Goals

* Modifying `README.md`, `src/core/README.md`, `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_role_endpoint_inventory.py`, or `src/core/pyproject.toml`.
* Modifying `SensorConsumer.__init__`'s SQL-only requirement (`UNSUPPORTED_STORE_SQL_REQUIRED`) or `sensor_scenarios.analyse`'s direct sequence validator.
* Completing analytics research phases R1-R3, changing `EXERCISE VALUE` thresholds, activating operational tasks, running live Azure SQL / IoT Hub infrastructure, or pushing commits to remote.

## Functional Requirements

* **FR-1 (Exact-replay set canonicalization vs conflict fail-closed)**: `derive_signal`, `reading_tuples`, `reproduce_sensor_analysis`, and `reproduce_review_task` must deduplicate byte-and-type-identical retained-reading replays regardless of input permutation while keeping any conflicting rows (different value, `reading_id`, schema fields, or value types at the same timestamp or key) distinct so `comparator.analyse` fails closed to `INSUFFICIENT` (`DUPLICATE` / `SCHEMA_FIELDS`).
  * Observable acceptance criteria: Shuffling `rows` and appending exact copies (`rows + rows[:k]`) produces identical `Signal`, `ReviewTaskCandidate`, `VersionProvenance`, `reading_tuples`, `input_digest`, and `output_digest`, whereas conflicting same-timestamp or same-ID rows produce `sufficiency == "INSUFFICIENT"` and `review_task is None` with distinct `input_digest`s.
* **FR-2 (Deterministic SQL row ordering and cursor-order invariance)**: `SensorConsumer.retained_envelopes` must order SQL results per requested `home` by `observed_at, sensor_id, reading_id`, and `analyse_retained` / `reproduce_retained` must return identical outputs and digests regardless of forward batch chunking, redelivery replay (`replay=True`), shuffled physical SQL row insertion order in `sensor_reading` / `sensor_delivery`, same-timestamp `(observed_at, sensor_id)` `reading_id` tie rows, or arbitrary `RetainedReadingSource` row order.
  * Observable acceptance criteria: `SqlStore` instances populated across varying chunk sizes or redelivery replays (`replay=True`), `SqlStore` instances whose identical retained rows are physically inserted into `sensor_reading` / `sensor_delivery` in forward vs shuffled/reversed SQL `INSERT` order (including same-`(observed_at, sensor_id)` tie rows), and a `RetainedReadingSource` returning envelopes in reversed/random order all produce identical `analyse_retained` and `reproduce_retained` payloads.
* **FR-3 (Cross-store retained-reading parity across `Store` and `SqlStore`)**: `sensor_analysis_store` must provide `RetainedReadingSource`, `JsonRetainedStore`, `retain_json_readings`, and `retained_source` so `analyse_retained`, `reproduce_retained`, `sensor_review_draft.read_drafts`, and `sensor_review_draft.draft_from_retained` operate identically on configured in-memory/JSON `Store` (including across `save()` and disk reload) and `SqlStore`, while unconfigured `Store` and unconfigured `SqlStore` both fail closed (`consent-withheld` on read; `RETAINED_READINGS_UNAVAILABLE` on `draft_from_retained` and `analyse_retained`).
  * Observable acceptance criteria: Given identical controls and retained readings, JSON `Store` (live and reopened from `live.json`) and `SqlStore` return byte-for-byte equal `Signal`, `ReproducedReviewTask`, `draft_from_retained` result, and `read_drafts` projection; `retain_json_readings` is idempotent on exact replay and raises `ConsumerError("IDENTITY_CONFLICT")` on conflicting `(sensor_id, reading_id)` payloads.
* **FR-4 (Stale/missing `INSUFFICIENT` fallback, priority non-mutation, and task deduplication)**: Across both `Store` and `SqlStore`, stale windows (`LATEST_READING_STALE`), empty windows (`NO_READINGS_IN_WINDOW`), `declined` / `unknown` consent, weather-only windows (`WEATHER_INPUT_NOT_INDOOR_MEASUREMENT`), and unreadable/unconfigured stores (`RETAINED_READINGS_UNAVAILABLE`) must fail closed with `priority_effect == "NONE"`, `diagnoses_hazard == False`, and `review_task is None`, never mutating `Store._ranking()` or `SqlStore` ranking (`_ranking()`, `cases.rkey`, `priority_correction`, `queue_*`), and repeated `SENSOR_REVIEW_DUE` derivations/draft proposals for the same `(home_id, window, policy_version, input_digest)` must deduplicate on `task_key` without creating duplicate tasks or drafts.
  * Observable acceptance criteria: Portfolio ranking snapshots before and after retained ingestion, `INSUFFICIENT`/`STALE`/`DECLINED` fallbacks, and approved synthetic `SENSOR_REVIEW_DUE` draft persistence are identical on both `Store` and `SqlStore`, and repeated `draft_from_retained` replays keep `len(case["sensor_review_drafts"]) == 1` with `existing == True`.

## Non-Functional Requirements

* **NFR-1 (Cross-process cryptographic determinism)**: Canonical SHA-256 digests (`input_digest`, `policy_digest`, `output_digest`, `task_key`, `draft_digest`) must not depend on wall-clock time, Python hash randomization (`PYTHONHASHSEED`), or dict/SQL iteration order.
  * Objective threshold or evaluation condition: 100% digest equality across distinct subprocesses with different `PYTHONHASHSEED` values (`1` vs `424242`) for both `Store` and `SqlStore`.
  * Operating condition or verification approach, if needed: Verified via `subprocess.run` in `src/core/tests/test_sensor_reproducibility_111.py`.
  * Observable acceptance criteria: Fresh Python processes produce identical JSON payloads and SHA-256 digests from the retained `live.json` and `.sqlite` files.
* **NFR-2 (Strict static typing, lint/format cleanliness, and conflict-free diff)**: All touched and new files must pass `ruff check`, `ruff format --check`, `mypy` (`strict = true`), and `tools/rename-zava-tests.py` with zero `# type: ignore` additions and zero edits to `README.md`, `server.py`, `test_role_endpoint_inventory.py`, or `pyproject.toml`.
  * Objective threshold or evaluation condition: Exit code `0` on all three caller validation commands and `git diff --name-only` restricted to `src/core/src/zava_forward/core/sensor_*.py`, `src/core/tests/test_sensor_reproducibility_111.py`, and `.copilot-tracking/`.
  * Observable acceptance criteria: Clean validation output and conflict-free file list verified before commit.

## Acceptance Criteria

* **AC-1**: `derive_signal`, `reading_tuples`, `reproduce_sensor_analysis`, and `reproduce_review_task` produce identical versioned outputs and digests across shuffled and exact-duplicate replayed reading slices while failing closed to `INSUFFICIENT` on conflicting duplicates.
* **AC-2**: `SensorConsumer.retained_envelopes` orders by `observed_at, sensor_id, reading_id`, and `analyse_retained` / `reproduce_retained` are invariant to SQL insertion order and arbitrary `RetainedReadingSource` row order.
* **AC-3**: Configured JSON/in-memory `Store` (in-memory and reloaded from disk) and `SqlStore` produce byte-for-byte identical `analyse_retained`, `reproduce_retained`, `draft_from_retained`, and `read_drafts` outputs, while unconfigured `Store` and `SqlStore` fail closed (`consent-withheld` / `RETAINED_READINGS_UNAVAILABLE`) and `SensorConsumer(json_store)` still raises `UNSUPPORTED_STORE_SQL_REQUIRED`.
* **AC-4**: Stale, missing, declined, unknown-consent, weather-only, and unavailable `INSUFFICIENT` fallbacks and repeated `SENSOR_REVIEW_DUE` draft replays never mutate priority/ranking (`Store._ranking()`, `SqlStore._ranking()`, `rkey`, `priority_correction`, `queue_*`) and never create duplicate tasks/drafts.
* **AC-5**: `src/core/tests/test_sensor_reproducibility_111.py` passes alongside all existing `test_sensor*.py` tests, `ruff check src tests`, `ruff format --check src tests`, `mypy`, and `tools/rename-zava-tests.py`, with zero edits to `README.md`, `server.py`, `test_role_endpoint_inventory.py`, or `pyproject.toml`.

## Implementation Context Record

| Context item | Current artifact or record |
| --- | --- |
| Plan | .copilot-tracking/plans/2026-11-15/111-reproducible-outputs-plan.md |
| Phase details | .copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-11-15/111-reproducible-outputs-plan-critique.md with Revise disposition resolved directly (`PC-001`..`PC-003` closed) |
| Relevant research | .copilot-tracking/research/2026-11-15/111-reproducible-outputs-research.md |
| Changes-record role | .copilot-tracking/changes/2026-11-15/111-reproducible-outputs-changes.md is created by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for implementation |
| Continuation context | Confirmed automatic RPI Agent parent continues directly to `rpi-implement` |

## Sources

* .copilot-tracking/research/2026-11-15/111-reproducible-outputs-research.md: Primary codebase evidence (`C1`-`C12`) and contrarian compatibility checks across `sensor_analysis.py`, `sensor_analysis_store.py`, `sensor_consumer.py`, `sensor_review_draft.py`, `store.py`, `sqlstore.py`, and existing sensor tests.
* docs/adrs/0003-journey-derived-capabilities-runtime-fit.md: Decision 6 requiring deterministic versioned sensor analysis reproducible from retained readings, non-authority, and no priority reduction on `INSUFFICIENT`/`DECLINED`.
* docs/prds/zava-forward-retrofit-programme-demonstrator.md: `FR-050`, `AC-067`, and `AC-068` governing sensor sufficiency, human-gated `SENSOR_REVIEW_DUE` proposals, and exercise threshold labelling.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Cross-Store Deterministic Sensor Analysis, Replay Canonicalization, and Review Draft Parity

* Intent: Make pure reading-set canonicalization, SQL retained-envelope ordering, JSON `Store` / `SqlStore` retained-reading reproduction, and `sensor_review_draft` retained derivation 100% deterministic and parity-aligned while preserving all fail-closed and mock seams.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Canonicalize Exact-Duplicate Replays in `sensor_analysis.py` and Total SQL Ordering in `sensor_consumer.py`

* Requirement and evidence: FR-1, FR-2, NFR-1, NFR-2; research `C2`, `C4`, `C5`, `C9`
* Expected result: `_by_observation` and `reading_tuples` collapse byte-and-type-identical retained-reading replays while keeping conflicting duplicates fail-closed (`INSUFFICIENT`), `_canonical_row` handles non-JSON fault values safely (`default=str`), and `SensorConsumer.retained_envelopes` orders by `observed_at, sensor_id, reading_id`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add `Store` and `SqlStore` Retained-Reading Adapter and Wire `sensor_review_draft.py`

* Requirement and evidence: FR-3, FR-4, NFR-1, NFR-2; research `C3`, `C6`, `C7`, `C8`, `C10`, `C11`, `C12`
* Expected result: `sensor_analysis_store.py` exposes `RetainedReadingSource`, `JsonRetainedStore`, `retain_json_readings`, and `retained_source` and accepts `SensorConsumer | SqlStore | Store | RetainedReadingSource` in `analyse_retained` and `reproduce_retained`; `sensor_review_draft.py` supports configured JSON `Store` alongside `SqlStore` while keeping `SensorConsumer(store)` for `_sql(store)` and returning `RETAINED_READINGS_UNAVAILABLE` on unconfigured `Store` and `SqlStore`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Focused Cross-Store Reproducibility Test Suite and Verification

* Intent: Lock cross-store reproducibility, arbitrary SQL ordering, duplicate/out-of-order replay, `INSUFFICIENT` non-mutation of priority, and `SENSOR_REVIEW_DUE` deduplication in `src/core/tests/test_sensor_reproducibility_111.py` and verify all required checks cleanly.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Author `src/core/tests/test_sensor_reproducibility_111.py` and Run Focused Validation

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1, NFR-2, AC-1..AC-5; research `C1`-`C12`
* Expected result: `src/core/tests/test_sensor_reproducibility_111.py` (<= 10 focused test methods, 0 existing test removals/edits, 0 `# type: ignore`) passes alongside all `test_sensor*.py` suites, `src/api/tests/test_sensor_review_draft_api.py` compatibility check, `ruff check src tests`, `ruff format --check src tests`, `mypy`, and `python3 tools/rename-zava-tests.py`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md

## Dependencies

* Python 3.12 standard-library `sqlite3`, `unittest`, and installed `ruff` (`0.17.1`) + `mypy` (`2.4.0`) in the active environment (verified passing at baseline).
* `src/core/tests/sensor_consumer_fixture.py` and `src/core/tests/dataset.py` test fixtures for deterministic synthetic `Store` and `SqlStore` construction.

## Critique Disposition

Single-pass `rpi-plan-critique` completed in `.copilot-tracking/reviews/plans/2026-11-15/111-reproducible-outputs-plan-critique.md` with verdict `Revise` (`0` Critical, `1` High, `1` Medium, `1` Low; all `planning_parent` direct planner corrections, no user decision required). Every finding is resolved below and finalized without a second critique loop.

| Critique run and finding | Disposition | Plan response or residual risk |
| --- | --- | --- |
| `PC-001` [High]: Indoor `schema_version` (`SCHEMA_VERSION = "sensor-fault-input-v1"` vs `"reading-v2"`), merge-on-replay semantics, `SqlStore`/`SensorMssqlConnector` guards, and per-home `(observed_at, sensor_id, reading_id)` ordering | resolved | Updated `P01-T02` in `.copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md` to match `SCHEMA_VERSION` (`"sensor-fault-input-v1"`), `LIVE_VERSIONS`, and legacy `"reading-v1"` with strict field-set and `type(v) is str` validation, merge incoming `readings` with existing retained readings while replacing `"controls"`, guard `JsonRetainedStore.__init__` and `retain_json_readings` against `isinstance(store, SqlStore)` while accepting `SensorMssqlConnector` in `retained_source`, and validate `home_ids`/`windows` first before sorting per `home` in `home_ids` order by `(observed_at, sensor_id, reading_id)`. |
| `PC-002` [Medium]: Distinguish `SensorConsumer.process` monotonic admission from shuffled physical SQL row insertion and same-timestamp tie-breaking | resolved | Updated `FR-2` in this plan and `P02-T01` item 2 in `.copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md` so `SensorConsumer.process` tests forward chunk-size variance and redelivery replay (`replay=True`), while shuffled/reversed SQL `INSERT`s into `sensor_reading` / `sensor_delivery` (including same-`(observed_at, sensor_id)` tie rows) and reversed/shuffled `RetainedReadingSource` cursors test arbitrary SQL row order and `reading_id` tie-breaking. |
| `PC-003` [Low]: Route untyped `Store.save()` and `Store._ranking()` / `SqlStore._ranking()` calls through typed `Protocol` / `Callable` wrappers under `mypy --strict` | resolved | Updated `P01-T02` and `P02-T01` in `.copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md` so `retain_json_readings` calls `.save()` through `_JsonStoreCarrier` and `test_sensor_reproducibility_111.py` calls `_ranking()` and untyped store helpers through typed `Protocol` / `Callable` wrappers with zero `# type: ignore` or `pyproject.toml` edits. |
| Accepted residual risk: Pre-publication external Full SQL gate (`tools/rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1` and `--verify-receipt`) | accepted with risk | Tracked in `## Follow-Up Items`; mandatory before any future `git push` or PR merge, and intentionally deferred in this session per the caller's explicit `Do NOT push` instruction. |

## Follow-Up Items

* **External Full SQL gate (`tools/rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1` and `--verify-receipt`) and hosted CI**: Outside immediate scope because the caller explicitly instructed `Do NOT push`; owner/next action is to run the live-MSSQL Full gate and verify an external receipt before pushing `feat/iot-111-reproducible-outputs` or opening/merging its PR.
* **Analytics research phases R1-R3 (`docs/reference/research/iot-sensor-analytics-research-plan.md`)**: Outside immediate scope because Issue #111 criterion 3 and PRD AC-068 require primary-standards research and named domain reviewer approval before replacing `EXERCISE VALUE` labels or activating an operational rule; keep commit linked with `Refs #111`.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/111-reproducible-outputs-changes.md
* Ready phase or task: Complete (ready for `rpi-review`)
* Remaining provisional question or blocker: none
