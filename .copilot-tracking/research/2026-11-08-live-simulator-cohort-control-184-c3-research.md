---
title: "Research: #184 correction 3 (format red file)"
ms.date: 2026-11-08
---

Disposition: executed, read-only, before any C3 edit. Start `78d25a13`, tree
`9b0f9141`; origin/main last fetched `6354b13f`.

## Finding

The independent functional review of `78d25a13` passed with one Low evidence
gap (restricted-grant main-entrypoint and rejected-DQ path not tested). That
gap stays open here.

## Factual correction

The C2 changes artifact and the review wrongly named `sensor_consumer.py` as the
file failing `ruff format --check`. The preserved `/tmp/c2-fmt.out` shows the
red file is `src/api/checks/sensor_sql_check.py` (lines 109-110); the other five
of the six files are formatted. C2 records are not rewritten; this artifact
corrects them additively. Source CI runs Ruff format, so the red file matters.

## Environment

Ruff 0.17.3. An ignored `src/core/.ruff_cache/` exists from a coordinator probe;
it is preserved, so the tree cannot be claimed ignored-inclusive clean.
The two failed C2 SQL attempts' raw output was overwritten by the rerun; only
their descriptions survive.

Planning Readiness: Ready.
