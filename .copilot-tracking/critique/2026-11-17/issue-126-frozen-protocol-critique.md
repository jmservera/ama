---
title: Issue 126 plan critique (single pass)
ms.date: 2026-11-17
---

# Critique

Verdict: proceed with one amendment, applied directly.

* Risk: a stricter pause could block existing flows. Mitigation: only breaches of kind `work package` are affected and none can exist in current data without a recorded breach; the full existing governance tests must pass.
* Risk: SQL store parity. `guard_case_event` is in `GovernanceMixin` and reads `self.data`; the SQL store inherits it. The change reads existing procurement data only, so no SQL schema or behaviour change; SQL tests stay opt-in and not run.
* Amendment: read procurement data without `setdefault` so a guard never mutates state.
* Hazard response stays outside the pause (guard is not routed for hazards).
