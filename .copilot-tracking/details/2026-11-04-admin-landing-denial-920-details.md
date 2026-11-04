# Details: admin-only landing (Refs #920)

* `src/api/src/zava_forward/api/server.py`: add `cases` to `services` in `/api/me`.
* `src/api/src/zava_forward/api/web/app.js`: before the final `listView` route, show "No case work for this account" with `role="status"` text (plain language, no console output, ordinary route back via navigation).
* `src/api/tests/test_expected_denials.py` and `src/api/checks/expected_denials_browser_check.py`: assertions above.
