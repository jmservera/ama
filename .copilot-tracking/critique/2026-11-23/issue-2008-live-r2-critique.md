---
title: Issue 2008 live re-proof critique (r2)
ms.date: 2026-11-23
---

Executed once on the final-candidate plan. Verdict: proceed.

* Risk: re-running duplicates evidence. Accepted; the owner wants fresh proof per run and the new directory is separate.
* Risk: the script embeds a worktree path. Handled by a path substitution at run time; credentials are only read at runtime and the output was grepped for `@` (0 matches).
* No conflict with owner decisions; no Azure resource created or changed.
