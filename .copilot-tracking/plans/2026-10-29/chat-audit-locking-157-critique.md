---
title: Chat receipt audit locking final-candidate plan critique
description: Independent bounded assessment for issue 157 and PR 503
ms.date: 2026-10-29
---

## Metadata

* Task ID: 157-pr503-audit-locking-2026-10-29.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/chat-audit-locking-157-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/chat-audit-locking-157-phase-details.md.
* Research: .copilot-tracking/research/2026-10-29/chat-audit-locking-157-research.md.
* Critique execution status: Complete.
* Assessment: exactly one independent final-candidate critique.
* Observed branch: feat/agent-chat-157; HEAD feccc77d.
* Read-only GitHub inspection confirmed PR 503 is open from that branch to main.

## Inputs and Criterion Boundary

* Caller requirements: serialize final chat.turn receipts, chat.answer and the
  panel's indirect chat.message.added events; retain inference outside newly
  acquired locks; preserve JSON/SQLite nesting and existing behavior; demonstrate
  the rejected-turn race using real hash-chain verification.
* Assessed the complete supplied plan, phase details and completed research
  conclusions C1-C9 against the relevant production code and existing core
  test_chat_panel.py fixtures. Consulted the existing component README, core
  tooling configuration and local-gate documentation for their stated contracts.
* Accepted decisions: module-scoped correction, existing reentrant locks, no
  global-store redesign, synthetic data and injected models only, no source
  changes outside chat_panel.py, existing core test owner and README update.
* Locked test ownership: src/core/tests/test_chat_panel.py; no removals; at most
  five new test methods and one small concurrency helper; no generated fixtures
  or changes to existing API/agents tests.
* Validation and closeout requirements: focused core/API/agent selectors using
  the caller's existing /tmp/mv interpreter, explicit sibling paths, Ruff check
  and format --check, dated original RPI evidence, one independent subsequent
  Review, and a local Conventional Commit with the Copilot trailer. No push,
  Azure operation or rubric JSON edit is authorized.
* This is implementation-readiness assessment, not implementation acceptance,
  a test run, publication approval or wider issue 157 acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Final receipt serialization; AC1; C1/C3 | Covered | chat_panel.py:374-377 calls the unlocked JSON audit path. P01-T03 encloses the final receipt itself in store.lock, including exceptions raised inside the existing try block. |
| Answer serialization; AC2; C2 | Covered | chat_panel.py:403-415 persists the assistant message and then audits chat.answer. P01-T03 keeps both operations in the same short lock section. |
| Indirect message events; AC2; C5 | Covered | chatthreads.py:317-342 releases repo.txn before _chat_event. Enclosing each complete panel chat_add_message call covers its post-transaction audit, unlike locking only repo persistence. |
| Inference availability; AC3; C6 | Covered | The model call follows question persistence and precedes finish. P01-T03 leaves that call, prompt construction and ordinary reads outside the new sections. P01-T01 requires a different thread to complete a locked append during the model callback. |
| JSON nesting; AC4; C3/C5 | Covered | Store initializes threading.RLock; MemoryRepo.txn reacquires that same lock. P01-T01 explicitly exercises nested callers with genuine ledger verification. |
| SQLite nesting and persistence; AC4; C4/C8 | Covered | _SyncLock has per-thread reentrant depth; SqlRepo.txn uses separate reentrant dblock. SqlStore.audit queues at positive depth, and _finish flushes at outermost exit. The plan explicitly requires real SQLite persistence and audit flushes rather than mock counts. |
| Genuine deterministic regression; AC1; C7/C9; P01-T01/P01-T02 | Covered | Existing JSON/SQLite fixtures support synthetic coverage. Capturing predecessor arguments before a bounded builder barrier exposes the unlocked fork; timeout/broken-barrier continuation permits serialized callers. Whole-chain verification, exact outcomes/counts, zero rejected dispatches and a subsequent locked append guard against a mock-only or tail-only success. |
| Completed and refused turns; AC2; P01-T01 | Covered | Phase details require completed turns, while the plan's AC2 includes refused turns and message events. These exercise question persistence and finish in addition to the rejected receipt path. |
| Bounded implementation and documentation; P01-T03 | Covered | Three persistence sections and the existing per-user chat storage README section are identified. No schema, lock hierarchy, dependency or unrelated module change is proposed. |
| Test ownership and maximum additions; P01-T01 | Covered | All new coverage belongs to the existing core panel test file. Subtests can cover both stores and outcome variants within the five-method/one-helper ceiling; no removal or sibling test edit is needed. |
| Focused validation; AC5; P01-T04 | Covered | Details specify interpreter, core selectors and sibling source/test paths; API's same-named panel module runs separately with API paths first. Ruff checks cover changed Python files. Mypy is supplementary, not substituted for required checks. |
| Independent Review and evidence; AC6; P02-T01 | Covered | One actual-diff Review must assess tests and SQL queued-audit behavior; its original result is preserved, not replaced through repeat Review. Material open findings remain visible rather than becoming an acceptance claim. |
| Local commit and publication boundary; AC6; P02-T02 | Covered | Details require authenticated account lookup, repository-local privacy-safe email, fix(chat), Refs #157 and the coauthor trailer. No push or full publication receipt is claimed; complete publication gates remain prerequisites for later publication. |

