---
title: Employee skills chat 530 final-candidate plan critique
description: One independent bounded assessment of the local test and evidence plan
ms.date: 2026-10-30
---

## Metadata

* Task ID: 530
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/employee-skills-chat-530-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/employee-skills-chat-530-phase-details.md
* Research: .copilot-tracking/research/2026-10-30/employee-skills-chat-530-research.md
* Critique execution status: Complete
* Assessment count: exactly one independent final-candidate plan critique; no delegation or further critique.
* Observed branch and HEAD: feat/employee-skills-chat-530 at 5634f9a077d175a931c15e3400114665d8c071ee, matching the supplied baseline.
* Initial worktree: supplied research, plan, details and workflow state were untracked. They were read without moving, committing or modifying them. Read-only remote inspection returned no matching branch or PR.

## Inputs and Criterion Boundary

The assessment covers the supplied research, plan and phase details, the current
issue #530 body, and their referenced implementation, test, browser and historical
Review evidence. The issue remains open with seven checked criteria and the
combined local/SQL/separate-live criterion unchecked.

The implementation is already merged. The authorized change is at most two new
test methods and needed imports in src/core/tests/test_chatthreads.py,
ChatBehaviour, plus src/api/README.md and canonical new RPI evidence. No
removals, runtime change, UI redesign, new harness or router is authorized.

Requirements assessed include six explicit selections, bounded cited answers,
one model call per successful answer, owner isolation, unavailable-model
fallback, metadata-only question references, persistence after reopen and
unchanged case records. Validation includes focused tests, requested complete
API discovery, component static checks, the existing local browser/axe check
and actual owned SQL Server execution. Live/model/human acceptance, Azure,
deployment, credentials on disk, publication receipts and push remain outside
authorization. A synthetic SQL password is permitted only in memory.

The dependency on employee journey PR #529 is recorded as merged. Docker,
the SQL image and mssql_python availability are research-reported prerequisites,
not independently exercised during this critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC1-AC7; research C2-C5 | Covered | Existing API guide, source and HTTP tests support reuse rather than replacement. Checked issue boxes are historical status, not new execution evidence. |
| P01-T01; six selections and grounding | Covered | ChatPanel accepts REGISTRY keys and general, adds workflow sources, filters case sources and validates citations. A permitted case-stage citation can exercise all six selections without new runtime code. |
| P01-T01; bounded additions and reuse | Covered | ChatBehaviour is inherited by MemoryChatTests, SqlChatTests and MssqlChatThreads. Two methods can contain selection loops, synthetic callables and assertions without adding another test class or harness. |
| P01-T01; persistence and audit | Covered | Existing factories reopen the same storage location; MSSQL make_store does not wipe on reopen. Planned question/answer/evidence and question-sequence audit assertions exercise real persisted state rather than a copied response. |
| P01-T01; denial, fallback and general context | Covered | The second method separates workflow-only/no-record behavior from foreign-owner rejection before inference. Existing HTTP matrix remains the evidence for role projection; owner denial alone is not represented as full authorization proof. |
| P01-T01; connection lifecycle | Covered | Details explicitly require cleanup of every opened SQL connection. Implementation must register the underlying db.close where the store itself has no close method, including the initial and reopened instances. |
| P02-T01; destructive actual SQL execution | Partial | MssqlChatThreads.setUp calls wipe; connection settings come from process environment. The intended ownership and memory-only boundaries need an executable admission/secret-handling protocol: PC-001. |
| P02-T01; API/static/browser checks | Covered | Fresh component checks and existing employee_chat_browser_check are named. Pinned axe, synthetic loopback server and blocked external browser traffic are required; skipped SQL/browser tests cannot satisfy AC8-local. |
| P02-T02; historical RV-003 and evidence distinctions | Covered | Original Review remains unchanged; fresh logs must establish new outcomes. Local synthetic model and intercepted rendering evidence are not live provider or employee-site evidence. |
| P03-T01; independent Review and local handoff | Covered | One later exact-diff Review, preserved findings, authenticated noreply identity, local commit and no push are consistent with the authorized loop. Adverse findings remain adverse even if the candidate is committed locally. |
| AC8-whole; publication and live follow-up | Covered | Full publication checks invoking Azure are blocked, not replaced by a partial receipt. Live and human acceptance remain explicitly unmet. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 1; Medium 0; Low 0.
* Rationale: The two-test strategy and evidence boundaries are credible. Before destructive actual SQL execution, P02-T01 needs a concrete fail-closed ownership and memory-only secret protocol. This is a direct safety refinement within existing scope, not a reason to redesign runtime code or request a new user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Destructive SQL execution lacks a concrete target-admission and memory-only password protocol

