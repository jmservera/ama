<!-- markdownlint-disable-file -->
---
title: Five Retrofit Assistants Research
ms.date: 2026-10-13
status: Source analysis complete; live-rollout authorization pending
---

## Research Brief

* Request: add the five reactive/proactive assistants to the PRD and ADR, then build a new version.
* Intended use: evidence for extending the existing Zava Forward MVP, not a separate application.
* Scope: current PRD, ADR 0001/0002, the published process map and existing MVP task, store, permission and worker contracts.
* Non-goals: autonomous approvals, resident consent, external messages, scheduling commitments, work release, safety decisions, funding submission or payment; merging PRs or moving private/existing work.
* Output mode: analysis preparing planning.
* Research posture: focused, selected for the named five-capability extension and existing application.
* Explicit limits/deadline: none supplied.
* Resolved evidence root: `.copilot-tracking/research/2026-10-13/`.
* Research-only: no canonical PRD/ADR, application, infrastructure or deployment changes in this phase.

## Extension Registry and Provenance

| Extension | Disposition | Boundary |
| --- | --- | --- |
| Repository instructions | Selected | Existing MVP/data lineage, topic/PR safeguards, quantitative evidence, approval boundaries and knowledge-base placement |
| RPI Agent and rpi-research | Selected | Manual intake; one focused wider/deeper/contrarian cycle; no automatic mode without confirmation |
| Requirements authoring / ADR authoring | Deferred | Relevant to the later document-authoring phase, not authority to edit canonical documents during research |
| Research specialists | Skipped | One tightly coupled existing-runtime trace; inline investigation avoids duplicate work |
| Cloud/SDK research | Deferred | No new service or SDK selection is made in this internal source gap analysis |

## User Participation and Research Decisions

The user expressly requested all five assistants, PRD/ADR integration and a new
version. The intended application target is strongly supported by the existing
MVP lineage, but "new version" did not explicitly distinguish image-only work
from deployment or a presentation update.

An intake form offered application deployment, image-only implementation or a
presentation-only update; automatic/manual execution; and an isolated stacked
worktree/PR versus continuing #68. The interaction tool reported that the user
was unavailable. None of its suggested choices was accepted. Do not treat
defaults as automatic-mode consent or permission to move existing work.

Continue bounded read-only research in manual mode. Keep the existing
presentation working files and private configuration untouched. No shared
environment deployment is authorized by the unanswered form.

## Direction Controls

* The five assistants are the capabilities shown in the published process map.
* Preserve staff-requested help and permitted event/scheduled review as separate invocation modes.
* The deterministic workflow owns eligibility, versions, gates and controlled state.
* Every assist produces an unreviewed proposal or raise-only flag for a named human owner.
* Use the continuing generated stock/programme dataset, real SQL and real AI for an accepted application exercise build.
* Do not infer that the presentation proves deployed proactive workers or measured value.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | Which assistant requirements already exist, and which explicit reactive/proactive contracts are missing? | Answered, C1/C10 |
| Q2 | Which existing runtime, review, storage and role contracts can be reused safely? | Answered, C4-C8/C11-C13 |
| Q3 | How do the current worker placeholders differ from the proposed proactive implementation? | Answered for inspected source, C3/C9/C14 |
| Q4 | What evidence and owner decisions are required before claiming a new deployed version? | Evidence requirements answered, C2/C15; intake direction remains unanswered |

## Prior Knowledge Gate

Reviewed the original case, evolving addendum, reference index, owner memory,
sector primer, capstone diagram handoff and current MVP README. The earlier
account-switch RPI task is completed/stopped; this is a distinct task.

Local source pin: `0af4a9b481008c0e00206c34532af8039c18b7a6`.
Open #68 remote head: `55596a5a8e8ede6bd2d65eeaafab9566b1da3b18`.
GitHub comparison shows only `.github/rubric/scores/latest.json` changed
upstream. Do not silently rebase or move the existing untracked deck outputs.

## Research Cycle Log

### Cycle 1

#### Wider

Existing documents already constrain bounded AI, a versioned task registry,
real-platform exercise acceptance and deterministic orchestration. The current
MVP has several on-request drafting/recommendation tasks; ADR 0001 explicitly
states that workers remain placeholders. Prioritize the exact task/review/store
paths and the worker source before recommending five new deployments.

#### Deeper

The existing request path can supply citations, explicit workflow-only output
and a persisted recommendation comparison record. However, it is not a
drop-in proactive task service: review is requester-only, the record has no
captured case/source version, and the funding drafting method updates the case
draft/status immediately. A background worker must not inherit that mutation
path or impersonate a staff requester.

The SQL driver already transactionally writes recommendation bodies alongside
audit entries with optimistic row versions. This is a useful persistence
primitive, not evidence of durable task claiming, event outbox publication or
exactly-once completion across replicas. Assess those properties separately.

