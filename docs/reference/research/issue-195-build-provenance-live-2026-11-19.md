---
title: Issue 195 build provenance and per-criterion proof 2026-11-19
description: Per-criterion proven and unproven table for the three unticked issue 195 criteria, with a source change that lets a deployed image state its source commit
ms.date: 2026-11-19
---

Scope: synthetic demo, desktop only. Refs #195. Live reads used the existing Azure login; no resource was created, changed or deleted, and no credentials were printed.

## Per-criterion table

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | #440 stabilization checkpoint reconciled before epic closure | Unproven | Needs the owner's disposition of #440 findings and its own two unticked criteria; not provable from this host |
| 2 | All child issues closed or explicitly deferred by the owner | Unproven | Closure or deferral is an owner decision; not a code or live-evidence question |
| 3 | Deployed container image rebuilt from `src/` and verified running | Partly proven | Running and src-only content proven earlier ([r2](./cutover-gate-live-r2-2026-11-18.md)); live read 2026-11-19: `ca-cutover-test-demo-api` revision `0000033`, running status `Running`, digest `sha256:5368f4e4...e5fb`. Source commit provenance was missing; this change adds it. A rebuild was not run: registry public access is disabled and ACR tasks fail from this host |

## Change delivered for criterion 3

* `src/api` Dockerfile accepts `ZF_BUILD_COMMIT` and exposes it as an environment variable.
* `src-deploy.yml` passes `$GITHUB_SHA` to the build.
* The server logs `build: commit=<sha>` at start, from `zava_forward.api.build_info`, which accepts only 7 to 40 hex characters and otherwise reports `unknown`.
* Tests: `src/api/tests/test_build_info.py` (4 cases, including log-line forgery). The deployed digest above predates the change, so it reports no commit until rebuilt by a permitted pipeline.

## Residual

Criterion 3 closes when a rebuilt image's container log shows the expected commit. Tier FULL applies (src, Dockerfile and deployment workflow changed); the full gate was not run here.
