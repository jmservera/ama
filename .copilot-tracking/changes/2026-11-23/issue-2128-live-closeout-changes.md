# Issue 2128 changes (2026-11-23)

Status: complete. Tier: FULL (src/core changed); this worker did not run `rpi-checks.py --all` and the coordinator must run the gate. Focused checks run: `src/core` device and provisioning tests (103 + 12 OK), mypy 411 files clean and ruff clean in a clean `dev`-extra venv.

## Source changes

* `src/core/src/zava_forward/core/synthetic/device_provision.py`: `hub_adapters(manifest, host, vault_url=None)` builds `DurableSasCredentialStore(KeyVaultSecretBackend(SecretClient))` when a validated `https://<name>.vault.azure.net` URL is given; CLI `--vault-url` (needs `--apply --hub-host`); fixed-code refusals `INVALID_VAULT_URL`, `VAULT_REQUIRES_HUB`, `ADAPTER_UNAVAILABLE`, `CREDENTIAL_BACKEND_FAILED`.
* `src/core/pyproject.toml`: optional `keyvault` extra (`azure-keyvault-secrets==4.12.0`).
* `src/core/tests/test_device_provision.py`: three tests.
* `src/core/README.md`: adapter section updated (stale "command line does not use it" removed).
* Docs: `docs/reference/research/issue-2128-live-credential-storage-2026-11-23.md`, index, log.

## Live actions (resource group `ama`)

Created and deleted: F1 hub `iot-thr2128-258`, Key Vault `kv-thr2128-258` (purged), two role assignments on them (removed with the resources). No demo resource changed. Evidence: `.copilot-tracking/evidence/2026-11-23/issue-2128-live/` (driver, run output, post-teardown count, log scans).

## Per-criterion table

| Criterion | Proven | Unproven or owner-gated |
| --- | --- | --- |
| Credentials issued and stored without appearing in source or logs | Issuance and no-leak: 1,113,253 live log lines (24 h) and a 10,819-byte debug log with 0 hits; repository search clean; durable store wiring via tests and stand-in backend run on a live hub | Real Key Vault write and revoke (vault network policy blocks a throwaway; production vault not used); stored value is the derived key, not the Hub key |
| Teardown removes all simulated identities | Live throwaway hub: restarted durable store, receipt zero residual, independent count 0 | Demo hub private and unreachable; 288 live simulator identities are intentional and untouched |
