---
title: RPI Plan Critique - Scoped consultation hold
description: Independent final-candidate planning assessment for task 92
ms.date: 2026-10-18
---

## Metadata

* Task ID: 92.
* Slug: issue-92-scoped-consultation-hold.
* Critique date: 2026-10-18.
* Plan: .copilot-tracking/plans/2026-10-18/issue-92-scoped-consultation-hold-plan.md.
* Phase details: .copilot-tracking/details/2026-10-18/issue-92-scoped-consultation-hold-phase-details.md.
* Critique execution status: Complete.
* Verdict: Revise.
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* Execution boundary: one independent final-candidate critique, not implementation
  or implementation Review. No delegation or second critique.

## Inputs and Criterion Boundary

* Exact owner direction: "Limit the hold to consultation-dependent actions; preserve unrelated service work".
* Read the supplied plan, phase details and research:
  .copilot-tracking/research/2026-10-18/issue-92-scoped-consultation-hold-research.md.
  Assessed research C1-C8 against the relevant procurement, building and advancement
  source and existing consultation, building and procurement HTTP tests.
* Required repository context considered: docs/case_study_48_original.md,
  the opening and exercise-baseline context of docs/case_study_48_addendum.md,
  docs/reference/README.md and docs/reference/memory.md.
* Observed branch: feat/consultation-record-controls-92; observed head:
  d276d4ce8e8acfd72c3eebded58959b24c534a1c. The caller supplies authorization
  for integration onto main 9c648b2006e8b2e563823ea7d5aabdf7f1ac7096.
  This critique does not repeat or extend that authorization.
* Decision boundary: remove five unconditional service guard calls; preserve direct
  unknown refusal, supplied-record provenance, current authority/source checks,
  explicit building holds and all independent controls. No inferred applicability,
  client flags, Legal authority, actual let/renew transition, purchase API, spend,
  deployment, role/web changes or shared queue/SQL-store/server/export edits.
* Acceptance boundary: ordinary unknown-consultation service operations and existing
  explicit dependency enforcement can receive synthetic engineering evidence.
  Neither is evidence of actual consultation applicability or let/renew acceptance.
  Issue #92 remains partial/open.
* Dependencies considered: current appointment commitments; existing building
  predicates; installed-package test execution; task-owned SQL; configured
  lint/format/mypy and actual CI API discovery; historical artifact preservation;
  active #76/#122 ownership; later single original Review and coordinator handoff.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner direction; C1; P01-T01 | Covered | Five blanket calls are identifiable in procurement.py; no invented applicability mechanism is needed to remove them. |
| C2-C4; direct refusal and provenance | Covered | Record validation, immutable effective unknown, server recorder/time, source hash and optimistic history tests have explicit preservation instructions. Positive supplied records never become Legal clearance. |
| C5-C6; exact scope; P01-T01 | Partial | Package-aware instruction checks and package-less case advancement have different existing semantics. PC-001 requires acceptance and tests to distinguish them. |
| C7; independent controls | Covered | Main appointment helper is required; appointment, resident, hazard, provider, funding, stock, technical and current-authority controls remain in force. |
| C8; ordinary work; P01-T01 | Covered | Failing-first unmocked lifecycle and replacement of obsolete blanket expectations address the reported regression; historical 40-test isolation is not presented as a full-suite result. |
| Test ownership lock | Covered | Existing methods retained; consultation-only bypass setup removed; at most four new core methods and one HTTP denial method; backend inheritance supplies parity. PC-001 fits inside that allocation. |
| P02-T01; persistence and local validation | Covered | Real task-owned SQL, non-root installed HTTP, actual CI API discovery and configured ruff/format/mypy are required, not replaced by SQLite or a custom lint invocation. |
| Documentation, preservation and publication | Covered | Component guides and existing synthesis/index/log are named; old digests and upstream log prefix must remain unchanged; publication is separate from acceptance. |
| Missing exact Legal/let acceptance | Covered as an explicit unmet boundary | Research reports no genuine transition or typed authority relation. Plan retains that gap and leaves real binding use outside scope. |

## Verdict

* Verdict: Revise.
* Rationale: The bounded restoration is otherwise credible and appropriately
  conservative. One acceptance promise conflates package-scoped work-order checks
  with case-wide final advancement. Clarify that promise before implementation so
  the test suite cannot pass by avoiding a counterexample or by weakening an
  explicitly preserved building guard.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Separate package-isolated instructions from case-wide final advancement

* Related IDs: C5, C6, P01-T01, P02-T01; functional requirement at plan lines 56-57;
  acceptance at plan lines 71-72; phase-details lines 33-37.
* Evidence: .copilot-tracking/plans/2026-10-18/issue-92-scoped-consultation-hold-plan.md
  promises other case/package scope remains unaffected.
  .copilot-tracking/details/2026-10-18/issue-92-scoped-consultation-hold-phase-details.md
  groups issue/reissue/correct/book/final advance with a same-building
  other-case/package isolation expectation.
  src/core/src/zava_forward/core/store.py:504-515 calls
  buildings.blockers(self.data, self.cases, c) without a package before
  require_booked_capacity. src/core/src/zava_forward/core/buildings.py:141-145
  excludes a nonmatching package only when a package argument is supplied.
  src/core/tests/test_buildings.py:88-159 proves another package's issue/reissue
  on the held case, but proves successful advancement only on a different case.
