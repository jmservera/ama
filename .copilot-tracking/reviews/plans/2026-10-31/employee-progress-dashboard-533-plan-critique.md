---
title: Employee progress dashboard 533 original plan critique
description: Independent assessment of the supplied final-candidate plan and phase details
ms.date: 2026-10-31
---

## Metadata

* Task ID: 533 / employee-progress-dashboard-533
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/employee-progress-dashboard-533-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/employee-progress-dashboard-533-phase-details.md
* Critique execution status: Complete
* Original verdict: Revise
* Severity counts: Critical 0; High 2; Medium 2; Low 0.
* This is the first actual independent critique. The earlier refused
  phase-authoring dispatch is not critique execution or an earlier verdict.
  Preserve this original assessment after parent dispositions.

## Inputs and Criterion Boundary

* Caller direction authorizes ordered RPI and eventual publication of
  feat/employee-progress-dashboard-533 to main using Refs #533, only after
  the exact complete gate. Existing functionality is merged; the missing slice
  is stock-scale synthetic acceptance evidence, not a feature rebuild.
* Supplied research:
  .copilot-tracking/research/2026-10-31/employee-progress-dashboard-533-research.md,
  including C1-C6, W1-W3, selected/deferred alternatives and readiness.
* Assessed both complete supplied candidate documents, including AC1-AC4,
  AC5-local, AC5-live, P01-T01 through P03-T03, the locked addition budget,
  validation dependencies and original-outcome retention.
* Source checks were bounded to cited progress semantics, existing test
  templates, seed-174 homes, the browser checker and its owned-server helper,
  component documentation and the complete-gate contract/lock implementation.
  Read the project specification and knowledge-base entry/context sections.
* Source-edit boundary: src/api/tests/test_progress_dashboard.py,
  src/api/checks/progress_browser_check.py and src/api/README.md. At most one
  fixture helper, one inherited unit method and one optional scale browser
  function; retain existing checks. No runtime edit without a demonstrated
  coupled defect, no source deletions, package tests, mvp, private data,
  credentials, live/cloud exercise, other worktrees or non-pip tooling.
* This assessment establishes planning credibility, not passing tests,
  browser execution, receipt validity, hosted approval, full Fluent adoption
  or owner/live acceptance. None of those checks was performed here.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller scope; C1-C4; locked candidate | Covered | Existing feature retained; three source targets and bounded additions are appropriate. |
| C5; P01-T01; AC1 | Covered | Four 15,000-case overlays give 45,000 known lifecycles, 15,000 currently open and 45,000 archived cases. |
| AI provenance; C1; P01-T01 | Covered | Explicit synthetic recorded reviews retained; implementation must remap admitted links without admitting the existing mixed/unmarked negative control. |
| AC2; C2/C4; P01-T02 | Covered | Six actual chart/table/API comparisons, demo labels and existing small semantic browser checks retained. |
| AC3; C3/C4; P01-T01/P01-T02 | Covered | Combined filters, exact page IDs, first/final/empty/beyond boundaries and retained small-fixture history checks are planned. |
| AC4; C5; P01 | Covered | Fictional homes plus labelled test lifecycle overlays, not generic event inference or private lineage claims. |
| AC5-local; P02-T01; P03-T02 | Partial | PC-001: execution-path incompatibilities; PC-004: missing nonqueued admission. |
| P02-T02; original outcomes; publication dependency | Partial | PC-002: all Review findings are routed forward without an explicit blocking disposition. |
| P03-T01 | Covered | Authenticated noreply identity, local configuration, required trailer and committed original evidence are specified. |
| P03-T02/P03-T03; C6 | Partial | PC-003: phase details do not execute the promised independent exact-head assessment. |
| AC5-live; W1; W3; human/hosted approval | Covered | Live acceptance remains unmet; partial Fluent retrieval and direct accessibility limitations remain explicit. |

## Verdict

