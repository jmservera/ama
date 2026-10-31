<!-- markdownlint-disable-file -->
# RPI Plan Critique: gate-chat-test-572

## Metadata

* Task ID: 572
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/gate-chat-test-572-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/gate-chat-test-572-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller direction requires ordered Research, Plan, Implement and Review; actual local exact-case Chromium execution; unexpected integration/dependency skips failing closed; regressions; and a fresh complete committed exact-head gate before publication.
* Assessed the supplied plan, phase details and research in full. Examined bounded tools/rpi-checks.py source covering selector identity, required-command verification, skip parsing, Runner.command, browser dispatch and gate admission. Examined tools/test_rpi_checks.py covering existing chat dispatch/discovery/receipt regressions and both successful receipt fixture generators.
* Consulted src/README.md's local-gate and shared-lock contract and the supplied C8 prior Review's acceptance and critique-disposition sections. Read repository context documents without treating owner memory or historical evidence as current execution proof.
* Scope remains optional exact verbose-success enforcement in the shared parser, selected at both execution and verification call sites; owned GateTests regressions; and the directly related guide. No test removals, at most two new methods plus existing mutation cases, and no workflow/UI/dependency changes.
* Publication includes pip-only local validation, synthetic data, no credential files/private data/main/other-worktree changes, existing shared heavy admission, one immutable original Review before commit, external fresh receipt verification and independent exact-head assessment before push, and PR Refs #572.
* This assessment determines planning credibility, not runtime success, issue closure, human acceptance or hosted approval. No tests, network calls, source edits or Git mutations were performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Ordered RPI; W1/W2 | Covered | Research records issue intake and merged #575/#595; candidate does not duplicate inherited wiring. |
| AC1; C1/C3/C4; P01-T01 | Covered | Both Runner.command and verify_commands currently rely on aggregate check_skips output; the optional exact-ID branch addresses the observed unrelated-success fixture weakness. |
| AC2; C2; P01-T01 | Covered | Preserve the exact API-discovery tuple and integration restriction; dedicated command must have zero skips. |
| AC3; P01-T02 | Covered | Existing GateTests remains owner; no removals; two-method ceiling; both fixture generators corrected; semantic mutation hashes recomputed; execution-path negative regression required. |
| P02-T01; C6 | Covered | Requested API commands and opted-in exact selector are explicit; browser claims remain local/synthetic, with shared heavy admission and external logs required. |
| P02-T02; original Review preservation | Partial | One original Review is correctly preserved, but unconditional residual deferral lacks an adverse-source-finding publication stop: PC-001. |
| AC4; C7/C8; P03-T01 | Covered subject to PC-001 | Commit precedes fresh complete gate; current fetched main, external receipt verification, separate exact-head assessment and no stale receipt reuse are required. |
| Resource/dependency and authority boundaries | Covered | Missing prerequisites, inherited failures and contention block publication; no skip bypass, cloud substitution, lock interference or unrelated edits are planned. |
| PR linkage and evidence limits | Covered | Refs #572 only; local evidence does not substitute for human/hosted approval. |

## Verdict

* Verdict: Revise
* Severity summary: Critical 0; High 1; Medium 0; Low 0.
* Rationale: The implementation direction is narrow and evidence-backed. Before implementation handoff, explicitly prevent the blanket Review deferral from allowing publication with an unresolved blocking source finding. This is a direct-compatible planner correction, not a new implementation/review loop or scope expansion.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Distinguish blocking original Review findings from permissible later evidence

