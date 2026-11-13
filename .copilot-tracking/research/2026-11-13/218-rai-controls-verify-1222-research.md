# Research: Epic #218 RAI controls unit verification (74a93a137a)

* Research disposition: executed (read-only file discovery; required docs read at start: case study original/addendum, knowledge-base index, memory)
* Planning Readiness: Ready
* Boundary: offline unit tests only; no Docker, MSSQL, Chromium, network or cloud. No edits to `src/` or `docs/`.

## Test modules located (base 74a93a137a)

| Package | Modules |
| --- | --- |
| src/core/tests | test_challenges, test_hazard_referral, test_cohort_eval, test_rai_release, test_rai_release_invalidation, test_resident_assistant |
| src/agents/tests | test_cohort_ai_eval, test_cohort_ranking_eval, test_review_effectiveness |
| src/api/tests | test_assistant_release, test_operator_suspension |

Support files: core/tests `release_support.py`, `cohort_eval_fixture.py`; agents `chat_fixture.py`.

## Issue mapping

* #219 reliance/release: rai_release, rai_release_invalidation, assistant_release
* #220 challenge and hazard referral: challenges, hazard_referral
* #221 operator suspension: operator_suspension
* #222 cohort and missing-data evaluation: cohort_eval, cohort_ai_eval, cohort_ranking_eval
* #223 human-review effectiveness: review_effectiveness
* #105/#106 task-registry/suggestions fallback: resident_assistant (core) plus api assistant_release as the nearest unit coverage; no dedicated task-registry module found.

## Boundaries

Passing results are synthetic or scripted proof only. Human OQ-017, OQ-018 and OD-35 exercises are not performed or evidenced by these tests.
