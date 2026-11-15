---
title: Issue 96 criteria 5 and 6 changes
description: Implemented changes and validation evidence (Refs #96)
ms.date: 2026-11-13
---

## Changes

* `src/core/tests/test_form_criteria_5_6.py` (new): whole-store no-write and Held-metadata proof for a fully reviewed export; baseline-to-after selectivity for source, per-field rule (calculation reference) and schema changes across proposals, approvals and saved export freshness.
* `src/api/src/zava_forward/api/server.py`: read-only `GET /api/cases/{case}/form-review/{draft}/proposal-freshness` exposing the existing `form_review.proposal_freshness` (gap G1); same authorisation as the form review, `Cache-Control: private, no-store`. The review view is unchanged because critique evidence showed adding proposals there adds source reads and breaks read-once tests.
* `src/api/src/zava_forward/api/web/role-screens.js`: funding panel loads the freshness per draft and shows "Proposals to check again" and "Approvals to review again", with explicit Unknown copy when unreadable or unscoped.
* Tests: two HTTP end-to-end tests in `test_form_held_download_api.py` (criterion 5 and 6, failing first without the route), one UI test in `test_finance_grants_screens.py`, endpoint inventory entry.

## Divergences from plan

* P3 view change replaced by the endpoint (tests showed the view contract reads each source once per report).
* Rule-reference changes stay form-wide and calculation inputs stay conservatively dependent (PC-001); documented, not narrowed.

## Validation (pip venv `/tmp/venv-96se-2035`, removed before commit)

* Core `test_form*.py` 73 OK; API form, content standard, accessibility baseline, finance, role, grant suites OK.
* `ruff check`, `ruff format --check` on src/core and src/api; `mypy` in both projects: clean.
* Not run: Playwright browser checks, full local gate, hosted CI. Not claimed: criteria 5 and 6 acceptance closure; the issue stays open.
