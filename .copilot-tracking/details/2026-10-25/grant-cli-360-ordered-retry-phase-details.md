# Phase details: grant CLI ordered retry (issue 360)

Date: 2026-10-25. Prospective; written before execution, after the research and plan.

## Phase 1: tests
File `infra/tests/test_grant_application_admin.py`, class `GrantCliTests`, next to `test_apply_refuses_an_unsafe_profile_before_any_az_call`.
* `test_apply_refuses_a_symlinked_profile`: create a real 0700 directory and a symlink to it in a temporary parent; pass the symlink as `--tenant-profile` with `--apply`; expect exit 1, "refused:" on stderr, no az calls recorded by `OfflineAz`.
* `test_apply_refuses_an_in_repo_profile`: use a 0700 temporary directory created under `setup.REPO` and removed in cleanup (path is under the checkout but is deleted by the test, never left behind); expect the same outcome.
* Reuse the existing `cli()` helper and `OfflineAz` call recorder; no new abstraction, no live call.

## Phase 2: validation
* `python3 -m unittest infra.tests.test_grant_application_admin` equivalent used by the repo for this file; all tests must pass.
* Confirm the new tests are not vacuous by running them against a scratch copy of the script outside the repository where `private_path` is bypassed; expect failure. The candidate file is not edited for this.

## Phase 3: record, review, gate
* Changes file for 2026-10-25 listing exactly what changed.
* Independent review (one record) of requirement, candidate and these phase artifacts.
* Commit with the privacy noreply identity and Copilot trailer; full `tools/rpi-checks.py --all` into a new external directory; `--verify-receipt`; push same branch; PR453 stays DRAFT.

## Rollback
Revert only the retry commit; earlier commits are untouched.

## Amendment after critique (before execution)
* Phase 1 now adds ONE test, `test_apply_refuses_a_symlinked_profile`, with target and symlink both created outside the repository.
* The in-repo test and the scratch-copy mutation check are removed. Sensitivity check: temporarily patch `setup.private_path` inside a throwaway test run (mock to return the path unchecked) via an ad hoc command, not committed, and expect the new test to fail.
