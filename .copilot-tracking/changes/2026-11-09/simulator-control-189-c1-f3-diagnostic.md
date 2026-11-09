---
title: Issue 189 C1 F3 import-collection diagnostic
description: Additive diagnostic record for the unresolved selected-suite error F3; no product change
ms.date: 2026-11-09
---

Additive to the frozen C1 records. A native qualified `rpi-agent` diagnostic continuation of C1 (cycle 1 of 5, four remain; a diagnostic alone does not reset the count). Head `3d8a7a012bdc2e09d7278fe443b95024cfc72ac1`, clean worktree, base `df8e858b2` untouched, `origin/main` `ad679b96b` with no `src/api` change.

## Question

Does importing every original API test module at unittest discovery, before executing only the failing method, reproduce the original error? The earlier bounded prefix (`test_a[a-i]*.py`, 110 tests) imported fewer modules.

## Reproducer

`/tmp/c1f3/repro.py` (not committed). From `src/api` with `PYTHONPATH=../core/tests:../agents/tests` and the head `.venv` (Python 3.12.3), it runs `TestLoader().discover("tests")` (imports every module, same as `unittest discover -s tests`), then runs only `test_ai_consumption_api.ConsumptionApi.test_assistant_completion_preserves_capacity_quarantine_and_terminal_release` with verbosity 2. Producer exit status is captured directly with no pipe filter. No private `ZF_DATA`, global install or credentials; no sleep, poll or retry loop.

## Results

| Run | Collection | Outcome |
| --- | --- | --- |
| 1 (invalid harness) | 1761 tests, 103 modules, 20 import failures | Discarded: the script directory, not `src/api`, was on `sys.path`, so `checks.*` imports failed. Fixed to match `python -m unittest` (cwd first). Raw `/tmp/c1f3/head-repro.txt` kept. |
| 2 (valid) | 2105 tests, 122 modules, 0 import failures | Target method ran 1 test in 11.0 s, subtests including `model='other-model', capacity=False, revoked=True`: OK, 0 errors, 0 failures, producer exit 0. Raw `/tmp/c1f3/head-repro2.txt`, copy `head-full-collection-repro.txt`. |

## Conclusion: UNKNOWN

* Not reproduced with full import collection at head. Per the brief the isolated pinned-base run was not made, because it applies only if the error reproduces.
* F3 cause is not established and the original error is not waived. No "unrelated", baseline-failure, flaky or Pass claim is made. The original `1 error` summary and the lost traceback stay as recorded.
* Coverage: all 122 modules imported (2105 collected, versus 2103 ran in the original, a difference not investigated), then only the one method executed. Not covered: execution of the other tests before it (shared state from running, as opposed to importing, earlier tests), wall-clock or load interaction, and the full-suite run order. Only the owner-selected full-suite capture with raw output can settle those.
* No product edit. No precise coupled regression was confirmed, so there is nothing for C2 source authorization.

## Not run

Whole suite, 300-test or 50-retry loops, SQL gate, full gate, cloud, push, PR, issue, board, merge. Final host integration still waits for #1292 on main.
