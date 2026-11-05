---
title: Issue 1214 correction cycle 2 changes
description: Append-only changes record for the rebase and final-head execution plan
ms.date: 2026-11-05
ms.topic: reference
---

## Changes

* Rebased fix/mobile-summary-gate-1214 onto origin/main 180dcf3e28d976169186ad38790471bec4b13934 (merge of #1217). Earlier commits were re-created; no content conflicts.
* Source change unchanged: one rule in src/api/src/zava_forward/api/web/style.css (`.top nav{row-gap:.125rem}` inside the existing max-width 600px block). Remaining margin against the unchanged 1600 bound is 7.59375px (from 1592.40625).
* Plan and details of the original cycle are unchanged; the earlier statement "P02 open for the runner only" remains true until P03 completes externally.

## Validation

Recorded outside the repository for the final head (a committed result would change the head): the maintained runner output directory, receipt hash and verification exit are given in the handoff. Historical evidence at 3ee3b53e5 (browser exit 0, 407 assertions, 72 unit tests OK) is preserved and is not claimed for this head. The correction 1 reproducibility invocation (read-only shared venv, candidate-first assertions) was permitted at that time and is not rewritten; this cycle uses the runner's owned environments instead.
