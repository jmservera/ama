---
title: Resident logout browser-check final-candidate plan critique
ms.date: 2026-10-28
---

## Metadata

* Task ID: PR-525-PRRT_kwDOUU8JX86xVDWZ
* Critique date: 2026-10-28
* Plan: .copilot-tracking/plans/2026-10-28/resident-logout-checks-525-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/resident-logout-checks-525-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: replace only the two stale SQL-browser cookie-deletion
  expectations with retained-token unauthenticated and signed-out session
  evidence; retain no-Set-Cookie behavior, failed-logout assertions, independent
  replay and resident isolation. Maximum four new helper tests, removal of only
  two stale assertions, and no application runtime changes.
* Evidence: the supplied plan, phase details and
  .copilot-tracking/research/2026-10-28/resident-logout-checks-525-research.md;
  relevant portions of src/api/checks/resident_demo_browser_check.py,
  src/api/tests/test_resident_demo_api.py,
  src/api/tests/test_resident_demo_check.py,
  src/api/src/zava_forward/api/resident_demo/app.py,
  src/api/checks/resident_assistant_browser_check.py,
  src/api/checks/resident_account_check.py, src/api/README.md and src/README.md.
* Decisions and dependencies: preserve Refs #520 without closing language; run
  relevant units, SQLite assistant/account browsers and the actual SQL demo
  browser; use nonblocking flock admission bounded to 40 minutes; use only
  task-owned resources; do not invoke az/Azure or read secrets/.env files.
  Governing environment instructions also forbid /tmp operations and require
  newly created working files to be project-relative.
* Publication boundary: committed original RPI evidence, a clean exact-head
  complete gate and immediately verified external receipt, independent
  exact-head assessment and retained hosted/human gates remain prerequisites.
  Focused validation cannot substitute for that receipt.
* Assessment boundary: credibility of this correction's implementation,
  validation and publication plan, not implementation acceptance, whole-issue
  #520 acceptance, UI conformance or live deployment. No tests, browsers,
  infrastructure commands, remote mutations or additional agents were run.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1; P01-T01; two stale expectations | Covered | Source confirms the normal and retry paths are the two deletion-on-success assertions. |
| C2; no-Set-Cookie; no runtime changes | Covered | Existing test_logout_revokes_and_replay_fails checks retained token, absent Set-Cookie and codec revocation; plan preserves it. |
| C4; P01-T01; original request fence | Partial | Capturing and replaying the original fence is planned, but the exact rejection oracle and proof of a usable original fence need PC-002. |
| P01-T01; session HTTP/body checks | Covered | Plan requires HTTP 200, signed_in false and session_id null, not merely sign-in-form visibility or an error response. Test sensitivity needs PC-002. |
| P01-T01; failure and isolation paths | Covered | Preserve 403/503/abort assertions, successful retries, separate replay context and Bob's successful protected request. |
| P01-T02; helper test budget | Partial | Four cases and type-only Playwright imports fit the budget; request arguments and invalid-response variants need explicit coverage within those same cases. |
| C5/C6; P01-T03; actual browser selection | Covered | Assistant uses a SQLite agenda; account driver is no-SQL; demo driver is SQL-backed without an invented --mssql option. |
| P01-T03; lock, scratch and isolation | Partial | Nonblocking bounded admission, new bounded loopback SQL and exact-owned cleanup are planned, but execution paths conflict with environment restrictions: PC-001. |
| C3/C7; P02-T01/P02-T02; original evidence and full gate | Covered | Plan preserves one original Review and records the full-gate/no-az conflict without weakening the gate. |
| P02-T03; publication and thread disposition | Covered | Push and thread resolution are conditional; Refs #520 and no closing language remain explicit. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.
* Rationale: the semantic direction and fail-closed publication handling are
  credible. The validation procedure nevertheless names forbidden filesystem
  operations, and the denial/helper-test contract needs a precise non-vacuous
  oracle. Both are direct planning corrections under existing instructions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Validation paths violate the governing filesystem boundary

