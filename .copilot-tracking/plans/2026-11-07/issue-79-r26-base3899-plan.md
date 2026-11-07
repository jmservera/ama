---
title: Issue 79 r26 plan, base reconciliation to main 38990b19
ms.date: 2026-11-07
---

## Plan

* Phase 1: rebase the run-owned local root onto `38990b19`, plain rebase (merge commits of main are ancestors of main and are dropped). No amend or reset. Stop on any conflict that is not provably both-sides-preservable.
* Phase 2: prove tree equality of topic-owned paths against `bb7e044c`, incoming paths equal main, log prefix preserved, original RPI blobs equal.
* Phase 3: light checks (own-source venv, external caches): ranking core and API wiring, exception register and data operator screens, Config, ruff, mypy.
* Phase 4: changes, author Review, state, one log entry; commit; verify clean.

## Critique (author, one pass, not independent)

* Rebase drops merge commits; accepted because required by the owner and the content is in main. Tree parity proof is the safeguard.
* New production logic is out of scope; any needed change is a blocker.
* Conflict risk is low (disjoint paths, clean merge-tree). Disposition: proceed.
* Records written after the rebase go in a new commit, so the original r25 commits are replayed unchanged.
