<!-- markdownlint-disable-file -->
# RPI Plan Critique: Deterministic Sensor Analysis, Review Task, and Digest Reproducibility Across Store and SqlStore

## Metadata

* Task ID: 111-reproducible-outputs
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/111-reproducible-outputs-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver the first remaining unticked acceptance criterion of Issue #111 (`Outputs are reproducible from retained readings`; PRD FR-050, AC-067, AC-068; ADR 0003 decision 6) across both in-memory/JSON `Store` and `SqlStore`, including arbitrary SQL row ordering, duplicate/out-of-order retained-reading replay, and stale/missing `INSUFFICIENT` fallbacks without mutating priority or generating duplicate tasks; add focused unit tests only in `src/core/tests/test_sensor_reproducibility_111.py` without editing `README.md`, `server.py`, or `test_role_endpoint_inventory.py`; pass the three caller validation commands; commit locally with `Refs #111` and the Copilot trailer without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/111-reproducible-outputs-research.md, .copilot-tracking/plans/2026-11-15/111-reproducible-outputs-plan.md, .copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md, src/core/src/zava_forward/core/sensor_analysis.py, src/core/src/zava_forward/core/sensor_consumer.py, src/core/src/zava_forward/core/sensor_analysis_store.py, src/core/src/zava_forward/core/sensor_review_draft.py, src/core/src/zava_forward/core/sqlstore.py, src/core/src/zava_forward/core/store.py, src/core/src/zava_forward/core/sensor_sql.py, src/core/src/zava_forward/core/synthetic/sensor_faults.py, src/core/src/zava_forward/core/synthetic/sensor_scenarios.py, src/core/src/zava_forward/core/synthetic/sensor_identity.py, src/core/pyproject.toml, tools/rename-zava-tests.py, src/core/tests/sensor_consumer_fixture.py, src/core/tests/test_sensor_analysis.py, src/core/tests/test_sensor_analysis_reproducibility.py, src/core/tests/test_sensor_analysis_store.py, src/core/tests/test_sensor_review_draft.py, src/api/tests/test_sensor_review_draft_api.py.
* Decisions, dependencies, and acceptance criteria considered: Research findings `C1` through `C12`, functional requirements `FR-1` through `FR-4`, non-functional requirements `NFR-1` and `NFR-2`, acceptance criteria `AC-1` through `AC-5`, phases `P01` (`P01-T01`, `P01-T02`) and `P02` (`P02-T01`), confirmed sibling-PR conflict-free exclusions, and local no-push closeout discipline.
* Assessment boundary: Evaluates technical accuracy, contract compatibility, strict typing, and testability of the candidate plan and phase details against the supplied codebase and caller rules. Live Azure SQL (`ZF_SENSOR_MSSQL=1`) and hosted CI execution remain out of runtime scope because the caller prohibited pushing in this session.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller Req 1, C1 (Issue #111 criterion 1, PRD FR-050 / AC-067 / AC-068, ADR 0003 D6) | Covered | Traced into `FR-1` through `FR-4`, `NFR-1`, and `AC-1` through `AC-4` with exercise labels, fail-closed sufficiency, and non-authority preserved. |
| Caller Req 2 (Inspect core modules and existing sensor tests) | Covered | Grounded in .copilot-tracking/research/2026-11-15/111-reproducible-outputs-research.md (`C1` through `C12`). |
| FR-1, AC-1, P01-T01 (Exact-replay set canonicalization vs conflicting duplicate fail-closed) | Covered | `_exact_row_key` combining `home_id` runtime type, `_canonical_row`, and `_schema_marker` collapses exact replays in `_by_observation` and `reading_tuples` while preserving `test_sensor_analysis.py` (`dup_a`/`dup_b`) and `test_sensor_scenarios.py` (`ss.analyse` untouched). |
| FR-2, AC-2, P01-T01, P02-T01 (Deterministic SQL ordering and arbitrary row-order invariance) | Partial | `ORDER BY observed_at, sensor_id, reading_id` in `P01-T01` is sound, but `FR-2` and `P02-T01` item 2 conflate `SensorConsumer.process` arrival-order admission (which rejects non-monotonic timestamps as `OUT_OF_ORDER`) with shuffled physical SQL row insertion and same-timestamp tie-breaking; see `PC-002`. |
| FR-3, AC-3, P01-T02 (Cross-store `Store` and `SqlStore` retained-reading parity) | Partial | Architecture preserves `UNSUPPORTED_STORE_SQL_REQUIRED`, unconfigured `JsonDraftCases`, and `mock.patch.object(srd, "SensorConsumer")`, but `P01-T02` specifies `"reading-v2"` instead of `SCHEMA_VERSION` (`"sensor-fault-input-v1"`) and leaves partial-replay/control-update merge and `SqlStore`-subclass / per-home ordering invariants underspecified; see `PC-001`. |
| FR-4, AC-4, P01-T02, P02-T01 (`INSUFFICIENT` fallbacks, priority non-mutation, task deduplication) | Covered | Aligns unconfigured `RETAINED_READINGS_UNAVAILABLE` refusals across `Store` and `SqlStore`, preserves `task_key` draft deduplication, and verifies `_ranking()`, SQL `cases` ranking columns, and hazards remain untouched. |
| NFR-1, P02-T01 (Cross-process `PYTHONHASHSEED` digest determinism) | Covered | Verified across fresh Python subprocesses against saved `live.json` and `.sqlite` artifacts. |
| NFR-2, AC-5, P01-T02, P02-T01 (Strict `mypy`, `ruff`, `rename-zava-tests`, conflict-free diff) | Partial | Forbidden files are excluded, but calling untyped `Store.save()` and `Store._ranking()` / `SqlStore._ranking()` directly without typed `Protocol` or `Callable` wrappers fails `mypy` `disallow_untyped_calls`; see `PC-003`. |

## Verdict

* Verdict: Revise
* Rationale: The overall architecture, module boundaries, and backwards-compatibility seams (`SensorConsumer` SQL-only guard, fail-closed unconfigured `JsonDraftCases`, and `DraftApi` mock seam) are well chosen, but three concrete specification bugs in `FR-2`, `P01-T02`, and `P02-T01` would cause runtime schema rejection on indoor readings (`"reading-v2"` vs `"sensor-fault-input-v1"`), test failures on shuffled `SensorConsumer.process` ingestion, and `mypy --strict` `[no-untyped-call]` errors unless corrected before implementation.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Incorrect indoor `schema_version` (`"reading-v2"`) and underspecified replay-merge and `SqlStore`-subclass guards in `P01-T02`

* Related IDs: FR-3, AC-3, C3, C5, C7, C10, P01-T02
* Evidence: .copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md, src/core/src/zava_forward/core/synthetic/sensor_faults.py, src/core/src/zava_forward/core/sensor_consumer.py, src/core/src/zava_forward/core/sqlstore.py, src/core/tests/test_sensor_analysis.py, src/core/tests/test_sensor_analysis_store.py
* Concern: `P01-T02` specifies `for reading-v2 project exact READING_FIELDS` in `retain_json_readings`, repeating a stale docstring phrase from `sensor_consumer.py:1038`. In code, indoor observations generated by `sensor_faults` and `sensor_scenarios` use `SCHEMA_VERSION = "sensor-fault-input-v1"` (`sensor_faults.py:10`, enforced by `SensorConsumer._shape` at `sensor_consumer.py:722` and asserted at `test_sensor_analysis.py:165`). In addition, `P01-T02` does not make four parity invariants explicit: (1) merging incoming `readings` with existing `store.data["sensor_retained"]["readings"]` while replacing `"controls"` so partial batch replay (`rows[:k]`) and consent updates (`retain_json_readings(store, [declined_control], [])`) preserve prior retained readings just like `SensorConsumer.process` + `SensorConsumer.configure`; (2) validating exact field sets and `type(v) is str` per schema (`LIVE_VERSIONS` -> `LIVE_FIELDS`, `SCHEMA_VERSION` -> `READING_FIELDS`, legacy `"reading-v1"` -> `READING_COLUMNS` minus `"injected_fault"` enriched from the matching `sensor_id` control) and raising `ConsumerError` on unknown `schema_version`, missing `"reading-v1"` control, or non-string/extra/missing fields instead of string-coercing arbitrary values; (3) rejecting `isinstance(store, SqlStore)` inside `JsonRetainedStore.__init__` as well as `retain_json_readings` (because `SqlStore` subclasses `Store` at `sqlstore.py:162`) and accepting `SensorMssqlConnector` alongside `SqlStore` in `retained_source`; and (4) validating `home_key` / `home_ids` / `windows` (`INVALID_HOME_SELECTION`) before reading `store.data` and sorting `JsonRetainedStore.retained_envelopes` per `home` in `home_ids` order by `(observed_at, sensor_id, reading_id)` to match `SensorConsumer.retained_envelopes` (`sensor_consumer.py:1066-1075`).
* Impact: Checking `"reading-v2"` rejects or misprojects every indoor scenario and fault reading on `Store`, breaking `Store` vs `SqlStore` parity (`FR-3`, `AC-3`), while overwriting rather than merging `"readings"` wipes previously retained rows during partial replay or consent reconfiguration tests.
* Smallest useful change: Update `P01-T02` in `.copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md` so `retain_json_readings` matches `SCHEMA_VERSION` (`"sensor-fault-input-v1"`), `LIVE_VERSIONS`, and legacy `"reading-v1"` with strict field-set and `str`-value validation (raising `ConsumerError` on unknown/malformed envelopes), merges new readings with existing retained readings while replacing `"controls"`, guards `JsonRetainedStore.__init__` against `SqlStore` and accepts `SensorMssqlConnector` in `retained_source`, and validates `home_ids`/`windows` first while ordering `retained_envelopes` per `home` in `home_ids` sequence by `(observed_at, sensor_id, reading_id)`.
* Action owner: planning_parent
* Exact resolving evidence: `.copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md` (`P01-T02`) specifies `SCHEMA_VERSION` (`"sensor-fault-input-v1"`) instead of `"reading-v2"`, strict envelope validation, merge-readings + replace-controls replay semantics, `SqlStore`/`SensorMssqlConnector` dispatch guards, and per-home `(observed_at, sensor_id, reading_id)` ordering.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: `FR-2` and `P02-T01` conflate `SensorConsumer.process` monotonic admission with shuffled physical SQL row order and same-timestamp tie-breaking

* Related IDs: FR-2, AC-2, C5, P02-T01
* Evidence: .copilot-tracking/plans/2026-11-15/111-reproducible-outputs-plan.md, .copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md, src/core/src/zava_forward/core/sensor_consumer.py, src/core/tests/test_sensor_analysis_reproducibility.py
* Concern: `FR-2` states that two `SqlStore` instances populated in "forward vs shuffled/replayed batch order" produce identical `analyse_retained` and `reproduce_retained` payloads, and `P02-T01` item 2 specifies populating two `SqlStore` databases in "forward vs shuffled/chunked order" and testing same-timestamp multi-reading tie ordering. However, `SensorConsumer._quality` (`sensor_consumer.py:953-955`) rejects any non-replay arrival on a sensor when `observed <= latest` with `"OUT_OF_ORDER"`, a behavior explicitly asserted by `test_out_of_order_arrival_is_rejected_so_only_retained_rows_drive_a_deterministic_result` (`test_sensor_analysis_reproducibility.py:148-159`), where shuffled `SensorConsumer.process` retains fewer than 672 rows and yields `INSUFFICIENT`. Likewise, `SensorConsumer.process` rejects a second reading at the same `(sensor_id, observed_at)` timestamp as `"OUT_OF_ORDER"`.
* Impact: Implementing `P02-T01` item 2 by feeding shuffled single-sensor batches through `SensorConsumer.process` will fail assertions comparing it against forward-ingested `SqlStore`, and will be unable to insert same-`(observed_at, sensor_id)` tie rows via `SensorConsumer.process` to exercise the new `ORDER BY observed_at, sensor_id, reading_id` clause.
* Smallest useful change: Clarify `FR-2` in `.copilot-tracking/plans/2026-11-15/111-reproducible-outputs-plan.md` and `P02-T01` item 2 in `.copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md` so (a) `SensorConsumer.process` covers forward chunk-size variance and exact redelivery replay (`replay=True`), while (b) arbitrary physical SQL storage order and same-`(observed_at, sensor_id)` `reading_id` tie-breaking are tested by inserting the identical retained rows into `sensor_reading` (and `sensor_delivery` witnesses, or legacy `"reading-v1"` rows for same-sensor timestamp ties) in shuffled/reversed SQL `INSERT` order alongside the reversed/shuffled `RetainedReadingSource` cursor test.
* Action owner: planning_parent
* Exact resolving evidence: `.copilot-tracking/plans/2026-11-15/111-reproducible-outputs-plan.md` (`FR-2`) and `.copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md` (`P02-T01` item 2) distinguish `SensorConsumer.process` chunk/redelivery replay from shuffled physical SQL row insertion into `sensor_reading`/`sensor_delivery` and direct retained-row tie-breaking on `(observed_at, sensor_id, reading_id)`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Low]: Untyped `Store` and `SqlStore` method calls (`save`, `_ranking`) need typed `Protocol` or `Callable` wrappers under `mypy --strict`

