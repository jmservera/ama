# Plan: issue #229, browser check for employee AI state distinctions

Research: [research](../research/2026-11-07-issue-229-ai-state-browser-research.md). Details: [details](../details/2026-11-07-issue-229-ai-state-browser-details.md). Tier FOCUSED, test-only.

* [x] Phase 1: add a Playwright-free module with synthetic ai_task records, staff override and expected phrases; wire into the checker fixture.
* [x] Phase 2: add the register browser section plus unavailable and empty intercepted scenarios.
* [x] Phase 3: add a no-browser regression test using the real role-screens.js and the real exception_register contract.
* [x] Phase 4: README note, focused tests, ruff, format, mypy; browser run NOT run (not admitted), recorded as pending.

Critique: executed once before implementation (independent agent); 7 findings applied directly, see the details file.
Non-goals: UI copy, API, schema, auth, SQL, deployment, model, policy, recovery; no full gate, images, scans or cloud.
