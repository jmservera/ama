<!-- markdownlint-disable-file -->
# RPI Plan: Azure exercise build contract and decision-model learning

## Task Metadata

* Task ID: AMA-AZURE-EXERCISE-20261011
* Task slug: azure-exercise-build-contract
* Planning status: Full-plan implementation complete; outcome review ready
* Plan date: 2026-10-11
* Phase details: .copilot-tracking/details/2026-10-11/azure-exercise-build-contract-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-11/azure-exercise-build-contract-plan-critique.md

## Executive Summary

Plan the documentation update that makes real AI, a real SQL database and a real
Azure deployment mandatory for the next and subsequent AMA application exercise
builds. A local SQLite workflow or mocked model remains development evidence,
not an accepted replacement for those three requirements. Extract the current
PR #58 learnings without importing its implementation or equating real
inference success with model-value evaluation.

The parallel decision-model benefits experiment remains independent. Its results
may select or reject individual scoring tasks; uncertainty about decision-model
benefits must not silently remove the required AI, SQL or Azure deployment.
The one final critique is complete; its five planner-owned findings are
disposed below. Canonical BRD/PRD and supporting edits are implemented,
locally validated and published to the existing PR; outcome review is ready.
Candidate requirements review/owner acceptance and actual build remain separate.

### What You May Not Know

* The previous accepted exercise baseline permitted local durable state. This
  user direction changes that baseline prospectively; historical evidence stays
  historical.
* Current #58 at 5136f192d583a5bf53adeeec4b0f21369b005c9d reports an actual
  Azure deployment, Azure SQL, Decision 1 candidate selection and cited
  GPT-4.1-mini generation on retained generated data. Earlier access-blocked
  conclusions are historical, not the current feasibility finding.
* Its provider endpoint correction resolved an observed authentication failure;
  optional confidence is not a substitute for normalized selection probabilities.
* A binary support adapter cannot establish the PRD three-class macro-F1 gate.
  The parallel experiment explicitly acknowledges this measurement mismatch.
* Source-tested later controls are not necessarily in deployed revision
  ca-properwarm-mvp--0000018. Documentation must distinguish source, image,
  deployment revision and test/result versions.
* The requirements do not authorize purchases, deployments, paid inference,
  production use or real resident data in this planning phase.

### Unresolved Decisions or Blockers

* Parallel experiment is user-confirmed. The pinned #58 MVE is a proposed
  ten-working-day protocol, not executed comparative evidence. Human participants,
  calibration and paired effort remain unverified.
* #58 records owner-authorized deployment/inference and a rebuild-specific budget
  override. Do not continue listing those earlier questions as blockers; do not
  extend that override or authorization to every future build.
* Planning produces plan/details/critique only. BRD/PRD updates are explicitly
  scoped for /rpi-implement, not silently performed by /rpi-plan.

## Sources

* Current user /rpi-plan arguments: prospective real AI/SQL/Azure requirement,
  BRD/PRD learning extraction and parallel decision-model experiment.
* docs/case_study_48_original.md: preserved fictional use case.
* docs/case_study_48_addendum.md: accepted 2026-10-10 assumptions and budget.
* docs/brds/agentic-retrofit-programme-brd.md: business intent and options gate.
* docs/prds/proper-warm-retrofit-programme-demonstrator.md: v0.12.0 exercise
  baseline, optional decision-scoring language and quantitative acceptance.
* docs/ideas/typesafe-system-one-agent-fit.md: API/task limits and alternatives.
* PR #58 at 5136f192d583a5bf53adeeec4b0f21369b005c9d: current unmerged exercise
  implementation and result evidence; source URL https://github.com/jmservera/ama/pull/58.
* Pinned #58 mvp/README.md, Current continuing MVP: enabled AI, Azure SQL,
  60,000 retained stock rows, 980 programme cases and current revision/image.
