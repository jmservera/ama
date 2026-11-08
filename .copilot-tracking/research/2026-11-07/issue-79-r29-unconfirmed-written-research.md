---
title: Issue 79 r29 research, written field of the unconfirmed runner outcome
ms.date: 2026-11-07
---

Research disposition: executed. Planning Readiness: Ready.

* Root `4a88793f0ea4c4c4ac1743f3256ef0f6c1c377a2`, tree `4afcca57`, ignored-clean; `origin/main` still `f0afa8d7`. Preserve ref `preserve/issue-79-pre-writtenfield`.
* Defect introduced by r28: `_confirmed` knows `outcome["written"]` (True after this call's first link) but `DurabilityUnconfirmedError` carries only path, published_on and cause, and the runner handler hardcodes `written=False`. The r28 runner test asserts False for a newly created record, which is wrong. Existing-record and race-loser outcomes are truthfully False.
* Callers: `Store.publish_ranking_snapshot` and the API use only the type, `.path` and `.published_on`; adding an optional `written` keyword (default None, meaning unknown) keeps them compatible. Unknown is never mapped to False.
* Child 61f3ebe1 `_confirmed` builds the same error, so child propagation must also carry `written` through its `_confirmed`; recorded as a requirement. The r28 runner JSON, earlier log entry and Review stay as history.
