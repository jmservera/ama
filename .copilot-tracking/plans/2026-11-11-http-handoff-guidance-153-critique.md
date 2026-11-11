---
title: Issue 153 pending-handoff HTTP refusal and error guidance critique
ms.date: 2026-11-11
task_id: 153-http-handoff-1111
---

## Critique (one bounded independent pass, final-candidate plan and details)

Reviewer: independent `rubber-duck` agent, read-only, no tests run. Verdict: revise. All seven findings were compatible with the brief and applied directly; none conflicts with a confirmed decision. The critique is not repeated for this task.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| C1 | Blocking | Fallback "open cases from the case list" can falsely reassure: "mine" filters by `owner_code` (`store.py:358`) so a pending recipient's handoff may be missing. | Applied: refusal copy now says to ask the sender or open a case you already know, because the case list may not show every handoff waiting. Recorded in research risks. |
| C2 | Blocking | An outer `flock` on `/tmp/ama-rpi-heavy.lock` would make `test_unaccepted_handoff_download_ui` skip, since it takes that lock itself. | Applied: details run that class without the outer lock and lock only the non-self-locking new cases; no-skips check kept. |
| C3 | Blocking | Existing `open()` navigates before returning, so a later `page.route` misses the first GET and breaks one-GET/refresh assertions. | Applied: details require a variant installing the route before the first `/app#/` navigation and counting from there. |
| C4 | Non-blocking | `"x"` and `null` already reach the fixed error through the catch, so they cannot prove the change. | Applied: labelled preservation checks; red-before required for 403, HTTP server-text, `{}` and `0`. |
| C5 | Non-blocking | `node --check` path wrong from `src/api`. | Applied: `src/zava_forward/api/web/app.js` from `src/api`. |
| C6 | Non-blocking | Clean-status resume gate conflicts with planning artifacts. | Applied: gate accepts only the expected 2026-11-11 planning artifacts. |
| C7 | Non-blocking | Research wrongly said abort paints the detached card. | Applied: corrected, abort returns silently (preserved). |

Residual, not a finding: copy owner wording differs from #83's "a programme owner"; kept as existing role names and flagged for the independent reviewer. Whether the 403 owner roles truly own role checks is an unverified internal interpretation; no named person or approval process is asserted.
