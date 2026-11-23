---
title: Issue 2128 live credential storage and teardown proof (demo)
description: Per-criterion proven and unproven results for the two remaining acceptance criteria of issue 2128, measured against main, the live revisions and a throwaway IoT Hub
author: AMA RPI agent
ms.date: 2026-11-23
ms.topic: reference
keywords:
  - issue 2128
  - issue 185
  - iot hub
  - key vault
estimated_reading_time: 4
---

Refs #2128 (split from #185). Scope is the synthetic desktop demo under the owner decisions of 2026-11-18: resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change. No credential file was read or printed. Raw evidence is in `.copilot-tracking/evidence/2026-11-23/issue-2128-live/`.

## Main versus live

* Main (dbf4e45fa7) holds `DurableSasCredentialStore` and `KeyVaultSecretBackend` (`live_provisioning.py`) with unit tests, added after the [2026-11-19 live note](issue-185-live-20261119-2026-11-19.md) found storage unproven. The `device_provision` command line still built only the in-memory store, so no command could store credentials durably.
* Live revisions: API `ca-cutover-test-demo-api--0000054` (image digest `3f2be664...`), simulator job image digest `295164ca...`. The demo hub `iot-cutover-test-rzsrg` is B1 with public access and local auth disabled; its data plane returns 401002 from this VM.
* The 288 enabled hub identities belong to the running live simulator (issue 184), whose X.509 keys sit in a Container Apps `Secret` volume (577 job secrets). They are intentionally live and were not touched.

## Observed

| Check | Result |
| --- | --- |
| Log Analytics `ContainerAppConsoleLogs`, last 24 h | 1,113,253 lines (1,105,302 simulator); 0 matches for PRIVATE KEY, BEGIN CERTIFICATE, SharedAccessSignature, primaryKey, SharedAccessKey, `sig=` values |
| Throwaway F1 hub `iot-thr2128-258`, current main `device_identity.provision` and `teardown` with the real adapter and `DurableSasCredentialStore` | 3 `SYN-` identities created; 3 durable entries; a restarted store recovered 3 references; teardown receipt zero residual; independent hub count 0 |
| Debug log of that run (10,819 bytes) | 0 key-shaped, `SharedAccess`, `sig=`, bearer or JWT matches; no stored value in the log |
| Key Vault backend | Not run live: a new vault in `ama` is forced to public access Disabled, the VM has no private path, and the policy was not bypassed. A dict-backed stand-in with the same client surface was used for that half |
| Cleanup | Hub deleted; vault deleted and purged; no role assignment left; `az iot hub list -g ama` shows only the demo hub |
| `src/core` device and provisioning tests, mypy, ruff (clean venv with `dev` extra) | 103 device tests, 12 live-provisioning tests OK; mypy no issues in 411 files; ruff clean on the changed files |

## Code change

`device_provision --apply --hub-host <host> --vault-url https://<name>.vault.azure.net` now builds the Key Vault-backed durable store (keyless Entra credential, new optional `keyvault` extra, strict URL pattern, fixed-code refusals). The default remains in-memory. Three focused tests cover the option and its refusals. This is a security-sensitive `src/core` change: tier FULL, coordinator gate required; not run here.

## Per-criterion table

| Criterion in #2128 | Result |
| --- | --- |
| Credentials are issued and stored without appearing in source or logs | Issuance and no-leak proven (throwaway hub, live logs, repository search). Durable storage proven in code and tests, and live only through a stand-in backend. Unproven: a real Key Vault write (network policy blocks a throwaway vault; the production vault was not used) |
| Teardown removes all simulated identities | Proven for the registry on a live throwaway hub with a restarted durable store (zero by two reads). Not re-proven on the demo hub (private, unreachable). The live simulator identities are intended residents of the hub, not teardown residue |

## Not proven or owner-gated

* Key Vault live write and revoke; needs an in-network runner or an owner-approved vault with a private path.
* The stored secret is the derived DPS-style key; the adapter discards the Hub-generated key, so whether the stored value authenticates a device is not shown.
* `lp.plan_simulated_provisioning` (`SIM-` ids) cannot drive `AzureIotHubRegistry` (`SYN-` only); separate design work.
* Hosted CI, independent exact-head review and the full local gate remain with the coordinator.

The issue stays open; nothing is ticked by this note.
