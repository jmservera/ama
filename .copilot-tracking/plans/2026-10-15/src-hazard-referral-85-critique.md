---
title: Hazard referral final-candidate plan critique
description: Single independent bounded assessment of issue 85 planning credibility
ms.date: 2026-10-15
---

## Metadata

* Task ID: 85, src-hazard-referral-85.
* Critique date: 2026-10-15.
* Plan: .copilot-tracking/plans/2026-10-15/src-hazard-referral-85-plan.md.
* Phase details: .copilot-tracking/details/2026-10-15/src-hazard-referral-85-phase-details.md.
* Critique execution status: Complete.
* Assessed branch: feat/src-hazard-referral-85.
* Execution: exactly one independent final-candidate assessment; no nested agents.

## Inputs and Criterion Boundary

* Caller requirements: src-only implementation reusing merged core workflow,
  API, buildings and handoff contracts; accepted ADR 0006 dependency direction;
  no hazard-service ownership, classification, clocks or closure; separately
  evidenced receipt and acceptance; home-scoped retrofit hold; visible external
  response and resident-update due/actual times; preserved human gates, consent
  and privacy.
* Delivery constraints: no new SQL or SQLite-specific behavior, Azure-only
  deployment boundary, pip rather than uv, local suites/lint/mypy and synthetic
  application before CI, no invented owner or live evidence, committed RPI
  artifacts and a PR using Refs #85. At most two new test modules; no test
  removals; only directly coupled legacy regression edits and narrowly scoped
  typed-call mypy overrides.
* Research considered:
  .copilot-tracking/research/2026-10-15/src-hazard-referral-85-research.md,
  including C1-C7 and recorded W1-W2 retrievals. W1-W2 were not re-retrieved.
* Context considered: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. Memory is context, not evidence.
* Code evidence considered: src/core/src/zava_forward/core/workflows.py,
  src/core/src/zava_forward/core/store.py,
  src/core/src/zava_forward/core/projection.py,
  src/api/src/zava_forward/api/server.py,
  src/api/src/zava_forward/api/web/app.js,
  src/api/tests/test_handoff_api.py, directly related workflow-test references,
  and the core/API pyproject.toml test-typing contracts.
* Decisions and acceptance considered: plan requirements and six acceptance
  criteria, P01-T01 through P03-T02, research's accepted/deferred alternatives,
  docs/adrs/0006-src-layout-and-cutover.md dependency rule, and the supplied
  C7 pointers to FR-003/RULE-003 in
  docs/brds/agentic-retrofit-programme-brd.md.
* Assessment boundary: engineering-plan credibility, not implementation
  correctness, current legal advice, live transport proof or full issue
  acceptance. No plan, details, research, source or review records were edited.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| ADR 0006; C1; src-only dependency and reuse constraints | Covered | Extends WorkflowMixin, existing case-body persistence and API/web; no parallel store, workload import in core or agents-image SQL/blob change. |
| RULE-003; C2/C5/C7; no classification, clocks or closure | Partial | Explicit architectural boundary and observation labels are sound; inherited summary/audit claims need an explicit target, PC-003. |
| P01-T01; distinct sent/receipt/acceptance | Covered for new referrals | Selected safety receiver, separate evidence, authenticated actors, sender follow-up and unchanged retrofit ownership are explicit. Legacy continuation is unresolved, PC-002. |
| P01-T01; provenance, snapshots, replay/index validation | Covered | Immutable source/awareness, versioned event snapshots, ledger, pre-mutation checks and strict indexes are specified. |
| C3/C6; linked-home hold and independent release | Covered | External repair evidence plus independent safety-role release reason; consent and building blockers remain independent. |
| P01-T01/P02-T01; external response/update times | Covered | External due/actual observations have evidence; missing values remain unknown and no statutory deadline is calculated. |
| Research contrarian requirement; uninterrupted urgent intake | Partial | AI/pause independence is specified, but closed retrofit records are not explicitly carried into implementation and validation tasks, PC-001. |
| C4; P01-T01/P02-T01; privacy and human authority | Covered | No-need narrative redaction, contractor default deny, no new model prompt data and server-supplied actors are explicit. |
| P01-T01; legacy compatibility | Partial | Read compatibility and unknown provenance are explicit; forward lifecycle for legacy referred/repaired records is not, PC-002. |
| Locked Test and Target Contract | Covered | Only test_hazard_referral.py and test_hazard_api.py may be added; existing coupled regressions retained; typed-call-only mypy override permitted. Findings fit these modules. |
| P03-T01; validation and documentation | Covered | All five src suites, ruff/mypy, synthetic loopback app, relevant migration regressions and Docker attempt; commands/results and infrastructure limitations recorded. Existing README/index/log updates planned. |
| P03-T02; review, commits and PR | Covered | One implementation review, reconciliation, safe identity, committed artifacts, topic push and main PR using Refs #85; no merge. |
| Owner/live evidence and application acceptance | Covered as unmet | Engineering slice is not delivered application or full issue acceptance; real model, SQL Server, Azure and human gates remain explicitly unclaimed. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: the bounded architecture and test scope are credible, but the
  following three task-level gaps leave known safety-continuity and inherited
  semantic risks to implementer interpretation. Direct revisions can resolve
  all three without expanding the approved engineering slice.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Carry closed-record hazard intake into the executable contract

