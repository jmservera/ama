# Research: issue 2061 single external demo environment (2026-11-19)

Task issue-2061-live. Research disposition: executed. Planning Readiness: Ready (criterion 1 only).

## Live read-only inventory (resource group ama, Azure CLI existing login, no secrets)

| Environment | Internal | Apps and jobs |
| --- | --- | --- |
| cae-cutover-test | true | ca-cutover-test-api (external ingress true), ca-cutover-test-agents (no ingress), 8 jobs (init, verify, ledger-verify, import, orchestrator, smoke, mi-http, public-audit) |
| cae-cutover-test-demo | false | ca-cutover-test-demo-api (external true), ca-resident-demo (external true) |

Identities: id-cutover-test-{api,agents,import,init,orchestrator} and id-resident-demo.
ca-resident-demo uses only id-resident-demo; ca-cutover-test-demo-api uses id-cutover-test-api.

Role inventory (principal -> scope, redacted subscription):

* id-cutover-test-api: Storage Blob Data Contributor and Storage Queue Data Message Sender on stcutovertestrzsrg; Key Vault Secrets User on kv-cutovertest-rzsrg (vault scope); AcrPull on crcutovertestrzsrg; Cognitive Services OpenAI User on aif-cutover-test-rzsrg.
* id-resident-demo: AcrPull on the registry; Key Vault Secrets User only on secrets resident-demo-password-verifier and resident-demo-session-key; Cognitive Services OpenAI User on aoai-resident-469.

Finding: the public resident app already has a least-privilege identity separate from the API identity. The public demo API still shares id-cutover-test-api with the private estate, which carries vault-wide Key Vault read, so a public/internal identity split for the demo API is not yet done.

## Repository findings

* infra/modules/containerapps.bicep line 83: `externalEnvironment = demoDirectIngress || allowPublicNetworkAccess`; the demo profile already builds an external environment with a direct-ingress API (infra/main.bicep `demoDirectIngress`). The remaining two-environment shape is a deployment history, not a missing module.
* Entra app registrations: `az ad app list` returned "Insufficient privileges", so redirect URIs cannot be listed with this login.

## Per-criterion proof status

See the changes record for the table. Only criterion 1 (decision record) is buildable without production-shaped Entra changes, owner approval of a delete list, a FULL-tier what-if and gate, or a live redeploy.
