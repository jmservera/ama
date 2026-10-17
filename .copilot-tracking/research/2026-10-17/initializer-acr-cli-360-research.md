---
title: Initializer ACR CLI research
description: Renewed publication investigation for issue 360
ms.date: 2026-10-17
---

## Research Brief

Task `initializer-acr-cli-360`, issue #360. Focused convergence research for an
ordered Research, Plan, Implement, Review delivery. Determine whether existing
hosted ACR quick builds can publish the retained-base initializer despite VM
private-endpoint failure. Audience: owner and independent reviewer.

## Research Parameters and Direction Controls

Research root: `.copilot-tracking/research/2026-10-17/`.
Use the existing registry, source Dockerfile/context and existing job only.
No new infrastructure, paid pool, public access, bypass, IAM, job execution,
Graph/SQL/private-data mutation, API restart or retirement. Preserve pinned base
security upgrades and the seven-file context fixed in #381. Local Docker proof
precedes the actual bounded hosted attempt in Implement. Historical run dbb is
not current publication evidence. Criteria d/e remain unmet.

## Extension Registry and Participation

Repository instructions and RPI research selected; focused inline investigation
fits one continuous trace, so no research worker. Later canonical phase skills
and independent critique/Review apply. No web changes or design skills.
The explicit full ordered request authorizes phase progression, not wider cloud
actions. No interactive questions are needed; supplied scope is sufficient.

## Questions and Candidate Areas

1. What exact source, base, context, local smoke and publication gates are retained?
2. What do current registry/run metadata and CLI contracts actually establish?
3. What is the safest image-only update preserving the complete existing job?

Start with infra/source guides, #360 and merged #375/#379/#381, existing evidence,
CLI help and read-only Azure metadata.

## Research Cycle Log

Cycle 1, Wider: read case original/addendum, KB index/memory/sector primer,
source/API and infra guides, issue #360 and merged #375/#379/#381 via GitHub.
Reflection: no feature work is needed; prior work never attempted hosted Tasks.

Cycle 1, Deeper: inspect exact Dockerfile/ignore, CLI 2.91.0 build/update help,
current job metadata and registry/run/pool readbacks. Docker Server 29.9.0
works, but the retained private base is not cached. Reflection: attempt local
build first with a finite bound, then actually try hosted quick build, irrespective
of local endpoint failure. Use `infra/`, not `src/`, for the proof Dockerfile;
the retained API base already contains the source distributions/security upgrades.

Cycle 1, Contrarian: current `show-run dbb` independently confirms historical
Succeeded, ordinary cpu2, 2026-10-16T13:53:04 through 13:53:24 UTC, repository
zava-forward-cutover-proof:proof-20261016 and digest
sha256:ef0058f8f380cc610d4b7113509293b3ed624d22afac95e807b4c69a4266dc72.
Five latest runs all succeeded; agent pools list is empty. These disprove the
claim that missing pool/private VM connectivity alone establishes hosted
unavailability, but do not prove a new build can upload source or authenticate.
Reflection: only the actual current build command can establish its failure
stage; do not replace it with network extrapolation.

Parent synthesis: one focused cycle covers all planning questions. No further
research cycle is necessary before bounded implementation experiments.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | `infra/cutover-proof.Dockerfile:1-6` | Retained API_IMAGE argument, exact five Python files and app-registration manifest; inherited UID/security contract |
| C2 | `infra/.dockerignore:1-8` | Seven-file native context from merged #381 retained without directory-wide exceptions |
| C3 | `infra/README.md:1839-1940` | Historical local route results and retained API digest; unattempted hosted builds incorrectly constrained to private publisher |
| C4 | `src/api/Dockerfile:2-34`, `src/README.md:53-83` | Pinned Python base and apt upgrades must not be replaced with an arbitrary cached image |
| C5 | `infra/tests/test_container_contract.py:77-115` | Existing pinned/nonroot/runtime controls regression coverage |
| W1 | https://learn.microsoft.com/en-us/azure/container-registry/container-registry-tasks-overview retrieved 2026-10-17 | Quick task uploads context and builds/pushes in cloud without local Docker |
| W2 | `az acr task show-run --run-id dbb` and `list-runs`, retrieved 2026-10-17 | Retrospective successful ordinary cpu2 runs; not current proof |
| W3 | `az acr show`, `agentpool list`, `containerapp job show`, retrieved 2026-10-17 | Public Disabled, bypass None, no pools; existing Manual proof job, old digest, six env names, no declared secrets |
| W4 | Azure CLI 2.91.0 `az acr build --help`, retrieved 2026-10-17 | Local context, relative Dockerfile, --timeout/--no-wait and default cloud push supported |

