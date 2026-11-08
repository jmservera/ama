---
title: "Changes: #184 correction 1"
ms.date: 2026-11-08
---

Source-only. No Azure change, send, grant, device registration or model call.

## Files

* `src/api/src/zava_forward/api/live_simulator.py`, `live_receiver.py` (F1, F3)
* `infra/live-receiver-job.bicep` (new), `infra/README.md` (F2)
* `src/api/README.md`, `src/api/tests/test_live_control.py`

## Validation (individual exit codes, output redirected to files)

| Check | Exit | Result |
| --- | --- | --- |
| Unit: test_live_control, test_live_simulator, test_iot_credential_hygiene, test_dependency_rule, test_live_readings, test_iot_stream | 0 | 127 tests OK |
| `ruff check --no-cache src/api`; `ruff format --check` | 0, 0 | pass |
| `mypy --cache-dir=/tmp/mypy-184` on live_receiver, live_simulator, live_control | 0 | no issues |
| `az bicep build` and `lint` (receiver and simulator jobs) | 0 | pass |
| Infra test_container_contract, test_identity_rbac, test_bicep_policy | 0 | 76 OK |
| `sensor_sql_check.py` under `flock -n /tmp/ama-rpi-heavy.lock`, task-owned SQL Server, worktree venv | 0 | 68 tests OK, 0 skipped |

The first SQL attempt exited 1 (4 import errors from stale editable installs of
another checkout); the rerun passed. The tests assert
`consumer.mssql == (ZF_SENSOR_MSSQL == "1")` and the check sets
`ZF_SENSOR_MSSQL=1`, so the MssqlStore backend was exercised. A JSON line
"passed": false, "refused": absent.csv in that output is a deliberate negative
test, not a failure.

Not run: browser suite, full gate, benchmarks, any cloud step.
