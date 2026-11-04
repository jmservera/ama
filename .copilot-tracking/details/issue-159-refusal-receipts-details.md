<!-- markdownlint-disable-file -->
---
title: Issue 159 refusal receipts phase details
description: Step-level details for the unstored and regulatory refusal receipt slice
ms.date: 2026-11-04
---

## Phase 1

* `src/core/src/zava_forward/core/chat_panel.py`: add `record_rejected_unstored(user)` writing `chat.turn.unstored` with `{outcome: access-rejected, model_calls: 0}`; wrap `current_user` in `ask_unstored`.
* `src/api/src/zava_forward/api/server.py`: the role gate calls it for `/api/chat/unstored-ask`.

## Phase 2

* `server.py` thread POST: wrap `_regulatory_access(user)` and record `app.panel.record_rejected(user, tid)` for `messages` and `ask` before re-raising `ChatForbidden`.

## Phase 3

* Core: `test_sql_revocation_before_unstored_ask_records_a_rejected_receipt`. API: `test_unstored_ask_role_gate_refusal_records_one_receipt_without_the_question`, `test_regulatory_capability_refusal_records_one_receipt_per_turn_route` (provider name patched to trusted-proxy with the CSRF header).
* Verified the new tests fail with the source changes stashed.
