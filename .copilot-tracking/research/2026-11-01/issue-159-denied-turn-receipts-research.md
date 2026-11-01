<!-- markdownlint-disable-file -->
---
title: Issue 159 conversational panel residual gap research
description: Evidence for the remaining engineering gap in the workbench conversation panel (C7 denied-turn receipts)
ms.date: 2026-11-01
---

## Task Metadata

* Task slug: issue-159-denied-turn-receipts. Research disposition: executed (reuse of issue closure audit plus source reading).
* Planning Readiness: Ready.

## Findings

* Criteria 1 to 5 are ticked from merged PRs #305 and #307; this slice does not change them.
* Criterion 6 (screen-reader tested, announcements) needs a named human AT run. Not satisfiable by code; stays unmet.
* Tokenomics criterion: closure audit (2026-10-31) says current-user denial occurs before receipt construction. Evidence:
  * `ChatPanel.ask` in `src/core/src/zava_forward/core/chat_panel.py` calls `self.iso.current_user(user)` before the receipt and the `finally` audit, so a removed or role-revoked user leaves no `chat.turn` receipt.
  * `src/api/src/zava_forward/api/server.py` `/chats/{tid}/messages` and `/ask` call `c.current_user` and `s.chat_resume` before `panel.ask`; a denial there also records no receipt.
* Existing receipt shape: thread_id, task, model_calls, tokens, provider_outcome, outcome, cost Unknown, bounds. Audit action `chat.turn`.

## Selected approach

Add `ChatPanel.record_rejected(user, tid)` writing a `chat.turn` receipt (outcome `access-rejected`, model_calls 0, tokens unknown) and call it from `ask` and from the server pre-check path. Failure to resolve an actor falls back to `unknown`. No model call, no stored message, no new fields.

## Out of scope

Human screen-reader test, prices, budgets, any controlled-record change.
