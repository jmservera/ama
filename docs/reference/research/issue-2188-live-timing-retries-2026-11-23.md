---
title: Issue 2188 live, retries visible in the gate timing report (2026-11-23)
description: The before and after timing tool now reports receipt retries so a retried shard cannot pass as a clean speed-up; per-criterion status for the gate speed-up issue
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Read-only analyzer change in `tools/rpi-gate-timing.py`; no `src/` change, no gate semantics change, no Azure access, no `rpi-checks.py --all`. Tier: focused.

## Gap

The gate runner retries a failed test shard once and records it in `receipt["retries"]`. The timing tool (`report` and `compare`) read only `commands`, so an arm that contained a retry reported the same fields as a clean arm while its span was inflated by the failed attempt. The speed comparison could therefore hide the retry evidence the issue asks for.

## Change

* `report` adds `retries` (count) and `retried_groups` (sorted group names); receipts without the key report 0.
* `compare` adds `retries` per arm and the markdown table gains a Retries column. A retry does not make arms NONCOMPARABLE; it is surfaced only. Retry rows carry no timestamps, so no retry duration is claimed.
* Test `test_retried_shards_are_visible_in_report_and_compare` fails on the previous tool (1 failure, 1 error) and passes now; 19 timing tests OK, ruff and mypy clean.

## Per-criterion status

| Criterion | Status | Evidence |
| --- | --- | --- |
| Drop `--no-cache` | Proven (unit level) | earlier notes; 70.5 s to 7.2 s on one image |
| Four concurrent image builds | Proven at scheduler level only | earlier note 2026-11-23 |
| Shard API tests | Proven (unit level) | `shard_partition` tests |
| Retry failed class once, recorded | Proven at shard level (unit); not test-class level | `receipt["retries"]` |
| Receipt records retries, visible when comparing | Proven (unit level), new here | timing test above |
| Verify rejects tampered evidence | Proven (unit level) | `tools.test_rpi_checks` tamper tests |
| Wall time before and after, same tree | Unproven | needs two full gates; `--all` forbidden for this worker; the coordinator can run them and feed `compare` |
