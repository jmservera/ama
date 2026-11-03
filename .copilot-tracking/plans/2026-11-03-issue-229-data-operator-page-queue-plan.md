# Plan: issue #229 slice 4, page-level conflict and return queue

Research: [research](../research/2026-11-03-issue-229-data-operator-page-queue-research.md). Details: [details](../details/2026-11-03-issue-229-data-operator-page-queue-details.md).

* [x] Phase 1: add page-level summary to the data-operator screen.
* [x] Phase 2: unit test summary (both values, returns, unavailable homes, no controls, no forward moves).
* [x] Phase 3: README note; unit tests, ruff, mypy, existing browser check with pinned axe.

Critique: one self-critique pass. Reuse the established `summarise` pattern; do not add unavailable-home hiding; keep copy plain and caveated. Stacked slices still open: assistive-technology and human acceptance (#155, #151), Fluent adoption (#150), browser-check coverage of the page-level view.