## Verdict

* Verdict: Pass.
* Rationale: the proposed lock boundaries match the actual direct and indirect
  audit call sites, respect the two repository transaction models, and avoid
  enclosing inference. The regression plan can establish the original failure
  and the corrected real-chain behavior without expanding the agreed scope or
  test budget.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.

## Findings

No actionable PC-xxx findings were identified within the supplied criterion
boundary. No planner correction or significant/divergent user decision is
required. No additional finding set is reserved for another critique pass.

## Strengths and Residual Risk

* The question-message section is included explicitly, closing the indirect
  audit gap that a receipt-only fix would leave.
* The original-failure step requires a genuine failed chain assertion before
  the source fix; the later ordinary locked event also checks predecessor
  continuity beyond the concurrent receipts.
* SQLite queueing is recognized explicitly. A nested call's successful return
  alone is not the proposed persistence evidence: genuine outer-exit flushes
  and a valid persisted ledger remain required.
* The plan explicitly accepts that cross-process JSON writers and other
  modules' unlocked writes are outside this correction. This Pass makes no
  global thread-safety claim.
* Existing exception behavior and receipt/privacy contracts remain in scope;
  the plan does not authorize moving initial current_user authorization into
  the receipt try/finally or otherwise expanding which rejected calls emit
  receipts.
* Local-only closeout does not waive later complete publication, hosted or
  human gates, and does not establish operational or epic acceptance.

## Questions or Blocking Evidence Gaps

None for deciding whether this bounded plan is credible for implementation.

## Limitations

* No source changes, regression execution, Ruff execution, dependency
  installation, implementation Review, commit or publication was performed by
  this critique. Interpreter availability and future test results are not
  independently certified here.
* Timeout values, worker completion/error propagation, assertion placement
  after SQLite outer-lock exit and the final test-method allocation remain
  implementation details to assess in the planned Review, not observed
  implementation evidence.
* Supplied research conclusions were checked against relevant local code.
  No new research cycle, global-store audit, live data/model access, SQL Server
  execution or legal/operational assessment was undertaken.
* Existing untracked plan, details, research and session-state inputs were
  retained unchanged. This critique writes only its designated output file.

## Recommended Next Action

* Highest-impact finding: none.
* Action owner: planning parent.
* Smallest next action: record this original Complete / Pass disposition and
  proceed to P01-T01 and P01-T02 under the locked test budget.
* User response required: no.
* No further critique pass is requested.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/chat-audit-locking-157-plan.md](.copilot-tracking/plans/2026-10-29/chat-audit-locking-157-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/chat-audit-locking-157-phase-details.md](.copilot-tracking/details/2026-10-29/chat-audit-locking-157-phase-details.md) | Assessed task details |
| [.copilot-tracking/research/2026-10-29/chat-audit-locking-157-research.md](.copilot-tracking/research/2026-10-29/chat-audit-locking-157-research.md) | Supplied C1-C9 evidence and scope decisions |
| [.copilot-tracking/plans/2026-10-29/chat-audit-locking-157-critique.md](.copilot-tracking/plans/2026-10-29/chat-audit-locking-157-critique.md) | Original independent critique |

## Next Steps

No user action is required. The planning parent may record this disposition and
continue the authorized implementation and validation stages. This independent
critique stops here without editing its inputs, implementing, committing or
launching another agent.
