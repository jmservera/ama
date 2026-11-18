<!-- markdownlint-disable-file -->
# RPI Changes: Deterministic Sensor Analysis, Review Task, and Digest Reproducibility Across Store and SqlStore

## Metadata

* Task ID: 111-reproducible-outputs
* Related plan: .copilot-tracking/plans/2026-11-15/111-reproducible-outputs-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`
* All remaining active-plan markers: none
* Status basis: All planned `src/core` source updates (`P01-T01`, `P01-T02`) and focused cross-store reproducibility tests plus validation checks (`P02-T01`) completed and passed cleanly.

## Execution Summary

Completed full-plan implementation on `feat/iot-111-reproducible-outputs` within the approved `src/core` source and test boundary (`sensor_analysis.py`, `sensor_consumer.py`, `sensor_analysis_store.py`, `sensor_review_draft.py`, and `src/core/tests/test_sensor_reproducibility_111.py`), preserving all conflict-free sibling-PR exclusions (`README.md`, `src/core/README.md`, `server.py`, `test_role_endpoint_inventory.py`, and `pyproject.toml`).

## Completed Work

### P01: Cross-Store Deterministic Sensor Analysis, Replay Canonicalization, and Review Draft Parity

* `P01-T01` (`src/core/src/zava_forward/core/sensor_analysis.py`, `src/core/src/zava_forward/core/sensor_consumer.py`): Updated `_canonical_row` with `default=str`, added `_exact_row_key` and `_dedupe_exact_rows` so `_by_observation` and `reading_tuples` deduplicate byte-and-type-identical retained-reading replays regardless of arrival permutation while keeping conflicting observations fail-closed (`INSUFFICIENT` / `DUPLICATE` / `SCHEMA_FIELDS`), and added `reading_id` tie-breaking (`ORDER BY observed_at, sensor_id, reading_id`) to `SensorConsumer.retained_envelopes`.
* `P01-T02` (`src/core/src/zava_forward/core/sensor_analysis_store.py`, `src/core/src/zava_forward/core/sensor_review_draft.py`): Added `JSON_RETAINED_KEY`, `RetainedReadingSource`, `_JsonStoreCarrier`, `retain_json_readings`, `JsonRetainedStore`, and `retained_source` so configured in-memory/JSON `Store` and `SqlStore` produce identical `analyse_retained`, `reproduce_retained`, `draft_from_retained`, and `read_drafts` outputs while keeping `SensorConsumer.__init__` SQL-only (`UNSUPPORTED_STORE_SQL_REQUIRED`), preserving `_sql(store) -> SensorConsumer(store)` mock compatibility in `sensor_review_draft.py`, and failing closed with `RETAINED_READINGS_UNAVAILABLE` / `consent-withheld` when unconfigured.

### P02: Focused Cross-Store Reproducibility Test Suite and Verification

* `P02-T01` (`src/core/tests/test_sensor_reproducibility_111.py`): Authored 5 focused test methods covering (1) cross-store `Store` vs `SqlStore` parity and disk reload durability across `sustained_high_humidity`, `repeated_overnight_peaks`, and `normal` scenarios plus `JSON_STORE_REQUIRED` / `UNSUPPORTED_STORE_SQL_REQUIRED` guards, (2) SQL batch chunking, redelivery replay, shuffled physical `sensor_reading` / `sensor_delivery` SQL insertion, reversed/shuffled `RetainedReadingSource` cursors, and same-`(observed_at, sensor_id)` `reading_id` tie-breaking, (3) exact-duplicate and out-of-order replay idempotence vs `IDENTITY_CONFLICT` / `DUPLICATE` fail-closed rejection, (4) unconfigured, weather-only (`WEATHER_INPUT_NOT_INDOOR_MEASUREMENT`), stale (`LATEST_READING_STALE`), empty-window (`NO_READINGS_IN_WINDOW`), `declined`, and `unknown`-consent `INSUFFICIENT`/`STALE`/`DECLINED` fallbacks with zero ranking/hazard mutation and `task_key` draft deduplication, and (5) fresh-subprocess `PYTHONHASHSEED` (`1` vs `424242`) determinism across both `Store` and `SqlStore`.

## Implementation-Time Plan and Detail Updates

* None (`STAMP_END = "2024-01-30T00:00:00Z"` and chunked `_ingest_pair` used inside `test_sensor_reproducibility_111.py` so the post-window weather observation sits cleanly inside the 30-day exercise consumer clock without altering any plan or phase-detail contract).

## Validation Record

| Check | Scope | Status | Evidence or reason |
| --- | --- | --- | --- |
| `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_sensor*.py' -q` | `src/core/tests/test_sensor*.py` | Passed | 304 sensor tests executed (`test_sensor_analysis.py`, `test_sensor_analysis_reproducibility.py`, `test_sensor_analysis_store.py`, `test_sensor_consumer.py`, `test_sensor_review_draft.py`, `test_sensor_scenarios.py`, and `test_sensor_reproducibility_111.py`); all 5 tests in `test_sensor_reproducibility_111.py` passed (`OK` in 306.67s) |
| `(cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy)` | `src/core` lint, format, and strict static types | Passed | `All checks passed!`, `289 files already formatted`, `Success: no issues found in 342 source files` |
| `(cd src/api && PYTHONPATH=src:.:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_sensor_review_draft_api.py -q)` | API `SensorConsumer` mock-seam compatibility | Passed | `Ran 6 tests in 8.677s — OK` |
| `python3 tools/rename-zava-tests.py` | Repository migration regression guard | Passed | `Ran 25 tests in 0.863s — OK` |

## Pre-Review Reconciliation

* Plan markers and phase details: reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01` all `[x]` / `complete`)
* Completed-work evidence and handoff prose: reconciled
* Validation, blockers, remaining work, and follow-up items: reconciled
* Review readiness: ready for single-pass `rpi-review`

## Blockers

* none

## Remaining Work

* none

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/111-reproducible-outputs-plan.md, `## Follow-Up Items`
* **External Full SQL gate (`tools/rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1` and `--verify-receipt`) and hosted CI**: Outside immediate scope per the caller's `Do not push` instruction; run before pushing or merging `feat/iot-111-reproducible-outputs`.
* **Analytics research phases R1-R3 (`docs/reference/research/iot-sensor-analytics-research-plan.md`)**: Outside immediate scope; required before replacing `EXERCISE VALUE` labels or activating operational rules (`Refs #111`).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`; remaining: none
* Validation coverage: Focused validation passed (`test_sensor*.py`, `test_sensor_reproducibility_111.py -v`, `ruff check .`, `ruff format --check .`, `mypy`, `test_sensor_review_draft_api.py`, `tools/rename-zava-tests.py`)
* Blockers: none
* Current plan and detail updates: none
* Planning and critique state: Ready (`PC-001`..`PC-003` resolved and verified)
* Follow-up items: Pre-publication Full SQL gate; analytics research R1-R3
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
