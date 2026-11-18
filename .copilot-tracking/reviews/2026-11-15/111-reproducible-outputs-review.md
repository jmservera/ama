<!-- markdownlint-disable-file -->
# Review: Deterministic Sensor Analysis, Review Task, and Digest Reproducibility Across Store and SqlStore (Issue #111)

## Scope and Evidence

* Task ID: 111-reproducible-outputs
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`)
* Assessed boundary: GitHub Issue #111 acceptance criteria (`Outputs are reproducible from retained readings`, `Thresholds are sourced or labelled exercise values`, and `Research phases R1 to R3 are complete before a derived measure is used beyond an exercise rule`), PRD `FR-050` / `AC-067` / `AC-068`, ADR `0003` Decision 6, plan requirements `FR-1`..`FR-4` and `NFR-1`..`NFR-2`, plan acceptance criteria `AC-1`..`AC-5`, critique dispositions `PC-001`..`PC-003`, `src/core` source and test diffs, conflict-free sibling-PR file exclusions (`README.md`, `src/core/README.md`, `server.py`, `test_role_endpoint_inventory.py`, `pyproject.toml`), and Focused-tier local validation outputs.
* Plan: .copilot-tracking/plans/2026-11-15/111-reproducible-outputs-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/111-reproducible-outputs-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/111-reproducible-outputs-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/111-reproducible-outputs-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/111-reproducible-outputs-research.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/adrs/0003-journey-derived-capabilities-runtime-fit.md, docs/reference/research/iot-sensor-analytics-research-plan.md, src/core/src/zava_forward/core/sensor_analysis.py, src/core/src/zava_forward/core/sensor_consumer.py, src/core/src/zava_forward/core/sensor_analysis_store.py, src/core/src/zava_forward/core/sensor_review_draft.py, and src/core/tests/test_sensor_reproducibility_111.py.

## Opening Review State

* Interpreted review goal: Assess once from reconciled RPI artifacts, code diffs, and Focused-tier validation evidence whether `feat/iot-111-reproducible-outputs` satisfies all planned `P01` and `P02` contracts and how its delivered evidence maps to each GitHub Issue #111 acceptance criterion.
* Review scope: Full task (`P01`, `P02`)
* Evidence readiness: Ready; research, post-critique plan, phase details, single-pass plan critique, reconciled changes record, four modified `src/core` modules, `src/core/tests/test_sensor_reproducibility_111.py`, and Focused-tier validation outputs are complete and reconciled.
* Acceptance basis: Issue #111 acceptance criteria (`1`..`3`), PRD `FR-050` / `AC-067` / `AC-068`, ADR `0003` Decision 6, plan `FR-1`..`FR-4`, `NFR-1`..`NFR-2`, `AC-1`..`AC-5`, critique items `PC-001`..`PC-003`, and conflict-free sibling-PR guardrails.
* First comparison boundary: Reconcile `P01` and `P02` checklist markers and `PC-001`..`PC-003` dispositions against `sensor_analysis.py`, `sensor_consumer.py`, `sensor_analysis_store.py`, `sensor_review_draft.py`, and `test_sensor_reproducibility_111.py` before recording Issue #111 criterion-by-criterion linkage (`Refs #111`).
* Active read-only boundaries: Read-only across source, test, research, plan, phase-details, critique, and changes files; review writes only `.copilot-tracking/reviews/2026-11-15/111-reproducible-outputs-review.md` before returning to the automatic RPI Agent parent.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass `rpi-review` on `2026-11-15` across full plan scope (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`), comparing all canonical `.copilot-tracking/` artifacts, the 4 modified `src/core` source files, `src/core/tests/test_sensor_reproducibility_111.py`, Issue #111's 3 acceptance criteria, and Focused-tier `unittest`, `ruff`, `mypy`, API mock-seam, and `rename-zava-tests` runs.

## Verdict Against GitHub Issue #111 Acceptance Criteria

| Issue #111 criterion | Issue checkbox state | Branch verdict | Evidence and linkage note |
|----------------------|----------------------|----------------|---------------------------|
| 1. Outputs are reproducible from retained readings | `[x]` | Proven within `src/core` (`Store` and SQLite `SqlStore`); pre-push live-MSSQL full gate deferred per no-push boundary | Exact-duplicate replay set canonicalization (`_exact_row_key`, `_dedupe_exact_rows`), total SQL ordering (`ORDER BY observed_at, sensor_id, reading_id`), store-neutral `RetainedReadingSource` / `JsonRetainedStore` / `retain_json_readings`, cross-store `sensor_review_draft` parity, `INSUFFICIENT` / `STALE` / `DECLINED` non-mutation of ranking, `task_key` draft deduplication, and `PYTHONHASHSEED` subprocess determinism are proven in `src/core/tests/test_sensor_reproducibility_111.py`. Live Azure SQL (`ZF_SENSOR_MSSQL=1`) full gate and hosted CI remain pre-push checks. |
| 2. Thresholds are sourced or labelled exercise values | `[x]` | Preserved and conformant | `THRESHOLD_LABEL = "EXERCISE VALUE"`, `SYNTHETIC EXERCISE ONLY` / `PROPOSED_SYNTHETIC_DRAFT` labels, `NO_APPROVED_RULE` refusal when `RuleApproval` is absent, and explicit `SYNTHETIC TEST ONLY` test sentinels remain intact across `sensor_analysis.py`, `sensor_review_draft.py`, and `test_sensor_reproducibility_111.py`. |
| 3. Research phases R1 to R3 are complete before a derived measure is used beyond an exercise rule | `[ ]` | Unmet (outside immediate software scope; requires `Refs #111`) | Primary-standards analytics research phases R1 to R3 (`docs/reference/research/iot-sensor-analytics-research-plan.md`), named domain-reviewer operational rule approval, live `SENSOR_REVIEW_DUE` operational task activation, and human assistive-technology/UI acceptance remain open governance and research work. Commit and PR must therefore use `Refs #111` rather than a closing keyword. |

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `### P01: Cross-Store Deterministic Sensor Analysis, Replay Canonicalization, and Review Draft Parity` | Reconciled | Plan markers `[x]`, phase-details `complete` status, changes summary, and diffs in `sensor_analysis.py`, `sensor_consumer.py`, `sensor_analysis_store.py`, and `sensor_review_draft.py` match `FR-1`..`FR-4`, `NFR-1`..`NFR-2`, and `PC-001`..`PC-003`. |
| `P02` (`P02-T01`) | `### P02: Focused Cross-Store Reproducibility Test Suite and Verification` | Reconciled | Plan markers `[x]`, phase-details `complete` status, `src/core/tests/test_sensor_reproducibility_111.py` (5 test methods, <= 10 limit, 0 existing test edits/removals, 0 `# type: ignore`), and passing Focused-tier validation record match `AC-1`..`AC-5`. |
| `## Follow-Up Items` | `## Follow-Up Items` | Reconciled | Both outside-scope items (pre-publication Full SQL gate with `ZF_SENSOR_MSSQL=1` and analytics research phases R1-R3) are mirrored across plan and changes records and kept outside active `P01`/`P02` acceptance claims. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | src/core/src/zava_forward/core/sensor_analysis.py, src/core/src/zava_forward/core/sensor_consumer.py | Added `default=str` in `_canonical_row`, added `_exact_row_key` and `_dedupe_exact_rows` in `_by_observation` and `reading_tuples` so exact-duplicate retained-reading replays collapse deterministically while conflicting rows remain distinct and fail closed (`INSUFFICIENT` / `DUPLICATE`), and added `reading_id` tie-breaking to `SensorConsumer.retained_envelopes` (`ORDER BY observed_at, sensor_id, reading_id`). | Verified in `sensor_analysis.py` and `sensor_consumer.py` diffs and proven by replay, conflict, SQL shuffle, and `reading_id` tie tests. | Passed (`test_sensor*.py`, `test_sensor_reproducibility_111.py`, `ruff`, `mypy`) | Reconciled |
| `P01-T02` | src/core/src/zava_forward/core/sensor_analysis_store.py, src/core/src/zava_forward/core/sensor_review_draft.py | Added `RetainedReadingSource`, `_JsonStoreCarrier`, `retain_json_readings`, `JsonRetainedStore`, and `retained_source` supporting `LIVE_VERSIONS`, `SCHEMA_VERSION` (`"sensor-fault-input-v1"`), and legacy `"reading-v1"` with strict string/field validation, idempotent replay merge, `IDENTITY_CONFLICT` rejection, `SqlStore` / `SensorMssqlConnector` dispatch guards, and cross-store `sensor_review_draft` parity while preserving `_sql(store) -> SensorConsumer(store)` and fail-closed unconfigured refusals (`RETAINED_READINGS_UNAVAILABLE`, `consent-withheld`). | Verified in `sensor_analysis_store.py` and `sensor_review_draft.py` diffs and proven across live/reloaded JSON `Store`, SQLite `SqlStore`, and `src/api/tests/test_sensor_review_draft_api.py`. | Passed (`test_sensor*.py`, `test_sensor_review_draft_api.py`, `ruff`, `mypy`) | Reconciled |
| `P02-T01` | src/core/tests/test_sensor_reproducibility_111.py | Added 5 focused tests proving `Store` vs `SqlStore` parity and reload durability, chunking/replay/shuffled-SQL-insert/tie-break order invariance, exact-replay idempotence vs conflict rejection, `INSUFFICIENT`/`STALE`/`DECLINED` fallback priority non-mutation and `SENSOR_REVIEW_DUE` deduplication, and fresh-subprocess `PYTHONHASHSEED` determinism, with zero edits to forbidden files. | Verified directly in `src/core/tests/test_sensor_reproducibility_111.py` and clean `git status --short` scope. | Passed (`5` tests in `test_sensor_reproducibility_111.py`, `ruff check`, `ruff format --check`, `mypy`, `tools/rename-zava-tests.py`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| None (test-fixture window bound inside `P02-T01` only) | Set `STAMP_END = "2024-01-30T00:00:00Z"` and used chunked `_ingest_pair` plus post-window `weather_window` (`[2024-01-29, 2024-01-30)`) in `test_sensor_reproducibility_111.py` so the 672-row scenario batch respects `preflight`'s 100-row batch ceiling and `SensorConsumer`'s 30-day `max_past_seconds` limit. | Triggered during local `unittest` verification in `P02-T01`; no user decision or plan/detail change required. | Recorded in `.copilot-tracking/changes/2026-11-15/111-reproducible-outputs-changes.md` under `## Implementation-Time Plan and Detail Updates`. | Not needed (`PC-001`..`PC-003` and plan readiness unchanged) | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All three critique items (`PC-001` matching `SCHEMA_VERSION = "sensor-fault-input-v1"` plus replay-merge and `SqlStore`/`SensorMssqlConnector` guards, `PC-002` separating `SensorConsumer.process` chunk/replay admission from shuffled physical SQL row insertion and `reading_id` tie-breaking, and `PC-003` typed `Protocol` / `Callable` wrappers for `save()` and `_ranking()` under `mypy --strict`) were applied before implementation and verified in the final code and tests.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: Phases executed sequentially (`P01` -> `P02`) with no material revision or premature resumption.
* Justification assessment: Fully supported by source diffs and passing Focused-tier validation checks.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| External Full SQL gate (`tools/rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1` and `--verify-receipt`) and hosted CI | Caller set Focused validation tier and prohibited `git push` in this session; repository policy requires the live-MSSQL Full gate and verified external receipt prior to pushing/publishing SQL-touching changes. | Branch owner / delivery coordinator before pushing `feat/iot-111-reproducible-outputs` or opening/merging its PR. | Open outside local no-push scope; routed as distinct pre-publication follow-up. |
| Analytics research phases R1 to R3 (`docs/reference/research/iot-sensor-analytics-research-plan.md`) and operational rule approval | Issue #111 criterion 3 and PRD `AC-068` require primary-standards research and named domain-reviewer sign-off before using derived measures beyond labelled `EXERCISE VALUE` rules. | Analytics researcher and named domain/compliance reviewer under Issue #111 (`Refs #111`). | Open outside `src/core` reproducibility slice; routed as distinct research/governance follow-up. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No defects, decision gaps, or material evidence gaps were found within the assessed `P01`-`P02` `src/core` reproducibility boundary.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | None | No `rpi-implement`, `rpi-plan`, or `rpi-research` remediation required for active `P01`-`P02` scope | Active `P01`-`P02` scope is conformant |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Pre-publication validation follow-up (outside local Focused/no-push boundary): Run `python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <new-external-directory>` with live `ZF_SENSOR_MSSQL=1`, verify the external receipt with `--verify-receipt`, and run hosted CI before pushing or merging.
* Issue #111 remaining governance/research work (`Refs #111`): Complete analytics research phases R1 to R3 (`docs/reference/research/iot-sensor-analytics-research-plan.md`), obtain named domain-reviewer approval before replacing `EXERCISE VALUE` labels or activating operational `SENSOR_REVIEW_DUE` tasks, and complete live UI/assistive-technology acceptance noted in Issue #111.

## Blockers and Remaining Work

* Blockers: None for the local Focused-tier `src/core` slice (remote push intentionally withheld per caller instruction).
* Remaining active work: None (`P01`, `P01-T01`, `P01-T02`, `P02`, and `P02-T01` are complete and verified).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `(cd src/core && PYTHONPATH=src:tests python3 -m unittest tests/test_sensor_reproducibility_111.py -v)` | `src/core/tests/test_sensor_reproducibility_111.py` | Passed | `Ran 5 tests in 306.673s — OK` across `Store` and SQLite `SqlStore`, SQL row-order/tie-break invariance, replay idempotence, `INSUFFICIENT` non-mutation, and `PYTHONHASHSEED` subprocesses |
| `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest discover -s src/core/tests -p 'test_sensor*.py' -q` | `src/core/tests/test_sensor*.py` | Passed | Existing sensor suites (`303` tests) plus all `5` tests in `test_sensor_reproducibility_111.py` passed with zero regressions |
| `(cd src/core && python3 -m ruff check .)` | `src/core` | Passed | `All checks passed!` |
| `(cd src/core && python3 -m ruff format --check .)` | `src/core` | Passed | `289 files already formatted` |
| `(cd src/core && python3 -m mypy)` | `src/core` (`strict = true`, 342 files) | Passed | `Success: no issues found in 342 source files` with zero `# type: ignore` additions |
| `(cd src/api && PYTHONPATH=src:.:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_sensor_review_draft_api.py -q)` | `src/api/tests/test_sensor_review_draft_api.py` | Passed | `Ran 6 tests in 8.677s — OK` confirming `SensorConsumer` mock seam compatibility |
| `python3 tools/rename-zava-tests.py` | Repository migration regression suite | Passed | `Ran 25 tests in 0.863s — OK` |
| `python3 tools/rpi-checks.py --all` (with `ZF_SENSOR_MSSQL=1`) and hosted CI | Full pre-publication SQL gate | Skipped | Explicitly deferred outside local Focused-tier no-push session; tracked as pre-push follow-up |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every planned requirement (`FR-1`..`FR-4`, `NFR-1`, `NFR-2`), acceptance criterion (`AC-1`..`AC-5`), critique disposition (`PC-001`..`PC-003`), and sibling-PR exclusion (`README.md`, `server.py`, `test_role_endpoint_inventory.py`, `pyproject.toml` untouched) is satisfied and verified. Against Issue #111, criterion 1 (`Outputs are reproducible from retained readings`) and criterion 2 (`Thresholds are sourced or labelled exercise values`) are proven and preserved across both `Store` and SQLite `SqlStore`, while criterion 3 (`Research phases R1 to R3 are complete before a derived measure is used beyond an exercise rule`) remains open outside this engineering slice, requiring `Refs #111` linkage.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | None | None |
| Decision gap or invalid assumption | None | None |
| Material evidence gap | None | None |
| Non-blocking residual work | Distinct follow-ups (`Refs #111`) | Pre-push live-MSSQL Full gate (`tools/rpi-checks.py --all` + `--verify-receipt` + hosted CI); analytics research phases R1-R3 and operational `SENSOR_REVIEW_DUE` / UI acceptance |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier passed (`test_sensor_reproducibility_111.py -v`, `test_sensor*.py`, `ruff check .`, `ruff format --check .`, `mypy` across 342 files, `test_sensor_review_draft_api.py`, and `tools/rename-zava-tests.py`); Full live-MSSQL gate deferred per no-push boundary
* Blockers: None
