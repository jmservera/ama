<!-- markdownlint-disable-file -->
# Changes: Epic 165 IoT, cohort and scenario join parity (2026-11-14)

Refs #165. Focused validation tier (test-only; no workflow, dependency, Dockerfile, SQL or security-control change).

## Added

* `src/core/tests/test_epic165_iot_cohort_scenario_join_parity.py` (7 tests): sensors, readings, households, events and PAS 2035 stages join one-to-one on `ZF-nnnnn` for seeds 165 and 166 with zero orphans; property archetype and EPC consistency and journey joins; manifest case ids, reviewed needs and dataset ids resolve; no PII patterns; byte-identical replay per seed.

## Validation

| Check | Result |
| --- | --- |
| New suite | 7 tests OK |
| `test_scenario_manifest`, `test_needs_inventory`, all `test_*synthetic*` and `test_epic165_*` in core | 82 tests OK (`PYTHONPATH=src:tests`) |
| Importer `test_epic165_*` | 5 tests OK (`PYTHONPATH=src:../core/src`) |
| `ruff check`, `ruff format --check`, `mypy` (from `src/core`) | pass; one import-order fix applied |

## Not run

* Hosted CI, independent exact-head review and the complete local gate (not required for this tier).
