# Changes: issue #176 generator determinism and manifest fields

* Date: 2026-11-14
* Plan: `.copilot-tracking/plans/2026-11-14/176-generator-determinism-manifest-plan.md`

## Added

* `src/core/tests/test_generator_determinism_matrix.py`: three tests.
  * Every generator in `determinism_audit.GENERATORS` is byte-identical across fresh interpreters with different hash seeds while wall clock and uuid raise; manifests carry `seed`, `version`, `generator_revision` (full sha256).
  * Stock register payload ignores `as_of` while its manifest records it; sensor backfill honours `as_of`.
  * `scale_fixture` manifests record each seed, version and revision.

## Divergences

* None. No generator source needed change.

## Validation (in `src/core`, `PYTHONPATH` set to worktree sources)

* `python3 -m unittest` on the new matrix, `test_scenario_manifest`, `test_needs_inventory`, `test_determinism_audit`, `test_synthetic_determinism`, `test_stock_register`, `test_sensor_stock`, `test_synthetic_provenance`, `test_synthetic_output_dir`: OK.
* `mypy .`: no issues in 308 files. `ruff check .`: passed. `ruff format --check .`: passed.
* Guard sanity: injecting `date.today()` into the guarded script made the replay fail as intended.
* Not run: the full `src/core` unittest discovery (exceeded practical time here); hosted CI must cover it. No other package touched.
