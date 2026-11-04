# Details: issue 108 held-out freeze check (2026-11-04)

## Phase 1

File: src/agents/src/zava_forward/agents/heldout_freeze.py. Checks versions, split (ids, seed, denominator, expected, critical errors, independent labeller), prompt/tuning leakage, thresholds and digest-bound approval, cohort subset and minimum sample. Outcome `frozen` or `insufficient`.

## Phase 2

File: src/agents/tests/test_heldout_freeze.py (13 tests, synthetic). README: Held-out freeze check section.

## Phase 3

Unit tests, ruff check and format, mypy with --cache-dir=/tmp/mypy-108. Not run: gate, benchmarks, full suites. No SQL, security, infrastructure or deployment change.