Reflection: the material extension needs a named task registry, immutable
version-bound evidence snapshots, role-owned review queues and a durable
invocation/claim lifecycle. New labels or a polling timer alone would not
satisfy the published assistant contract.

#### Contrarian

The proposed architecture already groups bounded tasks into an agent service
and deterministic orchestration, not five independent applications. Treat
five assistants as five registered capability contracts; separate physical
deployment is a different architectural decision.

The existing test suite deliberately rejects review by a different requester.
This confirms that existing personal recommendations cannot simply be turned
into shared proactive queues without changing the authority contract.
Quality acceptance and capacity/work-order controls already belong to named
humans and deterministic state machines. A new assistant must not bypass them.

Targeted searches of current MVP Python source/tests for `claim_task`,
`agent.task`, `assistant_task`, `task_registry`, `outbox`, `proactive` and
`scheduler` returned no matches. This is bounded negative search evidence,
not a proof that every conceivable background mechanism is absent.

Reflection: reject labels-only delivery, five new application rewrites, a
process-local timer presented as durable orchestration, and model-created
approval/quality/funding state. Preserve existing reviewed workflows and
implement a genuine proposal lifecycle before claiming proactive capability.

#### Parent Synthesis and Disposition

| Material | Disposition | Evidence |
| --- | --- | --- |
| Reuse the current MVP and its SQL/AI adapters | Supported candidate for application-spec planning; delivery target still requires owner direction | C2/C4/C7/C15 |
| Five named reactive/proactive contracts | Required by the user; elaborate existing bounded-task requirements rather than inventing agent authority | C1/C10 |
| Reuse requester-only review without change | Rejected for role-owned proactive queues | C5/C11 |
| Call the current funding-draft mutation path in a background job | Rejected for proposal-only proactive operation | C6 |
| Five independently rewritten applications | Unsupported expansion; capability count does not determine deployment count | C3/C9/C10 |
| Call a deterministic timer/flag a delivered AI assistant | Rejected; distinguish eligibility/routing from real inference | C2/C14 |

#### Cycle Re-entry Evaluation

No further internal source cycle is justified before the owner resolves the
deliverable/workspace direction. The current source gaps and constraints are
supported; new searching cannot supply absent owner authorization. Actual
cloud/SDK feasibility belongs to a confirmed application continuation and
must use current authoritative/tool evidence, not these source observations.

## Evidence Log

| ID | Finding | Source |
| --- | --- | --- |
| C1 | A versioned registry is already required for every AI-assisted task | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:645` |
| C2 | Accepted exercise builds require actual Azure, SQL and registered real AI; historical calls or templates cannot pass | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1081`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1179` |
| C3 | The current architecture expressly distinguishes worker placeholders from deployed MVP feasibility | `docs/adrs/0001-azure-architecture.md:43` |
| C4 | Existing task execution and separate review functions are present | `mvp/zavaforward_mvp/ai_tasks.py:179`, `mvp/zavaforward_mvp/ai_tasks.py:201`, `mvp/zavaforward_mvp/ai_tasks.py:223` |
| C5 | Current task records are requester-owned and do not capture case/source versions; review checks the requester's email | `mvp/zavaforward_mvp/ai_tasks.py:164`, `mvp/zavaforward_mvp/ai_tasks.py:223` |
| C6 | Current funding drafting writes the generated draft and changes the funding status before a separate review | `mvp/zavaforward_mvp/store.py:676` |
| C7 | Recommendation insert/update and audit append share a SQL transaction with optimistic concurrency | `mvp/zavaforward_mvp/sqlstore.py:300` |
| C8 | Existing MVP exposes authenticated priority and output-review routes | `mvp/zavaforward_mvp/server.py:318`, `mvp/zavaforward_mvp/server.py:349` |
| C9 | Agent/orchestrator images are infrastructure parameters with placeholder defaults | `infra/main.bicep:35`, `infra/main.bicep:42` |
| C10 | Bounded orchestration already prohibits model-controlled authority, validates results and requires source-version rechecks on review | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:832` |
| C11 | Existing tests expect another requester to be denied AI review | `mvp/tests/test_ai_tasks.py:125` |
| C12 | Quality acceptance is a separate human, role-constrained state machine with independence checks | `mvp/zavaforward_mvp/quality.py:42`, `mvp/zavaforward_mvp/quality.py:70` |
| C13 | Supplier commitments require evidence and work orders cannot exceed committed capacity | `mvp/zavaforward_mvp/procurement.py:105` |
| C14 | Bounded source search did not find the requested proactive task/claim/outbox registry terms | `mvp/zavaforward_mvp/ai_tasks.py:1`, `mvp/tests/test_ai_tasks.py:1`; targeted search scope and terms recorded in Contrarian |
| C15 | Every accepted application update retains 60,000-home stock and 980-case lineage with actual Azure/SQL/AI evidence | `docs/adrs/0002-pilot-readiness-architecture.md:23` |

