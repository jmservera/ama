---
title: Issue 185 fourth live audit, repository checks and hub state (demo)
description: Per-criterion audit of issue 185 against repository code, local tests and the live demo hub on 2026-11-18, with production-only items separated
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 185
  - iot hub
  - device identity
estimated_reading_time: 4
---

Refs #185. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes; Azure billing reconciliation, DPO/Legal approval and person-run assistive-technology testing not needed). This audit adds no new identities; it re-checks the earlier [three-run evidence](issue-185-live-device-identity-evidence-2026-11-18.md) against the repository and the hub as they stand now.

## Checks run

| Check | Result |
| --- | --- |
| `src/core` tests `test_device_registry_azure`, `test_iot_device_identity_enforcement` with the optional `iothub` extra installed in a throwaway virtual environment (removed afterwards) | 55 tests OK (observed; raw output not retained) |
| `src/core` tests `test_device_provision`, `test_live_provisioning` | 24 tests OK |
| `src/api` test `test_iot_credential_hygiene` | 12 tests OK |
| Same core tests without the optional SDK | 34 failures and 16 errors, all `SDK_MISSING` from the default-off adapter; adverse observation kept, it is the install gate, not a defect |
| Repository search for `SharedAccessSignature sr=` and 40-character `primaryKey` values under `docs`, `src`, `infra` | Only test fixtures that assert the scrubbers catch such strings (`test_live_provisioning.py`, `test_iot_credential_hygiene.py`); no real credential |
| `az iot hub show-stats` on the demo hub at about 16:11 UTC | total, enabled and disabled device counts all 0 |
| Hub settings (observed; raw output not retained) | public network access Disabled, local auth disabled, SKU B1, unchanged |
| IoT role assignments on the hub | one IoT Hub Registry Contributor dated 2026-10-30, pre-existing and untouched |
| Throwaway jobs in group `ama` | no `job-185*` job remains |

The hub-wide zero closes the adverse observation in run 3: the three same-id devices seen at 12:39 to 12:41 UTC are gone, so no simulated identity is left on the demo hub.

## Per-criterion table

| Criterion in #185 | Demo status | Evidence |
| --- | --- | --- |
| Approach decided and recorded with the owner of credentials | Proven (already ticked) | Owner decision 2026-11-18, Hub-generated symmetric keys; `live_provisioning.py` records the SAS approach with opaque `secretref://` addresses |
| Each simulated home maps to one device identity and one stock home ID | Proven (already ticked) | Source tests above; run 3 `one_device_per_home: true` using repository `sensor_key` |
| Credentials are issued and stored without appearing in source or logs | Issuance and no-leak proven for the demo; durable storage unproven | Runs 1 to 3: Hub-issued keys held in process memory only, `key_in_output: false`, 0 log matches; this audit's repository scan clean. Key Vault storage was excluded by the owner, so "stored" is in-memory only |
| Teardown removes all simulated identities | Proven for the demo hub | In-job delete 204 and empty read-back (runs 1 to 3); hub-wide count 0 today |

## Production-only items, not proven and not demo scope

* Durable secret store, rotation and named credential owner in production.
* X.509 issuance and the production receiver; the repository adapter supports X.509 thumbprints only, so SAS provisioning by repository code remains separate work (the live runs used a driver outside the repository).
* Scale to N homes (three identities were created), MQTT transport, and a repeatable repository command for the live SAS flow.
* Independent exact-head review and hosted CI for the evidence commits.

## Limits

No identities were created in this run, so it adds no new issuance proof. The 16:11 UTC hub count is one read by the operator; it does not prove the absence of identities at other times. The issue stays open; this note does not tick any criterion.
