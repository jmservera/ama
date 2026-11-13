# Research: 891 chat grounding core (2026-11-13)

Disposition: executed. Planning Readiness: Ready.

Read: case study original/addendum (headers), knowledge base index, memory, chat_panel.py, chat_case_answers.py, existing tests.

## Findings

* permitted_sources walks sorted(ctx) and stops at MAX_SOURCES=60, so work.*, waiting_on, hazards (alphabetically late) drop out on rich cases.
* chat_case_answers.INTENTS lacks unblock/safety phrasing; "how can we fix this safety? Should we schedule a visit?" falls to suggestions.
* _ask abstains or withholds (UNGROUNDED) with no deterministic fallback when the model draft is ungrounded.
* _reply has no answer_source, source label or per-citation source_kind.
* ModelUnavailable carries no meter_id/meter_root, so failed dispatched calls are not settled with eligible=False.

## Constraints

* Write surface: chat_case_answers.py, chat_panel.py and their two test files only.
* No banned jargon words in user-visible text. No fallback on WITHHELD security or ACTION_CLAIM, or refused requests.
* Keep case_id == "" abstain behaviour and existing StoredRulesFallbackTests (model == workflow-only on provider failure).
