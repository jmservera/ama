---
title: Workspace script retry correction1 plan critique
description: Independent final-candidate assessment for issue 524 correction1
ms.date: 2026-10-28
---

## Metadata

* Task ID: 524-correction1.
* Critique date: 2026-10-28.
* Plan: .copilot-tracking/plans/2026-10-28/workspace-script-retry-524-correction1-plan.md.
* Phase details: .copilot-tracking/details/2026-10-28/workspace-script-retry-524-correction1-phase-details.md.
* Critique execution status: Complete.
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: Correct RV-001 and RV-002 through a new correction loop;
  preserve adverse artifacts; parent executes heavy checks using explicitly
  authorized nonblocking admission every 60 seconds for at most 40 minutes.
  No Azure, secrets, .env, private datasets or live acceptance claims.
* Supplied research: .copilot-tracking/research/2026-10-28/workspace-script-retry-524-correction1-research.md.
* Original adverse evidence: .copilot-tracking/reviews/logs/2026-10-28/workspace-script-retry-524-review.md.
* Assessed all correction requirements, AC1-AC6, P01-T01/P01-T02,
  P02-T01/P02-T02, dependencies, selected alternatives and residual work.
* Direct source inspection was limited to the named loader, unit/browser
  owners, actual specialist entry point, existing synthetic-server lifecycle,
  src/README.md and tools/rpi-checks.py where needed to test plan credibility.
  Repository context was read without inspecting private data.
* Scope remains app.js, the two existing workspace test/check files and API
  README. Zero executable additions/removals; generated logs and authoritative
  receipts remain external. This assessment does not authorize implementation.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| RV-001; C1-C3; AC1; P01-T01 | Covered | Capture actual me object; null entry guard; identity and abort checks before post-await status/dispatch and stale catch rendering. Null/replaced sessions exercised without artificial abort, on success and failure. |
| AC2; P01-T02 | Covered | Constructed 401 uses real api()/login while retry remains held; same-document login, cleared status and absence of recovered dispatch are explicit contracts. |
| AC3; C4; P01-T02 | Covered | Observe initial failed request and absent readiness before retry release; assert real map/specialist view, bounded requests and one document request. |
| RV-002; AC4; P01-T02 | Covered | Unmodified script bytes, direct node listeners, precise coverage, bounded settlement, exact independent hash/status/view comparison before revisit, and explicit execution/cancellation alternatives. |
| Preserved behavior; P01-T01/P01-T02 | Covered | Existing route predicates, error-only budget, terminal timeout, native reload, polite status and healthy dependencies remain requirements. |
| RV-003; AC5; P02-T01 | Covered | Parent-owned full API discovery and focused Chromium under bounded admission; actual failures remain blockers. No claimed execution evidence yet. |
| AC6; P02-T02; lock dependency | Partial | Full runner defaults do not implement the specified admission policy; PC-001. |
| AC6; P02-T02; publication | Partial | Fresh-main receipt verification is present, but independent exact-head assessment is not scheduled after the committed gate; PC-002. |
| Scope, identity, retained evidence, RV-004 | Covered | Locked file ownership; privacy-safe commit and trailer; nonforce topic push and Refs #524; original outcomes immutable; live verification owner-pending. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 0 High, 2 Medium, 0 Low actionable findings.
* Rationale: The proposed source correction and browser contracts address the
  named defects credibly. Two bounded execution/publication details must be
  corrected before the candidate can reliably follow its acceptance gates.
  Neither finding challenges the owner's explicit lock retry authorization.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Full-gate admission does not specify the authorized retry policy

* Related IDs: AC6, P02-T01, P02-T02.
* Evidence: Correction details P02-T01 specifies nonblocking attempts at
  60-second intervals for up to 40 minutes. P02-T02 instead delegates admission
  to the runner without arguments or retry handling. In tools/rpi-checks.py,
  heavy_lock at lines 2175-2188 retries once per second, and --lock-timeout
  defaults to 600 at line 2201. The output directory is created before lock
  admission at line 2238; an existing output directory is rejected at lines
  2219-2223.
* Concern: The described full-gate invocation can silently use a different
  retry interval and stop after ten minutes. Merely repeating the same command
  after a denied admission also fails because its output directory now exists.
* Impact: The parent can exhaust or misexecute publication admission despite
  having explicit authorization for the requested 40-minute policy.
* Smallest useful change: Specify runner --lock-timeout 0 for each full-gate
  attempt, spaced 60 seconds apart within a monotonic 40-minute admission
  deadline. Use a fresh external output directory per invocation and preserve
  denied-admission logs. Retry only verified lock contention, not failed
  preflight or an admitted failed gate. Do not wrap the runner in a held copy
  of the same lock. Keep admission timeout distinct from admitted check runtime.
* Action owner: Planning parent.
* Exact resolving evidence: P02-T02 contains that concrete runner admission
  contract, including fresh-directory and failure classification behavior;
  later execution logs record attempts, exits and actual admitted gate output.
