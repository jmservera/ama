---
title: Issue 184 simulator CLI credential leak guard
ms.date: 2026-11-23
---

Scope: criterion "No device key or connection string in source, logs or telemetry" on #184 (demo, synthetic).

Probe (2026-11-23, constructed, no Azure call): `live_simulator.main` was run with a marker connection string in each of `ZF_SIM_HUB_HOSTNAME`, `ZF_SIM_APPROVAL`, `ZF_SIM_RESOURCE_GROUP`, `ZF_SIM_SEED`, `ZF_SIM_FAILURE_RATE`, `ZF_SIM_CADENCE_MINUTES` and `ZF_ASSIST_QUALITY_DEMO_HOMES`, and with a `RuntimeError` carrying it from the store. Every run exited 2 or 4 with only a stable code (`IOT_ACTIVATION_REQUIRED`, `SIM_CONFIG_INVALID`, `DEMO_HOMES_INVALID`, `SIM_FAILED`).

Regression guard: `CliLeakTests` in `src/api/tests/test_iot_credential_hygiene.py` (15 tests in the module pass). Not proven: live message bodies, because Event Hubs is network-private for the demo.
