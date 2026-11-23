---
title: Issue 2304 critique
ms.date: 2026-11-23
---

# Critique (one pass, final-candidate plan)

Verdict: accept with direct dispositions.

* Risk: memoising reads across one forecast uses a single point in time. Disposition: acceptable, the forecast is a read-only estimate and already ran on an autocommit connection.
* Risk: bulk reads of `assistant_tasks` ids and adoptable task bodies grow with history, not with open cases. Disposition: applied; bodies are fetched only for slot tasks in chunks of 500, adoptable history only when a case lacks a slot.
* Risk: shortcuts for homes without sensor data could change Quality results. Disposition: applied; shortcut only when a distinct-home read shows the home absent, and a failing probe repeats its failure so the old `unavailable` result is kept. Output equality was verified.
* Risk: a timeout returned as 400 or generic 503. Disposition: applied; dedicated `ForecastTimeout` mapped to 503 with `state: unavailable` and `Retry-After`.
* No finding conflicts with a confirmed owner decision; no user decision required.
