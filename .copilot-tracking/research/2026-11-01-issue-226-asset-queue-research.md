# Research: issue 226 asset queue across homes (2026-11-01)

Disposition: executed (child of issue-226-asset-board-views, PR 639 merged).

## Prior delivery
* PR 639 merged the single-home `asset-board` screen with eligibility Unknown, missing inputs, portfolio count, AI cost panel. It named two unmet criteria: queue-level cross-home comparison and WCAG keyboard/browser proof. Closed PR 491 superseded.
* Open PRs 656 and 662 touch other role screens only; no overlap.

## Evidence
* `src/api/.../web/role-screens.js` registers `asset-board`; `load()` only reads the permitted case count.
* `core/stock.py` holds `query_status`, owned queries with `left/right.date`, `query_owner`. `Store.page_cases` is role-filtered; `MANAGER_ROLES` gate used by `/api/ai/report`.
* `projection.STAFF_GET` lists permitted GET kinds; a new route needs a kind.
* No existing endpoint aggregates stock conflicts across homes.

## Decision
Add a manager-only read-only `GET /api/asset/stock-queue` (core `stock.queue_rows` + `Store.stock_queue`), and a "Stock conflict queue across homes" panel in the asset-board screen: per home open conflicts, fields, oldest source age date, owners, missing inputs fixed at Unknown. Keyboard: table-scroll region has tabindex and caption; add a node test asserting focusable region and textual states. Browser/axe not available locally; CI is evidence.

Planning Readiness: Ready.
