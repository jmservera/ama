---
title: Changes, issue 2255 run 5
ms.date: 2026-11-23
---

## Changes

* `src/core/tests/test_seed_merge.py`: added `test_stale_seed_cannot_erase_a_seeded_hazard_clock`.
* Research note [issue-2255-live-r5-2026-11-23.md](../../../docs/reference/research/issue-2255-live-r5-2026-11-23.md) with probe script, JSON, page text and screenshot.

Divergence: the test edit was made before this record was persisted, so the `implement-start` witness is out of order. Disclosed, not bypassed.

## Validation

* `PYTHONPATH=src:tests python3 -m unittest tests.test_seed_merge -q` in `src/core`: 22 tests OK.
* `python3 -m mypy` in `src/core`: 3 errors in 2 files, pre-existing (for example unused ignore in `device_provision.py`); none in the changed test.
* `ruff format --isolated --line-length 100 --check` on the test: clean.
* Tier: focused (test only, no src change); hosted CI and independent review remain outstanding.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Elapsed time shown against a target, not "unknown" | Proven on 0000056 | 22 of 22 rows, 0 unknown |
| Some clocks running with a target window | Proven | 5 open with due time, 17 overdue |
| Named accountable owner still shown | Proven | 44 owner text matches |
| Hazard service stays timing authority | Partly proven | page text names the hazard and repairs service; times synthetic |
| Seeded clock survives a re-seed | Proven at unit level (new test); live re-seed unproven, owner-gated | test_seed_merge |
| Generator emits the fields | Unproven, generator outside repository | owner-gated |
| Independent review, hosted CI, full local gate | Unproven here | coordinator runs gates |