The attempted network-restricted Tasks documentation URL returned 404 and is
not used as evidence. CLI/run evidence plus the successfully retrieved official
overview establish the experiment without speculative networking claims.

## Findings, Alternatives and Decision State

Selected: local retained-base attempt, safe no-network image smoke if possible,
then an actual bounded `az acr build` of the exact proof context using a unique
source-SHA tag. Record source upload separately from hosted agent pull/build/push.
If hosted succeeds but the resulting image cannot be pulled and actually
validated locally, do not pin; publication success is not runtime proof.

Rejected: arbitrary local cached-base substitution, new paid pools, bypass or
public registry changes, IAM changes, and any initialization execution. All
violate owner scope or destroy exact base/source provenance.

Conditional pin: inspect the current CLI implementation/ARM PATCH contract,
preserve the complete existing container/template/configuration/identity, compare
all non-image read-visible settings before/after, and never start a job.

## Open Questions, Risks and Residual Uncertainty

Current source upload and hosted-agent access remain empirical implementation
questions. Local base unavailable so local smoke may be blocked. Public
API/browser, tenant, SQL, AI and retirement acceptance remain out of scope.
Read-visible settings comparisons cannot attest secret-payload equality.

## Current Decisions and Potential Next Research

Existing owner publication/conditional pin approval applies, no broader consent.
No independent research delegation warranted. Re-enter research only for a
concrete command result requiring an in-scope alternative.

## Planning Readiness

Ready for bounded plan. Research disposition: executed. All three waves complete.
Artifact self-check: questions mapped, source refs/dated external refs recorded,
alternatives and failed retrieval disclosed. Parent continues to Plan.

## Authorized Read-Only Root Diagnosis Continuation (2026-10-17)

Brief: compare successful dbb (October16) and failed dbc (October17), current
registry/platform/task identity and caller action permissions, restricted ARM
activity metadata and official Microsoft documentation. Focused analysis-only
cycle2; no new full RPI or repeated critique/Review. Original Review remains
Complete/Residual work. No new builds/Azure writes, sensitive identity/activity
payloads, secrets/SAS/log payload retrieval, network/IAM/bypass changes.

Integration independently authorized: clean topic60134c5 rebased onto verified
origin/main bbbc9243505b606550327c64bf5429243f457f2e, result6311b51 before
this diagnosis. Only additive log conflict, exact main log prefix and both
upstream/topic routing retained. Historical dbc tested source remains bab4bf3,
not the integration head; command receipt and original Review byte-identical.

Cycle2 questions: did success precede a firewall configuration change; what
existing hosted identity/path and platform restrictions explain login403; are
trusted-service/VNet-agent alternatives documented and already available?
Start wider with retained sanitized receipts, registry/task metadata, action
permissions and official network/task guidance, then deepen timeline and
challenge the leading explanation. All findings remain evidence versus inference.
No interactive intake needed; explicit scope is sufficient. No research worker.
Readiness for cloud remediation is Not authorized; report smallest owner choice
with cost/security impact rather than mutate or repeat an empirical build.

Cycle2 Wider reflection: both runs are QuickRun Linux/amd64/cpu2, task null,
pool null; current named tasks/pools and ama VM inventory empty. Current
LegacyRegistryPermissions (not ABAC), Premium UK South, public Disabled/bypass
None, approved private endpoint. Current registry networkRuleSet defaultAllow
does not override publicDisabled. Prior primary evidence
`.copilot-tracking/changes/2026-10-16/deployed-src-proof-changes.md:20-26`
explicitly records all images captured BEFORE registry isolation. This materially
supports the firewall-change hypothesis; deepen timeline rather than assume
the successful run used today's network state. Official private-endpoint guide
explicitly documents default az acr build failure when public access is disabled.
General trusted-services page is not proof of task exemption; investigate the
task-specific bypass property separately. No log payloads retrieved.

