---
title: Epic 81 audit round 2 after the form-transport fix reached main (Refs #81)
description: Per-criterion proven/unproven table for epic 81 on 2026-11-19; the #1837 source fix is on main and passes locally, the deployed image predates it
ms.date: 2026-11-19
---

Refs #81. Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply (live Azure authorised in resource group `ama`, no production change). No source changed, FOCUSED tier, documentation only. No Azure resource was created, so nothing needed deleting. This note ticks nothing.

## What changed since the 2026-11-18 audit

The [round 1 audit](./issue-81-epic-audit-live-2026-11-18.md) blocked both unticked criteria on #1837 (standalone nomination forms returned 400 on the deployed image). Main at `e3494f476` now contains the #1837 fix from PR 2105 (`e91b6fa81`): the route forms are submitted as JSON with the CSRF header by script, and a native `application/x-www-form-urlencoded` post is refused by design with `Could not read that.` and writes nothing.

## Evidence

* Issue state, read with `gh` on 2026-11-19: #82 to #88 and #131 CLOSED; #130 OPEN (labels `status:partially-delivered`, `status:not-started`); #440 OPEN with two unticked criteria; #1837 still OPEN.
* Local run, from `src/api`: `python3 -m unittest tests.test_nomination_api_routes` gave 8 tests OK, no skips. It covers the browser submission of the three forms, the refusal of native encoding with no write, and the script posting JSON with the CSRF header.
* Azure, read-only: `ca-cutover-test-demo-api` revision `0000033` (created 2026-11-18T22:39Z) still runs image digest `sha256:5368f4e4...c17e5fb`, the same digest the round 1 probe observed, so the fix is not deployed. A redeploy changes the live app, which the owner's "no production changes" boundary excludes, so it was not attempted and the live form retest was not repeated.

## Epic 81 acceptance criteria

| # | Criterion | Proven for the demo? | Evidence and reason |
| --- | --- | --- | --- |
| 1 | Stabilization checkpoint #440 (unticked) | Unproven | #440 is OPEN with unticked criteria for owner-approved triage and PR artifacts; the criterion says merged children alone do not satisfy it. The triage verdict for #81 was Fix, gated by #1837, which is now fixed on main but not deployed or closed |
| 2 | All child features closed or deferred (unticked) | Unproven | #130 is OPEN and has no recorded owner deferral. Its code criteria are ticked; its unticked criterion needs authorised representative evidence, and its deployed forms still show the old behaviour |
| 3 | No controlled progression with unresolved safety evidence (ticked) | Not re-examined | No contradiction found |
| 4 | No work started without valid resident agreement or authorised exception (ticked) | Not re-examined | No contradiction found |

## Result

The first unmet criterion is 1. It has no remaining source gap: the blocking defect is fixed on main and passes locally. What remains needs the owner or a deployment: redeploy the demo API (separately authorised), rerun the round 1 probe expecting the script-driven submission to succeed, close #1837, then #130 or an explicit deferral, then #440.
