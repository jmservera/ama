---
title: Issue 145 live details (2026-11-24 10:26Z run)
ms.date: 2026-11-24
---

P1: `UPDATE assistant_allowance SET used_calls=calls, reserved_tokens=tokens WHERE used_calls<calls OR reserved_tokens<tokens`; return the row count. Call after `reapply_release_changes` in the post-restore sequence; no personal data involved.

P2: seed two pool rows (one with headroom, one already exhausted); assert count 1, both exhausted, second call returns 0, and a new authority id inherits via MAX (assert max used equals calls).

P3: runbook step 47 replaced "no reapply step yet" with the new function; README section near line 5008.
