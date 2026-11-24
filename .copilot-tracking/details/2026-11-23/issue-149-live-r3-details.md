---
title: Details, issue 149 live r3
ms.date: 2026-11-23
---

## Phase 1

`tile_notice` returns `page.locator(MAP_STATUSES).filter(has_not_text=COUNT_NOTICE)`. The unit test extends `FakeLocator.filter` to accept `has_not_text` and asserts the tile locator uses it and no sibling combinator.

## Phase 2

Run `python3 -m checks.map_tile_status_browser_check`, `python3 -m unittest tests.test_map_status_locators`, ruff check and format, mypy. Live: Playwright desktop load of `ca-resident-demo` and the API app, no credentials printed.

## Phase 3

Note `docs/reference/research/issue-149-map-check-locator-2026-11-23.md`, index and log.
