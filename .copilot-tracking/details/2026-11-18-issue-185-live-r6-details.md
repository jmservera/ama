---
title: Issue 185 live r6 phase details
ms.date: 2026-11-18
---

* Phase 1: `SasEnrollment(device_id)` validated with `DEVICE_ID`; `Enrollment` union; thumbprint uniqueness checks only X.509 items; `create` builds `AuthenticationMechanism(type="sas")` without `symmetric_key`. Delete, `run_of`, `list_run` are unchanged because they key on the marker and ETag, not the credential.
* Phase 2: reuse `HubSimulator`; extend its create response in tests with fake generated keys to prove they are discarded. Environment: venv with `azure-iot-hub==2.7.0` and `six==1.17.0` (system python lacks the SDK, so 34 baseline tests fail without it).
* Phase 3: hub has public access disabled; a job in `cae-cutover-test-demo` is needed, and the image must contain `azure-iot-hub`. Check the image first.
* Phase 4: focused gates: unittest, mypy, ruff format and check for `src/core`.
