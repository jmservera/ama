<!-- markdownlint-disable-file -->
# Details: aftercare blank stored state (issue 1402, C1)

## Phase 1: regression tests in `test_aftercare_intake.py`

New class `BlankStateTests(Base)`:

* absent file (None) read returns empty concerns; first write succeeds and assigns `AC-001`; an exact replay returns the same receipt (positive control).
* for each of `""`, `"   "`, `"\n\t \n"` written as bytes: `svc.concerns(MANAGER)` raises `StateInvalid`; `svc.record_concern` raises `StateInvalid`; `handle("POST", ...)` returns 503 with "left unchanged"; file bytes unchanged; a recreated store and service (restart) still refuses and bytes remain unchanged; no `.lock` side effects checked beyond bytes.
* existing valid nonempty document: record a concern, restart, read returns it and a second write gives `AC-002` (not reset).

Expected RED: the blank read returns an empty register and the write overwrites bytes.

## Phase 2: fix

`_parse`: `if text is None: return _blank()`.

## Success

New tests fail before and pass after; all existing affected tests pass; ruff/format/mypy clean for changed files.
