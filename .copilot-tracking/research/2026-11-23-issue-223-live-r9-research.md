# Research issue-223-live-r9 (2026-11-23)

Refs #223. Disposition: executed (reuses r8 research note and r8 follow-up #1).

## Findings
* r8 stores `review_seconds` in each `review_evidence` (`src/core/src/zava_forward/core/ai_tasks.py`), but `live_report()` (same file) only counts outcomes; nothing reports measured effort. Criterion 3 (total review effort reported) is therefore not measurable from live data.
* `human_review_effectiveness.py` already reports scripted effort; the live path needs its own aggregate.
* Criteria 1, 4, 5 and OQ-017 authority remain owner-only or offline-proven (see r7, r8 notes). Criterion 2 proven live in r7.
* Azure: no resource needed; the new field is not deployed, so a live proof of the aggregate is impossible in this run.

## Planning Readiness
Ready: add per-task `review_effort` to `live_report()` with a regression test in `src/api/tests/test_ai_tasks.py`.
