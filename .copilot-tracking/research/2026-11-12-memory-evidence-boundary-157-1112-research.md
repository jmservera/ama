---
title: Issue 157 memory-as-evidence boundary research
ms.date: 2026-11-12
task_id: memory-evidence-boundary-157-1112
---

## Scope and disposition

Research disposition: `executed`. Planning Readiness: `Ready` for one tests-only slice. Refs #157 only, literal acceptance criterion "No memory is used as evidence for a controlled decision". This is not epic acceptance and is not a generic chat or security audit.

Lineage (read-only, recorded at start):

* Branch `research/memory-evidence-boundary-157-1112`, worktree clean, HEAD `43b2187b918206666c63cb25d8b338be09791118` (tree `67cbe8ede92d4f9f02ac3a3f71d0de06872f6b55`).
* Declared PR target and parent `feat/demo-ai-integration-1112` resolves locally to the same commit and tree (`43b2187b9`, `67cbe8ede`); the remote has no such branch yet. Declared parent integration (#104) targets `main`; `origin/main` is also `43b2187b9`, tree `67cbe8ede`. The parent has not diverged from main.

Excluded (already delivered or owned elsewhere): #159 authenticated 400 receipts, #162 user isolation, #164 poisoning and multi-turn protocol, #1273 SQL/browser mechanics. Parallel ownership: #107 owns `src/api/tests/test_assistant_release.py` and `assistant_process_worker.py`; #153 owns the employee `app.js` confirmed-denial refresh path and its copy tests; #82 owns the missing-funding path in `store.py`. This slice touches none of them.

## Trace of the one path

Synthetic chat/memory -> registered-assistant proposal -> controlled evidence boundary. Current producer and consumer contracts:

* Producer, memory: `ChatPrivacy.add_memory` stores an opted-in item with id prefix `CM-` (`chatthreads.MEMORY_ID_PREFIX`). `prompt_memory` labels each item `authority="none", evidence=False`. Its only consumer in `src` is `ChatIsolation.build_prompt` (`chat_isolation.py`), which is not called by either HTTP turn route: `app.panel.ask` and `ask_unstored` use `ChatPanel`, whose results carry `memory_used=False`.
* Hand-off, chat to assistant: `POST /api/chat/threads/{id}/proposals` (`server.py`) reads only `body["capability"]` and the thread's `case_id`, then calls `app.assistants.invoke(user, capability, case_id)`. No thread content, message or memory is an argument.
* Consumer, assistant: `Assistants.snapshot` and `capture` (`assistants.py`) build the evidence from the case, procurement and consented sensor sources only. `assistants.py` has no reference to chat threads or `chat_memory`. Model citations must be in `snapshot["citations"]` (line 344), keyed `source:*` or `sensor_reading/*`, so a `CM-` id cannot be a valid citation.
* Controlled boundary: the chat thread records an assistant message whose `evidence` is `[proposal id]`; `chatthreads._clean_evidence` refuses any reference starting `CM-` ("Memory is never evidence and cannot be cited"). Proposals are `ready`, then need separate human `verify` and `accept`; `relied_on` needs accepted state (`assistants._view`).

## Existing proof, by hop

| Hop | Proof today | Gap |
| --- | --- | --- |
| Memory off the HTTP turn prompt | `test_chat_isolation.test_prompt_holds_only_own_content_and_projected_case`: memory canary absent from the HTTP turn prompt | None for the turn route |
| Memory is non-authoritative | `test_chat_memory.test_prompt_memory_is_non_authoritative_and_never_evidence` | None |
| Memory id refused as stored evidence | Same test, at `store.chat_add_message` | Not exercised through the proposals route |
| Output citations limited to captured sources | `test_assistants` `bad="citation"` (private id rejected) | Generic; no memory-id case |
| Proposal route denial paths | `test_chat_panel.test_proposal_request_uses_the_assistants_path_and_checks_role` (400, 403, 404 only) | No test reaches the 202 success path |
| Proposal route success with memory present | None found: grep of `src` tests for the chat `proposals` route finds only the denial test above, an endpoint inventory and a JS list | This is the exact hop |

Conclusion: the code already prevents promotion (no data path from `chat_memory` to the assistant snapshot, and the evidence guard exists). The unit hops are proved, but the end-to-end hop (active synthetic memory, successful chat proposal, assistant prompt and snapshot, stored thread evidence, citation attempt) has no explicit test. That is a missing, directly required boundary test for this literal criterion, not a defect.

## Distinct finite history check

Earlier #157 plans (`plans/2026-10-27/agent-chat-157-plan.md` and later 2026-10-29 chat plans) concern thread storage, masked length, SQL roster, audit locking and review fixes. A search of `.copilot-tracking` found no prior correction or exhaustion record for a memory-to-proposal boundary test. No renewed or exhausted correction is involved.

## Constraints carried into the plan

* Tests only; no production file edit. Expected values come from existing contracts (`CM-` prefix, `snapshot["citations"]`, `evidence=[proposal id]`), no new invariant.
* Add the case to the existing `src/api/tests/test_assistants.py` `ApiTests` harness (real `App`, real `SqlStore`, real chat privacy over SQL); it is not owned by #107, #153 or #82. If the shared parallel author touches it, order the merge; no concurrent edit was needed.
* Synthetic fixtures and a local test-double provider only. The provider double is simulated evidence, not a real model, human review, resident trial or production acceptance.
* Preserve the human boundary: the test creates a `ready` proposal and never accepts it; it records that no case record changed.
* The criterion stays unticked; this slice does not prove human acceptance, #440 stabilisation or the other epic criteria.