* Related IDs: P02-T02, P03-T01, AC1-AC4, original Review dependency.
* Evidence: .copilot-tracking/plans/2026-10-31/gate-chat-test-572-plan.md P02-T02 says to "route residual findings to later work, without a current-task implementation/review loop." P03 depends on completion of P02, while .copilot-tracking/details/2026-10-31/gate-chat-test-572-phase-details.md P03 requires the original Review and a clean candidate commit, without specifying disposition of blocking source findings. Its explicit failure stop concerns prerequisites and the later gate. The plan's general requirement to publish only when requirements pass does not resolve this conflicting blanket deferral.
* Concern: A completed one-pass Review can identify a current-task correctness defect in exact-ID enforcement or receipt verification. Completion is not approval. Deferring such a defect as later work would leave the frozen candidate ineligible even if its existing automated checks subsequently pass. Conversely, a Review's lack of the deliberately post-commit final receipt is not itself a reason to forbid the planned P03 validation.
* Impact: The executor lacks an unambiguous decision rule for the transition from original Review to candidate commit, final gate and publication. Automated checks and later exact-head assessment must not be treated as silently disposing of an adverse original Review.
* Smallest useful change: Amend P02-T02 and P03-T01 in both planning artifacts to distinguish (1) blocking current-task source/acceptance findings, which stop publication and are reported with preserved original Review evidence; (2) missing final committed gate evidence, which P03 is explicitly authorized to obtain; and (3) nonblocking residuals, whose explicit disposition is recorded without relaxing caller requirements. Preserve the single original Review and do not initiate another implementation/review loop. Independent exact-head assessment must return an eligible disposition before push; unresolved blocking findings remain a publication stop.
* Action owner: Planning parent, with implementation/publication coordinator enforcing the rule.
* Exact resolving evidence: Both artifacts explicitly state these three dispositions and the stop rule. Later original Review evidence identifies whether current-task source findings remain blocking; P03 publication evidence records no unresolved blocking findings, a fresh verified full receipt, and an eligible independent assessment of the same exact head. A completion marker or passing unit-test log alone does not resolve the finding.
* Decision route: Direct-compatible planner correction. Current caller direction already requires all acceptance and publication gates and one original Review; no significant/divergent user decision is needed.

## Strengths and Residual Risk

* Reusing CHAT_PANEL_DISCOVERY_SKIP's verbose ID avoids inventing a parallel identity convention; requiring one exact successful result and no other result lines strengthens the actual observed weakness.
* A default-None parser branch preserves existing generic suite and SQL behavior. Selecting it at both call sites avoids a live-execution/receipt-verification split.
* The budget is proportionate: retain all inherited tests, extend the existing semantic mutation test, and keep actual browser behavior owned by the unchanged chat test.
* Real Chromium, complete MSSQL/browser execution and fresh receipt verification remain later obligations, not claims inferred from mocked fixtures or available imports.
* Shared resource contention and inherited failures are acknowledged publication risks. The supplied prior Review explicitly records the parent's accepted shared-lock execution context; this critique does not reintroduce the previously rejected worker-only lock-location objection as a parent planning blocker.

## Questions or Blocking Evidence Gaps

* No missing evidence prevents assessing this bounded plan.
* No user clarification is required. Resolve PC-001 directly and retain any later actual validation blocker as adverse evidence, not a fabricated pass.

## Limitations

* Issue/PR facts and prerequisite availability are assessed as supplied research claims; no fresh network verification was performed.
* No validation commands ran. This critique proves neither current Chromium success nor full-gate feasibility.
* Source inspection was bounded to the requested gate/test ownership trace and directly supplied gate/Review evidence, not a repository-wide audit.
* Existing planning, research, source and historical Review records were not modified.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the explicit Review-disposition publication rule to P02-T02/P03-T01 in both artifacts and record PC-001's direct-compatible resolution.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/gate-chat-test-572-plan.md](../../../plans/2026-10-31/gate-chat-test-572-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-31/gate-chat-test-572-phase-details.md](../../../details/2026-10-31/gate-chat-test-572-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-31/gate-chat-test-572-research.md](../../../research/2026-10-31/gate-chat-test-572-research.md) | Supplied bounded evidence |
| [.copilot-tracking/reviews/plans/2026-10-31/gate-chat-test-572-plan-critique.md](gate-chat-test-572-plan-critique.md) | This single complete critique |

## Next Steps

Return Revise to the active planning parent. Resolve PC-001 directly and finalize without another critique; continue the caller-selected ordered loop only after recording that disposition. No user action is required. This critique stops here.
