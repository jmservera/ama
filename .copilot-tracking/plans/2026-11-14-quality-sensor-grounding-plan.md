# Plan: retained sensor values and Quality AI flag grounding (Refs #1288)

Date: 2026-11-14. Critique: executed once inline; no conflicting findings.

1. `sensor_view`: add `NOT_RETAINED`, `reading_text`, `grounding`; the employee view carries `grounding` (origin `decision_rule`).
2. `assistants.review_flag`: readings carry citation, values and text; add `origin: generative_model`, `origin_text`, `not_retained`.
3. Chat: `sensor` intent and `sensor_facts` in `chat_case_answers`; `ChatIsolation.sensors` injected by the server; denied or withheld views add no facts.
4. UI: `ops.js` grounding line; `assistants.js` flag readings and origin line.
5. Tests in `src/api/tests/test_quality_sensor_grounding.py`; run ruff, mypy and targeted unittest.
