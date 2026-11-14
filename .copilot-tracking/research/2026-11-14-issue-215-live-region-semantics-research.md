---
title: Issue 215 live-region semantics research
ms.date: 2026-11-14
---

* Research disposition: executed. Planning Readiness: Ready.
* Scope: `src/api/src/zava_forward/api/web/index.html`, `chat.js`, `chat-widget.js`. The task named a `static/` folder; the shipped assets are under `web/`.
* Alert banner (`regulatoryAlertsPanel`): labelled section, `role="status"` polite message, "Refresh alerts" button.
* Chat panel (`regulatoryChatPanel`): `details`/`summary`, `role="log"` with `aria-live="polite"`, polite usage region, labelled textarea, named submit button.
* `index.html`: one `role="alert"` (`#account-error`), polite `role="status"` elsewhere, no assertive live regions.
* No `tabindex` above 0 in any of the three files.
* Observation, not changed in scope: `chat-widget.js` sets `role="alert"` with `aria-live="polite"`, which downgrades urgency. Route to a follow-up.
* Not evidenced: assistive-technology and human usability testing. #215 stays open (`Refs #215`).
