<!-- markdownlint-disable-file -->
# RPI Phase Details: Deterministic Sensor Analysis, Review Task, and Digest Reproducibility Across Store and SqlStore

## Metadata

* Task ID: 111-reproducible-outputs
* Task slug: 111-reproducible-outputs
* Related plan: .copilot-tracking/plans/2026-11-15/111-reproducible-outputs-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/111-reproducible-outputs-research.md, docs/adrs/0003-journey-derived-capabilities-runtime-fit.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Cross-Store Deterministic Sensor Analysis, Replay Canonicalization, and Review Draft Parity | complete | P01, P01-T01, P01-T02 |
| P02 | Focused Cross-Store Reproducibility Test Suite and Verification | complete | P02, P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Cross-Store Deterministic Sensor Analysis, Replay Canonicalization, and Review Draft Parity

### Context

Research (`C2`, `C3`, `C5`, `C6`, `C7`, `C8`, `C10`, `C11`, `C12`) established that `src/core` already provides `VersionProvenance`, `policy_digest`, `output_digest`, `reproduce_review_task`, and `SensorConsumer`-backed `reproduce_retained`, but lacks (1) exact-duplicate replay deduplication in `sensor_analysis.py`, (2) `reading_id` SQL ordering tie-breaking in `SensorConsumer.retained_envelopes`, and (3) a retained-reading adapter for in-memory/JSON `Store` across `sensor_analysis_store.py` and `sensor_review_draft.py`.

### Intent

Ensure pure reading lists, JSON/in-memory `Store`, and `SqlStore` derive byte-for-byte identical versioned `Signal` records, `SENSOR_REVIEW_DUE` `ReviewTaskCandidate`s and case-local review drafts, and canonical replay digests from retained readings without breaking any existing SQL-only consumer, fail-closed JSON draft, API mock, or strict-typing contract.

### Boundaries

* Included: `src/core/src/zava_forward/core/sensor_analysis.py`, `src/core/src/zava_forward/core/sensor_consumer.py`, `src/core/src/zava_forward/core/sensor_analysis_store.py`, and `src/core/src/zava_forward/core/sensor_review_draft.py`.
* Excluded: `README.md`, `src/core/README.md`, `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_role_endpoint_inventory.py`, `src/core/pyproject.toml`, `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/sqlstore.py`, and `src/core/src/zava_forward/core/synthetic/sensor_scenarios.py`.

### Likely Targets

* src/core/src/zava_forward/core/sensor_analysis.py: Deduplicate exact-identical retained-reading replays while keeping conflicting duplicates fail-closed.
* src/core/src/zava_forward/core/sensor_consumer.py: Add `reading_id` tie-breaker to `retained_envelopes` SQL `ORDER BY`.
* src/core/src/zava_forward/core/sensor_analysis_store.py: Add `RetainedReadingSource`, `JsonRetainedStore`, `retain_json_readings`, and `retained_source`, and accept `Store | SqlStore | SensorConsumer | RetainedReadingSource`.
* src/core/src/zava_forward/core/sensor_review_draft.py: Support configured JSON `Store` via `retained_source(store)`, retain `SensorConsumer(store)` for `_sql(store)`, and align unconfigured `RETAINED_READINGS_UNAVAILABLE` refusals.

### Dependencies

* None.

### Validation Expectations

* `ruff check src tests`, `ruff format --check src tests`, and `mypy` pass in `src/core` with zero `# type: ignore` additions.
* All existing `test_sensor*.py` tests in `src/core/tests` and `test_sensor_review_draft_api.py` in `src/api/tests` continue to pass unchanged.

### Completion Evidence

* Clean `git diff` across the four `src/core/src/zava_forward/core/sensor_*.py` modules satisfying `FR-1`..`FR-4` and `NFR-1`..`NFR-2`.

### Unresolved Items

* none

<!-- rpi:task id=P01-T01 -->
### P01-T01: Canonicalize Exact-Duplicate Replays in `sensor_analysis.py` and Total SQL Ordering in `sensor_consumer.py`

#### Context

