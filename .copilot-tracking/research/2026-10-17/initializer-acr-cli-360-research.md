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
