# Research: admin-only landing 403s (Refs #920)

Disposition: reused (prior research 2026-11-04-assistants-denial-920) plus a focused code read. Planning readiness: Ready.

## Already delivered

* PR #929: four responses classified as expected; photo, law alerts and regulatory chat status skipped or worded plainly; Chromium check.
* PR #1017: `/api/assistants` skipped for roles without staff access; `services.assistants` on `/api/me`.
* PR #1006: strict mypy fix.

## Remaining gap

* The prior review recorded that an admin-only account (Application Administrator, no case access) lands on `listView`, which calls `/api/facets` and `/api/cases`. Both return 403 (`projection.allowed` denies kind `facets` and `cases`), so Chrome logs console errors. The browser check did not assert a clean console for that account.

## Classification

* `/api/facets` and `/api/cases` 403 for admin-only: expected denial (role has no case access), avoidable by not requesting.
