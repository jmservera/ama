---
title: Workspace script retry 524 final-candidate plan critique
description: Independent one-pass assessment of verification scope and executable boundaries
ms.date: 2026-10-30
---

## Metadata

* Task ID: 524
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/workspace-script-retry-524-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/workspace-script-retry-524-phase-details.md
* Critique execution status: Complete
* Candidate baseline: 5634f9a077d175a931c15e3400114665d8c071ee
* Execution count: one independent final-candidate critique.

## Inputs and Criterion Boundary

* Assessed the supplied plan, phase details and primary research in full, including research C1-C8/W1, requirements, AC1-AC5, both phases, task dependencies, test ownership and handoff.
* Considered the caller's already-merged #527 disposition, exact #524 scope, ordered RPI loop, local-only validation, no push, local commit identity/trailer requirements and prohibited operational access.
* Checked bounded evidence pointers in src/api/src/zava_forward/api/web/app.js, src/api/tests/test_workspace_scripts.py, src/api/checks/workspace_scripts_browser_check.py and src/api/README.md. Inspected the referenced synthetic-server helper and complete-gate contracts in src/api/checks/design_system_browser_check.py, src/README.md and tools/rpi-checks.py.
* Confirmed the selected branch is fix/workspace-script-retry-524 and HEAD matches the supplied baseline. The supplied new RPI inputs are untracked; they were not altered, moved or committed.
* This is a credibility assessment, not fresh test, browser, axe, live-site or complete-gate execution. No external research, cloud operation, implementation or nested delegation was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Exact issue scope; C1-C7; Q1-Q3 | Covered | Already-merged runtime and existing guide justify verification and evidence reconciliation, not another loader. |
| AC1 | Covered | Local HTTP checks establish current local delivery properties only; historical live cause remains explicitly unresolved. |
| AC2, AC4 | Covered | Canonical unit and real-browser owners cover failed initial delivery followed by recovery without document refresh. Fresh execution is required. |
| AC3 | Covered | Existing browser assertions cover exact terminal text, live status and native reload; the plan preserves bounded attempts and ambiguous-execution stopping. |
| AC5 | Covered | Owner-pending live verification is explicit and is not represented as delivered acceptance. |
| Semantic, non-colour and reduced-motion preservation | Covered | No runtime, style or test changes are planned. Scoped axe is supplemental, not accessibility conformance or proof of assistive-technology acceptance. |
| P01-T01; C8; validation dependencies | Partial | Exact API discovery and static commands are present, but interpreter/output locations need the execution-boundary correction in PC-001. |
| Canonical test ownership | Covered | Retain src/api/tests/test_workspace_scripts.py and src/api/checks/workspace_scripts_browser_check.py unchanged; zero production/test additions or removals. |
| Supplemental axe | Covered | Pinned, hash-verified 4.10.3, synthetic loopback data, recovery-relevant states and explicit coverage limitations are appropriate; no new repository suite is needed. |
| P02-T01; evidence and review | Covered | Update the existing API guide after execution; preserve original adverse evidence and run one independent post-implementation Review. |
| Complete gate; local commit; no push | Covered subject to PC-001 | Gate follows committed evidence, uses its own shared lock without nesting, and preserves failures as blockers. Exact-head assessment remains coordinator-owned. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* The verification-only runtime disposition is correct and sufficient for the permitted local issue scope. It must not be changed merely to create a code diff. One operational correction is required before execution; it does not justify runtime or test changes.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Reconcile interpreter and generated-output locations before execution

