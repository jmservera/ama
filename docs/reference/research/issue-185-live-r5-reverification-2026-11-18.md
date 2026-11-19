---
title: Issue 185 fifth live re-verification (demo)
description: Per-criterion re-check of the two unticked criteria of issue 185 against the live demo hub, repository tests and retained logs on 2026-11-18
author: AMA RPI agent
ms.date: 2026-11-18
ms.topic: reference
keywords:
  - issue 185
  - iot hub
  - device identity
estimated_reading_time: 3
---

Refs #185. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18 (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes). No source changed and no identity was created: the earlier [three-run evidence](issue-185-live-device-identity-evidence-2026-11-18.md) and [fourth audit](issue-185-live-r4-audit-2026-11-18.md) already hold the issuance proof, and a new run on a shared hub risks the id collision seen in run 3.

## Checks run (17:04 UTC)

| Check | Result |
| --- | --- |
| `az iot hub show-stats -n [hub]` | total, enabled and disabled device counts all 0 |
| `az iot hub show` | SKU B1, public network access Disabled, local auth disabled |
| IoT role assignments on the hub | one IoT Hub Registry Contributor dated 2026-10-30, pre-existing; no assignment left from any 185 run |
| Container Apps jobs in group `ama` whose name contains 185 | none |
| Retained logs (run 2 job log, run 3 job log, run 3 operator output): matches for `primaryKey`, `secondaryKey`, `SharedAccessSignature` | 0 in each file |
| Repository search under `docs`, `src`, `infra` for `SharedAccessSignature sr=` or a 40-character `primaryKey` value | only scrubber test fixtures in `test_live_provisioning.py` and `test_iot_credential_hygiene.py` |
| `src/api` `test_iot_credential_hygiene` | 12 tests OK |
| `src/core` `test_device_provision`, `test_live_provisioning` | 24 tests OK |

An unrelated job `tmp146d-failjob` exists in the group; it is not a 185 resource and was left alone.

## Per-criterion table

| Criterion in #185 | Demo status | Evidence |
| --- | --- | --- |
| Credentials are issued and stored without appearing in source or logs | Proven for issuance and no-leak; durable storage not proven | Hub-issued keys existed only in job memory in runs 1 to 3; the retained logs and the repository scan show no key text; tests pass. "Stored" means in-memory for the run because the owner excluded Key Vault work |
| Teardown removes all simulated identities | Proven for the demo hub | Delete 204 and empty read-back in runs 1 to 3; hub-wide count 0 again now, with no 185 job or role assignment left |

## Not provable for the demo

* A durable secret store, rotation and a named production credential owner (Key Vault excluded; production out of scope).
* X.509 issuance; the repository adapter supports X.509 thumbprints only, so SAS provisioning by repository code is separate work.
* Scale to N homes, MQTT transport and a repeatable repository command for the live SAS flow.
* The hub count is a point-in-time read; it does not show absence at other times.

The issue stays open; this note ticks nothing.
