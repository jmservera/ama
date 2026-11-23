# Changes: issue 462 third pass (2026-11-23)

Source change (full tier; the coordinator runs the gate, `rpi-checks.py --all` not run here):

* `src/api/src/zava_forward/api/resident_demo/app.py`: `Strict-Transport-Security: max-age=31536000` added to `HEADERS`.
* `src/api/tests/test_resident_demo_api.py`: assertion on that header.

Docs: `docs/reference/research/resident-showcase-live-r8-2026-11-23.md` (new), `docs/reference/README.md` row, `docs/reference/log.md` entry. Evidence: `.copilot-tracking/evidence/2026-11-23-resident-showcase-live-c/`.

Validation: `test_resident_demo_api` 50 OK; `test_resident_demo_check`, `test_resident_demo_script`, `test_resident_preview_api` 31 OK; `mypy` clean (372 files); `ruff check` and `ruff format --check` clean. Live: 36 Playwright checks ok on revision 0000027; HSTS absent live (not redeployed).

## Per-criterion table

| Criterion | Status | Evidence |
|-----------|--------|----------|
| 1. RPI artifacts and threat model | Proven (demo) | Dated artifacts; threat model 2026-11-16; October independent review not re-derived |
| 2. #444/#455 and failed rubric resolved | Proven (demo): hosted-history clauses via r7 `gh` history; local-preview clause via preview tests | r7, r8 |
| 3, 4 (ticked) | Re-observed live | 36 Playwright checks, revision 0000027 |
| 5 (ticked) | Targeted checks only | Local SQL Server, Docker, hosted CI and full gate not re-run; unproven in this pass |
| 6. Pre-spend record | Proven (demo) | r3; USD 700 decision; no fresh cost figure |
| 7. Browser proof | Proven (demo, desktop) | Live run; pre-deploy gates not claimed |
| 8 (ticked) | Partly refreshed | Digest prefix `sha256:e6c7e755`; source commit unconfirmed |

Unproven: live HSTS (needs redeploy), full-tier gate for this change, owner ticking of criteria 1, 2, 6 and 7.
