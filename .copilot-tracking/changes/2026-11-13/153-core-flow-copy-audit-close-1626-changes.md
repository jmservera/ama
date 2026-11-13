# Changes: issue 153 copy audit close

* `web/progress.js`: reworded "holds" to "contains"; failed-read message now names owner and next action.
* `web/chat.js`: unavailable, could-not-load, proposal, usage, alert, doubt, lookup and inbox failures state owner and next action.
* `web/aftercare.js`: unconfirmed save, earlier attempt, role-denied, read-only and server-refusal messages state owner and next action.
* `web/async-action.js`: shared failure notice is outcome-aware and names owner and next action.
* `tests/test_content_standard.py`: all served scripts and pages audited (completeness test); composed error messages checked for reason, owner and next action.
* `safetyPanel` in app.js and `role-screens.js` untouched.

Follow-up (not in this task): `app.js`, `ops.js`, `assistants.js`, `simulator-control.js`, `staff-intake.js` still show several `${error.message}` notices without an explicit Owner label.
