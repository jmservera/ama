# Plan: employee chat (#617)

* Critique: executed once, inline; verdict: proceed. Compatible advice applied: no storage-gate bypass, no model call, no content in audit.
* Phase 1: core `ChatPanel.ask_unstored` (rules-only, refusal for decisions, case visibility check, outcome-only audit).
* Phase 2: API `GET /api/chat/status` adds `storage_approved`; `POST /api/chat/unstored-ask` (only when storage unapproved).
* Phase 3: `chat.js` uses `resizable: true` and the unstored route when storage is unapproved; widget stays open.
* Phase 4: tests (core, JS harness), ruff, mypy, node --check, live Playwright check on local synthetic data.
