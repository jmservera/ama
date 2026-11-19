# Plan: #164 officer chat consent boundary (2026-11-14)

* `chat_case_answers.RULES`: add `workflow/ai-consent-boundary` plain-language rule naming the manual case-card path.
* `chat_isolation.ChatIsolation.ai_consent_state`: read the raw case consent state.
* `chat_panel`: after the existing out-of-scope refusal and before any prompt build or model call, return a deterministic `decision-rules` answer citing the workflow rule when consent is not `Given`; same guard in `ask_unstored`.
* Add `src/api/tests/test_chat_consent_boundary.py`: zero model calls, withdrawn and missing states, given unchanged, absent unchanged, plain-language limits, UI label and accessibility source checks, no case mutation.
* Validation (focused tier): unittest, ruff check, ruff format --check, mypy.
* Critique (once): risk is changing behaviour for existing cases; mitigated by treating an absent field as legacy. Applied directly.

## Cycle 1 correction

Plan: split the line, rerun ruff, mypy and focused tests, correct the changes record. Refs #164.
