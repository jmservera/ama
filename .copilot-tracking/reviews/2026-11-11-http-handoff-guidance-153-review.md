---
title: Issue 153 pending-handoff HTTP refusal and error guidance review
ms.date: 2026-11-11
task_id: 153-http-handoff-1111
---

## Review (one original author pass against the acceptance slice)

Executed once after implementation. Boundary: `app.js:755-774` and `test_handoff_read_guidance.py` on the frozen candidate. Outcome: **Residual work**, no blocker, no correction batch started.

| Slice requirement | Evidence | Result |
| --- | --- | --- |
| 403 fixed refusal, existing roles, no refresh/retry advice, manual path via sender/known case | Node 403 case and constructed Chromium 403 (alert, one GET, no retry) | Met |
| Other HTTP failures fixed load-failure copy, no raw text | Node 500/404/429/generic; Chromium 500 | Met |
| Malformed success not shown as empty | Node `{}`/`0` red before, green after; Chromium text and `{}` 200 | Met |
| 401, abort, transport, empty, rows, CSV links, #83 screen unchanged | Existing cases, download UI (6) and waiting-view (10) browser runs, 149 non-browser | Met |
| Manual refresh stays manual and recovers real rows | Chromium reload case with real backend projection | Met |

## Findings routed (none changed in this task)

* R1 (Low): the 403 owner roles are an internal interpretation of who handles role checks; no access process or named person exists, and none is claimed. Wording differs from #83 ("a programme owner"); needs the independent reviewer and the named human wording reviewer.
* R2 (Low): `Could not load handoffs: <message>` remains for the 401 path; the message is the fixed client string, and the sign-in screen replaces the view.
* R3 (Low): a 500 from `pending_handoffs` for a non-staff user (uncaught `PermissionError`) is server behaviour left unchanged by scope; it now reads as a load failure, not a refusal.
* R4 (Info): cold-start `fetchReadRetrying` retry on non-JSON 5xx pre-exists and is untouched; the card code itself adds no retry. 403 and 500 states are constructed responses, not backend-produced.
* R5 (Info): other panels still relay raw `e.message`; universal C3 unproved.

No unresolved blocker. Not established: named-human wording acceptance, assistive-technology or conformance results, hosted CI, independent exact-head review. Refs #153 only.
