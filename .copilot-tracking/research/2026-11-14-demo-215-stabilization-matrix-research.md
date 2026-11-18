# Research: #215 end-to-end alert-to-chat stabilization matrix (2026-11-14)

Disposition: executed. Planning readiness: Ready.

* Sibling #215 tests cover pieces: unblock/visit grounding (`test_alert_chat_unblock_visit_grounding_215.py`), citation attribution, plain language and non-colour, contrast, escape disclosure, keyboard.
* Gap: no single suite ties case/alert context injection (`chat.js` `/api/chat/threads` with `case_id`, prompt context), provenance badge, citations, AI-unavailable fallback, non-mutation and manual escape paths together, nor states the evidence boundary.
* Backend: `ai.evidence` envelopes with outcome `disabled`/`timeout` already route to rules-only answers; synthetic stub, no network.
* Finding: no product gap; test-only change.
* Not evidenced: live Azure OpenAI, browser render, screen reader, manual WCAG sign-off. Refs #215 only.
