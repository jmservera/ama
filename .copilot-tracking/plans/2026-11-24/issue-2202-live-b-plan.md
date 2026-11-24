---
title: Issue 2202 live plan b, 2026-11-24
ms.date: 2026-11-24
---

## Plan

* [x] Phase 1: record live evidence and the per-criterion table (docs/reference/research/issue-2202-live-r2-2026-11-24.md).
* [ ] Phase 2: in `HubReceiver.run`, treat an event after the deadline in a bounded window as the normal end of the window (stop requests still raise RUN_STOPPED); add one regression test in `src/api/tests/test_iot_stream.py`.
* [ ] Phase 3: run `tests.test_iot_stream`, mypy and ruff in `src/api`; update README index and log; write changes and review; commit locally.

Tier: FULL applies (src change); the coordinator runs the gate. `rpi-checks.py --all` is not run here. No push or PR.
