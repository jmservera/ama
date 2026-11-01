<!-- markdownlint-disable-file -->
# Employee chat grounded on the selected case: plan (2026-11-01)

Research: [2026-11-01-employee-chat-grounded-research.md](../research/2026-11-01-employee-chat-grounded-research.md). Refs #530.
Validation tier: focused (no `rpi-checks --all`, no `uv`).

## Phases

* [x] 1. Core: `chat_case_answers.py` facts extraction and tolerant rules router.
* [x] 2. Core: `ChatIsolation.case_facts` (projected, authorised) and
  `ChatPanel.ask_unstored` returns grounded replies with case-fact citations.
* [x] 3. Web: employee panel stays open on outside focus; larger default size;
  unstored note shown after the answer.
* [x] 4. Tests: core unit tests for both owner questions on a seeded case,
  phrasing variants, suggestions, negative tests (other case, contractor,
  approve/decide); API test; Node widget test.
* [x] 5. Validation: unittest core and api, ruff check, ruff format --check,
  mypy per project, Chromium employee chat check.
* [x] 6. Evidence: changes and review artifacts; commit, push, PR.

## Critique (single pass, compatible findings applied)

* Do not widen `chat_case` (it feeds the model prompt); build facts separately.
* Keep `fallback` kind for no-case and unmatched questions so existing clients
  and tests are unchanged; grounded replies use kind `answer`, model
  `workflow-only`.
* No model, no storage, no new audit content beyond outcome and skill.
