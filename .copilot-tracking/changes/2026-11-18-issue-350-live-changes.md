# Changes: issue 350 live parity proof (2026-11-18)

Tier: FOCUSED (documentation and evidence only; no src change; rpi-checks.py --all not run).
Plan: [plan](../plans/2026-11-18-issue-350-live-plan.md).

## Files

* Added docs/reference/research/deployed-parity-live-2026-11-18.md, screens/ (5 PNG), scripts/ (3 Python helpers).
* Updated docs/reference/README.md (index row) and docs/reference/log.md (entry).

## Per-criterion table (Refs #350, none closed)

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | 401 for browser-style anonymous API; page redirect kept | Unproven (fails) | Browser UA + Accept json gets 302; edge change not authorised |
| 2 | Staff prerequisite; all rows and 16 assets | Partly proven | Entra sign-in and 9 screens rendered; one role, other rows not run |
| 3 | Representative baseline | Partly proven | 443 open + 537 completed; sensors, documents, contractor not checked |
| 4 | Models, five assistants, workflow-only, durable state | Partly proven | Deployment Succeeded; all five release-denied (OQ-017, human); no live AI output |
| 5 | Licensed map provider; agreement; accessible alternative | Partly proven | OSM tiles 33 x 200, list alternative, 443 agree; licence and sensors unproven; CSV mine 133 vs 16 unexplained |
| 6 | Own-user photo | Deferred | 503, needs consent (#116) |
| 7 | Law store | Deferred | 503; human-owned, production data change |
| 8 | Ledger/document/digest durability, scheduled jobs | Partly proven | Ledger intact 999; digests 0; all jobs Manual |
| 9 | Time capture gated explanation | Partly proven, defect | /api/time/status 500 ProgrammingError; case work independent |
| 10 | Per-role results | Partly proven | Programme Manager only |

## Divergences and disclosures

* A GET of /api/briefing may have written a workflow-only briefing task record on the demo; no other write.
* No Azure resource was created, so nothing to delete. Session state files in /tmp were deleted.
* Concurrent jobs (ledger-verify, drill) belong to other workers and were not touched.

## Validation

* Documentation: link and diff review. Tests/mypy/ruff: not applicable (no source change).
