---
title: Regulatory evaluation gates final-candidate plan critique
description: Single complete implementation-readiness assessment for issue 216
ms.date: 2026-10-16
---

## Metadata

* Task ID: issue-216 / regulatory-eval-gates
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/regulatory-eval-gates-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/regulatory-eval-gates-phase-details.md
* Critique execution status: Complete
* Assessment count: One final-candidate critique, with one complete finding set.

## Inputs and Criterion Boundary

* Caller requirements: synthetic-only, independent per-check citation, refusal,
  hazard, recall and cadence evaluation; honest cards-only shipment recommendation;
  no overall pass. No real model, real staff trial, Azure or private datasets.
* Supplied research:
  .copilot-tracking/research/2026-10-16/regulatory-eval-gates-research.md,
  particularly C1-C7 and its contrarian synthesis.
* Dependencies: #328, #331 and #348 are merged, as supplied. They are not unresolved
  dependencies or requests for additional research.
* Accepted decisions: Juan Manuel Servera is the exercise Legal, Compliance and
  DPO owner only. Citation/refusal targets are provisional pending agreement.
  Recall has no threshold until the baseline and owner review. Human acceptance
  gaps do not block this bounded engineering slice.
* Locked test boundary: no methods removed; at most 45 added methods across the
  owners named in the plan. Existing regulatory suites retain retrieval, state,
  permission and handoff ownership. None of the findings requests expanding that
  budget or changing those owners.
* Narrow code evidence: existing extractive renderer/evaluator and its golden
  report test; server-owned regulatory retrieval; pure rule evaluation; source
  monitor cadence and relevant tests; card HTTP reads; synthetic scale generator.
  ADR 0005's Evaluation section is the supplied C2 acceptance reference.
* Repository case-study, index and memory entry context was consulted under
  repository instructions; no new legal or customer claims were derived from it.
* Assessment boundary: planning credibility for local synthetic implementation,
  not actual implementation correctness, regulatory currentness, operational
  approval, model safety, staff benefit or continuing-stock SQL performance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller constraints; research disposition and C3 | Covered | Merged dependencies, exercise-only authority, no paid inference/private data/cloud work, and explicit unmet acceptance are retained. |
| Citation/refusal; C4/C6; P01-T01 | Partial | Independent support is required, but the oracle boundary and user-visible safety grading are not executable contracts; PC-001. |
| Hazard/recall; C2/C7; P01-T02 | Partial | Critical misses and threshold deferral are correct; seeded coverage across both rule kinds and evidence states is unspecified; PC-002. |
| Cadence; C5/C6; P02-T01 | Partial | Due equality, failed-observation behavior and read-only intent are correct; mixed-source aggregation and read-time failure/clock cases need a contract; PC-003. |
| Cards-only gate; C2 and contrarian synthesis; local acceptance | Covered | Missing human comparison selects cards-only recommendation; structural lookup counts cannot establish benefit. Synthetic development access is distinct from shipment and operational approval. |
| Per-check reporting; provisional targets; no overall pass | Covered with compatibility correction | Numerators, denominators, failures and evidence limits are required; removing the old aggregate field has a known test dependency; PC-005. |
| Validation and negative controls; P03-T01 | Partial | Mutation tests, local SQLite HTTP exercise and component tools are planned. The substantive grader and cadence cases below must be included within existing ownership and budget. |
| Review and delivery; P03-T02 | Partial | One review, privacy-safe identity, PR-only delivery and no merge are correct. Blanket deferral of review findings is unsafe; PC-004. |
| Owner agreement, held-out grading, staff outcomes and continuing stock | Covered as unmet | Explicitly outside local acceptance; no invented agreement, trial results, recall threshold or platform acceptance is requested. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 2 High, 3 Medium, 0 Low.
* Rationale: the scope is appropriately bounded and honest, but five concrete
  implementation-readiness corrections are needed. All are direct planner
  corrections under current user direction. No significant or divergent user
  decision is needed to finalize this synthetic slice.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The grading contract does not pin independent expected behavior or all answer-bearing output