* Pinned #58 docs/ideas/typesafe-system-one-agent-fit.md, Observed Feasibility,
  Not Proven Incremental Value: current successful inference and open benefits.
* Pinned #58 .copilot-tracking/mve/2026-10-10/decision-model-value/mve-plan.md:
  proposed R/D/A/H comparison, independence, binary/three-class caveat and
  decision gates; no execution approval or outcome inferred.
* Official Microsoft Learn deployment guide, retrieved 2026-10-11:
  https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-microsoft-decision.
  Typed text/JSON questions and provider-specific endpoint, not free-form rationale.
* Session evidence files/research/2026-10-11/proper-warm-build-readiness-research.md:
  earlier review pinned to 8d8b970, reused with revision caveat.

## User Decisions and Requirements

* The next exercise build and all subsequent AMA application exercise builds
  must use AI, a real SQL database and a real Azure deployment.
* Extract learnings from PR #58, especially decision-model feasibility, and
  update the BRD and PRD.
* A parallel experiment is identifying the benefits of decision models; keep
  its evidence and decision state distinct from application acceptance.
* Preserve the original use-case responsibilities, synthetic-data lineage,
  resident authority, professional judgement and bounded AI controls.
* Keep all application iterations in this AMA programme on the existing
  generated 60,000-home stock and retained programme lineage; small fixtures
  remain tests, not replacement MVPs.

The shared scope term is "accepted application exercise build": each
subsequent delivered AMA prototype, PoC or MVP, including iterations of the
existing application. Documentation-only work, unit/CI tests and non-delivery
development checks are excluded; they cannot be relabelled delivered prototypes
to waive real services. At least one in-scope app task must exercise a real
generative or decision model, chosen by task. Manual case access must not
depend on model availability.

## Goals

* Remove ambiguity that permits a local-only or mock-only accepted exercise.
* Turn #58 findings into traceable requirements and feasible acceptance gates.
* Define a parallel-experiment handoff that can inform model selection without
  inventing benefits, copying the experiment into application state, or
  blocking independent SQL/Azure/control work.

## Scope and Non-Goals

### In Scope

* Plan BRD, PRD, addendum and directly related knowledge-base consistency updates.
* Documentary applicability clarifications in both existing ADRs to preserve
  production options while rejecting local-only future acceptance.
* Pin current #58 findings and determine observed, blocked and untested states.
* Define AI/SQL/Azure acceptance and experiment integration requirements.

### Non-Goals

* No application/infrastructure implementation, deployment, spending or model calls.
* No merge, checkout or wholesale import of #58; no rewrite of historical results.
* No experiment implementation, participant recruitment, rerun or new MVE plan.
* No new company/regulatory research or access to private exercise answer keys.
* No claim of production approval, measured business benefit or experiment success.

## Functional Requirements

* Real AI is present in the exercised application path with source-bound output,
  human authority and explicit failure/manual handling.
* Actual Azure SQL Database owns durable state, approvals and audit for the
  Azure-hosted app; an in-process SQLite DB or local SQL container is not the
  accepted deployment. Azure SQL is the documented existing realization,
  not evidence of new production selection.
* Actual Azure endpoint, identity and persistence evidence is required; local
  containers or plan diagrams alone cannot satisfy deployment acceptance.
* Decision-model feasibility and incremental benefits are separately classified.
* Parallel findings enter through versioned task/result provenance and review.
* Preserve existing live inference as current observed evidence while keeping
  failed calls, stale acceptance rows and historical snapshots intact.

## Non-Functional Requirements

* Record effective budget and authorization per build. The prior USD450
  default/360 warning/405 pause and #58 rebuild-specific override remain
  distinguishable; do not reimpose the old cap on #58 or propagate its removal.
  Preserve source/task permissions, input bounds, reservations and cost telemetry.
  When effective budget or authorization prevents real-service evidence,
  report acceptance Blocked or Not run. Never waive spend controls or pass
  through template/mock/local substitution.
