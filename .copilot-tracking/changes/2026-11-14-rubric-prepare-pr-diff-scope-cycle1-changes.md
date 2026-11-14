# Cycle 1 correction: rubric prepare PR diff scope (Refs #198)

Original RPI artifacts are unchanged.

* Review failure: `test_given_pr_deleting_scored_file_when_gated_then_drop_counts` hard-coded total 64, but the recorded baseline in `.github/rubric/scores/latest.json` totals 79.
* Fix: `test_prepare.py` derives the expected total from the seed (`SEED["total"]` minus the A2 drop of 2), giving 77.
* Lint: removed two unused `noqa: E402` directives flagged by ruff RUF100.
* `prepare.py` behaviour is unchanged. Workflows, `artifacts.json` and `scores/*` untouched.
* Validation: `python3 -m pytest .github/rubric/scripts/test_prepare.py -q` gives 76 passed; `ruff check` on both scripts passes.