* Related IDs: P01-T01, P01-T02, P03-T01; research C4/C6; citation/refusal acceptance.
* Evidence:
  .copilot-tracking/details/2026-10-16/regulatory-eval-gates-phase-details.md:9-13
  calls the server-selected expected bundle the oracle and names exact
  source/fact support, metadata and unsafe-answer counts.
  Lines 17-22 run actual retrieval, without specifying independently frozen
  expected retrieval selections or expected outcomes.
  src/core/src/zava_forward/core/regulatory_chat.py:140-224 selects the sources,
  conflicts and role-scoped facts that become that bundle.
  src/agents/src/zava_forward/agents/regulatory_chat.py, answer, emits separate
  reply text, quoted sections, safe_next_action, who_decides, kind and citations.
  The existing evaluate in
  src/agents/src/zava_forward/agents/regulatory_eval.py grades quote support and
  response kind, not the full visible safety contract.
* Concern: an oracle independent of output citations can still inherit an
  incorrect source/fact selection from the same retrieval under test. Also, a
  result can retain exact supported sections and the expected kind while its
  reply or safe_next_action asserts compliance, applies future law, resolves a
  conflict or removes human escalation. The proposed checks do not explicitly
  say how those unsafe answers fail. A list of adversarial questions alone does
  not resolve either ambiguity.
* Impact: the principal safety report can score incorrect retrieval or an unsafe
  visible answer as valid, despite correct citation fragments.
* Smallest useful change: define a frozen per-case expectation contract with
  expected kind, permitted/required source and fact fragments and identities,
  metadata, and conflict/refusal/escalation expectations authored independently
  of the run's retrieval. Distinguish that fixture oracle from the actual bundle.
  Define deterministic consistency checks over all answer-bearing fields,
  including reply and safe_next_action. This is bounded extractive-template
  validation, not a request for arbitrary entailment or real-model grading.
* Action owner: planning parent, P01-T01/P01-T02; preserve existing retrieval test
  ownership and reuse its fixtures/assertions where appropriate.
* Exact resolving evidence: phase details name the fixture contract and fields
  graded, plus negative controls that (1) inject an unapproved source/fact into
  retrieval and the resulting answer together, (2) append an unsafe assertion
  only to reply, and (3) replace required conflict escalation with a conclusion.
  Each must fail the relevant check with the frozen case ID while the original
  case remains valid. The controls fit within the existing test budget.
* Decision route: direct planner correction; no user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The 60,000-home baseline lacks a pinned coverage and denominator contract

* Related IDs: P01-T02, P03-T01; research C2/C7; hazard and recall acceptance.
* Evidence:
  .copilot-tracking/details/2026-10-16/regulatory-eval-gates-phase-details.md:20-22
  promises explicit seeded profiles, exact states and independent alert-required
  hazard recall but does not enumerate profiles, rule kinds or coverage units.
  docs/adrs/0005-regulatory-compliance-assistant.md, Evaluation, requires seeded
  hazard, evidence and automated-decision cases.
  src/core/src/zava_forward/core/rule_engine.py:82-178 implements distinct hazard
  and automated-decision branches, including unknown and not-applicable outcomes.
  src/core/src/zava_forward/core/synthetic/scale_fixture.py, homes, supplies
  fictional identities but not those rule-engine evidence contracts.
* Concern: generating 60,000 identities does not determine which evidence cases
  are exercised. A hazard-only or predominantly clear sample could satisfy the
  present task wording while leaving automated-decision and incomplete-evidence
  recall unmeasured. The plan also does not pin whether exact matches and hazard
  misses are counted per home, rule or evidence item.
* Impact: reproducible-looking scale totals can hide missing rule branches or
  dilute a safety failure, without establishing the requested baseline.
* Smallest useful change: specify a deterministic profile table for both rule
  kinds with nonzero expected coverage of their relevant states and boundary
  evidence, fixed seed/as-of/spec inputs, and explicit measurement units.
  Identify each alert-required hazard independently by home/rule/item; count
  omissions as misses rather than dropping them from the denominator. Keep
  hazard misses critical and recall threshold unset. Retain the stateless versus
  SQL/continuing-stock distinction.
* Action owner: planning parent, P01-T02.
* Exact resolving evidence: details contain the profile/count table summing to
  60,000 distinct fictional homes, expected-state/required-hazard definitions and
  report denominators. Planned assertions reconcile coverage and demonstrate
  that removing one required hazard outcome produces its exact failed identity
  and a critical miss irrespective of aggregate state accuracy. No extra test
  ownership or method allowance is required.
