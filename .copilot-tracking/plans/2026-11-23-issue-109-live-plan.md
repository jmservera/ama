---
title: Issue 109 live plan
ms.date: 2026-11-23
---

Refs #109. Single phase: reject non-finite or non-numeric channel values in the handover series.

## Critique (executed once, accepted)

* Compatible: reuse the existing `INVALID_HANDOVER_OBSERVATION` reason; no new code path or schema.
* Risk: stricter validation could reject valid rows; mitigated by running the existing ingest and handover tests.
* Scope stays code-only with a focused tier; no authority flags or ranking touched.

## Plan

1. Edit `_indoor_series` to require finite `Decimal` values for `CHANNELS`.
2. Add a regression test for NaN, Infinity and text values.
3. Run focused tests, mypy, ruff.
