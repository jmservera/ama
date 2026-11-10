---
title: Changes for #184 slice 2
ms.date: 2026-11-08
---

* Merged (no reset, rebase or force): fast-forward to remote parent `9476dc96`, then `origin/main` `ecb28815` as `e41546ab`; one conflict in `src/api/checks/sensor_sql_check.py` resolved by keeping main's selector structure plus the parent's extra default tests.
* Added `src/api/src/zava_forward/api/live_control.py` (control document, expiry and stop decision, atomic CLI) and `live_receiver.py` (bounded receiver host entry).
* Changed `live_simulator.py`: `--control-file`, hub sink requires it, cohort limited to control homes present in the store, per-slot fail-closed gate, nothing sent when stopped or expired.
* Changed `infra/live-simulator-job.bicep` (control file env var, share holds `control.json`); compiled and linted.
* Docs: `src/api/README.md` (cohort and control, frozen retained interface), `infra/README.md` (finite deployment plan).
* Tests: `src/api/tests/test_live_control.py` (18 tests; control, CLI, cohort, gate, receiver with fakes).
* Validation run: `test_live_control`, `test_live_simulator`, `test_iot_credential_hygiene`, `test_dependency_rule`, `test_live_readings`, `test_iot_stream` (119 OK); ruff check and format, mypy `--cache-dir=/tmp/mypy-184` on the four changed Python files; `az bicep build` and `lint`; infra `test_container_contract`, `test_identity_rbac`, `test_bicep_policy` (76 OK).
* Not run: complete gate, `rpi-checks.py`, full suites, SQL or browser suites (no UI, SQL or store change), docker build, what-if, any Azure write, send or model call.
* Divergence: the merge commit preceded the prospective plan file; recorded in research.
