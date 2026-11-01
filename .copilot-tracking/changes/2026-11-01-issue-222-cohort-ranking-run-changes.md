# Changes: #222 cohort ranking evaluation run

* Added `src/agents/src/zava_forward/agents/cohort_ranking_eval.py`: 48 paired constructed cases, hand-stated expected-rank manifest, real `ranking.rank` adapter, seeded drop and demote defects, CLI.
* Added `src/agents/tests/test_cohort_ranking_eval.py` (9 tests).
* Updated `src/agents/README.md` with the command and its evidence limits.
* No change to ranking, `cohort_eval` or `mvp/`/`prototype/`.
* Validation: unittest (new plus review_effectiveness, 24 OK), ruff check, ruff format --check, mypy for `src/agents` all pass. Full discovery in `src/agents` fails on a pre-existing module-name clash with `src/core/tests` when both are on the path; not touched. No heavy local gate (CI is the evidence).
* Divergence from plan: an unapproved run also reports `insufficient_sample` because the evaluator fails closed on min_sample when thresholds are unapproved; tests assert that.
