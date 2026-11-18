# Changes: #215 unblock and visit grounding (Refs #215)

* Added `src/api/tests/test_alert_chat_unblock_visit_grounding_215.py` (11 new tests; the API class also inherits the role-matrix tests).
* No source change: no deterministic grounding or provenance bug reproduced; PR #1576 behaviour untouched.
* Tracking records: research, plan, details, critique, this file, review, state.

## Validation (focused tier, run from `src/api`, PYTHONPATH set to worktree `src/*/src` and test dirs)

* `python3 -m unittest test_alert_chat_unblock_visit_grounding_215 test_chat_panel test_alert_chat_citation_source_attribution_215 test_chat_case_answers`: 101 tests OK.
* `ruff check`, `ruff format --check`, `mypy` on the new file: clean.
* Not run: `rpi-checks.py --all`, Docker, cloud calls, browser harness. Hosted CI for the exact head is not observed; not pushed.
