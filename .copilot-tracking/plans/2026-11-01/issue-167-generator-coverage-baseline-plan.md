# Issue 167 plan: register is_synthetic conformance check

* Date: 2026-11-01
* Research: [research](../../research/2026-11-01/issue-167-generator-coverage-baseline-research.md)

## Phases

* [x] Phase 1: add `check_register_labels(path)` and `--register PATH` to
  `src/core/src/zava_forward/core/synthetic/coverage.py`; report `register_label_conformance`
  (rows, labelled, unlabelled, missing_column), exit 1 when nonconforming; never print row content.
* [x] Phase 2: tests in `src/core/tests/test_generator_coverage.py` with fictional CSV rows
  (all true, a false/blank row, missing column, CLI exit code).
* [x] Phase 3: update core README and retrofit-synthetic-data README (open item), log entry.
* [x] Phase 4: ruff check, ruff format --check, mypy, unit tests; commit, push, PR with `Refs #167`.

## Critique (single pass)

* Compatible: keep output aggregate-only to avoid leaking private rows; accept `true/True/1`.
* Rejected: adding owner-approval claims; remains `not-established`.
