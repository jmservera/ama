---
title: Issue 80 capacity browser check time-status expectation, plan
description: One-edit plan to align the #/time status assertion in capacity_browser_check.py with the current timecapture copy
ms.date: 2026-11-10
---

Research: [research](../../research/2026-11-10/issue-80-capacity-c1-1110-research.md). Details: [details](../../details/2026-11-10/issue-80-capacity-c1-1110-details.md). Critique: [critique](issue-80-capacity-c1-1110-critique.md).

## Objective

Make the whole `capacity_browser_check --axe` reach both real export downloads and the empty-capacity zero-anchor assertion by correcting only the stale `#/time` expectation. No other source file changes.

## Phases

* [ ] Phase 1: edit the `elif href == "#/time"` branch (one file, `src/api/checks/capacity_browser_check.py`).
* [ ] Phase 2: focused validation at the exact head: Ruff check and format check of the checker, `node --check` of unchanged `ops.js`, API list-export tests (11), related static tests (60), then ONE whole `capacity_browser_check --axe` run under the canonical non-blocking heavy lock.
* [ ] Phase 3: reconcile records, native Review, commit, handoff.

## Decisions

* Assert the flag-driven copy the UI actually renders, never the server `reason` (the UI deliberately hides it).
* Three branches: enabled gives the exact "Time capture is on."; `flag_on` false gives the exact switched-off sentence with owner and next action (the maintained fixture state); any other blocked state asserts the shape (reason sentence, then `Owner:` and `Next action:`).
* Do not weaken to "some message exists", do not suppress the failure, do not touch the disabled/manual path (checklist and route table unchanged).
* One browser run. A failure is reported as found; no silent retry, no assertion weakening, no unrelated repair.
* Out of scope: R2, R3, R4 (accepted limitations), R5 (source-only attribution), fixtures, roles, `ops.js`, progress report.

## Validation tier

Focused demo. Rationale: a test-only expectation change with no product behaviour change. No full gate. Hosted CI and independent exact-head review remain required before publication.
