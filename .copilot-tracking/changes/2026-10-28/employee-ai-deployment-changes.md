---
title: Employee AI deployment changes and execution evidence
description: Source configuration, local validation and exact bounded Azure operations
ms.date: 2026-10-28
---

## Context and Scope

Task ID: employee-ai-deployment-2026-10-28. Automatic full-loop execution.
Plan: .copilot-tracking/plans/2026-10-28/employee-ai-deployment-plan.md.
Details: .copilot-tracking/details/2026-10-28/employee-ai-deployment-phase-details.md.
Research: .copilot-tracking/research/2026-10-28/employee-ai-deployment-research.md.
Original critique: .copilot-tracking/reviews/plans/2026-10-28/employee-ai-deployment-plan-critique.md.

Implementation scope is P01/P02 and P03 handoff/publication. No source app edits,
live app writes, inference, keys/secrets/.env/private datasets, resident
resources, other role assignments or deletions are authorized.

## P01: Initial State and Dependency Setup

Clean pre-created branch feat/employee-ai-deployment-bicep had no PR. Fetched
main and fast-forwarded e39166da to d783b63acb0e2e59ad52f1c8f999e093c149297b;
no existing commit rewritten. #514 remains an independent open PR, not source
ancestry; live coordinator redeploy follows its merge.

`python3 -m pip show zava-forward-core zava-forward-agents zava-forward-api
zava-forward-orchestrator ruff mypy PyYAML` reported the namespace distributions,
Ruff and mypy missing. After that failure, created external venv
`/tmp/ama-employee-ai-20261028-venv` and installed existing distributions with
pip `--no-deps -e src/core -e src/agents -e src/api -e src/orchestrator`,
hashed `src/api/requirements.txt`, PyYAML 6.0.3, Ruff 0.17.1 and mypy 2.4.0.
Install succeeded. No dependency manifest changed, no uv or PYTHONPATH hack.

## P01: Source Changes

Completed P01-T01/P01-T02: main has scalar model/version/SKU/capacity inputs,
one capacity-one default and retained nonempty array override. Foundry outputs
OpenAI-specific endpoint, deployment names and response-model version pins.
Containerapps forwards those five settings only when API AI is explicitly
enabled, retaining selected identity. Generic Foundry endpoint remains intact.
README replaces incompatible empty-model bootstrap and documents cost,
multi-tier, version, no-live-app-change and coordinator boundaries.

Four new compiled semantic test methods in existing policy file, no removals.
They evaluate defaults/scalar overrides through the real resource loop and
module/env chain, custom single/two-tier arrays, constraints, default-off AI,
endpoint distinction, selected identity, model pins and two targeted mutations.

Validation:

* `az bicep build --file infra/main.bicep --stdout`: passed, Bicep 0.48.1.
* Every `infra/*.bicep` and `infra/modules/*.bicep` compiled; all three
  `infra/*.bicepparam` build-params passed.
* `REQUIRE_AZ_BICEP=1 .../python -m unittest discover -s infra/tests -q`:
  466 tests, 116.326s, OK, no skips. External log:
  `/tmp/ama-employee-ai-infra-tests-20261028.log`.
* Changed-file Ruff E/F/I/B/UP and format check passed; mypy
  `--check-untyped-defs` passed; `git diff --check` passed.
* After annotation-only correction, focused `-p test_bicep_policy.py -k employee`
  rerun: 4 tests, 6.825s, OK.

Preserved initial failures: first policy run 54 tests / 4 failures because
the assertion helper's subTest swallowed expected mutation assertions, not a
production failure; removed the inner subTest and full infra run passed.
First mypy run reported eleven callback dictionary inference errors; annotated
the heterogeneous evaluator context `dict[str, Any]`, matching the existing
evaluator contract; mypy and focused tests then passed.

## P02: Azure Commands and Results

Research-only reads used signed-in az servicePrincipal in subscription
e51ebc89-79d0-4a52-a82b-01a292eefd5b. Commands:

```bash
az account show --query '{subscription:id,name:name,userType:user.type}' -o json
az cognitiveservices account show -g ama -n aif-cutover-test-rzsrg \
  --query '{name:name,kind:kind,location:location,endpoint:properties.endpoint,id:id,sku:sku.name}' -o json
az cognitiveservices account deployment list -g ama -n aif-cutover-test-rzsrg \
  --query '[].{name:name,model:properties.model,sku:sku}' -o json
az cognitiveservices account list-models -g ama -n aif-cutover-test-rzsrg \
  --query "[?name=='gpt-4o-mini'].{name:name,version:version,deprecation:deprecation,capabilities:capabilities,skus:skus}" -o json
az cognitiveservices usage list --location uksouth -o json
az role assignment list \
  --scope /subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama/providers/Microsoft.CognitiveServices/accounts/aif-cutover-test-rzsrg \
  --include-inherited \
  --query "[?principalId=='6ac4c6b9-c516-4e24-81a6-f32663a93aab'].{role:roleDefinitionName,scope:scope,principalId:principalId}" -o json
az containerapp show -g ama -n ca-cutover-test-demo-api \
  --query '{name:name,identity:identity,revision:properties.latestRevisionName,environment:properties.template.containers[].env[?name==`AZURE_CLIENT_ID` || name==`AI_ENDPOINT` || name==`AI_DEPLOYMENT` || name==`AI_DEPLOYMENT_STRONG`]}' -o json
```

