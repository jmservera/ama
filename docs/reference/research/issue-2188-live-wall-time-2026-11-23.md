---
title: Issue 2188 live, wall time in the gate receipt (2026-11-23)
description: The gate receipt now records total wall time so the before and after comparison needs no timestamp arithmetic; per-criterion status for the gate speed-up issue
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Tooling change in `tools/rpi-checks.py`, no `src/` change, no Azure access, no `rpi-checks.py --all`. Tier: focused (additive receipt field; verify reads only named keys and its command-identity check compares named row keys, so tamper detection is unchanged).

## Change

* `wall_seconds(rows)` returns seconds from the earliest command `started` to the latest `finished`, retries included, or `None` when no row finished.
* The sealed receipt gains `wall_seconds`. Command rows already carried `started` and `finished`.
* Test `test_wall_seconds_spans_earliest_start_to_latest_finish_with_retries` covers overlap, retries and missing data.

## Evidence

```text
python3 -m unittest tools.test_rpi_checks          Ran 130 tests, OK
python3 -m mypy tools/rpi-checks.py                Success: no issues found
ruff format --isolated --line-length 100 --check   already formatted
```

## Per-criterion table

| Criterion | Status | Reason |
| --- | --- | --- |
| Drop `--no-cache` | Proven (unit level) | 70.5 s to 7.2 s on one image, 2026-11-22 ([note](issue-2188-live-gate-speed-2026-11-22.md)) |
| Four concurrent image builds | Proven at scheduler level only | barrier test; no timed four-image build |
| Shard API tests | Proven (unit level) | shard tests pass |
| Retry a failed class once, recorded | Proven (unit level) | retry tests; no live receipt with a real retry |
| Wall time before and after, same tree | Unproven | receipts now carry `wall_seconds`, but the pair needs two full gates and `--all` is not permitted to this worker |
| Receipt records retries | Proven (unit level) | `receipt["retries"]` validated |
| Verify rejects tampered evidence | Proven (unit level) | tamper tests in the 130 |

Next step for the coordinator: run one full gate on the pre-change tool and one on this head against the same tree, then compare the two `wall_seconds` values.
