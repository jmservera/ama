# Changes: #82 eligibility strict fix

* Rebased onto b630279b4.
* grants.py: new `grant_eligibility` action (Grants and Evidence Officer only, Claimable only); verdict is unknown for missing, malformed, wrong-role or non-independent records (F1, F2); Rejected approval clears eligibility (F3); legacy pending eligibility ignored.
* panels.js: eligibility moved from the propose form to its own officer form.
* Tests: fixtures record eligibility via a distinct Grants Officer; legacy bypass test replaced by blocking tests; new role, independence and rejection tests.
* Validation (/tmp/venv-82c1-1848): core test_gates* 28, test_grant* 62 (22 skipped, SQL), test_finance* 78 (19 skipped), boundary 8 OK; api test_grant* 2, test_finance* 28, test_workflows* 19 OK; ruff and mypy clean (core, api). SQL-backed variants skipped, unobserved.
