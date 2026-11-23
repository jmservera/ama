---
title: Issue 149 live r2 plan
ms.date: 2026-11-23
---

Goal: remove horizontal overflow of law viewer provision text at 320 CSS px.

1. Add `#law-out pre{white-space:pre-wrap;overflow-wrap:anywhere}` to `style.css` beside the `.case-tab-panel pre` rule.
2. Add `tests/test_law_viewer_reflow.py`: the rule exists, is scoped to `#law-out`, and every `pre` created in `law.js` sits under `#law-out`.
3. Re-run the Playwright probe (expect no horizontal overflow), then `test_accessibility_baseline`, `test_content_standard`, the new test and the landmarks test; ruff and mypy for the new test.
4. Record a research note under `docs/reference/research/`, an index row, a log entry and the changes record with the per-criterion table.
