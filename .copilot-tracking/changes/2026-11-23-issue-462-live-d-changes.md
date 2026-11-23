# Changes: issue 462 fourth pass (2026-11-23)

Source (tier FULL; coordinator runs the gate, `rpi-checks.py --all` not run here):

* `src/api/src/zava_forward/api/resident_demo/app.py`: Handler `sys_version = ""`, so `Server` no longer discloses the Python version.
* `src/api/tests/test_resident_demo_api.py`: header test asserts no `Python` or version in `Server` on every route (failed before: `ZavaResidentDemo Python/3.12.3`).

Docs: `docs/reference/research/resident-showcase-live-r9-2026-11-23.md`, README row, log entry. Note: the implement-start witness recorded source already dirty because the test edit ran in the same step as the witness call.

Validation: 81 resident demo/preview tests OK; mypy clean (373 files); ruff check and format clean. Live: 36 Playwright checks ok on revision 0000028; HSTS and Server fix not observable live (not redeployed). No Azure change.

## Per-criterion table

| Criterion | Status | Evidence |
|-----------|--------|----------|
| 1. RPI artifacts and threat model | Proven (demo); owner ticks | Dated artifacts; threat model 2026-11-16 |
| 2. #444/#455, failed rubric | Proven (demo) hosted-history and preview clauses | r7; preview tests |
| 3, 4 (ticked) | Re-observed live | 36 checks, revision 0000028; new header test |
| 5 (ticked) | Targeted only; full gate, SQL Server, Docker, hosted CI unproven | tests above |
| 6. Pre-spend record | Proven (demo) | r3; USD 700 decision |
| 7. Browser proof | Proven (demo, desktop) | live run |
| 8 (ticked) | Partly refreshed | digest prefix; source commit unconfirmed |

Unproven: live HSTS and Server header (redeploy), full gate, owner ticking.