In `sensor_analysis.py`, `_by_observation` currently sorts rows by `(str(r.get("observed_at", "")), _canonical_row(r))` without deduplicating exact-identical retained-reading replays, so `rows + rows[:k]` alters `_row_digest_tuples` (`input_digest`) and triggers `DUPLICATE`/`OUT_OF_ORDER` -> `INSUFFICIENT` in `comparator.analyse` (`C2`). Meanwhile, `test_sensor_scenarios.py:163` calls `ss.analyse` directly expecting raw `(rows[0], *rows)` to fail closed, and `test_sensor_analysis.py:296` passes conflicting same-timestamp rows (`dup_a`, `dup_b`) expecting distinct `valid` and `input_digest` (`C4`). In `sensor_consumer.py`, `retained_envelopes` queries `ORDER BY observed_at, sensor_id` without `reading_id` (`C5`).

#### Intent

Make `derive_signal`, `reading_tuples`, `reproduce_sensor_analysis`, and `reproduce_review_task` true functions of the retained reading set (invariant to row permutation and exact-duplicate replay, fail-closed on conflicting duplicates) and make SQL `retained_envelopes` ordering total.

#### Boundaries

* Included:
  * In `sensor_analysis.py`: update `_canonical_row` to pass `default=str`; define `_exact_row_key(row: Mapping[str, str]) -> tuple[str, str, str]` returning `(type(row.get("home_id")).__qualname__, _canonical_row(row), _schema_marker(row))`; define `_dedupe_exact_rows(rows: Sequence[Mapping[str, str]]) -> list[Mapping[str, str]]`; apply `_dedupe_exact_rows` in `_by_observation` (sorting by `(str(r.get("observed_at", "")), _exact_row_key(r))`) and in `reading_tuples` before emitting metric tuples.
  * In `sensor_consumer.py`: change `ORDER BY observed_at, sensor_id` to `ORDER BY observed_at, sensor_id, reading_id` in `SensorConsumer.retained_envelopes`.
* Excluded: Do not alter `sensor_scenarios.analyse` or `SensorConsumer.__init__`.

#### Likely Targets

* src/core/src/zava_forward/core/sensor_analysis.py: `_canonical_row`, `_exact_row_key`, `_dedupe_exact_rows`, `_by_observation`, `reading_tuples`.
* src/core/src/zava_forward/core/sensor_consumer.py: `SensorConsumer.retained_envelopes`.

#### Dependencies

* none

#### Validation Expectations

* `test_sensor_scenarios.py`, `test_sensor_analysis.py`, `test_sensor_analysis_reproducibility.py`, and `test_sensor_consumer.py` pass 100%, and `mypy` + `ruff` report zero issues.

#### Completion Evidence

* Exact-duplicate replay (`rows + rows[:5]`) produces identical `Signal`, `ReviewTaskCandidate`, `VersionProvenance`, `reading_tuples`, `input_digest`, and `output_digest` as `rows`, while conflicting duplicates still yield `INSUFFICIENT` (`DUPLICATE`).

#### Unresolved Items

* none

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add `Store` and `SqlStore` Retained-Reading Adapter and Wire `sensor_review_draft.py`

#### Context

`sensor_analysis_store.py` currently restricts `analyse_retained` and `reproduce_retained` to `SensorConsumer`, and `sensor_review_draft.py` calls `SensorConsumer(store)` unconditionally (`C3`, `C6`). Plain unconfigured JSON `Store` has no `"sensor_retained"` entry in `store.data` and must continue failing closed in `JsonDraftCases` (`C10`), while `src/api/tests/test_sensor_review_draft_api.py:143` patches `mock.patch.object(srd, "SensorConsumer")` on `SqlStore` (`C11`). `pyproject.toml` enforces `mypy --strict` on `sensor_analysis_store.py` without `disallow_untyped_calls = false` (`C12`).

#### Intent

Provide a typed, durable JSON/in-memory `Store` retained-reading carrier (`JsonRetainedStore` + `retain_json_readings`) under `store.data["sensor_retained"]` and store-neutral `retained_source` resolution so `analyse_retained`, `reproduce_retained`, `read_drafts`, and `draft_from_retained` behave identically across `Store` and `SqlStore`.

#### Boundaries