Cycle2 Deeper reflection: registry-scoped activity metadata shows successful
registry writes AFTER dbb, first completing October16 13:56:53.6373221Z, then
14:07:30, 14:14:17 and22:34:36; dbc scheduleRun succeeded October17 17:57:22.
Metadata proves update timing, NOT which property changed or by whom; no caller,
claims, identity, request/response/change payload retained. Together with the
contemporaneous "before registry isolation" record, network isolation between
builds is the leading explanation, not an assumed same-state regression.

Effective caller permissions endpoint returns actions["*"], no exclusions,
empty dataActions; this supports control-plane read/schedule capability, not
hosted-agent token/pull authorization. Both QuickRuns task/pool null, so no
named managed-identity task or hidden inherited selected pool is demonstrated.
No identities/tokens or task credential payloads inspected.

Task-specific Microsoft guidance adds a material qualifier: SAMI task network
bypass defaults to denied when networkRuleBypassAllowedForTasks is unset
(June1,2025 transition), unlike generic trusted-service access. Current preview
GET returns null for that property; distinguish absent/null from literal false.
The exact daemon token identity is not exposed by selected run metadata; this
policy is a candidate contributing condition, not a proven SAMI attribution.
No blanket promise that toggling trusted services alone fixes QuickRun403.

Cycle2 Contrarian: explicitly test same-state/auth-only/pool hypotheses.
No named task or selected pool appears on either run; registry is not ABAC,
caller actions include wildcard, and source upload/schedule already succeeded.
These weaken a control-plane permission or ABAC-switch explanation but do NOT
attest daemon credentials. Preview2025-06-01 GET confirms task-bypass property
ABSENT (not false). Official policy says unset denies SAMI task bypass; it also
says UAMI is unaffected, but this does not establish any UAMI as present or
grant network access to an arbitrary quick build. Generic trusted-service table
lists ACR import, not an automatic default QuickRun exemption. Caller-identity
CLI option changes authentication, not network reachability.

The 194 selected exact-registry activity events are below requested max200,
oldest creation12:08:01 October16 within requested11:55 October16 to18:20
October17 window. This is bounded returned metadata, not a complete property
history or proof of no unlogged/provider changes. No role/principal history,
diagnostic login logs, SAS or build log payload fetched in this continuation.
UK South is absent from the published agent-pool preview region list (retrieved
October17); no new same-region pool should be presumed available. Existing ama
VM/pool inventory empty does not rule out an externally owned self-hosted runner
outside inspected scope. No such publisher demonstrated here. Reflection:
evidence saturates within authorized metadata scope; further empirical testing
or property-level/auth diagnostics would need separately bounded authority.

### Cycle2 Evidence and Source Register

