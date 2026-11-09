---
title: "#184 recovery details"
ms.date: 2026-11-09
---

## Owner-selected demo-targeted tier

Per the 2026-11-09 brief the blanket full gate is replaced for this demo push: no rpi-checks --all, no old receipt treated as current. Hosted checks and independent exact-head review remain mandatory; a failing selected test is not waivable.

## Commands (venv /home/azureuser/venv-184, PYTHONPATH src/api/tests:src/core/tests:src/agents/tests)

* Core unit: discover test_sensor*.py, test_device*.py, test_live*.py, test_resident_sensors.py in src/core.
* API unit: discover test_live*.py, test_iot*.py, test_sensor*.py in src/api; test_sensor_sql_check.
* Owned SQL: flock -n /tmp/ama-rpi-heavy.lock python src/api/checks/sensor_sql_check.py --selector default, then --selector analysis. Task-owned loopback container, removed after each run. If the lock is busy, do other work and retry; never queue.
* Gate tooling: python -m unittest tools.test_rpi_checks (pins changed).

## Stop conditions

A selected failure; a skip in the SQL selectors; an edit needed in runner logic or outside the named files.
