---
title: Masked chat question length final-candidate plan critique
description: Independent bounded plan assessment for issue 157 and PR 503
ms.date: 2026-10-29
---

## Metadata

* Task ID: 157-chat-masked-length-2026-10-29
* Task slug: chat-masked-length-157
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/chat-masked-length-157-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/chat-masked-length-157-phase-details.md
* Critique execution status: Complete
* Critique executions: One independent final-candidate assessment.

## Inputs and Criterion Boundary

* Caller requirements: reject redaction-expanded questions above MAX_QUESTION_CHARS with LIMIT_REACHED rather than dispatching truncated text; preserve the raw cap and existing behavior. Validate focused chat suites and Ruff lint/format checks, then commit locally only. No push, az, rubric score edits, generated targets or unrelated work.
* Research: .copilot-tracking/research/2026-10-29/chat-masked-length-157-research.md, especially C1-C5 and the supplied raw 977 / masked 2,297 reproduction.
* Assessed both supplied planning documents in full, including requirements, decisions, dependencies, phase tasks, acceptance criteria, test ownership and fallback behavior.
* Read named implementation evidence in src/core/src/zava_forward/core/chat_panel.py, src/core/src/zava_forward/core/chat_privacy.py and src/core/src/zava_forward/core/chat_isolation.py; owning tests in src/core/tests/test_chat_panel.py; and selected setup/assertion sections of src/api/tests/test_chat_panel.py and src/api/tests/test_chat_isolation.py.
* Consulted src/README.md for validation/publication boundaries and required repository context documents. These do not broaden the functional assessment.
* Boundary: assess whether this candidate is credible for the bounded implementation. Do not execute implementation, tests, independent implementation Review, publication checks or external research.
* Worktree inspection confirmed feat/agent-chat-157 and existing untracked task inputs. This assessment neither modifies nor moves those inputs. PR 503 lifecycle is supplied context, not independently refreshed here.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Functional requirements; C1-C4; P01-T02 | Covered | Existing raw-only guard precedes prompt construction. Adding strict masked-length overflow to the same condition prevents truncating neutralise from receiving an over-cap current question without changing the cap or redactor. |
| Refusal and fallback preservation; C2, C5; P01-T02 | Covered | Refusal remains earlier. The existing finish path preserves masked user and workflow assistant turns, empty citations, workflow-only response and audit/receipt behavior. |
| Regression; C3-C5; P01-T01 | Covered | The exact supplied postcode fixture has explicit raw/masked length assertions and must fail against unchanged source before the fix. Direct panel.ask avoids the helper's dispatch assumption. |
| Seven-mode coverage; P01-T01 | Covered | None, general and five REGISTRY keys each use a fresh permitted case-bound thread. The legacy None mode therefore has real sources and can expose the original dispatch defect rather than passing through lack of context. |
| No-dispatch acceptance; P01-T01 | Covered | LIMIT_REACHED, fallback kind, workflow_only, workflow-only model, empty citations, model_calls == 0 and an empty prompt spy jointly distinguish the intended refusal from a post-dispatch fallback. |
| Inclusive boundary; P01-T01 | Covered | The distinct 989 raw / 1,000 masked fixture requires one model call and the complete masked question at the end of the actual Question field. This catches accidental greater-than-or-equal admission or retained truncation. |
| Test ownership and scope lock | Covered | At most two new StoredQuestionTests methods, no removals, no generated targets and no unrelated implementation changes are explicit. Existing storage-expansion tests remain intact. |
| P02-T01 validation | Covered | Four core chat modules and two API chat modules exercise the affected path and surrounding privacy/isolation/storage contracts. Commands specify project directories, interpreter and shared fixture paths, plus core-wide Ruff check and format --check. Counts, exits and skips must be recorded. |
| Dependencies and missing prerequisites | Covered | Red reproduction precedes the source fix; both P01 tasks precede focused validation; reconciliation precedes independent Review and local commit. Dependency restoration follows an actual missing-dependency failure rather than speculative installation. |
| P02-T02 evidence and delivery | Covered | One independent implementation Review, preservation of original outcomes, dated evidence, scoped local commit, privacy-safe identity and co-author trailer are planned. Neither a local commit nor deferred Review findings establish approval. |
| Publication and authority boundaries | Covered | No push, az or rubric edit is authorized. Focused success is not a full publication receipt, hosted approval or live acceptance; those gates remain outside this local-only delivery. |

## Verdict

* Verdict: Pass
* Rationale: The proposed surgical guard change addresses the evidenced defect. The two-test design proves both expanded-overflow rejection and inclusive-boundary dispatch while retaining all existing tests. Sequencing, validation and local-only delivery are concrete and sufficient for this scope.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.

## Findings

No actionable PC-xxx findings within the supplied criterion boundary. No substantive correction or unresolved user decision is required.

## Strengths and Residual Risk

* The overflow regression is not vacuous: a case-bound legacy thread, injected model and prompt spy expose the existing model dispatch.
* The acceptance fixture verifies actual prompt semantics, not just a successful return kind; the fixture model returns an unusable reply, so a model-produced answer is appropriately not required.
* Redaction, storage schema, refusal precedence and neutralisation behavior are deliberately unchanged. Stored expanded text remains subject to existing storage bounds.
* Research-reported fixture lengths and environment availability are supplied evidence, not fresh execution results from this critique. Implementation must produce the planned red/green and validation evidence.
* Existing privacy approvals, hosted/human acceptance and complete publication checks remain unestablished. The plan explicitly retains these boundaries rather than using focused checks to waive them.
* A single future Review execution is not a promise of a passing outcome. Preserve its actual result and any routed findings without describing a non-passing candidate as independently accepted.

## Questions or Blocking Evidence Gaps

None for the bounded implementation decision.

## Limitations

* No tests, lint, formatting checks, provider calls or implementation Review were executed.
* No upstream status, authenticated commit identity or installed environment was refreshed; the implementer retains responsibility for the planned delivery checks.
* No unrelated files or prior task artifacts were assessed. Plan, phase details, research, source and tests remain unchanged by this critique.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: Record this Pass disposition, finalize the candidate and continue P01-T01 with the unchanged-source regression run.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/chat-masked-length-157-research.md](.copilot-tracking/research/2026-10-29/chat-masked-length-157-research.md) | Supplied focused research and C1-C5 evidence. |
| [.copilot-tracking/plans/2026-10-29/chat-masked-length-157-plan.md](.copilot-tracking/plans/2026-10-29/chat-masked-length-157-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-29/chat-masked-length-157-phase-details.md](.copilot-tracking/details/2026-10-29/chat-masked-length-157-phase-details.md) | Assessed execution details and validation commands. |
| [.copilot-tracking/reviews/plans/2026-10-29/chat-masked-length-157-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/chat-masked-length-157-plan-critique.md) | This original independent critique. |

## Next Steps

The active planning parent may record Pass and continue the owner-authorized implementation. No repeat critique or user action is required. This critique stops here; it does not execute implementation or Review.
