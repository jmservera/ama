---
title: Issue 2195 chat routing proof
description: Recorded evidence that employee and resident chat show which agent handled each question and why, with a per-criterion proven and unproven table
ms.date: 2026-11-21
ms.topic: reference
---

## Scope

Issue #2195 (owner feedback 2026-11-21, demo priority): the chat window must send each
question to the right subagent and show that in the reply. This note records what the change
does and the evidence for each criterion. All data is synthetic and the proof is desktop only.

## What changed

* Employee chat: `src/core/src/zava_forward/core/chat_routing.py` scores a question against the
  five agents in `assistants.REGISTRY`. `ChatPanel` (`ask` and `ask_unstored`) attaches a `routing`
  object (`agent`, `agent_name`, `routed`, `reason`, `text`) and uses the routed agent's evidence
  lens. Routing is deterministic: it adds no model call, and the existing refusal, consent
  and fallback checks are unchanged.
* The reply shows a bold line, for example "Routed to the Quality evidence agent. The question is
  about quality checks and inspection evidence."
* A refused request, a question that matches no agent, a tie between two agents and an agent meant
  for other roles all stay with the general agent and say so. A chosen agent in the list is kept.
* Resident chat: `chat.routing()` names the helper for each topic (for example "Case progress
  helper") and the General assistant when none matches; `/demo/assistant` returns it and the widget shows it.
* Limit: the five employee agents are evidence lenses over one bounded model call (existing
  design, one call per question). The routing line names the lens; the existing answer-origin label
  still says whether rules or the model produced the text.

## Evidence

Local synthetic servers (the loopback harness in `src/api/checks`), Playwright desktop 1280 by 900.
Raw results: [Programme Manager](./issue-2195-chat-routing-2026-11-21/employee-routing-pam.json),
[Liaison Officer](./issue-2195-chat-routing-2026-11-21/employee-routing-sam.json),
[resident](./issue-2195-chat-routing-2026-11-21/resident-routing.json).

| Question (role) | Routing shown |
| --- | --- |
| Is the quality inspection evidence complete? (Programme Manager) | Routed to the Quality evidence agent. |
| Can you check the grant claim and invoice? (Programme Manager) | Routed to the Funding evidence agent. |
| Which stock should we prioritise by EPC ranking? (Programme Manager) | Routed to the Stock prioritisation agent. |
| Plan the next resident appointment and handoff (Programme Manager and Liaison Officer) | Routed to the Works and resident coordination agent. |
| Is the grant claim quality checked and which defect? (Programme Manager) | Handled by the General agent: fits more than one agent. |
| Tell me what you can help with (Programme Manager) | Handled by the General agent: no specialist matches. |
| Approve the funding claim for this home (Programme Manager) | Handled by the General agent: no agent can do this; outcome refused. |
| Is the quality inspection evidence complete? (Liaison Officer) | Handled by the General agent: the Quality evidence agent is for other roles. |
| How is my case going? (resident) | Routed to the Case progress helper. |
| What is the weather like? (resident) | Handled by the General assistant. |

Screenshots (each reply with its routing line): [quality](./issue-2195-chat-routing-2026-11-21/emp-pam-quality.png),
[funding](./issue-2195-chat-routing-2026-11-21/emp-pam-funding.png),
[tie](./issue-2195-chat-routing-2026-11-21/emp-pam-tie.png),
[general](./issue-2195-chat-routing-2026-11-21/emp-pam-general.png),
[refused](./issue-2195-chat-routing-2026-11-21/emp-pam-refused.png),
[other role](./issue-2195-chat-routing-2026-11-21/emp-sam-quality.png),
[works](./issue-2195-chat-routing-2026-11-21/emp-sam-works.png),
[resident status](./issue-2195-chat-routing-2026-11-21/res-status.png),
[resident general](./issue-2195-chat-routing-2026-11-21/res-none.png).
The employee server had no model configured, so every employee reply in the run is also the
AI-unavailable path ("The assistant is not available right now", workflow-only help).

Tests run from the worktree (sequentially):

* `src/core`: `test_chat_routing` (12 new), `test_chat_panel`, `test_chat_isolation_single_model_route`: 76 pass.
* `src/api`: `test_resident_assistant_api` (1 new), `test_accessibility_baseline`, `test_content_standard`,
  `test_resident_api`: 81 pass, 1 skipped. Chat suites (`test_chat_panel`, widget, origin badge, consent
  boundary, resident chat, home chat and others): 199 pass, 1 skipped.
* `ruff check` and `ruff format --check` and `mypy` clean in `src/core` (mypy override added for the new
  test module) and `src/api`.

## Criteria

| # | Criterion | Verdict | Basis |
| --- | --- | --- | --- |
| 1 | Routing decision shown in the reply with agent name and plain-language reason | Proven locally | Table and screenshots above; `PanelRoutingTests` |
| 2 | Unroutable questions stay with the general agent and say so | Proven locally | General rows above; `RouteQuestionTests` |
| 3 | Human-approval and consent boundaries unchanged | Proven locally | Refusal and consent checks run before routing text is added; refused row shows outcome refused with 0 model calls; `test_chat_consent_boundary` passes. Not changed: no approval or consent code touched |
| 4 | AI-unavailable path still works | Proven locally | Unavailable model gives the fallback reply with routing (`test_ai_unavailable_still_falls_back_with_routing`; screenshots) |
| 5 | Tests | Proven | Counts above |
| 6 | Web changes pass accessibility and content-standard tests | Proven for the automated tests | `test_accessibility_baseline`, `test_content_standard` pass. The pinned axe browser run was not performed (axe file not available); person-run assistive-technology testing is out of scope for the demo |

Not proven: the deployed apps `ca-cutover-test-demo-api` and `ca-resident-demo` still run the earlier
image, because this task made no deployment (owner rule: no production changes). The live routing
display therefore needs a later image build and deploy by the coordinator.
