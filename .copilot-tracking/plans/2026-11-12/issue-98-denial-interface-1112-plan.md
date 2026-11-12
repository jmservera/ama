<!-- markdownlint-disable-file -->
# Plan: issue-98-denial-interface-1112

Research: [research](../../research/2026-11-12/issue-98-denial-interface-1112-research.md). Details: [details](../../details/2026-11-12/issue-98-denial-interface-1112-details.md).

* [x] Phase 1: failing-first regression `test_changed_open_issue_stales_only_its_field` (both stores) captured before the fix.
* [x] Phase 2: in `form_export.export_freshness`, group saved and current `open_issues` by `field_id`; add fields whose group differs to the stale set; malformed saved issue shape is Invalid, not trusted.
* [x] Phase 3: focused tests (`test_form_*`, API finance screens selector), ruff, mypy; README/log line; changes record.
* [x] Phase 4: single post-implementation Review.

Scope guard: no rule evaluator, no approval fields, no hold semantics change, no web change.
