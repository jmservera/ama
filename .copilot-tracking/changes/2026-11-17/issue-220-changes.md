---
title: Issue 220 changes
ms.date: 2026-11-17
---

# Changes

* Planned: test in `src/api/tests/test_challenge_non_retaliation_hazard_guard.py`; status note in `src/core/README.md`.

# Done

* Added `test_hazard_concern_is_routed_to_hazard_intake_and_saves_nothing` (measured: first draft expected 200; real behaviour is a 400 redirect to independent hazard intake, nothing saved, hazards and ranks unchanged; test corrected to that behaviour).
* `src/core/README.md`: 2026-11-17 assessment under the #220 status record; criterion 5 stays unmet.
* Validation: `src/api` guard test file, 9 tests OK (PYTHONPATH to worktree sources); `src/core` `tests.test_challenges` 19 OK (base); `ruff format --isolated --line-length 100 --check` on the test file OK; `mypy .` in src/api: no issues in 309 files. Not run: rpi-checks --all (full gate lock held, FOCUSED tier), browser checks (no UI change).
