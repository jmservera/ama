# Plan: issue 1204 live (2026-11-24)

* [x] Add `require_extended` to `check_ticks` and `--require-extended` to the CLI in `tools/check-tick-log.py`; a row lacking any extended key gets a `schema` violation.
* [x] Add focused tests in `tools/test_check_tick_log.py`.
* [x] Run unittest, ruff, and the checker on the real 216-tick window (default and strict).
* [x] Research note with per-criterion table; changes record; review.
