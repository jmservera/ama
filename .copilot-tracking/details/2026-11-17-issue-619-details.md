---
title: Issue 619 details
ms.date: 2026-11-17
---

## Phase 1

New viewport step after `chat_widget`: set viewport 320x256, reload case view, assert
`scrollWidth <= innerWidth` (no two-direction scrolling), tab panel visible; open chat and assert
the textarea and Send button are inside the viewport horizontally. Emulate `prefers-reduced-motion: reduce`
and assert no running CSS animation with duration over 0.01 s on the chat panel. Helper
`horizontal_overflow(metrics)` is pure for the unit test.

## Phase 2

Protocol: add "Zoom and reflow equivalent (2026-11-17)" subsection; limits unchanged. README one sentence.
log.md append entry.

## Phase 3

Run `tests.test_production_config_a11y_check`, ruff, mypy src/api, and the browser check.

## Critique (single pass, recorded)

Risk: overflow assertion could fail on existing UI; if so, record as finding and fix only if tiny, else
record as follow-up. Chat reduced-motion check must not assume animation exists (pass when none).