* Decision route: direct planner correction; choosing an engineering fixture
  mix is not agreement on an operational recall threshold.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Card freshness aggregation and incomplete monitor storage are undefined

* Related IDs: P02-T01, P03-T01; research C5/C6; stale-source acceptance.
* Evidence:
  .copilot-tracking/details/2026-10-16/regulatory-eval-gates-phase-details.md:27-32
  defines individual-source cadence cases but not the card reduction across
  sources or behavior when monitor tables are absent.
  src/api/src/zava_forward/api/server.py:466-493 returns both card collections
  and per-card version histories.
  src/core/src/zava_forward/core/regulatory_chat.py:140-224 builds chat cards
  separately from those HTTP reads.
  src/core/src/zava_forward/core/source_monitor.py, SourceMonitor.__init__,
  creates monitor storage; due at lines 213-235 checks the latest observation's
  clock before looking for the last successful observation.
  src/core/tests/test_source_monitor.py,
  test_clock_cannot_precede_latest_failed_attempt, protects the failed-attempt
  clock case.
* Concern: a card with one in-cadence and one overdue/unknown source has no
  specified card-level status. A read-only implementation also cannot initialize
  monitor tables by constructing SourceMonitor, so pre-monitor law stores need an
  explicit unknown path. Reading only successful observations can incorrectly
  label a source in-cadence when the newest failed attempt is in the future.
* Impact: collection, history and chat views can disagree or label partially
  unobserved cards as fresh; an ordinary card read can fail on a law store without
  monitor storage.
* Smallest useful change: pin a shared read-model contract for source lookup and
  multi-source card reduction. For example, retain per-source states, expose any
  known overdue source at card level, report unknown when no overdue source is
  known but coverage is incomplete, and use in-cadence only when all required
  sources qualify. Define absent tables/config/observations as unknown without
  writes, and check clock consistency against the latest attempt as well as the
  successful cadence anchor. Apply the same semantics to each returned card
  version and chat card; do not change rule eligibility or suppress alerts.
* Action owner: planning parent, P02-T01.
* Exact resolving evidence: details give the source/card status truth table and
  missing-storage behavior. Existing owner suites cover mixed-source states,
  absent monitor tables without schema mutation, and a future failed attempt
  following an earlier success, with matching HTTP/chat labels and unchanged
  rule/alert behavior within the locked budget.
* Decision route: direct planner correction; no legal activation or user decision.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Review closeout defers every finding without a safety or correctness stop

* Related IDs: P03-T02; local acceptance and delivery gate.
* Evidence:
  .copilot-tracking/details/2026-10-16/regulatory-eval-gates-phase-details.md:44-47
  says review findings route to later work and then directs commit, push and PR.
  It provides no disposition distinction for acceptance failures, safety defects
  or ordinary follow-up suggestions.
* Concern: avoiding repeated reviews does not authorize deferring defects in
  this slice's grading, freshness labels, critical-miss reporting or cards-only
  recommendation. The wording currently allows those findings to remain in a
  purportedly complete implementation.
* Impact: known defects can invalidate the evidence and delivery claim even
  though the mandated independent review occurred.
* Smallest useful change: retain exactly one independent review, but require
  in-scope correctness/safety and acceptance failures to be fixed and covered by
  targeted reruns, or explicitly block readiness and disclose them in the PR.
  Only nonblocking or genuinely out-of-scope improvements route to later work.
  Corrections and test reruns do not require another independent review.
* Action owner: planning parent, P03-T02.
* Exact resolving evidence: phase details state the disposition rule and stop
  condition; the planned delivery record maps every review finding to a fix with
  validation, a justified nonblocking follow-up, or a disclosed readiness blocker.
  No unresolved in-scope blocker is described as completed acceptance.
* Decision route: direct planner correction under existing correctness and
  safety requirements; no additional user approval or review cycle.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Removing the historical aggregate has a concrete unplanned golden-test dependency

