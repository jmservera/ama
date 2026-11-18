# Issue 122 live details

Phase 2: POST `/api/continuity/change` with kind `configuration`, subject `zf-demo-continuity-probe-122`, versions `v0` to `v1`, evaluation `pass`, `synthetic` true, from inside the signed-in page. Then GET `/api/continuity`, POST `/api/continuity/change-reverse` with the CHG id, GET again. Row is metadata only; no runtime behaviour reads this subject. The register is append-only, so two synthetic rows (applied then reversed) persist; this is disclosed. No suspension or restart is invoked (drills excluded).
Phase 3: screenshot of the workbench continuity page if one exists; otherwise API JSON only.
