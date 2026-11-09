---
title: Issue 149 parent correction 3 phase details
ms.date: 2026-11-07
---

## Phase 1: checker source-cell contract

* `checks/data_operator_ai_state.py`: `SOURCE_COLUMN = 6`; `failed_ai_rows` requires a full row.
* `checks/data_operator_browser_check.py`: IDs come from `row[ai.SOURCE_COLUMN]` of the Kind-selected rows.
* `tests/test_data_operator_ai_state.py`: render helper returns cells; new test on the real render; stub rows follow the real layout.
