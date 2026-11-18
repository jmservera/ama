# Issue #111 criterion 6 research (2026-11-14)

* Research disposition: executed. Planning Readiness: Ready.
* `src/core/src/zava_forward/core/sensor_analysis.py` already carried `ANALYSIS_VERSION`, `policy_version` and `input_digest` on every `Signal`; `sensor_analysis_store.analyse_retained` reads retained readings.
* Gaps: the digest hashed whole row dicts rather than `(sensor_id, metric, timestamp, value, unit)` tuples; no pure reproduction function from retained readings; no API-level test module.
* Decision: keep the existing version label `sensor-analysis-exercise-v1` (labelled exercise, not a sourced standard); no thresholds are sourced.
