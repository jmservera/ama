# Plan: issue 616 paging

1. [x] Core: `list_work_orders` and `list_packages` accept `limit`/`offset`, filter then slice.
2. [x] API: validate `limit` 1-100 and `offset` >= 0 (400 otherwise); unpaged callers unchanged.
3. [x] Client: bounded initial load (5 packages, 20 orders), native Previous/Next buttons, polite status text with counts and page number (non-colour), focus moves to the status after paging, out-of-range offset self-corrects.
4. [x] Tests: new `test_workspace_paging.py`; Node mock updated to the envelope.
5. [x] Focused validation, then PR.

Critique: executed once; compatible findings (filter before slice, contractor totals exclude hidden orders) applied directly.
