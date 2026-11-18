# Research: workbench chat keyboard and live announcement (Refs #159)

Date: 2026-11-14. Disposition: executed. Planning Readiness: Ready.

Criterion: "Panel is keyboard operable, screen-reader tested, and announces new messages".

## Findings

* The employee chat is `chat-widget.js` (shared) driven by `chat.js`. It already has a native button launcher with `aria-expanded`/`aria-controls`, Escape close returning focus to the launcher, Enter submit and Shift+Enter newline in a textarea, a keyboard-scrollable log (`tabindex=0`), native `details` for sources, and a single `role="status"` (`.chat-widget-status`) updated with `statusFor(kind)` after each reply (answer, withheld, refused, fallback).
* Gap: the transcript `role="log"` declared `aria-relevant="additions"` only, so text changes inside an existing entry were not announced. Required value: `additions text`.
* Sources render as plain text, so there are no citation links; no clear/reset control exists, so none needs keyboard work.
* Invariants: `#regulatory-alerts` keeps exactly one `[role="status"]` (`chat.js`); no `aria-invalid` is added; the widget adds no second status.
* Screen reader testing with real assistive technology is not performed here; static and Node harness checks only.

## Evidence

* `src/api/src/zava_forward/api/web/chat-widget.js`, `chat.js`, `index.html`; existing tests `test_chat_origin_badge_a11y.py`, `test_chat_widget_focus.py`.
