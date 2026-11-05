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

## Base movement and interrupted attempts

* Attempt 1 (head 47caaedb9, base 180dcf3e2, out /tmp/rpi-1214-c2): preflight and namespace passed; project-api was interrupted by signal 15 after 1049 tests reported ok (runner exit 1, failed receipt retained, no test failure). The cause was the launching shell being torn down, not the code; no result is claimed.
* Attempt 2 (same head, out /tmp/rpi-1214-c2b): the runner blocked immediately with "Reviewed base differs from current origin/main" because origin/main moved to 7e0fe64892a1b9a65cc2f580faf2369f3bf009ef (chore(rubric) score file only). No checks ran.
* Rebased again onto 7e0fe6489 (tracking records still name 180dcf3e2 as the #1217 merge base; the gate base is 7e0fe6489). Attempt 3 runs on the rebased frozen head with out /tmp/rpi-1214-c2c.
