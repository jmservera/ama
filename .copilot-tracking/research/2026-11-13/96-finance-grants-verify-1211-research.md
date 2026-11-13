# Research: Issue #96 finance, grants and form-assisted funding evidence unit verification at 3b05143179

Task: `96-finance-grants-verify-1211`. Research disposition: executed. Planning Readiness: Ready.
Docs read: case study original and addendum, knowledge base README, memory (context only).
Tier: Focused (offline unit tests, tracking-only writes). No src/ or docs/ edits.

## Test modules located (excluding browser checks)

Core (`src/core/tests/`):

* test_finance_match_controls.py, test_finance_signoffs.py, test_funding_automation_boundary.py
* test_grant_lifecycle_controls.py, test_chat_case_funding_sources.py
* test_form_staging.py, test_form_review.py, test_form_review_pack.py, test_form_dependencies.py, test_form_export.py
* test_exposure_limits.py (investment envelope, liquidity, downside tolerance, #99)

API (`src/api/tests/`):

* test_finance_match_api.py, test_grant_lifecycle_api.py, test_finance_grants_screens.py
* test_finance_exposure_api.py, test_finance_exposure_screen.py
* test_form_staging_api.py, test_form_held_download_api.py

## Acceptance criteria boundaries (literal, from issues at retrieval)

#96: unchecked: approved versioned schema per form; reviewed export never submits or implies eligibility; source/schema/rule change marks only dependents stale. Checked: candidate lineage, per-field accept/correct/reject, field-specific validation.
#98: unchecked: validation uses approved rules and reviewer-confirmed inputs only; pack links fields, evidence, attachments with template and input versions. Checked: field review isolation, finance review history.
#99: unchecked: envelope and tolerances human-approved inputs not invented; breach produces pause signal for a human decision.

Unit test passes are engineering evidence only. They do not satisfy human, Finance, FD01-FD14, OD12/15, legal or submission approvals, and prove no eligibility.

## Plan readiness

Offline run in a /tmp venv with editable installs; MSSQL and browser tests expected to skip. Ready.
