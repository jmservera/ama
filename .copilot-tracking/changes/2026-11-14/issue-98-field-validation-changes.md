# Issue #98 changes (2026-11-14)

* src/core/.../form_review.py: `_reviewer_confirmed`; unconfirmed values fail validation; attachments carry template_version and input_version.
* src/core/.../form_export.py: fields carry template_version and input_version.
* src/core/tests/test_form_export.py: two new tests.
* Validation: test_form_export, test_form_review, test_form_criteria_5_6, test_form_dependencies (50 OK); api test_form_held_download_api, test_form_staging_api (32 OK); ruff and mypy clean. No discover run, no push.
