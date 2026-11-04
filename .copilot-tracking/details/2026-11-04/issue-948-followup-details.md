<!-- markdownlint-disable-file -->
# Details: issue 948

* Phase 1: `src/agents/src/zava_forward/agents/candidate_comparison.py` (`REGRESSIONS`, `_measure` baseline value 0, `compare_candidates` computes the count against baseline-accepted case ids); `src/agents/README.md` paragraph.
* Phase 2: `src/agents/tests/test_candidate_comparison.py::test_dropping_an_accepted_proposal_is_a_regression` and `::test_candidate_accepting_more_than_baseline_is_not_a_drop`.
* Phase 3: `python3 -m unittest tests.test_candidate_comparison` from `src/agents`, ruff check, mypy with `--cache-dir=/tmp/mypy-946`.
