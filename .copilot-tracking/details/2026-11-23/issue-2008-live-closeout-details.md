---
title: Issue 2008 close-out details, 2026-11-23
ms.date: 2026-11-23
---

Phase 1: copy `evidence-2026-11-22-live-xlsx/live_xlsx_import_check.py`, change `W` and `OUT` to this worktree and the 2026-11-23 folder, run with `python3`. Success: `import_check_responses` is `[200]`, `source_unchanged` is true, screen text shows mapping, a duplicate-reference conflict and ten row verdicts.
Phase 2: note `docs/reference/research/issue-2008-closeout-live-2026-11-23.md`.
Phase 3: `git diff --stat`, relative link check, sloptrim detector on the note.
