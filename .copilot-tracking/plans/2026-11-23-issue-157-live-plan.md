# Plan 2026-11-23: issue 157

* Phase 1: add a failing regression test in src/core/tests/test_chat_privacy.py (contractor cannot start a thread on another contractor's case; hidden and missing case raise the same ChatNotFound; no thread stored; visible case still works).
* Phase 2: make `ChatPrivacy.start_thread` resolve the case through `store.detail(case_id, user)` and raise ChatNotFound for hidden or unknown cases, after the approval check.
* Phase 3: run core chat tests and api chat thread tests, mypy and ruff in src/core. Tier FULL for src change (commit-level; no rpi-checks --all).
* Phase 4: per-criterion table in the changes record.
