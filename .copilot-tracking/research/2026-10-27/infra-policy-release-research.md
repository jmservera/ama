<!-- markdownlint-disable-file -->
# Task Research: infra-policy-release

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-27/infra-policy-release-research.md |

## Research Brief

Research #147 and #138 for Bicep/workflow authoring only, preparing the
requested full RPI loop and one PR. Audience: repository owner and reviewers.
Output mode: convergence. Verify existing delivery before adding code.
Success requires criterion-level evidence without claiming live acceptance.

## Research Parameters

* Focused posture, selected for named issues and bounded authoring scope.
* Internal candidates: infra, deployment workflows, ADR 0002/0006 and linked
  BRD/PRD requirements. External candidates: official Azure/GitHub guidance
  only if a material API contract needs clarification.
* Evidence root: .copilot-tracking/. Research edits only evidence and state.
* No deployment, Azure writes, private data, secrets, environment/protection
  changes, uv or full gate. Local Bicep build and existing infra tests required.
  At most one optional scoped heavy gate; no need presumed.

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instruction | Repository instructions, all paths | Selected; src layout, evidence and branch safeguards |
| Skill | rpi-research | Selected; ordered wider/deeper/contrarian research |
| Specialist | RPI Researcher | Skipped; one tightly coupled evidence trace handled inline |
| Skill | security planning / mcsb | Skipped; no new security assessment or control activation authorized |

## User Participation and Research Decisions

User explicitly requests the full ordered loop and authoring-only PR. No
routine phase confirmation needed. Owner Defender spending and live OIDC/
environment decisions remain unapproved, not inferred.

## Scope and Success Criteria

Read issues/comments and linked requirements; compare existing authoring to
criteria; implement independent gaps only; compile Bicep and run infra tests.

## Task Research Requests and Direction Controls

No live acceptance or issue closure inferred from offline tests. Reuse supplied
clean topic branch feat/infra-policy-147 (no existing PR). One PR to main.
User's explicit local-only/no-full-gate direction governs this invocation.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What governance authoring exists and what needs owner decision? | depth | Answered |
| Q2 | What deployment authoring exists and which criteria are only offline? | depth | Answered |
| Q3 | What independent gaps can be fixed without cloud/owner decisions? | depth | Answered |

## Prior Knowledge Gate

Read case study, addendum opening, reference index opening and owner memory.
Issues/comments report prior #274/#333/#357 delivery; verify current sources.
No historical delivery is treated as current acceptance without inspection.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Issue comments identify existing governance and CI/CD authoring plus explicit
owner blockers. Inspect those sources and linked requirement sections next.
Reflection: do not recreate already merged pipelines or fabricate enablement.

#### Wave 2: Deeper

Inline inspection verifies OIDC environment separation, same-run digests,
private SQL checks, strict HTTP denials and sanitized plan artifacts already
exist (C3-C5). Pilot locks are only an example setting, not a guard (C6).
Release rebuilds/scans images but does not require successful complete source
CI on the release SHA and omits SBOM for those exact release images (C7-C8).
Reflection: reuse existing helpers; fix template/workflow wiring only.

#### Wave 3: Contrarian

Challenge: a green PR run is not proof for a later merge SHA; the current source
CI has no push trigger (C8). Require a successful manual main source-CI run
for the exact release SHA, not any historical green run. A source-CI SBOM is
not the SBOM of independently rebuilt release images. Explicitly disabled
Defender must not submit Free pricing resources, downgrade shared plans or be
enabled merely to close a criterion (C3). A stale exception reason must not
be treated as authority to expose SQL (C9). Naming-length suspicion rejected:
no demonstrated default-name defect; no naming changes justified.
Reflection: owner setup and paid-plan decisions remain blockers only for live
acceptance, not for bounded independent authoring.

#### Parent Synthesis and Disposition

Accept pilot lock guard and exact-source CI/SBOM release wiring, based on
C6-C8. Accept historical-only exception clarification based on C9. Reject
duplicate pipelines, subscription control activation, fabricated pricing or
claims of live acceptance. All waves performed inline; no delegated lane.

#### Cycle Re-entry Evaluation

No additional cycle needed: bounded contracts are established and remaining
unknowns require owner decisions/live execution explicitly excluded here.

## Evidence Log

* C1: Issue #147 and comments, retrieved with gh 2026-10-27: paid Defender
  decision/cost remains unrecorded; assignment/lock/exception criteria were
  already ticked by owner, not changed by this task.
* C2: Issue #138 and comments, retrieved with gh 2026-10-27: merged offline
  workflows do not establish OIDC, approval, push or deployed health acceptance.
* C3: infra/governance.bicep:6-72: pricing resources conditional on opt-in,
  built-in policy IDs and DoNotEnforce assignments.
* C4: .github/workflows/infra-plan.yml:1-110: default-branch workflow_run,
  separate environment plan identity and sanitized attached result.
* C5: infra/scripts/pipeline.py:211-450: required approval configuration,
  digest binding, ama-only incremental apply, SQL and HTTP probes.
* C6: infra/main.bicep:105-106,147-170 and
  infra/modules/guard.bicep:53-55: locks default false and pilot production
  guard does not independently require locks.
* C7: .github/workflows/src-deploy.yml:20-106: build/startup/scan gates,
  but no complete-source-CI prerequisite and no release-image SBOM.
* C8: .github/workflows/src-ci.yml:1-8,161-182: PR/manual triggers,
  source image SBOM and broad source/SQL/infra checks.
* C9: infra/policy-exceptions.json:9 and infra/README.md:1187-1195:
  historical exception reason contradicts current always-private SQL boundary.
* C10: docs/adrs/0002-pilot-readiness-architecture.md:932-965:
  pilot deployment depends on CI checks. ADR 0006:100-128 requires installed
  src packages, external tests and one workload image using src context.
* C11: docs/brds/agentic-retrofit-programme-brd.md:1487,1618 and
  docs/prds/zava-forward-retrofit-programme-demonstrator.md:2055,2153:
  application acceptance needs actual Azure/SQL/AI, unlike docs/unit/CI checks.

## Findings, Alternatives and Decision State

Selected approach: bounded guard and workflow wiring, retaining names, helpers
and all existing security defaults. Alternative of running CI automatically
through workflow writes/reusable restructuring adds unnecessary permissions/
check-shape change; require explicit manual source CI on main instead.

## Open Questions, Risks and Further Research

Subscription owner @jmservera must choose Defender service coverage/subplans,
accept current subscription-specific cost and approve activation. Effective
price/inventory and approval are unavailable; do not estimate a bill from
unknown quantities. Owner must provision protected environments, OIDC/RBAC and
private ephemeral runners before any real pipeline acceptance. No issue ticks
or cloud execution authorized here.

## Planning Readiness

Ready for independent authoring only. Research disposition: executed.
Self-check: all questions answered, ordered waves complete, evidence pointers
recorded, alternatives and owner blockers explicit; no live claims.
