---
title: Changes for #184 live simulator container slice 1
ms.date: 2026-11-04
---

* Added: `src/core/src/zava_forward/core/synthetic/live_readings.py`, `src/core/tests/test_live_readings.py` (19 tests).
* Added: `src/api/src/zava_forward/api/live_simulator.py`, `src/api/tests/test_live_simulator.py` (24 tests).
* Added: `src/api/live-simulator.Dockerfile`, `infra/live-simulator-job.bicep`.
* Edited: `src/api/README.md`, `infra/README.md`, `docs/reference/research/iot-sensor-analytics-research-plan.md` (ms.date 2026-11-04), `docs/reference/log.md`.
* Divergence: none from plan. Amendment: runner placed in `api`, not a new project, to avoid CI registry changes.
* Validation run: unit tests above plus `test_iot_credential_hygiene`, `test_iot_stream`-adjacent `test_dependency_rule` (api); ruff check and format; mypy with `--cache-dir=/tmp/mypy-184` on the new files; `az bicep build` and `az bicep lint`; infra `test_identity_rbac` and `test_container_contract` (pass).
* Not run: complete gate, `rpi-checks.py`, benchmarks, full suites, docker build, any Azure what-if or deployment, live send. Infra `test_iothub_module` could not be imported with the module path used.
