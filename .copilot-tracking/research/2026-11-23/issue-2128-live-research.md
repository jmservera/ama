# Issue 2128 research (2026-11-23)

Task: compare the two unticked criteria of #2128 with main (dbf4e45fa7) and live revisions. Disposition: Research executed. Planning Readiness: Ready.

## Evidence (recorded under `.copilot-tracking/evidence/2026-11-23/issue-2128-live/`)

* Prior notes (#185 r4 to r6, 2026-11-19 live) left "storage" unproven because the repository had only an in-memory store. Main now has `DurableSasCredentialStore` and `KeyVaultSecretBackend` (`live_provisioning.py`, #2159) with unit tests in `test_durable_credential_store.py`.
* Gap 1 (code): `device_provision.hub_adapters` still builds the in-memory `SymmetricSasCredentialStore`, so no CLI path stores credentials durably and a separate `--action teardown` process cannot revoke earlier references.
* Gap 2 (tooling, not changed): `lp.plan_simulated_provisioning` yields `SIM-` ids that `AzureIotHubRegistry` refuses (`SYN-` only); the `device_identity` path (`SYN-`) is the one that works with the hub adapter.
* Live demo hub `iot-cutover-test-rzsrg`: B1, public access Disabled, local auth off; 288 enabled devices belong to the live simulator (#184, X.509, `SYN-` ids, secrets mounted as a Container Apps Secret volume, 577 job secrets). They are intentionally live, not #185 residue, and were not deleted.
* Log scan, Log Analytics workspace `log-cutover-test`, last 24 h of `ContainerAppConsoleLogs`: 1,113,253 lines (1,105,302 from the simulator); 0 hits for PRIVATE KEY, BEGIN CERTIFICATE, SharedAccessSignature, primaryKey, SharedAccessKey, `sig=`.
* Throwaway run (F1 hub `iot-thr2128-258`): current main `device_identity.provision` and `teardown` with the real adapter and `DurableSasCredentialStore`: 3 identities, 3 stored secrets, restart recovered 3 references, teardown zero residual, independent hub count 0, debug log 10,819 bytes with 0 key matches. Key Vault itself could not be exercised: a new vault in `ama` is forced to public access Disabled (policy) and the VM is not on a private path; the policy was not bypassed. A dict-backed stand-in with the same client surface was used and is labelled so. Throwaway hub and vault deleted, vault purged, no role assignments remain.

## Decision

Implement a small FULL-tier change: `hub_adapters` and the CLI accept an optional `--vault-url`, building `DurableSasCredentialStore(KeyVaultSecretBackend(SecretClient(...)))` with keyless Entra credentials; the default stays in-memory. Add focused tests. Key Vault live proof stays unproven; the stored secret is the derived DPS-style key, not the Hub-generated key (the adapter discards that), stated as a limit.
