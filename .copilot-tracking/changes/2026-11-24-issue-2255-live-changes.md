---
title: Issue 2255 live changes
description: Changes record
ms.date: 2026-11-24
---

Started: adding `demo_hazard_clock_seed.py` and `test_demo_hazard_clock_seed.py` under src/core. Tier FULL (src change); no `rpi-checks.py --all` run.

Done: added the seed tool, 3 unit tests and [research note](../../docs/reference/research/issue-2255-live-2026-11-24.md). Local checks: unittest 3 OK, ruff check and format clean; mypy in src/core reports 3 errors in telemetry.py and device_provision.py only (missing optional stubs, unrelated files). Tier FULL (src change); the coordinator owns the full gate.

| Criterion | Status |
| --- | --- |
| Hazards carry awareness time and target | Proven (tests) |
| Clock shows elapsed vs target | Proven (tests) |
| Hazard service stays timing authority | Proven (no service edit) |
| Reversible, skips recorded timing | Proven (tests) |
| Live queue shows clock | Unproven: live SQL write not authorised for the demo; owner step in research note |
