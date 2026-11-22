---
title: Issue 2201 live plan (second pass)
ms.date: 2026-11-21
---

## Critique (executed once, final candidate)

* Risk: declaring root cause from the old source reading alone. Disposition: accepted; the note states what is proven (fix on main, one post-fix success with a captured stdout line) and what is not (cause of the 22:00 and earlier failures; exit code).
* Risk: changing src without a log-backed defect. Disposition: no src change; a blind memory or timeout tweak would be speculation. If a watcher captures a new stderr code, reopen.
* Risk: altering the Log Analytics network rule to read logs. Disposition: rejected; production-adjacent Azure write beyond the owner's scope.
* Tier: documentation and evidence only, focused tier. Full tier only if src changes.

## Plan

1. Persist evidence (executions, probe JSON, map screenshot, log capture) and a watcher that records executions to 00:30 UTC.
2. Write research note `docs/reference/research/issue-2201-live-receiver-proof-2026-11-21.md` with a per-criterion table; update the index and log.
3. Re-read executions at the end; score "three consecutive Succeeded" only on scheduled runs after the 21:33 modification.
4. Single Review, then one local commit.
