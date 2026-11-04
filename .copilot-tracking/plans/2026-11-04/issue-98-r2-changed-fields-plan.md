<!-- markdownlint-disable-file -->
# Plan: issue-98-r2-changed-fields

* [x] Phase 1: add `changed_fields` in `form_review._freshness` (type-aware compare of value, state).
* [x] Phase 2: extend `test_input_and_schema_changes_stale_saved_manifests` and the source-only test; README line; log entry.
* [x] Phase 3: focused tests, ruff, mypy (`--cache-dir=/tmp/mypy-98`).

Critique (single, by implementing agent): compatible. Risk: an unreviewed field compared as Unknown/None on both sides is unchanged, correct. Not a security, SQL, infrastructure or deployment change.
