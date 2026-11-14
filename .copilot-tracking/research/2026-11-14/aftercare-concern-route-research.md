---
title: Aftercare concern route research (#133)
date: 2026-11-14
---

Task: aftercare-concern-route-133. Disposition: executed. Planning Readiness: Ready.

Findings:

* `src/core/.../aftercare.py` already records routes `digital` and `staff_recorded`, channels `phone`, `in_person`, `paper`, `assisted_visit`, and `raised_by` household or representative with a required representative basis.
* `aftercare_intake.py` surfaces the channels, the paper manual route and a durable receipt; the API delegates to `AftercareService`.
* The deterministic guard `neutral_text` covered only some templates. `manual_route`, `owner_note`, channel labels, notes and unknowns were not checked, and no strip helper existed.

Gap: guard coverage of all fixed templates and a strip option.
