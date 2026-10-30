<!-- markdownlint-disable-file -->
# RPI Plan Critique: Capacity page correction

## Metadata

* Task ID: 523-correction
* Task slug: capacity-page-523-correction
* Branch: fix/capacity-page-523
* Critique date: 2026-10-28
* Plan: .copilot-tracking/plans/2026-10-28/capacity-page-523-correction-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/capacity-page-523-correction-phase-details.md
* Critique execution status: Complete
* Assessment: One independent final-candidate critique; no repeat critique requested.

## Inputs and Criterion Boundary

* Caller requirements: Correct RV-002 unsaved-draft loss and RV-003 weak browser
  proof; retain the original Review; require actual local SQL/browser validation
  under the parent's authorized nonblocking 60-second/40-minute admission policy.
  No Azure, environment files, private datasets, heavy execution or lock probing
  belongs to this critique. Ruff line length remains 100.
* Candidate inputs: The plan and phase details above, and
  .copilot-tracking/research/2026-10-28/capacity-page-523-correction-research.md,
  including C1-C8/W1 and its final Ready disposition.
* Historical evidence:
  .copilot-tracking/reviews/logs/2026-10-28/capacity-page-523-review.md,
  particularly RV-001/RV-002/RV-003 and its distinction between initial-route
  cancellation/session coverage and mutation-refresh recovery.
* Bounded read-only source checks: src/api/src/zava_forward/api/web/ops.js,
  src/api/src/zava_forward/api/web/app.js,
  src/api/src/zava_forward/api/web/timecapture.js,
  src/api/checks/capacity_browser_check.py,
  src/core/src/zava_forward/core/appointments.py,
  src/api/README.md and src/README.md.
* Decisions and dependencies: Capacity-local retry, no mutation replay or router
  overhaul, retained legacy compatibility repair, canonical browser ownership,
  generated fictional fixtures, owned SQL resources, separate original Review,
  committed-candidate full gate and external exact-head publication assessment.
* Acceptance boundary: AC1-AC5 and P01-P03 were assessed together. This critique
  assesses planning credibility, not implementation correctness, executed runtime
  acceptance, live causality, WCAG conformance or permission to publish.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| RV-002, AC1, C1-C3, P01-T01 | Covered | Read-only go invocation retains live DOM on repeated failed reads; success-only capture restores unrelated drafts. Scenario includes values, checks, expansion, context/event reference, edits during failure and saved-form cleanliness. |
| Mutation replay, C7, P01-T01 | Covered | Real configure mutation and persisted configuration proof; actual POST counting distinguishes a read retry from replay, including idempotent replay attempts. No fabricated authority or mocked success. |
| Navigation/session recovery isolation, P01-T01, AC4 | Partial | Implementation guard is required, but the specified browser scenarios do not exercise cancellation or expiry through the changed go/retry closure. PC-001. |
| RV-003, AC2/AC3, C4-C6, P01-T02 | Covered | Actual navigation href contracts, exact headings, specific content/empty states, successful browser GETs with route identity, unknown-entry failure, API HTTP/transport tracking and rendered package/order IDs/counts are required. |
| Cancellation destination, AC3, P01-T02 | Covered | Staff time capture and successful status read replace the existing permissive non-error-heading assertion. PC-001 concerns the additional mutation-refresh path, not this initial-route scenario. |
| Test ownership and size, P01 | Covered | One canonical browser target; at most two new helpers plus route-contract data and inline scenarios; no new test file, production export, dependency or removal. Existing HTTP regressions remain unchanged. |
| RV-001, AC4, C8, P02-T01 | Covered | Real generated-demo --mssql browser and full API execution remain mandatory; SQLite or source-only success cannot substitute. Parent owns admitted execution, task-owned resources and cleanup. |
| Static checks and web review, P02 | Covered | Strict Ruff/format at 100, Node syntax, API mypy and scoped regressions precede heavy work; independent Review includes required web rules. |
| Review history, P02-T02 | Covered | Original Review remains immutable; one new correction Review reconciles retained repair and correction evidence; material findings block publication rather than trigger an in-task review loop. |
| AC5, C8, P03-T01 | Covered | Commit precedes full gate; current-base verification, external authoritative receipt and separate external exact-head assessment precede push/PR. Changed candidate/base/tool/image/input invalidates evidence. |
| Authority, exclusions and follow-ups | Covered | No Azure/private data or invented contract authority; owner live acceptance and RV-004/005/006 remain separate; no merge or issue-closure claim. |

## Verdict

* Verdict: Revise
* Severity summary: Critical 0; High 0; Medium 1; Low 0.
* Rationale: The recovery approach and route/read/render proof are credible.
  One targeted validation gap remains: existing initial-route race checks do not
  prove that the newly changed recovery closure leaves a later route or login
  untouched. This is a direct planner correction within the selected design.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Exercise cancellation and session expiry through the changed recovery closure

* Related IDs: P01-T01, P01-T02, P02-T01, AC4; functional requirement
  "Navigation abort/session expiry do not overwrite a new route or login."
