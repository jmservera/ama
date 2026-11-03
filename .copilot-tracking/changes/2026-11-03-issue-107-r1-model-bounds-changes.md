<!-- markdownlint-disable-file -->
# Issue 107 R1 model bounds: changes

## Changes

* `src/core/src/zava_forward/core/assistants.py`: constants, `model_bounds()`, registry view field, `ATTEMPT_CEILING` used in limit bounds (value unchanged, 3).
* `src/api/tests/test_assistants.py`: 3 tests.
* `src/agents/tests/test_dispatch.py`: 1 test.
* `src/agents/README.md`: bounds section and unmet items.

## Validation (focused tier; PYTHONPATH to src dirs, no install, no ignored files)

| Command | Result |
| --- | --- |
| `test_assistants test_assistant_release` (src/api) | 155 OK, 53 skipped (MSSQL not enabled) |
| `test_dispatch` (src/agents) | 15 OK |
| `ruff check` / `ruff format --check` on touched files | clean |
| `mypy --cache-dir=/tmp/mypy-107` on the new test | only import-untyped notes for installed-path resolution; no errors in new code |

Not run: gate, benchmarks, full suites, MSSQL tests, CI jobs. Not security, infrastructure, SQL or deployment tier.

## Acceptance criteria status

Met by earlier merged work: base criteria 1 to 5 and RAI criteria 2, 4, 6, 7, 9. Advanced here: Tokenomics 1 (stated and tested, in code only). Still unmet: RAI 1 (approvers unset), 3 (serving attestation), 5 (independent Azure SQL race evidence), 8 (delivered-build evidence); Tokenomics 2 and 3. Hence `Refs #107`.
