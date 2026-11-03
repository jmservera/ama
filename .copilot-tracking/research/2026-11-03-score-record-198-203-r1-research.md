---
title: Issues 198 and 203 score record research
ms.date: 2026-11-03
---

Research disposition: executed. Planning Readiness: Ready.

## Prior delivery checked

* #198: #292 (registry exclusions), #507, #705 (README and failure reassessment), #851 (dead mvp excludes). #203: #706, #799, #850.
* The pack already held the 47 baseline and carried snapshots but no pre-cut-over versus after-cleanup comparison on current main.

## Evidence (Git history of .github/rubric/scores/latest.json, main 9a9f9dada)

* 47 baseline (2026-10-14); 77 at run 40548249080 (2026-10-27, commit 89c52cba); 77 at run 41647768785 (2026-11-03, commit 949f9346).
* 118 distinct scoring points since 2026-10-27 17:18 are all 77, rubric_version 2. Solution-code criteria identical at both 77 points.
* artifacts.json has no mvp/ or prototype/ glob; 51 tracked files still match a literal mvp/ or prototype/ search.

## Slice

Add the dated score record and acceptance-effect table to the pack. Docs only; focused tier.

## Unmet

* #198: per-PR dual-window records, dedicated registry PR ordering.
* #203: literal search, deployed app and CI green; link criterion not re-evidenced.
