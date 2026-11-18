---
title: Issue 187 anomaly injector research
ms.date: 2026-11-14
---

## Scope

Issue #187: named anomaly scenarios (damp/mould, underheating, overheating, sensor faults, post-works verification) with a ground-truth manifest that stays out of live operational views.

## Findings

* `sensor_faults.py` injects ten fault packets; truth is kept separately (`truth-*.jsonl`, `truth/manifest.json`) by `sensor_backfill.write`.
* `sensor_scenarios.py` has damp, sensor_fault, missing_data and four retrofit cases with a `Truth` dataclass written under `truth/`; it has no underheating or overheating pattern.
* `sensor_consumer.py` drops `injected_fault` from retained rows; `resident_showcase.py` still accepts `injected_fault` in its input shape (pre-existing, out of scope).
* Gap: no single named-scenario injector and no guard that refuses label keys in live rows.

## Planning readiness

Ready. Disposition: executed (code inspection only; no external sources).
