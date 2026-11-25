---
title: Issue 2202 live changes 2026-11-25
ms.date: 2026-11-25
---

Refs #2202. Tier FULL (src/core change); targeted tests, mypy and ruff run locally; `rpi-checks.py --all` not run (the coordinator runs gates). No push, no PR, no Azure change.

## Changes

* `src/core/src/zava_forward/core/assistants.py`: `sensors` and `map_sensors` read through `_read_connection()` instead of the write-lock `transaction()`. Cause: the Home sensors tab got 503 and stayed on "Loading home sensors" while the receiver held the SQL write lock.
* `src/api/tests/test_map_sensors.py`: new test that neither read takes `transaction()`; the three overlay-failure tests inject failure through `_read_connection`.
* `docs/reference/research/issue-2202-live-r72-2026-11-25.md` and its evidence directory; index entry in `docs/reference/README.md`; entry in `docs/reference/log.md`.

## Validation

* api: test_map_sensors, test_quality_sensors, test_sensor_trend_summary, test_iot_seed_to_quality_ui_bridge (236 OK, 94 skipped), test_sensor_consistency, test_sensor_staleness_ui_badge (61 OK).
* mypy src/api clean; mypy src/core same 3 environment errors before and after; ruff check and format clean.
* Not run: full local gate, hosted CI, deployed-host proof of the fix.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Images rebuilt from main and rolled (API, resident, simulator, receiver) | Partly proven | All run and Healthy or Succeeded; digest-to-commit not readable (registry firewall); jobs and API run different digests. |
| Revisions Running and Healthy | Proven | az-state.txt |
| ZF_CONTAINER_HARDENING enforced with rollback noted, agents difference explained | Proven (enforced, agents idle by design); rollback noted, not exercised | az-state.txt; no drills authorised. |
| Sensor charts | Proven without contention; 503 under receiver load fixed in source, unproven live | live-chart-probe.json, diag-sensors-tab.png |
| Map gauges | Proven | live-map-card-probe.json |
| Consent checkbox | Proven | probe-resident-result.json |
| Chat routing | Proven (routing and refusal; answers workflow-only) | live_routing_probe.json |
| Half of homes with readings | Proven, 58.9% | coverage-result.json |
| Live receipt and log entry | Proven | research note and log entry |
