# Research: chat origin badge accessibility (#215, #164)

Date: 2026-11-14. Branch: feat/demo-215-chat-origin-a11y-0959 (parent f907cd2c7, PR #1641).
Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue #215 (UX for regulatory alerts and the home chat), criterion 3: non-colour cues and plain language.
* `src/api/src/zava_forward/api/web/chat.js`: `attribution()` returns an origin label and detail for rules (`RULE_LABEL`), generative (`MODEL_LABEL`) and withheld (`WITHHELD_LABEL`, abstain); `sourceLine()` tags `[Workflow rule]`, `[Decision rule]`, `[Case record]`; `statusFor()` feeds `ui.setStatus`.
* `chat-widget.js`: log is `role=log` polite; status is `role=status` polite atomic; each assistant message shows `Outcome:` text, label, reply, detail, then `Sources (N)` with a no-source note.
* Existing tests (`test_regulatory_a11y_cues`, `test_alert_chat_accessibility`) do not cover origin labels, live status text or source counts.

## Findings

* aria-live detail is already present; no source edit needed.
* Gap: no regression test pins origin wording, announcement text or source-count disclosure.
* Observation, not changed: detail text says "grounded on case rules" for generative replies, mildly technical. Route to a later copy review.
* Limits: static source checks only, not screen reader or comprehension evidence.
