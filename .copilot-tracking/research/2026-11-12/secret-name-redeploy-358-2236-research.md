<!-- markdownlint-disable-file -->
# Research: name the Bicep secret parameter for redeploys (Refs #358, 2026-11-12)

* Task ID `secret-name-redeploy-358-2236`; branch `research/demo-secret-rebuild-readiness-358-2220` at `eac1206c6ca08bd551e3d0d2384bb87a1f05c24f` (tree `ff26901294f2678afc877d68457cbb1db2ef49e4`), clean at start.
* Disposition: `executed` (prospective; started after the owner admitted the docs-only slice). Planning Readiness: `Ready`.
* Prior readiness result (preserved, not rewritten): research-only `NOT_READY`; external result `rpi-358-readiness-2220-result.json`. Its tests: 278 ran, 1 error (`test_ledger_alert_queries_match_the_verifier_markers`, `ModuleNotFoundError: zava_forward.orchestrator`, distribution not pip-installed). That run is not a pass.

## Question

`infra/README.md` says to "Retain the resulting Key Vault secret reference on subsequent Bicep redeploys" but names no mechanism. What exactly is that mechanism, and who is the authority for it?

## Actual source reconciliation

* `infra/main.bicep:54` declares `param entraClientSecretName string = 'entra-client-secret'` and passes it at line 412 to `modules/containerapps.bicep:21` (same default).
* `modules/containerapps.bicep:143` sets the API tag `zava-forward-credential-name: entraClientSecretName`; line 161-162 renders `secrets` entry `{name: entraClientSecretName, keyVaultUrl: '<vault>/secrets/<entraClientSecretName>', identity}` (unless bearer-only); line 283 sets auth `clientSecretSettingName` to the same parameter.
* `infra/scripts/setup-entra.py` `secret_reference` (1469-1597) creates the generated name `entra-<client id without dashes>-<12 hex>`, stores the Key Vault secret under that name, PATCHes `secrets` plus the tag `zava-forward-credential-name` to that name. `record_credential_store` (1599-1609) also writes the tag when it adopts an existing matching credential.
* Therefore after setup the tag `zava-forward-credential-name` on the API Container App is the single recorded name of the live credential. The authority for the value is setup (owner of the tag after Bicep); the authority for what Bicep renders is the parameter.
* A Bicep redeploy with the default parameter renders the secret, tag and `clientSecretSettingName` as `entra-client-secret`, replacing the generated entry/tag (source-derived: the template renders these three values from the parameter; the deployment effect itself is unverified). Result: setup would again report browser credential drift, or the generated name would be dropped.
* Parameter acceptance: `src/orchestrator/.../rebuild_azure.py` allows an `entraClientSecretName=[a-z][a-z0-9-]{0,126}` assignment; generated names fit that pattern (lowercase hex and dashes, `entra-` prefix). `infra/tests/test_bicep_policy.py::test_bearer_only_keeps_validation_and_omits_browser_secret` pins the parameter wiring; `test_rebuild_azure.py::test_custom_secret_name_is_the_checked_credential` pins the orchestrator reading a custom name.
* Existing documentation gap: `infra/README.md` line 717 only. `infra/README.md` ~3781 says provision `entra-client-secret` for a first rebuild, which is a different (fresh vault) situation and stays.

## Boundaries and unknowns

* Unobserved: no live redeploy was run; no Graph, Key Vault, deployment or credential call. The claim is source-derived only.
* Reference form: Bicep renders a versionless vault URL; setup's stored reference may be versioned (local CLI path returns the vault id) or versionless (ARM handoff). The parameter preserves the secret name, not necessarily the exact stored reference. The tag is trustworthy only after a successful setup and can be stale or overwritten. No claim is made that a live redeploy preserves sign-in.
* Not claimed: whole-demo acceptance, round-trip of `secret_reference`, closure or AC tick for #358.

## Selected approach

One concise sentence in `infra/README.md` line 717 paragraph: pass `entraClientSecretName=<value of the app's zava-forward-credential-name tag>` on later Bicep deployments, read from the tag, never a secret value. Plus an append-only `docs/reference/log.md` entry. No index entry: no knowledge-base file is added, moved or retired; the README is an infra how-to already linked from the index.

## Alternatives rejected

* Change `setup-entra.py` to match `entra-client-secret`: weakens the credential-expiry guard; source changes are out of scope.
* New section or evidence-pack entry: duplicates existing preservation evidence.
