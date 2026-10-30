<!-- markdownlint-disable-file -->
---
title: Both demo sites redeployment research
description: Bounded operational research for an owner-authorized image-only refresh
ms.date: 2026-10-29
---

# Task Research: both-demo-sites-redeploy

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/both-demo-sites-redeploy-research.md |

## Research Brief

* What to research: exact prior ACR build/policy restoration route, employee and resident Docker contexts, safe image-only update and live verification.
* Why it matters: owner needs both public demo sites on latest main without configuration drift.
* Audience or intended use: deployment execution and independent operational review.
* Scope: ca-cutover-test-demo-api and ca-resident-demo in ama, environment cae-cutover-test-demo; existing ACR.
* Non-goals: source/UI changes, paid inference, authenticated testing, cost queries, infrastructure redeployment, SQL, other apps, roles, networking, subscription changes, deleting images, push or PR creation.
* Criteria: pinned main and digests, full private configuration backup, one new revision each, all other app configuration unchanged, healthy revisions/startup and unauthenticated smoke checks.
* Requested outputs: dated research, plan, critique, changes and independent Review; local evidence commit only.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Which exact build route and update preserve both apps and existing ACR policies? What proves success without authentication or secret disclosure? |
| Codebase scope | infra/, src/* Dockerfiles, prior deployment artifacts, docs/reference/log.md |
| External scope | Existing authorized Azure CLI resource reads and installed command help |
| Initial internal candidate areas | Previous employee redeploy and resident deployment records; resident Bicep/helper |
| Initial external candidate areas | Installed az acr build and az containerapp command help |
| Research posture | focused |
| Posture provenance | Default for explicit bounded operations request |
| Explicit limits / deadline | Owner's exact resource and operation restrictions; no invented deadline |
| Posture-specific completion basis | Scope coverage and materiality |
| Edits allowed during research? | no, research-only evidence and workflow state |
| Resolved evidence root | .copilot-tracking/ |
| Known constraints / excluded sources | Never read .env, private data or secret values; no gh or cost queries |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | Repository AMA and tracking instructions | Research and evidence scope | Preserve original evidence and local publication gates | Selected |
| Skill | rpi-research | Explicit full RPI loop | Three ordered evidence waves | Selected |
| Skill | Web/design skills | No web source edits or visual audit | Not applicable | Skipped |
| Research specialist | RPI Researcher | Available; single coupled operational trace | Separate lane unnecessary | Skipped; direct investigation |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision |
| --- | --- | --- | --- |
| Intake | Explicit user authorization and exact constraints sufficient; non-interactive execution | Full loop explicitly requested | Execute Research, Plan, Implement, Review in order without routine prompts |

## Scope and Success Criteria

Verify historical procedure against current inputs and CLI. Keep full configuration backups external with restricted permissions; commit only non-secret evidence. Build from a clean tracked snapshot of fetched main. Never use general infrastructure deployment helpers to refresh these existing apps.

## Task Research Requests

Record before/after image digests and revision IDs; verify app invariants, live health and startup; preserve min replicas zero. Roll back only for unhealthy deployment or startup errors, never just a tool error. Commit locally with owner privacy-safe identity and mandated Copilot trailer.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect |
| --- | --- | --- | --- |
| narrow | Two specified apps, existing ACR approved route only | Owner intake | Excludes broad infrastructure changes |
| exclude | Cost queries, gh, pushes, secret reads, image/tag deletion, SQL and unrelated resources | Owner intake | All phases |
| change | Latest fetched main rather than historical image source | Owner intake | Pin current main d70ee60ab3d7346a9991cf64382d9985f4d09f2e |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | What is the approved build/policy restore procedure? | depth | H | answered |
| Q2 | What is each build context and immutable deployment route? | straightforward | H | answered |
| Q3 | What live invariants and probes prove safe operation? | depth | H | answered |

## Prior Knowledge Gate

User historical revision and prior records are claims to verify. Case study, addendum, knowledge-base index and owner memory read at intake. Clean topic branch equals fetched origin/main; no source branch change needed.

## Research Cycle Log

### Cycle 1

* Active controls: owner limits above.
* Posture: focused; one continuous investigation inline, no artificial worker split.
* Wave order: Wider, Deeper, Contrarian.

#### Wave 1: Wider

Read prior employee redeploy and resident #474 execution, live resident follow-on,
Dockerfiles, Bicep/helper and knowledge-base log. C1-C4 establish local Docker
build/push as the earlier successful approved route. Cross-session history lookup
returned no matching recent sessions; durable repository records supply evidence.

Reflection: do not run the resident infrastructure helper: it can create role
assignments and is outside this image-only authorization.

#### Wave 2: Deeper

Verified installed CLI help for update, revision list/show and logs. System logs
must be app-scoped without revision/container selectors, whereas console supports
both. Current employee baseline matches the owner's exact historical re-apply.
Resident baseline is later than #474 and has a future existing expiry. Both use
Single mode, external FQDNs and min replicas zero. C5-C7.

Reflection: preserve the *current* resident configuration, not the older closed
ingress/October expiry. Preserve all employee AI entries without setting them
again. Both Dockerfiles require src/ context.

#### Wave 3: Contrarian

Challenged remote ACR builds against private registry and strict approved route.
#474's actual remote run failed registry-login 403; widening to arbitrary ACR
worker IPs or AzureServices bypass would exceed the successful VM-only route.
Choose local Docker build from clean exported main and unique-tag push through
the exact earlier approved expose-token route. This is the explicitly allowed
approved-route alternative, not a cloud-build pass. Installed Docker works.
App metadata health alone previously masked resident startup failures; require
actual HTTP health and positive target-revision startup/ready evidence. Tool
failure is never itself an unhealthy revision. Existing digests must remain
pullable and no registry deletion is allowed.

Reflection: caller criteria and route are covered; remaining live execution
uncertainty belongs to implementation. No further research cycle is justified.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs | Parent disposition | Rationale | Treatment |
| --- | --- | --- | --- | --- |
| Approved local build plus VM-only push | C1-C3, C7 | accepted | Actual earlier success; no worker-network widening | Planning route |
| Full resident infrastructure deploy | C4 | rejected | Changes identities/roles, not just image | Excluded |
| ARM Healthy alone proves startup | C2 | rejected | Earlier resident ProgrammingError despite metadata health | Require real health/logs |
| Historical resident closed ingress should be restored | C2, C6 | rejected | Current app differs; owner requires current exact preservation | Back up current baseline |

#### Cycle Re-entry Evaluation

Another complete cycle needed: no. All three questions answered with directly
verified sources and installed capabilities; no material unresolved alternative.

## Evidence Log

| ID | Source | Evidence |
| --- | --- | --- |
| C1 | .copilot-tracking/changes/2026-10-28/employee-redeploy-changes.md:32-112,145-189 | Exact approved re-apply, previous digest, local build/push route and policy restoration; bare-IP normalization |
| C2 | .copilot-tracking/changes/2026-10-27/deploy-resident-474-changes.md:48-114 | Remote ACR 403; successful local build/push; metadata health insufficient |
| C3 | .copilot-tracking/details/2026-10-28/employee-redeploy-phase-details.md:115-144 | VM-only /32, public Disabled before rule, exports allowed temporarily, public enabled only with default Deny, memory-only expose token, private-first finally and exact equality |
| C4 | infra/resident-demo.bicep:95-155; infra/scripts/resident_demo_deploy.py:1-15; src/api/Dockerfile:1; src/api/Dockerfile.resident-demo:1-3 | Resident helper changes roles, so not used; exact Dockerfiles and src/ context |
| C5 | Installed az containerapp update/revision/logs help, inspected 2026-10-29 | Image/container/suffix-only update; console revision selectors; system logs app scoped |
| C6 | Live safe Azure GET summaries, 2026-10-29; .copilot-tracking/changes/2026-10-27/resident-live-acceptance-changes.md | Employee emp-reapply-20261028-110058 digest e6b6e744...; resident 0000003 digest fab6a853...; resident expiry 2026-12-31T23:59:00Z; min0/max4 and min0/max1; same environment |
| C7 | git fetch origin main, git rev-parse and Docker version, 2026-10-29 | main d70ee60ab3d7346a9991cf64382d9985f4d09f2e; src tree 6684959daaa64df7f8768c4fddb24406f198a308; Docker29.9.0; ACR Premium, public Disabled/default Allow/no rules/bypass None/exports disabled/admin false |
| C8 | docs/reference/log.md:7627-7644 | Earlier resident deployment boundary and unproved authenticated acceptance |

Delegation: inline; tightly coupled trace, no independent research lane needed.
Live metadata and installed help are non-secret operational evidence, not legal
or acceptance authority.

## Findings Mapped to Questions and Evidence

Q1: C1-C3/C7 support exact approved local build/push and restoration.
Q2: C4/C7 support clean main export, correct Dockerfiles and digest-only updates.
Q3: C1/C2/C5/C6 support complete backup/equality, revision-set proof,
positive startup and anonymous-only endpoint smoke testing.

## Alternatives and Decision State

Image-only app update is the caller-selected boundary. Full infrastructure redeployment is excluded.

## Open Questions, Risks, and Residual Uncertainty

Full private configuration and auth metadata backups occur before mutation.
Billing/headroom remains unknown by explicit no-query direction. Registry token
availability, builds and new runtime health are execution risks, not proven yet.
Anonymous probes cannot establish authenticated new-feature or human acceptance.

## Planning Readiness

Ready. Evidence supports the selected bounded route. Current configuration must
be backed up and rechecked immediately before mutation; no cloud writes occurred
during Research.

## Research Disposition

Executed, complete. Primary artifact self-check: brief, extension provenance,
ordered waves/reflections, evidence IDs, alternatives, constraints, risks and
readiness recorded. Return to active parent for Plan.
