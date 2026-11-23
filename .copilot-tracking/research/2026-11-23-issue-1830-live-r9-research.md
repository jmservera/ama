---
title: Issue 1830 live r9 research (2026-11-23)
ms.date: 2026-11-23
---

Research disposition: executed. Planning Readiness: Ready.

Scope: first unticked criterion that code can satisfy. Criteria 2 and 3 are proven for the demo by r6 to r8; criterion 4 needs a pull request (forbidden). Criterion 1 is partly proven and its unproven part, queue wait, is a tooling matter: `tools/rpi-gate-timing.py report --log` reads only the first log line.

Finding (read of `tools/rpi-gate-timing.py` lines 192-206 and the producer at `tools/rpi-checks.py` line 3765): when `--log` is given but the first line is not the `Lock queued ...; acquired ...;` line, the report silently omits `queue_wait_seconds`, so a reader cannot tell "no wait" from "not measured". A malformed timestamp raises an uncaught `ValueError` traceback, and an acquired time before the queued time yields a negative wait. The existing test only covers the valid line.

Live Azure is out of scope by the issue boundary ("no live Azure").
