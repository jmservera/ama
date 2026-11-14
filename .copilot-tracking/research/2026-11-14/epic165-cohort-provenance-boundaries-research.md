# Research: Epic #165 cohort provenance and boundary tests (2026-11-14)

Disposition: executed. Planning Readiness: Ready. Branch: test/demo-165-cohort-provenance-0432, stacked on test/demo-165-seed-reproducibility-0341 (#1629). Refs #165.

## Findings

* `scenario_manifest.validate_manifest` checks the #103 manifest structure. `needs_inventory.py` does not exist; only `needs-inventory.json` and `test_needs_inventory.py` do.
* `scenario-manifest.json` carries top-level `is_synthetic: true`, `contains_real_data: false`, warning, fixture_provenance and coverage_note. Profiles and workflows are per-entry `unavailable` with reason and safe_endpoint (the boundary).
* Dataset entries live in `provenance-register.json` (visibility, data_dictionary, personal_data) and `src/agents/evals/registry.json` (`contains_real_data`).
* No existing benchmark split covers the six required categories. Deterministic sources: `scale_fixture` homes (open_safety_issue) and households (consent, adjustment, representative), and `sensor_scenarios.generate` (sensor_fault, missing_data).
* New test must pass ruff format and strict mypy.

## Boundary

Synthetic fixtures only; no private datasets read. Tests establish neither fairness evidence nor owner approval.
