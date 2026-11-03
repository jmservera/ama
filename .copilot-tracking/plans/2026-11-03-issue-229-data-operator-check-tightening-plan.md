# Plan: issue #229 slice 3, tighten the data operator browser check

Research: [research](../research/2026-11-03-issue-229-data-operator-check-tightening-research.md). Details: [details](../details/2026-11-03-issue-229-data-operator-check-tightening-details.md).

* [x] Phase 1: scope phrase assertions to the returns and conflict table regions and assert the reopened reason.
* [x] Phase 2: add `ZF_AXE_REQUIRED=1` fail-on-skip and document RESULT as authoritative in `src/api/README.md`.
* [x] Phase 3: run the check with the pinned axe file, ruff check and mypy; record changes and review.

Critique: one pass, self-critique only (small test-only change); no conflicts with decisions. Stacked slices still open: assistive-technology and human acceptance (#155, #151), Fluent component adoption (#150).
