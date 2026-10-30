---
title: Chat panel gate plan critique
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: #572, chat-panel-test-in-gate-572.
* Critique date: 2026-10-30.
* Plan: .copilot-tracking/plans/2026-10-30/chat-panel-test-in-gate-572-plan.md.
* Phase details: .copilot-tracking/details/2026-10-30/chat-panel-test-in-gate-572-phase-details.md.
* Critique execution status: Complete.
* Original verdict: Revise. This is the single independent final-candidate critique, not an implementation review.

## Inputs and Criterion Boundary

* Caller requirements: own the existing exact chat-panel case in the local Chromium gate, include its flag and command/coverage inventory, reject unexpected skips, add regression coverage within four added methods with no removals, and obtain a fresh committed exact-head complete gate including SQL. No product/UI/workflow changes, cloud, deployment, paid inference, real sign-in, credential files, secret access or push.
* Supplied research: .copilot-tracking/research/2026-10-30/chat-panel-test-in-gate-572-research.md, including C1-C7 and the rejected broad-allowlist/all-discovery alternatives.
* Source evidence: relevant portions of tools/rpi-checks.py, tools/test_rpi_checks.py, src/api/tests/test_chat_panel.py and its src/api/tests/test_role_matrix.py fixture; the local-gate and exact-case guidance in src/README.md and src/api/README.md.
* Project context: docs/case_study_48_original.md, opening scope of docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md. These do not supply test execution evidence.
* Selected branch: fix/chat-panel-test-in-gate-572. The supplied research records selected HEAD/base 5634f9a077d175a931c15e3400114665d8c071ee. No branch/base reselection is proposed.
* Assessment covers AC1-AC4, P01-T01 through P02-T03, dependencies, scope controls, regression feasibility and receipt verification. It establishes planning credibility, not implementation correctness, actual Chromium/SQL success, hosted approval or publication eligibility.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC1; C3-C5; P01-T02 | Covered | Plan requires identical exact selector, opt-in flag, own/shared fixture paths, verbose output, suite accounting and integration semantics in both required_checks and Runner.browser. |
| AC1; P01-T03 | Covered | Command manifest plus component ownership/reproduction documentation are planned; existing workflow coverage maps the project job to browser without requiring a hosted workflow change. |
| AC2; C1; P01-T01 | Covered | Exact ID/reason exception is restricted to project-api non-integration accounting, with group context propagated through runtime and verification. Existing global reasons and SQL exception remain unchanged. |
| AC3; C6; P01-T03 | Covered | At most four added gate methods, no removals, runtime-dispatch mocks, negative exception cases, receipt mutations and the existing eight-to-nine suite fixture adjustment are feasible within the current owner. |
| Receipt integrity; P01-T01/P01-T03 | Covered | verify_commands compares trusted command identity and re-parses logs; the plan explicitly adds matching exception context and browser mutation coverage. Missing, changed, failed, skipped and zero-execution evidence remain rejection requirements. |
| AC4; C7; P02-T01/P02-T03 | Partial | Exact-head commit, full --all, SQL, fresh external receipt, base fetch and verification are required, but the specified execution paths conflict with the active filesystem restriction; PC-001. |
| Independent review; P02-T02 | Covered | One original implementation Review, preserved adverse findings and separate human/hosted/coordinator boundaries are explicit. Later candidate/input changes still invalidate receipts. |
| Scope, safety, branch/base and budget | Covered | No product test rewrite, UI/workflow edit, new harness, broad skip exception, push or issue-closing claim is planned. |

## Verdict

* Verdict: Revise.
* Rationale: The proposed gate change and bounded regressions are credible. Validation is not executable as written under the active no-/tmp/no-temporary-directory restriction. Correct that operational premise or explicitly retain a blocked full-gate prerequisite before treating the plan as implementation-ready for all four acceptance criteria.
* Severity summary: Critical 0; High 1; Medium 0; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Validation assumes prohibited filesystem access and an unavailable lock workaround

