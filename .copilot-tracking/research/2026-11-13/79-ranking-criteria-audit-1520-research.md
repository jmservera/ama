---
title: Issue 79 ranking criteria audit research
ms.date: 2026-11-13
---

## Scope

Audit the four acceptance criteria of issue #79 against `origin/main` at `0893bbcdb`.

Research disposition: executed. Planning Readiness: Ready.

## Issue #79 criteria (read with `gh issue view 79`, 2026-11-13)

* [x] Same data and policy version give the same order
* [x] Policy file changes are versioned and hash-verified
* [ ] Named policy owner signs the first rule order
* [ ] Ranking snapshot publication is scheduled and retained (ADR 0002 deviation)

## Findings

* The brief names `test_ranking` and `programme.js`; neither path exists. Ranking tests are `src/api/tests/test_ranking_policy.py`, `test_ranking_scale.py`, `test_ranking_publication_wiring.py` and `src/core/tests/test_ranking_publication*.py`, `test_ranking_archive_blob.py`. The programme screen is `src/api/tests/test_programme_screen.py` against `role-screens.js`.
* `policies/ranking-v1.json` still has `owner: "to be named"` and status "Draft rule order, not yet signed off". `test_shipped_policy_loads_with_owner_and_status_unchanged` pins that state.
* `ranking.signoff_problems` reads a recorded sign-off but states it cannot prove a human approved. Signing is a human step.
* `ranking_publication.SCHEDULE` states runner "deployment scheduler (not yet configured)", owner "to be named", retention "not set". Publish and verify are tested; scheduling and the retention period are not delivered.
* Cohort balancing named in the issue title has no code in `ranking.py` and no acceptance criterion.

## Test run (venv `/tmp/venv-79-1520`, `--system-site-packages`, removed before commit)

* `src/api`: `PYTHONPATH=../core/tests:../agents/tests:tests python -m unittest tests.test_ranking_policy tests.test_ranking_scale tests.test_ranking_publication_wiring tests.test_programme_screen`: 83 tests OK.
* `src/core`: `PYTHONPATH=tests python -m unittest tests.test_ranking_publication tests.test_ranking_publication_runner tests.test_ranking_archive_blob`: 136 tests OK.
