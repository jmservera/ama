---
title: SQL wave checkpoint 440 current-main preparation research
ms.date: 2026-11-09
task_id: 440-sql-wave-checkpoint-1109-mainprep
---

## Disposition

Research executed 2026-11-09 (read-only Git and `gh`). Planning Readiness: Ready. This is source-preserving current-main preparation, not a new corrective cycle; C1 and C2 stay spent (3 of 5 remain, not used here).

## Evidence

* Candidate head `f2e07999386399694abe91562555b35c0105ab9b`, tree `3e88be1b392adfdd470f771bd07337b7cc89896a`, branch `docs/demo-sql-checkpoint-440-1109`, clean tracked tree.
* Merge base with `origin/main` is `ef28d4da42d83b111d48f14df9b70e3c4932a477`.
* Fetched `origin/main` is `3a9767d5cf728c5e3be76813ce0bfdac4c06841e`, tree `d5b8e46c4931e729bdd04ef5701be5da32e46c2e`. It adds `1464b4d85` (#1312, `tools/rpi-checks.py`, `tools/test_rpi_checks.py`, tracking) and `3a9767d5c` (PR 1240, controlled lifecycle integration, #81).
* PR 1240: state MERGED 2026-11-09T16:50:00Z, merge commit `3a9767d5c`, head `ccc7358dad0628a660b76b1feb4e3a3556cc952c`, status rollup 19 of 19 SUCCESS (read with `gh pr view`).
* Main versus the observed SQL-wave source `8d6f029ca`: 225 changed paths overall; `src/` has 12 files (`src/core` only: appointments, complaints_route, gates, procurement, quality, resident_decisions, store, tests, README); outside `src/` and tracking, only `.github/rubric/scores/latest.json`, the pack and `tools/rpi-checks.py` plus its test.
* `git merge-tree --write-tree --name-only HEAD origin/main` exits 0 with no conflicted path. Main changed the pack in two insertion hunks (an issue 81 alignment section before the 2026-11-08 checkpoint and a 141-line block before the demo stabilization section). Main changed neither `docs/reference/README.md` nor `docs/reference/log.md` after `ef28d4da4`. Own pack changes are one appended section at the end, so a clean ordinary merge is expected and both intents persist.
* External independent Readiness `b1111a45` (under `independent-440-context-complete/`) completed the earlier partial assessment at `f2e07999`: `approve_with_comments`, 0 Critical, 0 High, 0 Medium, 1 Low (15 versus 17 record scope). The Low is a durable follow-up (#1314, D5 after C1 and C2). It is not fixed here and the original authored outcomes are not rewritten.

## Boundaries

* The SQL-wave record observed source `8d6f029ca`. Main `3a9767d5c` includes lifecycle source that the SQL-wave record did not retest or accept. Whole #81, #440 stay open.
* The existing pack section holds a resume condition that depends on "the #1240 lifecycle integration evidence". A dated preparation note in that section can truthfully record the changed identity, the trigger and the hold. It cannot record a completed lifecycle checkpoint, which needs new integrated evidence.
* Independent #189, #954 and #159 source work is not blocked. No legal, resident or production approval is implied.

## Planning Readiness

Ready: bounded ordinary merge plus one append-only dated note, index and log entry, with byte-equal source proof against `origin/main`.