Results: AIServices/S0, uksouth, private networking, local auth disabled; zero
deployments. Selected model listed with chatCompletion and GlobalStandard;
inference retirement 2027-04-14, unspecified minimum capacity, usage list [].
Employee principal role filter []; existing agent has invocation and Foundry
User roles, untouched. App revision 0000006; attached/selected API user-assigned
identity client 1b1fe44e-f4cf-4aae-98d0-b30c7927a5e3, principal
6ac4c6b9-c516-4e24-81a6-f32663a93aab. Three named AI settings absent.

Preserved failed query: initial `contains(model.name, 'mini')` failed because
the catalogue is flat, not nested; corrected to `contains(name, 'mini')`.
Earlier nested gpt-4o-mini equality filter [] was not unavailability evidence.
No live writes during Research. Fresh pre-write reads revalidated zero models,
UK South/private/keyless account, same API identity/revision and absent role.

### P02-T01: ARM-compatible assignment name

Microsoft's ARM guid documentation, retrieved 2026-10-28:
https://learn.microsoft.com/en-us/azure/azure-resource-manager/templates/template-functions-string#guid
specifies UUID v5, namespace 11fb06fb-712d-4ddd-98c7-e71bbd588830,
hyphen-concatenated string arguments. Local Python uuid5 DNS RFC known answer
`www.widgets.com` -> `21f7f8de-8051-5b89-8680-0195ef798b6a` passed.
Using exact account ID from the account GET, principal
6ac4c6b9-c516-4e24-81a6-f32663a93aab and literal `openai-user` yields
`207df5ea-ca56-5fb7-9ebb-f533d02dadb8`, matching the existing Bicep naming
algorithm rather than a random role-assignment UUID.

### P02-T01: Initial provider rejection and bounded replacement

Exact initial write:

```bash
az rest --method put --uri 'https://management.azure.com/subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama/providers/Microsoft.CognitiveServices/accounts/aif-cutover-test-rzsrg/deployments/standard?api-version=2025-06-01' \
  --body '{"sku":{"name":"GlobalStandard","capacity":1},"properties":{"model":{"format":"OpenAI","name":"gpt-4o-mini","version":"2024-07-18"},"versionUpgradeOption":"NoAutoUpgrade","raiPolicyName":"Microsoft.DefaultV2"}}' \
  --query '{name:name,state:properties.provisioningState,model:properties.model,sku:sku,versionUpgradeOption:properties.versionUpgradeOption,raiPolicyName:properties.raiPolicyName}' -o json
```

Result: HTTP Bad Request / ServiceModelDeprecating: "The model
'Format:OpenAI,Name:gpt-4o-mini,Version:2024-07-18' is in deprecating state and
cannot be used for new deployments." No role write ran (shell `&&`);
subsequent read-only list still [].

Fallback check returned gpt-4.1-nano 2025-04-14, lifecycle Legacy,
chatCompletion=true, GlobalStandard available, inference date 2027-04-14.
Selected this small non-reasoning GPT-4.1 chat model at capacity one rather
than a newer reasoning model that needs different runtime token parameters.
Official model catalogue retrieved 2026-10-28:
https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure#gpt-41-series
and exact account model metadata support the chat-family selection, not live
runtime/evaluation acceptance. No cheapest-ever price assertion is made.
Plan/details/source/tests/handover must reconcile to this replacement before
Review. This is the explicitly planned in-scope fallback, not new authority.

### P02-T01: Successful writes and read-only confirmation

Only the following successful resource writes occurred:

