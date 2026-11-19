---
title: Issue 110 plan critique
ms.date: 2026-11-17
---

# Critique (single pass)

Verdict: proceed with amendments.

* Test must fail when a route module imports the consumer or defines an ingestion path; prove with a temporary mutation (red) then revert (green).
* Restrict to HTTP modules (server, workbench, nomination_routes, resident apps); reader imports (sensor_scenarios) must stay allowed.
* Doc entry must not tick C1 or claim live acceptance; keep Refs #110.
* Disposition: all three applied directly; no conflict with confirmed decisions.
