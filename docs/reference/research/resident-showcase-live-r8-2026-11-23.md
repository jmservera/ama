---
title: Resident Showcase HSTS Header and Live Recheck r8 (Issue #462)
description: Live desktop recheck on resident revision 0000027, the HSTS defect fix with its tests, and the per-criterion proven/unproven table
ms.date: 2026-11-23
---

## Scope and limits

Session `rpi-462-live`, 2026-11-23, third pass, under the 2026-11-18 owner decisions: synthetic demo, desktop only, live Azure in resource group `ama`. Billing reconciliation, Legal/DPO approval and person-run assistive-technology testing are out of scope. No Azure resource was created, changed or deleted and nothing was deployed. This is not a security, identity or accessibility acceptance. It supplements [r6](./resident-showcase-live-r6-2026-11-23.md) and [r7](./resident-showcase-live-r7-2026-11-23.md).

Sign-in values were read at runtime from the owner file and never printed. Evidence is in `.copilot-tracking/evidence/2026-11-23-resident-showcase-live-c/` (`live_r8.py`, `live-checks.json`, five desktop screenshots).

## Live recheck

* Active resident revision `ca-resident-demo--0000027`, image digest prefix `sha256:e6c7e755`; r6 recorded revision 0000026, so the app was redeployed between passes.
* The r6 Playwright script ran unchanged: "ok 36 checks" (CSRF and origin denial, generic 401 for wrong password and unknown email, forged cookie 401, case override attempts ignored, own-email-only projection, HttpOnly Secure SameSite=Strict cookie, write routes 405, sign-out then 401, rate limit 429).
* `curl -I` on the HTTPS root: 200, `no-store`, CSP, `x-frame-options: DENY`, no `Strict-Transport-Security`.

## Defect and fix

The resident app did not send `Strict-Transport-Security`. The issue asks for HTTPS-only session handling; cookies were already `__Host-`, Secure and HttpOnly, and http redirects to https, but a first plain-http visit stayed downgradable without the header. `HEADERS` in `src/api/src/zava_forward/api/resident_demo/app.py` now includes `max-age=31536000`, the value the employee API uses, with no `includeSubDomains` or `preload`.

Local evidence: `test_resident_demo_api` (50 tests, one new assertion on the header), `test_resident_demo_check`, `test_resident_demo_script` and `test_resident_preview_api` (31 tests) pass; `mypy` reports no issues in 372 files; `ruff check` and `ruff format --check` pass on both changed files. The passing preview tests are the evidence for the clause that existing local previews remain available. The live app is not redeployed, so the header is not observed live.

## Per-criterion result

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1. RPI artifacts and threat model | Proven for the demo | Dated artifacts for all passes; [threat model](./resident-demo-threat-model-2026-11-16.md); the October independent review is not re-derived |
| 2. #444/#455 and failed rubric resolved | Proven for hosted-history clauses and the local-preview clause | [r7](./resident-showcase-live-r7-2026-11-23.md) run history; preview tests above |
| 3, 4 (ticked) | Re-observed live | 36 Playwright checks on revision 0000027 |
| 5 (ticked) | Targeted checks re-run | Resident demo and preview tests, mypy, ruff; no full gate or SQL Server, Docker or hosted CI claimed here |
| 6. Pre-spend record | Proven for the demo | [r3](./resident-showcase-live-r3-2026-11-18.md); the USD 700 owner decision supersedes the October cap; no fresh cost figure |
| 7. Deployed showcase in a browser | Proven on the demo, desktop only | Live run above; "gates passed before deploy" not claimed |
| 8 (ticked) | Partly refreshed | Revision and digest prefix recorded; source commit behind the digest unconfirmed (private registry) |

Unproven: live HSTS (needs a redeploy outside this pass), the full-tier gate for the source change (coordinator-run), and ticking of criteria 1, 2, 6 and 7, which belongs to the owner. The issue stays open. Refs #462.
