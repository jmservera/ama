# Details: issue 749 stored chat rules fallback

Recorded after implementation (2026-11-01).

## Phase 1

* File: `src/core/src/zava_forward/core/chat_panel.py`.
* Add `RULES_NOTE`. In `_ask`, if `kind == "fallback"`, text is `FALLBACK` and `case_id` is set, load `iso.case_facts` for the current user; if facts exist, call `grounded_answer`, append the note and keep only cited sources. Model name is workflow-only.
* Unchanged: out-of-scope refusals, limit-reached and withheld paths. Explain-only; no record changes.

## Phase 2

* `src/core/tests/test_chat_panel.py`: new `StoredRulesFallbackTests`.
* `src/api/tests/test_chat_panel.py`: fallback cases now expect kind answer, model workflow-only, citations present.
* `src/api/tests/test_ai_consumption_api.py`: prompts changed to an out-of-scope "Tell me a story." so the provider call path is still exercised.
* `src/agents/tests/test_chat_eval.py`: `non_ai_panel_answers` now expected greater than 0.

## Phase 3

Live verification after redeploy is left to the owner.
