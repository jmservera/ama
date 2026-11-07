---
title: Issue 82 quality gate details (2026-11-05)
ms.date: 2026-11-05
---

## Phase 1: tests

* `src/core/tests/test_gates.py`: `QualityGateTests` with unit cases for `gates.quality_gate` (pass, fail listing gaps, unknown for None, future rule unknown, rule record fields) and store cases using the JSON fixture from `test_quality_procurement`: blank, missing and unreadable `items` refuse `accept_quality` and `hand_over_quality` with `GateError`, leave the record state unchanged, and a complete record still accepts and hands over.

## Phase 2: implementation

* `gates.py`: `QUALITY_RULE` (gate `quality`, effective 2026-11-05, version 1, unreviewed exercise reviewer) and `quality_gate(gaps, owner, on)`; `None` is unknown.
* `quality.py`: `evidence_gaps(rec)` returns gaps or `None` when unreadable; `quality_evidence_gate(rec)`; `handover_blockers` reuses it so the view and the transition agree.
* `store.py`: `require_quality_evidence(rec)` raises `GateError` with reason, owner and next action; called from `accept_quality` after the state check and from `hand_over_quality` for accepted records.

## Phase 3: validation

* `cd src/core && python3 -m unittest test_gates test_quality_procurement` (from `tests`), `ruff check`, `ruff format --check`, mypy per `src/core` config.

## Phase 4: gate

* Inspect the lock holder; use `--lock-timeout 0`; no waiting or duplicate gate.
