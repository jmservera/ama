---
title: Issue 144 live3 research (hosting proof with retained raw output)
ms.date: 2026-11-18
---

Refs #144. Task `issue-144-live3`, session `rpi-144-live`. Research disposition: `executed` (partly reuse).

## Reused evidence

* `docs/reference/research/issue-144-container-hosting-live-evidence-2026-11-18.md` (runs 1 and 2, merged in main). No `../ama-wt/issue-144*` worktree remains, so main is the reuse source.
* Gap found: the second-run raw output was not retained and the job count (nine versus eight) was unreconciled.

## Plan inputs

* Unticked criteria: (1) images real, versioned, deployed through the pipeline; (3) hardening enforced in the deployed app.
* Plan: re-run read-only `az` queries retaining redacted raw output, reconcile the job count, check `src-deploy.yml` runs, one exec hardening probe, one bounded `/healthz` load test (cost far below USD 700), record per-criterion table.
* Planning readiness: Ready. Owner authorisation 2026-11-18: live Azure in `ama`, no drills, no rotation, no production change.
