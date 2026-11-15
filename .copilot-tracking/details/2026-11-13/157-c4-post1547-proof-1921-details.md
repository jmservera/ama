# Details: #157 Criterion 4 proof (157-c4-post1547-proof-1921)

* Commands (venv `/tmp/venv-157c4-1921`): from `src/core/tests` run `python -m unittest test_chat_panel -q`; from `src/api/tests` run `PYTHONPATH=../../core/tests:../../agents/tests python -m unittest test_chat_panel test_chat_widget_focus -q`.
* Clauses: calls per request; context size per thread; memory use; per-role limits; reported before activation; workflow-only fallback.
* Strict rule: no test assertion, or a constant standing in for a measurement, means `NOT FULLY PROVEN`.
* Output: `.copilot-tracking/changes/2026-11-13/157-c4-post1547-proof-1921-changes.md`.
