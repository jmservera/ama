---
title: Issue 222 approval binding changes
ms.date: 2026-11-03
---

## Changes

* `core/cohort_eval.py`: `manifest_digest`, `approve`, lawful-fields owner and digest binding required for approval; blocker text updated.
* Fixtures and ranking run approve after the manifest is final.
* Tests: `test_approval_must_be_complete_and_bound_to_manifest_content`; three existing tests re-approve after edits.
* `agents/README.md`: fail-closed approval note.

## Validation

Run: `test_cohort_eval` (25 OK), `test_cohort_ranking_eval` and `test_cohort_manifest_draft` (31 OK), review_effectiveness tests (20 OK), ruff check and format, mypy for the changed core and agents sources (cache /tmp/mypy-222).

Not run: gate, benchmarks, full suites, hosted CI. No divergences.
