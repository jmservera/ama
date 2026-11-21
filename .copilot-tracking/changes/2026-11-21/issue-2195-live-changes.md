# Issue 2195 changes record

Date: 2026-11-21. Status: implemented. Tier FULL applies (src changed); the coordinator runs the gate. Only targeted tests were run; `rpi-checks.py --all` was not run.

## Files changed

* `src/core/src/zava_forward/core/chat_routing.py`: new deterministic router `route_question`.
* `src/core/src/zava_forward/core/chat_panel.py`: `ask` and `ask_unstored` add `routing`; the routed agent becomes the evidence lens.
* `src/core/pyproject.toml`: mypy override for the new test module.
* `src/core/tests/test_chat_routing.py`: 12 new tests.
* `src/api/src/zava_forward/api/web/chat-widget.js`, `chat-widget.css`, `chat.js`: visible routing line.
* `src/api/src/zava_forward/api/resident_demo/chat.py`, `app.py`, `web/assistant.js`: resident helper routing.
* `src/api/tests/test_resident_assistant_api.py`: 1 new test.
* `docs/reference/research/issue-2195-chat-routing-2026-11-21.md` and its folder, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

* core: 76 chat tests pass; ruff check, ruff format and mypy clean for changed files.
* api: 81 pass (1 skipped) including accessibility baseline and content standard; 199 pass across chat suites; ruff and mypy clean.
* Playwright desktop on local synthetic servers: Programme Manager, Liaison Officer, resident (see research note).
* Not run: pinned axe browser check (axe file unavailable), person-run assistive-technology testing (out of scope), Azure deployment (no production changes).

## Per-criterion table

| # | Criterion | Verdict | Evidence |
| --- | --- | --- | --- |
| 1 | Routing shown with agent name and plain reason | Proven locally | Research note table, screenshots |
| 2 | Unroutable questions stay general and say so | Proven locally | Research note, router tests |
| 3 | Approval and consent boundaries unchanged | Proven locally | No approval or consent code changed; refusal case; consent suite passes |
| 4 | AI-unavailable path works | Proven locally | Fallback reply carries routing; unit test and screenshots |
| 5 | Tests | Proven | Counts above |
| 6 | Accessibility and content-standard tests pass | Proven for automated tests only | Both test files pass |

Live deployed display: unproven; the deployed apps run the earlier image.

## Divergences

None. Critique findings PC-001 to PC-004 were applied.
