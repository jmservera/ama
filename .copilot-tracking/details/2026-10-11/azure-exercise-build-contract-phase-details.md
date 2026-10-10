<!-- markdownlint-disable-file -->
# RPI Phase Details: Azure exercise build contract and decision-model learning

## Metadata

* Task ID: AMA-AZURE-EXERCISE-20261011
* Task slug: azure-exercise-build-contract
* Related plan: .copilot-tracking/plans/2026-10-11/azure-exercise-build-contract-plan.md
* Evidence: Current user direction, BRD/PRD/addendum, decision-model synthesis,
  earlier session review and PR #58 pinned to 5136f192d583a5bf53adeeec4b0f21369b005c9d.
* This plan is documentation-only. Canonical amendments belong to /rpi-implement;
  the planning phase owns only plan, details and one critique.
* Readiness: Ready after one final critique and planner-owned dispositions;
  task status below refers to future implementation, not planning completion.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Extract learning and freeze delta | Pending | P01-T01 |
| P02 | Update canonical requirements | Pending | P02-T01, P02-T02 |
| P03 | Validate and publish handoff | Pending | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Extract learning and freeze requirements delta

### Context

The earlier review established adequate fictional requirements but accepted
local SQLite continuation. The owner now explicitly requires real AI, real SQL
and Azure for every next application exercise build, not every unit test.
Current #58 reports actual Azure SQL/deployment, Decision 1 selection and
GPT-4.1-mini generation on retained data; old access failures are historical.

### Boundaries

* Read current pinned PR source/results read-only.
* Do not retrieve secrets, execute models, deploy, merge or import implementation.
* Treat the parallel experiment as user-confirmed, without assumed results.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Classify PR #58 decision-model and build evidence

#### Intent

Prepare source-pinned findings for canonical requirements updates.

#### Likely Targets

* Pinned PR #58 mvp/README.md, Current continuing MVP; acceptance Blocking
  Work; changes deployment/activation sections; decision-model synthesis.
* Pinned .copilot-tracking/mve/2026-10-10/decision-model-value/mve-plan.md.
* Existing docs/ideas/typesafe-system-one-agent-fit.md.

#### Dependencies

* None; current GitHub source read is sufficient for documentation planning.

#### Validation Expectations

* Distinguish provider eligibility, deployment, successful inference, schema
  conformance, quality/latency/cost and incremental benefits.
* Check SQL and Azure evidence separately from local SQLite/MSSQL CI.
* No undocumented experiment outcome or unsupported infeasibility conclusion.

#### Completion Evidence

* Verified register below supplies implementation evidence; transfer concise
  findings to existing syntheses without importing #58 implementation.

#### Unresolved Items

* Comparative execution/benefits and human participants remain unverified.
  Proposed protocol is located; missing outcomes do not block documentation.

#### Verified Learning Register

Each PR observation is pinned to 5136f192d583a5bf53adeeec4b0f21369b005c9d.
These are inspected source/report results, not live probes rerun by this planner.

| Learning | Source section | Classification and consequence |
| --- | --- | --- |
| Azure SQL-backed deployed continuing MVP retains 60,000 stock rows and 980 programme cases | mvp/README.md, Current continuing MVP | Recorded actual deployment; small fixtures remain tests, no guessed stock-to-case links |
| Decision 1 selected a source-bound EPC candidate with probabilities, model/version/usage and Not reviewed | README and synthesis Observed Feasibility, Not Proven Incremental Value | Narrow technical feasibility observed; no general calibration, task accuracy or benefit established |
| GPT-4.1-mini produced a citation-verified catch-up summary | Same sources | Real generative integration observed; failed earlier verification remains historical |
| Generic cognitive-services host failed; Foundry services host with /providers/microsoft/v1/systemone succeeded | README, Current continuing MVP | Provider endpoint/auth conformance matters; authentication bug is not proof of model infeasibility |
| Optional confidence validates separately from option probabilities | Same source | Require finite schema-valid responses and probability checks; optional confidence is not calibrated probability threshold |
| Later work-order controls are source-tested, not necessarily in revision ca-properwarm-mvp--0000018 | README, Work-order evidence version controls | Tie source/image/deployment/runtime evidence; no full acceptance claim from later source tests |
| Prior inference cap removed by owner for this rebuild; input/task/source/reservation/usage guards remain | README and acceptance Blocking Work | Record scoped effective override; no reimposed historical cap or implied future unlimited spend |
| Held-out calibration/paired human benefit remain incomplete | Synthesis and acceptance Blocking Work | Feasible does not mean better/cheaper; do not delete or relabel failed historical result rows |
| Deployed support adapter is binary; proposed target is three-class macro-F1 | mve-plan.md, Dataset, Controls and Analysis | Separate frozen three-option shadow test or Not evaluated; binary labels cannot establish three-class success |

