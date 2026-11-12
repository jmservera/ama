<!-- markdownlint-disable-file -->
# Details: issue-98-denial-interface-1112

## Phase 2

File `src/core/src/zava_forward/core/form_export.py`, `export_freshness`.

* Inside the integrity `try`, build `saved_issues` by `field_id` from `body["open_issues"]`; `KeyError`, `TypeError`, `AttributeError` or `ValueError` mark the copy Invalid.
* After `draft_export`, build `current_issues` the same way from `current["open_issues"]`.
* `changed` also contains every field id whose issue list differs between the two maps (added, removed or altered). Existing reasons stay; the "A bound source or field state changed." reason applies when no schema/input reason exists.
* Unchanged behavior: Invalid, Unavailable, schema/input reasons, `unaffected_fields`, `reviewed=False`.

Success: new test passes on both stores; the 67 existing form tests still pass; ruff and mypy clean on touched files.
