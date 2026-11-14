---
title: RAI harm threshold incident phase details
date: 2026-11-14
---

## Phase 1

Tests: seeded critical harm to HTTP suspension, owner, affected task, blocked execute and manual-route text, SQL reopen; approved breach needs an owner; constructed thresholds are offline-only and cannot open a live incident; unapproved live thresholds are blocked; unauthorised role and repeat suspension are refused.

## Phase 2

Validation from `src/api` with `PYTHONPATH=tests:../core/tests:../agents/tests` because dotted `tests.` imports need `tests/` on the path (the unmodified command fails for existing tests too).
