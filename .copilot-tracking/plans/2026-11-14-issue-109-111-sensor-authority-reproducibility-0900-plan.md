---
title: Sensor non-authority and reproducibility plan (Refs #109, #111)
date: 2026-11-14
---

## Phases

* [x] 1. Canonicalise row order in `derive_signal` (`_by_observation`) so output depends only on the reading set.
* [x] 2. Core test: identical output bytes across row permutations, batch sizes, replays, redelivery and fresh processes with differing hash seeds; versions and review-task trigger stable; out-of-order arrival fails closed.
* [x] 3. API test: ingest extreme, adverse, normal and declined readings for five homes carrying a live hazard, service clocks, hazard hold and legal hold; assert full state, hazards, clocks, holds and ranking snapshots unchanged; approved synthetic draft adds only the draft record and one audit row.
* [x] 4. Run focused tests, `ruff`, `mypy`; commit locally without push.

## Critique

Executed once on the final candidate (self-review): compatible findings applied (draft test excludes the data version and meta row, which any permitted draft write advances, and asserts the ranking and hazards are unchanged). No conflicts with confirmed decisions.
