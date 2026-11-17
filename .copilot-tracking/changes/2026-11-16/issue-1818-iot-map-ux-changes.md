---
title: Issue 1818 changes
date: 2026-11-16
task_id: issue-1818
---

## Status

Implementation complete on `feat/iot-map-ux-visibility-1818` (base 5e0c7f744). Tier: FOCUSED (issue
scoped UX/API change on stored synthetic data; no infrastructure, SQL schema, deployment,
dependency or security-control change).

## Changes

* Core: new `sensor_map.py` (bounded latest synthetic reading per home, fail-closed consent, text
  states, cap 100, `calibrated: false`); `insights.attach_sensors` and `map_view(sensors=)`;
  `Store.map_view(sensors=)` computes outside the lock; `Assistants.map_sensors` projects by role and
  per-case `quality-evidence` authorisation.
* API: `/api/map` supplies the sensor provider. Clusters and the Coordinator map carry no sensor data.
* Employee UI (`app.js`, `style.css`): map-home-card sensor box, maplist and marker text, "Show only
  homes with stale or offline sensors" filter, Fluent tokens, non-colour text/badge cues.
* Resident (`resident_showcase.py`, `demo.js`): `sensors.freshness`, `source`, `calibrated`; "Reading
  status" badge and "Source" line; single-home isolation unchanged.
* Checks: `employee_acceptance_check.py` tolerates the sensor suffix on home labels;
  `map_fullscreen_browser_check.py` uses `.first` for the status locator (a tile note adds a second
  `role=status` when external tiles are blocked); `resident_sensors_browser_check.py` asserts status/source.
* Tests: `src/api/tests/test_map_sensors.py` (new), `SensorFreshnessTests` in core
  `test_resident_showcase.py`. README notes in `src/api/README.md`.

## Validation run

* `test_map_sensors`, `test_resident_showcase`, `test_resident_api`, `test_resident_demo_api`,
  `test_employee_acceptance_check`, `test_map_fullscreen`, quality-sensor and bulk-edit/procurement/
  sensor-consumer modules: pass when run serially.
* `checks.resident_sensors_browser_check`: pass.
* `checks.map_fullscreen_browser_check` with axe 4.10.3: one full PASS run (all checks, no axe
  violations, no JS errors). Other runs fail intermittently at timing-sensitive steps ("embedded
  browser shortcuts issue no map requests", "filter label and focus fit at 390x568"). The baseline
  commit fails the first of these every time on this loaded shared host, so this is recorded as an
  environmental flake, not a verified clean pass on every run.
* `ruff check` (core src, api src, changed tests/checks): pass. `mypy` in `src/core`: pass.

## Not run

Hosted CI, the complete local RPI gate and an external receipt. Core device-registry tests need
`azure-iot-hub` (absent: `SDK_MISSING`). `test_discovery_assistant_demo` worktree install test
fails because editable installs point at the main checkout. A first parallel suite run showed
spurious failures caused by another gate sharing the host and SQL; serial reruns passed.

## Open criterion

The live Azure IoT Hub walkthrough criterion in #1818 stays unticked. Any PR must use `Refs #1818`.
