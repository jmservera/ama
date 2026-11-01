<!-- markdownlint-disable-file -->
# Employee chat grounded on the selected case: changes (2026-11-01)

Plan: [2026-11-01-employee-chat-grounded-plan.md](../plans/2026-11-01-employee-chat-grounded-plan.md). Refs #530.

## Added

* `src/core/src/zava_forward/core/chat_case_answers.py`: case facts from the
  user's projected card and a tolerant rules router (funding, blocked, missing,
  next step, owner, status, suggestions). Unrecorded facts are stated plainly
  with who to ask. No model, no storage.

## Changed

* `chat_isolation.py`: `case_facts` (same projection and authorisation as
  `case_context`).
* `chat_panel.py`: `ask_unstored` answers from the case, cites case facts
  (`ZF-n/path`), keeps refusal of approve/decide requests first, appends a
  short rules-only and nothing-saved note. Kind `answer` for grounded replies,
  `fallback` for no case or unmatched questions (with suggested questions).
* Web: employee panel no longer closes on outside focus; default size 40vw by
  80dvh (resident default 35 by 70); minimum width raised; rules replies are
  labelled "Summary by rules".
* Tests: core `GroundedUnstoredTests`; API unstored route; Node widget tests.

## Not changed

* Stored chat, memory, DPIA and lawful-basis checks; consumption controls. A
  stateless model answer was not added (see research follow-up).

## Validation (focused tier)

* core `chat*` unittest 112 OK; api `chat*` unittest 83 OK (1 skip, pre-existing).
* `ruff check`, `ruff format --check` clean in core and api; core `mypy` clean.
* api `mypy`: 4 errors in `tests/test_ai_consumption_api.py` (missing
  `zava_forward.agents` stubs), identical at baseline.
* Chromium `employee_chat_browser_check`: fails at the late-success route case
  (workspace text timing) both on baseline and on this change, before the
  sizing steps; sizing is covered by the Node widget tests. Not a pass.
