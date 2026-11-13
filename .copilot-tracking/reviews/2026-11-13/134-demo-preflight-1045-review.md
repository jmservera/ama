---
title: Issue 134 demo preflight review
ms.date: 2026-11-13
---

Independent code-review executed once on the changes log and inspection script. Outcome: Findings, minor, none blocking; no `src/` or `docs/` edits, no secrets.

Dispositions:

* Sensor claim overstated: corrected to "no sensor-like fields found; not verified".
* Absence claims rest on sampled keys: wording now says sampled.
* Stand-alone inference from `building_id` and `scheme_id` None: accepted, not the runbook generator rule.
* Unit counts come from the local status and log files in `/tmp/pf1045` (deleted after commit prep); counts were read from the unittest output in this session.

No findings remain open. Routed follow-up: verify sensors, simulator cohort, AI scope and links in a deployed-store preflight under separate authority.
