# Issue 222 research: cohort and missing-data evaluation record

Status: opened. Research disposition: executed (measurement below).
Base: origin/main eb51af5c. Issue comments show criteria 1-5 ticked after #636/#697/#821/#939/#975/#956; criterion 6 needs owner/DPO approval (out of scope).

## Plan of measurement

* Run the existing cohort evaluator tests (core and agents), sequentially.
* Compare evaluator outputs with each criterion and look for a documentation or regression gap.

## Measurements (2026-11-17, synthetic only, run sequentially from src/core and src/agents with PYTHONPATH on worktree sources)

* `src/core`: `python3 -m unittest test_cohort_eval` with `PYTHONPATH=src:tests`: Ran 25, OK.
* `src/agents`: `python3 -m unittest test_cohort_ranking_eval test_cohort_ai_eval test_cohort_manifest_draft` with `PYTHONPATH=../core/src:src:../core/tests:tests`: Ran 36, OK.
* `python3 -m zava_forward.agents.cohort_ranking_eval`: 48 cases, status blocked, activation false, every cohort `sufficient=False` (n=42 and n=6), blockers `insufficient_sample` and `unapproved_thresholds`; seeded [] detected [].
* Same with `--defects`: seeded history-2-b, history-3-b, sensor-1-b, sensor-4-b; all four detected; per-cohort errors reported per cohort (for example support_need/none 4, appointment_history/missed 2), not averaged; `unjustified_exclusion` blockers.
* Counts reconcile (n + missing per dimension equals 48); source_completeness/partial review_burden 1.0 with interval [0.0, 0.3903] on error rate.

## Findings

* No defect reproduced; criteria 1 to 5 behave as ticked. Criterion 6 needs owner/DPO approval; not provable here.
* Gap (documentation): `docs/reference/research/evaluation/cohort-evaluation-review-pack.md` banner and AC table still say "NOT EXECUTED" and "All six acceptance criteria remain unmet" and "Not met" for AC1 to AC5, while its own 2026-11-04 status record and the code show executable evidence. The structural draft test pins the draft manifest's AC statuses, not the page.

## Planning Readiness

Ready. Smallest change: add a dated measured-run section and an engineering-status pointer to the page, preserving the original draft statuses, update the log. No code change, no new test (no defect to regress; the behaviour is covered by the 61 existing tests).
