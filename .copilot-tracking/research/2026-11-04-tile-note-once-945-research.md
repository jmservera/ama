---
title: Research for #945 tileNote rewritten on every tileerror
ms.date: 2026-11-04
---

* Task: fix/issue-945-followup, Refs #945 (review note from #917).
* Research disposition: executed (code read only).
* Prior delivery check: merged PR #917 added the announcement; no merged PR addresses #945.
* Finding: in `src/api/src/zava_forward/api/web/app.js` the `tileerror` handler assigned `tileNote.textContent` on every event. The note is a `role="status"` `aria-live="polite"` region, so each assignment can be re-announced. Leaflet GridLayer fires `loading` at the start of a load cycle and `load` when all visible tiles have loaded or failed.
* Planning Readiness: Ready.
