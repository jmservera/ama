# Plan: #107 F1-F4 fixes (1531)

* [ ] P1 `ai_consumption.py`: limit 80 shared constant; oversized str -> sentinel; new `_SECRET`.
* [ ] P2 `assistants.py`: annotate `Limits.__init__`, `sanitize_identity`, `shape_result`; stop pre-truncating identity fields.
* [ ] P3 tests: annotate; add oversize, F2 shapes (hex32, JWT, AKIA, ghp_, github_pat_), F4 accepted names (gpt-4.1-nano, gpt-4.1-mini, resident-mini, task-summarisation-v1, offline-fixture).
* [ ] P4 run mypy x3, ruff, unit tests in /tmp/venv-107-c1-1531.

Details: `.copilot-tracking/details/2026-11-13/107-c1-review-fixes-1531-details.md`
