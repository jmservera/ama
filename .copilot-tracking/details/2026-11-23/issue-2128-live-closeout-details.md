# Issue 2128 details (2026-11-23)

## Phase 3

* `hub_adapters(manifest, hostname, vault_url=None)`: with `vault_url`, validate `https://<name>.vault.azure.net` (regex), lazily import `azure.keyvault.secrets.SecretClient`, use `DefaultAzureCredential`, return `lp.DurableSasCredentialStore(lp.KeyVaultSecretBackend(client))`. Failures raise `ProvisionError("ADAPTER_UNAVAILABLE")` or `INVALID_VAULT_URL`, no detail.
* CLI `--vault-url` only valid with `--apply --hub-host`; otherwise refuse `VAULT_REQUIRES_HUB`.
* Docstring updated. Credentials report text unchanged except durable note when a vault is used: add `credentials_store` key `key-vault` or `in-memory`.

## Phase 4 tests

* vault option builds durable store (stub SecretClient via injected factory) and cycle leaves vault empty with no key in the report.
* invalid vault URL refused without detail; `--vault-url` without `--hub-host` refused.
