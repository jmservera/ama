---
title: Changes for the handoff waiting integrated-main checkpoint
ms.date: 2026-11-11
---

## Changes

* Committed Root's admission amendment, then merged pinned main `ef3e00ad05a78c3a0fd3b342b860fb3d43796223` with an ordinary merge. `src` at HEAD equals the pin's `src` tree `f82975df`; only `.copilot-tracking/` files differ from the pin.
* Appended one dated section to `docs/architecture/cutover-evidence-pack.md` and one entry to `docs/reference/log.md`. No index row was needed. No source, test, configuration, workflow, requirement or ADR change.

## Observations (local, constructed synthetic fixtures)

| Id | Selector | Exit | Ran | Skips |
| --- | --- | --- | --- | --- |
| W4 | `tests.test_unaccepted_handoff_csv_api` | 0 | 13 | 0 |
| W5 | `tests.test_handoff_api` | 0 | 7 | 0 |
| W6 | `tests.test_role_endpoint_inventory.RoleEndpointInventory` | 0 | 24 | 0 |
| W7 | `tests.test_accessibility_baseline` | 0 | 12 | 0 |
| W8 | `tests.test_workbench.WorkbenchNavigation` | 0 | 5 | 0 |
| W2 | `tests.test_handoff_read_guidance`, shared lock held around it only | 0 | 9 | 0 |
| W3 | `tests.test_unaccepted_handoff_download_ui` | 0 | 6 | 0 |
| W1 | `tests.test_handoff_waiting_view` | 0 | 10 | 0 |
| S1 | `node --check`, Ruff check and format check of the new test | 0 | n/a | n/a |

Total 86 tests, no skips, no failures. Counts differ from Root's 81-test combined command and are not reconciled. W9 was not run.

## Divergences and amendments

* First attempt of W2, W3 and W1 used an isolated HOME that hid the user-site Playwright: `ModuleNotFoundError` in `setUpClass`, zero product assertions. Preserved raw outside the repository; repeated once with the existing user-site directory restored, no install.
* W2 ran under a held non-queued lock per Root's amendment; W1 and W3 were not wrapped.
* Main scorer run `42991793134` was in progress and no Source CI on the pin was observed; not called passing.

## Not done

No push, PR, board write, tick, mypy, full gate, W9, SQL, Docker or cloud.
