---
title: Issue 153 C2 changes
ms.date: 2026-11-13
---

## Changes

* role-screens.js: Owner and Next action added to Screen unavailable, paging failure, stage-list not-installed line, finance queue unknown, Invalid file status. Existing substrings and "Try again" kept.
* law.js: missing-file notice gains Owner and Next action; fail() no longer duplicates them when the server message has them.
* server.py: 500 body gains Owner and Next action.
* test_content_standard.py: one new test for all seven notices plus the law.js dedupe guard.

## Validation (venv /tmp/venv-153c2-1800, removed before commit)

* unittest: test_content_standard, test_programme_screen, test_regulatory_ux_check, test_lawstore, test_workspace_scripts, test_error_logging, test_exception_register_screen, test_handoff_read_guidance, test_finance_grants_screens: 159 tests, OK after playwright install (21 skipped).
* ruff check on changed source and test: pass. mypy (src/api): pass. node --check on both scripts: pass.
* Not run: browser checks (programme_paging, loading_briefing) because Playwright browsers were not exercised; the preserved substrings were verified by grep. ruff format flags pre-existing server.py formatting, not changed.
* app.js untouched.
