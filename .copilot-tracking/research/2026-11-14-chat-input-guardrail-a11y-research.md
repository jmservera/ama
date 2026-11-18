---
title: Chat input label and PII notice research (Refs #215)
date: 2026-11-14
---

* Disposition: executed. Planning Readiness: Ready.
* Branch `test/demo-215-chat-input-guardrail-a11y-0441`, stacked on parent `test/demo-215-escape-disclosure-0436` (799909e72).
* `chat-widget.js`: textarea and skill select carry `aria-label` from caller, `autocomplete="off"`, `maxlength`; Enter sends unless Shift, composing or keyCode 229; error uses `role="alert"`.
* `chat.js` employee chat: `aria-describedby` includes `employee-chat-entry-warning` (exact PII/non-mutation notice) and `employee-chat-error`.
* Regulatory lookup: `<label for>`, `aria-describedby="regulatory-privacy"`, no Enter handler.
* Alert panel has no filter inputs; its controls are the plain-language checkbox (label for) and Refresh button.
* No defect found; `aria-invalid` count unchanged, baseline docs untouched.
* Tier: Focused (test-only).
