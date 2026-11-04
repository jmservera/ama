---
title: Plan for #945
ms.date: 2026-11-04
---

* Slice: single slice, whole issue.
* Phase 1: write the note only when its text differs; count errors per load cycle (reset on `loading`); on `load` clear the note only if the cycle had no tile errors. The message text, including the list-alternative pointer, and the list box are unchanged.
* Phase 2: string-level regression test (the front end has no JS unit runner) plus a throwaway node simulation of the logic.
* Validation tier: focused (front-end text change; no security, infrastructure, SQL or deployment). Gate not run. Web guidance: the change keeps the existing polite status region, native semantics and manual list path; no visual change, so no design-skill restyle was applied.
* Critique: executed once, inline. Compatible finding applied: clearing on `load` alone would clear immediately after a failed cycle because Leaflet fires `load` after errored tiles too, hence the per-cycle error count.
* Details: [details](../details/2026-11-04-tile-note-once-945-details.md).
