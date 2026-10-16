---
title: RPI Plan Critique - Rule engine gating regressions
description: One bounded final-candidate critique for issue 329
ms.date: 2026-10-16
---

## Metadata

* Task ID: 329
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/rule-engine-gating-329-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/rule-engine-gating-329-phase-details.md
* Critique execution status: Complete
* Critique count: One final-candidate assessment; no implementation or plan edits.

## Inputs and Criterion Boundary

* Caller requirements: test consultation/historical gating and cross-episode
  attention limits; fix only demonstrated defects; mutations must produce
  intended assertion failures. Use local pip-venv unit, ruff and mypy validation,
  with source under src/ and tests outside installed packages.
* Primary inputs: the plan and phase-details paths above.
* Bounded implementation evidence: src/core/src/zava_forward/core/rule_engine.py,
  src/core/tests/test_rule_engine.py and src/core/README.md.
* Project-context orientation: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. These do not establish runtime acceptance.
* Decisions assessed: retain production behavior unless a red regression proves
  a defect; at most six new focused methods; tighten the existing source test;
  one critique and one implementation review; references-only PR.
* Dependencies assessed: installed core/dev tools and this critique before
  P01-T01; P01-T01 before validation/documentation/delivery in P01-T02.
* Acceptance assessed: exact source labels, preserved citations, no prohibited
  publications, distinct episodes, persisted evaluations/publication counts,
  boundary behavior, independent throttle keys, breach bypass and targeted
  mutation rejection.
* Exclusions: no private dataset, protected configuration, issue-cache access,
  external research, test execution, deployment or operational/legal acceptance.
  The issue body and ADR are referenced by the candidate but were not
  independently retrieved; caller direction supplies the assessment contract.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| P01-T01: consultation/historical/future gating | Covered | Exact not-applicable assertions replace the permissive existing assertion; eligible cards, retained citation status and raw alert-row absence are required. |
| P01-T01: unknown-source negative controls | Covered | Partial, unreviewed, stale and missing citations remain exactly unknown. Existing active-source tests provide attention/breach positive controls. |
| P01-T01: distinct episodes | Covered | Another case changes the episode's case dimension; changing awareness/due time on the same case changes its due-time dimension. Checkpoint/check IDs and relevant revisions/due times must be asserted. |
| P01-T01: shared publication window | Covered | Same home/card/step/item is held constant for suppression; a long clock keeps attempts in attention beyond 24 hours. |
| P01-T01: boundary and durable evidence | Covered | Just-before suppression and exact-boundary publication are explicit. Plan acceptance requires persisted publication counts; details require every check/checkpoint and forced schedule/revision freshness. |
| P01-T01: isolation and escalation controls | Covered | Independent home/card/step/item keys and cross-case breach bypass are explicit positive controls against over-broad suppression. |
| P01-T02: mutation sensitivity | Covered | Consultation and historical guards are mutated independently; shared throttling is disabled while episode deduplication remains. Intended assertion failures and exact failed tests must be recorded. |
| P01-T02: validation and production-change gate | Covered | Baseline first, minimal demonstrated fixes only, full core unit/ruff/format/mypy validation in an installed pip environment; related downstream unit suites if behavior changes. |
| P01-T02: delivery and evidence boundaries | Covered | README/index/log, changes/review evidence, authenticated privacy-safe commit identity, non-forced push and references-only PR are planned; hosted and human acceptance remain separate. |

## Verdict

* Verdict: Pass
* Severity counts: Critical 0; High 0; Medium 0; Low 0.
* Rationale: The final candidate explicitly separates shared throttling from
  episode deduplication and checkpoint replay. Its acceptance criteria and
  phase details jointly require durable publication evidence and meaningful
  boundary, negative and positive controls. No evidence-backed substantive
  correction is needed before implementation.

## Findings

* None.

## Strengths and Residual Risk

* rule_engine.py defines the shared key as home/card/step/item, while the episode
  key includes case/card/version/step/item/due time. Both planned episode
  variations therefore exercise real differences without weakening the shared
  key. Distinct check IDs alone would not prove this; the candidate also calls
  for case/due-time changes and relevant revision/due-time assertions.
* The schedule checkpoint key has minute granularity, whereas ordinary
  data-change retries reuse checkpoints until revision or contract changes.
  The explicit freshness requirement is important: implementation must select
  distinct schedule minutes or revisions for the boundary attempts.
* The open-alert projection can replace or hide publications. The plan's
  persisted-count acceptance criterion and the details' raw-row gating checks
  avoid mistaking a filtered view for absence of publication.
* Existing test_five_results_exact_thresholds_and_citations exercises executable
  active sources. Independent-key publication and breach bypass complement
  suppression assertions, so an implementation that simply never publishes
  cannot satisfy the planned suite.
* Mutation evidence is limited to regression sensitivity. The candidate
  explicitly leaves actual human approval, source currentness, live platforms
  and operational acceptance outside this synthetic slice.

## Questions or Blocking Evidence Gaps

* None within the supplied planning boundary. No user decision is required.

## Limitations

* This is a credibility assessment of the specified candidate, not verification
  of tests that have yet to be implemented. Actual fixture validity, SQL counts,
  boundary results and mutation AssertionError outcomes remain implementation
  evidence to be recorded under P01-T02.
* No commands installing packages, running tests or linters, changing source,
  editing planning inputs, or accessing external systems were performed.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent, then implementing agent.
* Smallest next action: Record this passing critique and proceed to P01-T01
  without another critique pass.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/rule-engine-gating-329-plan.md](.copilot-tracking/plans/2026-10-16/rule-engine-gating-329-plan.md) | Final-candidate plan assessed without edits |
| [.copilot-tracking/details/2026-10-16/rule-engine-gating-329-phase-details.md](.copilot-tracking/details/2026-10-16/rule-engine-gating-329-phase-details.md) | Bounded test and validation details |
| [.copilot-tracking/reviews/plans/2026-10-16/rule-engine-gating-329-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-16/rule-engine-gating-329-plan-critique.md) | Complete single-pass critique |

## Next Steps

The active planning parent can finalize the passing critique disposition and
hand P01-T01 to implementation. No user action or additional critique is
required.
