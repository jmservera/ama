<!-- markdownlint-disable-file -->
---
title: Issue 159 route-level validation receipts phase details (prospective)
description: Phase details for the bounded receipt slice; not executed
ms.date: 2026-11-09
---

## Phase 1: core helper

* File: src/core/src/zava_forward/core/chat_panel.py, next to `record_rejected` and `_record_unstored_refusal`.
* Signature: `record_validation_refused(self, user: dict[str, Any], tid: str | None = None) -> None`.
* Behaviour: `self.iso.current_user(user)`; on `(PermissionError, LookupError)` call `record_rejected(user, tid)` when `tid` else `record_rejected_unstored(user)`, then re-raise. Success path writes one audit row under `self.iso.store.lock`, actor `user_key(user)` (fallback `unknown` as the existing helpers do).
* Stored detail: `json.dumps(self._receipt(tid), sort_keys=True)` (outcome `rejected`, model_calls 0, tokens None). Unstored detail: `{"model_calls":0,"outcome":"rejected"}` with target `""`.
* No parameter carries the body, keys or skill, so nothing sensitive can be retained.

## Phase 2: handlers

* Unstored: `if set(body) - {...}: app.panel.record_validation_refused(user); raise ValueError(...)`, before `c.current_user(user)`.
* Stored: inside `parts[2] == "ask"`, call `app.panel.record_validation_refused(u, tid)` before each existing `ValueError`. The `messages` route and regulatory-thread paths are untouched.
* The helper commits its own audit row (`with store.lock`) and returns before the raise, so the SQL queued-audit flush is not rolled back by the exception.
* Exactly-one guarantee: both raises happen before `ChatPanel.ask`, whose `finally` is the only other writer, so no path writes two receipts.

## Phase 3: tests (existing files only)

* HTTP (src/api/tests/test_chat_panel.py, patterns from `test_foreign_and_missing_thread_turns_record_one_receipt_per_route`): for each of the three branches assert status 400, exactly one new audit row of the expected action, outcome `rejected`, model_calls 0, tokens None (stored), canary question, unknown key name and value absent from the new row `detail`, no stored messages, `self.prompts == []`.
* Controls: valid stored ask +1 `chat.turn` with model call counted; role-gate, foreign thread and workflow-fallback tests re-run unchanged; removed user with extra keys on unstored gets 403 and one `access-rejected` row.
* Core (src/core/tests/test_chat_panel.py): helper writes one row per mode and none of its inputs reach `detail`.
* Negative control: with the handler edit reverted the new HTTP tests must fail on the receipt delta.

## Phase 4: commands (to be recorded exactly when run)

* From `src/api`: `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests.test_chat_panel -q`; from `src/core` the matching `tests.test_chat_panel`; ruff and mypy per the component READMEs and CI definitions at the integrated base. Not run in this preparation.

## Out of scope observations for follow-up only

* Adjacent unreceipted 400s and anonymous 401 (research).
