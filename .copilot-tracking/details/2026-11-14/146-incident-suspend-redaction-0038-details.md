---
title: Issue 146 incident suspension and diagnostic redaction details
date: 2026-11-14
task_slug: 146-incident-suspend-redaction-0038
---

## Phase 1

* `SENSITIVE` (public) adds: dotted emails, Basic auth, UK phone, UK postcode, NI number, `sk-` keys,
  32+ hex, 40+ base64 runs and key/value pairs for secrets (`api-key`, `sig`, `sv`, `token`, `password`,
  `AccountKey`, `authorization` with optional scheme) and identifiers (`uprn`, `resident_ref`,
  `household_ref`, `tenant_id`, `name`, `address`, `postcode`, `phone`, `email`).
* `_TRACEBACK` and `_EXCEPTION_TEXT` keep the exception class and drop its message or repr.
* `_mask` replaces matches with `<redacted>` plus `%.0s` for swallowed placeholders so logging never raises.
* `monitoring_coverage._SENSITIVE` now aliases `SENSITIVE`.

## Phase 2 and 3

* `test_diagnostic_logging.py`: three tests. `test_operator_suspension.py`: one end-to-end test using
  `reconcile_events`, `evaluate_indicator` (approved threshold), ownerless refusal, task-scoped suspend,
  manual call logging, reopen, unauthorised restart refusal.

## Phase 4

Commands: `ruff check`, `ruff format --check`, `mypy` per project; `unittest discover` per project.
