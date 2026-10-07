<!-- markdownlint-disable-file -->
# Review: Proper Warm Architecture and PoC

## Scope and Evidence

* Task ID: 4aaf9ee3-da69-4ebb-812a-edccc5637af7
* Review date: 2026-10-07
* Review scope: full bounded task P01-P04, AC-P01-AC-P07.
* Assessed boundary: synthetic local application and documented provisional
  architecture; not full PRD MVP, live AI, operational approval or cloud release.
* Plan: .copilot-tracking/plans/2026-10-07/retrofit-application-poc-plan.md
* Phase details: .copilot-tracking/details/2026-10-07/retrofit-application-poc-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-07/retrofit-application-poc-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-07/retrofit-application-poc-changes.md
* Research: .copilot-tracking/research/2026-10-07/retrofit-application-poc-research.md
* Other evidence: application source/tests/manifest, architecture/resource
  ledger, real browser/runtime/restart results and published PR24.

## Opening Review State

* Interpreted review goal: assess the implemented bounded acceptance once and
  route defects or residual work without modifying implementation.
* Evidence readiness: plan markers and phase statuses completed, changes record
  reconciled, fixed scope and measured evidence available.
* Acceptance basis: AC-P01-AC-P07, frozen authority/stage/replay contracts,
  PC-001-PC-009 dispositions and confirmed synthetic local delivery.
* First comparison boundary: domain/store and contract tests against authority,
  gate invalidation, seed atomicity and replay requirements.
* Active read-only boundaries: only this canonical Review record may change
  during assessment; source and prior phase artefacts remain read-only.
* Initial blockers: none for bounded assessment. Hosted rubric is pending;
  local/hosted application validate checks passed. Operational approvals are
  intentionally ungranted and do not block this synthetic acceptance boundary.

## Execution Status

* Execution status: Complete.
* Review execution evidence: one assessment of P01-P04, AC-P01-AC-P07,
  code/contract/validation and release boundaries. No repeated critique or
  correction/review loop. One reproduced defect is routed to later work.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01/P01-T01 | Verified Application | Reconciled | 39 contract tests pass; later accepted-quality replacement uncovered by Review |
| P02/P02-T01 | Workbench Delivered, Verified Application | Reconciled | exact-envelope UI, visible errors and real mobile/browser evidence |
| P03/P03-T01 | Architecture and Container Sources, Created Resources | Reconciled | local vs proposed architecture and real inventory distinguishable |
| P04/P04-T01 | Verified Application | Reconciled | browser, health, restart and scoped performance observed |
| P04/P04-T02 | Publication and Review Handoff | Reconciled | PR24 open, no merge; hosted validate passed, rubric pending |
| Follow-Up Items | release boundaries and PR follow-ups | Reconciled | identity/model/human ratification excluded from active acceptance |

The plan's final Handoff paragraph retains its historical planning-to-Implement
wording. Current markers, phase status, changes handoff and state unambiguously
record completed implementation and this Review; it is not current routing.

## Completed Work Assessment

| Acceptance | Files / evidence | Assessment |
| --- | --- | --- |
| AC-P01 | apps/proper-warm/src/domain.mjs, store.mjs, tests/domain.test.mjs, tests/api.test.mjs | roles, closed payloads, version/replay and nine workflows evidenced; RV-001 covers missing post-completion quality replacement invariant |
| AC-P02 | tests/helpers.mjs happyJourney, domain tests | full gated candidate-to-handover journey passed; negative fixtures stay blocked; RV-001 limits continued completion validity |
| AC-P03 | store fault/reopen tests, resource ledger restart observation | transaction rollback, atomic seed and persistent restart demonstrated |
| AC-P04 | public/app.js, scripts/verify-browser.py, changes/browser evidence | sourced action, hazard denial, draft/error/task, exact lost-response replay, export/filter/drilldown/reflow observed |
| AC-P05 | src/assistant.mjs, evaluation, tests/assistant.test.mjs | deterministic citation/schema/prohibited-effect/fallback checks; no real-model claim |
| AC-P06 | docs/architecture/proper-warm-resources.md, app README | all created local objects inventoried; zero Azure/M365 resources; safe scoped teardown; generator only dry-run |
| AC-P07 | docs/architecture/proper-warm-poc.md | alternatives, authority, threats, failure domains, scale/migration, cost formula and all twenty rubric gaps disclosed |

## Implementation-Time Plan and Detail Update Assessment

| Area | Update and reason | Trigger / user direction | Assessment |
| --- | --- | --- | --- |
| P01-P04 | independent P03 docs/container phase, integration P04 | disjoint worker boundaries | preserved scope and acceptance; no material revision requiring second critique |
| P04-T02 | publication/review-ready handoff, Review belongs to next lifecycle phase | circular dependency removed | one critique/one Review preserved |
| P02 | Clawpilot theme, sidebar min-width and real reflow check | activated artifact rules and browser overflow observation | appearance fix, no authority/behavior change |
| P01/P04 | Fetch Metadata restriction to POST, retained Host/Origin controls | initial browser canvas GET was rejected | navigation corrected without allowing cross-site writes; API regression passed |
| P04 | hidden retained JSON assertion uses textContent | browser assertion targeted hidden details | checks the required exact intent rather than visibility proxy |
| Documentation | generator path and dry-run evidence | owner's support/synthetic-data message and PR request | no import, approval inference, private answer-key publication or existing-data overwrite |
| Publication | merge updated main, preserve both upstream log entries | base moved during implementation | non-rewriting branch update, application code unaffected |

