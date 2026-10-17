---
title: Issue 206 final-candidate plan critique
description: One bounded assessment of lifecycle and exact-head recording safeguards
ms.date: 2026-10-17
---

## Metadata

* Task ID: 206
* Task slug: issue-206-rubric-deleted-head
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/issue-206-rubric-deleted-head-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/issue-206-rubric-deleted-head-phase-details.md
* Critique execution status: Complete
* Critique count: exactly one final-candidate critique; no further critique requested.

## Inputs and Criterion Boundary

* Caller requirements: ordered Research, Plan, Implement and Review; issue/run
  evidence; immutable scored SHA; explicit closed-state handling distinct from
  API errors; unchanged/moved-head correctness; local validation with installed
  gh-aw; no inference dispatch, ref recreation, main fallback or force push.
* Supplied research: .copilot-tracking/research/2026-10-17/issue-206-rubric-deleted-head-research.md,
  questions Q1-Q3 and evidence C1-C5/W1-W3.
* Decisions and dependencies: P01 follows research and critique disposition;
  P02 follows P01; AC1-AC8 define acceptance. Preserve deterministic gates,
  model, permissions, action pins and check/job names. One new focused test
  module under .github/rubric/scripts; no removals; source and compiler-generated
  lock change together.
* Relevant implementation evidence inspected: .github/workflows/rubric-score.md,
  especially the conclusion step and record safe-output steps, plus existing
  .github/rubric/scripts/test_safe_output_runtime.py extraction patterns and
  bounded searches of existing rubric tests.
* Assessment boundary: credibility of this supplied implementation candidate,
  not a source-code review of a completed repair. No source, plan, details,
  research or existing review record was changed. No live GitHub API call,
  workflow dispatch, compiler invocation, local Git race experiment, Azure,
  environment-file or private-data inspection was performed. Historical issue
  and run claims are assessed as supplied research evidence, not reverified.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Ordered RPI and AC8 | Covered | Plan requires persistent phase events, implementation evidence, one Review and Refs #206 publication without merge or closure |
| Q1, C1, W1-W3, AC1 | Covered | Research identifies deleted mutable checkout after PR #204 closure and distinguishes historical failure from current code |
| Q2, C2/C5, AC3/AC4, P01-T01 | Partial | Immutable checkout and ordinary push are appropriate; hook input and atomic-race evidence need PC-001 |
| AC2/AC5, P01-T01/P01-T02 | Partial | Explicit closure versus API exceptions is specified; invalid successful responses need PC-003 |
| AC2-AC5, P01-T01 | Partial | Lifecycle step outputs and failure outcomes need an explicit consumer contract under PC-002 |
| AC3/AC4, P01-T01/P01-T02 | Partial | Publication must distinguish scored SHA from a successfully pushed bot SHA under PC-004 |
| AC6/AC7, P02-T01 | Covered | Compiler-only lock, invariant comparison, focused/full local suites and separate baseline failures are required |
| Locked ownership and exclusions | Covered | One new test module; no removals, dependencies, inference, unrelated workstreams or gate/model/permission/pin/name changes |
| P02-T02 | Covered | Acceptance audit and exact outcomes precede Review; no human approval or live-run result is inferred |

## Verdict

* Verdict: Revise
* Severity counts: 0 Critical, 3 High, 1 Medium.
* Rationale: the repair direction is credible and does not require a divergent
  design decision. Four bounded contracts are insufficiently explicit to
  implement and test fail-closed behavior consistently. In particular, a
  successful deterministic decision must never override a failed lifecycle
  preflight merely because the record step was skipped.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Specify a fail-closed hook input contract and prove the post-advertisement race

* Related IDs: Q2, C5, AC3/AC4, P01-T01/P01-T02.
* Evidence: phase details P01-T01 requires rejecting zero or unexpected
  advertised OIDs for refs/heads/HEAD_REF; P01-T02 names late deletion and
  backward movement but does not specify their timing or empty hook input.
* Concern: an OID comparison inside a stdin loop can succeed vacuously when Git
  supplies no proposed update, including an up-to-date destination. Checking
  only matching destination lines can also ignore unexpected updates. Further,
  deleting or moving a remote before advertisement tests the hook comparison,
  not the claimed server-side old-OID protection after advertisement.
  These are missing acceptance details, not evidence that ordinary push lacks
  compare-and-update protection.
