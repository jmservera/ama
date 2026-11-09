<!-- markdownlint-disable-file -->
# Review (authored, once): PR 1295 main-provenance hash repair

* Execution: executed once after implementation. Outcome: conformant for the assigned four-file scope; findings none open. This is an author self-review, not independent review.
* Scope: four metadata files only; no capstone, catalog, receipt, deck, PNG, pitch, runbook, QX, financial or manifest file changed. No new scope needed.
* Evidence: staleness proven first by a failing `--check`; metadata-only delta, masked byte equality and PNG invariance verified; bounded checks pass (see changes record).
* Qualifications: `test-geometry.mjs` and PowerShell capstone checks were not run (missing `excalidraw` CLI and `pwsh`); geometry invariance rests on masked byte equality. Owner-merged PR 1295 hosted checks are pending and are not a coordinator Pass; the follow-up PR's own CI remains the gate. No whole or live acceptance claim; native, AT, runbook and QX items stay with the owner.
* Routed follow-ups: optional `control.json` wording; rerun geometry and capstone Verify where the CLI and `pwsh` exist.