## Critique and Material Revision Assessment

* PC-001-PC-009 each has a recorded compatible disposition in plan/details.
  Role/stage matrices, independent review, invalidation, replay ordering,
  closed API shape, atomic seed, scenario mapping, no-access exclusions,
  assistant fallback and resource ownership are represented in implementation.
* No confirmed user decision was overridden. Local-first synthetic scope
  remains consistent with permission, which did not mandate cloud creation.
* One final-candidate critique ran; no second critique. Review is distinct
  from factual PR-description summaries, which did not certify correctness.
* RV-001 is a remaining implementation defect, not a planner decision gap or
  justification for another critique or Review in this task.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner / next action | Route |
| --- | --- | --- | --- |
| Entra identity and managed relational store | synthetic loopback API and single local SQLite process only | platform owner; ratify authority, then implement identity/store contracts before ingress | distinct follow-up Research |
| Real-model evaluation | deterministic assistant deliberately has no model calls | AI lead; approved corpus/task evaluation and release thresholds | distinct follow-up Research |
| Operating-model/legal/control ratification | no genuine company authority, professional approval or validated threshold | owner and named human professionals; prepare evidence/decision pack, preserve unchecked approvals | distinct follow-up Research |
| Generated-pack import/quarantine | analytical statuses do not establish current operational approval | data owner; define source/lineage/conflict/quarantine mapping before loading cases | distinct follow-up Research |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Accepted quality replacement leaves a stale handed-over stage

* Related scope: P01/P01-T01, AC-P01 and AC-P02; continuing validity and
  quality/handover independence.
* Evidence: apps/proper-warm/src/domain.mjs record_quality clears
  facts.handover for both outcomes, but only a returned outcome changes stage.
  portfolio counts accepted handovers from stage alone.
* Reproduction: createStore(:memory:), happyJourney, then quality_reviewer
  record_quality with accepted, new evidenceId EX-REVIEW-NEW-QUALITY and current
  designVersion1. Observed stage handed_over, handover null and blocker
  HANDOVER_ACCEPTANCE. No source, real container or resident data was changed.
* Impact: continued accepted-handover count can include a case whose separate
  handover acceptance was invalidated. The stage also prevents accept_handover,
  which requires quality_accepted, without an additional controlled return.
* Destination: later rpi-implement under current approved direction, or the
  first user-selected automatic child task.
* Smallest useful next action: downgrade an already handed-over case to
  quality_accepted when new accepted quality invalidates its handover (or
  require explicit return before replacing evidence); preserve independent
  reacceptance and audit. Add a post-handover replacement regression covering
  stage, handover blocker and portfolio count. No correction performed here.

## Defects

* RV-001: one Medium domain/completion validity defect, reproduced in memory.
  Existing tests do not cover this accepted replacement path.

## Routed Findings

| Finding | Destination | Owner / next action | Reason |
| --- | --- | --- | --- |
| RV-001 | later rpi-implement / selected child loop | backend implementer; restore stage/acceptance consistency and regression | bounded defect, accepted direction unchanged |

Later implementation does not require another Review of this completed task.

## Residual Work

* Published hosted rubric score was pending at observation. Application
  validate and repository validate were SUCCESS. Rubric output is a separate
  capstone evidence assessment, not proof of production acceptance.
* Real identity, managed persistence, approved imports, model evaluation and
  human ratification remain distinct follow-ups, not added active scope.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining active implementation: none within the completed pass.
* Open defect: RV-001 routed, not resolved; do not claim conformant acceptance.
* Operational release remains prohibited by documented identity/privacy/store,
  live-model/evidence and human approval gaps.

## Validation Evidence

| Check | Status | Scope and result |
| --- | --- | --- |
| npm --prefix apps/proper-warm test | Passed | final 39 tests, including cross-site GET; not RV-001 path |
| simulator evaluation | Passed | five deterministic fixtures; not real-model quality |
| actual container health | Passed | latest GET health reports ready/writable/synthetic |
| runtime/browser/restart/performance | Passed | recorded executed checks; localhost p95 28.55ms, no production-load claim |
| generator --seed1341953496 --dry-run | Passed | 980 candidates, 13 observed tables, 23528 rows, zero errors; no files written |
| documentation links / git diff --check | Passed | 126 links before publication; whitespace clean |
| gh pr checks24 | Passed / Pending CI | both validate checks SUCCESS; rubric agent running, rubric/score pending |
| RV-001 in-memory command reproduction | Failed invariant | stage handed_over with handover null and HANDOVER_ACCEPTANCE blocker |
| live AI, cloud availability, operational human approval | Skipped | deliberately excluded from scope; no certification claimed |

## Outcome

* Outcome: Defects found.
* Outcome rationale: bounded PoC architecture, runnable runtime and publication
  delivered; one reproduced completion-validity defect remains routed. Passing
  tests and CI do not establish conformance of the missing invariant. No
  production, full-MVP or agentic-autonomy acceptance is claimed.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | later rpi-implement / first ranked child | RV-001 domain invariant and test |
| Decision gap or invalid assumption | none in active scope | approved local/simulator boundary preserved |
| Material evidence gap | none blocking bounded Review | operational evidence is explicitly outside scope |
| Non-blocking residual work | distinct follow-up Research | imports, identity/store, model and human ratification |

* Execution status: Complete.
* Outcome: Defects found, one Medium unresolved.
* Validation coverage: fixed local scope executed; missing accepted-quality
  replacement exposed by this Review. Hosted rubric pending.
* Blockers: none to Review completion; RV-001 must not be represented as closed.
