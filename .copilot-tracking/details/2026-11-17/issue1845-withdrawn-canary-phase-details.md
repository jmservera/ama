---
title: Issue 1845 withdrawn-sensor canary phase details
description: Step-level details, commands and evidence expectations for the canary repair
ms.date: 2026-11-17
ms.topic: reference
---

## Phase 1: helper and test update

File: `src/api/tests/test_quality_sensors.py` only.

Helper, placed beside `stamp` (revised after the critique):

```python
def exposes(body: Any, value: str) -> bool:
    """True when value appears in a key or string, or as a numeric leaf equal to it."""
    if isinstance(body, dict):
        return any(exposes(k, value) or exposes(v, value) for k, v in body.items())
    if isinstance(body, list | tuple):
        return any(exposes(item, value) for item in body)
    if isinstance(body, bool):
        return False
    if isinstance(body, int | float):
        return body == float(value)
    return value in str(body)
```

Rationale: epoch-second metadata (`created_at`, `as_of`, `not_before`, `at`)
is a JSON number, `1794924123.7340033` is not equal to `23.7`, so it no longer
collides, while every string value or key keeps the original substring
semantics and `23.70` or a bare reading `23.7` still match by value. Limit: a
numeric leaf exactly equal to the canary is treated as exposure.

Edits in the target test: positive controls use `assertTrue(exposes(body, ...))`
on the parsed output and detail bodies; the loop uses
`assertFalse(exposes(body, derived), name)` without serializing.

## Phase 2: constructed-metadata regressions

New `class WithdrawnCanaryMatch(unittest.TestCase)` in the same file (no
subclass elsewhere, so it runs once and never under the SQL fixtures):

* `test_numeric_timestamps_that_contain_the_canary_are_not_exposure`: body with
  `created_at 1794924123.7340033`, `as_of 1794924123.7119958`,
  `at 1794924124.9123`; assert the substring collision exists for `23.7` and
  `24.9` (documents the old false positive) and `exposes` is False.
* `test_original_edited_and_numeric_exposure_is_still_found`: for each of the
  mock provider's three original fields, the edited summary and a
  `temperature_c` number, a `23.70` value and a key, embed it with the
  colliding timestamps and assert `exposes` is True for its canary.

## Phase 3: failing-before and passing-after

Environment: venv `work/venv` (pip, editable from `git archive` of HEAD under
`work/archive`), `ZF_DATA=work/zfdata-1845/zavaforward.json` (synthetic,
run-local), from `src/api`:
`PYTHONPATH=tests:../core/tests:../agents/tests`.

* Failing-before (scratch copies under `work/scratch`, never committed):
  1. scratch copy with the old substring assertion and clean colliding
     timestamps injected into every projection: the integration test fails;
     the fixed test with the same injection passes;
  2. fixed test with the original text, then the edited text, injected into
     one projection at a time (detail, list, export, sensors): each run
     fails on that named projection.
* Passing-after: run `test_quality_sensors.WithdrawnCanaryMatch`, the target
  `Http` test, the other `_after_withdrawal` users and the whole `Http` and
  `ReadModel` classes for this module; record counts and skips. SQL-gated
  `Mssql*` classes skip by design (no SQL admission); the skip count and
  reason are reported, not counted as pass.

## Phase 4: static checks

From `src/api`: `ruff check . && ruff format --check .` and `mypy` (CI
commands), plus `git diff --check` and `git status` for stray caches. No
broad Core/API discovery run and no duplicate command.

## Validation tier record

FULL by the conservative brief decision. The coordinator runs the final full
gate on the frozen candidate; this launch's Review is Partial while that
evidence is missing.