* Related IDs: P02-T01; research C6/Q3; Non-Functional Requirements; AC8-local.
* Evidence: src/api/tests/test_mssqlstore.py:34-47 enables SQL from ZF_TEST_MSSQL and drops the audit trigger and listed tables using connection_string(). Its MssqlChatThreads.setUp at lines 436-446 calls wipe before constructing the shared fixture. src/core/src/zava_forward/core/mssqlstore.py:91-118 derives server, database, port and authentication from environment; authentication defaults to managed identity. The plan requires a newly owned labelled loopback container and memory-only authentication, but the details do not specify how these conditions are positively checked before wipe or how the password reaches SQL Server without persistence.
* Concern: The existing SQL fixture deliberately trusts its supplied environment and provides no container-ownership interlock. Merely creating a disposable container does not ensure the destructive test process targets it. Separately, a conventional Docker password environment option persists the value in container configuration while that container exists; avoiding credential files and deleting the container afterward is not the same as keeping the password only in memory. These are execution-plan gaps, not evidence that a foreign database has been touched or a secret has leaked.
* Impact: A mistaken inherited connection setting can direct destructive setup outside the owned resource. A conventional container launch or unsanitized diagnostic capture can violate the explicit no-persisted-secret boundary even when all tests pass.
* Smallest useful change: Expand only P02-T01 details with a fail-closed protocol before implementation proceeds to SQL. Construct an isolated child environment with all inherited ZF_SQL_* and SQL-test activation values removed, then set the exact owned loopback host, dynamically observed port, synthetic database and explicit password authentication. Verify the captured container ID, issue-specific ownership label, bounded resource settings, expected loopback binding and SQL readiness before enabling ZF_TEST_MSSQL=1. Use a memory-fed launch/bootstrap channel that does not put the password in Docker configuration, command arguments, files or retained logs; do not use password-bearing Docker environment configuration or env files. Bound readiness/test execution and establish exact-ID cleanup on success, failure and timeout, without touching unrelated resources. If those guarantees cannot be met, record actual SQL as blocked rather than weakening them.
* Action owner: Planning parent for the protocol; implementation parent for its bounded execution.
* Exact resolving evidence: Revised P02-T01 plan/details identify the environment isolation, pre-wipe admission assertions, memory-only password-transfer mechanism, time bounds and exact-ID cleanup. Subsequent sanitized execution evidence records only the nonsecret container identity/label, loopback endpoint, image identity, admission/readiness result, MssqlChatThreads test count and zero SQL skips, exit status and cleanup outcome. It must not include full Docker environment inspection, password-bearing connection strings or the password. SQL remains unproven until that later execution succeeds.
* Decision route: Direct planner correction. The user already permits a synthetic memory-only password and prohibits foreign resources and persisted secrets; no significant or divergent user decision is needed.

## Strengths and Residual Risk

