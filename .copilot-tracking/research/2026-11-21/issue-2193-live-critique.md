---
title: Issue 2193 critique (single pass)
ms.date: 2026-11-21
---

Verdict: proceed with the planned approach, findings applied directly.

* Colour alone must not separate the two lines: use solid line with circle markers for temperature and dashed line with square markers for humidity, direct labels at the line ends, and axis titles with units.
* Independent axes can imply false correlation: state in the text that the two axes have different scales and that the chart is advice, not a cause.
* Stale and offline readings must not look current: show a visible "out of date" note above the chart when the model has a stale or offline alert; withheld, no-readings and unavailable states return no readings so no chart renders (unchanged).
* Fewer than 2 numeric points: show text only, no chart.
* Map card: gauges only when numeric values exist; reuse the existing text line as the primary value and mark `meter` with an accessible label. Stale state keeps its badge and text.
* No animation, so reduced motion is satisfied; nothing relies on hover.
* No live redeploy (no production change); live proof is observation of existing deployment only.
