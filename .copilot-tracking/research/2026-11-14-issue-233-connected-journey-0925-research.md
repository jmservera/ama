# Research: #233 connected journey across role screens (2026-11-14)

Disposition: executed. Planning Readiness: Ready. Parent: PR #1639 (`1d761f6e`), `Depends on #1639`, `Refs #233`.

* Parent added tension callouts and a "one home" sentence on the stage map, which exists only in `programme-queue` (Programme Manager, Support Officer, Coordinator).
* Audit: other role screens (technical, quality, resident choice, packages, job pack, finance, safety, hazard, data operator, service issues) show the selected home but give no route to the other stages, so Housing Officer (Resident Liaison), Quality Inspector, Contractor, Finance and Building Safety walkers could not follow one home across screens. `screenHref` already preserves the exact `case` id; no screen links another case.
* Probe: `roleScreensView()` renders for all role/screen pairs on a bare case except `asset-board` and `programme-queue`, which need richer fixtures.
* Constraints: `browser_check.py` not touched (manifest SHA untouched); Fluent `screenPanel`, h2 hierarchy, text status, no colour/icon meaning; web-design-guidelines fetched 2026-11-14 (navigation as `<a>`, URL carries state, specific link text).