* Included:
  * In `sensor_analysis_store.py`:
    * Define `JSON_RETAINED_KEY = "sensor_retained"`, `RetainedReadingSource` (`Protocol` with `home_consent(self, home_id: str) -> str` and `retained_envelopes(self, home_ids: Sequence[str], windows: Mapping[str, tuple[str, str]] | None = None) -> list[dict[str, str]]`), and `_JsonStoreCarrier` (`Protocol` with `lock: AbstractContextManager[object]`, `data: dict[str, Any]`, and `def save(self) -> None`).
    * Implement `retain_json_readings(store: Store, controls: Sequence[SensorControl], readings: Sequence[Mapping[str, object]], *, save: bool = True) -> int`:
      * Reject `isinstance(store, SqlStore)` with `ConsumerError("JSON_STORE_REQUIRED")` so SQL stores always use `SensorConsumer`; bind `carrier: _JsonStoreCarrier = store` so `.save()` is strictly typed without `disallow_untyped_calls` violations.
      * Validate `len(controls) <= 100`, unique `c.sensor_id`, `c.validate()`, and `home_key(c.home_id)`.
      * Validate each reading envelope with strict `type(v) is str` and exact field-set checks matching `SensorConsumer`: for `schema_version in LIVE_VERSIONS` require `set(row) == set(LIVE_FIELDS)` and validate `SensorConsumer._live_shape`; for `schema_version == SCHEMA_VERSION` (`"sensor-fault-input-v1"`) require `set(row) == set(READING_FIELDS)` and validate `SensorConsumer._shape`; for legacy `schema_version == "reading-v1"` require `set(row) == {k for k in READING_COLUMNS if k != "injected_fault"}` with `home_key(row["home_id"])`, valid `utc(row["observed_at"])`, and an existing matching control by `sensor_id` to enrich `temperature_unit`, `humidity_unit`, and `calibrated`; raise `ConsumerError("SENSOR_OUTCOME_MALFORMED")` on any unknown `schema_version`, missing control, or malformed field/type.
      * Merge incoming `readings` with any existing valid readings already stored under `carrier.data.get("sensor_retained")` while replacing `"controls"` (mirroring `SensorConsumer.configure` + `SensorConsumer.process`), deduplicating exact-identical replays on `(sensor_id, reading_id)` idempotently and raising `ConsumerError("IDENTITY_CONFLICT")` if an existing or batch reading with the same `(sensor_id, reading_id)` has a different canonical envelope.
      * Persist `{"controls": [...], "readings": [...]}` canonically ordered by `(observed_at, sensor_id, reading_id)` into `carrier.data["sensor_retained"]` under `carrier.lock` and call `carrier.save()` when `save=True`.
    * Implement `JsonRetainedStore`:
      * Reject `isinstance(store, SqlStore)` in `__init__` with `ConsumerError("JSON_STORE_REQUIRED")`.
      * Validate `home_key(home_id)` in `home_consent` (`INVALID_HOME_ID`) and validate `home_ids` / `windows` (`INVALID_HOME_SELECTION`, UTF-16 length `<= 64`, `utc(...)` bounds) in `retained_envelopes` before inspecting `carrier.data.get("sensor_retained")`; if `"sensor_retained"` is absent in `carrier.data`, raise `ConsumerError(UNAVAILABLE)` so unconfigured JSON `Store` stays fail-closed, and raise `ConsumerError("SENSOR_OUTCOME_MALFORMED")` if `"sensor_retained"` has malformed structure or conflicting `(sensor_id, reading_id)` entries.
      * Implement `home_consent(home_id)` with exact `SensorConsumer.home_consent` semantics (`"declined"` wins, `"granted"` iff `states == {"granted"}`, else `"unknown"`).
      * Implement `retained_envelopes(home_ids, windows)` and `observed_series(home_ids, windows)` iterating `for home in home_ids:` in caller order and sorting each home's matching window rows by `(observed_at, sensor_id, reading_id)`, projecting `LIVE_FIELDS` for `LIVE_VERSIONS`, `READING_FIELDS` for `SCHEMA_VERSION`, and control-enriched fields for `"reading-v1"` identically to `SensorConsumer.retained_envelopes`.
    * Implement `retained_source(source: SensorConsumer | SqlStore | SensorMssqlConnector | Store | RetainedReadingSource) -> RetainedReadingSource` (dispatching `SqlStore | SensorMssqlConnector` -> `SensorConsumer(source)`, non-SQL `Store` -> `JsonRetainedStore(source)`, else `source`) and accept that union in `analyse_retained` and `reproduce_retained`.
  * In `sensor_review_draft.py`:
    * Define `_retained_reader(store: DraftStore) -> RetainedReadingSource` returning `SensorConsumer(store)` when `_sql(store)` is `True` and `retained_source(store)` otherwise.
    * Use `_retained_reader(store)` in `_consent_granted` and `_from_retained`; evaluate `policy = server_policy()` once in `_from_retained`; if `signal.reasons == (UNAVAILABLE,)`, return `_refusal("RETAINED_READINGS_UNAVAILABLE")`.