* Impact: implementation can report push success without having enforced its
  exact advertised scored-OID precondition; inadequate race tests can leave the
  central no-recreation claim unproved.
* Smallest useful change: require exactly one hook update record, the explicit
  full destination ref, the intended local bot-commit OID, and a nonzero remote
  OID equal to the scored SHA. Reject empty or unexpected input. Keep the
  workflow-owned isolated hook and explicit non-force refspec. Separate
  pre-advertisement rejection tests from tests that mutate the remote after
  the hook receives the expected advertisement but before the update request.
* Action owner: planning parent, with implementation owner executing tests.
* Exact resolving evidence: P01 details name the input contract; the single
  focused module executes the extracted shell/hook against local remotes and
  proves unchanged-head success, zero/mismatch/empty-input rejection, and
  deletion/backward/forward movement after advertisement returning push failure.
  Assert no recreated ref or overwritten moved ref, no new_sha output and no
  passing publication on those failures.
* Decision route: direct-compatible planner correction. No force push, lease
  override, ref recreation or additional runtime helper is authorized.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Lifecycle outcomes must participate explicitly in publication eligibility

* Related IDs: AC2-AC5, P01-T01/P01-T02.
* Evidence: .github/workflows/rubric-score.md currently runs Publish verdict
  under (!cancelled()). Its blocked calculation uses only MOVED, PUSH_FAILED
  and RECORD_OUTCOME === 'failure'; a skipped record is not a failure.
  Phase details adds pre-checkout and pre-record API steps but does not define
  their output names, success-outcome requirements or publication inputs.
* Concern: if the deterministic gate has already written a passing decision,
  a subsequent lifecycle API failure can skip recording while publication
  still runs. Preserving the existing push/record gates alone does not block
  that pass. Conversely, suppressing publication on every unsuccessful
  preflight can conceal operational API failures rather than retain visible
  failure. An empty output is neither affirmative eligibility nor explicit
  closure.
* Impact: a failed preflight can become a success-shaped verdict, or closed
  heads can still receive comments/reviews/statuses via unguarded consumers.
* Smallest useful change: add a lifecycle state/outcome table and exact step
  conditions. Only a successful, validated response may establish eligible,
  moved or obsolete. Guard checkout and filesystem-dependent steps explicitly.
  Require all applicable lifecycle checks to have successful outcomes and the
  appropriate validated state before passing. Explicit closed state produces a
  notice and no verdict side effects; errors/unknown outputs fail the job and
  cannot pass. If a failure diagnostic is published, it must remain failure,
  not a rubric pass. Audit the existing missing-verdict conclusion condition
  so deliberate obsolescence is not mislabeled as a rerun-needed verdict.
* Action owner: planning parent, with implementation owner wiring consumers.
* Exact resolving evidence: revised P01 details list producer IDs, output values,
  outcome checks and consumers. Extracted source/compiled tests combine a valid
  passing decision with pre-record API failure, absent output and skipped
  record; assert no success status or APPROVE. Also cover closure at each
  lifecycle boundary with zero verdict side effects, initial preflight failure
  before checkout, and non-PR no-op behavior preserving main/calibration paths.
* Decision route: direct-compatible planner correction. Existing caller
  direction already resolves fail-closed versus obsolete behavior.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: A successful API call still needs validated lifecycle data

* Related IDs: Q2, AC2/AC4/AC5, P01-T01/P01-T02.
* Evidence: the candidate distinguishes explicit closed/open state and API
  exceptions; named API tests cover 404/403/500 but not malformed successful
  responses or missing head fields.
* Concern: HTTP/API success is not evidence that state and head SHA are usable.
  Unknown state, missing data/head, or a malformed SHA must not be interpreted
  as eligible, obsolete, or an ordinary moved-head result.
* Impact: permissive defaults can bypass lifecycle checks or hide bad data
  behind an obsolete notice or misleading movement diagnosis.
* Smallest useful change: define validation at every PR API boundary. Require
  explicit recognized state; for an open PR require a usable head object and
  full GitHub commit OID before comparison. Explicit closed state may short
  circuit without a usable head because deletion is an intended case.
  Unexpected data fails visibly without pass or record.
* Action owner: planning parent, with implementation owner writing validation.
* Exact resolving evidence: P01 details state accepted response shapes;
  extracted JS tests exercise null/missing data, unknown state, missing/null
  head, missing/invalid head SHA, and explicit closed state with unavailable
  head data. Assert failed checks emit no eligibility/obsolete-success output
  and cannot reach recording or passing publication.
