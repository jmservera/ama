---
title: Changes - UI and cache required observations follow-up (Refs #440)
description: Implementation record, actual commands and divergences
ms.date: 2026-11-05
ms.topic: reference
---

## Changes

* `docs/architecture/cutover-evidence-pack.md`: appended a dated "Required-observations continuation: actual results" subsection after the seventh checkpoint; the earlier text is unchanged.
* `docs/reference/README.md`: two sentences added to the existing seventh-checkpoint index paragraph.
* `docs/reference/log.md`: one entry appended after the seventh-checkpoint entry.
* No source, test, tool, workflow, coordinator, ADR or requirement change.

## Actual results

| Step | Result |
| --- | --- |
| Admission probe (lock, processes, main, child) | lock free, main `bb3a3b03` stable |
| New `/tmp/m440b` worktree | exit 0, clean |
| Attempt 1 (`/tmp/o440b`) | check 1 exit 0; check 2 exit 1 from a harness mistake (pre-created output directory, pre-imported module); not a product result; preserved |
| Attempt 2 (`/tmp/o440c`), one lock hold 15:03:36Z to 15:05:14Z | check 1 exit 0 (1 test OK); check 2 exit 0 (407 PASS, 0 FAIL, 87 axe scans, 0 page errors, 320x800 bottom 1592.40625 against 1600) |
| `/tmp/m440b` status after | 0 tracked, untracked or ignored entries; no bytecode |

## Divergences

* Attempt 1 was repeated, so the lock was acquired twice in total (attempt 1 held it for 3 seconds); each attempt held it across both checks.
* The runner script and its copy were written under `/tmp`, outside the repository, and one `sed` copy was used for the second script; no repository file was written that way.
* No independent critique agent; no full receipt claimed.
