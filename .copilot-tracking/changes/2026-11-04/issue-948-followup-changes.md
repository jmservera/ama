<!-- markdownlint-disable-file -->
# Changes: issue 948

* `src/agents/src/zava_forward/agents/candidate_comparison.py`: new `dropped_accepted_proposals` count, included in `REGRESSIONS`.
* `src/agents/tests/test_candidate_comparison.py`: two tests (the drop test fails before the fix).
* `src/agents/README.md`: grader paragraph updated.
* `docs/reference/log.md`: entry.

## Validation

* Run: `tests.test_candidate_comparison` (14 OK; both new tests error before the fix), ruff check and format on touched files, mypy on touched files.
* Not run: gate, benchmarks, full suites, CI. `PYTHONPATH` pointed at this worktree. No `pyproject.toml` edited.
