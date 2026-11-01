# Changes: issue 226 asset queue across homes (2026-11-01)

* core `stock.queue_rows`, `Store.stock_queue` (manager only), `projection.STAFF_GET` gains `stock_queue`.
* api route `GET /api/asset/stock-queue` (403 non-manager; POST not routed).
* web `asset-board`: "Stock conflict queue across homes" panel (source-age order, not priority, owners, investment inputs Unknown, load failure shown as Unknown).
* Repair: `role-screens.js` on main had four unclosed `render(c) {` blocks (data-operator, contractor-job-pack, resident-choice, hazard registrations) causing a SyntaxError that disabled every role screen and failed existing screen tests. Closing braces added; no behaviour change otherwise.
* Tests: core stock queue test (json and SQL stores), API route test, node-vm queue, keyboard-region and failure tests.
* Validation: core stock tests, api test_ai_tasks, test_mvp, screen tests pass; ruff check/format clean in core and api; mypy: core clean, api 36 pre-existing errors unchanged (none in touched files). Browser/axe not run locally; CI is the evidence.
