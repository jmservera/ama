---
title: Safety consent PR 509 rebase final-candidate plan critique
ms.date: 2026-10-29
critique_execution: Complete
verdict: Revise
---

## Metadata

* Task ID: pr-509-rebase-2026-10-29.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/safety-consent-130-rebase-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/safety-consent-130-rebase-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one independent final-candidate plan critique.

## Inputs and Criterion Boundary

* Caller requirements: rebase docs/safety-consent-130, draft PR #509, onto
  fetched origin/main; preserve both implementations and append-only entries;
  retain main's rubric directory and scenario manifest; use src-only source
  and separately owned tests; run the requested component checks and focused
  unittests; respect the heavy-test lock, no-Azure and no-push boundaries.
* Canonical research:
  .copilot-tracking/research/2026-10-29/safety-consent-130-rebase-research.md,
  including C1-C5 and their supplied component evidence.
* Additional supplied evidence inspected: src/README.md; core/API pyprojects;
  .github/workflows/src-ci.yml;
  .copilot-tracking/reviews/logs/2026-10-27/safety-consent-130-131-review.md;
  core resident, hazard, dependency and manifest test evidence; API resident,
  hazard and procurement test evidence; scenario-manifest.json; exact topic
  and upstream store deltas. Required case-study and reference context was
  read without deriving new regulatory or company claims.
* Decisions and dependencies: P01 precedes P02; P03 records validation before
  one independent Review and a local evidence commit. Existing test owners,
  no removals, at most two coupled regression additions and semantic versus
  regression coverage are locked by the plan.
* Acceptance boundary: assess credibility of the complete supplied plan,
  requirements, research, phases, tasks, dependencies, risks, decisions and
  acceptance criteria. This is not implementation Review, test execution,
  publication approval or a fresh hosted/operational assessment.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Branch, base, C1 and P01-T01 | Covered | Active branch and tracked upstream match the stated topic; local origin/main is 356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7. Rebase direction and per-hunk composition are explicit. |
| C3, intake and tenure requirements | Covered | Existing resident tests cover originals, corrections, current entitlement, persistence, transaction replay and non-releasing deletion; historical Review remains qualified. |
| C5, newer main runtime intent, acceptance 2 | Partial | Main changes briefing authorization, scope and cache behavior in store.py; focused selectors do not explicitly cover that behavior. PC-001. |
| Controlled rubric/manifest copies, P01-T02 | Covered | Equality with main is required; manifest validation checks source provenance rather than permitting blind digest replacement. |
| Append-only README/log/index preservation | Covered | Both sides' additions must survive; historical RPI evidence is immutable. |
| Source/test ownership and test budget | Covered | Source stays under src; core/API tests remain outside packages; no removals or generated fixture writes are authorized. |
| C4, P02-T01 | Covered | Full-project Ruff/format/mypy use component policy; sibling source/test imports and honest SQL-skip reporting are specified. |
| P02-T02 | Covered | Dependency, manifest and migration regressions are required, with tightly coupled repair only. |
| Heavy-test lock, no Azure, no push | Covered | Optional full API discovery requires the probe and a held nonblocking lock; local work cannot authorize cloud or publication actions. |
| P03-T01 and acceptance 4 | Covered | Literal commands, counts/skips, conflict decisions, dated original evidence and authenticated commit identity are required. |
| P03-T02 and P03-T03 dependency | Partial | Review precedes handoff, but all residual findings are routed identically without a blocking-defect stop. PC-002. |
| Acceptance 5 and publication boundary | Covered | Hosted CI, publication receipt, exact-head publication assessment and human acceptance remain explicitly unrun coordinator responsibilities. |

## Verdict

* Verdict: Revise.
* Rationale: The rebase and bounded validation approach is credible, but the
  plan needs an explicit validation obligation for main's changed store
  behavior and a fail-closed disposition for material findings from the
  single independent Review.
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Explicitly validate the newer main briefing behavior being preserved

* Related IDs: C5; functional requirement to retain newer main store behavior;
  acceptance criteria 2-3; P01-T01; P02-T01.
* Evidence: The supplied upstream delta for
  src/core/src/zava_forward/core/store.py changes Store.briefing: permission
  checking, programme versus assigned selection, entitlement-sensitive cache
  keys, status minimisation and response scope metadata. The topic delta
  changes Store.detail privacy. The plan's locked regression list and details'
  P02-T01 name resident, hazard, consultation and procurement suites, but no
  briefing behavior selector.
* Concern: The requirement to preserve both runtime intentions lacks an
  explicit behavioral check for the main-side store change. Passing intake
  suites and project lint/types does not establish briefing compatibility.
* Impact: Integration could retain the intake while losing or breaking newer
  briefing scope, privacy or cache behavior without failing a named check.
