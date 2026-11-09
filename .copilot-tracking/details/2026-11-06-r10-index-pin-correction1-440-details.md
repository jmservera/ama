---
title: R10 index pin correction 1 details
description: Phase details for the R10 index pin correction
ms.date: 2026-11-06
---

## Context

Plan: `.copilot-tracking/plans/2026-11-06-r10-index-pin-correction1-440-plan.md`. Evidence: the research record for this task and root assessment `440-r10-root-assessment-r68.md`. Worktree `/home/azureuser/source/ama-wt/docs-parent123-history-checkpoint`, branch `docs/queue-dispatch-protocol-checkpoint-440`.

## P1 Correct the index pin and append the log entry

* P1-T1 In `docs/reference/README.md`, in the Seventeenth paragraph, change the parenthesized `1e199209` to `1e192099`. Completion: one-line diff; the old token is absent.
* P1-T2 Append one entry at the end of `docs/reference/log.md`, matching the existing entry style (dated heading, short `*` list). It states: the index paragraph printed `1e199209`; the correct short pin is `1e192099` for commit `1e19209985d93e053dd449e873e792f214dd110c`; the pack, log and tracking records were already correct; no checkpoint, renumbering, source, requirement, ADR or design change; the earlier 38 records are unchanged. Completion: additions only and the earlier log prefix byte-identical.

## P2 Run focused checks

* P2-T1 Checks, each with its command and exit captured:
  * fresh `git fetch` of main and the governance branch, pins compared with `bb3a3b03...` and `11982835...`;
  * `git grep` for the old short pin (expected only in the new log entry) and the new short pin, a check of every other hash token in the README paragraph, and a prefix comparison of `1e192099` with the exact commit id;
  * README anchor target for the Seventeenth section exists as a pack heading slug;
  * `git diff --check`, numstat, and pack diff empty;
  * log prefix equals the start head's log bytes;
  * byte comparison of all 38 existing batch tracking records against the start head, plus the earlier R10 records;
  * frontmatter, ASCII and JSON parse for the new records that exist at that time;
  * ignored-inclusive `git status`.
  Completion: all pass, or failures recorded without relabelling.

## P3 Record Changes, Review, state and commit

* P3-T1 Changes record lists the files, the actual check results and exits with limits, and the additive qualification: the old R10 state JSON shows `session_status` running and the old plan keeps its original markers as artifact metadata from that cycle; neither is rewritten and neither describes a live process.
* P3-T2 Review per the rpi-review skill, in a later completed turn, author-only, not independent.
* P3-T3 State JSON written once after Review; commit with a freshly resolved noreply identity; verify clean.

## Test and validation ownership

No tests added or removed; documentation and Git checks only.
