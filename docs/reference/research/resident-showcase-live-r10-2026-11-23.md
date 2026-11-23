---
title: Resident Showcase Content-Length Guard and Live Recheck r10 (Issue #462)
description: Live desktop recheck on resident revision 0000028, the non-ASCII Content-Length defect fix with its regression test, and the per-criterion proven/unproven table
ms.date: 2026-11-23
---

## Scope and limits

Session `rpi-462-live`, 2026-11-23, fifth pass, under the 2026-11-18 owner decisions: synthetic demo, desktop only, live Azure in resource group `ama`. No Azure resource was created, changed or deleted and nothing was deployed. This is not a security, identity or accessibility acceptance. It supplements [r9](./resident-showcase-live-r9-2026-11-23.md).

Sign-in values were read at runtime from the owner file and never printed. Evidence is in `.copilot-tracking/evidence/2026-11-23-resident-showcase-live-e/` (`live_r10.py`, `live-checks.json`, five desktop screenshots).

## Live recheck

* Active revision `ca-resident-demo--0000028`, digest prefix `sha256:e6c7e755`, the only active revision at 100% traffic; unchanged since r9.
* The r8 Playwright script ran unchanged: "ok 36 checks" (CSRF and origin denial, generic 401 for wrong password and unknown email, forged cookie 401, case override attempts ignored, own-email-only projection, HttpOnly Secure SameSite=Strict cookie, write routes 405, sign-out then 401, rate limit 429).
* `curl -I` still shows no `Strict-Transport-Security` and `server: ZavaResidentDemo Python/3.12.15`: main carries both fixes but is not redeployed.

## Defect and fix

`_body()` in `src/api/src/zava_forward/api/resident_demo/app.py` checked `Content-Length` with `str.isdigit()` before `int()`. `isdigit()` accepts non-ASCII digits such as superscript two, `int()` then raises `ValueError` outside the `try`, and the handler thread dies: a local probe with valid CSRF cookie and header received an empty reply instead of the generic 401. The guard now also requires `isascii()`. The new test `test_non_ascii_digit_content_length_is_a_generic_denial` failed before the change (error) and passes after, and a normal login still succeeds. The live app runs the old code, so no live effect is claimed.

Local evidence: `test_resident_demo_api`, `test_resident_demo_check`, `test_resident_demo_script`, `test_resident_preview_api` (82 tests) pass; `mypy` clean (375 files); `ruff check` and `ruff format --check` pass on both changed files. Tier: FULL because `src/` changed; the coordinator runs the gate and `rpi-checks.py --all` was not run.

## Per-criterion result

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1. RPI artifacts and threat model | Proven for the demo | Dated artifacts for every pass; [threat model](./resident-demo-threat-model-2026-11-16.md); the October independent review is not re-derived |
| 2. #444/#455 and failed rubric resolved | Proven for the hosted-history and local-preview clauses | [r7](./resident-showcase-live-r7-2026-11-23.md); preview tests above |
| 3, 4 (ticked) | Re-observed live | 36 Playwright checks on revision 0000028; new malformed-header test |
| 5 (ticked) | Targeted checks only | No full gate, SQL Server, Docker or hosted CI claimed |
| 6. Pre-spend record | Proven for the demo | [r3](./resident-showcase-live-r3-2026-11-18.md); USD 700 owner decision; no fresh cost figure |
| 7. Deployed showcase in a browser | Proven on the demo, desktop only | Live run above; pre-deploy gates not claimed |
| 8 (ticked) | Partly refreshed | Digest prefix recorded; source commit behind the digest unconfirmed (private registry) |

Unproven: live HSTS, live `Server` header and live Content-Length behaviour (all need a redeploy), the full-tier gate (coordinator-run), and owner ticking of 1, 2, 6 and 7. The issue stays open. Refs #462.
