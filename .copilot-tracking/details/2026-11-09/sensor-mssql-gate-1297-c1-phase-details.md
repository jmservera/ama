---
title: Phase details - #1297 correction C1
date: 2026-11-09
---

## P01 Selection rule and tests

* P01-T01: in `changed_groups`, inside the `src/<project>` branch, add `project == "core" and "sensor" in path.lower()` to the mssql condition. Evidence: research C1-C4.
* P01-T02: tests in tools/test_rpi_checks.py (existing class near test_changed_selection_mapping_and_closure): affected paths select mssql; unrelated paths (api sensor module, non-sensor core) do not gain mssql through this rule; selection for a sensor-only change includes the sensor command with expected count and flag via the matrix; no test claims execution. Test ownership: add only (no removals), at most two new methods.
* Validation: `cd tools && python3 -m unittest test_rpi_checks`; ruff and mypy --strict as in the original changes record. Heavy validation by coordinator.

* Critique corrections: T01 also updates `SKIP_REASONS["mssql"]` text (add sensor); T02 asserts via `required_checks` (receipt with executed_groups from changed_groups) that the flagged sensor command is present with `required_sql_count` 8, and that unrelated paths (core non-sensor, api sensor_ingestion.py) do not gain mssql through the sensor rule. Use subTest, at most two new methods.
