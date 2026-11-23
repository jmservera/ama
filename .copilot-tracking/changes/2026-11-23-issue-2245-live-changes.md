---
title: Changes for issue 2245 (employee chat thread creation)
ms.date: 2026-11-23
---

## Changes

* `src/api/src/zava_forward/api/server.py` `_unhandled`: a busy SQL write lock on `POST /api/chat/threads` answers 503 with `Retry-After: 5` and logs `cause=sql-write-lock-busy`; other POSTs keep 500.
* `src/api/tests/test_error_logging.py`: two tests added; the 503 test failed with 500 before the fix.
* Research note [issue-2245-live-2026-11-23.md](../../docs/reference/research/issue-2245-live-2026-11-23.md), probes and screenshots, index and log entries.

## Validation

* `tests.test_error_logging` and `tests.test_chat_panel`: 90 tests OK (1 skipped). `python3 -m mypy` in `src/api`: no issues. `ruff check` and `ruff format --check`: clean.
* Tier FULL (src change). The full gate is owned by the coordinator; `rpi-checks.py --all` was not run. Hosted CI not observed (nothing pushed).

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Thread creation answers 503 not 500 on a busy SQL write lock | Proven locally (failing-first test) |
| Cause of the 2026-11-22 500 | Unproven (logs denied; not reproduced live, 13 creates all 200) |
| Model-answerable question shows "Model calls: 1" live | Unproven (open AI suspension from 2026-11-18 blocks it; restart is a human action) |
| Banner states plainly when answers are rule-based | Proven live (banner and screenshot) |
| Which skills and routes call the model and why none did | Proven (code reading and live replies) |
