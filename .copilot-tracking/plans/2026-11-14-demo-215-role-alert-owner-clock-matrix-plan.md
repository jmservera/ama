# Plan: #215 role alert owner clock safe-action matrix (2026-11-14)

* [x] Add `src/api/tests/test_epic215_role_alert_owner_clock_safe_action_matrix.py`: static template/CSS checks plus engine checks for all 7 role groups and suppliers.
* [x] Run the four focused checks, then clean up the mypy cache.
* [x] Commit with `Refs #215` and the Copilot co-author trailer; do not push.

Critique: executed once; accepted. Compatible findings applied directly: use the real `AUDIENCES` for expectations, add a second synthetic card so coordinator alerts exist, avoid trivially-true assertions.
Classification: focused tier (test-only, no gate, workflow or dependency change).