* Related IDs: AC4; P02-T01; P02-T03; research readiness and heavy-lock assumptions.
* Evidence: .copilot-tracking/details/2026-10-30/chat-panel-test-in-gate-572-phase-details.md:45-49 specifies /tmp/mv/bin/python and flock against /tmp/ama-rpi-heavy.lock. P02-T03 relies on the runner taking that lock. tools/rpi-checks.py:2243-2246 hardcodes that same path and opens it with create/read-write flags. The active execution restriction prohibits all /tmp and temporary-directory file operations. Additionally, tools/test_rpi_checks.py:48 and src/api/tests/test_role_matrix.py:178 create TemporaryDirectory fixtures, so simply removing the visible shell paths is not a complete execution-policy assessment.
* Concern: The plan presents the focused checks and complete gate as ready to execute without reconciling this known restriction. Selecting another interpreter or setting TMPDIR does not relocate the runner's hardcoded shared lock. Silently using a different lock would also stop coordinating with existing heavy-gate owners.
* Impact: AC4 cannot currently be promised in this execution environment. An implementer following the details would violate the active restriction or could incorrectly report incomplete/unserialized validation as the required full gate.
* Smallest useful change: Revise P02-T01/P02-T03 to remove prohibited interpreter/scratch assumptions, identify policy-compatible validation storage and fixture handling, and record the hardcoded shared-lock conflict as a blocking execution prerequisite unless a compliant authorized execution context is already available. Preserve global serialization; do not bypass locking, change the shared lock contract opportunistically, use a partial/cloud substitute, or claim a receipt while blocked.
* Action owner: Planning parent for the correction and truthful blocker state; execution coordinator for providing an authorized compatible validation context.
* Exact resolving evidence: Updated phase details and readiness/handoff explicitly account for interpreter, fixture/cache/output paths and the unchanged shared lock under the applicable execution policy. To clear AC4 rather than merely document its blocker, retain actual successful full --all logs and external receipt at the committed candidate, showing real browser and MSSQL execution, followed by successful --verify-receipt against freshly fetched current origin/main in that compliant context. No source change or receipt produced by this critique establishes that evidence.
* Decision route: Direct planner correction and prerequisite routing. No user decision is needed to preserve the restriction or report blocked validation. Any proposed policy exception or material lock-contract/scope change is not authorized by this critique and must not be inferred from it.

## Strengths and Residual Risk

* The exact selector already owns a constructed-data loopback server and fake model, and blocks off-origin browser requests. Required execution therefore need not add a browser harness, sign in to a real service or call paid inference.
* The discovery exception preserves the actual enumerated skip rather than concealing it. Integration remains strict and the general allowlist is not broadened.
* Runtime and manifest are separate definitions today; the planned isolated runtime-dispatch assertion is important evidence beyond merely finding a selector in required_checks.
* The existing full-receipt test already rejects each missing required command. Browser-specific flag/selector/skip mutations complement that shared verification coverage within the locked method budget.
* The research explicitly acknowledges that real gate prerequisites or unrelated failures may block completion. Such failures must remain adverse evidence, not invite out-of-scope UI fixes, skipped SQL or substituted historical receipts.
* Original implementation Review is not final publication approval. Coordinator exact-head assessment and retained human/hosted gates remain separate, as the plan states.

## Questions or Blocking Evidence Gaps

* No unresolved product or branch/base choice requires a user answer.
* A policy-compatible execution context for the required unchanged shared lock has not been established in the supplied materials. This blocks successful validation claims, not the source-level assessment above.

## Limitations

* Read-only assessment of supplied plans and relevant source; no gate, browser, SQL, deployment, sign-in or model call was executed.
* Research's historical 31-test result was not rerun and is not fresh candidate evidence.
* The GitHub issue was represented by the supplied research rather than independently retrieved; no external research was performed.
* Only this critique artifact was written. Plans, phase details, research, session state and source remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Correct the validation premises and explicitly route the shared-lock execution blocker, then finalize this single critique's disposition without commissioning another critique.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/chat-panel-test-in-gate-572-plan.md](.copilot-tracking/plans/2026-10-30/chat-panel-test-in-gate-572-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/chat-panel-test-in-gate-572-phase-details.md](.copilot-tracking/details/2026-10-30/chat-panel-test-in-gate-572-phase-details.md) | Validation correction target |
| [.copilot-tracking/research/2026-10-30/chat-panel-test-in-gate-572-research.md](.copilot-tracking/research/2026-10-30/chat-panel-test-in-gate-572-research.md) | Supplied evidence and decisions |
| [.copilot-tracking/reviews/plans/2026-10-30/chat-panel-test-in-gate-572-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/chat-panel-test-in-gate-572-plan-critique.md) | Original single critique and complete finding set |

## Next Steps

The active planning parent should disposition PC-001 directly, preserve this original Revise verdict and finalize the plan with accurate validation readiness or blocker status. No additional critique or user action is required. Do not execute prohibited filesystem operations or claim AC4 until its execution prerequisite is resolved and fresh exact-head evidence exists.
