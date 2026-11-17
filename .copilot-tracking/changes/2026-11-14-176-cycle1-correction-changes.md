# #176 Cycle 1 correction changes (2026-11-14)

* `src/core/src/zava_forward/core/synthetic/resident_preview_fixture.py`: deterministic `build(seed, as_of)`, provenance fields, `VERSION`, `SEED`, `AS_OF`, `revision_sources()`.
* `src/core/src/zava_forward/core/synthetic/sensor_backfill.py`: `generator_revision` in truth manifest.
* `src/api/src/zava_forward/api/resident_preview/__main__.py`: `--as-of` (default today).
* Tests: `test_generator_determinism_matrix.py` (preview under clock/uuid guards, fault-rates revision); `test_resident_preview.py`, `test_resident_preview_api.py` pass `as_of=date.today()`.
* Validation: focused core tests (matrix, scenario_manifest, needs_inventory, resident_preview, sensor_scenarios, determinism_audit, sensor_privacy) and api resident preview tests pass; scoped ruff check/format pass on touched files. Repo-wide `ruff` and `mypy src` already fail at baseline (not caused here); touched files add no mypy errors. `scenario-manifest.json` needed no refresh.
