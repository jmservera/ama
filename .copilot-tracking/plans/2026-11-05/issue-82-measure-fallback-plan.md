---
title: Issue 82 non-string measure fallback plan (2026-11-05, correction 3)
ms.date: 2026-11-05
---

* [ ] Phase 1: shared `Flows` regressions first, capture RED (details: `../../details/2026-11-05/issue-82-measure-fallback-details.md`).
* [ ] Phase 2: one explicit guard in `evidence_gaps`.
* [ ] Phase 3: JSON and SQLite targeted tests, configured ruff check and format (`--no-cache`), mypy with external cache; capture real exits.
* [ ] Phase 4: commit with gh-derived noreply identity; full gate with SQL Server pending admission.

## Critique (single pass, self-run)

* Guard only when the checklist name is not recognised and the measure is neither None nor a string: return None (Unknown). Absent or empty measure keeps the legacy General fallback. Applied.
* No coercion to string, no General success shape for corrupt values, no broad catch. Applied.
* Corruption persisted and reopened so `JsonFlows`, `SqlFlows` and `MssqlProcurement` inherit the test. Applied.
* Acceptance must raise a controlled `GateError` with the record unchanged; no replacement is claimed for a non-string measure. Applied.
* Controls: known checklist with non-string measure still passes (measure unused), null measure with an unrecognised checklist keeps legacy fallback. Applied.
