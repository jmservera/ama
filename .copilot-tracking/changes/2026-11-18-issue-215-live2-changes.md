# Changes: issue 215 live2 (2026-11-18)
Status: complete. Divergence: a CSS prototype was applied during Research to measure the fix, then reverted before the changes file; the first implementation (drop sticky tools) broke the #520 short-window Send guarantee, so the final design keeps the tools row always visible via a scrolling entry region.

## Files
* src/api/src/zava_forward/api/web/chat-widget.css: composer column, `.chat-widget-entry` scroll region, non-sticky tools row, log 40% reserve from 900px.
* src/api/src/zava_forward/api/web/chat-widget.js: wrap helper lines and text area in `.chat-widget-entry`.
* src/api/tests/test_chat_widget_helper_line_visible.py: new Playwright regression test.
* docs/reference/research/issue-215-live-helper-line-fix-2026-11-18.md, README index, log.

## Validation (focused tier)
* New test: fails on old code, passes on fix. 57 related tests pass. `--employee-layout` browser check passes. mypy, ruff check and format pass.
* Full chat_widget_browser_check fails in reply_scroll on baseline and on the change alike (pre-existing).
* No rpi-checks run; no Azure action; live app not re-probed.

## Per-criterion table
| Criterion | Status |
| --- | --- |
| Alert and chat patterns per role | Proven (ticked, earlier runs) |
| Alert content: what, source, status, action, owner, clock | Proven (ticked) |
| WCAG 2.2 AA (colour, keyboard, plain language) | Unproven overall; helper-line defect fixed locally; deployed re-check and AT testing outstanding/waived |
| Doubt route and no-source states | Proven (ticked) |
| Staff comprehension | Unproven; person-run, waived for demo |
