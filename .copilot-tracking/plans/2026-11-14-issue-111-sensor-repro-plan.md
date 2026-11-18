# Issue #111 criterion 6 plan (2026-11-14)

* [x] Replace `_digest` with SHA-256 over canonical sorted reading tuples; add `reading_tuples`.
* [x] Add pure `reproduce_sensor_analysis(retained_readings, thresholds=...)`.
* [x] Add `src/api/tests/test_sensor_analysis_reproducibility.py`.
* [x] Validate with the fast formula and core reproducibility/store tests.
* Critique: one pass, no conflicting findings. Scope excludes new HTTP endpoints (no sensor analysis route existed to project).
