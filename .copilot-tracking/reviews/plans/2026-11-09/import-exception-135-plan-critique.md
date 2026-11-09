---
title: Issue 135 plan critique
description: Single independent critique of the failed-import producer plan and its dispositions
ms.date: 2026-11-09
---

* Executed once, 2026-11-09T22:30Z, by the read-only `rubber-duck` agent against plan, details, research and the named source files. Verdict: revise. Not repeated for this task.

| Id | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Ledger key includes name and structure but the unchanged feed dedupes refusals by hash alone | Accepted. Ledger primary key becomes `ref = file:<sha256 or name>`, identical to the feed. One row per content hash; the first reason stays. Tests for same content under two names. |
| 2 | Blocking | Feed drops `structure` from the item, contradicting the planned item assertion | Accepted. Item assertions drop `structure`; structure stays in the ledger and `Routing` detail. Optional feed extension added to the contract. |
| 3 | Blocking | Reasons and notes can carry input-controlled text | Partly accepted. Refusal and conflict reasons become allowlisted fixed phrases with declared field names only; adversarial headers and part names tested. Rejected-batch notes stay as the human-entered original reason (issue requires originals kept); recorded as a limit: free text typed by a steward. |
| 4 | Blocking | CLI viewer is not authenticated | Accepted as a scope statement. `exceptions` is a local diagnostic tool, says so in output, and reads through `queue.queue(actor)`. Access control remains the served screen. Role scope tested on the queue. |
| 5 | Non-blocking | Select-then-insert race | Accepted. Integrity error is caught, rolled back and the existing row re-read; test with a forced race. |
| 6 | Non-blocking | Fallback hashing can mismatch or defeat the size guard | Accepted. Fallback hash only for files at or under the size limit with a stable stat; otherwise empty digest and a name ref. |
