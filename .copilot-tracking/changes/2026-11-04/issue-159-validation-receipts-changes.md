<!-- markdownlint-disable-file -->
---
title: Issue 159 validation-refused receipts changes
description: Changes and validation for the validation-refused receipt slice
ms.date: 2026-11-04
---

## Changes

* src/core/src/zava_forward/core/chat_panel.py: refused unstored asks (validation, missing case) now record one receipt.
* src/core/tests/test_chat_panel.py: new behavioural test; fails with the source change stashed (4 subtests fail), passes with it.
* docs/reference/log.md: entry appended.

## Validation (focused tier)

* Run: core `test_chat_panel.py` (43 OK); api `test_chat_panel.py` (52 OK, 1 skipped); ruff check and format clean on changed files; mypy `--cache-dir=/tmp/mypy-159` clean on chat_panel.py.
* Not run: complete gate, full suites, benchmarks, browser/axe/screen-reader checks, hosted CI, independent review. Audit-write only; no SQL schema, infrastructure or deployment change.
