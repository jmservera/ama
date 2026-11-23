---
title: Research issue 2237 live4
ms.date: 2026-11-23
---

Research disposition: executed (reused earlier evidence plus one new code read). Planning Readiness: Ready.

## Prior coverage

* live, live2, live3 and smoke0055 workers proved reproduce (history), cause (sql write-lock busy, 503 after #2290), fix and regression tests, and live 200 on 0000056. All four criteria are already proven or stated unprovable; see `docs/reference/research/issue-2237-live3-2026-11-23.md`.

## New angle

* `DocControls.retention_due` (src/core/src/zava_forward/core/doc_controls.py) lists due documents for the whole store in one pass. `_trigger` calls `_day`, which uses `strptime` on `retention_trigger` or `stage_since`. One malformed date on one case raises `ValueError`, which the API maps to 500 for the entire listing, hiding every other due record from the Programme Manager.
* A silent skip would hide a retention record, so the fix surfaces the document as a row with status `needs review: trigger date unreadable` and lists the rest.
* Live proof: the existing live probe returned 200 on revision 0000056 (live3 evidence); the new code is not deployed, so no live re-proof of the new behaviour is claimed.
