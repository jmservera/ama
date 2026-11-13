<!-- markdownlint-disable-file -->
# Details: 165-synth-coverage-pii-2244

## Phase 1: coverage evidence validation

* `src/core/src/zava_forward/core/synthetic/coverage.py`: add `coverage_evidence_issues(inventory) -> list[str]`; `build_baseline` raises `ValueError` listing the first issue; report gains `coverage_evidence_validated: true`.
* Rule per need: coverage in `COVERAGE`; nonblank `note`; non-empty `dataset_ids` of nonblank text; non-blank `gap_closure.note`.
* Tests in `tests/test_generator_coverage.py`: committed inventory passes; blanking each field is rejected; an invalid status is rejected.

## Phase 2: emission guards

* `privacy.py`: add `emission_issues(row)` = `record_issues(row, "source_type")`-style check requiring `source_type == "SYNTHETIC"` plus patterns; codes only, never values.
* `sensor_stream.wire`: after the size check, raise `StreamError("STREAM_ROW_NOT_SYNTHETIC")` or `StreamError("STREAM_ROW_PERSONAL_DATA")`.
* `device_provision.report`: add `source_type` and `contains_real_data`; `build_manifest`/`report` refuse a pattern-matching owner with `ProvisionError("CREDENTIAL_OWNER_PERSONAL_DATA")`.

## Phase 3: audit test

* `tests/test_synthetic_output_audit.py`: sample scale rows, live reading row, backfill wire frames, stream descriptor, provision report; assert labels and no pattern issues; negative cases for wire and report.
* Run: unittest for needs, manifest, coverage, privacy, sensor stream/backfill/provision/live tests; `ruff check`; `mypy`.
