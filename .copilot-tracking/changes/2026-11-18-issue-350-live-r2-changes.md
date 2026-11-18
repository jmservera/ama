# Changes: issue 350 live parity proof, re-run r2 (2026-11-18)

Tier: FOCUSED (documentation and evidence only; no src change; rpi-checks.py --all not run). Basis: no source, workflow, dependency, infrastructure, SQL or security-control file changed; the live run was read-only (GET).
Plan: [plan](../plans/2026-11-18-issue-350-live-r2-plan.md). Note: docs/reference/research/deployed-parity-live-r2-2026-11-18.md.

## Files

* Added the research note, its folder (raw/ 15 files, screens/ 17 PNG, scripts/ 5 Python helpers).
* Updated docs/reference/README.md (index row) and docs/reference/log.md (entry).
* Added the .copilot-tracking research, plan, details, critique, changes, review and state records for this run.

## Per-criterion table (Refs #350, nothing closed)

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | 401 for browser-style anonymous API; page redirect kept | Unproven (fails) | Raw matrix: native curl 401, browser UA plus JSON Accept 302 on every protected path; Easy Auth RedirectToLoginPage; edge change not authorised |
| 2 | Staff prerequisite; all dated rows and 16 assets | Partly proven | Entra sign-in; 14 screens rendered; 16 assets 200 (8 hash-match, 8 older than head); one role; no write rows |
| 3 | Representative baseline | Partly proven | 443 open and 537 completed; visits, orders, finance, funding read; sensors and contractor cases 403; no restore performed |
| 4 | Models, five assistants, workflow-only, durable state, release | Partly proven | Deployment Succeeded; five assistants disabled without operator authority; releases 0; 86 persisted records; no live model output |
| 5 | Licensed map; map/list/chart/CSV/sensor agreement; accessible alternative | Partly proven | 18 OSM tiles 200; 443 markers = 443 list rows = stats = chart = CSV; licence and sensors unproven; CSV mine 133 vs list 16 |
| 6 | Own-user photo | Unproven, deferred | 503; token store disabled; needs consent (#116) |
| 7 | Law store | Unproven, deferred | No ZF_LAW settings; 503 on four law routes; human-owned data change |
| 8 | Ledger, document, digest durability; scheduled jobs | Partly proven | Ledger intact 1,722; continuity healthy; five generated docs download; digests_checked 0; Blob plane blocked; all jobs Manual |
| 9 | Time capture gated explanation; case work independent | Partly proven, defect | /api/time/status 500 ProgrammingError reproduced; case work independent; FULL-tier fix is a follow-up |
| 10 | Per-role results | Partly proven | Programme Manager only; resident app is a showcase |

## Divergences and disclosures

* Run 1 of the same day covered the same criteria; this run adds retained raw output and new observations. Differences from run 1: ledger 1,722 entries (999), eight jobs (nine), 18 tiles (33), staff list shows four staff.
* No Azure resource was created, changed or needs deleting. Session state files in /tmp were deleted.
* The run 1 state file is unchanged; this run's state is in `issue-350-live-r2-state.json`.
* Identifiers (client and tenant ids) in `raw/00-app-config.txt` are replaced with `[id redacted]`.

## Validation

* Documentation: link and diff review, secret and PII scan of raw output. Tests, mypy and ruff: not applicable (no source change).
