---
title: Issue 232 resident engagement screens accessibility phase details
ms.date: 2026-11-13
---

## Phase 1

`screenTable(label, headings, rows, limit, cell, rowHeader = false)`: when `rowHeader` is true the first cell of each body row is `th scope="row"`. `screenRecordTable` passes it. Resident tables: Choice and update commitments by home, Measure choices by version, Measures paused or withdrawn, Service requests and contact needs, Open service issues by home, Service issues and contact needs, Recorded response steps. Default behaviour of the other 41 callers is unchanged.

## Phase 2

Table "Service requests and contact needs" columns become Request, Route, State and meaning, Contact needs, Next update using `serviceStatus(r)` and `serviceNeeds(r)`.

## Phase 3

* `tests/test_resident_choice_screen.py`, `tests/test_resident_service_screen.py`: caption, `th scope="col"`, `th scope="row"` first cell; state meaning text.
* `checks/role_screens_browser_check.py`: `check_table_headers`, `run_axe` (extracted), queue-state axe and header check for resident stories, `reach_table_regions` at 320 px for resident stories.
* Negative proof: with the JS change stashed, the 232 browser check fails on "no row header".

## Phase 4 and 5

Commands and results are in the [changes record](../../changes/2026-11-13/232-resident-a11y-2220-changes.md).
