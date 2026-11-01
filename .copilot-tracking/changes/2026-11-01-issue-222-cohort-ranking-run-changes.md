# Changes: #222 cohort ranking evaluation run

* Added `src/agents/src/zava_forward/agents/cohort_ranking_eval.py`: 48 paired constructed cases, hand-stated expected-rank manifest, real `ranking.rank` adapter, seeded drop and demote defects, CLI.
* Added `src/agents/tests/test_cohort_ranking_eval.py` (9 tests).
* Updated `src/agents/README.md` with the command and its evidence limits.
* No change to ranking, `cohort_eval` or `mvp/`/`prototype/`.
* Validation: unittest (new plus review_effectiveness, 24 OK), ruff check, ruff format --check, mypy for `src/agents` all pass. Full discovery in `src/agents` fails on a pre-existing module-name clash with `src/core/tests` when both are on the path; not touched. No heavy local gate (CI is the evidence).
* Divergence from plan: an unapproved run also reports `insufficient_sample` because the evaluator fails closed on min_sample when thresholds are unapproved; tests assert that.
* Correction cycle: cases carry sensor, source and appointment fields; accessibility pairs share waiting days (declared pairs lowest days, no-support partners last); `observe` compares relative precedence among retained cases and accepts a `rank_fn`; `run()` and the CLI no longer accept approval (`--approved` removed, `_run(approval=...)` is test-only); new tests for field-sensitive controls (exclude missing, penalise appointments, ignore support), paired days, the combined exclusion and demotion defect, and always-blocked runs. README updated.
* Correction cycle 2 (thread on `observe`): a case is `deprioritised` when any retained case with a later expected unit ranks before it, so earlier demotions cannot mask a later penalty; added a combined-demotions regression. ruff, format, mypy and the full `src/agents` discovery (157 tests) pass.
