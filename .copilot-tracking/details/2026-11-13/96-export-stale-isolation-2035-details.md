---
title: Issue 96 criteria 5 and 6 phase details
description: File-level steps and checks for the plan
ms.date: 2026-11-13
---

## P2 and P3

* `src/core/tests/test_form_criteria_5_6.py`: add a test that `form_review.view` drafts carry `dependency_impact.proposals` equal to `proposal_freshness` proposals; after a source change only the dependent candidate is Stale.
* `src/api/tests/test_form_held_download_api.py` (or the staging API file): over HTTP, `GET /api/cases/ZF-1/form-review` returns the same list; an unrelated document and another case's document change leave all Current.
* `form_review.view`: after `_report`, set `report["dependency_impact"]["proposals"] = _proposals(store, case, draft, impact)` where `impact` is the report's schema impact. Read-only.

## P4

* `role-screens.js` `fundingDraftPanel`: two rows listing field names whose proposals are not Current and approvals in Review required, "None recorded" otherwise; plain words, no gate, hold, provenance, trace, snapshot or envelope.

## P5

* HTTP test: Held export headers and body notice, state before and after unchanged, then source/schema changes through the API view and freshness endpoint stay selective.

## Validation

`unittest` for form tests in `src/core` and `src/api`, content standard, role screens, finance grants screens, accessibility baseline; `ruff check`, `ruff format --check`, `mypy` in each project.