* Related IDs: C8, P01-T01, P02-T01, locked targets and generated-output boundary.
* Evidence: .copilot-tracking/plans/2026-10-30/workspace-script-retry-524-plan.md:104-106 mandates an existing temporary-location interpreter; lines 135-138 permit external session/temp outputs and the helper's workspace scratch. .copilot-tracking/details/2026-10-30/workspace-script-retry-524-phase-details.md:28-29 repeats the interpreter dependency. The current execution boundary does not permit general temporary-directory file operations. src/README.md also requires the final gate output outside the candidate worktree and rejects dirty/untracked/ignored candidate inputs.
* Concern: The candidate has not reconciled its ordinary interpreter/cache/runner/output paths with the available executor's file-operation boundary. Successful import probes do not resolve location permission. Moving all generated output into the worktree without a plan would instead undermine clean-candidate gate admission.
* Impact: Execution could violate the permitted boundary or stop on a predictable location/admission failure before establishing fresh local evidence.
* Smallest useful change: Replace the hardcoded temporary interpreter dependency with a permitted existing persistent interpreter, or a permitted isolated pip environment after an actual missing-dependency result. State permitted concrete locations for supplemental tooling, caches, logs and final gate output, and how newly owned scratch is separated from the clean candidate. Treat the caller-prescribed shared-lock path separately from general scratch authorization; do not silently substitute another lock or infer blanket temporary-storage permission. If the executor cannot satisfy both the prescribed lock/external-gate contract and its location restrictions, record that specific execution blocker and stop the affected command rather than bypassing either boundary.
* Action owner: Planning parent, with the implementation coordinator responsible for checking the selected execution environment.
* Exact resolving evidence: Revised P01/P02 execution details identify the permitted interpreter and storage layout, retain the exact four API commands and unchanged test owners, and show how the final candidate remains clean. Before execution, record permission/prerequisite checks for that layout; if no compliant layout exists, record the precise blocked commands and do not claim their success. No runtime or test-file delta resolves this finding.
* Decision route: Direct planner correction. No new product, scope or significant/divergent user decision is required.

## Strengths and Residual Risk

* Existing retry behavior is finite and shared per page: two automatic attempts, 250/500ms delays, five-second attempt timeout, and no reinjection after ambiguous execution. Preserving it avoids duplicate lexical execution risks.
* Synthetic browser coverage verifies actual scripts and bounded requests, native keyboard reload and stale route/session protection. Reusing these owners is stronger than adding a redundant mock-only suite.
* The existing helper owns a responsive loopback server and terminates its exact process. Browser requests are restricted to its local origin.
* No new source or test changes should be manufactured. A demonstrated defect requires a recorded divergence, not silent scope expansion.
* Historical transport causation, deployment and live acceptance remain unresolved and explicitly owner-pending. Neither source inspection nor clean local/axe results can close those gaps.
* Full-gate prerequisite failures remain blockers. Local evidence does not replace independent exact-head review, hosted checks, human approval or publication permission.

## Questions or Blocking Evidence Gaps

* No unresolved product or user-choice question.
* PC-001 is the complete actionable finding set for this supplied boundary. No further critique pass is requested after direct disposition.

## Limitations

* Did not execute tests, browser journeys, dependency installation or the full gate. Their anticipated results remain unproven until implementation.
* Issue/PR lifecycle and historical findings are assessed from the supplied research and caller context, not a new remote inspection.
* The selected interpreter and final output layout were not probed. This assessment identifies their planning conflict, not a demonstrated test failure.
* Scoped axe findings cannot establish whole-site WCAG, screen-reader, voice-control or operational acceptance.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Disposition PC-001 directly in the execution details, then continue the already-authorized ordered loop with unchanged runtime and tests.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/workspace-script-retry-524-plan.md](.copilot-tracking/plans/2026-10-30/workspace-script-retry-524-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/workspace-script-retry-524-phase-details.md](.copilot-tracking/details/2026-10-30/workspace-script-retry-524-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-30/workspace-script-retry-524-research.md](.copilot-tracking/research/2026-10-30/workspace-script-retry-524-research.md) | Primary research and evidence mapping |
| [.copilot-tracking/reviews/plans/2026-10-30/workspace-script-retry-524-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/workspace-script-retry-524-plan-critique.md) | This original one-pass critique |

## Next Steps

The active planning parent should resolve PC-001 directly, preserve this original
verdict and continue to Implement only within the reconciled execution boundary.
No second critique, user response, implementation by this reviewer, commit or
remote write is required or authorized.
