---
title: Independent plan critique - Employee briefing loading assurance
description: Single complete assessment of the implementation-ready candidate for issue 531
ms.date: 2026-10-31
---

## Metadata

* Task ID: 531
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/employee-briefing-loading-531-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/employee-briefing-loading-531-phase-details.md
* Critique execution status: Complete
* Assessment count: Exactly one complete independent critique; no nested agents.
* Observed branch: feat/employee-briefing-loading-531
* Observed HEAD: 5666bd33
* Write boundary: This critique artifact only.

## Inputs and Criterion Boundary

* Caller direction requires ordered Research, Plan, Implement and Review, pip-only requested API discovery/Ruff/local Playwright, original dated evidence, privacy-safe local commit with the specified trailer, and the full exact-head gate before push and PR to main.
* The supplied research records issue-first inspection, merged #529/#538/#581, C1-C7/W1-W5, three research waves, the UX invocation returning questions only, and unavailable live AC7. Remote issue/PR state was not independently retrieved in this critique.
* Reviewed the supplied plan, phase details and corresponding research; the existing loading browser runner; its owned-server lifecycle and briefing fixtures; the API loading guide; existing API review tests and actual report/review contracts; and the local gate policy and lock implementation.
* Read repository context in docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md. Memory is context, not acceptance evidence.
* Implementation boundary remains one added scenario function and one invocation in src/api/checks/loading_briefing_browser_check.py, no removals, the directly related README, and dated RPI artifacts. No runtime redesign, replacement runner, authority change or additional specialist dispatch is recommended.
* Assess local assurance readiness, including real successful accept/edit/reject responses, record identity, exact values, immutable-review barriers and unchanged case data. Do not infer live, human, full WCAG/Fluent or UX-specialist acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Ordered RPI and publication requirements; C7; P01-T02 | Partial | Ordered original Review/commit/full gate is present; current-base, self-locking and post-gate exact-head assessment need explicit sequencing, PC-003. |
| Reuse merged UI; C1-C5/W1-W3; P01-T01 | Covered | No new runtime defect is claimed; draft-only labels and existing loading/HAX patterns are preserved. |
| Locked target/function budget; C6; P01-T01 | Covered | Existing runner and fixture/server ownership are explicitly selected; no removals are authorized. |
| Three durable successful outcomes; P01-T01 | Partial | Real actions are specified, but the promised report record does not exist in the report response, PC-002. |
| Exact text/reasons and draft authority; C3-C4; P01-T01 | Covered | Requirements specify exact values, conditional fields and a draft-only disclaimer; assertions must bind them to the same record. |
| Case invariance and repeated-review refusal; P01-T01 | Partial | Explicit goals are credible; resolving observation boundary belongs with the record/history correction in PC-002. |
| API discovery, Ruff, focused mypy and pinned-axe browser checks; P01-T02 | Partial | Named validation is appropriate; prohibited storage/lock locations block literal execution, PC-001. |
| Constructed data, loopback, external outputs and no forbidden files | Partial | Network/data restrictions are good; inherited server scratch and hardcoded lock contradict storage direction, PC-001. |
| UX participation and live AC7; W1/W4/W5 | Covered | Missing specialist deliverable and live verification are honestly disclosed, not silently substituted. |
| Existing responsive axe/loading/retry/motion regressions; C6 | Covered | Plan explicitly retains them; current runner contains these checks. No fresh pass is claimed. |

## Verdict

* Verdict: Revise
* Rationale: The bounded assurance work is appropriate, but execution paths conflict with current storage restrictions, durable-record evidence is underspecified against the actual API, and publication sequencing needs a fail-closed clarification.
* Severity counts: Critical 0; High 2; Medium 1; Low 0.
* Execution readiness: Implementation planning can be corrected directly. Heavy validation and publication remain blocked under the literal current lock/storage contract until a compliant path exists. This is separate from the Complete critique status.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Required validation locations conflict with the current storage boundary

