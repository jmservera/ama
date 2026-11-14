# Research: recommendation origin provenance (Refs #104, #164)

Date: 2026-11-14. Disposition: executed. Planning Readiness: Ready.

* Issue #104 criterion: AI never approves, executes, ranks or mutates controlled records; recommendations are advice beside the deterministic order.
* `Store.ai_priority` builds the card; `_rec_view` in `src/core/src/zava_forward/core/store.py` is the single serialiser. The card had only `source` (`ai` or `template`) and the label, with no explicit origin field. `chat_panel.ANSWER_ORIGINS` already uses `decision_rule` and `generative_model` for chat, which is out of scope (sibling chat work).
* Gap: no machine-readable statement that the order is rule-based and only reason wording can be generative.
* Decision: derive origin from `source` so fallback, workflow-only and financial-hold mutations stay consistent.

Cycle 1 correction research: review findings were validation evidence, a formatting/typing defect in `origin_of`, and the PYTHONPATH workaround. Editable install pointed at the main checkout, so an isolated venv was used.