* Related IDs: P01-T03; C3/C5; resource isolation and bounded heavy execution.
* Evidence: phase details P01-T03 specifies an external venv and acquisition of
  /tmp/ama-rpi-heavy.lock. The governing environment forbids /tmp file operations
  and requires created working files to be project-relative.
  src/api/checks/resident_assistant_browser_check.py:623 defaults browser
  output to tempfile.mkdtemp, and :638 also creates agenda scratch through
  tempfile.TemporaryDirectory even when --out is supplied.
* Concern: the planned lock cannot be opened under the current restriction;
  merely selecting a browser --out does not redirect all scratch. An external
  venv also conflicts with the working-file creation restriction. The plan
  currently reads as though focused validation is executable and only
  publication is blocked.
* Impact: validation would violate explicit instructions or stop before
  producing the required actual browser evidence. Choosing a private
  replacement lock would also lose coordination with other heavy workers.
* Smallest useful change: revise P01-T03 to name task-owned project-relative
  venv, evidence and scratch locations, with child-process scratch redirected
  there before any unit/browser execution and explicit assistant --out.
  Cover dependency tools and Chromium scratch as well as Python fixtures.
  Identify an available, permitted shared-lock mechanism coordinating the
  relevant heavy workers; preserve flock -n retries with one monotonic
  admission deadline of at most 40 minutes. If no such mechanism is available,
  record heavy validation as Blocked and do not start it. Do not silently use
  an independent lock or broaden this correction to shared-runner changes.
  Keep scratch out of commits, clean only exact task-owned resources, and
  preserve original evidence.
* Action owner: planning parent, then implementer for actual path and cleanup
  evidence.
* Exact resolving evidence: revised P01-T03 names permitted paths and either
  documents a coordinated permitted lock or explicitly marks heavy checks
  blocked. Any executed validation records its nonblocking admission outcome,
  bounded retry duration, isolated scratch/output configuration, task-owned
  SQL container/loopback port, and exact cleanup without forbidden-path writes.
* Decision route: Direct planner correction. Existing instructions resolve
  the boundary; no user response is needed to comply and report a blocker.
  Changing the shared lock convention or relaxing filesystem restrictions
  would be a separate significant decision, not authority granted by this plan.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Specify the exact denial oracle and fence-sensitive helper tests

* Related IDs: C4; P01-T01; P01-T02; retained-token denial and original-session
  acceptance criteria.
* Evidence: plan Functional Requirements says "deny a view request"; phase
  details P01-T01 similarly says "denies" and captures session_id without
  specifying a validated signed-in precondition. P01-T02 lists four response
  scenarios but does not require checking request headers.
  src/api/src/zava_forward/api/resident_demo/app.py:228 checks the token before
  the request fence: an invalid/revoked token receives 401, whereas a valid
  token with a missing or mismatched fence receives 409.
  src/api/checks/resident_demo_browser_check.py currently requires exactly 401
  for independent replay.
* Concern: an implementation accepting any non-200 response could count a
  fence-only 409 as revocation. Mocked responses alone would not reveal an
  omitted or incorrect X-Resident-Session header. Capturing a null or otherwise
  unusable pre-logout session_id would not establish a valid original fence.
* Impact: the new shared helper could appear to pass while the retained token
  remains usable, or while the check never sends the caller-required original
  session fence. The strengthened replay could lose the exact 401 protection
  already present.
* Smallest useful change: require exactly HTTP 401 for both retained-context
  /demo/view and independent replay, not arbitrary failure. Validate the
  pre-logout /demo/session response as HTTP 200 with signed_in exactly true and
  a nonempty valid original session_id, captured with the original cookie
  before either logout or failure interception. Establish a successful
  protected request with that same context and fence before the logout
  under test. Require the retained cookie value to equal the captured token.
  Preserve the post-logout HTTP 200 requirement with present signed_in and
  session_id fields whose values are exactly false and null.
  Within the same maximum four helper test methods, assert exact request
  headers/arguments and use subcases for 200/409/503 view responses,
  non-200 session responses, signed_in true, non-null session_id and missing
  required fields. Do not add runtime tests or remove other assertions.