Official corroboration retrieved 2026-10-11:
https://learn.microsoft.com/en-us/azure/foundry/foundry-models/how-to/use-foundry-models-microsoft-decision.
The typed text/JSON API provides choices/probabilities, not generated rationale.
Official API documentation does not validate app calibration, costs or benefits.

#### Parallel Experiment Intake

* User confirms parallel work; available protocol remains proposed. No execution
  approval, real participants or measured result is inferred from the design.
* Reuse four arms R rules/manual, D Decision/templates, A generative agent,
  H agent with Decision tools. A versus D is narrow replacement; H versus A
  measures complementarity. Do not treat all agents as replaced by a scorer.
* Protocol uses 120 grouped families, 30 tuning/30 calibration/60 held-out,
  declared 720 dispositions, two human adjudicators and twelve human pack blocks.
  Preserve family splits, independent review and complete preparation/correction
  effort; synthetic role-agent labels/timings are not human truth.
* Intake records protocol/split/source hashes, frozen task/question/prompt/
  model/deployment/schema/threshold versions, denominators/exclusions, repeated
  trials, failures/fallbacks, quality/critical errors, coverage/calibration,
  paired full-pack effort, cost/latency and uncertainty.
* Preserve existing PRD 95% disposition, 98% selection, 50% coverage,
  F1 0.90 screening and 15% paired effort targets as unproved targets.
  Additional experimental comparative margins remain proposed until frozen.
* Negative results can reject a narrow model task; insufficient people,
  labels/schema or precision remain Inconclusive or Not evaluated. Results
  do not waive mandatory whole-app real AI/SQL/Azure or human approval.
* No duplicate experiment implementation or participant recruitment. Shared
  application platform/control work proceeds independently where dependencies
  permit; value claims and adoption decisions require reviewed results.

<!-- rpi:phase id=P02 -->
## P02: Update canonical requirements and supporting evidence

### Intent

Make the prospective platform/AI baseline unambiguous without erasing history.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Update BRD, PRD and addendum

#### Context

PRD v0.12.0 and EXA-012 allow local durable state; DD-007 is optional scoring
while EXA-016 requires actual Decision 1. Resolve mandatory app AI versus
conditional task placement without presuming measured decision-model value.
Use actual Azure SQL as the existing realization; no production option winner
or costly new topology is implied by the exercise baseline.

#### Likely Targets

* docs/brds/agentic-retrofit-programme-brd.md
* docs/prds/proper-warm-retrofit-programme-demonstrator.md
* docs/case_study_48_addendum.md

#### Dependencies

* P01-T01.

#### Validation Expectations

* Real AI/SQL/Azure are required for accepted future builds.
* Local development and deterministic/manual recovery remain supported but
  cannot satisfy real-platform/model acceptance.
* Preserve effective budget, data and no-unauthorised-action safeguards. Old
  USD450/360/405 thresholds and #58's rebuild-specific override are distinct;
  do not reimpose the cap on #58 or authorize all future spending.
