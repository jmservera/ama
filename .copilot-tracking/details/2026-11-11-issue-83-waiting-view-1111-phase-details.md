---
title: Issue 83 waiting-time screen phase details
ms.date: 2026-11-11
task_id: issue-83-waiting-view-1111
---

## Test ownership (locked before critique)

* Owner: new `src/api/tests/test_handoff_waiting_view.py` (Node source-slice cases and opt-in Chromium cases, reusing `Served`, `START/END` style helpers from existing tests).
* Removals: none. Existing tests unchanged unless a header-link count breaks them (none found in grep of `See all cases`/`Check a spreadsheet` beyond a link-by-name lookup).
* Maximum additions (revised after PC-002): about 12 Node scenarios in one Node run and 6 Chromium methods. Node slice markers: `const WAITING_READ_ERROR` through the end of `handoffWaitingView`.
* Required cases: queue present with empty personal list (constructed response, labelled, PC-001); empty; due-time reason; merely old with no reason and no limit (server-derived only); already escalated; 403 distinct from 500; malformed including 200 non-JSON; non-null limit; abort; keyboard on entry link, case link and re-check button; no non-login POST and unchanged store.
* Semantic coverage: rendering, scope text, failure honesty, no mutation. Regression coverage: existing guidance, download, API and inventory suites rerun, not copied.
* Generated targets: none.

## P01 View, route and entry link

Evidence: research C1, C2, C6, C7, C8.

* P01-T01 Add `const WAITING_READ_ERROR`, a `waitingRows(data)` validator and `async function handoffWaitingView()` after `workSteps`-area code and before `listView` (outside the `pendingHandoffs` to `let briefingBox` slice). Uses `h`, `api`, `show`; one `api("/api/handoffs/unaccepted")` call; abort returns silently; failures use the fixed message; validator returns null on malformed.
* P01-T02 In `route()` add `if (hash === "#/handoff-waiting") return await handoffWaitingView();` before the list fallback, and route status label for that hash.
* P01-T03 In `listView` header row add `h("a", { class: "btn alt", href: "#/handoff-waiting" }, "Handoff waiting times")`.
* Done when `node --check` passes and the view renders in Chromium.

## P02 Focused tests

* P02-T01 Node cases by evaluating the real `WAITING_READ_ERROR` through `handoffWaitingView` source slice with stubbed `h`, `api`, `show`.
* P02-T02 Chromium cases: entry by keyboard, table content for merely-old vs due vs escalated, card-failure independence, failure and malformed (page fetch wrapper constructs responses explicitly, labelled as constructed), no non-login POST, store unchanged.
* Done when new tests pass, or skip reasons are recorded.

## P03 README note and focused validation

* P03-T01 Short section in `src/api/README.md` stating the screen, scope and limits.
* P03-T02 Run: new tests (Node and `ZF_BROWSER_TESTS=1`), `test_unaccepted_handoff_download_ui`, `test_handoff_read_guidance`, `test_handoff_api`, `test_role_endpoint_inventory`, `node --check`, Ruff and mypy on new test file. Record commands, head, exits and skips.

## P04 Original Review

* One `rpi-review` execution on the frozen candidate; web rules refetched and applied to changed web files with `file:line`.
