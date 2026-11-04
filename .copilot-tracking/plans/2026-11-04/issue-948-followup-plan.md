<!-- markdownlint-disable-file -->
# Plan: issue 948

Details: [../../details/2026-11-04/issue-948-followup-details.md](../../details/2026-11-04/issue-948-followup-details.md)
Research: [../../research/2026-11-04/issue-948-followup-research.md](../../research/2026-11-04/issue-948-followup-research.md)

* [x] Phase 1: count dropped accepted proposals and add to `REGRESSIONS` in `candidate_comparison.py`; docstring and README.
* [x] Phase 2: tests for the drop and for a candidate that accepts more.
* [x] Phase 3: focused tests, ruff, mypy; log entry.

## Critique (single pass)

* Verdict: proceed. Risk: the existing synthetic test with `accepted=i != 3` now also drops one case; it asserts costs only, so it is unaffected. Compatible finding applied: a candidate accepting more than the baseline must not count as a drop (tested).