* Smallest useful change: Add the smallest existing focused briefing
  selector(s) that exercise the upstream change to P02-T01 and its coverage
  mapping. If supplied/upstream tests do not establish that behavior, use the
  existing two-method addition budget for the missing assertion, or record
  the uncovered contract as an explicit blocker rather than claiming it
  passed. Do not authorize full API discovery or unrelated test expansion.
* Action owner: Planning parent; implementation owner executes the selected
  checks after rebase.
* Exact resolving evidence: Revised plan/details name the owning test path
  and runnable module/class/method selectors and map them to preserved
  authorization, scope, minimisation and cache behavior; changes evidence
  records their commands and outcomes against the rebased candidate.
* Decision route: Direct planner correction. Preserving main's behavior is
  already required; no significant or divergent user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Separate blocking integration defects from accepted Review residuals

* Related IDs: P03-T02; P03-T03; acceptance criteria 1-5; local handoff goal.
* Evidence: P03-T02 in
  .copilot-tracking/details/2026-10-29/safety-consent-130-rebase-phase-details.md
  says, "One Review; residual findings route to follow-up, not a second
  implementation/Review loop." P03-T03 then commits and verifies the local
  candidate without specifying how an adverse Review changes readiness.
* Concern: The instruction does not distinguish explicitly excluded human/
  operational residuals from newly discovered source defects, failed
  preservation requirements or missing mandatory validation. It permits an
  in-scope blocking defect to be treated like an accepted follow-up.
* Impact: The coordinator could receive a clean committed candidate as a
  completed rebase handoff despite evidence that its integration is unsafe
  or a required acceptance criterion failed.
* Smallest useful change: Retain exactly one Review, but define its
  disposition gate: excluded/accepted residuals remain follow-ups; any
  material in-scope defect or failed required check blocks ready-for-push
  handoff. Preserve the adverse Review and return the blocker to the
  coordinator. A local commit may retain evidence, but must be labelled
  blocked/not ready and must not imply acceptance. Do not silently add a
  second Review or expand the approved execution loop.
* Action owner: Planning parent for the gate; implementation/handoff owner
  for truthful final status.
* Exact resolving evidence: Revised P03-T02/P03-T03 and acceptance/handoff
  wording distinguish accepted residuals from blocking findings and state
  the stop/return route; final changes/state reconcile every Review finding
  with readiness without upgrading the original verdict.
* Decision route: Direct planner correction. An honest blocked handoff
  follows existing requirements; no user response is needed to define it.

## Strengths and Residual Risk

* Correct rebase-side interpretation, ancestry/equality checks, range-diff
  inspection and no-skip conflict policy protect preservation.
* Fixed test ownership and coverage categories avoid opportunistic rewrites.
* Full API discovery is optional and lock-protected; narrower suites are not
  presented as complete CI or real SQL acceptance.
* Existing human/Legal/privacy/operational blockers remain separate from this
  bounded integration. No finding asks the planner to manufacture approval.
* Deferral of the complete publication gate is credible only because this
  task explicitly does not push or claim publication readiness. Coordinator
  publication obligations and repository gates remain intact.

## Questions or Blocking Evidence Gaps

* No unresolved user decision is needed for either finding.
* Exact future conflict hunks and post-rebase test results are execution
  evidence, not facts this critique can pre-certify.

## Limitations

* Read-only supplied-evidence assessment; no fetch, rebase, tests, cloud,
  commit, push or delegated assessment was performed.
* Initial status contains the caller's untracked dated research, plan, details
  and session evidence. These were neither moved nor changed; the details'
  clean-start statement describes the earlier research baseline, not this
  observation.
* No approval of final source correctness, hosted CI, legal compliance,
  accessibility or publication is inferred.

## Recommended Next Action

* Highest-impact finding: PC-002.
* Action owner: Planning parent.
* Smallest next action: Add the blocking-Review handoff rule and explicit
  main-side briefing coverage, then disposition both findings directly.
* User response required: No.
* Do not request another critique or start a subsequent phase from this worker.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/safety-consent-130-rebase-research.md](.copilot-tracking/research/2026-10-29/safety-consent-130-rebase-research.md) | Canonical supplied research |
| [.copilot-tracking/plans/2026-10-29/safety-consent-130-rebase-plan.md](.copilot-tracking/plans/2026-10-29/safety-consent-130-rebase-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/safety-consent-130-rebase-phase-details.md](.copilot-tracking/details/2026-10-29/safety-consent-130-rebase-phase-details.md) | Assessed execution details |
| [.copilot-tracking/reviews/plans/2026-10-29/safety-consent-130-rebase-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/safety-consent-130-rebase-plan-critique.md) | This single independent critique |

## Next Steps

Return Complete / Revise to the active planning parent for direct correction
and disposition of PC-001 and PC-002. No user action is required. This worker
stops here without implementation, another critique or subsequent-phase invocation.
