<!-- markdownlint-disable-file -->
# Task Research: issue137-pilot-capability

## Research Brief

2026-10-18; RPI parent; Complete. Focused audit preparing planning for
issue #137, not deployment approval. Determine exact template requirements,
verify the owner's region/ownership comment, and collect current management-plane
capability/quota evidence. Audience: delivery coordinator and human reviewer.
Output: dated sanitized evidence in the existing infrastructure environment section.
Non-goals: runtime/template changes, cloud changes, data-plane access and issue closure.

## Research Parameters

* Resolved evidence root: `.copilot-tracking/research/2026-10-18/`.
* Initial internal areas: infra README, main and module Bicep, environment
  parameter examples, ADR 0002, reference index/memory and case specification.
* External areas: live GitHub owner comment and signed-in Azure management GETs.
* Focused posture follows the caller's bounded scope; at most two distinct
  read-only approaches per unavailable surface, individually timed out.
* No private .env, stock, support, ZF_DATA, data planes, identities inventory,
  secrets or resource identifiers may enter committed evidence.

## Extension Registry and Provenance

* Repository copilot instructions selected for documentation and branch rules.
* rpi-research selected; later phases are parent-owned explicit caller requests.
* Research specialists skipped: tightly coupled source/query trace is inline.
* No interaction needed: caller explicitly requests the complete ordered loop.

## Direction Controls

The user authorizes the full ordered loop, one independent plan critique and one
original Review, local documentation/artifact writes, commit, branch push and
draft PR only. Cloud authorization is read-only management-plane evidence.
Initial branch/base verified clean at `612cbed78a35a4ab426571aa7d2aeb0ae6d691dd`;
no existing PR. Preserve adverse receipts and all original phase artifacts.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | What does current source request, and what did the owner actually decide? | Answered C1-C4, W1 |
| Q2 | Which capabilities and scoped quota metrics are returned for uksouth? | Answered with explicit unknowns R1-R17 |
| Q3 | What evidence cannot establish deployability or authority? | Answered; no admission, reservation, approval or complete quota evidence |

## Prior Knowledge Gate

Original case, addendum introduction, reference index and memory read.
The supplied issue body matches live issue's four ticked criteria and single
unticked region/quota criterion. Memory is context, not approval.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Opening source inventory and live-comment verification underway. Source details
and scoped provider surfaces must precede queries.

Reflection: current comment W1 contradicts the README's unsupported 2026-10-16
supersession claim. The example also repeats the stale undecided premise, but
the caller explicitly forbids parameter-example edits: explain that contradiction
in the README instead of changing the example. SQL region is separately unselected.

#### Wave 2: Deeper

Inspected main, pilot example and six exact service modules before live queries.
Read provider catalog/capability and subscription regional usage surfaces through
Azure CLI 2.91.0. Current default account state Enabled; identifiers used only
locally and not published. No proof binds that account to an approved pilot
subscription. Each remote query had a 55-second subprocess timeout and disabled
dynamic extension installation; raw stdout/stderr are private session scratch.
All query outcomes are preserved in the sanitized receipt below.

Reflection: SQL catalog reports exact 2-vCore serverless and zone support, while
Container Apps returns subscription counts but no environment consumption-core
metric. Model catalogs contain exact AIServices models, but usage is empty.

#### Wave 3: Contrarian

Tested apparent catalog success against actual missing quota/zone evidence:
Microsoft.App location GET denied; no zone mapping in provider metadata.
IoT usage failed Bad Gateway with both API versions; IoT/ACR SKU collections
empty despite regional provider listings. Model and SQL usage remain empty on
second GET approaches. StorageV2 must be filtered by kind as well as SKU.
Model `maxCapacity=3` differs from SKU capacity maximum 1000000; no semantic/unit
equivalence is assumed. Duplicate fine-tuning GlobalStandard entries are
excluded using usageName, rather than selecting the first SKU by name.

Reflection: reject "catalog available means deployable"; accept scoped support
facts, defer unavailable quota and ambiguous capacity semantics to human review.

#### Parent Synthesis and Disposition

