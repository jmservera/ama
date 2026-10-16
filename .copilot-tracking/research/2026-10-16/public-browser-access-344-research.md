<!-- markdownlint-disable-file -->

# Task Research: public-browser-access-344

| Field | Value |
| --- | --- |
| Date | 2026-10-16 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-16/public-browser-access-344-research.md |

## Research Brief

Restore public src browser entry for #344, selecting the simplest safe edge
allowed by the owner. Audience: deployment operator and cut-over reviewer.
Scope: infra, src, deployment and requested evidence. Non-goals: legacy changes,
private datasets, tenant consent, operational legal approval and resource-group
deletion. Output mode: convergence. Criteria: public health 200, anonymous API
401, Entra redirect, private SQL, complete feature audit and explicit blockers.

## Research Parameters

Focused posture (bounded caller request); .copilot-tracking is the evidence root.
Read-only research. No time ceiling. External scope: official Azure networking
and authentication documentation. Exclude private data, credential contents,
.env, .vscode and github-issues tracking.

## Extension Registry and Provenance

Repository instructions and ADR 0006 selected for all paths. RPI research
selected for evidence. No specialist dispatched: networking/auth is one
continuous trace, not independent lanes. User interaction unavailable; supplied
owner direction authorizes bounded deployment, gap filing and PR publication.

## Research Questions

### Owner-requested PR 352 continuation evidence

Supplied independent CHANGES verdict at 3f33ff1 is reused, not a new broad
research/critique cycle. Fetched main 204b434 contains merged PR 356's setup
command. Its existing stateful test
`test_pending_edge_custom_forward_headers_and_public_url_fit` covers this
edge's public callback, Custom forwarded headers and idempotence. Preserve
the legacy main() delegate; no setup algorithm extension is necessary.

The previous nonempty auth-client check accepts the managed-identity sentinel.
Require UUID hexadecimal syntax, exact length and separators through the
existing nested minLength guard pattern. Compiled-expression tests must reject
the old nonempty-only behavior. UUID syntax does not prove Graph existence.
The auth helper PUT preserves only fields present in its read response;
document the omitted/reference limit rather than claiming credential recovery.
Fresh public probes reproduce browser JSON API 302 versus native 401; #350
must retain the explicit unmet coexistence criterion. Planning readiness:
Ready for owner-requested P04; real login and feature acceptance remain Blocked.

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Can the existing internal environment safely expose the API via Private Link? | depth | Supported by official guidance/live resource advertisement; deployed transport requires execution proof |
| Q2 | Can browser auth reuse the existing registration/credential? | depth | No valid retained workbench registration/credential; Blocked, #349 |
| Q3 | Which historical visible features have deployed proof? | depth | Matrix's complete capability/asset audit identifies required evidence; positive-user acceptance Blocked, #350 |

## Prior Knowledge Gate

Read original/addendum, knowledge index/memory, #344/#143/#118, infra README,
main/containerapps/edge, parity matrix, cut-over pack/JSON and ADR 0006.
Clean worktree on dedicated feat/public-browser-access-344, no open PR.
Supplied internal/bearer-only facts confirmed through scoped management queries.

## Direction Controls

SQL public access stays Disabled; no exemptions, firewall or policy bypass.
Only ama resources, no group deletion. Named human approval remains necessary
for legal interpretation, rule activation, safety, consent and commitments.
Juan Manuel Servera is the synthetic exercise Legal/Compliance/DPO owner;
ADR 0005 acceptance is synthetic-development-only, not operational approval.

## Research Cycle Log

### Cycle 1

#### Wider

Inspected existing edge implementation and independent environment/data access
controls. Existing main couples public API networking to all public services,
including SQL. Reusing that switch would violate the owner constraint.

Reflection: select a separate edge or API-only external environment, never
allowPublicNetworkAccess on the entire existing stack.

#### Deeper

Current environment internal=true/publicNetworkAccess=Disabled. API pinned to
src digest 111b26226cad06e229bcf1c3174877510c4c68c5a5fefc885167a2b4c821657d.
Auth Return401, registration configured, no secret settings. Vault access
from operator VM is denied by private networking; do not weaken it.
VNet has 10.40.0.0/23 ACA and 10.40.4.0/24 PE subnets.

Reflection: lack of browser credential is a separate prerequisite from a public
network path. The public welcome and application API already enforce their own
anonymous boundaries.

#### Contrarian

Official networking guidance permits private endpoints on existing workload
profile environments, including internal ones. The live environment advertises
managedEnvironments. FD avoids replacing an environment, subnet, apps or jobs.
The external-environment alternative is allowed but adds a parallel environment
and deployment wiring without solving the tenant prerequisite.

The existing auth client is the non-UUID literal systemAssignedIdentity, not
a usable application registration. Both operator and isolated tenant reads
confirmed no such registration. The isolated profile matches the deployment
tenant and can list applications, but bounded discovery found no retained
Zava/properwarm workbench registration. Do not create tenant objects or invent
credentials under resource-group-only authority.

Reflection: choose Front Door Premium, WAF Prevention and Private Link against
the existing internal environment. Deploy a scoped additive edge, not the full
development stack or a production-profile conversion. Browser sign-in is
Blocked on tenant registration/secret/callback/staff prerequisites; a redirect
alone cannot satisfy real-user sign-in.

## Evidence Log

| ID | Location | Finding |
| --- | --- | --- |
| C1 | infra/main.bicep:112 | publicAccess couples development access for all data services |
| C2 | infra/modules/containerapps.bicep:53 | environment internal immutable direction follows public switch |
| C3 | infra/modules/containerapps.bicep:209 | browser default, bearer-only opt-in, exact public paths |
| C4 | src/api/src/zava_forward/api/server.py:199 | public health/welcome, /sign-in and protected API 401 |
| C5 | infra/modules/edge.bicep:1 | internal environment Private Link marked unverified |
| C6 | infra/README.md:591 | callback repair requires isolated authorized tenant profile |
| W1 | https://learn.microsoft.com/en-us/azure/container-apps/networking | Retrieved 2026-10-16: internal environment cannot become external; private endpoints supported |
| W2 | https://learn.microsoft.com/en-us/azure/container-apps/how-to-integrate-with-azure-front-door | Retrieved 2026-10-16: Premium, managedEnvironments and explicit connection approval |
| W3 | https://learn.microsoft.com/en-us/azure/container-apps/private-endpoints-with-dns | Retrieved 2026-10-16: existing workload-profile environments support Private Link; added charges |

## Alternatives and Current Decisions

Accept additive FD + WAF + Private Link (C5, W1-W3); reject global publicAccess
(C1); defer external replacement (more churn, same tenant blocker). No claim
that development proof establishes production controls or pilot approval.
No second cycle: named alternatives and material unknowns are resolved or
explicit prerequisites; additional source discovery cannot provide consent.

## Self-check

All three waves completed inline; no worker results claimed. Source/data
boundaries preserved. Real-user, full deployed parity and owner acceptance
remain unknown. Cost is a trade-off, not a new quoted estimate or approval.

## Planning Readiness

Ready for scoped edge/auth configuration and honest audit. Research disposition:
executed. User explicitly requested remaining phases. Tenant prerequisites block
real-user acceptance, not public network-path validation.