* Related IDs: P01-T01, P02-T01, uninterrupted-referral acceptance, research
  Contrarian wave and reflection.
* Evidence: research explicitly requires referral availability "including
  closed retrofit records". In
  src/core/src/zava_forward/core/workflows.py, raise_hazard rejects c["closed"].
  In src/api/src/zava_forward/api/web/app.js, safetyPanel hides the intake form
  behind !c.closed. The task details mention AI/pause independence, but omit the
  closed-record exception and its UI/HTTP regression.
* Concern: "uninterrupted referral" does not explicitly require removing both
  known closed-record barriers. An implementer can satisfy the listed
  outage/pause tests while retaining this researched failure.
* Impact: a newly observed hazard on a completed retrofit record can require
  manager reopening before staff can log it, coupling safety intake to an
  unrelated retrofit lifecycle decision.
* Smallest useful change: specify that authorised staff can raise and refer
  a new observation on a closed retrofit record without reopening it or
  changing completion, consent, ownership or other gates. Include the safety
  panel's closed-record intake control and explicit HTTP/core regression.
* Action owner: planning parent, with implementation assigned to P01-T01 and
  P02-T01.
* Exact resolving evidence: revised tasks name the closed-record behavior;
  tests in the two permitted new modules demonstrate authenticated raise and
  refer on a closed record, preserved closed/stage/owner/consent state, and a
  reachable intake control rather than the inherited !c.closed condition.
* Decision route: direct planner correction. Supplied research already resolves
  the intended behavior; no significant or divergent user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Define prospective continuation of legacy referrals

* Related IDs: P01-T01 legacy read compatibility; C2; distinct receipt/acceptance
  and evidence requirements.
* Evidence: src/core/src/zava_forward/core/workflows.py stores legacy referral
  owner as a display name, with referred/job fields but no selected receiver
  code, receipt or acceptance events. refer_hazard rejects a second referral.
  P01-T01 requires only the selected safety receiver to receive/accept and
  requires receipt before acceptance, while promising only legacy read
  compatibility and unknown missing provenance.
* Concern: the plan does not say how an already referred or repaired legacy
  hold obtains a verified receiver and the new evidence chain. Inferring
  acceptance from existing dates would violate the no-fabrication rule;
  applying the new prerequisites without a prospective path can strand it.
* Impact: existing held homes can become impossible to progress safely, or
  implementation may silently manufacture receiver/receipt/acceptance history
  to retain the old repair/release behavior.
* Smallest useful change: specify a forward-only legacy reconciliation rule:
  retain old records and unknown historical fields, require an authorised
  prospective receiver binding/evidence step before applicable new transitions,
  and state the treatment of existing repaired and already released records.
  Do not infer an authenticated receiver from a display name or backdate events.
* Action owner: planning parent, assigned to P01-T01 with matching HTTP
  coverage in P02-T01.
* Exact resolving evidence: a short legacy state/transition contract in phase
  details plus JSON/SQLite restart tests for legacy raised, referred, repaired
  and released fixtures. Tests show explicit denials until required new
  evidence, a safe prospective continuation for active holds, no fabricated
  historical receipt/acceptance and no retroactive reopening of released holds.
* Decision route: direct planner correction within the established preservation,
  authenticated-identity and no-fabrication requirements; no user response
  required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Include inherited gate and audit claims in the boundary cleanup