* Accepted C1-C4/W1/R1-R17 for documentation-only planning.
* Rejected fabricated region/ownership supersession, zero-quota inference,
  summing separate model families, and reference strings as human approval.
* Deferred all missing quotas/zone facts and live operational acceptance.
* Re-entry: no; two distinct missing-surface approaches exhausted where
  meaningful, and remaining gaps must be recorded rather than probed repeatedly.

## Evidence Log

| ID | Finding | Location / source | Retrieval |
| --- | --- | --- | --- |
| W1 | Owner selected pilot uksouth and subscription owner @jmservera only | https://github.com/jmservera/ama/issues/137#issuecomment-6192754703 | 2026-10-18; original 2026-10-15 |
| W2 | Issue remains open; region/quota criterion unticked | https://github.com/jmservera/ama/issues/137 | 2026-10-18 |
| C1 | Region, SQL region, IoT and model deployment inputs; reference guards | infra/main.bicep:10-18,30-35,112-139,168-170 | Base 612cbed78a35a4ab426571aa7d2aeb0ae6d691dd |
| C2 | Empty pilot locations/references and stale undecided comment; source must remain untouched | infra/main.pilot.example.bicepparam:1-14 | Same base |
| C3 | Exact provider configurations | infra/modules/containerapps.bicep:56-74; infra/modules/sql.bicep:17-58; infra/modules/iothub.bicep:9-41; infra/modules/foundry.bicep:16-68 | Same base |
| C4 | Unsupported supersession and outdated implementation status | infra/README.md: Environments; docs/adrs/0002-pilot-readiness-architecture.md: Implementation status | Same base |

## Sanitized Query Receipts (2026-10-18)

All queries use the same current signed-in default subscription, not a proven
authorized pilot subscription. `S` below means
`https://management.azure.com/subscriptions/<subscription-id>`.
REST command shape: `az rest --method get --url "S/<path>?api-version=<version>"`
with `--only-show-errors -o json`; CLI commands also use those output flags.
All remote calls bounded to 55 seconds. No tokens or account inventory published.
Pass means only the explicitly described catalog fact.

