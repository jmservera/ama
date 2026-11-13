<!-- markdownlint-disable-file -->
# Changes: secret-name-redeploy-358-2236 (2026-11-12)

* Plan: .copilot-tracking/plans/2026-11-12/secret-name-redeploy-358-2236-plan.md; no amendments or divergences.
* `infra/README.md` (Direct Entra setup and acceptance): one sentence naming `entraClientSecretName` and the `zava-forward-credential-name` tag.
* `docs/reference/log.md`: appended one entry; no index change (no knowledge-base file added, moved or retired).
* Validation (docs-only, no local gate): `git diff --check` clean; `test_setup_entra` 124 OK; `test_bicep_policy` bearer-only test 1 OK. Raw output: /home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/rpi-358-refill-2236-raw/
* Not run: live redeploy, Graph, Key Vault, cloud, full gate. Prior NOT_READY and 278-tests/one-error (missing distribution) preserved, not a pass.
