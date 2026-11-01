---
title: Issue 153 core-flow copy changes
date: 2026-11-01
---

* `web/role-screens.js`: gate wording replaced by phase check.
* `web/app.js`, `web/ops.js`: generic error states reason, owner and next action; `generic` flag replaces literal comparison.
* `web/law.js`, `checks/loading_briefing_browser_check.py`: failure status names owner and next action; browser check string updated (not run, no Playwright).
* `core/store.py`: plain ranking permission error.
* `tests/test_content_standard.py`: guard extended to three files; two new tests.
* Docs: `content-standard.md`, `log.md`.

Validation: content-standard tests 13/13 pass; api ruff check, format, mypy clean. Full api suite and core ruff/mypy are blocked by a pre-existing IndentationError in `core/assistant_release.py` line 184 on main (from #658), not touched here. Playwright checks not run.