* Decision route: Direct planner correction. Owner authorization is settled;
  no user decision, alternate lock or runner source change is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The publication sequence omits independent exact-head assessment

* Related IDs: AC6, P02-T02.
* Evidence: Correction details P02-T02 schedules independent Review before
  commit, then full gate, receipt verification and push. It does not schedule
  an independent assessment of the resulting committed HEAD and verified
  receipt. src/README.md:150-158 requires fresh-main verification immediately
  before independent exact-head review and push. The original Review's
  remaining publication prerequisites retain that same distinction.
* Concern: The single substantive correction Review can assess stable source
  before commit, but that alone does not establish an independent assessment
  of the later exact commit, final external receipt and current base.
* Impact: The parent could publish after self-verification while omitting a
  repository-required independent publication gate.
* Smallest useful change: Add an explicit post-gate, pre-push independent
  exact-head assessment handoff bound to HEAD, base and verified receipt.
  Preserve the one substantive correction Review; this handoff can confirm
  reviewed-source identity and final gate evidence without restarting a
  substantive Review loop. Keep its final attestation external so recording
  it does not create another candidate commit and invalidate the receipt.
* Action owner: Planning parent, coordinating the independent assessor.
* Exact resolving evidence: Updated P02-T02 orders commit, full gate,
  fresh-main receipt verification, independent exact-head assessment and
  nonforce push. Final external assessment identifies the reviewed commit,
  base and receipt; any candidate/base change requires renewed valid evidence.
* Decision route: Direct planner correction. No new product choice or user
  response is required.

## Strengths and Residual Risk

* Object identity is the correct proposed boundary: a truthiness or user-ID
  check alone would miss replacement sessions. Guards must precede every
  planned stale status write, dispatch and catch render, not merely suppress
  the eventual exception. The plan expressly includes these positions.
* The real 401 scenario avoids the original artificial abort and
  document-navigation false assurance. Retain the requested measurement of
  actual view invocation: unchanged login DOM alone cannot exclude an attempted
  invocation that throws before rendering.
* Direct listeners attached before insertion survive handler-property cleanup
  and node removal. Precise coverage should identify the target script's
  top-level execution range, not sum function/range counts. A zero count is
  cancellation evidence only after a positively observed terminal outcome;
  a bounded wait expiring is a failure, not proof of cancellation.
* These are implementation obligations already implied by the plan's
  deterministic settlement and actual-evaluation contracts, not additional
  actionable planning findings. Require actual runtime evidence: no browser
  behavior or reliable cancellation event was demonstrated by this critique.
* Exact status/hash/independent-view checks must occur after settlement and
  before route revisit, as planned. One document request proves the no-refresh
  contract only when collection begins before initial navigation.
* Historical RV-003 remains adverse. Later successful execution supplies new
  evidence without rewriting it. RV-004 remains owner-pending live work.

## Questions or Blocking Evidence Gaps

* No unresolved user decision. Runtime browser behavior and environment
  prerequisites remain validation responsibilities, not inferred successes.

## Limitations

* No implementation edits, tests, browser execution, heavy checks, lock access,
  Azure, dependency installation, commit, push or delegation occurred.
* No fresh generic web-guideline review or application conformance claim:
  this is a bounded plan critique using supplied research and source evidence.
* Existing untracked correction artifacts were left untouched. Branch
  fix/workspace-script-retry-524 was retained; no Git lifecycle change occurred.
* This is the complete actionable finding set for the supplied boundary.
  Original adverse artifacts and all plan/research sources remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001, because the prescribed final gate can use the
  wrong admission contract and reject a reused output directory.
* Action owner: Planning parent.
* Smallest next action: Directly resolve PC-001 and PC-002 in P02-T02 and record
  dispositions, then finalize planning without a second critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-28/workspace-script-retry-524-correction1-plan.md](.copilot-tracking/plans/2026-10-28/workspace-script-retry-524-correction1-plan.md) | Assessed correction plan |
| [.copilot-tracking/details/2026-10-28/workspace-script-retry-524-correction1-phase-details.md](.copilot-tracking/details/2026-10-28/workspace-script-retry-524-correction1-phase-details.md) | Assessed execution contracts |
| [.copilot-tracking/research/2026-10-28/workspace-script-retry-524-correction1-research.md](.copilot-tracking/research/2026-10-28/workspace-script-retry-524-correction1-research.md) | Supplied correction evidence |
| [.copilot-tracking/reviews/logs/2026-10-28/workspace-script-retry-524-review.md](.copilot-tracking/reviews/logs/2026-10-28/workspace-script-retry-524-review.md) | Immutable original adverse Review |
| [.copilot-tracking/reviews/plans/2026-10-28/workspace-script-retry-524-correction1-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/workspace-script-retry-524-correction1-plan-critique.md) | This single independent critique |

## Next Steps

Return Complete / Revise to the active planning parent. Parent resolves both
planner-owned findings directly, records dispositions and finalizes the plan
before implementation. No user action or second critique is required.
