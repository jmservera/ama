<!-- markdownlint-disable-file -->
# Changes: closed-stdin refusal D1

* Plan `.copilot-tracking/plans/2026-11-10-issue-129-stdin-d1-1110-plan.md`. Status: implementation complete; D1 Review pending. Start head `5cec9663559bebfae3b3a2a7d38fd179b8c84b10`, clean.

## Changes

* `src/core/src/zava_forward/core/learning_test_bundles.py`: 4 lines. `main` raises the existing handled `ValueError` with a fixed message when `sys.stdin is None`, before `isatty`/`buffer`. No broader catch or fallback.
* `src/core/tests/test_learning_test_bundles.py`: 17 lines. One real subprocess test `test_closed_standard_input_is_one_line_refusal` closes descriptor 0 in the child via `preexec_fn`, runs the real module in an empty temp cwd with the nonexistent-`ZF_DATA` environment, and asserts exit 1, empty stdout, one `Learning report refused: ` stderr line, no `Traceback`, and an empty directory. `sys.stdin` is not mocked.
* Unchanged: README, engine, render, comparators, zero targets, bundles, O16, schema, bounds, labels, config, dependencies, KB index/log/protocol, and all original records.

## Validation (external evidence `phase129-stdin-d1-evidence-1110/`; venv `~/.venvs/issue129-learning-cli-1110`, Python 3.12.3, ruff 0.17.1, mypy 2.4.0, from `src/core`)

* Red on original source (`d1-red-test.txt`, `d1-red-cli.txt`): the new test fails with the `AttributeError` traceback; 21 tests, 1 failure, exit 1.
* Adverse (`d1-green-checks.txt`): first guard edit used a 109-column line; `ruff check` exit 1 (E501) and `ruff format --check` exit 1. Tests passed and mypy passed. Fixed by wrapping the message, with no semantic change.
* Green (`d1-green-checks-rerun.txt`): 21 tests OK; `ruff check` exit 0; `ruff format --check` exit 0 (235 files); `mypy` exit 0 (288 files).
* Actual CLI with descriptor 0 closed (`d1-green-cli.txt`): exit 1, stdout empty, one refusal line.
* Not run by design: full, `--changed`, SQL, browser or live gates; private data; random-signature tests.

## Disposition

Original self-review R1 is untouched and addressed by this one D1 debit. There is no historical balance reset and no automatic D2/D3.
