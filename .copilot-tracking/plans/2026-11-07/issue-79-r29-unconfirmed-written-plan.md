---
title: Issue 79 r29 plan
ms.date: 2026-11-07
---

* RED first: strengthen the runner regression so a first-created record asserts `written` True with `committed_unconfirmed`, exit 2, uncertainty, path, date and no `publish_failed`; add core assertions that the typed error carries `written` True (first link), False (existing record, race loser) and None when constructed without it.
* Helper: `DurabilityUnconfirmedError(path, published_on, cause, written=None)` stores `written`; `_confirmed` passes `outcome["written"]`.
* Runner: output `written` from the error as is (True, False or null for unknown); never defaults unknown to False. Stage_retained unchanged. Fix the earlier wrong assertion.
* Docs: one README clause; new log entry; changes, author Review, state. Light core, runner, API, ruff, mypy only.

## Critique (author, one pass, not independent)

* A null `written` is a third value for consumers; accepted because genuine unknown must not be false, and in-repo `_confirmed` always supplies it.
* Disposition: proceed; no other behaviour changes.
