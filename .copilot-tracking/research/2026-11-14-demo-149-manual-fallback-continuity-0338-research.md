---
title: Epic 149 manual fallback continuity research
ms.date: 2026-11-14
---

Task: `demo-149-manual-fallback-continuity-0338` (Refs #149). Research disposition: executed. Planning Readiness: Ready.

## Evidence (workspace paths under `src/api/src/zava_forward/api/`)

* Staff case progression: `web/app.js` "Final checks" card lists gate blockers as text and the manual advance button calls `POST /api/cases/{id}/advance`; `server.py` handles action `advance`.
* Evidence checklist: `web/app.js` Documents card renders `Have: kind` or `Need: kind`; `.flag.danger:before` in `web/style.css` adds a warning glyph, so the cue is not colour alone. Funding card states "Still needed: ...".
* Staff AI-unavailable states: `web/assistants.js` sets `data-assistance` to "AI assistance unavailable. Work continues manually." for role, disabled and failure cases and writes owner/next-action text in a `role="status"` paragraph; `web/case-workspace.js` exposes an `aria-live` AI count with "AI review count unavailable."; `server.py` 503 bodies say to continue manually.
* Resident: `resident_demo/web/assistant.js` offers a manual callback form "without chat or AI" and a `role="alert"` load-failure message; `resident_demo/web/demo.js` falls back to a rules-based summary with a plain reason (AI is not enabled / assistant could not be reached).

## Gaps

* No single test ties these manual-path and plain-language cues together for Epic #149. Existing tests cover design tokens, content standard and accessibility separately.

## Boundaries

Static engineering evidence on source only. Not WCAG conformance, assistive-technology acceptance or staff/resident comprehension evidence; those stay with named human testers.