| ID | Evidence, retrieved 2026-10-17 | Finding |
| --- | --- | --- |
| C6 | `.copilot-tracking/changes/2026-10-16/deployed-src-proof-changes.md:20-31` | dba/dbb images captured before registry isolation, private bootstrap completed14:03:51 |
| C7 | `infra/modules/registry.bicep:16-33` | Explicit development public switch, bypassNone; no task-specific bypass declared |
| C8 | `.copilot-tracking/changes/2026-10-17/initializer-acr-cli-360-command-receipt.json:1-147` | Actual historical sourcebab4bf3/context/payload/base, dbc failure and unchanged-job proof, preserved byte-identical |
| W5 | https://learn.microsoft.com/en-us/azure/container-registry/container-registry-private-endpoints#use-az-acr-build-with-private-endpoint-and-private-registry | PublicDisabled default-build limitation; dedicated pool or regional public IP allowlist alternatives |
| W6 | https://learn.microsoft.com/en-us/azure/container-registry/manage-network-bypass-policy-for-tasks | Task-specific SAMI bypass opt-in, unset denies; UAMI qualifier; self-hosted/private and pool alternatives |
| W7 | https://learn.microsoft.com/en-us/azure/container-registry/allow-access-trusted-services | Generic trusted-service opt-in does not remove auth requirements; ACR import usage, not blanket Tasks claim |
| W8 | https://learn.microsoft.com/en-us/azure/container-registry/tasks-agent-pools | VNet support, allocation billing, preview/region limits; UK South not listed |
| W9 | https://learn.microsoft.com/en-us/azure/container-registry/container-registry-tasks-authentication-managed-identity | Task identity attached/configured explicitly; no inherited named task shown for these QuickRuns |
| W10 | https://learn.microsoft.com/en-us/azure/container-registry/container-registry-troubleshoot-access | Network403 and authentication symptoms can overlap; no automatic RBAC conclusion |
| W11 | Exact-registry activity-log GET, October16 11:55 to October17 18:20, max200, projection timestamp/operation/status only | dbb precedes writes13:56:53,14:07:30,14:14:17,22:34:36 October16; no property delta or actor attribution |
| W12 | Registry GET preview2025-06-01 and permissions GET2022-04-01 at exact registry scope | Task bypass absent; publicDisabled/bypassNone; actions["*"], no exclusions; empty dataActions not proof of daemon-token access |
| W13 | Registry/task/pool/run GET projections and ama VM inventory | Premium/UKSouth/LegacyRegistryPermissions, both QuickRun linux/amd64/cpu2/no task/no pool; no current named task/pool/ama VM |

### Cycle2 Synthesis, Options and Explicit Authority Gap

Leading likely root reason, strongly supported: successful dbb preceded registry
isolation; default hosted dbc later encountered registry network restrictions.
This is not evidence that ACR Tasks cannot run: its upload/scheduling worked.
Activity metadata corroborates later configuration writes; original primary
record supplies the before-isolation fact. Exact public/bypass value at dbb,
exact changed property/write, daemon token identity and server403 subreason
remain unproven by this deliberately payload-free diagnosis. No RBAC denial
claimed and no need for a new grant demonstrated.

| Candidate next option | Security/cost impact and authority |
| --- | --- |
| Identify an already existing authorized private-connected Docker runner/operator | Preferred no-bypass path if one exists; uses existing rights/capacity, no new service allocation; access, authorization and capacity not demonstrated here. Owner must identify exact runner and approve bounded build/pull/smoke/publication |
| VNet-integrated ACR agent pool | Preserves private registry path but new allocated compute is billed even idle; none exists, UK South not in documented preview list. Requires separately reviewed region/support, network, quota, price/ceiling and owner spend approval; not provisioned |
| Task-specific/SAMI and generic trusted-service bypass investigation/opt-in | May avoid new dedicated compute but explicitly relaxes network isolation and requires exact identity/applicability validation; absent property does not authorize toggle. No guaranteed one-flag remedy, no current approval |
| Regional public task-IP allowlist/public access | Documented alternative, but changes public network boundary; conflicts with standing owner requirement and is not recommended or authorized |
| Change auth flag/new role alone | Not evidence-backed cure for blocked network path; no IAM change justified; no retry authorized |
| Microsoft support using sanitized metadata | Non-mutating diagnosis option if exact service-side cause needed; no ticket or external payload submission made; owner controls support/cost context |

Smallest owner decision for later work: identify an existing authorized
private-connected publisher, or keep image delivery blocked while deciding
whether to separately appraise a costed private-pool design or explicit
task-bypass exception. Current no-public/no-bypass constraint remains in force.
Do not ask for blanket permission/new roles or represent this as regulatory
approval. No command is authorized by the option table.

Cycle2 research execution Complete, disposition executed, analysis-only.
No repeat Plan/Implement/Review; original single Review remains Residual work.
No cloud remediation handoff authorized. Parent may integrate documentation
and publish PR385 under explicit coordinator direction, then stop for external
review/owner authority. No additional cycle needed within metadata-only scope;
re-entry requires precise approved access evidence or service-side subreason.