* Related IDs: Non-functional requirements; Locked Test Ownership; P01-T02; C7.
* Evidence: The plan explicitly requires flock -w 600 /tmp/ama-rpi-heavy.lock. tools/rpi-checks.py:2273-2274 hardcodes that same path. src/api/checks/design_system_browser_check.py:233-234 creates repository-local .venv scratch; its owned lifecycle writes synthetic.json and server.log there. The caller requires external generated outputs, and current execution instructions prohibit /tmp and temporary-directory file operations.
* Concern: Naming an external --out directory relocates screenshots/axe results, not the inherited server fixture/logs or lock. External package installation also does not relocate that lifecycle. Existing unittest fixtures use tempfile.TemporaryDirectory(), so their storage prerequisites need explicit checking as well.
* Impact: Literal planned commands cannot satisfy the current file-operation boundary. An alternate lock would not serialize with the existing full gate, and unauthorized harness edits would break the locked scope.
* Smallest useful change: Correct the plan/details to inventory these locations and mark affected validation/publication blocked unless an already authorized, compliant execution arrangement satisfies both shared serialization and storage requirements. Do not run the prohibited commands, silently replace the shared lock, add an unlocked fallback, or broaden the implementation to change the harness/gate. Continue only actions permitted by the established boundary.
* Action owner: Planning parent.
* Exact resolving evidence: Plan/details identify the real lock and fixture/log locations, distinguish external retained outputs from owned scratch, and either cite a concrete compliant existing execution mechanism or explicitly record the validation/publication blocker with no success claim. A storage relocation alone is not resolving evidence for shared-lock compatibility.
* Decision route: Direct planner correction and prerequisite disposition. Existing user direction already fixes scope and prohibits bypasses; no divergent redesign or new user decision is requested by this critique.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: The aggregate report cannot prove the promised exact durable record

* Related IDs: Functional requirements; acceptance criteria; P01-T01; C4/C6.
* Evidence: Phase details promise an exact durable report record. src/api/src/zava_forward/api/server.py:511-519 restricts /api/ai/report to managers. src/api/tests/test_ai_tasks.py:606-608 proves sam@example.test gets 403. src/core/src/zava_forward/core/ai_tasks.py:379-399 returns aggregate counts and recent task/action/reason entries, not record IDs, override text or complete review evidence. The successful review response returns the full record at ai_tasks.py:367-377.
* Concern: The selected sign_in helper authenticates sam@example.test. Even an authorized manager report would not independently establish exact edit text or uniquely identify an accepted record. A captured request and displayed status alone do not establish the claimed subsequent durable history.
* Impact: The scenario can fail at report access, pass against unrelated aggregate history, or overclaim persistence without verifying the same record and its values.
* Smallest useful change: Specify the actual evidence contract before implementation: exact successful response status/body and original record ID for each UI action; a supported independent observation of retained state keyed to that ID; exact expected disposition/reason/override fields; and unchanged state after a second review attempt returns the existing refusal. Identify any separately authenticated constructed manager observation explicitly. Use a supported authorized read or owned synthetic-state observation, not a fabricated report field or new production endpoint. Define whether case invariance covers full constructed case records or only permitted API projections, and describe only that proven boundary.
* Action owner: Planning parent, implemented by the P01-T01 browser-scenario owner.
* Exact resolving evidence: Revised P01-T01 names the real response fields, observer authorization and independent retained-state mechanism; distinguishes aggregate deltas from record-level evidence; and specifies same-ID refusal, no second committed outcome and before/after case equality. The implementation evidence must later show all three successful real API actions without fulfilled synthetic success responses.
* Decision route: Direct planner correction. No change to runtime authority, target ownership, function budget or accepted live/UX limitations is necessary.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Publication details omit the current-base and self-locking exact-head sequence

