<!-- markdownlint-disable-file -->
# Plan: issue-98-denial-interface-1112

Research: [research](../../research/2026-11-12/issue-98-denial-interface-1112-research.md). Details: [details](../../details/2026-11-12/issue-98-denial-interface-1112-details.md).

* [x] Phase 1: failing-first regression `test_changed_open_issue_stales_only_its_field` (both stores) captured before the fix.
* [x] Phase 2: in `form_export.export_freshness`, group saved and current `open_issues` by `field_id`; add fields whose group differs to the stale set; malformed saved issue shape is Invalid, not trusted.
* [x] Phase 3: focused tests (`test_form_*`, API finance screens selector), ruff, mypy; README/log line; changes record.
* [x] Phase 4: single post-implementation Review.

Scope guard: no rule evaluator, no approval fields, no hold semantics change, no web change.

## Amendment 1 (PR 1482 hosted type-check defect; correction cycle 1 of this PR)

Original phases above are unchanged. SourceCI run 43308748514 job 131499109903: configured `mypy` failed on `tests/test_form_export.py:170` and `:172` (`change_metadata`, `batch` not explicitly exported by `test_form_review`). Reproduced locally with pinned mypy 2.4.0 (exit 1, 2 errors, 298 files; evidence `correction1-mypy-before*.out`). The original CI log stays at `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/pr1482-src-core-original-failure-1112.log` and is not duplicated.

* [x] Import `change_metadata` from `dataset` and `batch` from `test_form_staging` (the pattern in `test_form_dependencies.py`); no ignores, casts, re-exports or config change. Production code untouched.
* [x] Validate: configured `mypy` over its full scope, 69 form tests, 20 API finance tests, changed-file ruff check/format; one Review of the final head.