| ID | Exact GET/list command shape (S is the placeholder above) | Exit | Inspected sanitized result | Classification / limitation |
| --- | --- | --- | --- | --- |
| R1 | `az provider show -n Microsoft.App` | 0 | managedEnvironments lists UK South; no UK South zoneMappings | Pass regional listing; Unknown zone support |
| R2 | `az containerapp list-usages --location uksouth --subscription <subscription-id>` | 0 | `ManagedEnvironmentCount`: currentValue=2, usage=2, limit=50; no unit field. Other returned metrics: SubscriptionDedicatedNCA100Gpus 0/0; SessionPools 0/50; ExpressEnvironmentCount 0/500; SandboxCores 0/20000 | Subscription/uksouth scope. No managed-environment Consumption-core metric returned; sandbox/GPU/count metrics are not that quota |
| R3 | `S/providers/Microsoft.App/locations/uksouth?api-version=2025-07-01` | 1 | AuthorizationFailed | Blocked location details; no access changes attempted |
| R4 | `S/providers/Microsoft.Sql/locations/uksouth/capabilities?api-version=2023-08-01` | 0 | Region status Available; server 12.0 / GeneralPurpose / GP_S_Gen5_2 status Available, computeModel Serverless, SKU GP_S_Gen5 capacity 2, performanceLevel 2 VCores, zoneRedundant true, supportedZones [], zonePinning false; minCapacity 0.5 Default; autoPause default 60 Minutes | Pass exact catalog SKU/zone flag in candidate uksouth, not SQL-region selection or server admission |
| R5 | `S/providers/Microsoft.Sql/locations/uksouth/usages?api-version=2023-08-01` | 0 | value=[] | Unknown quota, not zero |
| R6 | `S/providers/Microsoft.Devices/skus?api-version=2023-06-30` | 0 | value=[] | Unknown B1 one-unit SKU support/limits |
| R7 | `S/providers/Microsoft.Devices/locations/uksouth/usages?api-version=2023-06-30` | 1 | Bad Gateway | Blocked usage; sanitized error label only |
| R8 | `az cognitiveservices model list --location uksouth --subscription <subscription-id>` | 0 | AIServices S0 / OpenAI format: gpt-4.1-mini and gpt-4.1, version 2025-04-14, lifecycle Legacy; each GlobalStandard inference SKU maximum 1000000, default 10, minimum/step null; model-level maxCapacity 3; rateLimits count 1 and 1000, each renewalPeriod 60, rules null | Pass exact catalog entries only. Requested capacity 30 per deployment; conflicting/undefined capacity semantics prevent overall capacity Pass |
| R9 | `az cognitiveservices usage list --location uksouth --subscription <subscription-id>` | 0 | [] | Unknown quota/current usage. Catalog usageName OpenAI.GlobalStandard.gpt4.1-mini and OpenAI.GlobalStandard.gpt4.1 have no matching usage row/unit |
| R10 | `az storage sku list --subscription <subscription-id>` | 0 | StorageV2 Standard_LRS and Standard_ZRS list uksouth, restrictions=[] | Pass exact regional SKU listing; not storage quota or selection of redundancy |
| R11 | `S/providers/Microsoft.ContainerRegistry/skus?api-version=2025-04-01` | 0 | value=[] | Unknown Premium-specific SKU/zone/quota support |
| R12 | `S/providers/Microsoft.App/locations/uksouth/availableManagedEnvironmentsWorkloadProfileTypes?api-version=2025-07-01` | 0 | Consumption category, cores=4, memoryGiB=8 | Pass profile listing only; cores field describes profile, not environment quota or available new cores |
| R13 | `az provider show -n Microsoft.Devices` | 0 | IotHubs lists UK South; no UK South zoneMappings | Pass regional resource-type listing only, not B1/one-unit capability |
| R14 | `S/providers/Microsoft.Devices/locations/uksouth/usages?api-version=2021-07-02` | 1 | Bad Gateway | Blocked; second/final usage approach |
| R15 | `S/providers/Microsoft.CognitiveServices/locations/uksouth/usages?api-version=2025-06-01` | 0 | value=[] | Unknown; second/final usage approach |
| R16 | `S/providers/Microsoft.Sql/locations/uksouth/usages?api-version=2021-11-01` | 0 | value=[] | Unknown; second/final usage approach |
| R17 | `az provider show -n Microsoft.ContainerRegistry` | 0 | registries lists UK South; no UK South zoneMappings | Pass regional resource-type listing only |

No environment selected or enumerated to obtain per-environment quota.
No quotas' units were inferred from metric names. No existing deployments
were queried or treated as spare capacity. No zero/default substitutions.
No other service's capability or quota is asserted: Key Vault, networking,
identity, monitoring and optional edge remain unverified by this receipt.

## Findings, Decisions and Residual Risks

Q1: W1 selects only pilot region and subscription owner. It does not select SQL
region, subscription/account binding, sizing, redundancy, costs, networking or
credential ownership. Reconcile prose; keep every example byte unchanged.
Q2: R1/R4/R8/R10/R12/R13/R17 provide bounded support evidence, not complete
quota checks. R2 is not environment-core capacity. R3/R7/R14 are adverse.
Q3: catalog support, existing usage and per-deployment capacity are distinct
from available subscription quota, admission, reservations and human authority.
Human reviewer remains unassigned; do not create reviewed-reference tokens.

## Planning Readiness

Ready for documentation-only plan, with recorded unknowns, not deployment.
Research disposition: executed; all three waves completed inline in order.
Artifact self-check: evidence IDs, scoped commands, adverse receipts, caller
boundaries and deferred authority preserved. Parent continuation: Plan.

## Preserved-task reproduction (2026-10-19)

This is P02 implementation validation of the existing research, not a repeated
Research phase. Original 2026-10-18 receipts and critique remain unchanged.
All seventeen identical command shapes above reran at 06:43 UTC on 2026-10-19,
each bounded to 55 seconds with dynamic installation disabled; account binding
GET was bounded to 20 seconds. Raw stdout/stderr remain in separate private
session scratch. Private comparison confirmed the same default subscription
as the original receipts and account state Enabled, not approved pilot binding.
No additional missing-surface approach, cloud write or resource enumeration.

