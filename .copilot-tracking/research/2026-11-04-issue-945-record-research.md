# Research: issue 945 recheck

* Merged PR 985 (Refs #945) delivered the fix in src/api/src/zava_forward/api/web/app.js: tileNote is written only when the text differs, errors are counted per Leaflet load cycle, and the note clears after a clean load.
* Verified on main at 281d4b0e8: lines 1921-1926 of app.js and test_tile_failure_note_is_written_once_and_clears_after_a_clean_load in src/api/tests/test_ui_support.py.
* Criteria 1 and 2 are met in code and string tests only. Criterion 3 (list pointer retained) is met and asserted.
* Unmet: observation in a real browser and with assistive technology. That is a human step; no code slice remains.
* Planning readiness: Ready for a docs-only record.
