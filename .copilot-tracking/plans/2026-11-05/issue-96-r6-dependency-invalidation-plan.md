<!-- markdownlint-disable-file -->
# Plan: issue-96-r6-dependency-invalidation

* [x] Phase 1: `forms.schema_impact` (exact definition diff, form-wide references, condition closure, undeclared calculation inputs, lineage failure) in `src/core/src/zava_forward/core/forms.py`.
* [x] Phase 2: `form_review._report` uses the impact for per-field staleness; adds read-only `dependency_impact` (schema impact, proposal freshness, approval-reference review-required); manifest freshness uses the impact; `form_export` carries the impact outside the hashed body and uses it in `export_freshness`.
* [x] Phase 3: focused behavioural tests (new `test_form_dependencies.py`) and amendment of tests that assumed all-or-nothing schema staleness.
* [x] Phase 4: README note, knowledge-base log entry, focused validation, FULL tier admission attempt.

Details: [details](../../details/2026-11-05/issue-96-r6-dependency-invalidation-details.md). Critique: [critique](../../reviews/plans/2026-11-05/issue-96-r6-dependency-invalidation-critique.md). Research: [research](../../research/2026-11-05/issue-96-r6-dependency-invalidation-research.md).

Out of scope: approved schema, reviewed export, approved rule evaluation, any write path for approvals, API/web, Azure.