* Related IDs: P01-T01, P03-T01; Test Ownership and Targets; research C4.
* Evidence:
  .copilot-tracking/plans/2026-10-16/regulatory-eval-gates-plan.md:89-92
  requires a new canonical report and removes aggregate passed from the historical
  report while preserving its other evidence.
  src/agents/tests/test_regulatory_answers.py:72-76 compares evaluate output
  against src/agents/evals/regulatory_chat_results.json and directly asserts
  first["passed"]. It also retains the 3/3 cited-answer and 10/10 refusal totals.
* Concern: deleting the field from the evaluator/report alone makes the retained
  regression fail. The supplied plan does not say whether the historical
  evaluator remains a compatibility producer or the new schema replaces its
  output; the exact-equality test currently couples those choices.
* Impact: an explicitly required behavior change breaks existing validation or
  tempts retaining the misleading aggregate solely to keep tests green.
* Smallest useful change: state how the legacy evaluator, historical golden
  artifact and existing test migrate together. Replace the aggregate assertion
  with per-check assertions and preserve the historical cases, counts and
  structural comparison evidence. Define which runner regenerates which report.
  Do not remove a method or reclassify historical results as new semantic proof.
* Action owner: planning parent, P01-T01/P03-T01; agents remains the test owner.
* Exact resolving evidence: details explicitly name the existing golden test,
  evaluator and report as coordinated edits, identify report regeneration
  commands, and require that retained method to pass without an aggregate
  boolean while preserving the historical evidence and deterministic equality.
* Decision route: direct planner correction; no method-budget increase or user
  decision.

## Strengths and Residual Risk

* The plan correctly rejects structural lookup counts as staff-benefit evidence
  and selects a cards-only recommendation without a qualifying human comparison.
  Cards still have their own approval gates; this is not operational permission.
* Provisional citation/refusal targets are labelled pending owner agreement;
  recall remains unthresholded before its baseline and owner review. There is no
  request to invent agreement or a single overall pass.
* Exact-fragment grading, mutation controls, critical hazard misses, due-boundary
  labels and last-success cadence are appropriate bounded engineering goals.
* No new model, staff trial, Azure verification, private dataset access, broad
  research or additional agent is necessary to resolve this finding set.
* Held-out legal grading, real staff precision/acknowledgement/comprehension,
  continuing-stock integration and live platform performance remain explicitly
  unmet and outside the evidence this slice can establish.

## Questions or Blocking Evidence Gaps

* No user question is required. The evidence supports a Revise verdict, not a
  Blocked assessment. The planning parent can resolve all five findings directly.
* Actual threshold agreement and human comparative evidence remain later gates,
  not missing facts to manufacture during planning or prerequisites for this
  critique.

## Limitations

* No issue/PR network lookup, external research, legal-source check, runtime test,
  real dataset access or implementation was performed. Dependency status and
  owner direction are accepted as supplied.
* Narrow code reads establish existing contracts and dependencies, not new
  evaluation results. Planned outcomes have not been observed.
* Only this critique artifact is written. Plan, details, research, test owners
  and the 45-method ceiling remain unchanged by this assessment.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: pin the frozen expected-case and full visible-answer
  grading contract in P01 details, then dispose PC-002 through PC-005 in the same
  planning revision before implementation.
* User response required: No.
* Finalization: return this complete set to the active parent. Revise and record
  disposition without commissioning another plan critique.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/regulatory-eval-gates-plan.md](.copilot-tracking/plans/2026-10-16/regulatory-eval-gates-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-16/regulatory-eval-gates-phase-details.md](.copilot-tracking/details/2026-10-16/regulatory-eval-gates-phase-details.md) | Assessed task completion contracts |
| [.copilot-tracking/research/2026-10-16/regulatory-eval-gates-research.md](.copilot-tracking/research/2026-10-16/regulatory-eval-gates-research.md) | Supplied evidence and scope boundary |
| [.copilot-tracking/plans/2026-10-16/regulatory-eval-gates-critique.md](.copilot-tracking/plans/2026-10-16/regulatory-eval-gates-critique.md) | This single complete finding set |

## Next Steps

The active planning parent should resolve PC-001 through PC-005, record each
disposition, and finalize the plan without another critique. Preserve the
synthetic-only scope, existing test ownership, maximum 45 additions and no
removals. No user action is required.
