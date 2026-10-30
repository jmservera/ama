---
title: Finance 510 refresh final-candidate plan critique
description: Independent bounded assessment of the local rebase and validation plan
ms.date: 2026-10-29
---

## Metadata

* Task ID: finance-510-refresh-2327.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/finance-510-refresh-2327-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/finance-510-refresh-2327-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one independent final-candidate plan critique.

## Inputs and Criterion Boundary

* Caller requirements: local rebase of docs/finance-96 / PR #510 onto
  origin/main; preserve both contributions, with main authoritative for
  .github/rubric/* and scenario-manifest.json; source under src and tests
  outside packages; existing /tmp/mv tools, sibling paths, Ruff check/format,
  mypy and relevant tests; full API suite only after the specified successful
  nonblocking lock probe and with held admission; no Azure or push;
  Conventional Commit and Copilot trailer; Refs #96 without closing keywords;
  explicit full RPI loop.
* Primary evidence:
  .copilot-tracking/research/2026-10-29/finance-510-refresh-2327-research.md,
  including C1-C5 and the Wider, Deeper and Contrarian analysis.
* Supplied evidence pointers read: src/README.md, src/core/pyproject.toml,
  src/api/pyproject.toml and
  .copilot-tracking/changes/2026-10-29/finance-510-refresh-2221-changes.md.
  Required project context read: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md (opening context), docs/reference/README.md
  (opening context) and docs/reference/memory.md.
* Decisions and dependencies: score-only remote fast-forward before the
  authorized rebase; pinned-main conflict policy; integration proof before
  focused checks; checks before independent Review; committed original
  evidence before the complete-gate attempt; no remote publication.
* Acceptance boundary: assess credibility and safety of the proposed local
  execution and evidence handoff, not actual conflict resolution, fresh test
  results, finance approval, hosted acceptance or a successful complete gate.
  Existing research observations are supplied evidence, not independently
  re-executed facts.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1; finance authority boundaries | Covered | Research and plan retain Held/Unapproved status and prohibit operational approval claims. |
| C4-C5; P01-T01 | Covered | Remote score-only ancestry, pinned main, explicit rebase authority and original object retention are identified. |
| P01-T02; preservation and authoritative inputs | Covered | Main-owned rubric/manifest byte equality, append-only log prefix/suffix, both index contributions, source composition and original RPI bytes are explicit. |
| C3-C4; P02-T01; tooling and provenance | Covered | Component working directories, local/sibling source and test paths, existing tools, import origins, project-local fixtures and no unnecessary environment mutation are specified. |
| P02-T01; relevant regression scope | Covered | Finance, review/staging/pack, signoffs, lifecycle, provenance, rescan, manifest, dependency and HTTP role selectors are listed. No unconditional full API discovery is needed. |
| P02-T01/P02-T03; heavy admission | Covered | Plan requires probe plus held nonblocking lock for full API work and zero-timeout runner admission; busy ownership blocks rather than authorizes waiting or bypass. Apply this boundary to runner-invoked full API work too. |
| P02-T02; independent Review disposition | Partial | One Review and immutable adverse evidence are required, but the transition after an adverse current Review is not explicitly fail-closed; PC-001. |
| C2; P02-T03; final receipt lifecycle | Partial | Committed candidate, external fresh output and receipt invalidation after commits are covered; successful receipt verification and changed-base handling are not scheduled; PC-002. |
| Commit and handoff restrictions | Covered | Authenticated noreply author/committer, Conventional Commit, required coauthor, Refs #96, no issue-closing keywords, no push and no Azure remain explicit. |

## Verdict

* Verdict: Revise.
* Rationale: the integration and focused validation approach is credible.
  Two evidence-transition gaps need direct planner corrections before execution.
  Neither requires widening the test scope, another critique or a user decision.
* Severity counts: Critical 0; High 0; Medium 2; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Make an adverse independent Review an explicit readiness stop

* Related IDs: P02-T02, P02-T03; acceptance criteria for independent Review and
  local handoff.
* Evidence: .copilot-tracking/details/2026-10-29/finance-510-refresh-2327-phase-details.md,
  P02-T02 says "Record outcome and route new work" and then specifies the
  commit; P02-T03 proceeds "After committing" to the gate.
  The plan requires one Review and preservation of original adverse evidence
  but does not state the resulting readiness transition.
* Concern: the task sequence does not expressly distinguish an accepted
  candidate from a candidate with unresolved substantive Review findings.
  Recording an adverse result is not the same as stopping a ready handoff.
* Impact: a passing local gate or clean commit could be presented as resolving
  a Review objection even though local checks do not replace independent
  assessment. The one-Review constraint makes the unresolved-work route
  particularly important.
* Smallest useful change: add a fail-closed branch to P02-T02 and the handoff:
  retain the single original Review; an adverse or blocked result keeps the
  candidate not ready and records each unresolved finding, owner and next
  action. Any permitted evidence commit or diagnostic gate attempt must retain
  that status. Do not silently run another Review or treat a corrected,
  subsequently unassessed delta as independently accepted.
* Action owner: planning parent.
* Exact resolving evidence: revised P02-T02 and handoff text stating the
  outcome-dependent stop, with the later changes record required to preserve
  the actual Review verdict and unresolved work independently of gate results.
* Decision route: direct planner correction; no significant or divergent user
  decision. The existing instruction already requires one Review, not a loop.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Complete the successful gate receipt verification path

* Related IDs: C2, P02-T03; exact-head/current-main evidence handoff.
* Evidence: .copilot-tracking/details/2026-10-29/finance-510-refresh-2327-phase-details.md,
  P02-T03 specifies an external complete-gate attempt and forbids covering a
  later commit with its receipt, but contains no --verify-receipt step.
  src/README.md, Local RPI gate, requires receipt verification and treats
  changed base, candidate or tool/image identity as invalidating evidence.
* Concern: a successful runner exit is the end of the planned procedure even
  though the receipt has not been verified. "Current fetched main" also lacks
  a defined fail-closed response if it differs from the integration baseline.
* Impact: the local handoff could carry an unverified or stale receipt.
  No push is planned, but the coordinator still needs to know whether the
  receipt was verified and which exact head/base it covers.
* Smallest useful change: add a success-only receipt-verification step using
  the existing runner's --verify-receipt interface and the recorded base.
  Record head/base and verification exit. If refreshed main differs from the
  integrated baseline, stop and report reconciliation/new-gate work rather
  than claim current-main coverage. Missing prerequisites, busy locks or a
  failed attempt remain explicitly blocked; do not require a nonexistent
  success receipt or substitute cloud execution. Require fresh fetch and
  verification again before any later authorized publication assessment.
* Action owner: planning parent.
* Exact resolving evidence: P02-T03 names the verification command/interface,
  success/failure branches and base-drift disposition; the eventual external
  output and changes record identify the candidate, base, receipt and actual
  verification result without modifying the committed candidate afterward.
* Decision route: direct planner correction; no significant or divergent user
  decision and no authorization to push.

## Strengths and Residual Risk

* Preservation is semantic as well as syntactic: both documentation sides,
  source deltas and historical RPI bytes must survive; generated policy inputs
  have a separately explicit main-authoritative exception.
* Cross-worktree editable-install risk is addressed through local import
  provenance, sibling paths and the existing environment without blind installs.
* Focused tests are appropriate for the stated integration boundary. This
  critique does not prescribe full API discovery; the complete-gate attempt
  remains subject to existing nonqueued admission and prerequisite controls.
* Actual conflicts, optional integration skips, tool availability and hosted
  results remain execution uncertainties, already acknowledged by the plan.
  A blocked complete gate is an honest possible outcome, not authority to
  weaken checks or use Azure.

## Questions or Blocking Evidence Gaps

* None requiring user input for this bounded assessment. PC-001 and PC-002 are
  planner-owned corrections under existing direction.

## Limitations

* No implementation, rebase, tests, lock probe, dependency installation,
  commit or remote mutation was performed for this critique.
* Read-only status inspection found docs/finance-96 with four untracked
  current-task artifacts. They were not changed, moved, stashed or committed.
* Historical passing tests are context, not evidence for the future rebased
  candidate. This assessment does not establish operational, accessibility,
  legal, SQL, Azure or hosted acceptance.
* Only this critique artifact was written. Plan, details, research and earlier
  Review outcomes remain unchanged. No other agent was invoked.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: directly add the adverse-Review readiness branch and
  PC-002's success-only receipt verification/base-drift branch; record both
  dispositions while preserving this original Revise verdict.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/finance-510-refresh-2327-plan.md](.copilot-tracking/plans/2026-10-29/finance-510-refresh-2327-plan.md) | Assessed plan |
| [.copilot-tracking/details/2026-10-29/finance-510-refresh-2327-phase-details.md](.copilot-tracking/details/2026-10-29/finance-510-refresh-2327-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-29/finance-510-refresh-2327-research.md](.copilot-tracking/research/2026-10-29/finance-510-refresh-2327-research.md) | Supplied research |
| [.copilot-tracking/reviews/plans/2026-10-29/finance-510-refresh-2327-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/finance-510-refresh-2327-plan-critique.md) | Original independent critique |

## Next Steps

The active planning parent should disposition PC-001 and PC-002 directly and
finalize without another critique. No user action is required. This independent
critique stops here; it does not execute implementation or authorize publication.
