<!-- markdownlint-disable-file -->
---
title: Issue 159 denied-turn receipts changes
description: Implementation record for per-turn receipts on permission-denied conversation turns
ms.date: 2026-11-01
---

## Changes

* `src/core/src/zava_forward/core/chat_panel.py`: extracted `_receipt`, added `record_rejected`; `ask` records a receipt when the per-turn current-user check fails.
* `src/api/src/zava_forward/api/server.py`: `/threads/{tid}/messages|ask` pre-check denial records a receipt before the 403/404.
* Tests: `src/core/tests/test_chat_panel.py` (every revoked-roster case asserts one receipt), `src/api/tests/test_chat_panel.py` (HTTP disabled-user turn).

## Validation

* Core `test_chat*.py` 99 tests OK; API `tests.test_chat_panel` 42 OK (1 skipped, pre-existing).
* ruff check and format check clean for core and api; `mypy src` strict clean for both.
* Not run: heavy local gate (CI is the evidence), browser checks.

## Divergences

* None from plan. Phases 1 to 3 complete; phase 4 is publication.
