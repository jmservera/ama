# Research: #215 doubt route and no-source held-state parity (2026-11-14)

Disposition: executed. Planning readiness: Ready.

* Siblings `test_alert_chat_role_wcag_plain_matrix.py` (static cues, one role-copy check) and `test_regulatory_chat_api.py` (one role, HTTP flow) exist. Neither runs the doubt and no-source states across every staff role with a zero-mutation check.
* UI contract in `chat.js`: no-source `li` (`state-no-source`, glyph and dotted border), doubt `button` (native `type=button`, `aria-disabled` keeps focus, sent state text plus `state-sent` glyph), `role=status` outcome line, plain-words copy, native plain-language checkbox.
* Runtime: `RegulatoryChat.ask` returns `refused` with empty citations for unsupported questions (the no-source state); `doubt` returns an idempotent receipt and writes only chat thread and audit records. Verified by prototype for every `STAFF_ROLES` role on the SQL-backed fixture.
* Not evidenced: browser, screen reader, staff comprehension. Refs #215 Criteria 3 and 4.