* Concern: On case A with a hold explicitly scoped to package P1, a P2 instruction
  can pass the existing building predicate, while advancing case A still holds
  even if its only active appointed order belongs to P2. Removing the five
  consultation calls does not change that. The candidate does not distinguish
  this retained case-wide behavior from its broader package-isolation promise.
* Impact: An implementer could incorrectly report package-isolated advancement,
  use only a different-case sibling to imply that result, or change a building/
  advancement control to satisfy an acceptance promise outside the authorized
  five-call restoration. This is a pre-existing guard distinction, not a request
  to repair unrelated behavior.
* Smallest useful change: Revise only the new plan/details acceptance and test
  matrix to distinguish:
  (1) matching case/package issue, reissue, correction and booking remain held;
  (2) a different case can complete the ordinary lifecycle when independently
  eligible; (3) another package on the held case can perform package-aware
  operations, but final case advancement retains its existing case-wide hold.
  State the last behavior explicitly as retained, not as package-isolation
  success. Cover it in the allocated scoped-dependency method using subtests;
  no additional method allowance or production guard change is needed.
* Action owner: Planning parent.
* Exact resolving evidence: The new plan and phase details contain the explicit
  three-way matrix and the retained final-advance limitation, with no unconditional
  same-case/other-package advancement-success claim. The test specification
  requires one otherwise eligible case with a single active P2 appointed order,
  a separate P1 hold on that case, real current appointment/capacity/resident
  bindings, and a building GateError with unchanged case/order/audit state.
  It separately requires matching P1 denials, P2 package-aware success and
  different-case lifecycle success. Later execution records results across the
  planned JSON/SQLite/task-owned SQL backends, not just a direct predicate probe.
* Decision route: Direct planner correction. The caller already requires existing
  building controls to remain unchanged. No significant or divergent user decision
  is needed, and this finding does not authorize widening implementation scope.

## Strengths and Residual Risk

* Ordinary work has a genuine unmocked success target, not merely absence of a
  consultation exception. Existing HTTP lifecycle and independent-denial suites
  remain part of the validation boundary after removing bypass setups.
* A source-backed generic scoped hold is a valid test of existing dependency
  enforcement. Its label is not an applicability parser and its resolution is
  not Legal approval. The plan correctly refuses both interpretations.
* Direct explicit refusal remains unconditional even for supplied complete,
  not_applicable, forged or stale claims. Provenance and authority tests are
  retained rather than removed to obtain service success.
* Missing actual consultation authority and genuine let/renew acceptance are
  honestly documented. They remain unmet; the owner-approved restoration need
  not invent either capability to proceed.
* Actual SQL availability and full-suite baseline results are future execution
  evidence, not observed successes of this critique. An unavailable required
  SQL run must remain an explicit validation gap, not be counted as parity.
* One original implementation Review and coordinator exact-head acceptance remain
  later gates. This verdict does not confer either.

## Questions or Blocking Evidence Gaps

* No unresolved user question is needed for this bounded plan correction.
* No decision-critical research gap prevents assessment of the supplied scope.
  Missing actual Legal/let acceptance remains outside scope, not a reason to
  approve binding use or to fabricate a new transition.

## Limitations

* Static assessment, not implementation validation. No application files, tests,
  plan sources, research, state or historical records were edited.
* An attempted read-only import probe could not load zava_forward because the
  current shell lacks the installed distribution. No dependencies were installed.
* A subsequent in-memory source-isolated probe of buildings.blockers removed
  only the unused relative projection import from the parsed module. Synthetic
  case A/P1 was held; A/P2 was clear; A/no-package was held; sibling B/no-package
  was clear. This corroborates the source distinction only; it is not an installed
  application, backend, HTTP or acceptance test.
* Historical digests stored outside the supplied repository evidence were not
  retrieved. Historical artifacts were not opened for modification; tracked
  content was clean before this critique. Their publication-time digest gate
  remains the planning parent's responsibility.

## Recommended Next Action

* Highest-impact finding: PC-001, Medium.
* Action owner: Planning parent.
* Smallest next action: Directly disposition PC-001 in the new plan/details,
  distinguishing retained case-wide advancement from package-aware operations.
  Finalize without another critique, then continue only through authorized gates.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-18/issue-92-scoped-consultation-hold-plan.md](.copilot-tracking/plans/2026-10-18/issue-92-scoped-consultation-hold-plan.md) | Assessed final-candidate plan; unchanged by this critique |
| [.copilot-tracking/details/2026-10-18/issue-92-scoped-consultation-hold-phase-details.md](.copilot-tracking/details/2026-10-18/issue-92-scoped-consultation-hold-phase-details.md) | Assessed phase details; unchanged by this critique |
| [.copilot-tracking/research/2026-10-18/issue-92-scoped-consultation-hold-research.md](.copilot-tracking/research/2026-10-18/issue-92-scoped-consultation-hold-research.md) | Supplied C1-C8 research; unchanged by this critique |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-92-scoped-consultation-hold-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-92-scoped-consultation-hold-plan-critique.md) | This single independent critique |

## Next Steps

The active planning parent should resolve PC-001 directly and finalize without a
second critique. No user action is required. This critique stops after this artifact;
it does not implement, publish, merge or start an implementation Review.
