<!-- markdownlint-disable-file -->
# Research: Escape and disclosure semantics for alert and chat controls (#215)

* Task: `215-escape-disclosure-0436`; branch `test/demo-215-escape-disclosure-0436`, stacked on `test/demo-215-plain-language-noncolour-0418` (#1632). Refs #215.
* Research disposition: executed (static inspection). Planning Readiness: Ready.

## Findings

* Chat widget (`src/api/src/zava_forward/api/web/chat-widget.js`): launcher carries `aria-controls`, `aria-haspopup="dialog"` and `aria-expanded`, kept in step by `open()` and `hide()`. A root `keydown` handler maps Escape to `hide()`, which unhides the launcher before `launcher.focus()`. The close button shares `hide()`. No focus trap, `showModal` or `stopPropagation`.
* "Open chat" button in `chat.js` calls the same `employeeChat.open()`, so Escape returns focus to the one persistent launcher, a predictable trigger.
* Regulatory lookup (`chat.js`) is a native `details`/`summary`; Escape closes it and focuses its summary only when open. Native semantics expose expanded state, so ARIA attributes are intentionally absent.
* Alert entries are static `article` elements and citations are an always-visible `ul`; neither is a disclosure, so no `aria-expanded`/`aria-controls` or Escape handling applies and nothing can trap focus.
* No discrepancy found, so no workbench static asset changes, no `scenario-manifest.json` recipe SHA update and no Core manifest/needs-inventory run.

## Gaps and limits

* Static source assertions only. No live browser run was performed; live keyboard coverage exists in `test_alert_chat_keyboard_live.py`.
* Not an accessibility conformance claim.