```bash
az rest --method put --uri 'https://management.azure.com/subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama/providers/Microsoft.CognitiveServices/accounts/aif-cutover-test-rzsrg/deployments/standard?api-version=2025-06-01' \
  --body '{"sku":{"name":"GlobalStandard","capacity":1},"properties":{"model":{"format":"OpenAI","name":"gpt-4.1-nano","version":"2025-04-14"},"versionUpgradeOption":"NoAutoUpgrade","raiPolicyName":"Microsoft.DefaultV2"}}' \
  --query '{name:name,state:properties.provisioningState,model:properties.model,sku:sku,versionUpgradeOption:properties.versionUpgradeOption,raiPolicyName:properties.raiPolicyName}' -o json
az role assignment create --subscription e51ebc89-79d0-4a52-a82b-01a292eefd5b \
  --name 207df5ea-ca56-5fb7-9ebb-f533d02dadb8 \
  --assignee-object-id 6ac4c6b9-c516-4e24-81a6-f32663a93aab \
  --assignee-principal-type ServicePrincipal \
  --role 5e0bd9bd-7b93-4f28-af87-19fc36ad61bd \
  --scope /subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama/providers/Microsoft.CognitiveServices/accounts/aif-cutover-test-rzsrg \
  --query '{name:name,principalId:principalId,principalType:principalType,roleDefinitionId:roleDefinitionId,scope:scope}' -o json
```

PUT result: standard, Succeeded, OpenAI/gpt-4.1-nano/2025-04-14,
GlobalStandard/capacity1, NoAutoUpgrade, Microsoft.DefaultV2.
Role result: exact expected UUID, requested principal/ServicePrincipal,
Cognitive Services OpenAI User role ID and exact account scope.
No Foundry User, resident role, subscription role or other assignment created.

Read-only verification:

```bash
az cognitiveservices account deployment list \
  --subscription e51ebc89-79d0-4a52-a82b-01a292eefd5b -g ama -n aif-cutover-test-rzsrg \
  --query '[].{name:name,state:properties.provisioningState,model:properties.model,sku:sku,versionUpgradeOption:properties.versionUpgradeOption,raiPolicyName:properties.raiPolicyName}' -o json
az role assignment list \
  --scope /subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama/providers/Microsoft.CognitiveServices/accounts/aif-cutover-test-rzsrg \
  --include-inherited \
  --query "[?principalId=='6ac4c6b9-c516-4e24-81a6-f32663a93aab'].{name:name,role:roleDefinitionName,principalId:principalId,scope:scope}" -o json
az containerapp show --subscription e51ebc89-79d0-4a52-a82b-01a292eefd5b \
  -g ama -n ca-cutover-test-demo-api \
  --query '{revision:properties.latestRevisionName,identity:identity,settings:properties.template.containers[].env[?starts_with(name,`AI_`) || name==`AZURE_CLIENT_ID`]}' -o json
az cognitiveservices account show -g ama -n aif-cutover-test-rzsrg \
  --query '{localAuthDisabled:properties.disableLocalAuth,publicNetwork:properties.publicNetworkAccess}' -o json
```

Results: list length exactly1, standard Succeeded with the same model,
version/SKU/capacity/upgrade/filter above. Employee role list length1,
name 207df5ea-ca56-5fb7-9ebb-f533d02dadb8, correct account scope/principal
and role name. App revision still ca-cutover-test-demo-api--0000006,
same attached id-cutover-test-api identity and selected client ID, no AI_*
variables. Account still publicNetwork Disabled/localAuthDisabled true.
No containerapp write/redeploy, keys, private data, inference or deletion ran.

## P01/P02: Fallback Reconciliation and Final Validation

Immediately relevant planned fallback, not a new user decision: changed
chatModelName/chatModelVersion defaults and compiled default assertion to
gpt-4.1-nano/2025-04-14. README actual live state and intended settings,
Plan executive summary/requirements/P02 and Details match accepted provider
configuration. Historical Research/critique and the original failures remain.
No additional critique was performed.

Final validation after reconciliation:

* `az bicep build --file infra/main.bicep --stdout`: passed.
* `REQUIRE_AZ_BICEP=1 .../python -m unittest discover -s infra/tests -q`:
  466 tests, 111.776s, OK, no skips. Final external log:
  `/tmp/ama-employee-ai-infra-tests-nano-20261028.log`.
* Changed-file Ruff check/format, mypy and `git diff --check`: passed.
* A subsequent `gh api user --jq '{id:id,login:login}'` identity query had
  invalid jq field syntax; corrected dot-qualified selectors before committing.
  This did not affect source validation or any Azure operation.

## Amendments and Divergences

Critique dispositions are in Plan. PC-001's /tmp prohibition does not exist in
the parent execution context and was rejected, not followed. PC-002..005 were
applied before implementation. This is not a second critique.

## Validation and Review

Local source validation complete. Independent Review execution Complete,
outcome Conformant with justified divergence; no implementation defects.
Original Review: .copilot-tracking/reviews/logs/2026-10-28/employee-ai-deployment-review.md.
Reviewer independently passed four compiled tests and UUID/source-boundary
checks; RV-001 activation and RV-002 lifecycle/cost remain separate follow-ups.
Full --all explicitly forbidden by the supplied owner brief. One
scoped --changed attempt at most with native --lock-timeout 0, after final
candidate commit. Local full-tier, hosted approvals, live inference and human
acceptance are not implied.