* Related IDs: NFR-2, AC-5, C12, P01-T02, P02-T01
* Evidence: .copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md, src/core/src/zava_forward/core/store.py, src/core/src/zava_forward/core/sqlstore.py, src/core/pyproject.toml
* Concern: Neither `zava_forward.core.sensor_analysis_store` nor `test_sensor_reproducibility_111` has `disallow_untyped_calls = false` in `src/core/pyproject.toml`, and `NFR-2` prohibits editing `pyproject.toml` or adding `# type: ignore`. While `P01-T02` defines `_JsonStoreCarrier` (`Protocol`) and `P02-T01` wraps `Store` and `SqlStore` constructors via `cast(Callable[..., Store], Store)`, `Store.save` (`store.py:114`) and `Store._ranking` (`store.py:207`, inherited by `SqlStore`) are untyped methods. Calling `store.save()` directly on `store: Store` in `retain_json_readings` or calling `store._ranking()` (or untyped `detail` / `audit_entries`) directly on `Store` / `SqlStore` instances in `test_sensor_reproducibility_111.py` raises `mypy` `[no-untyped-call]` errors.
* Impact: Validation command 2 (`cd src/core && ... python3 -m mypy`) will fail during implementation if `.save()` or `._ranking()` is invoked on `Store` / `SqlStore` rather than through typed `Protocol`s or `Callable` casts.
* Smallest useful change: Note in `P01-T02` that `retain_json_readings` invokes `.save()` through `_JsonStoreCarrier`, and note in `P02-T01` that `test_sensor_reproducibility_111.py` invokes `_ranking()` (and any other untyped `Store`/`SqlStore` helper methods) through a small typed `Protocol` or `cast(Callable[...], ...)` helper alongside the constructor wrappers.
* Action owner: planning_parent
* Exact resolving evidence: `.copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md` (`P01-T02` and `P02-T01`) specifies routing `save()` through `_JsonStoreCarrier` and routing `_ranking()` (and any untyped store methods) in `test_sensor_reproducibility_111.py` through typed `Protocol` / `Callable` helpers.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Strong contract preservation: Keeping `SensorConsumer.__init__` SQL-only (`UNSUPPORTED_STORE_SQL_REQUIRED`), keeping unconfigured `Store` fail-closed (`consent-withheld` and `RETAINED_READINGS_UNAVAILABLE`), and preserving `SensorConsumer(store)` when `_sql(store)` is `True` in `sensor_review_draft.py` protects `test_sensor_consumer.py`, `JsonDraftCases`, and `src/api/tests/test_sensor_review_draft_api.py` without touching forbidden files.
* Sound replay-vs-conflict separation in `P01-T01`: Keying `_dedupe_exact_rows` on `(type(row.get("home_id")).__qualname__, _canonical_row(row), _schema_marker(row))` inside `sensor_analysis.py` cleanly makes signals, `SENSOR_REVIEW_DUE` candidates, and digests idempotent under exact-duplicate retained-reading replay while preserving fail-closed `DUPLICATE` / `SCHEMA_FIELDS` outcomes on conflicting observations and leaving `sensor_scenarios.analyse` untouched.
* Accepted residual risk: Under `.github/copilot-instructions.md` and `src/README.md`, edits to `sensor_analysis.py` and `sensor_consumer.py` require the external Full SQL gate (`tools/rpi-checks.py --all` with live `ZF_SENSOR_MSSQL=1` and `--verify-receipt`) plus hosted CI prior to pushing/merging a PR; deferring that gate to pre-publication follow-up is explicitly required here by the caller's `Do NOT push` instruction and is transparently recorded under `## Follow-Up Items`.

## Questions or Blocking Evidence Gaps

* none

## Limitations

* This critique assessed static code contracts and supplied research/test evidence only; it did not execute live `MssqlStore` (`ZF_SENSOR_MSSQL=1`) or modify any repository source/test files.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-15/111-reproducible-outputs-plan.md` (`FR-2`, `Critique Disposition`) and `.copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md` (`P01-T02`, `P02-T01`) to resolve `PC-001`, `PC-002`, and `PC-003`, then finalize the plan and proceed to `rpi-implement` without another critique pass.
* User response required: no