* The canonical shared behavior class gives JSON, SQLite and actual SQL the same assertions, avoiding a misleading SQL-only duplicate or production-test changes.
* The planned case-stage citation, per-selection call counts, persisted message evidence, actual question-sequence references and audit-chain verification test observable behavior. Keep per-selection assertions identifiable; a final aggregate call count alone should not replace the required one-call-per-answer checks.
* General mode must expose workflow sources without a case record; model absence/failure must be distinguished from an unauthorized request that must not invoke inference. The plan accounts for both.
* Reopening a store proves persistence across independent store instances, not a Docker/SQL Server restart or process-crash recovery. The supplied plan requires reopen evidence and should report exactly that.
* Existing role-matrix HTTP tests and the local browser check complement the storage tests. Synthetic privacy references enable fixtures only; they do not prove a real DPIA or operational authorization.
* Historical RV-003 remains an original adverse result. New passing local evidence can address its missing-evidence boundary without rewriting that result or closing live/publication criteria.
* Any unavailable prerequisite, failed check or skip remains explicit. The bounded no-Azure/no-live/no-push handoff is not publication eligibility or whole-issue completion.

## Questions or Blocking Evidence Gaps

* No unresolved user choice.
* PC-001 blocks safe SQL execution until the parent specifies the direct correction. The remaining assessment does not require open-ended research.

## Limitations

This was a plan critique, not implementation Review or validation execution.
No tests, static checks, browser session, SQL connection, container, heavy lock,
Azure command, source edit, commit or push was executed. Research-reported tool
availability and prior external test logs were not reproduced. Source inspection
does not establish runtime conformance, model quality, privacy guarantees,
assistive-technology acceptance or operational approval.

Only this critique artifact was written. Plan, details, research, workflow state
and historical Review records remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Record the fail-closed SQL admission and memory-only password protocol in P02-T01, reconcile the compatible critique disposition, then continue the authorized ordered RPI loop.
* User response required: No.
* Do not dispatch another critique. Preserve this Complete / Revise outcome and assess implementation later in the single required independent Review.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/employee-skills-chat-530-research.md](.copilot-tracking/research/2026-10-30/employee-skills-chat-530-research.md) | Supplied focused research and evidence distinctions |
| [.copilot-tracking/plans/2026-10-30/employee-skills-chat-530-plan.md](.copilot-tracking/plans/2026-10-30/employee-skills-chat-530-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/employee-skills-chat-530-phase-details.md](.copilot-tracking/details/2026-10-30/employee-skills-chat-530-phase-details.md) | Assessed phase details |
| [src/core/tests/test_chatthreads.py](src/core/tests/test_chatthreads.py) | Locked shared regression target and JSON/SQLite factories |
| [src/api/tests/test_mssqlstore.py](src/api/tests/test_mssqlstore.py) | Shared MSSQL inheritance and destructive fixture |
| [src/core/src/zava_forward/core/mssqlstore.py](src/core/src/zava_forward/core/mssqlstore.py) | SQL connection environment behavior |
| [src/api/tests/test_chat_panel.py](src/api/tests/test_chat_panel.py) | Existing selection, role, privacy and audit HTTP evidence |
| [src/api/checks/employee_chat_browser_check.py](src/api/checks/employee_chat_browser_check.py) | Existing synthetic local browser/axe check |
| [src/api/README.md](src/api/README.md) | Design decision and local/live acceptance boundaries |
| [.copilot-tracking/reviews/logs/2026-10-29/employee-chat-skills-530-review.md](.copilot-tracking/reviews/logs/2026-10-29/employee-chat-skills-530-review.md) | Preserved original adverse Review including RV-003 |
| [.copilot-tracking/reviews/plans/2026-10-30/employee-skills-chat-530-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/employee-skills-chat-530-plan-critique.md) | This single independent critique |

## Next Steps

The active planning parent should apply the direct PC-001 correction, preserve
this verdict, and continue implementation followed by the single independent
Review. No user action, further critique or peer-stage invocation is required
from this reviewer. Actual SQL remains conditional on safe admission; live
acceptance and publication remain outside this run.
