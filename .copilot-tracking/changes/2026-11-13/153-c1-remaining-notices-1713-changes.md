# Changes: issue 153 criterion 3 remaining notices

Status: implemented.

* `ops.js`, `assistants.js`, `simulator-control.js`, `staff-intake.js`, `panels.js`: per-file `*Owned` helper (keeps a message that already has `Owner:` before `Next action:`, else appends both); fixed error and blocked literals carry Owner and Next action; dynamic message sinks wrapped. `safetyPanel` and `app.js` untouched.
* `tests/test_content_standard.py`: three tests cover ordered Owner then Next action in literals, dynamic sink wrapping, and runtime helper behaviour in node (complete, partial, incidental, undefined).
* `tests/test_case_journey.py`: extracted-function harness now includes `panelOwned`.

Validation: see the review file. A code-review fix made the helpers status-aware (4xx names the team manager).

Divergences: `data-assistance` attribute strings and `AI assistance unavailable. Work continues manually.` left unchanged because `test_case_journey` asserts them exactly; owner assignments are unreviewed by a named human.
