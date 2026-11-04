<!-- markdownlint-disable-file -->
# Details: issue 946

## Phase 1

* In `_hazard_receiver`, replace the single `or` condition with: if released and not `allow_released`, raise "This safety issue's retrofit hold has already been released."; then if no `referral_version`, raise the existing referral message.

## Phase 2

* Add `test_receiver_error_names_the_failing_condition` to `JsonHazardReferral` (inherited by `SqlHazardReferral`): unreferred report gives the referral message; after referral, acceptance, repair and release by the independent accountable role, receipt gives the released message (exact text).

## Phase 3

* `PYTHONPATH=<worktree src dirs> python3 -m unittest discover -s tests -p test_hazard_referral.py` from `src/core`; ruff check; mypy strict with `--cache-dir=/tmp/mypy-946`.
