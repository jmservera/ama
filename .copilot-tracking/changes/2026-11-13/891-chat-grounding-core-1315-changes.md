# Changes: 891 chat grounding core

* chat_case_answers.py: `unblock` intent and answer (human-action note first, open safety items, then recorded stops).
* chat_panel.py: priority-first permitted_sources (MAX_SOURCES kept at 60 for the prompt budget), tightened SYSTEM, skill-scoped decision-rules fallback for abstain/ungrounded drafts, answer_source, answer_source_label, citation source_kind, ModelUnavailable meter_id/meter_root copied to receipt.
* Tests: UnblockTests, HybridAttributionTests (RED first, then green).

Validation: unittest chat_case_answers 7, chat_panel 53, ai_consumption 34, chat_memory 21, chat_privacy 29 all OK; ruff check, ruff format --check, mypy src clean.
Divergence: MAX_SOURCES not raised (would exceed MAX_INPUT_CHARS); ordering fix suffices.
