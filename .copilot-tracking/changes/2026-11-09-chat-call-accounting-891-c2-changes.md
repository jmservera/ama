---
title: Issue 891 chat call accounting C2 changes
ms.date: 2026-11-09
task_id: issue-891-chat-call-accounting-1109-c2
---

## Chronology (actual)

* 23:17:13Z start at clean head `613a1919`. Planning commit `87f57eb45` (research, plan, details, one critique: Revise, dispositioned directly). 23:18:44Z Implement activated by `date -u` and read back as `Implement` (the first activation script failed on a typo and wrote nothing; the retry is the real activation). Red regression run next, before any fix. Source commit `662c8466d` at 23:21:01Z.
* C1 records and original reviews are untouched. C1 wording "upper bound" is corrected only in the README and here; the C1 records keep their original text as history.

## Changes (tests and wording only; no production source)

* `src/core/tests/test_ai_dispatch_marker.py`: the guard-denial case uses a scoped context patch, repeated `setUp` calls were replaced by an `ExitStack` of scoped patches; new `GuardPatchIsolation` subprocess regression (marker `DispatchWitness`, assert guard original, `patch.stopall()`, assert original, then `test_ai_input_bounds` in the same interpreter); new pin that withdrawal, `TimeoutError` and `HTTPError` raised from the opener after hand-off each count one attempt with one `.open` call and zero `urlopen` calls.
* `src/agents/README.md`: the unwitnessed count is an unverified legacy assumption of one call, not exact, not a bound, not a billing estimate; attempt means a request handed to the transport, for the trusted synchronous `Ai.evidence` composition.

## Red to green

| Check | Exit | Result |
| --- | --- | --- |
| red core marker (`c2-red-core-marker.log`) | 1 | new regression failed: "guard leaked after stopall"; 9 other tests passed |
| core marker | 0 | 10 OK |
| order: marker, `test_ai_input_bounds`, `test_data_protection`, `test_ai_consumption` in one interpreter | 0 | 67 OK |
| core `test_ai_consumption*` / `test_chat*` | 0 / 0 | 42 / 134 OK |
| agents full / `test_chat_model test_dispatch test_worker` | 0 / 0 | 309 / 34 OK |
| API `test_ai_call_site_inventory` / `test_chat_panel` | 0 / 0 | 6 / 55 OK (1 skipped opt-in Chromium; no UI evidence) |
| ruff check, format --check, mypy (core, agents) | 0 | pass |

Preserved failed logs: `c2-core-mypy-FAILED-first.log` (3 type errors), `c2-core-ruff-FAILED-first.log` (import order). Logs in `/home/azureuser/source/ama-demo-wt/logs-891-fresh-accounting-1109/c2-*.log`. No SQL, browser, model, provider or network. Cycles: 2 of 5.

## Limits

Criterion 2 of #891 stays unmet; no production, financial, privacy, activation or gate change; no receipt provenance feature.
