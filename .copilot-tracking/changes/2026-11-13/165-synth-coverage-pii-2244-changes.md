<!-- markdownlint-disable-file -->
# Changes: 165-synth-coverage-pii-2244

Plan: [.copilot-tracking/plans/2026-11-13/165-synth-coverage-pii-2244-plan.md](../../plans/2026-11-13/165-synth-coverage-pii-2244-plan.md)

## Added

* `src/core/tests/test_synthetic_output_audit.py`: audits scale fixture, stream frames (every fault), stream descriptor, live reading row and provisioning report for labelling and patterns; negative wire and report cases.

## Modified

* `src/core/src/zava_forward/core/synthetic/coverage.py`: `coverage_evidence_issues`; `build_baseline` rejects a need without valid status, note, volume, owner or dataset ids; report adds `coverage_evidence_validated`.
* `src/core/src/zava_forward/core/synthetic/privacy.py`: `emission_issues` (label and pattern codes, no values).
* `src/core/src/zava_forward/core/synthetic/sensor_stream.py`: `wire` refuses non-SYNTHETIC or pattern-matching rows (`STREAM_ROW_NOT_SYNTHETIC`, `STREAM_ROW_PERSONAL_DATA`) after the size check.
* `src/core/src/zava_forward/core/synthetic/device_provision.py`: report labelled `source_type=SYNTHETIC`, `contains_real_data=false`; personal-data owner refused (`CREDENTIAL_OWNER_PERSONAL_DATA`).
* `src/core/tests/test_generator_coverage.py`: seven new field mutations and the new report flag.

## Validation (Focused tier, pip venv `/tmp/venv-165-2244`, removed afterwards)

* unittest (discover per module) passed: synthetic_output_audit 5, generator_coverage 16, needs_inventory 11, scenario_manifest 8, sensor_stream 15, device_provision 10, device_identity 40, sensor_privacy 17 (1 skipped), synthetic_determinism 8, sensor_backfill 5, sensor_faults 10, sensor_stock 16, sensor_scenarios 16, synthetic_provenance 12, cutover_audit 9, determinism_audit 16.
* `ruff check .` clean; `mypy` clean (301 files).
* Not run: full local gate, hosted CI. No inventory coverage values changed; owner approval stays not-established.

## Critique (single, final candidate)

* Executed once, self-critique. Verdict: proceed. Applied: size check precedes the label check so the existing oversize contract is unchanged; fixed error codes never echo matched values.
