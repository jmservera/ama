---
title: Issue 2253 live r4 plan
ms.date: 2026-11-23
---

Plan: in `sensorChart` (demo.js) (1) when the forced latest marker is within `markerGap` of the previous marker, remove the previous marker so no pair touches; (2) when the space left of the divider is under 90 user units (label width at 12 px), start-anchor "Latest stored" to the right of the divider so it cannot reach the 45 tick. Add a regression test in `src/api/tests/test_epic149_child_ux_contracts.py`. Tier FULL for src, but `rpi-checks.py --all` is not run (coordinator runs gates); targeted tests, mypy and Playwright proof are run.

Critique (executed once): the change is small and compatible with the legend and the singleton case (one circle remains). Verdict: proceed. Static assertions mirror the existing test style; a Playwright proof of the touching pair with a local fixture is added if feasible.
