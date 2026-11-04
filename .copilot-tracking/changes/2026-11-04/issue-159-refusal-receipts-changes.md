<!-- markdownlint-disable-file -->
---
title: Issue 159 refusal receipts changes
description: Changes and validation for the unstored and regulatory refusal receipt slice
ms.date: 2026-11-04
---

## Changes

* `src/core/src/zava_forward/core/chat_panel.py`: `record_rejected_unstored`; `ask_unstored` records a rejected receipt on current-user refusal.
* `src/api/src/zava_forward/api/server.py`: role gate records it for unstored asks; regulatory capability refusal records a `chat.turn` receipt for `messages` and `ask`.
* Tests: one core test, two API tests.
* `docs/reference/log.md`: one entry. No change to permissions, responses or private data.

## Validation (focused tier; PYTHONPATH to src projects, no installs, no ignored files)

| Command | Result |
| --- | --- |
| `src/core`: unittest discover `test_chat_panel.py` | Ran 42, OK |
| `src/api`: unittest discover `test_chat_panel.py` | Ran 52, OK (1 skipped) |
| `src/api`: unittest discover `test_chat_widget_focus.py` | Ran 10, OK |
| New tests with source changes stashed | fail (as expected) |
| `ruff check` on the four changed files | clean |
| `mypy --cache-dir=/tmp/mypy-530` on `chat_panel.py` | clean; project-wide run from `src/api` shows 9 errors in 2 files that I did not touch or compare |

## Not run

* Complete local RPI gate, full suites, benchmarks, browser checks, screen-reader or any assistive-technology run, hosted CI, independent review.
* Tier: focused. Audit-write only; coordinator decides whether a gate is needed.
