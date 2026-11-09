---
title: "#184 C5 details"
ms.date: 2026-11-08
---

## Tests (synthetic controls only, no network or persistence)

* decide: 365 days and 14 days plus 1 second give INVALID; exactly 14 days gives SEND; a 1-day window gives SEND; expired stays EXPIRED even when also far in the past; a disabled over-window control gives INVALID, and a disabled in-window control gives STOPPED.
* Receiver: `window_seconds` refuses an over-window control; run_window with a far-future file never constructs the receiver type; a file rewritten to over-window during the window sets the stop event (via `_watch`).
* Simulator: `main` with a 365-day control file and the in-memory sink sends nothing and returns 0 (extend the existing stopped-control test pattern).
* Later file change: valid file rewritten to expiry beyond 14 days stops the watcher.

## Commands

Environment: retained /tmp/v184-c4-1794169588 is a non-editable copy built from the pre-edit tree and would test stale code. Use PYTHONPATH pointing at the worktree src dirs ahead of it, and print module `__file__` to prove the checkout is imported. Unit: `python -m unittest test_live_control test_live_receiver_sql test_sensor_ingestion`. Static: ruff check, ruff format --check, mypy per package. Exit codes come from the process, not a pipe.

## Stop conditions

A change needed outside live_control.py, tests or the one README sentence; unexpected failures in unrelated tests.
