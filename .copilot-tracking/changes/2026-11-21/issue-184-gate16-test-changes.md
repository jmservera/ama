---
title: Issue 184 gate run16 test fix changes
ms.date: 2026-11-21
---

# Changes

* Modified src/api/tests/test_live_control.py: ReceiverJobContractTests asserts the conditional trigger expression, the empty default cronExpression and the manual/schedule config selectors. Bicep unchanged.
* Tier: focused (test-only, no src change).

## Acceptance criteria (issue #184)

| Criterion | Status | Basis |
| --- | --- | --- |
| All child stories closed or deferred | Already ticked in the issue | Not re-proven; out of scope for this test fix |
| Simulator never connects to, discovers or represents installed real devices | Already ticked in the issue | Not re-proven; out of scope |
| No device key or connection string in source, logs or telemetry | Already ticked in the issue | Not re-proven; SecretHygieneTests still run in the suite |

No criterion is unticked, so no live Azure evidence was gathered.

## Validation

* `test_live_control`: 58 tests, OK (includes the amended ReceiverJobContractTests).
* Whole src/api suite, sequential: 4379 tests, 662 skipped, 2 errors. Both are import errors (`test_assistants_dispatch`, `test_keepalive`: `ModuleNotFoundError: opentelemetry`), an environment gap unrelated to this change.
* ruff check and ruff format (line length 100) on the test file: clean.
* mypy in src/api: 7 errors in one file (src/core/tests/telemetry_support.py, missing opentelemetry stubs). Identical count with the change stashed, so pre-existing and environmental.
* implement-start witness qualification: the test edit was issued in parallel with the witness call, so the witness saw a dirty source tree.
