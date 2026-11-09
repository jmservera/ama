<!-- markdownlint-disable-file -->
---
title: Issue 159 validation-refusal receipts initial implementation details
description: Phase details for the revised plan
ms.date: 2026-11-09
---

## Phase 1: core helper

* File: src/core/src/zava_forward/core/chat_panel.py, next to `record_rejected_unstored`.
* Signature `record_validation_refused(self, user: dict[str, Any], tid: str | None = None) -> None`.
* Behaviour: `try: user = self.iso.current_user(user) except (PermissionError, LookupError): return`. Build the actor with `user_key(user)`. Under `with self.iso.store.lock`, stored: `audit(actor, "chat.turn", "", json.dumps(receipt, sort_keys=True))` where `receipt = self._receipt(tid)`; unstored: `audit(actor, "chat.turn.unstored", "", json.dumps({"outcome": "rejected", "model_calls": 0}, sort_keys=True))`.
* No parameter carries request content; the helper cannot retain it.
* Success: one audit row. Stored receipt: `model_calls=0`, `tokens=None`, `provider_outcome="not-called"`, cost "Unknown". Unstored payload: exactly `{"model_calls": 0, "outcome": "rejected"}` (no token or cost field, as in the existing unstored refusal; critique PC-001).

## Phase 2: handler

* File: src/api/src/zava_forward/api/server.py, `_chat`.
* Unstored: before the `set(body) - {...}` raise call `app.panel.record_validation_refused(user)`.
* Stored ask: after `chat_resume` and the regulatory-thread handling, before each of the two raises call `app.panel.record_validation_refused(u, tid)`; the `ask` branch condition and message text are unchanged.
* Keep the helper call outside any lock the raise would roll back (the helper owns its `store.lock` block and returns first).
* Success: the three branches still return 400 with the same message; no new route or branch.

## Phase 3: tests

* API: a test helper reading the audit rows for `chat.turn` and `chat.turn.unstored` before and after, plus the existing prompt spy (`self.prompts`). Canary strings in question, extra field name and value, and skill. Assert status 400, exactly one new row, `model_calls` 0, no canary anywhere in the serialized audit rows or response, unstored target empty, stored thread id equals the owner thread. Controls: valid ask yields exactly one row and one model call; foreign and missing thread yield one `access-rejected` row; a user refused before the thread checks keeps 403 plus one `access-rejected` row (PC-002a).
* Core: stored and unstored helper exact shapes asserted on both JSON and SQL-backed stores via the existing fixture (PC-003); refused user at the helper writes nothing (PC-002b).
* Red evidence: run the new tests on the merged tree before the source change and record the failures.

## Phase 4: validation commands

* Resolve the repository CI invocations for pytest or unittest, Ruff 0.17.1 and mypy 2.4.0 from `.github/workflows` and component READMEs before running; run them in an owned venv under a session-qualified mktemp directory. Install only if a declared dependency is missing.
* Store raw commands, stdout, stderr, exit codes and hashes externally under the session files directory.

## Phase 5

* Changes, Review and state artifacts under .copilot-tracking dated 2026-11-09; commit with `git config --local user.email` as already set, Copilot trailer.