* Keep v0.12.0/2026-10-10 acceptance as history; new candidate is not
  automatically owner-accepted, independently quality-passed or production-approved.

#### Completion Evidence

* BRD v0.16.0 / PRD v0.13.0 candidate amendments dated 2026-10-11,
  aligned metadata, counts/traceability and dated addendum direction.

#### Unresolved Items

* None for document amendment. Future build authorization/budget and benefit
  evidence remain independent execution gates.

#### Canonical Amendment Map

| Target section | Amendment |
| --- | --- |
| BRD Status/Executive/Synthetic demonstrator Scope | Mandatory real AI/SQL/Azure in all subsequent AMA prototypes/PoCs/MVPs, original generated-stock lineage, no production platform/benefit approval inferred |
| BRD Digital Foundation/Authority, Imposed Constraints and Validation | At most new CON-007 and AC-086, connected to existing state/assistance requirements, relevant goals and human authority rules; if IDs now exist, amend rather than duplicate |
| BRD Benefits Register/Assumptions/Source Review | Observed narrow Decision1 feasibility, unproved quality/benefits, versioned experiment intake and scoped spend override |
| PRD Exercise Baseline Authority, Components/Proposed Azure, DD-001/007/008 | Supersede local-only delivery prospectively; actual Azure SQL is deployed state authority; task scoring optional does not mean whole-app AI optional |
| PRD NFR-002/003/004/006/009/011 and Exercise Acceptance Contract | Distinct deployed workflow, durability, enabled inference and cost/identity evidence; local test/performance passes cannot become deployed proof |
| PRD Constraints/AC/Traceability | At most CON-009 and AC-057 traced to existing state/AI FRs/goals, preserving all existing 46 FRs/56 AC IDs and safety/consent/finance gates |
| PRD Model Evaluation, Release Framing, Risks, OQ-016 | Current real selection is feasible; support/calibration/benefit open. Four-arm intake and three-class mismatch explicit; negative task results cannot waive mandatory platform/AI |
| PRD Sign-Off/Metadata | New candidate version needs fresh review/acceptance. Annotate historical blockers with dated current status, never overwrite historical Pass/Fail/Not run |
| Addendum, dated prospective 2026-10-11 direction | Earlier EXA-012 local option and EXA-016 unconditional task interpretation superseded where conflicting; preserve earlier dated register; annotate new current evidence/scoped budget history |

* Clarify PRD FR-044, SA-004 and Components "optional System One", related
  BRD optional AI wording and RULE-018 context in place: real AI is required
  in the accepted deployed app, while invoking assistance for a particular
  record and access/manual draft completion never depend on model availability.
  No FR additions or renumbering.
* Use one term in BRD, PRD and addendum: "accepted application exercise build"
  means every subsequent delivered AMA prototype/PoC/MVP, including updates to
  this application. Docs-only work, unit/CI tests and non-delivery development
  checks may use SQLite/mocks, but never satisfy delivery acceptance. This is
  application-level acceptance, not a new paid AI call in every atomic module.

#### Required Real-Platform Acceptance Shape

1. Authorized Azure app browser/API core path plus immutable source/image/
   revision/config reference and explicit accessible errors/manual fallback.
2. API state/audit writes to actual Azure SQL under verified workload identity;
   before/after independent SQL checks prove acknowledgement and persistence
   after an app restart. Local SQLite/MSSQL CI is separate development proof.
3. Current-build application invokes actual enabled AI on permitted generated
   sources; retain task/source/model/provider/input/usage/output outcome,
   citations and Not reviewed authority. Template/mock/prior unrelated call
   is not current-build proof.
   At least one in-scope exercised task must use a real generative or Decision
   model selected for that task. Rejecting a narrow Decision task retains
   rules/manual handling there, not an entirely disabled-AI delivery.
4. Reused unchanged infrastructure is allowed: prove changed-build connection
   and real-service workflow, not gratuitous fresh deployments. Preserve
   existing full generated data and no guessed entity links.
