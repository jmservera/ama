# Issue 2195 plan: visible question routing in employee and resident chat

Task: issue-2195-live. Date: 2026-11-21. Tier: FULL applies because src changes; the
coordinator runs the gate. This task runs targeted tests only.

## Design

* New pure module `src/core/src/zava_forward/core/chat_routing.py`: `route_question(question, skill, role, refused)`
  returns `{agent, agent_name, routed, reason, text}`. Keyword scoring over the five
  `assistants.REGISTRY` agents. No model call, no I/O.
* Employee chat: routing applies only when the selected skill is `general`. A chosen agent stays
  as chosen (`routed` false, text says the user chose it). A refused question, an unroutable question,
  a tie and a role the agent is not for all stay with the general agent and say so.
  The routed agent becomes the effective skill lens (`skill_sources`), so the answer uses that agent's sources.
* `ChatPanel._ask` and `ask_unstored` add `routing` to every reply, after the refusal, consent and
  limit checks are unchanged; routing never adds a model call, so the AI-unavailable fallback is the same path.
* Employee UI: `chat.js` passes `answer.routing.text` to `chat-widget.js`, which renders a visible
  line `Routing: ...` in the assistant message (plain language, no banned terms).
* Resident chat: `chat.routing(question_topic)` maps each topic to a named helper with a short reason;
  `resident_demo/app.py` returns `routing` and `assistant.js` shows it. Unrouted questions say
  the general assistant keeps them.

## Phases

1. Router module and core tests (`src/core/tests`).
2. Wire `chat_panel.py` (stored and unstored paths).
3. Wire employee and resident UI and API.
4. Tests: core router and panel integration, api resident, a11y baseline, content standard, mypy, ruff.
5. Live proof: deploy is not changed (no production changes); prove through a local server run with Playwright
   against the local app, and read-only live checks of the deployed apps where possible.
6. Research note with per-criterion proof; changes record.

## Success criteria

Each of the six issue criteria has a test or recorded evidence; unproven items are stated.
