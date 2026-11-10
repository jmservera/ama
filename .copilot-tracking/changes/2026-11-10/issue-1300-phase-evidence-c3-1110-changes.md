# C3 changes (written before source edits, 2026-11-10)
Planned: tools/rpi_phase_witness.py `log_contained` derived-destination containment; tools/test_rpi_phase_witness.py ancestor-layout regression and disjoint success. No other source file. Counter C3/5, two left. Baseline HEAD e463233505f576e32ca172e73f9ea5b610e0636c.

## Implemented (2026-11-10T04:35Z)
* Helper: `log_contained` now refuses when the resolved issue directory, log or lock equals or lies inside the resolved repo ("derived witness log destination must be outside the candidate worktree"). Refusal precedes any open.
* Tests: ancestor-layout refusal (exit 2, no events files in the candidate) and a disjoint-sibling success; 33 tests pass. Verified the ancestor test FAILS on the C2 helper (git show HEAD helper restored temporarily) and the sibling test passes on both.
* Ruff check and format were run on the two files only. Step 5 not edited. Earlier directory-wide formatter deviations (C1: 12 files, C2: 16 files) remain adverse history.
