---
title: Issue 153 staff-time refusal and error guidance details
ms.date: 2026-11-09
task_id: 153-staff-time-copy-1109
task_slug: staff-time-copy-153
---

## Approved copy (pattern: reason. Owner: role. Next action: step.)

Managers means "a manager (Retrofit Programme Manager or Programme Support Officer)". Support means "application support".

### Blocked states (`timeBlockedText(st, manager)`, first matching flag wins)

* `!flag_on`: "Time capture is switched off, so nothing can be recorded. Owner: application support. Next action: ask application support to switch it on when the programme agrees to start staff time capture."
* `!dpia_recorded`: "Time capture cannot start until a data protection impact assessment (DPIA) reference is recorded. Owner: application support. Next action: ask application support to record the DPIA reference in the service settings. It cannot be recorded on this screen."
* `!consultation_recorded`: same shape for "the staff consultation".
* `!notice_approved`: "Time capture cannot start until an approval reference that covers the current staff notice wording is recorded. Owner: application support. Next action: ask application support to record the approval reference for the current notice in the service settings." (No claim that approval is authentic.)
* `!requested`: "A manager has not yet asked for time capture to be enabled. Owner: a manager (...). Next action:" manager: "choose Request enabling (audited) below." else: "ask a manager to request enabling."
* `!activated`: "Enabling was requested by {requested_role} and now needs a manager in a different role. Owner: a manager in a different role from the requester. Next action:" manager: "if that is you and your role differs, choose Enable time capture (audited) below." else: "ask that manager to enable it." (requested_role is rendered as text only.)
* No explaining flag while `enabled` is false: "Time capture is not available and the reason is not shown here. Owner: application support. Next action: refresh this page, then contact application support if it continues."

### Action failures (`timeActionFailureText(error, kind)`, kind is record, request, enable or notice)

* 401: no text (the sign-in screen already shows the reason).
* Validation (record, status 400): "Minutes must be a whole number, for example 15." / "Minutes must be from 1 to 600." / "Choose an activity from the list." / otherwise "Some details were not accepted." each followed by " Nothing was saved. Owner: you. Next action: correct it and choose Save again." Classified by message substring; text is our own.
* Unknown case (record, 404): "That case reference was not found, so nothing was saved. Owner: you. Next action: copy the case reference from the case page and choose Save again."
* 403, recognised pre-write refusals only (critique C1, C5): notice not read -> "Nothing was saved because you have not confirmed that you read the staff notice. Owner: you. Next action: refresh this page, read the notice and choose I have read the notice."; only a manager -> "Nothing was changed because this step is for a manager. Owner: a manager (...). Next action: ask a manager to do it."; no enabling request yet -> "Nothing was changed because enabling needs a request first. Owner: a manager (...). Next action: ask a manager to request enabling, then ask a manager in a different role to enable it."; request made by the same person or role -> "Nothing was changed because a manager in a different role must enable it. Owner: a manager in a different role from the requester. Next action: ask that manager to enable it."; time capture off or not ready (reason text beginning "Time capture ") -> "Nothing was saved because time capture is not available yet. Owner: see the checklist. Next action: refresh this page and follow the checklist." Every other 403 is treated as an unknown outcome because the server can raise one after a write (audit).
* Pending or conflict (409, critique C2): "Another save is still in progress or its result is not known. Owner: you. Next action: wait for it to finish, then refresh this page and check My entries before you save again."
* Unknown outcome (no status, 5xx, unrecognised 403, outcome uncertain or committed): record: "We cannot tell whether this entry was saved. Owner: you. Next action: refresh this page and check My entries (it lists only your latest 200 entries) before you save again, then contact application support if it continues." Other kinds: "We cannot tell whether this change was saved. Owner: application support. Next action: refresh this page and read the checklist before you try again, then contact application support if it continues."
* Any other status: "This could not be completed and the reason is not shown here. Owner: application support. Next action: refresh this page and check the checklist and My entries before you try again."

### Load failure (`timeLoadFailureText(error)`)

* 403 (critique C4): notice not read -> "You have not confirmed that you read the staff notice. Owner: you. Next action: refresh this page, read the notice and choose I have read the notice."; otherwise "Time capture is not available to you right now. Owner: a manager or application support. Next action: refresh this page, then contact application support if it continues." The checklist is not assumed visible.
* Otherwise: "Staff time capture could not load. Owner: application support. Next action: refresh to try again, then contact application support if it continues."

## Edit steps

1. Append the three helpers after `timeView` using plain `Error.status`/`outcome`; no DOM use.
2. Replace `st.reason` (line 9), `error.message` in `save` (line 13, kind passed from the path) and the view catch (line 48). Skip text for 401.
3. Add the test file; keep literal strings in one place (the JS) and assert pattern markers (`Owner:`, `Next action:`) plus case-specific phrases.

## Test matrix

| Case | Layer |
| --- | --- |
| Each blocked flag, manager and non-manager | Node VM |
| 400 x4, 404, 403 x4, unknown outcome (no status, 500, 409, outcome committed), other status | Node VM |
| Unsafe detail `Traceback ... /srv` and `<img onerror>` never in output | Node VM and browser |
| Disabled, missing DPIA, invalid minutes, read failure, ambiguous save | Served browser (opt-in) |
| Ambiguous save, both committed (request passed through, response dropped) and uncommitted (aborted first): the text claims neither and the entry count shows each real outcome | Served browser |
| Mine/report 403 reads, role mismatch refusals, unrecognised 403 treated as unknown, 409 pending | Node VM and browser |
| Banned terms (gate, hold, provenance, trace) and em dashes absent in every output; live region role kept | Node VM and browser |
