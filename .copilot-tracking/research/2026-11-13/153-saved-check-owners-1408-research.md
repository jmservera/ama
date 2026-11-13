# Research: #153 AC3 owners in saved-check errors

Disposition: executed. Planning Readiness: Ready.

* role-screens.js:1376 HELD_CHECK_ERRORS: 400, 404, 409, 502 lack `Owner:`; 403 and HELD_CHECK_NOT_RUN have it.
* content-standard.md line 40: Owner is a named person or role, never "unassigned".
* test_content_standard.py BANNED regex bans gate/hold/provenance/trace/snapshot/envelope words.
* Owner wording: 400/409 the signed-in reviewer; 404/502 application support (matches HELD_CHECK_NOT_RUN).
