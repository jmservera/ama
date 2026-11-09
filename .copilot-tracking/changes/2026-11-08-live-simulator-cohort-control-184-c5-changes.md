---
title: "#184 C5 changes: readers enforce the 14-day control maximum"
ms.date: 2026-11-08
---

Research and plan/details were committed first (37f0299c). Pre-edit head 10c550a8, tree 725fe080.

## Source

* src/api/src/zava_forward/api/live_control.py: new INVALID outcome; `decide` returns EXPIRED first, then INVALID for an expiry beyond now + 14 days, then SEND or STOPPED. Simulator gate, receiver `window_seconds` and the receiver watch all use `decide`, so none changed.
* src/api/tests/test_live_control.py: five new tests (decide table incl. exactly 14 days, 365 days, 1 day, disabled over-window; expired stays EXPIRED; receiver window refusal and run_window; mid-window rewrite beyond 14 days stops the watcher; simulator `main` with a 365-day file). All synthetic, no network or persistence.
* sha256 live_control.py 2c787033e08bc3c606ceceb5f5fe1c61f7dc5ad5d065015a1b5434ba4ae04cbe; test_live_control.py f20dc25abee72d272d4bfb6d68fd7883fabfa746d15641fe825f6aab41734446.

## Results (separate files /tmp/c5-*.{out,err,exit}; checkout source imported, path printed)

| Step | Exit | Result |
| --- | --- | --- |
| Red, unchanged source, test_live_control | 1 | 34 run, 3 failures, 1 error (no INVALID; over-window reached the store, main code 3 not 0) |
| Green: test_live_control, test_live_receiver_sql, test_sensor_ingestion, test_iot_stream | 0 | 120 OK, 2 expected SQL-only skips |
| ruff check, two files | 0 | clean |
| ruff format --check, two files | 0 | formatted |
| mypy 2.4.1 (system python, --cache-dir=/tmp/mypy-184), live_control, live_receiver, live_simulator | 0 | no issues |

Retained venv lacks mypy and holds a stale non-editable copy, so PYTHONPATH put the checkout first. The first mypy attempt in that venv failed (module missing); output /tmp/c5-mypy.err was overwritten by the rerun, noted here as a limitation.

## Not done

* No SQL Server, Docker, browser or heavy gate. Earlier f28 SQL 70/0 skip and unit 139/2 skip are historical after this edit.
* Low gap (exact-grant live_receiver.main and rejected data-quality SQL tests) unrelated and still open.
* FULL local gate and external receipt pending; coordinator admits it on the exact final commit in a clean checkout and verifies against fresh origin/main.
