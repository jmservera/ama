---
title: Issue 891 chat demo phase details
description: Phase details
ms.date: 2026-11-07
---

* Phase 1: `test_demo_switch_keeps_suspension_privacy_refs_and_retention_gates` in `src/api/tests/test_chat_panel.py`.
* Phase 2: `chat.js` inserts the note with `ui.intro.before(...)`; `chat-widget.css` `.chat-widget-demo-note`; `checks/employee_chat_browser_check.py` demo scenario.
* Phase 3: README, demo activation record, `docs/reference/log.md`.
* Phase 5 blocker: sign-in to the Entra-protected demo app needs the owner-held test-user password. Exact blocker: unauthenticated GET /api/chat/status returns 401 (Easy Auth). After the owner supplies the credential interactively and deploys this branch via `src-deploy.yml`, run Playwright on the demo URL: warm `/healthz`, sign in, open the assistant, expect `#chat-demo-disclaimer` and a reply labelled "Model-generated, not approved. Demo only.", with 120 s timeouts and retries.