* Evidence: The phase details require captured abort/session guards in go, but
  the new interaction specified under P01-T01 ends with successful recovery.
  P01-T02 strengthens the existing cancellation destination without specifying a
  go/retry-origin race. In src/api/checks/capacity_browser_check.py:231-268,
  cancellation begins with page navigation and the 401 begins with page.reload.
  Neither enters the mutation-success/failed-refresh go catch in
  src/api/src/zava_forward/api/web/ops.js:149-163. The historical Review explicitly
  distinguishes these paths.
* Concern: The planned validation can pass with correctly guarded initial route
  loading while the changed local retry still renders/focuses a stale status,
  starts a refresh after leaving, or interferes with session-expiry login.
  Assertions about the initial route are not resolving evidence for the new
  closure's lifecycle.
* Impact: The correction can retain AC1 drafts yet regress the explicitly retained
  navigation/session boundary, especially while a refresh or retry is pending.
  Required real browser execution would not expose that defect with the stated
  scenarios alone.
* Smallest useful change: Add inline scenarios to the existing canonical harness:
  after a real successful configure mutation, hold a refresh or read-only retry
  GET, navigate away with explicit handling of the unsaved-draft dialog, then
  release/abort that request and assert the exact Staff time capture heading,
  successful status read, absence of stale capacity status/focus, and no new
  capacity reads or POSTs after departure. Separately return a named 401 from
  that recovery path and assert login remains visible and focused appropriately,
  with no capacity rerender/retry or mutation replay after session termination.
  Scope expected cancellation/401 failures to those requests; do not weaken the
  unexpected-error tracker.
* Action owner: Planning parent for the plan/detail amendment; implementing parent
  for inline assertions and admitted runtime evidence.
* Exact resolving evidence: P01-T01/P01-T02 and P02-T01 explicitly own these
  recovery-path scenarios, still within the two-helper ceiling and zero-removal
  rule. The subsequent task-owned real SQL/browser run records each scenario's
  destination/login assertions, named injected requests, successful expected
  GETs and unchanged POST count, without unscoped ignored failures.
* Decision route: Direct planner correction. No significant or divergent user
  decision; the current requirements already demand lifecycle isolation.

## Strengths and Residual Risk

* Retry reuses the existing success-only replacement boundary rather than
  introducing a global router change or an extra draft store.
* AC1 expressly checks edits made while failure remains visible, not merely a
  stale snapshot captured before saving.
* Route-specific successful browser reads and response-derived rendered row proof
  are materially stronger than independent request-context reads or heading-only
  checks. Implementers must correlate responses to the current navigation/scenario,
  not satisfy a contract from an earlier response.
* Actual SQL/browser results, prerequisite availability, admission and cleanup
  remain unknown and explicitly gate publication. They are not planning successes.
* The full gate does not automatically invoke this separate capacity harness;
  retaining both explicit P02 SQL/browser evidence and the P03 full receipt is
  necessary and is correctly planned.
* The reviewed original outcome, later correction Review, exact-head publication
  assessment and hosted/owner approval remain distinct evidence boundaries.

## Questions or Blocking Evidence Gaps

* No unresolved user decision or decision-critical research gap.
* Runtime outcomes are pending implementation and authorized parent execution;
  they cannot be supplied by this read-only critique.

## Limitations

* No tests, SQL/browser processes, lock probes, external source retrieval,
  publication operations or source changes were performed.
* W1 was considered as supplied research evidence, not freshly retrieved or a
  fresh web-interface conformance review.
* The original plan, details, research and historical Review were not edited.
  Existing untracked correction artifacts were treated only as supplied inputs.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the two recovery-lifecycle inline scenarios to the
  owned tasks and validation checklist; dispose this finding and finalize the
  plan without another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-28/capacity-page-523-correction-plan.md](.copilot-tracking/plans/2026-10-28/capacity-page-523-correction-plan.md) | Assessed candidate plan |
| [.copilot-tracking/details/2026-10-28/capacity-page-523-correction-phase-details.md](.copilot-tracking/details/2026-10-28/capacity-page-523-correction-phase-details.md) | Assessed task details |
| [.copilot-tracking/research/2026-10-28/capacity-page-523-correction-research.md](.copilot-tracking/research/2026-10-28/capacity-page-523-correction-research.md) | Supplied focused evidence |
| [.copilot-tracking/reviews/logs/2026-10-28/capacity-page-523-review.md](.copilot-tracking/reviews/logs/2026-10-28/capacity-page-523-review.md) | Unchanged original Review |
| [.copilot-tracking/reviews/plans/2026-10-28/capacity-page-523-correction-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/capacity-page-523-correction-plan-critique.md) | This single critique |

## Next Steps

Return Complete / Revise to the active automatic planning parent. The parent
directly resolves PC-001, finalizes the candidate without a second critique, and
continues implementation and the required runtime/review/publication gates.
No user action is required. This critique stops here.
