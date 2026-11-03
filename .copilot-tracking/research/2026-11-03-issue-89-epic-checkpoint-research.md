<!-- markdownlint-disable-file -->
# Research: issue 89 epic checkpoint (2026-11-03)

Research disposition: executed. Planning Readiness: Ready.

## Question

What has merged for epic #89 (provider capacity, work orders, quality acceptance), what remains unmet, and what is the smallest coherent slice?

## Evidence

* Pin: origin/main b855aec86b47939ed4cafd38bc17b9318f2284c7; BRD and PRD 0.21.0 blobs unchanged since the third #440 checkpoint.
* Children: #90 and #91 closed (delivered in `core/procurement.py`, `core/quality.py`); #92 open (PR #389 merged, both criteria unmet per the 2026-10-31 closure audit; PR #900 open); #132 (PR #873 open) and #133 (PR #869 open) not started on main.
* Epic criteria: (1) scoped stabilization checkpoint per #440 is unmet, no epic-scoped checkpoint exists; (2) children closed or deferred is unmet (three open).
* Contradiction: PRD FR-016/FR-017 (provider package, quality) differ from BRD FR-016/FR-017 (progression stops, handoff contents). The epic cites both.
* In-flight PRs for the children belong to other lanes; not duplicated.

## Slice decision

Smallest coherent slice: an epic-scoped, documentation-only checkpoint (partial progress on criterion 1). Building #92, #132 or #133 would duplicate open PRs. Focused tier; no security, infrastructure, SQL or deployment change, so no gate is needed or run here.