No external sources used. No current Azure resource or regional-availability
claim is made in this source analysis.

## Planning Readiness

Research disposition: executed. Source analysis complete.

Planning Readiness: Ready. The latest owner directive explicitly requires
autonomous implementation rather than another planning stop. Existing MVP/
data lineage and consolidated #68 continue in the retained worktree. The
single critique is completed and its compatible corrections incorporated;
automatic implementation is active. This supersedes the initial unanswered
procedural intake, not shared-runtime/spending authority.

## Findings Mapped to Questions

The PRD already has FR-036 registry and bounded orchestration requirements.
It needs an explicit per-assistant contract linking its permitted source
schema, requested and event/scheduled trigger, eligibility/version checks,
output/reviewer, failure/manual handling and measurable acceptance evidence.
ADR 0002 should explain its amendment to the deferred worker topology in ADR
0001 rather than silently claiming those placeholders are deployed.

| Capability | Reactive assistance | Proactive review | Human boundary |
| --- | --- | --- | --- |
| Stock Prioritisation | Explain/reconcile source-bound candidate facts | Conflicting, missing or stale stock facts | Data owners confirm; Assets owns ranking policy; no queue/rank changes |
| Assessment Preparation | Assemble a sourced survey/design preparation pack | Changed, missing or stale assessment evidence | Separate competent assessor/coordinator sign-off |
| Grant and Funding Evidence | Draft source-linked application/claim evidence | Changed terms or missing inputs | Finance validates/submits; no eligibility, totals, approval or funding-state mutation by the assistant |
| Works and Resident Coordination | Draft updates and suggest committed-capacity options | Unaccepted handoffs or missed update commitments | Resident choice and Programme/contract release; no auto-send, booking or instruction |
| Quality Evidence Review | Assemble per-measure evidence for independent review | Missing or conflicting quality evidence | Independent quality acceptance; no hold release, defect closure or technical certification |

All five require typed source/version-bound proposals, role-authorized owned
queues, visible stale/failed/disabled states and a manual route. Reactive and
proactive invocation need shared source/authority semantics but distinct
requester/trigger provenance. Proactive task claims need durable, bounded
retry/deduplication and restart/concurrency evidence, not a process-local lock.
The existing SQL recommendations provide a useful primitive, not a finished
outbox/claim design.

## Alternatives and Unresolved Decisions

* Existing MVP with shared registered tasks and a durable bounded worker is
  the best-supported application candidate, not yet an approved plan.
* Five separate new applications would add unexplained operational complexity
  and conflict with preserving the current MVP lineage.
* A diagram-only update would not implement the assistants; the diagram and
  capstone handoff are already completed in #68.
* A local/container-only image can be an intermediate build but cannot satisfy
  accepted application delivery under CON-009/AC-057.
* The unconfirmed workspace options are a child worktree/stacked PR based on
  #68 or continuing #68. Do not move or commit existing untracked presentation
  outputs as part of making that choice.

## Risks and Acceptance Evidence

Snapshot/version invalidation, role/source projection, shared-queue authority,
SQL claim races, duplicate delivery, crash recovery, retry intent, output
validation and cost/usage limits are material to this extension. Each proposed
assistant needs its own behavior/failure tests; aggregate historic model
feasibility does not establish all five or their proactive mode.

A deployed version needs source/image/config/revision linkage, real SQL
write/read/restart evidence, registered real AI output, provider/usage/source
provenance and explicit failure/manual checks. Comparative task quality,
review/correction effort and business value remain distinct, unmeasured gates.
No user acceptance, deployment, cloud availability, task calibration or benefit
experiment was executed in this research.

## Artifact Self-Check

All three waves and their reflections are recorded. Source claims have stable
evidence IDs and path/line provenance. Negative-search scope is bounded.
No external facts, thresholds, approvals or deployment results were invented.
Only this research artifact and required RPI tracking state were written.
Original case, PRD, ADRs, BRD, owner memory, regulatory snapshots, application,
presentation assets and infrastructure remain untouched.

## Current Decisions and Unresolved Decisions

The five-assistant scope and existing-application build are confirmed by the
latest autonomous-completion directive. Retain the existing worktree/branch/
PR and private/unrelated files. Specific live rollout and incremental allowance
confirmation was unavailable; this blocks actual live acceptance, not local
runtime implementation, validation, container build and source publication.

## Continuation

Active automatic parent executes the approved plan with one completed
critique. No renewed procedural intake or second critique is needed. Shared
runtime rollout/inference remain gated on effective scoped approval and actual
version-linked service evidence; no previous #58 spend override is inherited.
