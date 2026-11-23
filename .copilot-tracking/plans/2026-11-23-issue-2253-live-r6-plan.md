---
title: Issue 2253 live r6 plan
ms.date: 2026-11-23
---

Refs #2253. Single phase: add the node-executed geometry test to `src/api/tests/test_epic149_child_ux_contracts.py`; no `src` change; focused tier.

Critique (executed once, verdict proceed): the test slices `el` and the sensor helpers out of the demo.js IIFE with a regex, which couples to function order; accepted because the existing tests already read the file by pattern and `shutil.which("node")` skip guards missing node. A mutation (`markerGap = 1`) must fail the test. Compatible findings applied; none conflict with owner decisions.
