# Plan: issue 130 identity 403 (2026-11-18)

* [x] Phase 1: replace whole-dict comparison in `resident_decisions._operation` by `_same_signed_in_person` over email, code, oid.
* [x] Phase 2: regression tests in `src/core/tests/test_resident_decisions.py` (matching Entra principal accepted; forged principals refused without mutation; differing roster person refused).
* [x] Phase 3: validation (resident tests, mypy per project, ruff), mutation probe, per-criterion research note, knowledge-base index and log.
* No push, no deploy, no full gate. Details: `.copilot-tracking/details/2026-11-18/issue-130-identity403-live-details.md`. Critique: `.copilot-tracking/critiques/2026-11-18/issue-130-identity403-live-critique.md`.
