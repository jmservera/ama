<!-- markdownlint-disable-file -->
# Phase details: secret-name-redeploy-358-2236

## Phase 1 (infra/README.md)

* Target: the paragraph ending "Retain the resulting Key Vault secret reference on subsequent Bicep redeploys." (line ~717, `Refs #360` section).
* Replace that sentence with: "Retain the resulting Key Vault secret reference on subsequent Bicep redeploys by passing `entraClientSecretName` equal to the `zava-forward-credential-name` tag that a successful setup recorded on the API app (read the name from the tag, never a value); the default `entra-client-secret` would replace the generated name. This preserves the secret name, not proof of sign-in."
* ASCII punctuation, no new heading, no em dash.

## Phase 2 (log)

* Append at end of `docs/reference/log.md`, format `## [2026-11-12] update | ... (Refs #358)`, `*` bullets: change, evidence class (source-derived, no live run), prior NOT_READY and 278-test/1-error preserved, no closure/tick, evidence path.

## Phase 3 (validation)

* `git diff --stat` shows only intended files; `git diff --check`.
* From `infra/tests`: `python3 -m unittest test_setup_entra` and `python3 -m unittest test_bicep_policy.BicepPolicyTests.test_bearer_only_keeps_validation_and_omits_browser_secret`; raw output to the external session files directory. Docs-only: no local gate.

## Phase 4

* `git config --local user.email` already `8036360+jmservera@users.noreply.github.com`; commit `docs(infra): name entraClientSecretName for Bicep redeploys (Refs #358)` with the Copilot trailer. Record head/tree.
