---
title: Issue 2061 single external demo environment, live read-only inventory (2026-11-19)
description: Read-only inventory of environments, apps, identities and roles in resource group ama, with per-criterion status for issue 2061
ms.date: 2026-11-19
---

Refs #2061. Demo only. No Azure resource or Entra object was created, changed or deleted; no credential was read. The decision record is [ADR 0008](../../adrs/0008-single-external-demo-environment.md). Per-criterion status is in the changes record `.copilot-tracking/changes/2026-11-19/issue-2061-live-changes.md`: only criterion 1 is built (Proposed); criteria 2 to 8 are unproven for the reasons recorded there.
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

