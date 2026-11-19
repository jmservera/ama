# Issue 198 live research (2026-11-19)

* Scope: first unmet criterion of #198 that code can fix; demo, desktop only.
* Prior evidence: `docs/reference/research/issue-198-rubric-live-r2-2026-11-18.md` (criteria 3 and 4 unproven, 10 failing tests in `test_safe_output_runtime.py`).
* Criteria 3 and 4 are historical process records; code cannot satisfy them. The one tightly coupled code defect is the test fixture still using the retired `mvp/` sample path and assuming both triggers.
* Live Azure, browser and sign-in proof do not bear on any criterion; none gathered.
* Research disposition: reused (prior note) plus fresh re-run below. Planning Readiness: Ready.