* Related IDs: User publication requirements; Dependencies; Handoff; P01-T02; C7.
* Evidence: P01-T02 supplies a hardcoded full-gate base and says to fetch/verify before push. Its general heavy-command instruction does not exclude the self-locking gate. src/README.md:109-111 requires the gate's own --lock-timeout 600, not an outer flock; src/README.md:209-217 requires current-base verification before independent exact-head assessment and push.
* Concern: A moved origin/main makes the hardcoded receipt stale. Wrapping the self-locking gate with the same outer lock can block itself. The planned original pre-commit Review is necessary but does not replace the later independent assessment of the committed, gated exact head.
* Impact: An otherwise successful assurance change can time out unnecessarily or reach publication with invalid base/head evidence or missing independent exact-head assessment.
* Smallest useful change: State the sequence explicitly: original independent Review; privacy-safe implementation/evidence commit with the required trailer; fetch and establish the reviewed current main SHA; full --all gate using its internal --lock-timeout 600 and fresh external outputs; fetch again and verify the receipt against current origin/main immediately before independent exact-head assessment and push. If head/base/tool/image/candidate inputs change, preserve the old receipt and rerun; do not silently rebase. Keep outer shared locking for other heavy commands only, subject to PC-001.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T02 names the original Review and distinct post-gate exact-head assessment, dynamically reconciles the reviewed base with fetched main, excludes outer flock for the full gate, and records fail-closed invalidation conditions. Publication evidence must later identify matching HEAD/base, verified full receipt and independent exact-head result.
* Decision route: Direct planner correction; current user direction already requires this sequence.

## Strengths and Residual Risk

* The plan avoids unnecessary redesign and preserves truthful draft-review authority, human approval, resident consent and manual paths.
* Actual real-server success coverage complements, rather than removes, existing adverse-outcome, startup, retry, responsive axe and reduced-motion checks.
* UX invocation returned questions only. The inherited HAX mapping remains parent-authored pattern evidence, not specialist participation or usability acceptance.
* Live AC7 remains unavailable. Refs #531 is appropriate; local assurance must not close whole-issue acceptance.
* General-discovery skips must remain visible and cannot stand in for required browser execution. Missing local prerequisites block publication without cloud fallback.

## Questions or Blocking Evidence Gaps

* No user response is required for the planner-owned corrections.
* PC-001 is an execution prerequisite conflict, not permission to relax the caller's restrictions.
* PC-002 needs a concrete retained-state observer within the existing scope before the implementation is called ready.

## Limitations

* This is a plan critique, not implementation Review or a fresh UI/accessibility audit.
* No API tests, Ruff, mypy, browser/scanner/SQL/full gate, live requests or credential inspection were performed.
* Remote dependency and UX invocation outcomes are assessed as supplied research evidence, not newly reproduced outcomes.
* No plan, details, research, source, existing review or workflow state was changed. Untracked input artifacts were left intact.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Record and resolve or explicitly block the prohibited validation locations, then correct the record-observation and publication contracts.
* User response required: No.
* Complete this disposition from the one full finding set; do not request another critique pass or erase adverse evidence.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/employee-briefing-loading-531-plan.md](.copilot-tracking/plans/2026-10-31/employee-briefing-loading-531-plan.md) | Assessed candidate plan |
| [.copilot-tracking/details/2026-10-31/employee-briefing-loading-531-phase-details.md](.copilot-tracking/details/2026-10-31/employee-briefing-loading-531-phase-details.md) | Assessed implementation details |
| [.copilot-tracking/research/2026-10-31/employee-briefing-loading-531-research.md](.copilot-tracking/research/2026-10-31/employee-briefing-loading-531-research.md) | Supplied research and limitations |
| [.copilot-tracking/reviews/plans/2026-10-31/employee-briefing-loading-531-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/employee-briefing-loading-531-plan-critique.md) | Complete independent critique |

## Next Steps

The active planning parent should directly disposition PC-001 through PC-003 and finalize the plan without another critique. Continue the authorized ordered RPI only where execution prerequisites are satisfied; otherwise record the blocker and stop before the prohibited validation/publication action. No user command or response is required by this critique.
