---
title: Issue 185 SAS enrolment in the repository registry adapter (demo)
description: Per-criterion status of issue 185 after adding Hub-generated SAS enrolment to the keyless IoT Hub registry adapter, with test evidence and stated limits
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 185
  - iot hub
  - device identity
estimated_reading_time: 4
---

Refs #185. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18. This round changed source: the earlier [live evidence](issue-185-live-device-identity-evidence-2026-11-18.md) listed as a gap that `device_registry_azure.py` supported X.509 thumbprints only, while the owner chose Hub-generated symmetric keys for the demo.

## Change

* New `SasEnrollment(device_id)` beside `X509Enrollment`; an `EnrollmentSpec` may mix both.
* `create` for a SAS enrolment sends `authentication.type = sas` with no key, so the Hub generates the pair. The identity starts DISABLED with the run marker and `If-None-Match: *`, exactly as the X.509 path.
* The adapter never reads, returns or logs a key; the create response is discarded. Delete, ownership read and run listing are unchanged (marker plus exact ETag).
* Activation and durable storage of the keys remain with the credential lifecycle, outside the adapter.

## Evidence (local, run with `azure-iot-hub==2.7.0` and `six==1.17.0` in a venv)

| Check | Result |
| --- | --- |
| `src/core` `test_device_registry_azure` (39 baseline plus 4 new SAS tests, real SDK serialisation over a simulated Hub) | 43 OK |
| `test_device_registry_azure`, `test_device_identity`, `test_device_provision`, `test_live_provisioning`, `test_iot_device_identity_enforcement` | 125 OK |
| `src/api` `test_iot_credential_hygiene` | 12 OK |
| `mypy` in `src/core` | no issues in 396 files |
| `ruff check`; `ruff format --isolated --line-length 100 --check` on the two changed files | pass |

The new tests show the request body holds no key; a key placed in the simulated Hub response reaches no return value, log (`assertNoLogs`), repr, error or traceback; owned SAS identities are deleted with the exact ETag and none remain; invalid or duplicate ids are refused.

Without the SDK installed (system Python) the 39 baseline tests report 34 failures and 16 errors; that is environmental and was seen before the change.

## Per-criterion table

| Criterion in #185 | Demo status | Evidence |
| --- | --- | --- |
| Credentials are issued and stored without appearing in source or logs | Issuance and no-leak proven live (rounds 1 to 3, out-of-repository driver) and now by repository code in simulator tests; durable storage not proven | Live notes linked above; new tests |
| Teardown removes all simulated identities | Proven live for the demo hub (in-job delete 204 and empty read-back; hub count 0 in r5); repository adapter delete proven in simulator tests only | Live notes; `DeleteTests`, `SasEnrollmentTests` |

## Not proven

* The new adapter code was not run against the live hub. The hub has public network access disabled, the demo API image does not contain `azure-iot-hub`, and running the code live needs a new image pushed to the shared registry, a change beyond the demo authorisation. The simulator is a local contract test, not proof of Azure behaviour.
* Durable secret storage, rotation and a production credential owner (Key Vault excluded; production out of scope); X.509 issuance; scale to N homes; MQTT.
* FULL-tier gate: `src/core` changed, so the coordinator must run the complete local gate and verify the receipt; this worker did not run `rpi-checks.py --all`.

No Azure resource was created or changed in this round. The issue stays open; nothing is ticked.
