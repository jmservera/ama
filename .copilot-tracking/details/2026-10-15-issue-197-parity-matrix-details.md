---
title: Issue 197 parity matrix details
ms.date: 2026-10-15
---

* Phase 1 success: every tracked path listed once; modules grouped by import level.
* Phase 2 success: each PR has a move-or-rebuild decision; reopen only where an acceptance criterion is unmet and evidenced.
* Phase 3 success: outcomes limited to migrate, rebuild, archive, retire; targets use the owner layout; groups ordered dependency-first.
* Phase 4 success: `git ls-files mvp prototype` paths all present in the matrix; relative links resolve; index and log updated, earlier log entries untouched.
* Constraints: no Azure resource used; no `.env`, `.vscode` or `.copilot-tracking/github-issues` change; no commit to main.
* Phase 5 success: merge conflict in `docs/reference/log.md` resolved keeping both entries.
* Phase 6 success: no statement that PR 287 is open or must not merge; three new rows present; counts equal `git ls-files`; 450 sandbox files mapped as retire.
* Phase 7 success: every target equals the ADR 0006 mapping or is listed as an amendment; no `devtools` target; no draft wording.
* Phase 8 success: coverage script reports no missing tracked path outside the sandbox pattern; README row and log entry updated; earlier log entries untouched.
