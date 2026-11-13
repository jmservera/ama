# Details: 165 sensor and stock seed trace

* Probe imports `build_mvp_dataset` with `load_register` patched to the fictional register from `src/core/tests/test_generated_dataset.py` (`register()`), writes to a temp file, reads JSON.
* Sensor check: `sensor_stock.select(register_rows_with_consent_granted, homes=N)` then `.sensors(seed)`; map anchors to `sensor_identity.sensor_key`.
* Stock story: filter cases with `stock_epc.conflict_type != ""`, not closed; report ids, type, stage.
* Exit codes saved via direct `$?` to files; outputs hashed with sha256.
* Limits: fictional register only; deployed private store may differ; proposals not seeded by generators.

## Critique amendments
* Probe at `/tmp/probe-165.py`, sha256 and source recorded in changes file.
* All fixture rows set consent granted (hypothetical), select homes=len(rows), sensor seed 20260901.
* Report absent vs `[]` for `stock_reconciliation`; note shared anchors; fixture-only, deployed unknown.
