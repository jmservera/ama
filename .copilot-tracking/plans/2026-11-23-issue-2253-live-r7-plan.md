---
title: Issue 2253 live r7 plan and critique
ms.date: 2026-11-23
---

Refs #2253. Plan: add a `yFor(value)` helper in `sensorChart` (`demo.js`) that clamps the plotted y to 10..150, used for stored points and forecast points; add a node test with an out-of-range stored reading and forecast. Tier: src change in one web file, so web guideline, accessibility and content standard tests run, plus ruff and mypy; `rpi-checks.py --all` is not run (brief).

Critique (executed once): the risk is hiding true values. Mitigation: the table and the description still list every exact value; only the drawn mark is pinned to the plot edge. Verdict: proceed.
