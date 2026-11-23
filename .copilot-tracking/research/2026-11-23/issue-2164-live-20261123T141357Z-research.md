---
title: Research for issue 2164 live r8
ms.date: 2026-11-23
---

Disposition: executed. Planning Readiness: Ready.

* Prior notes: recheck 2026-11-22 and staff-verified audit 2026-11-23 on this HEAD (50dc2acf88); fix 6a03928ccb (assistants) and the sensor draft gate fix are ancestors.
* Open unproven items: the deployed image carries the fix (earlier note said the digest is untraceable), and live behaviour.
* Plan: read-only `az containerapp exec` grep of the deployed package for fix markers; rerun unit tests; no roster edit on live data.
