---
title: Issue 891 chat call accounting C1 changes
ms.date: 2026-11-09
task_id: issue-891-chat-call-accounting-1109-c1
---

## Chronology (actual `date -u` and commit times)

* 22:52:31Z main fetched (`1b7a1719`); 22:52:34Z merge `97f0036b`; 22:53Z research probe (red evidence); 22:55:46Z planning commit `ab6d7b1ab` (research, plan, details, single critique).
* 22:55:50Z Implement activated and read back as `Implement` in the C1 state before any test or source edit. Tests first: the new core test module and the rewritten adapter tests, run red at about 22:56Z (logs `c1-red-*.log`: agents 3 failures, core 1 failure and 12 errors on the missing marker). Then `ai.py` and `chat.py`.
* 23:01:43Z source commit `f466f4997`.
* The earlier parent-loop state lag is preserved and not touched.

## Changed files

* `src/core/src/zava_forward/core/ai.py`: `DispatchWitness`, `DISPATCH` context variable, `count_dispatches()`; `Ai.evidence` marks the open witness; `Ai._request` increments attempts after the opener is built and directly before `with open_request(...)`. No reserve, complete, check, guard, bound or outcome mapping changed.
* `src/agents/src/zava_forward/agents/chat.py`: `provider_calls` heuristic removed; `ChatModel` opens a witness around `worker.provider_call`. Unwitnessed providers log a bounded warning and assume one call.
* `src/core/tests/test_ai_dispatch_marker.py` (new, 8 tests), `src/agents/tests/test_chat_model.py` (heuristic tests replaced by transport-counted tests; one stub-provider test adjusted to the unverified count), `src/agents/README.md` (counting contract and limits).
* No server, navigation, store, schema, activation, registry, `ai_transport.py`, `ai_consumption.py`, `chat_panel.py` or dependency edit.

## Case mapping (real `Ai`, counted `urlopen` stub)

| Case | Transport | Reported |
| --- | --- | --- |
| unconfigured, meter missing, reserve held, check hold after reservation, guard denial, token failure, input refusal, opener construction failure | 0 | 0 |
| response, transport error, completion hold after dispatch | 1 | 1 |
| two concurrent invocations (one sent, one held) | 1 | 1 and 0 |
| nested, closed and copied-context witnesses | n/a | own invocation only |
| non-Ai provider with spoofed envelope keys | n/a | 1, logged unverified |

## Validation (exit codes; raw logs in `logs-891-fresh-accounting-1109/c1-*.log`, not committed)

| Check | Exit | Result |
| --- | --- | --- |
| red, agents `test_chat_model` | 1 | 3 failures (expected) |
| red, core `test_ai_dispatch_marker` | 1 | 1 failure, 12 errors (expected) |
| agents `test_chat_model` | 0 | 13 OK |
| agents full suite | 0 | 309 OK |
| core marker plus `test_ai_input_bounds` | 0 | 14 OK |
| core `test_ai_consumption*` | 0 | 42 OK |
| core `test_chat*` | 0 | 134 OK |
| core `test_*demo*` | 0 | 7 OK |
| API `test_ai_call_site_inventory`, `test_chat_panel`, `test_chat_isolation`, `test_ai_consumption_api`, `test_continuity`, `test_quality_simulation_lane` | 0 | 6, 55 (1 skipped opt-in Chromium, no new UI evidence), 32, 17, 22, 30 OK |
| ruff check, ruff format --check, mypy (agents and core) | 0 | pass |
| core `test_*simulation*` pattern | 5 | matched no tests (the simulation lane tests are the API module above) |

Failed attempts kept: `c1-agents-ruff-check-FAILED-first.log`, `-FAILED-second.log` and `c1-core-ruff-check-FAILED-first.log` (E501 line length), `c1-agents-mypy-FAILED-first.log` (unused type-ignore). Each was fixed by editing and rerun. Correction cycles spent: 1 of 5 (this C1).

## Limits

* Exactness holds for the trusted composition where the provider is core `Ai.evidence`. A non-Ai or other-thread provider is an unverified upper bound of 1, not shown as measured in the receipt; a provenance field needs the shared `chat_panel.py` (follow-up).
* A fence withdrawn inside the opener before the first byte still counts as an attempt; redirects inside `urlopen` are not counted separately.
* Criterion 2 of #891 is not established: no token, cost, privacy, retention or refusal conjunction, no live observation. Focused tier, not the complete gate.
