# Changes: issue 135 exception queue slice

Date: 2026-11-01

* Added `src/core/src/zava_forward/core/exception_queue.py`.
* Added `src/core/tests/test_exception_queue.py` (10 tests).
* Added README section in `src/core/README.md`.

Divergence: none from plan. Validation: unittest (new tests and dependency rule) pass; ruff check and ruff format --check pass on touched files. mypy on touched files passes with `--follow-imports=skip`; the project-wide mypy run fails on a pre-existing syntax error in `assistant_release.py:185` on main, untouched here (also breaks repo-wide ruff check, which reports only that file).

Review-thread amendments (PR 666): `access_report` now needs a named actor and filters item-linked audit entries to the role scope; steward denials in `set_outage`/`clear_outage` are audited; outage note and clearance evidence are appended to the audit; `outage_banner` returns Unknown for missing, malformed, future or stale (over one hour) checks. Tests extended (12 tests).

Second review-thread amendment (PR 666): backing collections made private (`_items`, `_audit`, `_outages`); `clear_outage` normalises the component like `set_outage`; `access_report` appends a `viewed_access_report` audit event after its scoped snapshot. Two tests added (13 tests).
