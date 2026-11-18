# Research: unblock/visit chat grounding (Refs #164, Refs #159)

* Disposition: executed. Planning Readiness: Ready.
* Modules are `src/core/.../chat_case_answers.py` and `chat_panel.py` (not `src/api`); UI is `src/api/src/zava_forward/api/web/chat.js`.
* Existing: `unblock` intent routes rules-first (`decision-rules`, `answer_origin=decision_rule`, workflow/safety-sequence and visit-consent citations). Ungrounded generative drafts already fall back to rules.
* Gap: phrasings such as "can we book a visit?", "what should we do to get this moving?" missed the intent and could reach the model and be withheld (`Sources (0)`).
* Gap: chat footer derived the label from `answer_source` only, without naming the origin token.
* Decision: withheld action-claim drafts stay withheld (existing test `test_no_fallback_for_withheld_actions_or_refusals`).
* Env note: editable installs point at the main checkout, so tests need `PYTHONPATH` set to this worktree's `src/*/src`.