* Action owner: planning parent for the explicit contract; implementer for
  helper/call-site assertions and the bounded test cases.
* Exact resolving evidence: revised P01-T01/P01-T02 spells out the precondition,
  exact statuses, mandatory body values and call-argument checks. The eventual
  diff and four-or-fewer new helper test methods demonstrate rejection of a
  live token, fence-only 409, incorrect retained token and invalid session
  responses, while proving the original fence is sent. Actual SQL browser
  evidence covers normal logout, all three failure/retry cases and independent
  replay with Bob's session still succeeding.
* Decision route: Direct planner correction. It sharpens the already requested
  non-vacuous assertion contract without expanding scope or requiring a
  significant user decision.

## Strengths and Residual Risk

* Both stale checks are correctly treated as check drift, not an application
  defect. Retaining the logout cookie protects the existing delayed-response
  fence; restoring deletion is neither needed nor authorized.
* Explicit HTTP 200 and false/null session-body checks are already in the
  plan. Their semantics must survive helper extraction; sign-in visibility
  alone is insufficient.
* The supplied research reports a wider deletion-expectation search. This
  critique confirms the named source assertions but does not independently
  repeat that repository-wide search or convert it into fresh test evidence.
* New memory/CPU-bounded loopback SQL with an in-memory fake password,
  task-owned database cleanup and no foreign-container inspection is the right
  resource boundary. That intent does not resolve PC-001.
* Publication remains blocked under the supplied full-gate/no-az conflict.
  Do not invoke az, downgrade to a partial gate, fabricate a receipt or claim
  remote correction/thread resolution. src/README.md describes a small-change
  tier, but it does not override the governing instruction requiring this
  final candidate's complete gate. Resolving that conflict would require
  separate authority; it is not a prerequisite to correcting the plan or
  honestly recording local blockers.
* Original critique and Review outcomes must remain immutable. The planning
  parent should disposition this complete finding set directly, not commission
  another critique to replace it.

## Questions or Blocking Evidence Gaps

* No user question is required for the two direct corrections.
* A permitted coordinated heavy-lock mechanism is not supplied. Until one is
  evidenced, treat heavy validation as blocked rather than claim admission.
* No compliant complete-gate execution is evidenced under the no-az
  restriction. Publication remains blocked as the plan already acknowledges.

## Limitations

* This is one read-only final-candidate assessment, not an implementation
  Review, test run, receipt verification or fresh remote PR assessment.
* The inspected branch is feat/resident-chat-520 tracking
  origin/feat/resident-chat-520. Supplied planning/research/state artifacts
  are untracked at assessment time; they were not moved or modified.
* No source, plan, phase-details, research or review record was changed. Only
  this caller-specified critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: correct P01-T03's filesystem and shared-lock procedure,
  record any resulting validation blocker, and disposition PC-002 in
  P01-T01/P01-T02 within the existing test/removal budget.
* User response required: No for these revisions. Any later request to change
  filesystem, lock coordination or publication-gate authority is separate.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-28/resident-logout-checks-525-plan.md](.copilot-tracking/plans/2026-10-28/resident-logout-checks-525-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-28/resident-logout-checks-525-phase-details.md](.copilot-tracking/details/2026-10-28/resident-logout-checks-525-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-28/resident-logout-checks-525-research.md](.copilot-tracking/research/2026-10-28/resident-logout-checks-525-research.md) | Supplied research and decisions |
| [.copilot-tracking/plans/2026-10-28/resident-logout-checks-525-critique.md](.copilot-tracking/plans/2026-10-28/resident-logout-checks-525-critique.md) | Complete original independent critique |

## Next Steps

The active planning parent should directly revise and disposition PC-001 and
PC-002, preserve this original critique unchanged, and finalize without another
critique. No user action is required for that handoff. Do not execute blocked
heavy checks or publish without the separately required evidence and authority.