* Verdict: Revise.
* The implementation slice is credible and proportionate. The proposed
  publication sequence is not yet executable and sufficiently fail-closed.
  The four findings below are the complete actionable set for these supplied
  inputs; they are not deferred invitations for further critique passes.
* Execution is Complete because the evidence supports these conclusions.
  Publication is currently blocked by PC-001, independently of this critique's
  Revise verdict. No missing live evidence needs to be invented to finish the
  planning assessment.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Validation assumes incompatible paths and an unestablished clean execution environment

* Related IDs: AC5-local; P02-T01; P03-T02; non-functional requirements.
* Evidence: .copilot-tracking/plans/2026-10-31/employee-progress-dashboard-533-plan.md:55-59
  selects /tmp/mv and /tmp/ama-rpi-heavy.lock.
  .copilot-tracking/details/2026-10-31/employee-progress-dashboard-533-phase-details.md:45-51
  repeats that interpreter and source-tree PYTHONPATH instead of establishing
  installed-distribution validation.
  src/api/tests/test_progress_dashboard.py:106-109 creates default temporary
  scratch; src/api/checks/design_system_browser_check.py:233-234 creates
  checkout-local .venv scratch. tools/rpi-checks.py:2273-2275 unconditionally
  opens /tmp/ama-rpi-heavy.lock. src/README.md:210-215 rejects dirty,
  untracked and ignored candidate inputs.
* Concern: The current execution context does not permit the proposed /tmp
  file operations or temporary-directory creation. This is not resolved by
  changing only --out or setting cache variables: the exact gate itself opens
  its fixed lock, and existing focused tests/helper create scratch. The
  browser helper can also leave a checkout-local .venv parent, invalidating
  a subsequent clean-candidate gate. The additional production source roots
  on PYTHONPATH do not prove the required installed-distribution path.
* Impact: Implementation can be mistaken for verified acceptance, or the
  parent can reach publication with an impossible command/environment
  assumption. Silently changing the runner, using a different lock, skipping
  checks or deleting historical/foreign scratch would violate scope or gates.
* Smallest useful change: Revise both documents to separate permitted source
  work from blocked validation/publication. Specify pip-installed src
  distributions and the documented shared-test import paths, with
  caller-owned evidence/cache locations and a clean-input preflight. Explicitly
  record the fixed-lock and scratch incompatibilities as unresolved execution
  prerequisites, not as solved by output-directory substitution. Do not alter
  the runner or browser helper outside the locked source scope.
* Action owner: Planning parent.
* Exact resolving evidence: Matching plan/details dispositions identifying
  the compatible installed interpreter, actual commands and clean-input
  contract, plus an established execution context permitting every existing
  test/helper/gate file operation. Until that exists, dated evidence must say
  those checks and publication are Blocked; no receipt or pass is presumed.
* Decision route: Direct planner correction to disclose and enforce the
  blocker. No divergent source/tooling change is authorized; a different
  execution context must be established rather than assumed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Review findings have no mandatory publication-blocking disposition

* Related IDs: P02-T02; P03-T01 through P03-T03; original-outcome retention.
* Evidence: .copilot-tracking/details/2026-10-31/employee-progress-dashboard-533-phase-details.md:58-61
  instructs the parent to route "any findings to later work," while the
  subsequent publication tasks continue.
  .copilot-tracking/plans/2026-10-31/employee-progress-dashboard-533-plan.md:96-105
  does not require Review readiness before those tasks.
  src/README.md:269-273 requires corrections and the original Review to be
  stable before final-candidate validation/publication.
* Concern: A demonstrated fixture error, missing acceptance assertion or
  other blocking Review finding could be deferred while the same candidate
  is published. One Review is an execution limit, not authority to accept
  adverse findings or reinterpret them as residual live approval.
* Impact: Even a passing gate could validate a candidate that the independent
  Review found unsuitable for the promised acceptance slice.
