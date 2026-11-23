---
title: Resident Showcase Server Header Disclosure and Live Recheck r9 (Issue #462)
description: Live desktop recheck on resident revision 0000028, the Python version disclosure fix with its regression test, and the per-criterion proven/unproven table
ms.date: 2026-11-23
---

## Scope and limits

Session `rpi-462-live`, 2026-11-23, fourth pass, under the 2026-11-18 owner decisions: synthetic demo, desktop only, live Azure in resource group `ama`. No Azure resource was created, changed or deleted and nothing was deployed. This is not a security, identity or accessibility acceptance. It supplements [r8](./resident-showcase-live-r8-2026-11-23.md).

Sign-in values were read at runtime and never printed.

## Live recheck

* Active revision `ca-resident-demo--0000028` (digest prefix `sha256:e6c7e755`), the only active revision at 100% traffic.
* The r8 Playwright script ran unchanged: "ok 36 checks".
* `curl -I` on the HTTPS root still shows no `Strict-Transport-Security` (source fix not redeployed) and `server: ZavaResidentDemo Python/3.12.15`.

## Defect and fix

The Python interpreter version in the `Server` header helps an attacker pick known exploits on a public login surface. `BaseHTTPRequestHandler.version_string()` appends `sys_version`; the resident demo Handler in `src/api/src/zava_forward/api/resident_demo/app.py` now sets `sys_version = ""`. `test_security_headers_and_static_revalidation_policy` asserts on every route that `Server` carries no `Python` or version number; it failed before the change (`ZavaResidentDemo Python/3.12.3`) and passes after. The live header changes only after a redeploy, so no live effect is claimed.

Local evidence: `test_resident_demo_api`, `test_resident_demo_check`, `test_resident_demo_script`, `test_resident_preview_api` (81 tests) pass; `mypy` clean (373 files); `ruff check` and `ruff format --check` pass on both changed files.

## Per-criterion result

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1. RPI artifacts and threat model | Proven for the demo | Dated artifacts; [threat model](./resident-demo-threat-model-2026-11-16.md); October independent review not re-derived |
| 2. #444/#455 and failed rubric resolved | Proven for hosted-history and local-preview clauses | [r7](./resident-showcase-live-r7-2026-11-23.md); preview tests above |
| 3, 4 (ticked) | Re-observed live | 36 Playwright checks on revision 0000028; new header regression test |
| 5 (ticked) | Targeted checks only | No full gate, SQL Server, Docker or hosted CI claimed |
| 6. Pre-spend record | Proven for the demo | [r3](./resident-showcase-live-r3-2026-11-18.md); USD 700 owner decision |
| 7. Browser proof | Proven on the demo, desktop only | Live run above; pre-deploy gates not claimed |
| 8 (ticked) | Partly refreshed | Digest prefix recorded; source commit unconfirmed |

Unproven: live HSTS and live Server header (need redeploy), the full-tier gate (coordinator-run), and owner ticking of 1, 2, 6 and 7. The issue stays open. Refs #462.
