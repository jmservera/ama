# Issue 2195 research: chat routes each question to the right subagent

Task: issue-2195-live. Research disposition: executed. Date: 2026-11-21.

## Scope

Issue #2195 (owner 2026-11-21, demo priority): the chat window must route each
question to the right subagent and show the routing decision (agent name and a
plain-language reason). Criteria, all unticked:

1. Routing decision shown in the reply with agent name and plain-language reason.
2. Unroutable questions stay with the general agent and say so.
3. Human-approval and consent boundaries unchanged.
4. AI-unavailable path still works.
5. Tests.
6. Web changes pass the accessibility and content-standard tests.

## Findings from code

* Employee chat: `src/core/src/zava_forward/core/chat_panel.py` (`ChatPanel._ask`,
  `ask_unstored`). The five subagents are `assistants.REGISTRY` keys
  (`stock-prioritisation`, `assessment-preparation`, `funding-evidence`,
  `works-resident-coordination`, `quality-evidence`) plus `GENERAL`. The caller
  chooses the skill in a select (`web/chat.js`); today nothing routes a question.
* Consent and out-of-scope refusal run before any model call in `_ask`; the AI-unavailable
  path returns `FALLBACK` or rules answers. Routing must be a deterministic pre-step that
  only narrows the skill lens and never adds a model call.
* Resident chat: `src/api/src/zava_forward/api/resident_demo/chat.py` already routes
  a question to a topic (`route()`), with no model subagents; it can show the topic helper
  and reason.

## Planning readiness

Ready. Planning Readiness: Ready.
