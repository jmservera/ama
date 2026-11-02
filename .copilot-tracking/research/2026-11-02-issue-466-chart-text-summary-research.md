---
title: "Research: issue 466 chart text summaries (r5), 2026-11-02"
ms.date: 2026-11-02
---

* Research disposition: reused (r4 research, issue 466 comments, merged #471 to #474, #586, #603) plus a read of the demo UI code. Planning Readiness: Ready.
* Only criterion 1 (owner confirms scope and priority) is unmet and is a human approval; not substituted here.
* Gap found: `resident_demo/web/demo.js` charts have a short generic `desc` and a table behind a disclosure, but no plain-language text alternative stating what the chart shows (lowest, highest, latest versus first, missing readings). WCAG 1.1.1 and the plain-language standard favour a visible summary.
* CO2 is not in the synthetic sensor stock (temperature and humidity only), so adding it would change the dataset; out of scope. The same synthetic 60,000-home stock is used unchanged.
