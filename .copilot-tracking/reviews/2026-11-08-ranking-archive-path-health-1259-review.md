---
title: Issue 1259 ranking archive path health review
description: One authored post-implementation review of the LIGHT source preparation
ms.date: 2026-11-08
---

## Execution and outcome

Review execution: Complete (author review, single pass, not independent). Outcome: Residual work. Boundary: the diff of the three source/test paths over frozen parent 26b4ea39 plus the Changes record.

## Assessment against plan and critique

* Phases 2.1 to 2.4 and 3.1 done in order; red recorded before source edits. PC-001 (dangling ancestor), PC-002 (exercise), PC-003 (installed distributions, documented PYTHONPATH for API/agents) and PC-005 (fixed fallback) addressed; PC-004 preserved as residual; PC-006 and PC-007 handled in plan wording and the later gate note.
* Acceptance evidence (LIGHT, local): absent versus unusable distinguished; unusable gives the archive_unreadable shape, unknown window and no write; first-run absent and link-to-folder preserved; path-free; regressions failed before the fix. No criterion is accepted as closed.
* Parent behavior preserved: 90 ranking publication tests (including 1258 regressions) and the full core suite pass; hunks are disjoint from the 1258 helper.

## Findings

* R1 (Low) Stat failure is covered by a mock only; no live permission test.
* R2 (Low) stat then listdir is not atomic; a concurrent change surfaces as OSError, still unreadable-shaped.
* R3 (Medium, pre-existing, deferred) Store status shows overdue True and a path-bearing fallback for unreadable archives (PC-004).
* R4 (Low) 226 core skips not analysed; parent R1 to R6 unchanged.

## Unperformed gates

FULL tier `--all` run and external receipt, receipt verification against the current origin/main, independent exact-head assessment per declared target, hosted checks, human approvals, SQL, browser and scanner tiers. Issue 1259 is not accepted and not closable; use Refs only while stacked.

## FULL resume point

Coordinator admission, fetch main, commit the final head, run `python3 tools/rpi-checks.py --all --base <origin/main sha> --stack <1258 head> --stack <1259 head> --out <new external dir>`, verify the receipt before push, then independent assessment and hosted checks. Any later commit or base move invalidates this LIGHT evidence.