The live owner comment W1 was reverified unchanged. The live issue remains
OPEN with the four original ticks and only region/quota unticked. The later
2026-10-16 delivery comment says region/ownership remain open, contradicting
W1 without a replacement owner decision. Preserve that contradiction; correct
current prose without silently rewriting historical evidence. C4's historical
ADR table is not contradicted at its original date, as PC-002 established.

| Query | Reproduction exit | Comparison against original allowlisted fields/category |
| --- | --- | --- |
| R1 | 0 | Same UK South managedEnvironments listing and absent UK South zone mappings |
| R2 | 0 | Same five metric names/currentValue/usage/limit values; all units absent |
| R3 | 1 | Same AuthorizationFailed; no access change attempted |
| R4 | 0 | Same exact server/edition/SKU/status/compute/zone/performance/default minimum and auto-pause fields |
| R5 | 0 | Same empty value collection; quota unknown |
| R6 | 0 | Same empty value collection; exact B1 support unknown |
| R7 | 1 | Same Bad Gateway; retained original and reproduction failures |
| R8 | 0 | Same two AIServices/S0/OpenAI exact versions, lifecycle, inference usageNames, capacity and rate-limit fields |
| R9 | 0 | Same empty collection; no model-family use/limit/unit |
| R10 | 0 | Same StorageV2 LRS/ZRS uksouth listing and no restrictions |
| R11 | 0 | Same empty value collection; Premium-specific support unknown |
| R12 | 0 | Same Consumption profile category/4 cores/8 GiB, not quota |
| R13 | 0 | Same UK South IotHubs listing and absent UK South zone mappings |
| R14 | 1 | Same Bad Gateway; second approach, no third attempted |
| R15 | 0 | Same empty value collection; no third approach |
| R16 | 0 | Same empty value collection; no third approach |
| R17 | 0 | Same UK South registries listing and absent UK South zone mappings |

Comparison inspected explicit public fields, not whole-response equality.
All model selection additionally filters kind AIServices, account SKU S0,
format OpenAI and inference usageName (excluding fine-tuning). No unit
conversion, cross-family sum, admission or complete-quota conclusion follows.

### Configuration-byte binding across original and approved main

Every file below was compared byte-for-byte with both
612cbed78a35a4ab426571aa7d2aeb0ae6d691dd and
fa659cfd021100f7c64f8ec73bbff76c03adf234 using `git show <base>:<path>`.
Every comparison passed. These hashes describe unchanged source, not historical
execution on the later base or a completed pilot parameter set.

| Source | SHA-256 at both bases and reproduction checkout |
| --- | --- |
| infra/main.bicep | daea1e37adc95f704fba7673883e0b4b6c7b65ab00179b59d8473654ab71f42a |
| infra/main.pilot.example.bicepparam | 0f56ffda3adb95d13ff2b37b77b78411330fbdd0ac01df3384a6d48018431427 |
| infra/modules/containerapps.bicep | 844eceb68671bec4e449501cc9af045a2095d179af30f342aac68d0f19cf8518 |
| infra/modules/sql.bicep | 8081d31f9242d2b2297a35ed43a81ae6cf5937574415b1f80cd14c5b08a32da6 |
| infra/modules/iothub.bicep | 62daa94d236b453fa3c20e84eab95f6ce1dc4fb035cd9e22ee3023aa01fc1ff0 |
| infra/modules/foundry.bicep | 85ee423ab6383c0e8988ee665d97a2a9bf7532d3f2f277a42b95380b04bb1e2e |
| infra/modules/storage.bicep | f48df7a6f36614a875cda308859b19f5eb5867da81531be60e5bb96470483b3e |
| infra/modules/registry.bicep | a5dcd4ec8a9f756017b78109f5986234ff32aeb24b0e9f184efc36abe61513ec |

### Superseding delivery instruction

On 2026-10-19 the owner required the canonical full local gate even for
documentation and prohibited push/PR until independent coordinator review of
exact-head source/RPI/primary evidence and the final matrix receipt. Original
research/critique mentions of docs-only test exemption and draft PR permission
are historical, not current authorization. All cloud/privacy/approval limits
and original critique dispositions continue unchanged.
