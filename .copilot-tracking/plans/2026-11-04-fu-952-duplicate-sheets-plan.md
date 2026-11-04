# Plan: issue 952 duplicate sheets

Research: [research](../research/2026-11-04/fu-952-duplicate-sheets-research.md). Details: [details](../details/2026-11-04-fu-952-duplicate-sheets-details.md).

Scope: one slice, no stacking needed (the issue is small).

* [x] Phase 1: fingerprint sheets in `pool_human_sessions`, exclude repeats from totals, report `duplicate_sheets` and `duplicate_note`.
* [x] Phase 2: regression test for duplicates.
* [x] Phase 3: focused tests, ruff, mypy; log entry.

Critique (single pass, self-run): the fix must not change the worksheet contract and must keep the first occurrence; both satisfied. No conflicts with confirmed decisions.