* Smallest useful change: Add an explicit dependency: original Review executed,
  all blocking findings dispositioned, and candidate readiness established
  before publication. Preserve the single original Review. Resolve direct
  in-scope findings with recorded corrections and targeted revalidation;
  have the already required exact-head assessment evaluate their closure.
  If that cannot establish closure, stop publication rather than schedule
  another RPI Review or silently defer the blocker.
* Action owner: Planning parent; implementation parent owns any correction.
* Exact resolving evidence: Both documents state the stop condition and
  dependency; later dated changes/dispositions link each original blocking
  Review finding to its correction, observed revalidation and exact-head
  assessment conclusion. Original adverse wording/verdict remains unchanged.
* Decision route: Direct planner correction. Existing authorization does not
  accept unknown future defects; no user response is currently required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Phase details omit the independent exact-head assessment promised by the plan

* Related IDs: P03-T02; P03-T03; C6; exact-candidate publication requirement.
* Evidence: .copilot-tracking/plans/2026-10-31/employee-progress-dashboard-533-plan.md:102-103
  explicitly requires an independent exact-head assessment.
  .copilot-tracking/details/2026-10-31/employee-progress-dashboard-533-phase-details.md:73-79
  names it in the heading but specifies only gate execution and receipt
  verification. src/README.md:210-219 requires current-main verification
  immediately before independent exact-head review and push.
* Concern: The executor has no assessment owner, assessed inputs, persisted
  outcome or stop condition. The receipt verification command itself is also
  omitted. A heading or a historical source Review cannot substitute for
  independent assessment of the actual committed and gated HEAD.
* Impact: The authorized PR could be pushed without its required final
  independent assessment, or after a new commit/base/evidence change invalidates
  the assessment or receipt.
* Smallest useful change: Add a concrete ordered substep: commit stable original
  evidence; run the complete gate against fetched main; fetch again and execute
  python3 tools/rpi-checks.py --verify-receipt <external-receipt.json> --base
  <current-origin-main-sha>; obtain an independent persisted exact-head
  assessment of HEAD/base, full receipt and original finding dispositions;
  verify again immediately before push if the assessment intervenes.
  Any candidate, base, tool/image, receipt-evidence or dirty-input drift stops
  publication and requires fresh applicable gate evidence.
* Action owner: Planning parent specifies the step; the independent assessor
  owns its later assessment, not a second RPI Review.
* Exact resolving evidence: Revised P03-T02 details name ownership, inputs,
  output and fail-closed conditions. Actual publication later requires a
  preserved independent assessment identifying the exact HEAD/base and
  full receipt, followed by successful current-base verification with no
  intervening invalidating change.
* Decision route: Direct planner correction; the caller already requires
  this assessment and publication gate.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Heavy-check admission lacks the current nonqueued ownership guard

* Related IDs: P02-T01; P03-T02; shared-environment risk.
* Evidence: .copilot-tracking/details/2026-10-31/employee-progress-dashboard-533-phase-details.md:51
  only says to use the shared lock; :75-76 omits --lock-timeout 0.
  tools/rpi-checks.py:2299 defaults to a 600-second wait.
  src/README.md:255-262 requires actual ownership inspection, nonqueued
  --lock-timeout 0 admission and recording a busy gate as blocked without
  duplicate/waiting gates, foreign-output inspection or polling.
  src/README.md:115-116 says the runner owns its lock and must not be wrapped
  in outer flock.
* Concern: The plan permits waiting on a shared gate by default and does not
  distinguish outer-lock admission for focused commands from the runner's
  own lock. The older retry guidance in src/api/README.md:492-494 does not
  resolve the current root guide's stricter nonqueued coordination boundary.
* Impact: Avoidable contention, duplicate work or a self-locking deadlock can
  prevent bounded validation in an environment shared with other tasks.
* Smallest useful change: Once PC-001's execution prerequisite is resolved,
  require read-only inspection of actual lock ownership, nonblocking admission
  for standalone heavy checks, and --lock-timeout 0 for the self-locking gate
  without outer flock. A busy owner means Blocked evidence and independent
  lightweight work; resume only after an explicit coordination event, without
  polling or touching another task's resources.
