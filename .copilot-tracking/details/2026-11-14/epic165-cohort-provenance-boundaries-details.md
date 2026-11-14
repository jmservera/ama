# Details: Epic #165 cohort provenance and boundary tests

File: `src/core/tests/test_epic165_synthetic_provenance_boundaries.py`

* Phase 1: assert manifest synthetic flags, per-entry boundaries, register dataset stance, eval registry `contains_real_data` false, no UPRN or UK postcode in public metadata, and fixture addresses and postcodes matching the fictional Test Road and TE# 1ST patterns.
* Phase 2: derive categories (normal, exception, safety_escalation, accessibility_language_support, resident_refusal, degraded_telemetry) by fixed precedence from seeded fixtures; split into development and evaluation; assert determinism, per-split coverage, disjoint IDs, one category per case and stable assignment as the cohort grows.
* Phase 3: run the validation commands from the task.
