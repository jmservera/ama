<!-- markdownlint-disable-file -->
# Plan: #176 criteria evidence (validation-only)

* Date: 2026-11-13. Research: `.copilot-tracking/research/2026-11-13-demo-generator-determinism-176-0638-research.md`.
* Scope: execute bounded existing tests and the existing audit CLI against frozen main; record per-command true exit codes; write changes and review artifacts. No source, test, generator or policy change.
* Deviation disclosed: discovery runs of the same commands happened during Research (all exit 0). The Implement phase repeats them in a fresh output directory so the recorded evidence follows the plan.

## Phases

* P1 Environment: new exclusive venv, `pip install ./src/core` (core has no third-party dependencies; guide requires installed distribution, no PYTHONPATH workaround).
* P2 Commands (cwd `src/core`, `TMPDIR` inside the exclusive directory, direct exit capture, no pipes):
  * `python -m unittest -v tests.test_synthetic_determinism tests.test_stock_register tests.test_determinism_audit`
  * `python -m unittest -v tests.test_sensor_stream.ReplayTests.test_descriptor_records_seed_version_and_full_generator_revision tests.test_sensor_stream.ReplayTests.test_generator_revision_changes_with_each_source_and_composition tests.test_sensor_scenarios`
  * (superseded after critique) whole-module `tests.test_stock_fabric` is replaced by three named tests, see Critique.
  * six named `tests.test_generated_dataset.GeneratedDatasetTests` determinism and manifest tests (excluding the SQL restart test).
  * `python -m zava_forward.core.synthetic.determinism_audit`, JSON report kept.
* P3 Disposition: map results to C1/C2 per generator; keep the original private stock register gap and the 16-hex support revision as explicit limitations.
* P4 Freeze: commit only `.copilot-tracking` artifacts with repo-local privacy-safe email and Copilot trailer; independent Review of the final committed evidence.

## Stop conditions

* A failing selected test is recorded as a confirmed gap with a future initial-scope plan, not repaired.
* No defect or coverage gap is invented to fill capacity.

## Critique

Independent rubber-duck critique executed once, verdict Revise. All findings verified against source and applied directly (none conflicts with a confirmed decision):

* SQL test: discovery run of whole `tests.test_stock_fabric` included `test_connected_60000_home_980_case_builder_and_closed_sqlite_restart`. That run is disclosed and discarded as evidence; the rerun selects `test_legacy_seeded_draws_are_unchanged`, `test_cli_determinism_hashes_defaults_and_explicit_failures` and `test_revisions_cover_moved_dependency_and_ignore_physical_roots` only.
* Install: `pip install ./src/core` uses build isolation and may fetch setuptools from the network; disclosed, no network isolation claimed. The new venv is exclusive.
* Inventory widened: `zf_documents.py`, `zf_document_controls.py` (fixture JSON headers) and `live_readings.py` (pure-function live generator) added; `src/importer/tests/test_document_form_fixtures.py::test_deterministic_and_labelled_synthetic` and `test_live_readings.GeneratorTests` are added to the run.
* Matrix corrections: stream manifest is written by the audit from `descriptor()`, not by the generator; its replay origin is fixed, not as-of driven; EPC `--manifest` is a conflicts CSV, provenance is in `summary.json`; MVP receipt bytes are not compared by the selected test; `test_sensor_scenarios.test_snapshot_bytes_hashes_schema_and_no_truth_leakage` itself byte-compares written files.
* Disposition rule: exit 0 is not criterion completion; unavailable generators (original stock register), the public-pack seed-7 validation refusal and untested items are dispositioned explicitly.
