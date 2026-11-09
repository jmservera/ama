---
title: Issue 189 C1 complete src/api suite capture
description: Additive record of the one owner-authorized complete src/api unittest discovery at source head; no product change
ms.date: 2026-11-09
---

Additive to the frozen C1 records and the F3 diagnostic. A native qualified `rpi-agent` validation continuation of C1 (cycle 1 of 5, four remain; no counter reset, no synthetic sixth cycle). Source `3d8a7a012bdc2e09d7278fe443b95024cfc72ac1`, evidence head `3fa677c42`, clean worktree before the run, base `df8e858b2` untouched. Coordinator authorized exactly one complete `src/api` discovery to resolve the impacted-API validation gap after the narrow method, predecessor prefix, 110-test discovery and 122-module import-only collection did not reproduce F3.

## Preconditions verified

* Interpreter `../../.venv/bin/python` 3.12.3 (the original one).
* `zava-forward-api`, `-agents` and `-core` 0.1.0 are editable installs whose `direct_url.json` points at this worktree's `src/api`, `src/agents` and `src/core`. No global install.
* No `ZF_*`, Azure or OpenAI variables set; `~/.zava-forward` does not exist, so no private `ZF_DATA`. Tests use temporary data and synthetic fixtures; no model, live or Azure call.
* Skips are the tests' own opt-in gates. No SQL lock, network or provider activation, no other project suite, no repeat.

## Command and result

From `src/api`: `PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -v`, stdout and stderr redirected to separate files with no pipe filter; the producer's exit status was captured directly.

| Item | Value |
| --- | --- |
| Producer exit | `0` |
| Summary | `Ran 2105 tests in 935.920s`, `OK (skipped=365)` |
| Window (UTC) | 2026-11-09T13:49:06Z to 14:04:43Z |
| Errors and failures | None. `test_ai_consumption_api...test_assistant_completion_preserves_capacity_quarantine_and_terminal_release` ran `ok` |
| Worktree after | Clean apart from this evidence |

Raw output is retained unfiltered in [stdout](simulator-control-189-c1-api-capture/stdout.txt) (rendered-check lines, sha256 `7f80af79...986acb`), [stderr](simulator-control-189-c1-api-capture/stderr.txt) (unittest verbose log, sha256 `0955d188...a8c8b`) and [producer exit](simulator-control-189-c1-api-capture/producer-exit.txt). The 280 `Traceback` lines in stderr are logged, handled exceptions inside tests that then report `ok` (for example `Rule evaluation unavailable for ZF-1` in `test_auth.ProxyHttpTests`); none belongs to an `ERROR` or `FAIL` result.

## Named opt-in skips (365, not SQL or browser proof)

227 `needs a SQL Server (ZF_TEST_MSSQL=1)`; 66 `needs disposable SQL Server (ZF_TEST_MSSQL=1)`; 37 `owned local MSSQL opt-in`; 11 `opt-in loopback SQL Server`; 8 `opt-in isolated local SQL Server`; 7 `opt-in loopback MSSQL`; 2 `needs the task-owned SQL Server`; 1 `JSON does not have a SQL COMMIT acknowledgement boundary`. Browser: 2 `opt-in Chromium journey`, 1 each `Opt-in rendered check requires local Playwright browser`, `opt-in local Chromium`, `opt-in local Playwright`, `opt-in local browser`. SQL and browser behaviour stay unproven locally.

## F3 disposition

The complete current API suite passes at the exact source. The original `1 error` was not reproduced by this capture or the earlier diagnostics, and its traceback was lost. Its cause is not established and is not claimed unrelated, flaky or baseline. This record is current exact-source validation only, so the pinned-base minimal comparison was not applicable. All earlier adverse and invalid harness outputs (original error summary, F3 diagnostic run 1 invalid harness) are retained. No product edit and no C2 source authorization. The record does not replace independent exact-head review, human approval, hosted CI or the full tier for the shared host integration, which still waits for #1292 on main.
