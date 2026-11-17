---
title: Issue 1258 plan
ms.date: 2026-11-17
---

## Plan

* [x] Phase 1: Research and measure (see research file).
* [ ] Phase 2: Record the evidence outcome in changes; make no source edit because the unfixed behavior is already guarded.
* [ ] Phase 3: Run focused checks (targeted unit tests, ruff format, mypy for `src/core`) and review.

Details: no source or test change. Rationale: mutation of the parent-sync loop fails 12 existing tests, and the 57-test module passes. Adding another test would duplicate `AncestorDurabilityTests`.

## Critique (single pass, self-run)

* Verdict: compatible. Adding a duplicate test or touching PC3-1 would exceed the issue's smallest-fix scope and the brief; rejected.
* Risk: committing only tracking artifacts delivers no source change. Accepted and reported honestly; issue stays `Refs`.
