# Plan: issue 226 asset queue across homes (2026-11-01)

1. core: `stock.queue_rows(cases)` returns, for cases with unresolved queries, id, address, town, open count, fields, owners, oldest source date; unresolved only; sorted oldest source first then id. Unit test in core tests.
2. core: `Store.stock_queue(user)` manager gate (PermissionError), lock, skips closed cases. Add `stock_queue` to `projection.STAFF_GET`.
3. api: route `/api/asset/stock-queue` in `get_kind` and GET handler (403 non-manager). API-level test.
4. web: `asset-board.load` fetches queue (catch to null -> Unknown state); render panel with caption table, textual status, "Portfolio scope, not this home" label, evidence boundary note; no controls. Node-vm test update.
5. Validate: unit tests, ruff check, ruff format --check, mypy on touched projects.

Critique (single, inline): keep read-only; no ranking of investment priority (sort is by source age only, labelled so); owner Unknown stays "Unassigned" never inferred; cap rows at 100 with visible truncation message. Accepted.
