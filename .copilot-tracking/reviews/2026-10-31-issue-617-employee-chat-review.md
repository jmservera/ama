# Review: employee chat (#617)

* Review executed once; outcome: conformant for code, with one open acceptance item.
* Storage gate preserved: no thread or message is stored when unapproved; no model call; audit holds skill and outcome only (tested with a canary).
* Web: native controls reused from the shared widget (dialog, log, status, reduced motion, Escape, focus return); no new visuals. Source guidelines were not re-fetched in this run (disclosed).
* Open: live check with the test user on the deployed site (routed to owner or a later task). Reply uses rules fallback; AI-backed replies still need approval references.
* Follow-ups: record CHAT_* approval references if stored chat is wanted.

## Correction cycle 1 (PR 620)

* Added HTTP regression tests in src/api/tests/test_chat_panel.py: storage_approved in both states, unstored-ask rules-only with no storage or model call, rejections (approved, 403, 401, invalid fields, unknown case).
* Widget test now asserts the chat-widget-resizable class and 35/70 default range controls; verified it fails without resizable: true.
* Focused tests, ruff and node --check pass; mypy reports only pre-existing import-not-found errors. Heavy gate not run.
