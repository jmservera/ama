---
title: Issue 157 per-role chat limits details
ms.date: 2026-11-13
---

* Role limits keyed by role name; unknown roles resolve to the zero bound (default deny).
* Thread bound counts prior user messages from `thread["messages"]` before the new question; reaching the cap yields kind `fallback`, model `workflow-only`, zero calls.
* `context_chars` in the receipt is the assembled system plus prompt length (0 when no model prompt was built); `history_chars` is the length of the history block sent.
* No user-visible text may contain: gate, hold, provenance, trace, snapshot, envelope.
* No change to retries, output tokens or admission logic.

## Critique dispositions (rubber-duck, verdict Revise, applied directly)

* PC-001: count prior user turns inside the same `store.lock` block that persists the question, so concurrent turns serialise.
* PC-002: `thread_turns_used` includes the current question (first turn reports 1); a turn over the cap reports the cap.
* PC-003: `chat.js` usage note shows turns used of the cap.