* Keep synthetic/non-identifying data and least-privilege access boundaries.
* Retain honest Pass/Fail/Not run/Blocked results, tied to source and deployment versions.
* Preserve mandatory safety, resident, professional, payment and funding controls.

## Acceptance Criteria

* BRD and PRD explicitly require real AI, real SQL and Azure for each accepted
  subsequent application exercise build.
* Contradictory local-only and optional-AI acceptance language is dispositioned.
* #58 learning statements are source-pinned and distinguish technical integration
  from actual model feasibility, benefit and full application acceptance.
* Parallel-experiment result ownership, validation and adoption gates are explicit.
* Decision-model technical feasibility is recorded as observed for the
  demonstrated candidate-selection path; general accuracy, calibration,
  three-class support screening and net benefit remain unproved.
* AI-required does not mean Decision 1 must pass every task. Negative/inconclusive
  task results retain rules/manual handling for that task, without accepting an
  entirely disabled-AI application as delivery.
* Plan/details are complete and exactly one final-candidate critique is disposed.

## Implementation Context Record

| Item | Record |
| --- | --- |
| Plan | .copilot-tracking/plans/2026-10-11/azure-exercise-build-contract-plan.md |
| Details | .copilot-tracking/details/2026-10-11/azure-exercise-build-contract-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-11/azure-exercise-build-contract-plan-critique.md; complete, findings disposed |
| Changes role | .copilot-tracking/changes/2026-10-11/azure-exercise-build-contract-changes.md; active implementation evidence |
| Readiness | Full-plan documentation implementation complete; outcome review ready |
| Continuation | User-directed RPI continuation through implementation and outcome review; no app deployment |

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Extract current learning and freeze requirements delta

* Intent: Translate prospective user direction and pinned #58 learning.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Classify PR #58 decision-model and build evidence

* Requirement and evidence: #58 current source/results; parallel experiment user statement.
* Expected result: Source-pinned learning register, current successful
  feasibility and explicit remaining task/value proof.
* Detail section: P01-T01 in the phase-details artifact.

<!-- rpi:phase id=P02 -->
### [x] P02: Update canonical requirements and supporting evidence

* Intent: Apply the documented baseline change consistently.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update BRD, PRD and addendum

* Requirement and evidence: Prospective real AI/SQL/Azure direction.
* Expected result: BRD v0.16.0 / PRD v0.13.0 candidate amendments, dated
  2026-10-11, consistent mandatory requirements and observable gates;
  historical v0.12.0 acceptance is not transferred to the changed version.
* Detail section: P02-T01 in the phase-details artifact.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Integrate learning and experiment handoff into existing knowledge base

* Requirement and evidence: Pinned learning register and existing decision-model synthesis.
* Expected result: Indexed findings, immutable historical evidence,
  experiment intake and ADR applicability clarifications with append-only log.
* Detail section: P02-T02 in the phase-details artifact.

<!-- rpi:phase id=P03 -->
### [x] P03: Validate and publish the documentation handoff

* Intent: Confirm requirements consistency and publish without executing the build.
* Dependencies: P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Validate traceability and deliver through a PR

* Requirement and evidence: Mandatory build gates, preserved historical baseline.
* Expected result: Reviewed diff, link/requirement checks and documentation PR.
* Detail section: P03-T01 in the phase-details artifact.

## Dependencies

* Current #58 commit: Source/result pin must remain explicit, not a moving-branch claim.
* Experiment outcomes: Not required for documentation or independent application
  platform work; required before benefit claims or value-based placement.
  Do not stop all integration until the experiment finishes.
* Cloud execution: Reuse actual #58 feasibility observations where applicable;
  future builds require their own source/image/deployment and functional proof.
  This documentation plan does not perform cloud execution.

## Locked Change and Validation Contract

* One documentation implementer owns all canonical edits; no parallel writers
  to BRD/PRD/addendum and shared ID tables. No runtime code or test owner changes.
