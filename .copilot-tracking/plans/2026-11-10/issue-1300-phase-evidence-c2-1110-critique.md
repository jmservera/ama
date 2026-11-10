---
title: Issue 1300 C2 plan critique
description: One independent critique (rubber-duck) of the C2 plan, 2026-11-10; Revise, four findings dispositioned
ms.date: 2026-11-10
---

Executed once; verdict Revise. Not repeated.

1. Path substitution race (blocking). Applied in part: open log and lock with `O_NOFOLLOW` on the final component after the resolved-containment check; a full directory-descriptor design is not adopted. The residual check-to-open race by a local writer to the trusted evidence directory is recorded as a limit, not claimed closed.
2. Wrong-repository binding (blocking). Applied: in external mode `--repo` must resolve to Git's own worktree root, else refuse.
3. Inconsistent snapshot (blocking). Applied: binding check runs under the exclusive append lock and writes nothing on mismatch; verify hashes the same bytes it parses.
4. Step 5 hash handoff (non-blocking). Applied: verify uses `--json` and the SQL record takes `final.log_sha256`.