* Excluded: Do not edit `store.py`, `sqlstore.py`, or `pyproject.toml`.

#### Likely Targets

* src/core/src/zava_forward/core/sensor_analysis_store.py: `JSON_RETAINED_KEY`, `RetainedReadingSource`, `JsonRetainedStore`, `retain_json_readings`, `retained_source`, `analyse_retained`, `reproduce_retained`.
* src/core/src/zava_forward/core/sensor_review_draft.py: `_retained_reader`, `_consent_granted`, `_from_retained`.

#### Dependencies

* P01-T01

#### Validation Expectations

* `test_sensor_analysis_store.py`, `test_sensor_review_draft.py` (`JsonDraftCases` and `SqliteDraftCases`), and `src/api/tests/test_sensor_review_draft_api.py` pass 100%; `mypy` and `ruff` pass with zero errors.

#### Completion Evidence

* Identical `analyse_retained`, `reproduce_retained`, `draft_from_retained`, and `read_drafts` results across JSON `Store` and `SqlStore`, and identical fail-closed refusals when unconfigured.

#### Unresolved Items

* none

<!-- rpi:phase id=P02 -->
## P02: Focused Cross-Store Reproducibility Test Suite and Verification

### Context

Caller Requirement 3 locks new focused tests in `src/core/tests/test_sensor_reproducibility_111.py` without modifying `README.md`, `server.py`, or `test_role_endpoint_inventory.py`, and Requirement 4 specifies three focused validation commands.

### Intent

Prove every reproducibility, replay, SQL ordering, fail-closed `INSUFFICIENT`, ranking non-mutation, and task-deduplication invariant in `src/core/tests/test_sensor_reproducibility_111.py` under strict `mypy` and `ruff`, then run all required validation suites cleanly.

### Boundaries

* Included: Creating `src/core/tests/test_sensor_reproducibility_111.py` (<= 10 test methods; 0 removals/renames of existing tests; 0 `# type: ignore` comments) and executing the three caller validation commands plus a read-only `src/api/tests/test_sensor_review_draft_api.py` + `test_sensor_analysis_reproducibility.py` compatibility sanity check.
* Excluded: Editing any existing test file, `README.md`, `server.py`, `test_role_endpoint_inventory.py`, or `pyproject.toml`.

### Likely Targets

* src/core/tests/test_sensor_reproducibility_111.py: New focused cross-store reproducibility test module.

### Dependencies

* P01

### Validation Expectations

* `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_sensor*.py' -q` exits `0`.
* `(cd src/core && python3 -m ruff check src tests && python3 -m ruff format --check src tests && python3 -m mypy)` exits `0`.
* `python3 tools/rename-zava-tests.py` exits `0`.

### Completion Evidence

* Passing outputs recorded in `.copilot-tracking/changes/2026-11-15/111-reproducible-outputs-changes.md`.

### Unresolved Items

* none

<!-- rpi:task id=P02-T01 -->
### P02-T01: Author `src/core/tests/test_sensor_reproducibility_111.py` and Run Focused Validation

#### Context

`src/core/pyproject.toml` runs `mypy` with `strict = true` across `tests/`, and `Store` / `SqlStore` in `store.py` / `sqlstore.py` are legacy-untyped (`C12`). Using small typed `Protocol` / `Callable` helper wrappers (`cast(Callable[..., Store], Store)`, `cast(Callable[..., SqlStore], SqlStore)`, and a typed `_RankedStore` protocol for `_ranking()`) inside `test_sensor_reproducibility_111.py` keeps strict typing 100% clean with zero `# type: ignore` directives and zero `pyproject.toml` edits.

