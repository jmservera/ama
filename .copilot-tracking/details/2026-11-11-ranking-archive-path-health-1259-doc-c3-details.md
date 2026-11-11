---
title: Issue 1259 documentary C3 details
description: Phase details for the four-finding documentary qualification
ms.date: 2026-11-11
---

## Phase 1 Prospective records

* Research, plan and details committed before the qualification files exist. Success: one commit containing exactly these three paths.

## Phase 2 Canonical qualification

* New changes record states: old-source red reaches only the verify tuple assertion in four subtests, plus the separate schedule-exit, Store and path-leak failures; current green covers all operations. Today's counts: 8 run, 7 failure records across four methods; six regression-class methods and two pre-existing. Historical 6/7 and 90 post-fix stay historical.
* `run.sh` is a scratch-dependent log collector, not a standalone, reusable or gate runner; `native=0 tee=0` is not a test exit; `manifest.txt` was planned and not produced; setup is external to the repository, in the native log.
* Process disclosure of collateral writes, restoration, broad globs, `git add -A`, cache, whitespace normalization, plan checkbox edit and missing manifest; AST substitution was not the only deviation.

## Phase 3 Pointers and review

* Append pointer sections to three original records. New review and state; originals untouched otherwise.

## Phase 4 Hygiene and handoff

* Diff, link and ASCII checks only. Explicit-path `git add`. Handoff outside the repository lists exact head, tree, base, original and new RPI paths and the note count.