* Related IDs: RULE-003, C2/C3/C5, P01-T01, P02-T01, no operational clock rules.
* Evidence: src/core/src/zava_forward/core/store.py gate_reasons says the owner
  "confirms it is resolved", and status_line stops work until the owner confirms
  the "safety issue is resolved". These strings reach case detail and summaries.
  src/core/src/zava_forward/core/workflows.py raise_hazard emits an Emergency
  audit entry instructing referral "the same day"; safetyPanel repeats that
  promise. The plan targets safety-panel labels, detail/note projection and
  external timing observations, but does not expressly retire these inherited
  service-resolution and same-day-policy assertions.
* Concern: updating the panel's state labels alone can leave the shared
  summary/gate path conflating retrofit-hold release with hazard resolution,
  while new ledger entries continue to assert a timing policy that this slice
  explicitly does not own or validate.
* Impact: staff and audit readers can interpret the retrofit record as proof of
  service resolution or a promised response time, contrary to the caller's
  authority boundary and deferred owner timing policy.
* Smallest useful change: explicitly include coupled gate/status wording and
  newly emitted emergency audit text in P01/P02. Describe an active retrofit
  hold and its accountable release action, not hazard closure; replace the
  unverified same-day promise with neutral manual-referral guidance and unknown
  external timing. Preserve historical audit entries unchanged.
* Action owner: planning parent, assigned to P01-T01/P02-T01.
* Exact resolving evidence: revised target contract names gate_reasons,
  status_line and new emergency audit messages; permitted semantic/HTTP tests
  assert hold-only wording, no new same-day service promise, unchanged historical
  ledger records and independently supplied timing observations.
* Decision route: direct planner correction. Current direction already excludes
  invented timing policy and service closure; no divergent decision or owner
  policy selection is needed.

## Strengths and Residual Risk

* Reusing the existing JSON case body avoids a schema migration and preserves
  the SQL portability boundary. JSON/SQLite semantic coverage does not claim
  SQL Server durability.
* Explicit receiver receipt and acceptance, unchanged retrofit ownership,
  independent evidence-backed hold release and role-projected narratives are
  well aligned with the supplied scope.
* The two-module cap is feasible: the findings add cases to the already planned
  semantic and HTTP/synthetic modules, not new test infrastructure or broad
  regression rewrites.
* The plan explicitly leaves operational timing policy, actual service
  transport/receipt, real model/SQL Server/Azure execution and human acceptance
  unmet. This is honest engineering-slice readiness, not permission to mark
  those gates complete or claim a delivered application has passed them.

## Questions or Blocking Evidence Gaps

* None requiring a user answer for this bounded plan revision.
* Missing operational and live evidence is declared, not substituted with
  fixtures. Any future activation remains outside this assessment.

## Limitations

* This assessment read supplied artifacts and relevant local code, not an
  implementation diff. No tests, live application, CI, Azure, model or database
  service were executed.
* W1-W2 are the research parent's recorded retrieval evidence, not independent
  verification here. No additional issue comments, owner decisions or current
  legal-source claims are inferred.
* All actionable concerns discovered within this boundary are included above;
  no separate late finding set or repeat critique is requested.
* The pre-existing untracked RPI artifacts were left untouched. This critique
  does not authorise committing, moving or changing them.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: add closed-record core/HTTP/UI intake behavior and
  preservation tests to P01-T01/P02-T01, then disposition PC-002 and PC-003 in the
  same direct revision before finalizing implementation readiness.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-15/src-hazard-referral-85-plan.md](.copilot-tracking/plans/2026-10-15/src-hazard-referral-85-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-15/src-hazard-referral-85-phase-details.md](.copilot-tracking/details/2026-10-15/src-hazard-referral-85-phase-details.md) | Assessed implementation and validation tasks. |
| [.copilot-tracking/research/2026-10-15/src-hazard-referral-85-research.md](.copilot-tracking/research/2026-10-15/src-hazard-referral-85-research.md) | Supplied research and evidence boundary. |
| [.copilot-tracking/plans/2026-10-15/src-hazard-referral-85-critique.md](.copilot-tracking/plans/2026-10-15/src-hazard-referral-85-critique.md) | This single complete finding set. |

## Next Steps

The active planning parent should directly revise and disposition PC-001 through
PC-003, then finalize without another plan critique. No user action is required.
This critique execution stops here; it does not invoke implementation, review or
another agent.
