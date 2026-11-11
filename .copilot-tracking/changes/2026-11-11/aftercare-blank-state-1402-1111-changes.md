<!-- markdownlint-disable-file -->
# Changes: aftercare blank stored state (issue 1402, C1 of 3)

Plan: [plan](../../plans/2026-11-11/aftercare-blank-state-1402-1111-plan.md). Critique: [critique](../../plans/2026-11-11/aftercare-blank-state-1402-1111-critique.md). Planning commit `6ac95f78b` precedes all source/test changes.

## Source

* `src/core/src/zava_forward/core/aftercare_intake.py` `_parse`: `if text is None or not text.strip()` became `if text is None`. Blank or whitespace text now reaches `json.loads`, raising the existing `StateInvalid` ("left unchanged"). Absent state still initialises.

## Tests

* `src/core/tests/test_aftercare_intake.py` new `BlankStateTests`: absent-state initialisation and replay (RC-AC-001), blank read refusal, blank write refusal, HTTP 503 and restart with bytes unchanged for `""`, `"   "`, `"\n\t \n"`, and a valid nonempty document not reset (RC-AC-002).

## Evidence (`.copilot-tracking/evidence/2026-11-11/aftercare-blank-state-1402-1111/`, per-attempt stdout/stderr/exit)

* `red-1`: exit 1, failed 9 subtests plus 2 errors caused by my test using wrong receipt keys and a reused request id (test bug, preserved, not hidden).
* `red-2`: corrected tests against unfixed source, exit 1, 9 failures (all blank-state paths), the 2 positive controls pass. Source SHA256 `d8c21eee...a15`.
* `green-1`: same tests on fixed source, exit 0. Source SHA256 `30ce83d9...b4ef`.
* `green-2-intake`: full intake module, exit 0. `green-3-core-aftercare`: exit 5 NO TESTS RAN because of my wrong discover pattern (preserved; superseded by `green-5`). `green-5-core-aftercare`: `tests.test_aftercare` 23 tests, exit 0. `green-4-api-screen`: exit 0.
* `lint-ruff-check` and `lint-ruff-format`: exit 1, one line too long in my new test (fixed). `lint-mypy`: exit 0.
* Final candidate after the line fix: `lint-2-ruff-check` 0, `lint-2-ruff-format` 0, `green-6-intake-final` (`test_aftercare_intake` + `test_aftercare`, 67 tests) 0, `green-7-api-screen` 0.
* Imports: all resolved to this worktree's `src/core/src/zava_forward/core/aftercare_intake.py` via explicit `PYTHONPATH`; no installs.

## N/A (explicit)

* `test_aftercare_store.py`, `test_aftercare_served.py`: reference SQL stores, unreachable branch through `DocumentStateStore`, SQL not admitted: N/A.
* SQL, MSSQL, cloud, deployment, private data, resource lock, full gate: N/A. Numeric-ordering source and tests untouched.

## Limits

Standalone `FileStateStore` only. A raw blank JSON through the connected runtime adapters is not claimed. A refused update may leave an empty `.lock` file beside the preserved state file.
