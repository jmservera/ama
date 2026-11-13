# Plan: 233 queue row link + page context, 230 pager disabled ends

* [ ] P1 RED tests in src/api/tests/test_programme_screen.py: row link and page context (port from 837da4fde), pager disabled at ends.
* [ ] P2 Port role-screens.js changes (screenTable cell renderer, Connected view column, programmeCell, start offset, screenPageSize).
* [ ] P3 Add disabled on #programme-prev / #programme-next, refreshed after every go().
* [ ] P4 Port browser check steps, sync scenario-manifest recipe SHA, update atlas-screen-trace row. No log.md edit.
* [ ] P5 Validate: unittest (programme_screen, role_screens, conformance, content_standard), core manifest/needs tests, ruff check/format, mypy strict.

Amendments from critique: guard absent pager buttons; adjust browser check keyboard journey (not run, Chromium forbidden); narrow types in tests for strict mypy; verify manifest only hashes workbench_browser_check.py; keep limit=20 literal.
