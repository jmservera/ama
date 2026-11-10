---
title: Issue 891 chat call accounting C2 details
ms.date: 2026-11-09
task_id: issue-891-chat-call-accounting-1109-c2
---

* Regression module `src/core/tests/test_ai_dispatch_marker.py`: `IsolationTests.test_guard_patch_is_restored_after_the_witness_cases` runs `DispatchWitness` through `unittest.TextTestRunner(stream=io.StringIO())` and asserts `data_protection.dispatch_hold is original` and the run passed. A second test runs a subprocess `python -m unittest test_ai_dispatch_marker test_ai_input_bounds` in one interpreter (core tests dir on PYTHONPATH) and asserts exit 0, proving order independence.
* Case helper: `arrange(self, label)` returns a context manager; denial uses `mock.patch(..., return_value="denied")` entered with `with`.
* New pins: `test_withdrawal_from_the_opener_still_counts_one_attempt` (patch `ai_consumption.SEND_FENCE` and `ai_transport.opener` to return an object whose `.open` raises), `test_timeout_and_http_error_after_handoff_count_one`.
* README: replace "upper bound" sentence.

## Amendments from the critique

* Subprocess script: load `test_ai_dispatch_marker.DispatchWitness` only, run, assert guard is original, `patch.stopall()`, assert original, then run `test_ai_input_bounds`; use `subprocess.run(..., timeout=120)`. It sits in class `IsolationTests`, never selected by the subprocess.
* Pins assert `DispatchWithdrawn` from the stub `.open` (outcome `suspended-before-dispatch`), TimeoutError (`timeout`), HTTPError (`provider-unavailable`), each with one hand-off and one stub invocation.
