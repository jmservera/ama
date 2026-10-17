---
title: Setup API selection research
description: Safe migration discovery for issue 360
ms.date: 2026-10-17
---

## Research Brief and Parameters

Task360 / setup-api-selection-360, full ordered RPI requested. Focused convergence
research: owner laptop --check refuses old+new migration APIs. Determine an
existing explicit authoritative selector; never fuzzy order/suffix selection.
Audience: owner/coordinator/reviewer. Same clean topic/PR385, new artifact set.
Research root .copilot-tracking/research/2026-10-17/. Prior ACR evidence immutable.
Fresh origin/main verified bbbc924, already ancestor; no rebase needed.

## Direction Controls and Extensions

Repository instructions and rpi-research selected; inline continuous discovery
trace, no researcher delegation. New Plan/critique/Implement/independent Review
will follow only after Research Ready. Source scope setup script/tests/runbook.
Read-only ARM metadata only; no actual setup mutation, SQL/Graph/secret payload,
build/image/pin/start/restart/network/IAM/deletion. Explicit --container-app wins,
unknown/multiple valid targets refuse, single/legacy Front Door behavior retained.
No web or regulatory assessment. User has supplied sufficient bounded scope;
if no existing safe selector exists, decision gap must not be invented away.

## Questions and Candidate Areas

Which existing discovery/tag/Bicep/config contract identifies intended direct demo?
Does deployed metadata actually contain it? Why does current helper still refuse?
Can offline --check prove no cloud/private-data writes on success or failure?

## Cycle1

Opening: current code appears to already prefer explicit role+ingress tags.
Verify actual metadata and all selection/read-only branches before conclusions.

Wider: read original/addendum/index/memory and infra guide, discover/choose,
existing stateful setup tests and Bicep tags. Current discovery only considers
direct candidates with new zava-forward-role=api, while generic choose already
supports legacy workload=api. Reflection: investigate deployed legacy tag
combination rather than adding a selector or guessing a suffix.

Deeper: selected read-only ARM API metadata confirms old workload=api/no role/
no ingress tag and replacement workload=api/no role/zava-forward-ingress=direct,
external ingress in existing demo environment. Deployment Succeeded metadata
does not expose requested demoDirectIngress/apiName parameters (null); an initial
keys(null) projection failed and was corrected to bounded fields, no write.
Reflection: explicit deployed ingress plus existing workload compatibility is
the authoritative discriminant already used by this repository.

Contrarian: multiple direct candidates, unrelated ingress-only resources,
conflicting explicit role tags and explicit legacy override must not be masked
by preference. Preserve choose's role-tag precedence: legacy workload accepted
only if modern role absent; contradictory role must not become an API.
No new tag or persistent selector necessary. Existing --check Azure SQL fallback
CAN create temporary job/secret despite no SQL mutation; owner explicitly requires
no cloud writes now. A narrow azure_staff guard for check as well as dry-run
must stop both explicit Azure mode and automatic candidate/check fallback before
payload/transport. Local read-only SQL remains supported; mutation-mode Azure
transport remains unchanged. This is directly coupled safety scope, not inferred
permission to execute setup live.

## Evidence, Decisions and Planning Readiness

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | infra/scripts/setup-entra.py:370-405 | choose recognizes workload fallback but direct preference requires modern role |
| C2 | infra/modules/containerapps.bicep API tags | Modern Bicep explicitly emits direct-ingress selector; deployed older migration retained workload tag |
| C3 | infra/tests/test_setup_entra.py:297-361,467-505 | Existing direct/ambiguity/legacy/read-only contracts, stateful fake |
| C4 | infra/scripts/setup-entra.py:603-630,923-1038 | --check can reach Azure job transport; guard required to honor explicit no-cloud-write request |
| W1 | az containerapp list/show -g ama selected tags/environment/external fields, 2026-10-17 | Actual old+replacement legacy-workload pair, only replacement explicitly direct |
| W2 | az deployment group show demo-stage-360-20261017 selected state/parameter fields, 2026-10-17 | Succeeded, selected parameters null; not usable alternate selector |

Selected recommendation: extend direct tag filter to existing legacy workload API
when modern role absent, never name/order heuristic. Explicit name always wins;
multiple eligible direct targets retain refusal. Fail closed --check Azure staff
transport before any cloud write or roster/Graph payload; document incomplete
private-host handoff rather than pretend verified SQL.

Rejected: delete old API, hardcode demo name, suffix/order, infer from external
environment alone, new tag/config/IAM/cloud mutation. Existing owner scope
authorizes narrow check guard and compatibility behavior; no design question
needed. Readiness Ready, disposition executed, focused cycle complete. Parent
continues Plan/one critique then Implement/one independent Review. No external
web source needed for internal discovery contract. Actual image/runtime gates
and prior ACR receipts unchanged; no live setup was run.
