<!-- markdownlint-disable-file -->
# Plan: name the Bicep secret parameter for redeploys (Refs #358, 2026-11-12)

* Task ID `secret-name-redeploy-358-2236`; branch `research/demo-secret-rebuild-readiness-358-2220`, base `eac1206c6`.
* Research: .copilot-tracking/research/2026-11-12/secret-name-redeploy-358-2236-research.md (disposition `executed`, Planning Readiness `Ready`).
* Details: .copilot-tracking/details/2026-11-12/secret-name-redeploy-358-2236-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-11-12/secret-name-redeploy-358-2236-plan-critique.md (one independent critique, final candidate).

## User decisions

* Docs-only initial slice admitted by the owner; one concise existing-README instruction plus directly required log; no source, credential, Graph, Key Vault, deployment or cloud action; no closure, AC tick, push or PR.
* Preserve prior research-only `NOT_READY` and the 278-test run with one missing-distribution error (not a pass).

## Phases

* [ ] Phase 1: edit `infra/README.md` paragraph at line ~717 with one sentence naming `entraClientSecretName` and the `zava-forward-credential-name` tag.
* [ ] Phase 2: append a `docs/reference/log.md` entry (no earlier entry rewritten); no index change.
* [ ] Phase 3: validate by diff and link/anchor review, plus source inspection of the tag/parameter wiring (no existing test pins the tag expression) and the focused existing checks that pin the parameter (`test_bicep_policy` bearer-only test) and the setup tag writes (`test_setup_entra`); record raw output externally.
* [ ] Phase 4: commit locally with the noreply identity and Copilot trailer; freeze head/tree; independent Review once.

## Acceptance

* The sentence states: pass `entraClientSecretName` equal to the API app's `zava-forward-credential-name` tag value on later Bicep deployments; read the name from the tag, never a value; a default redeploy reverts to `entra-client-secret`.
* Diff touches only `infra/README.md` (about 3 lines), `docs/reference/log.md` and original `.copilot-tracking` artifacts.
* The sentence preserves the secret name, not necessarily the exact reference; the tag is read after a successful setup.
* No claim of live verification, sign-in or acceptance.
