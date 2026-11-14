# Plan: monitoring outputs wiring contract tests (Refs #146)

* [x] Add `infra/tests/test_bicep_monitoring_outputs_wiring.py` (source-shape tests, 7 cases).
* [x] Validate with unittest, `ruff check`, `ruff format --check`.
* [x] Commit on the stacked branch; do not push.
* Critique: executed once, verdict compatible; no Bicep edits since no gap exists. Local-only focused tier (test-only, no gate/infra change).
