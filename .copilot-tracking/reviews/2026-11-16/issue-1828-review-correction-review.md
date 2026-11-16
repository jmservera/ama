---
title: Issue 1828 review correction cycle 1 review
description: Single post-implementation review of the viewport premise attribution
ms.date: 2026-11-16
ms.topic: reference
---

Review executed once, after implementation. Boundary: `git diff` of `src/api/checks/map_fullscreen_browser_check.py`, `src/api/tests/test_map_viewport_premise.py` and the correction artifacts against head 3a7c655603eeae861c476eca1268a0188efde9bc. Own review; independent exact-head review remains required.

Outcome: conformant for the FOCUSED scope with one qualification (browser validation deferred).

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| R1 | Medium | The real-Chromium equality of bbox-projected width and `#leaflet.clientWidth` and the full map/axe terminal pass are unobserved because the heavy lock is held by #1297. | Routed: named handoff in the changes artifact; unmet, not claimed |
| R2 | Low | The fake `expect_request` is unused by the new logic; it exists so the test drives the previous implementation. | Accepted, retained |
| R3 | Low | If the container does not narrow with the viewport the check fails rather than skipping. | Intended; no weakening |

Checked: the `no map requests` assertion text and strength are unchanged; no application, permission, consent, SQL, deployment, workflow or gate file changed (FOCUSED holds); the viewport and listener are restored in `finally`; the three false-positive cases fail on the old logic (3 of 4) and pass on the fix; focused regressions pass; ruff clean. Web-design-guidelines (fetched 2026-11-16) and redesign skills: no markup, style or behaviour changed, so no file:line findings apply.
