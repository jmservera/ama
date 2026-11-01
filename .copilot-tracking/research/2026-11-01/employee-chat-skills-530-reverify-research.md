# Research: employee chat skills re-verification on current main (#530)

* Task: `employee-chat-skills-530-reverify`; branch `feat/employee-chat-agent-skills`; base `origin/main` efebfc6d.
* Research disposition: `reused` (prior evidence adequate) plus fresh executed checks. Planning Readiness: `Ready`.

## Findings

* The feature is already on main: PR #541 (one chat agent, five skills, design note in `src/api/README.md#employee-chat-with-bounded-skills-530`), PR #579 and PR #634 (verification records), PR #545 (redeploy).
* Criteria 1 to 7 are covered by merged tests: `core/chat_panel.py` (`chat_skills()` from `assistants.REGISTRY`, labels, sources, fallback, audit), `api/tests/test_chat_panel.py` (all five skills plus general, role scope, audit without content), `api/checks/employee_chat_browser_check.py` (focus, live region, reduced motion, axe).
* The launcher `#employee-chat-launcher` is a body-level control outside `#app`, so it is present on every signed-in employee screen.
* Criterion 8 live part stays unmet: no attested employee sign-in (#612). No source defect is known.

## Scope decision

Evidence-only refresh at current main: focused tier plus the employee chat browser and axe check. No source change; `Refs #530`.
