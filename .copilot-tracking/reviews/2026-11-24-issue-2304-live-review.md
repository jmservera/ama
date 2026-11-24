---
title: Issue 2304 live review (2026-11-24)
ms.date: 2026-11-24
---

# Review (executed once)

Outcome: conformant for the changed scope, with routed items.

* Fresh answers are never delayed or replaced by the cache, so state-change tests pass (605 OK).
* Concurrency: one job per key under a lock; daemon threads; the job holds its own connection; waiters share a read-only result copied with `deepcopy`.
* Security: role is checked before any job; the stale answer is counts only and keyed by identity; revocation can lag up to 900 s only when a fresh answer is late. Routed: tighten by re-checking the staff row cheaply if the owner wants it.
* Routed: the job cap 120 s can still leave the first cold request on 503; live proof needs deployment (owner).
* Routed: `ruff format` of `assistants.py` was pre-existing unformatted and left alone.
