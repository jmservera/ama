# Research: synthetic needs to phase-gate traceability (Refs #165)

Disposition: executed. Planning Readiness: Ready.

* Inventory `needs-inventory.json` v1.3.0 (13 rows SN-01..SN-13, 11 partial, 2 covered, 0 missing), status draft-awaiting-owner-review.
* Manifest `scenario-manifest.json` binds inventory version, reviewed rows and `owner_review: pending`.
* README section "Synthetic data needs inventory and phase gate" is the readiness summary: row count, version, gated epics (#109 SN-09, #157 SN-08), owner boundary.
* Existing tests cover binding and mutations; no test ties README summary to rows or checks emitted-record provenance end to end.
* Generators: `scale_fixture.write` (is_synthetic on records), `live_readings.Generator` (source_type SYNTHETIC), `privacy` scanners.
* Real data: only documented OpenStreetMap anchors (provenance register); public pack scans clean.
