# Changes: issue #219 authority-holder register (2026-11-01)

Plan: [plan](../plans/2026-11-01-issue-219-rai-release-record-plan.md)

* `src/core/src/zava_forward/core/rai_release.py`: added `AUTHORITY_ROLES`, `authority_register()`.
* `src/core/src/zava_forward/core/assistant_release.py`: denial adds `authority_holders` (additive).
* `src/core/tests/test_rai_release.py`, `src/api/tests/test_assistant_release.py`: new assertions.
* `src/core/README.md`: documents the key.

Validation: core release tests (12) OK; api `test_assistant_release` and `test_assistants` 149 OK (50 skipped); ruff check, ruff format --check, mypy (core) clean; ruff clean for api. Local pip packages not installed, so PYTHONPATH src paths were used. No heavy gate run; CI is the evidence.

Divergences: none.

## Correction cycle (PR #696 review threads)

* `src/core/README.md`: `authority_holders` scoped to `assistant_release.denial()` denials; disabled-task path excluded.
* Review artifact: independent review marked pending; original self-review preserved.
