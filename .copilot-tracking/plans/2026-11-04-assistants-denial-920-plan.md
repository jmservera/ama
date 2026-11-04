# Plan: assistants denial (Refs #920)

Details: [details](../details/2026-11-04-assistants-denial-920-details.md)

* [x] 1. Server: `/api/me` `services.assistants` is true only for staff roles.
* [x] 2. Client: `assistantCasePanel` and `assistantQueueView` skip the request when the flag is false and show plain words.
* [x] 3. Tests: unit test for the flag and the unchanged 403; Chromium check for an admin-only account.
* [x] 4. Focused validation (unittest, ruff, mypy, node --check, Chromium check).

Critique: executed once, inline. Verdict: proceed. No conflicts with confirmed decisions; server enforcement stays unchanged.
