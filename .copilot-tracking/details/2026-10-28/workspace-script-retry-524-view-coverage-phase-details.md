<!-- markdownlint-disable-file -->
---
title: Original view coverage implementation details
description: Direct function coverage instead of late listener instrumentation
ms.date: 2026-10-28
---

Task ID: 524-view-coverage. Scope: full one-task implementation continuation.

<!-- rpi:phase id=P01 -->
## P01: Correct and validate original-function measurement

<!-- rpi:task id=P01-T01 -->
### P01-T01: Replace wrapper with actual function-entry coverage and validate

CDP precise coverage is enabled before initial navigation. Read the actual
role-screens.js top-level count and the named original roleScreensView function's
first function-entry range. Require exactly one original function entry in the
script's coverage when evaluated. Use takePreciseCoverage reset semantics:
first sample proves one top-level evaluation/zero calls before revisit; a second
sample after visible legitimate specialist render proves one function call.
Remove the wrapper and its window counter; keep direct load/error listeners,
real bytes, global readiness and exact pre/post independent route/status.
Keep the explicit cancelled/no-global/terminal budget alternative.
Run focused Chromium under nonblocking lock, retry every60s up to40min if busy;
then package static/unit checks and exact source line threshold.
Record result in the new changes artifact, not by rewriting the preserved Review.

## Completion Evidence

P01/P01-T01 complete: final real Chromium suite passes with original function-entry
zero before revisit and one afterward. A constructed early call, before the load
observer and with its thrown error suppressed, is detected by the new count.
The negative control changes only served app.js inside an owned synthetic test
context; real role-screens.js bytes and checkout sources remain unchanged.
32 focused units, package Ruff/format, mypy92, syntax and <=100-character Python
lines pass. No second RPI Review; final exact-head assessor receives this delta.
