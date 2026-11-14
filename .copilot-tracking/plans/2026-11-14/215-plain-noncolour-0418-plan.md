---
title: Plan - #215 non-colour, keyboard and plain-language matrix
description: Test-only plan with live-region decision
ms.date: 2026-11-14
ms.topic: reference
---

Details: [details](../../details/2026-11-14/215-plain-noncolour-0418-details.md). Research: [research](../../research/2026-11-14/215-plain-noncolour-0418-research.md).

## Phases

* [x] Phase 1: add `src/api/tests/test_alert_chat_role_wcag_plain_matrix.py`.
* [x] Phase 2: add thin `test_alert_chat_accessibility.py` and `test_alert_chat_keyboard_live.py` so the specified command runs.
* [x] Phase 3: decide the `chat-widget.js` live-region change (no change, see research), so no workbench script or manifest recipe SHA moves.
* [x] Phase 4: run targeted tests, ruff and mypy; commit with `Refs #215`; do not push.

## Critique

Executed once on the final candidate. Verdict: proceed. A source change to the widget error would alter existing assertions and is rejected; matrix tests avoid duplicating existing cases.