#### Intent

Create `src/core/tests/test_sensor_reproducibility_111.py` with focused semantic and regression tests covering `AC-1`..`AC-5`:

1. **Cross-store `Store` vs `SqlStore` parity + reload durability**: Seed identical synthetic cases, controls, and 7-day `sustained_high_humidity` / `repeated_overnight_peaks` / `normal` readings into JSON `Store` (and reopened `Store` from `live.json`) and `SqlStore`; verify byte-for-byte identical `analyse_retained`, `reproduce_retained`, `reproduce_sensor_analysis`, `reproduce_review_task`, `VersionProvenance`, `input_digest`, `policy_digest`, `output_digest`, `draft_from_retained` (both unapproved default refusal and synthetic-approved `SENSOR_REVIEW_DUE` draft), and `read_drafts`.
2. **Arbitrary SQL row ordering and same-timestamp tie-breaking**: Verify forward chunk-size variance and redelivery replay (`replay=True`) through `SensorConsumer.process`, populate two `SqlStore` databases by inserting the identical retained rows into `sensor_reading` / `sensor_delivery` in forward vs shuffled/reversed physical SQL `INSERT` order (plus same-`(observed_at, sensor_id)` `reading_id` tie rows in `retained_envelopes`), and wrap a custom `RetainedReadingSource` returning envelopes in reversed/shuffled order; assert identical signals, candidates, and digests.
3. **Duplicate and out-of-order retained-reading replay vs conflicting duplicates**: Verify that `rows + rows[:12]` shuffled in pure `derive_signal` / `reading_tuples` / `reproduce_sensor_analysis` / `reproduce_review_task`, repeated `retain_json_readings` replay on `Store`, and repeated `SensorConsumer.process` replay (`replay=True`) on `SqlStore` produce unchanged outputs and digests, whereas conflicting duplicate payloads fail closed (`ConsumerError("IDENTITY_CONFLICT")` on retain; `INSUFFICIENT` with `"DUPLICATE"` and `review_task is None` on pure replay).
4. **Stale, missing, withheld-consent, weather-only, and unavailable `INSUFFICIENT` fallbacks + priority non-mutation + zero duplicate tasks**: Across both `Store` and `SqlStore`, verify that stale `as_of`, empty window, `declined` / `unknown` consent, weather-only `LIVE_VERSIONS` rows, and unconfigured stores return `priority_effect == "NONE"`, `diagnoses_hazard == False`, `review_task is None`, leave `Store._ranking()`, `SqlStore._ranking()`, SQL `cases` columns (`rkey`, `priority_correction`, `queue_*`), and hazards completely unchanged, and that replaying `draft_from_retained` across identical or shifted `as_of` timestamps never creates duplicate `SENSOR_REVIEW_DUE` drafts (`existing == True`, count stays `1`).
5. **Fresh-process `PYTHONHASHSEED` reproducibility across `Store` and `SqlStore`**: Re-open both the saved `live.json` (`Store`) and `.sqlite` (`SqlStore`) in fresh Python subprocesses under `PYTHONHASHSEED=1` and `PYTHONHASHSEED=424242` and assert identical serialized `reproduce_retained` JSON and digests.

#### Boundaries

* Included: `src/core/tests/test_sensor_reproducibility_111.py` (<= 10 test methods; 0 removals/edits to existing tests).
* Excluded: Modifying any other file in `src/core/tests/`, `src/api/`, `README.md`, or `pyproject.toml`.

#### Likely Targets

* src/core/tests/test_sensor_reproducibility_111.py: New test file.

#### Dependencies

* P01-T01, P01-T02

#### Validation Expectations

* All three caller validation commands exit `0` with zero skipped assertions inside `test_sensor_reproducibility_111.py`.

#### Completion Evidence

* Command outputs captured in `.copilot-tracking/changes/2026-11-15/111-reproducible-outputs-changes.md`.

#### Unresolved Items

* none
