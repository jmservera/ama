<!-- markdownlint-disable-file -->
---
title: Issue 159 route-level validation receipts plan critique
description: Single critique of the final prospective plan candidate
ms.date: 2026-11-09
---

## Execution

* Critique executed once on the final candidate, by the preparing agent. It is NOT independent; the independent exact-head review remains required later.
* Verdict: Approve for the plan, with the dispositions below. Not repeated for this task.

## Findings and dispositions

* C1 (applied): helper must run and return before the `ValueError` is raised, outside any lock that the raise would roll back. In `SqlStore`, `audit` is queued while `store.lock` is held and committed at lock exit, so the helper owns its own `with store.lock` block and returns before the raise. Recorded in details Phase 2.
* C2 (applied): double-receipt risk checked. Both stored raises precede `ChatPanel.ask`, whose `finally` is the only other `chat.turn` writer; the unstored raise precedes `ask_unstored`. Exactly-one is therefore structural and the negative control proves the delta.
* C3 (applied): `tid` is retained in the stored receipt only after `chat_resume` succeeded, so it is a resolved, owner-verified thread, not raw body content. The unstored target is empty (D2) so an unvalidated body `case_id` is never retained.
* C4 (disposition: decision D1, planned default): moving the unstored key check behind the user recheck changes 400 to 403 for a user removed between the role gate and the handler. This is consistent with "permission denials preserved", and is tested. Flag for reviewer, no human decision required.
* C5 (rejected as out of scope): extending coverage to the adjacent unreceipted 400s, anonymous 401, or the `messages` route. The approved comment bounds the slice to three branches.
* C6 (recorded, not resolved): the demo-targeted tier conflicts with the 7 Nov FULL wording and the repository security-sensitive full-tier rule. The owner replacement for this demo push is applied; the reviewer must confirm or require more.
* C7 (blocker, not a plan defect): gates G1 to G4 are unmet. The plan must not be implemented until they hold.