* Canonical targets: docs/brds/agentic-retrofit-programme-brd.md,
  docs/prds/proper-warm-retrofit-programme-demonstrator.md,
  docs/case_study_48_addendum.md, docs/adrs/0001-azure-architecture.md,
  docs/adrs/0002-pilot-readiness-architecture.md,
  docs/ideas/typesafe-system-one-agent-fit.md,
  docs/reference/research/ux/prototype-learnings-and-simplicity-review.md,
  docs/reference/research/gap-analysis-next-build.md, docs/reference/README.md,
  docs/reference/log.md.
* Maximum additions: zero new production documents, zero executable tests,
  zero dependency/tooling additions; at most two new canonical requirement
  rows per requirements document, with complete existing ID/trace/count updates.
  Implementation changes record is the single stage-owned evidence addition.
* Exact removals: none. Amend contradictory active wording; never delete
  historical acceptance/results, old log entries or former failed attempts.
* Generated targets: none. Do not modify rubric badges/scores, binary decks,
  generated data or application assets.
* Semantic coverage: inspect all active platform/AI/model/budget/fixture
  statements against this task's mandatory baseline and experiment boundary.
  Sweep local-only, local durable, SQLite, optional AI/assistance/scoring,
  optional System One, fixture/MVP, not deployed, blocked inference,
  450/360/405 and EXA-012/016 across all ten targets. Each relevant hit needs
  an explicit disposition: superseded active wording, valid per-task/manual
  fallback, test-only path or clearly dated historical evidence.
* Regression coverage: preserve all existing human/consent/safety/financial
  gates, 46 PRD FRs, existing AC IDs and formal governance limitations. If
  rows are added, update coverage/counts instead of renumbering existing IDs.
  Expected canonical counts: PRD FR 46 unchanged, AC 56 to 57, CON 8 to 9;
  BRD FR 44 unchanged, AC 85 to 86, CON 6 to 7. Update all affected
  traceability/coverage/count summaries; count unique canonical table IDs,
  not repeated traceability references.
* Validation evidence: rendered Markdown and Git diff; relative-link and
  requirement/traceability consistency; original case/regulatory snapshots/
  owner memory untouched; no app tests or cloud calls for docs-only changes.

## Critique Disposition

| Finding | Disposition | Response |
| --- | --- | --- |
| PC-001 | Applied | Details explicitly target PRD FR-044, SA-004 and Components plus BRD AI/RULE-018 context: required deployed AI, optional individual assistance/manual access. No new FR. |
| PC-002 | Applied | Shared accepted-application-build definition and minimum real in-scope AI task above and in details; tests/docs excluded, delivered prototypes never waived. |
| PC-003 | Applied with budget correction | Missing effective budget/authorization blocks acceptance; no mock waiver. Reject blanket "USD450 unchanged" interpretation: #58 owner override is recorded for that rebuild, never propagated or erased. |
| PC-004 | Applied | Ten-target residual-term dispositions, explicit before/after unique counts and matching traceability/metadata requirements locked above and in P03 details. |
| PC-005 | Applied | Metadata, executive summary, context and handoff synchronized; single critique is complete, no second critique. |

## Follow-Up Items

* Fresh full-BRD/PRD requirements-quality review and owner acceptance of new
  candidate versions; RPI outcome review does not manufacture these approvals.
* Actual Azure/SQL/AI build and runtime validation belong to a subsequent build
  plan, not this requirements-documentation implementation.
* Parallel experiment owner supplies versioned execution results when available;
  existing proposed protocol is located on #58, not evidence of completed runs.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-11/azure-exercise-build-contract-changes.md
* Ready stage: RPI outcome review after full-plan completion and publication.
* Completed tasks: P01-T01, P02-T01, P02-T02, P03-T01; none remaining.
* Boundary: Ten-document implementation complete; no runtime deployment or
  independently accepted new BRD/PRD version is claimed.
