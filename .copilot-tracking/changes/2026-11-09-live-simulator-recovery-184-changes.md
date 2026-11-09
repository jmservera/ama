---
title: "#184 recovery changes: main reconciliation and ten-test sensor contract"
ms.date: 2026-11-09
---

Pre-merge HEAD 57d152760. Merge commit cc8c478c1 brought in origin/main b46a9ad9a (#1299) with no conflicts and no src/infra overlap.

## Edits

* src/api/tests/test_sensor_sql_check.py: default-selection test now expects the six candidate selectors; analysis count literals 8 to 10.
* src/api/checks/sensor_sql_check.py: ANALYSIS_TESTS 8 to 10 (exact count and clean OK still required, so any skip still fails).
* tools/rpi-checks.py: SENSOR_MSSQL_REQUIRED_TESTS gains test_live_weather_rows_are_not_indoor_input and test_weather_only_window_is_insufficient_with_explicit_reason. No runner logic changed.
* tools/test_rpi_checks.py: four count literals derived from the pinned tuple length.
* src/api/README.md: "exactly eight" to ten with the reason.

## Results (venv /home/azureuser/venv-184 with editable worktree installs; logs under /home/azureuser/logs-184, not committed)

| Step | Result |
| --- | --- |
| core unit: test_sensor*.py | 192 run, OK, 11 skipped (opt-in SQL/flag tests, covered by the SQL runs below) |
| core unit: test_device*.py / test_live*.py / test_resident_sensors.py | 48 / 22 / 10 OK |
| api unit: test_live*.py (control, receiver, simulator, expiry) | 66 OK, 2 skipped (SQL opt-in) |
| api unit: test_iot*.py | 49 OK |
| api unit: test_sensor*.py | 103 OK |
| api: test_sensor_sql_check | 4 OK |
| tools.test_rpi_checks | 102 OK (after fixing one NameError in my own edit) |
| Owned SQL, selector default (before the test-only edits; harness unchanged for this selector) | 70 run, OK, 0 skips, exit 0 |
| Owned SQL, selector analysis, first run with harness at 8 | 10 run, OK, harness "rejected", exit 1 (reproduced the owner-reported contract defect) |
| Owned SQL, selector analysis after reconciliation | 10 run, OK, 0 skips, accepted, exit 0 |

SQL ran on task-owned loopback containers (mssql 2022-latest) removed after each run, under the shared nonblocking heavy lock; the lock was busy for about 20 minutes with another lane and was retried, not queued.

## Not run (missing prerequisites or not applicable)

* Browser checks: playwright not installed in the venv, and the parent changes no web asset, route or template. test_workbench_live_defaults and test_employee_live_acceptance failed to import for that reason and are not claimed.
* No rpi-checks --all or --changed, ruff or mypy results claimed (system ruff reports unrelated pre-existing findings under its default config; project config not exercised).
* No live IoT, cloud, model or credential action.