* Action owner: Planning parent.
* Exact resolving evidence: Both validation phases specify that admission
  contract; later logs record admitted ownership or the exact busy blocker,
  never a queued duplicate. The directly related README update reconciles
  its retry wording with the current root guide without changing tooling.
* Decision route: Direct planner correction; no scope expansion or user
  response is required.

## Strengths and Residual Risk

* The cohort math is credible: the completed template has two closure episodes,
  the withdrawn template one, and the open template none. Across the three
  known-lifecycle cohorts this yields 60,000 openings including 15,000 reopens,
  45,000 closure episodes and final backlog 15,000 for the specified date window.
  Unknown-closure cases remain archived but not historical flow evidence.
* src/core/src/zava_forward/core/synthetic/scale_fixture.py:37-45 provides
  deterministic padded IDs and fictional attributes without private geography.
  Preserve template lifecycle/stage authority when overlaying generated
  attributes; random generated stages/events are not lifecycle evidence.
* Small-test and browser semantic coverage is retained. New scale checks
  need not become a performance SLA or a new testing abstraction.
* Existing AI negative controls must remain exclusions after ID remapping:
  src/api/tests/test_progress_dashboard.py:70-97 and
  src/api/src/zava_forward/api/progress.py:201-232 distinguish admitted links,
  non-AI templates, unreviewed records and unknown review dates. Nothing
  supports multiplying actual recorded AI usage with the case cohort.
* AC5-live, human accessibility/usability, full Fluent adoption, hosted
  approval and owner merge remain expressly outside local acceptance.
  Refs #533 is appropriate; no issue closure or live acceptance is warranted.

## Questions or Blocking Evidence Gaps

* No user clarification is needed to select the source slice or acceptance
  boundary. PC-001 identifies an actual execution prerequisite, not missing
  permission to rebuild tooling or bypass a gate.
* Research C6 reports historical skips and stale-base failure. It does not
  supply current passing validation; subsequent evidence must report actual
  exits, individual skip reasons and any unexecuted checks.

## Limitations

* No tests, lint/type checks, browser, scanner, SQL, gate, installation, live
  interaction or GitHub mutation was performed.
* Issue/merge and web-retrieval claims were assessed as supplied research,
  not freshly re-retrieved. Project context was read in relevant bounded
  sections, not as a new whole-project requirements audit.
* Initial status showed the supplied research/plan/details and session state
  untracked on the requested topic branch. No existing work was moved,
  committed or altered. This critique creates only the authorized output.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Directly disposition PC-001 through PC-004 in both
  candidate documents, preserving this original verdict. Establish or record
  blocked execution prerequisites before attempting validation/publication.
* User response required: No. No significant/divergent decision is necessary
  for these corrections; incompatible execution remains blocked rather than
  presumed authorized.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-31/employee-progress-dashboard-533-research.md](../../../research/2026-10-31/employee-progress-dashboard-533-research.md) | Supplied focused evidence and limits |
| [.copilot-tracking/plans/2026-10-31/employee-progress-dashboard-533-plan.md](../../../plans/2026-10-31/employee-progress-dashboard-533-plan.md) | Assessed candidate plan, unchanged |
| [.copilot-tracking/details/2026-10-31/employee-progress-dashboard-533-phase-details.md](../../../details/2026-10-31/employee-progress-dashboard-533-phase-details.md) | Assessed candidate details, unchanged |
| [.copilot-tracking/reviews/plans/2026-10-31/employee-progress-dashboard-533-plan-critique.md](employee-progress-dashboard-533-plan-critique.md) | Original complete critique and finding set |

## Next Steps

The active planning parent should revise/disposition this complete finding set
directly and finalize without another critique. No user action is required.
This assessor stops here; no peer RPI phase or publication is invoked.