* Decision route: direct-compatible planner correction, not a new API policy
  or permission change.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Define publication's expected SHA after a successful bot push

* Related IDs: C2, AC3/AC4, P01-T01/P01-T02.
* Evidence: source recording emits NEW_SHA only after successful push;
  publication targets SCORED_SHA and NEW_SHA. Candidate requires fresh PR state
  before publication but does not define which current head is then acceptable.
* Concern: always comparing current PR head to event SHA rejects the normal
  successful bot commit. Accepting event SHA or NEW_SHA indiscriminately permits
  a reset back to the scored SHA after recording, despite a later moved head.
  Merely checking open state misses a post-push movement altogether.
* Impact: the repair can either break active unchanged-head recording or publish
  a passing verdict after the PR head has moved again.
* Smallest useful change: define the publication expectation by actual recording
  result. After confirmed push, require current open head exactly NEW_SHA; if
  recording legitimately produced no commit, require exactly SCORED_SHA.
  Failed recording, failed lifecycle checks or incomplete outcomes cannot
  choose the no-change path. Preserve the existing status/review targets and
  moved diagnostic; closure remains obsolete rather than pass.
* Action owner: planning parent, with implementation owner adding branch cases.
* Exact resolving evidence: revised P01 details state this decision table.
  Extracted publication tests prove successful push/current NEW_SHA passes;
  legitimate unchanged/no-commit/current SCORED_SHA retains existing semantics;
  post-push forward move, backward move to SCORED_SHA, unrelated SHA and closure
  cannot publish success. Repeat against source and generated scripts.
* Decision route: direct-compatible planner correction. No different-SHA
  scoring, gate change or additional user decision is needed.

## Strengths and Residual Risk

* Immutable event-SHA checkout plus independent current-head checks preserves
  the moved-head signal that a SHA-only checkout change would lose.
* An isolated workflow-owned pre-push hook plus normal server old-OID checking
  is compatible with the no-force-push requirement. PC-001 tightens its contract
  and evidence rather than replacing the design.
* Closure and Git updates are not one transaction; the supplied candidate
  explicitly acknowledges that limit. Likewise, a PR can move after the final
  publication read. Retaining exact scored/bot SHA targets limits that residual
  race; do not claim atomic PR-lifecycle publication.
* Compiler-produced lock parity and explicit baseline-failure comparison are
  appropriate. The supplied 21 failures, 117 passes and 7 skips are baseline
  claims, not validation performed by this critique.
* All recommended tests fit the locked one-module budget and existing tooling.

## Questions or Blocking Evidence Gaps

* No user question or divergent decision is required.
* Implementation must supply the local executable evidence named in PC-001
  through PC-004. This critique does not substitute reasoning for those tests.

## Limitations

* No completed repair exists within the assessed inputs; findings identify
  substantive plan gaps, not confirmed bugs in a future implementation.
* Existing test helpers establish reusable patterns, not lifecycle coverage.
  No test suite or compiler was run during this read-only plan assessment.
* Review scope excludes live scoring, unrelated workstreams and all external
  operational acceptance.

## Recommended Next Action

* Highest-impact finding: PC-002.
* Action owner: planning parent.
* Smallest next action: revise P01-T01/P01-T02 with the explicit lifecycle
  producer/consumer and publication-SHA tables plus PC-001/PC-003 test cases;
  record disposition for all four findings and finalize without another critique.
* User response required: no.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-17/issue-206-rubric-deleted-head-plan.md](.copilot-tracking/plans/2026-10-17/issue-206-rubric-deleted-head-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-17/issue-206-rubric-deleted-head-phase-details.md](.copilot-tracking/details/2026-10-17/issue-206-rubric-deleted-head-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-17/issue-206-rubric-deleted-head-research.md](.copilot-tracking/research/2026-10-17/issue-206-rubric-deleted-head-research.md) | Supplied research and issue/run evidence |
| [.copilot-tracking/reviews/plans/2026-10-17/issue-206-rubric-deleted-head-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/issue-206-rubric-deleted-head-plan-critique.md) | Complete single-candidate critique |

## Next Steps

Return Complete / Revise to the active planning parent. The parent makes the
direct-compatible corrections, records their disposition, and finalizes before
Implement. No user action, peer-stage invocation or repeat critique is required.
