<!-- markdownlint-disable-file -->

# Research: issue-99 S2 signal read

* Disposition: reused. PR 885 delivered `exposure_limits.py` (record_limits, assess); evidence in `.copilot-tracking/research/2026-11-03/issue-99-exposure-limits-research.md`.
* Gap: the pause signal is wired to no live path and limits have no intake route.
* Blocked: persisting limits in the store needs SQL/store design (SQL tier, coordinator gate); Board OD-12/15 figures do not exist in the repository and must not be invented.
* Smallest unblocked slice: read-only finance method that loads limits from a person-supplied file and compares recorded commitments. Planning Readiness: Ready.
