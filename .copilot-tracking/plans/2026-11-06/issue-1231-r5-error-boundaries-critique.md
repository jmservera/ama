---
title: Issue 1231 plan critique r5 (single independent pass)
ms.date: 2026-11-06
---

## Execution

One independent critique by a rubber-duck agent at about 14:01Z on the r5 research, plan and details, before any rebase, test or source edit. It will not be repeated for this task. Verdict: changes needed (one blocking, two non-blocking). All three are compatible with confirmed owner direction and were applied directly to the details file.

## Findings and dispositions

* Blocking: the planned `finally` would re-raise a cleanup error for the concurrent loser after the winner's record was read, losing a valid already-published outcome. Applied: the loser returns the winner's metadata with `written` False and `stage_retained`; test added.
* Non-blocking: a cleanup error could mask the primary link or `_existing` read error. Applied: primary exception propagates and the cleanup failure is attached with `add_note`; test with simultaneous link and unlink failure added.
* Non-blocking: `stage_retained` was not always true (for example `ENOENT`). Applied: `FileNotFoundError` reports nothing retained; other `OSError` reports the retained stage; the warning says it is a hard-link alias of the committed record and must not be modified; test added.
