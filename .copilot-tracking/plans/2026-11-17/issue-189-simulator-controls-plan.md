# Issue 189 plan: one accountable-text rule for run controls

Refs #189. Tier FOCUSED. Research: `.copilot-tracking/research/2026-11-17/issue-189-simulator-controls-research.md`.

## Phases

* [x] Phase 1: `live_control.parse` uses `sensor_stream.accountable_text` for owner and approval_reference; strip as before.
* [x] Phase 2: regression test in `src/api/tests/test_live_control.py` for `nobody`, `<owner>`, over-long values (parse and CLI start writes nothing).
* [x] Phase 3: run targeted tests, mypy for `src/api`, ruff format check.

## Critique (single pass, self)

Risk: existing tests use short values (`o`, `r`); `accountable_text` accepts them. `PLACEHOLDERS` list has `tbc`, which accountable_text lacks, so keep PLACEHOLDERS check in addition. Admin `_clean` unchanged (still stricter via identity.display). Verdict: proceed.
