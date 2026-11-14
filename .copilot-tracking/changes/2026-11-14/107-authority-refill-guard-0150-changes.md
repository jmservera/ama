# Changes: authority rotation guard (Refs #107)

* `src/core/src/zava_forward/core/assistants.py`: new `Assistants._pool`; `_reserve` and `disabled` use it. Attempts keep settling against their original pool id.
* `src/api/tests/test_assistant_restart_non_replenishment.py`: three rotation tests.

## Validation (focused tier)

* Failing-first: 3 new tests failed without the change.
* `ruff check` (core src, api tests): pass. `mypy src` in `src/core`: pass.
* Core `test_rai*.py` (15) and `test_assistants*.py` (5): OK.
* API `test_assistant_restart_non_replenishment`, `test_assistants`, `test_assistant_reserve_guard`, `test_assistant_release`: 216 tests OK (66 skipped).
* Not run: full local gate, hosted CI, independent exact-head review, human approvals.

`docs/reference/log.md` deliberately not edited.
