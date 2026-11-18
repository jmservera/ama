<!-- markdownlint-disable-file -->
# Changes Record: Child Hardening Pass 15 for Issue #216 (`RV-038`..`RV-040`)

* Task ID: `216-citation-eval-2142-c15`
* Plan Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c15-plan.md`
* Phase Details Path: `.copilot-tracking/details/2026-11-14/216-citation-eval-2142-c15-phase-details.md`
* Critique Path: `.copilot-tracking/plans/2026-11-14/216-citation-eval-2142-c15-plan-critique.md`
* Status: `Completed`

## Summary

Implemented `P01-T01` and `P01-T02` in `src/core` to close `RV-038`..`RV-040` (noun-vs-verb `"meeting"` refusal precision via `_OBLIGATION_PREPOSITION_GUARD_RE` / `_OBLIGATION_OBJECT_RE`, mandatory consistent `observed_at` / `recorded_at` paired observation timestamps in `[agreed_on, eval_day]`, and pre-observation `agreed_on` bound for `accepted_definition` and `verified_agreement`).

## Task Progress

* [x] `P01-T01`: Harden `regulatory_eval_gates.py` (`RV-038`..`RV-040`).
* [x] `P01-T02`: Populate `"observed_at"` in `_valid_observations`, add `test_c15_meeting_noun_precision_mandatory_observation_dates_and_accepted_def_ordering`, update `src/core/README.md`, and pass all `src/core` checks.

## Divergences and Amendments

* None.

## Validation Evidence

* `python3 -m mypy`: `Success: no issues found in 318 source files`
* `python3 -m ruff check .` and `python3 -m ruff format --check .`: `All checks passed!`, `265 files already formatted`
* `python3 -m unittest discover -s tests -p 'test_*216*.py' -v`: `18` tests `OK`
* `PYTHONPATH=src:tests python3 -m unittest tests/test_regulatory_chat.py tests/test_gates.py tests/test_live_doc_links.py`: `58` tests `OK`
