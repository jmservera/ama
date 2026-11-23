# Research: issue 2311 live re-run (2026-11-23)

Disposition: executed. Planning Readiness: Ready.

Finding: all four criteria are already delivered on main by a04f370c40 (registry of 13 contracts, `ai_prompts.render` enforcement, tests). Live Azure is not needed; every criterion is code and tests.

Remaining code gap (the earlier follow-up): the contract for `chat-case-conversation` is declared but the chat prompt builder in `chat_panel.py` does not call `task_contracts.enforce`, so an over-long or prohibited-content context could reach the model. Assistant and concern-pack builders are the same class of gap and stay later work.

Chosen change: call `enforce` in `ChatPanel` before the model call, with fields `question` (masked) and `case_facts` (source JSON); a refusal gives the existing fallback and no model call. Regression test in `test_chat_panel*`.