5. Effective per-build budget/authorization, source/task/input bounds and
   cost reservations/telemetry documented separately from cap override.
   No credentials or raw generated resident records in evidence documents.
   If effective budget or authorization prevents obtaining real-service
   evidence, mark acceptance Blocked or Not run; no mock/local/template
   substitution or silent pause/cap override. #58's scoped owner override
   remains valid for that rebuild; it is not a general future budget decision.

#### Branch Boundary

Use the clean existing topic branch. #58 supplies evidence, not a merge/base
dependency or authorization to import implementation. Integrate targeted
requirements wording only; preserve any later concurrent canonical edits.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Integrate learning and experiment handoff

#### Intent

Reuse existing syntheses; give the experiment a versioned evidence intake.

#### Likely Targets

* docs/ideas/typesafe-system-one-agent-fit.md
* docs/reference/research/ux/prototype-learnings-and-simplicity-review.md
* docs/reference/README.md
* docs/reference/log.md
* docs/reference/research/gap-analysis-next-build.md
* docs/adrs/0001-azure-architecture.md
* docs/adrs/0002-pilot-readiness-architecture.md

#### Dependencies

* P01-T01; P02-T01 supplies the current requirements references.

#### Validation Expectations

* Findings remain observed, blocked or unknown with pinned source references.
* No presumption of a positive benefit or blanket decision-model infeasibility.
* Index and append-only log stay consistent; original case and owner memory unchanged.
* Add dated ADR applicability notes only: historical options remain, local-only
  future acceptance is superseded. Do not create a new production ADR.
* Align existing next-build synthesis with mandatory baseline. Use pinned
  GitHub experiment/source URLs; no local links to absent branch-only artifacts.

#### Completion Evidence

* Indexed learning/requirement links and explicit experiment adoption gates.

#### Unresolved Items

* Protocol located on #58; execution results unverified. Apply intake above,
  not invented results or a new MVE plan.

<!-- rpi:phase id=P03 -->
## P03: Validate and publish documentation handoff

<!-- rpi:task id=P03-T01 -->
### P03-T01: Validate traceability and deliver through a PR

#### Intent

Publish the documentation delta, not an executed Azure build.

#### Likely Targets

* All P02 documentation targets and Git diff.

#### Dependencies

* P02-T01 and P02-T02.

#### Validation Expectations

* Check Markdown, relative links, requirement IDs/counts/version metadata and
  scope conflicts. No app tests or paid calls for documentation-only changes.
* Commit privacy-safe identity and required trailers; push topic and use PR tool.
* Use the locked contract in the plan: zero code/test/tool/dependency additions,
  ten canonical documents, zero document removals and at most two added
  requirement rows per requirements document.
* Check every listed active local/optional-model/budget/fixture clause is
  superseded or unmistakably historical. Update requirement coverage/counts
  and all affected metadata/index/review-state references.
* Across the ten canonical files, sweep local-only/local durable/SQLite,
  optional AI/assistance/scoring/System One, fixture/MVP, not deployed,
  blocked inference, 450/360/405 and EXA-012/016. Record relevant hit
  dispositions in the changes record: amended active requirement, permitted
  manual/per-task handling, test-only path or dated historical evidence.
  Explicitly check FR-044, SA-004, Components and BRD RULE-018 context.
* Assert unique canonical counts before/after: PRD FR 46 unchanged,
  AC 56 to 57, CON 8 to 9; BRD FR 44 unchanged, AC 85 to 86,
  CON 6 to 7. Match amended traceability/coverage/version/ms.date summaries.
* Original case, snapshots, owner memory and prior log entries unchanged.
  No application suite/cloud/model call for documentation-only work.

#### Completion Evidence

* Changes record and published documentation PR with provenance/limitations.

#### Unresolved Items

* None; single final critique is disposed in the plan. Planning publication contains
  only plan/details/critique; implementation publishes canonical amendments.
