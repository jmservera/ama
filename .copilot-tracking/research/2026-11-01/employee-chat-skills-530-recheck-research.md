# Research: employee chat skills recheck on main 51657d30 (#530)

* Task: `employee-chat-skills-530-recheck`; branch `feat/employee-chat-agents`; base `origin/main` 51657d30.
* Research disposition: `reused` (PR #541, #579, #634, #680 evidence) plus fresh executed checks. Planning Readiness: `Ready`.

## Findings

* The feature is on main: one chat agent with five skills (`core/chat_panel.py` `chat_skills()` from `assistants.REGISTRY`, plus `general`), design note in `src/api/README.md#employee-chat-with-bounded-skills-530`, launcher `#employee-chat-launcher` outside `#app`, `web/chat.js` and `web/chat-widget.js`.
* Criteria 1 to 7 are covered by merged tests: `api/tests/test_chat_panel.py` (five skills plus general, role scope, audit without content, fallback), `api/checks/employee_chat_browser_check.py` (focus, live region, reduced motion, pinned axe).
* Criterion 8 live part stays unmet: no attested employee sign-in (#612). No source defect found.

## Scope decision

Evidence-only refresh on current main; no source change; `Refs #530`.