## Remaining Work and Handover

P01/P02 and independent Review complete. Evidence commit, scoped gate attempt,
push and Refs-only PR remain. Coordinator owns app configuration/redeploy
after #514, registered release/evaluation, private reachability and bounded
source=ai verification. USD30 additional employee AI authorization through
2026-10-31 is a spending authorization, not a configured hard cap.

## Exact Coordinator Settings (Not Applied)

| Name | Value |
| --- | --- |
| AI_ENDPOINT | https://aif-cutover-test-rzsrg.openai.azure.com/ |
| AI_DEPLOYMENT | standard |
| AI_DEPLOYMENT_STRONG | standard |
| AI_MODEL_VERSION | gpt-4.1-nano-2025-04-14 |
| AI_MODEL_VERSION_STRONG | gpt-4.1-nano-2025-04-14 |
| AZURE_CLIENT_ID (retain) | 1b1fe44e-f4cf-4aae-98d0-b30c7927a5e3 |

Both tiers share the one small model, not an accepted capable-tier evaluation.
Release/evaluation model identity must be reconciled before activation; no
governed approval or inference result is fabricated.

## Pre-Review Reconciliation

P01/P02 and their task markers complete in Plan; Details carries same state.
Changes records actual writes, model fallback and passing final validation.
P03 publication remains intentionally unchecked until Review/commit/gate/PR.
No implementation blocker; residual operator/release/model-quality work is
explicitly outside current live scope. This pre-Review reconciliation snapshot
was followed by the one completed independent Review, not a second assessment.

## P03: Review Boundary and Publication Preparation

Source-review SHA256 (`git diff origin/main -- infra`):
`589cb6072ca2cb33211843f9b140e2f61f6c2505634982a985122b7adb4ccd89`.
Review assessed uncommitted source at HEAD d783b63a against freshly advanced
main 98b0bb98; main had no infra delta. #514 merged at
2026-10-28T08:36:17Z as 98b0bb98f2424dd23c00e386378f44892a7a79e0.
Fast-forwarded the topic to that main before the first implementation commit;
infra patch fingerprint remained identical. No source was changed after
Review; later state/evidence/publication metadata is parent-owned, not a
repeat independent assessment or human approval.

Authenticated GitHub identity: id8036360/login jmservera. Set only local
user.email to `8036360+jmservera@users.noreply.github.com`; retained local
name jmservera; author/committer use the privacy-safe address.

A separate exact-HEAD external worktree will isolate the one gate attempt from
test-generated ignored caches/editable metadata in this working copy; do not
delete historical inputs or claim that ignored inputs pass the runner.
Use runner-native --changed/--lock-timeout0, never --all or an outer lock.

### One Authorized Scoped Gate Attempt: Failed Preflight

Committed implementation/original RPI evidence at
`02b9d0aa5c3daea943fe287f6d176b55f82db6d4`, tree
`eaa3ff7570e479db7e2705bf105353963d81d163`, base
`98b0bb98f2424dd23c00e386378f44892a7a79e0`. Exact command:

```bash
git worktree add --detach /tmp/ama-employee-ai-gate-candidate-20261028 HEAD
cd /tmp/ama-employee-ai-gate-candidate-20261028
python3 tools/rpi-checks.py --changed --jobs 1 --lock-timeout 0 \
  --base 98b0bb98f2424dd23c00e386378f44892a7a79e0 \
  --out /tmp/ama-employee-ai-scoped-gate-20261028
```

Nonblocking native heavy lock acquired at 2026-10-28T08:47:29Z. Selected
only preflight, namespace, static, infra (partial scope). Python3.12.3,
Node24.21.0, Docker29.9.0, Bicep0.48.1, actionlint1.7.12,
ShellCheck0.11.0 and Trivy0.76.0 preflight commands succeeded, then failed:
`preflight: Workflow matrix drift: src-deploy.yml`. This PR does not change
that workflow or runner. No selected groups completed; executed_groups and
groups are empty. This is not a scoped or full-tier success.

Original failed receipt retained externally at
`/tmp/ama-employee-ai-scoped-gate-20261028/receipt.json`; console log at
`/tmp/ama-employee-ai-scoped-gate-20261028.log`. No retry/resume/--all or
cloud fallback. Removed only the task-owned external candidate worktree
with `git worktree remove /tmp/ama-employee-ai-gate-candidate-20261028`;
retained original failed output/evidence. Fresh fetch still resolves main to
98b0bb98; reviewed infra fingerprint unchanged.

Later publication-only evidence/state commits cannot make this failed receipt
valid for a later head. No passing receipt exists, so passing-receipt
verification is inapplicable and no gate acceptance is claimed. The explicitly
requested PR is published with this gate exception and retained hosted/human
approval requirements, not as a merge/release-ready candidate.
